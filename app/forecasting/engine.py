import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.database.models import OperationalData, ForecastResult
from app.database.session import SessionLocal
from loguru import logger

try:
    from prophet import Prophet
    HAS_PROPHET = True
except ImportError:
    HAS_PROPHET = False
    logger.warning("Prophet not installed. Run `pip install prophet` for advanced forecasting. Falling back to moving average.")

class ForecastingEngine:
    def __init__(self, db: Session = None):
        self.db = db or SessionLocal()
        self.metrics_to_forecast = {
            'revenue': 'Total Revenue',
            'costs': 'Total Costs',
            'employee_productivity': 'Efficiency Score'
        }

    def generate_forecasts(self, days_to_forecast=30):
        logger.info("Starting advanced Prophet forecasting for multiple metrics...")
        self.db.query(ForecastResult).delete() # Reset old forecasts
        
        data = self.db.query(OperationalData).all()
        if not data:
            return
            
        df_raw = pd.DataFrame([{
            'date': pd.to_datetime(d.date),
            'revenue': d.revenue,
            'costs': d.costs,
            'employee_productivity': d.employee_productivity
        } for d in data])
        
        # Aggregate to daily levels
        df_daily = df_raw.groupby('date').sum().reset_index()
        # Averages for productivity instead of sum
        df_daily['employee_productivity'] = df_raw.groupby('date')['employee_productivity'].mean().values

        for metric_col, metric_display_name in self.metrics_to_forecast.items():
            df_metric = df_daily[['date', metric_col]].rename(columns={'date': 'ds', metric_col: 'y'})
            
            if HAS_PROPHET:
                # Configure Prophet for enterprise data (weekly/yearly seasonality)
                model = Prophet(
                    yearly_seasonality=True,
                    weekly_seasonality=True,
                    daily_seasonality=False,
                    interval_width=0.95 # 95% confidence intervals
                )
                model.fit(df_metric)
                
                future = model.make_future_dataframe(periods=days_to_forecast)
                forecast = model.predict(future)
                
                predictions = forecast.tail(days_to_forecast)
                
                for _, row in predictions.iterrows():
                    res = ForecastResult(
                        metric_name=metric_display_name,
                        forecast_date=row['ds'].date(),
                        predicted_value=float(row['yhat']),
                        lower_bound=float(row['yhat_lower']),
                        upper_bound=float(row['yhat_upper']),
                        model_version="Prophet Enterprise v2.0"
                    )
                    self.db.add(res)
            else:
                # Fallback: Simple moving average projection
                last_val = df_metric['y'].iloc[-14:].mean() # 14-day MA
                last_date = df_metric['ds'].max()
                
                for i in range(1, days_to_forecast + 1):
                    f_date = last_date + timedelta(days=i)
                    noise = np.random.normal(0, last_val * 0.05)
                    pred = last_val + noise
                    
                    res = ForecastResult(
                        metric_name=metric_display_name,
                        forecast_date=f_date.date(),
                        predicted_value=float(pred),
                        lower_bound=float(pred * 0.9),
                        upper_bound=float(pred * 1.1),
                        model_version="MA Fallback v1.0"
                    )
                    self.db.add(res)
                    
        self.db.commit()
        logger.success("Advanced multi-metric forecasting completed.")

if __name__ == "__main__":
    engine = ForecastingEngine()
    engine.generate_forecasts()
