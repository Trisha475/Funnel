import pandas as pd
from typing import Dict, List, Any

class FunnelAnalyzer:
    """
    Analyzes funnel data to identify drop-offs and calculate conversion rates
    """
    
    def __init__(self):
        self.funnel_stages = ['Visitor', 'Lead', 'MQL', 'SQL']
    
    def analyze_funnel(self, funnel_data: Dict[str, int], threshold: float) -> Dict[str, Any]:
        """
        Analyze funnel data and identify problematic stages
        
        Args:
            funnel_data: Dictionary with stage names as keys and counts as values
            threshold: Drop-off threshold percentage (30-40)
            
        Returns:
            Dictionary containing analysis results
        """
        stages = list(funnel_data.keys())
        values = list(funnel_data.values())
        
        # Calculate conversion rates and drop-offs
        stage_analysis = []
        problematic_stages = []
        
        for i, stage in enumerate(stages):
            if i == 0:
                # First stage (Visitor) - baseline
                conversion_rate = 100.0
                drop_off = 0.0
            else:
                # Calculate conversion rate from previous stage
                conversion_rate = (values[i] / values[i-1]) * 100
                drop_off = 100 - conversion_rate
                
                # Check if drop-off exceeds threshold
                if drop_off > threshold:
                    problematic_stages.append(stage)
            
            stage_analysis.append({
                'Stage': stage,
                'Count': values[i],
                'Conversion Rate (%)': round(conversion_rate, 1),
                'Drop-off (%)': round(drop_off, 1),
                'Status': '🔴 Needs Attention' if stage in problematic_stages else '🟢 Healthy'
            })
        
        # Calculate overall funnel health
        overall_conversion = (values[-1] / values[0]) * 100
        
        # Identify biggest drop-off
        biggest_drop_stage = None
        biggest_drop_value = 0
        
        for i in range(1, len(stage_analysis)):
            if stage_analysis[i]['Drop-off (%)'] > biggest_drop_value:
                biggest_drop_value = stage_analysis[i]['Drop-off (%)']
                biggest_drop_stage = stage_analysis[i]['Stage']
        
        return {
            'stage_analysis': stage_analysis,
            'problematic_stages': problematic_stages,
            'overall_conversion': overall_conversion,
            'biggest_drop_stage': biggest_drop_stage,
            'biggest_drop_value': biggest_drop_value,
            'threshold_used': threshold,
            'total_visitors': values[0],
            'final_conversions': values[-1]
        }
    
    def calculate_potential_impact(self, analysis_results: Dict[str, Any]) -> Dict[str, Any]:
        """
        Calculate potential impact of fixing problematic stages
        
        Args:
            analysis_results: Results from analyze_funnel method
            
        Returns:
            Dictionary with potential impact calculations
        """
        stage_analysis = analysis_results['stage_analysis']
        problematic_stages = analysis_results['problematic_stages']
        
        impact_analysis = {}
        
        for stage_data in stage_analysis:
            if stage_data['Stage'] in problematic_stages:
                current_count = stage_data['Count']
                
                # Calculate potential if drop-off was reduced to threshold
                threshold = analysis_results['threshold_used']
                improved_conversion = (100 - threshold) / 100
                
                # Find previous stage count
                prev_stage_index = None
                for i, s in enumerate(stage_analysis):
                    if s['Stage'] == stage_data['Stage']:
                        prev_stage_index = i - 1
                        break
                
                if prev_stage_index is not None and prev_stage_index >= 0:
                    prev_count = stage_analysis[prev_stage_index]['Count']
                    potential_count = int(prev_count * improved_conversion)
                    potential_increase = potential_count - current_count
                    
                    impact_analysis[stage_data['Stage']] = {
                        'current_count': current_count,
                        'potential_count': potential_count,
                        'potential_increase': potential_increase,
                        'improvement_percentage': ((potential_increase / current_count) * 100) if current_count > 0 else 0
                    }
        
        return impact_analysis
    
    def get_benchmark_comparison(self, analysis_results: Dict[str, Any]) -> Dict[str, Any]:
        """
        Compare funnel performance against industry benchmarks
        
        Args:
            analysis_results: Results from analyze_funnel method
            
        Returns:
            Dictionary with benchmark comparisons
        """
        # Industry benchmark conversion rates (these are typical B2B SaaS benchmarks)
        benchmarks = {
            'Visitor to Lead': 2.0,  # 2% of visitors become leads
            'Lead to MQL': 50.0,     # 50% of leads become MQLs
            'MQL to SQL': 40.0,      # 40% of MQLs become SQLs
            'Overall': 0.4           # 0.4% overall conversion
        }
        
        stage_analysis = analysis_results['stage_analysis']
        
        # Calculate actual conversion rates
        actual_rates = {}
        for i in range(1, len(stage_analysis)):
            prev_stage = stage_analysis[i-1]['Stage']
            current_stage = stage_analysis[i]['Stage']
            stage_key = f"{prev_stage} to {current_stage}"
            actual_rates[stage_key] = stage_analysis[i]['Conversion Rate (%)']
        
        # Overall conversion rate
        actual_rates['Overall'] = analysis_results['overall_conversion']
        
        # Compare with benchmarks
        comparison = {}
        for stage, actual_rate in actual_rates.items():
            if stage in benchmarks:
                benchmark_rate = benchmarks[stage]
                performance = "Above" if actual_rate > benchmark_rate else "Below"
                difference = actual_rate - benchmark_rate
                
                comparison[stage] = {
                    'actual': actual_rate,
                    'benchmark': benchmark_rate,
                    'performance': performance,
                    'difference': difference
                }
        
        return comparison
