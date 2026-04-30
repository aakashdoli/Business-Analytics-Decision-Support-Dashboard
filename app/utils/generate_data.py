import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import os
from loguru import logger

def generate_enterprise_data(num_years=3):
    logger.info(f"Generating {num_years} years of highly realistic enterprise operational data...")
    num_days = int(365 * num_years)
    start_date = datetime.now() - timedelta(days=num_days)
    
    regions = ['North America', 'EMEA', 'APAC', 'LATAM']
    departments = ['Sales', 'Manufacturing', 'Logistics', 'Marketing', 'Customer Support', 'Operations']
    
    data = []
    
    # Base macro-economic trend (overall growth with some cycle)
    base_trend = np.linspace(50000, 120000, num_days)
    macro_cycle = np.sin(np.linspace(0, 4 * np.pi, num_days)) * 5000
    daily_base_revenue = base_trend + macro_cycle
    
    for i in range(num_days):
        date = start_date + timedelta(days=i)
        month = date.month
        day_of_week = date.weekday()
        
        # Seasonality: Strong Q4, Slow Summer (July/Aug)
        seasonality_factor = 1.0
        if month in [11, 12]:
            seasonality_factor = 1.35
        elif month in [7, 8]:
            seasonality_factor = 0.85
            
        # Weekend drop for enterprise B2B
        weekend_factor = 0.3 if day_of_week >= 5 else 1.0
        
        # Daily Anomaly Injection (e.g., flash crash, viral marketing)
        is_anomaly = random.random() < 0.02
        anomaly_multiplier = random.uniform(0.5, 2.0) if is_anomaly else 1.0
        
        for region in regions:
            reg_factor = {'North America': 1.0, 'EMEA': 0.8, 'APAC': 0.9, 'LATAM': 0.4}.get(region)
            
            # Regional daily baseline
            region_daily_rev = daily_base_revenue[i] * reg_factor * seasonality_factor * weekend_factor * anomaly_multiplier
            
            # Add noise
            region_daily_rev += random.gauss(0, region_daily_rev * 0.05)
            region_daily_rev = max(1000, region_daily_rev) # floor
            
            for dept in departments:
                record = {
                    'date': date.strftime('%Y-%m-%d'),
                    'region': region,
                    'department': dept,
                    'revenue': 0.0,
                    'costs': 0.0,
                    'units_sold': 0,
                    'inventory_level': 0,
                    'logistics_delay_days': 0.0,
                    'employee_productivity': 0.0,
                    'headcount': 0,
                    'status': 'Active'
                }
                
                # Headcount scaling
                base_hc = {'Sales': 50, 'Manufacturing': 200, 'Logistics': 100, 'Marketing': 20, 'Customer Support': 80, 'Operations': 40}.get(dept)
                hc_growth = int(i / 365 * (base_hc * 0.1)) # 10% YoY growth
                record['headcount'] = int(base_hc * reg_factor) + hc_growth + random.randint(-2, 2)
                
                # Productivity (bounded 60-100)
                prod_base = 85.0
                if is_anomaly and random.random() < 0.3:
                    prod_base -= random.uniform(10, 25) # Productivity hit
                record['employee_productivity'] = round(max(60, min(100, random.gauss(prod_base, 5))), 1)
                
                # Financials per department
                if dept == 'Sales':
                    record['revenue'] = round(region_daily_rev, 2)
                    record['units_sold'] = int(region_daily_rev / random.uniform(120, 150))
                    # Sales costs (Commissions, travel) ~ 10-15% of rev
                    record['costs'] = round(region_daily_rev * random.uniform(0.10, 0.15), 2)
                    
                elif dept == 'Manufacturing':
                    # COGS ~ 35-45% of total expected revenue (to ensure 15-50% gross margins later)
                    record['costs'] = round(region_daily_rev * random.uniform(0.35, 0.45), 2)
                    record['inventory_level'] = int(record['headcount'] * random.uniform(50, 100))
                    
                elif dept == 'Logistics':
                    # Logistics costs ~ 5-10% of rev
                    record['costs'] = round(region_daily_rev * random.uniform(0.05, 0.10), 2)
                    delay_base = 1.0 if region in ['North America', 'EMEA'] else 2.5
                    if is_anomaly: delay_base += random.uniform(2, 5) # Supply chain shock
                    record['logistics_delay_days'] = round(max(0.1, random.gauss(delay_base, 0.5)), 1)
                    
                elif dept in ['Marketing', 'Customer Support', 'Operations']:
                    # Fixed + Variable costs based on headcount
                    record['costs'] = round((record['headcount'] * random.uniform(200, 400)) + (region_daily_rev * random.uniform(0.01, 0.05)), 2)
                
                # Status
                if record['logistics_delay_days'] > 4.0 or record['employee_productivity'] < 65:
                    record['status'] = 'Warning'
                    
                data.append(record)
                
    df = pd.DataFrame(data)
    os.makedirs('data', exist_ok=True)
    df.to_csv('data/enterprise_operations.csv', index=False)
    logger.success(f"Generated {len(df)} realistic enterprise records in data/enterprise_operations.csv")

if __name__ == "__main__":
    generate_enterprise_data()
