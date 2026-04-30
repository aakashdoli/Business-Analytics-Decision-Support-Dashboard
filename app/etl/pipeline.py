import pandas as pd
import numpy as np
from sqlalchemy.orm import Session
from datetime import datetime
from loguru import logger
from app.database.models import OperationalData
from app.database.session import SessionLocal, init_db

class ETLPipeline:
    def __init__(self):
        init_db()
        self.db = SessionLocal()

    def process_csv(self, file_path):
        try:
            logger.info(f"Starting ETL for {file_path}")
            df = pd.read_csv(file_path)
            
            # Validation
            required_columns = ['date', 'department', 'revenue', 'costs', 'units_produced', 'units_sold']
            for col in required_columns:
                if col not in df.columns:
                    raise ValueError(f"Missing required column: {col}")

            # Cleaning
            df['date'] = pd.to_datetime(df['date'])
            df = df.fillna({
                'revenue': 0.0,
                'costs': 0.0,
                'units_produced': 0,
                'units_sold': 0,
                'headcount': 0,
                'status': 'Unknown'
            })

            # Data Transformation
            # (In a real app, we might add more logic here)

            # Ingestion
            records = []
            for _, row in df.iterrows():
                record = OperationalData(
                    date=row['date'].date(),
                    department=row['department'],
                    revenue=float(row['revenue']),
                    costs=float(row['costs']),
                    units_produced=int(row['units_produced']),
                    units_sold=int(row['units_sold']),
                    headcount=int(row['headcount']),
                    status=row['status']
                )
                records.append(record)

            # Clear existing data for demo purposes (optional)
            # self.db.query(OperationalData).delete()
            
            self.db.add_all(records)
            self.db.commit()
            logger.success(f"Successfully ingested {len(records)} records")
            return len(records)

        except Exception as e:
            self.db.rollback()
            logger.error(f"ETL Error: {str(e)}")
            raise e
        finally:
            self.db.close()

if __name__ == "__main__":
    pipeline = ETLPipeline()
    pipeline.process_csv('data/sample_operations.csv')
