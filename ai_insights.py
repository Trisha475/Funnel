import json
import os
from typing import Dict, List, Any, Optional
from openai import OpenAI

class AIInsights:
    """
    Generates AI-powered insights and recommendations using OpenAI GPT-4
    """
    
    def __init__(self):
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        if self.openai_api_key:
            self.client = OpenAI(api_key=self.openai_api_key)
        else:
            self.client = None
    
    def generate_insights(self, analysis_results: Dict[str, Any], 
                         funnel_data: Dict[str, int]) -> Optional[Dict[str, Any]]:
        """
        Generate AI-powered insights and recommendations
        
        Args:
            analysis_results: Results from funnel analysis
            funnel_data: Raw funnel data
            
        Returns:
            Dictionary with AI insights or None if API unavailable
        """
        if not self.client:
            return None
        
        try:
            # Prepare data for AI analysis
            context = self._prepare_context(analysis_results, funnel_data)
            
            # Generate insights using GPT-4
            response = self.client.chat.completions.create(
                model="gpt-4o",  # the newest OpenAI model is "gpt-4o" which was released May 13, 2024. do not change this unless explicitly requested by the user
                messages=[
                    {
                        "role": "system",
                        "content": """You are an expert marketing analytics consultant specializing in conversion funnel optimization. 
                        Your task is to analyze funnel data and provide actionable insights for marketing teams.
                        
                        Provide analysis in JSON format with the following structure:
                        {
                            "summary": "Executive summary of funnel performance",
                            "recommendations": ["List of specific actionable recommendations"],
                            "priorities": ["List of optimization priorities in order of impact"],
                            "insights": {
                                "key_findings": ["Key insights from the data"],
                                "opportunities": ["Specific opportunities identified"],
                                "risks": ["Potential risks or concerns"]
                            }
                        }
                        
                        Focus on practical, implementable recommendations that marketing teams can act on immediately."""
                    },
                    {
                        "role": "user",
                        "content": f"Analyze this funnel data and provide insights:\n\n{context}"
                    }
                ],
                response_format={"type": "json_object"},
                max_tokens=2000,
                temperature=0.7
            )
            
            # Parse and return insights
            insights = json.loads(response.choices[0].message.content)
            return insights
            
        except Exception as e:
            print(f"Error generating AI insights: {e}")
            return None
    
    def _prepare_context(self, analysis_results: Dict[str, Any], 
                        funnel_data: Dict[str, int]) -> str:
        """
        Prepare context string for AI analysis
        
        Args:
            analysis_results: Analysis results
            funnel_data: Raw funnel data
            
        Returns:
            Formatted context string
        """
        context = f"""
FUNNEL PERFORMANCE ANALYSIS

Raw Data:
{json.dumps(funnel_data, indent=2)}

Analysis Results:
- Overall Conversion Rate: {analysis_results['overall_conversion']:.1f}%
- Total Visitors: {analysis_results['total_visitors']:,}
- Final Conversions: {analysis_results['final_conversions']:,}
- Drop-off Threshold Used: {analysis_results['threshold_used']}%
- Problematic Stages: {len(analysis_results['problematic_stages'])}

Stage-by-Stage Performance:
"""
        
        for stage_data in analysis_results['stage_analysis']:
            context += f"- {stage_data['Stage']}: {stage_data['Count']:,} visitors, {stage_data['Conversion Rate (%)']:.1f}% conversion, {stage_data['Drop-off (%)']:.1f}% drop-off\n"
        
        if analysis_results['problematic_stages']:
            context += f"\nProblematic Stages Identified:\n"
            for stage in analysis_results['problematic_stages']:
                context += f"- {stage}: Exceeds {analysis_results['threshold_used']}% drop-off threshold\n"
        
        if analysis_results['biggest_drop_stage']:
            context += f"\nBiggest Drop-off: {analysis_results['biggest_drop_stage']} ({analysis_results['biggest_drop_value']:.1f}%)\n"
        
        context += "\nPlease provide specific, actionable recommendations for improving conversion rates and reducing drop-offs."
        
        return context
    
    def generate_optimization_plan(self, insights: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate a structured optimization plan based on insights
        
        Args:
            insights: AI-generated insights
            
        Returns:
            Structured optimization plan
        """
        if not insights:
            return {}
        
        plan = {
            "immediate_actions": [],
            "short_term_goals": [],
            "long_term_strategy": [],
            "kpis_to_track": []
        }
        
        # Extract recommendations and categorize them
        recommendations = insights.get('recommendations', [])
        
        for rec in recommendations:
            if any(keyword in rec.lower() for keyword in ['immediately', 'urgent', 'asap', 'critical']):
                plan["immediate_actions"].append(rec)
            elif any(keyword in rec.lower() for keyword in ['test', 'optimize', 'improve', 'enhance']):
                plan["short_term_goals"].append(rec)
            else:
                plan["long_term_strategy"].append(rec)
        
        # Add relevant KPIs
        plan["kpis_to_track"] = [
            "Conversion rate by stage",
            "Drop-off percentage",
            "Time to convert",
            "Cost per conversion",
            "Lead quality score"
        ]
        
        return plan
    
    def generate_executive_summary(self, analysis_results: Dict[str, Any], 
                                 insights: Dict[str, Any]) -> str:
        """
        Generate executive summary for stakeholders
        
        Args:
            analysis_results: Analysis results
            insights: AI insights
            
        Returns:
            Executive summary string
        """
        summary = f"""
FUNNEL PERFORMANCE EXECUTIVE SUMMARY

OVERVIEW:
• Total Visitors: {analysis_results['total_visitors']:,}
• Final Conversions: {analysis_results['final_conversions']:,}
• Overall Conversion Rate: {analysis_results['overall_conversion']:.1f}%
• Issues Identified: {len(analysis_results['problematic_stages'])} problematic stages

PERFORMANCE STATUS:
"""
        
        if analysis_results['overall_conversion'] > 1.0:
            summary += "🟢 HEALTHY - Conversion rate above 1%\n"
        elif analysis_results['overall_conversion'] > 0.5:
            summary += "🟡 MODERATE - Conversion rate needs improvement\n"
        else:
            summary += "🔴 CRITICAL - Conversion rate below 0.5%\n"
        
        if analysis_results['problematic_stages']:
            summary += f"\nCRITICAL ISSUES:\n"
            for stage in analysis_results['problematic_stages']:
                summary += f"• {stage} stage showing excessive drop-off\n"
        
        if insights and 'recommendations' in insights:
            summary += f"\nTOP RECOMMENDATIONS:\n"
            for i, rec in enumerate(insights['recommendations'][:3], 1):
                summary += f"{i}. {rec}\n"
        
        summary += f"\nNEXT STEPS:\n"
        summary += "• Review detailed analysis in dashboard\n"
        summary += "• Implement high-priority recommendations\n"
        summary += "• Monitor conversion rates daily\n"
        summary += "• Schedule weekly funnel review meetings\n"
        
        return summary
