import random
import pandas as pd
from typing import Dict, List
from datetime import datetime, timedelta

class DataGenerator:
    """
    Generates realistic funnel data for analysis
    """
    
    def __init__(self):
        self.traffic_multipliers = {
            'Google Ads': 1.2,
            'Facebook Ads': 1.0,
            'Organic': 0.8,
            'Direct': 0.6,
            'Email': 0.4
        }
        
        self.time_multipliers = {
            'Last 7 Days': 0.3,
            'Last 30 Days': 1.0,
            'Last 90 Days': 2.8
        }
    
    def generate_funnel_data(self, time_period: str = "Last 30 Days", 
                           traffic_sources: List[str] = None) -> Dict[str, int]:
        """
        Generate realistic funnel data based on time period and traffic sources
        
        Args:
            time_period: Time period for analysis
            traffic_sources: List of traffic sources to include
            
        Returns:
            Dictionary with funnel stage counts
        """
        if traffic_sources is None:
            traffic_sources = ['Google Ads', 'Facebook Ads']
        
        # Base visitor count
        base_visitors = 1000
        
        # Apply time period multiplier
        time_multiplier = self.time_multipliers.get(time_period, 1.0)
        
        # Apply traffic source multipliers
        traffic_multiplier = sum(self.traffic_multipliers.get(source, 1.0) for source in traffic_sources) / len(traffic_sources)
        
        # Calculate total visitors
        total_visitors = int(base_visitors * time_multiplier * traffic_multiplier)
        
        # Add some randomness (±20%)
        randomness = random.uniform(0.8, 1.2)
        total_visitors = int(total_visitors * randomness)
        
        # Generate funnel with realistic drop-offs
        funnel_data = self._generate_realistic_funnel(total_visitors)
        
        return funnel_data
    
    def _generate_realistic_funnel(self, visitors: int) -> Dict[str, int]:
        """
        Generate realistic funnel conversion rates
        
        Args:
            visitors: Total number of visitors
            
        Returns:
            Dictionary with stage counts
        """
        # Define realistic conversion rate ranges
        conversion_ranges = {
            'Visitor_to_Lead': (0.015, 0.035),    # 1.5% - 3.5%
            'Lead_to_MQL': (0.40, 0.65),          # 40% - 65%
            'MQL_to_SQL': (0.25, 0.50)            # 25% - 50%
        }
        
        # Generate conversion rates with some variability
        visitor_to_lead_rate = random.uniform(*conversion_ranges['Visitor_to_Lead'])
        lead_to_mql_rate = random.uniform(*conversion_ranges['Lead_to_MQL'])
        mql_to_sql_rate = random.uniform(*conversion_ranges['MQL_to_SQL'])
        
        # Occasionally create problematic stages (for demo purposes)
        if random.random() < 0.3:  # 30% chance of having a problematic stage
            problematic_stage = random.choice(['Lead_to_MQL', 'MQL_to_SQL'])
            if problematic_stage == 'Lead_to_MQL':
                lead_to_mql_rate = random.uniform(0.20, 0.35)  # Lower conversion
            else:
                mql_to_sql_rate = random.uniform(0.15, 0.30)   # Lower conversion
        
        # Calculate stage counts
        leads = int(visitors * visitor_to_lead_rate)
        mqls = int(leads * lead_to_mql_rate)
        sqls = int(mqls * mql_to_sql_rate)
        
        # Ensure minimum counts
        leads = max(1, leads)
        mqls = max(1, mqls)
        sqls = max(1, sqls)
        
        return {
            'Visitor': visitors,
            'Lead': leads,
            'MQL': mqls,
            'SQL': sqls
        }
    
    def generate_historical_data(self, days: int = 30) -> pd.DataFrame:
        """
        Generate historical funnel data for trend analysis
        
        Args:
            days: Number of days of historical data
            
        Returns:
            DataFrame with daily funnel data
        """
        historical_data = []
        
        for i in range(days):
            date = datetime.now() - timedelta(days=days-i)
            
            # Generate daily data with some trends
            base_visitors = random.randint(800, 1200)
            
            # Add weekly patterns (higher on weekdays)
            if date.weekday() < 5:  # Monday to Friday
                base_visitors = int(base_visitors * 1.1)
            
            daily_funnel = self._generate_realistic_funnel(base_visitors)
            
            for stage, count in daily_funnel.items():
                historical_data.append({
                    'date': date.strftime('%Y-%m-%d'),
                    'stage': stage,
                    'count': count
                })
        
        return pd.DataFrame(historical_data)
    
    def generate_traffic_source_breakdown(self, funnel_data: Dict[str, int], 
                                        traffic_sources: List[str]) -> Dict[str, Dict[str, int]]:
        """
        Generate traffic source breakdown for funnel data
        
        Args:
            funnel_data: Main funnel data
            traffic_sources: List of traffic sources
            
        Returns:
            Dictionary with traffic source breakdown
        """
        breakdown = {}
        
        for source in traffic_sources:
            # Generate percentage for this source
            if source == 'Google Ads':
                percentage = random.uniform(0.4, 0.6)
            elif source == 'Facebook Ads':
                percentage = random.uniform(0.2, 0.4)
            elif source == 'Organic':
                percentage = random.uniform(0.1, 0.3)
            elif source == 'Direct':
                percentage = random.uniform(0.05, 0.2)
            elif source == 'Email':
                percentage = random.uniform(0.02, 0.1)
            else:
                percentage = random.uniform(0.05, 0.15)
            
            # Calculate counts for this source
            source_data = {}
            for stage, count in funnel_data.items():
                source_count = int(count * percentage)
                source_data[stage] = max(1, source_count)  # Ensure minimum of 1
            
            breakdown[source] = source_data
        
        return breakdown
