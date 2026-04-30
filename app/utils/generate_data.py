import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import os
from loguru import logger

def generate_enterprise_data(num_years=2.5):
    logger.info(f"Generating {num_years} years of enterprise operational data...")
    num_days = int(365 * num_years)
    start_date = datetime.now() - timedelta(days=num_days)
    
    regions = ['North America', 'EMEA', 'APAC', 'LATAM']
    departments = ['Sales', 'Manufacturing', 'Logistics', 'Marketing', 'Customer Support']
    
    data = []
    
    # Base trends
    revenue_trend = np.linspace(5000, 15000, num_days) # Growing business
    
    for i in range(num_days):
        date = start_date + timedelta(days=i)
        month = date.month
        day_of_week = date.weekday() # 0-6
        
        # Seasonality factors
        q4_boost = 1.5 if month in [10, 11, 12] else 1.0
        weekend_slowdown = 0.6 if day_of_week >= 5 else 1.0
        
        for region in regions:
            # Regional variance
            reg_factor = {'North America': 1.2, 'EMEA': 1.0, 'APAC': 1.1, 'LATAM': 0.8}.get(region)
            
            for dept in departments:
                # Core metrics
                base_rev = revenue_trend[i] * reg_factor * q4_boost * weekend_slowdown
                
                if dept == 'Sales':
                    revenue = base_rev + random.uniform(-1000, 1000)
                    units_sold = int(revenue / random.uniform(50, 80))
                else:
                    revenue = 0
                    units_sold = 0
                
                # Costs with inefficiencies
                costs = (base_rev * 0.4) + random.uniform(1000, 3000)
                if i % 100 == 0: # Random cost spike (anomaly)
                    costs *= 2.5
                
                # New metrics
                inventory_level = random.randint(500, 2000) - (units_sold if dept == 'Sales' else 0)
                logistics_delay = random.uniform(0.5, 5.0) if region == 'LATAM' else random.uniform(0.1, 2.0)
                productivity_score = random.uniform(70, 95) + (np.sin(i/50) * 5) # Cyclic productivity
                
                headcount = random.randint(20, 100)
                
                data.append({
                    'date': date.strftime('%Y-%m-%d'),
                    'region': region,
                    'department': dept,
                    'revenue': round(max(0, revenue), 2),
                    'costs': round(max(0, costs), 2),
                    'units_sold': units_sold,
                    'inventory_level': max(0, inventory_level),
                    'logistics_delay_days': round(logistics_delay, 2),
                    'employee_productivity': round(productivity_score, 2),
                    'headcount': headcount,
                    'status': 'Active' if random.random() > 0.05 else 'Maintenance'
                })
                
    df = pd.DataFrame(data)
    os.makedirs('data', exist_ok=True)
    df.to_csv('data/enterprise_operations.csv', index=False)
    logger.success(f"Generated {len(df)} records in data/enterprise_operations.csv")

if __name__ == "__main__":
    generate_enterprise_data()
