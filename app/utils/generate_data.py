import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import os

def generate_sample_data(num_days=365):
    start_date = datetime.now() - timedelta(days=num_days)
    departments = ['Sales', 'Manufacturing', 'Logistics', 'Marketing', 'Customer Support']
    
    data = []
    for i in range(num_days):
        date = start_date + timedelta(days=i)
        for dept in departments:
            # Base metrics with some seasonality and noise
            revenue_base = 5000 if dept == 'Sales' else 0
            if dept == 'Sales':
                revenue = revenue_base + random.uniform(1000, 5000) + (np.sin(i/30) * 1000)
            else:
                revenue = 0
            
            costs = random.uniform(2000, 4000) + (revenue * 0.1)
            units_produced = random.randint(50, 200) if dept == 'Manufacturing' else 0
            units_sold = random.randint(40, 180) if dept == 'Sales' else 0
            headcount = random.randint(10, 50)
            
            # Introduce some anomalies
            if i % 45 == 0: # Every 45 days, drop revenue
                revenue *= 0.5
            if i % 60 == 0: # Every 60 days, spike costs
                costs *= 2.0
                
            data.append({
                'date': date.strftime('%Y-%m-%d'),
                'department': dept,
                'revenue': round(revenue, 2),
                'costs': round(costs, 2),
                'units_produced': units_produced,
                'units_sold': units_sold,
                'headcount': headcount,
                'status': 'Active'
            })
            
    df = pd.DataFrame(data)
    os.makedirs('data', exist_ok=True)
    df.to_csv('data/sample_operations.csv', index=False)
    print(f"Generated {len(df)} rows of sample data in data/sample_operations.csv")

if __name__ == "__main__":
    generate_sample_data()
