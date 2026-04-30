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
    from sklearn.linear_model import LinearRegression

class ForecastingEngine:
    def __init__(self, db: Session = None):
        self.db = db or SessionLocal()

    def generate_forecasts(self, days_to_forecast=30):
        data = self.db.query(OperationalData).all()
        if not data:
            return
        
        df = pd.DataFrame([{
            'ds': pd.to_datetime(d.date),
            'y': d.revenue
        } for d in data])
        
        # Aggregating by day in case of multiple depts
        df = df.groupby('ds').sum().reset_index()

        if HAS_PROPHET:
            model = Prophet()
            model.fit(df)
            future = model.make_future_dataframe(periods=days_to_forecast)
            forecast = model.predict(future)
            
            # Extract only future dates
            predictions = forecast.tail(days_to_forecast)
            
            for _, row in predictions.iterrows():
                res = ForecastResult(
                    metric_name="Revenue",
                    forecast_date=row['ds'].date(),
                    predicted_value=float(row['yhat']),
                    lower_bound=float(row['yhat_lower']),
                    upper_bound=float(row['yhat_upper']),
                    model_version="Prophet v1.0"
                )
                self.db.add(res)
        else:
            # Simple Linear Regression fallback
            df['ordinal'] = df['ds'].map(datetime.toordinal)
            X = df[['ordinal']].values
            y = df['y'].values
            
            model = LinearRegression()
            model.fit(X, y)
            
            last_date = df['ds'].max()
            for i in range(1, days_to_forecast + 1):
                f_date = last_date + timedelta(days=i)
                ordinal = f_date.toordinal()
                pred = model.predict([[ordinal]])[0]
                
                res = ForecastResult(
                    metric_name="Revenue",
                    forecast_date=f_date.date(),
                    predicted_value=float(pred),
                    model_version="LinearRegression Fallback"
                )
                self.db.add(res)
                
        self.db.commit()
        logger.success("Forecasting completed.")

if __name__ == "__main__":
    engine = ForecastingEngine()
    engine.generate_forecasts()
