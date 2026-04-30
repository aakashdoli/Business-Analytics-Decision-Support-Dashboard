# 📊 Business Analytics & Decision Support Dashboard

An enterprise-grade, end-to-end analytics platform designed to transform raw operational data into actionable executive insights. This system integrates automated ETL, SQL-based data warehousing, machine learning forecasting, and AI-driven narrative generation.

## 🚀 Key Features

- **Automated ETL Pipeline**: Robust processing of CSV/Excel datasets with schema validation and cleaning.
- **SQL Data Warehouse**: Structured storage using SQLAlchemy (SQLite for local, PostgreSQL for production).
- **KPI Engine**: Automated calculation of Financial, Operational, and Sales metrics.
- **Forecasting & ML**: Time-series revenue forecasting using Facebook Prophet and statistical anomaly detection.
- **AI Insight Engine**: Rule-based narrative generation for executive summaries and recommendations.
- **Interactive Dashboards**: Modern, multi-page Streamlit UI with Plotly visualizations.
- **Enterprise Security**: Basic authentication and session management.
- **Dockerized Architecture**: Full stack containerization for easy deployment.

## 🛠 Tech Stack

- **Frontend**: Streamlit, Plotly
- **Backend**: Python, Pandas, NumPy
- **Database**: SQLAlchemy, PostgreSQL / SQLite
- **Machine Learning**: Scikit-learn, Prophet
- **DevOps**: Docker, Docker Compose
- **Logging**: Loguru

## 📂 Project Structure

```text
business-analytics-dashboard/
├── app/
│   ├── analytics/      # KPI and Anomaly engines
│   ├── forecasting/    # Predictive modeling
│   ├── ai_insights/    # Narrative generation
│   ├── etl/            # Data processing pipeline
│   ├── database/       # SQLAlchemy models and session
│   └── dashboard/      # Frontend components
├── data/               # Raw and processed datasets
├── pages/              # Streamlit multi-page routes
├── main.py             # Entry point & Authentication
├── Dockerfile          # Container config
└── docker-compose.yml  # Orchestration
```

## 🚥 Quick Start

### 1. Local Setup
```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the application
streamlit run main.py
```

### 2. Docker Deployment (Recommended)
```bash
docker compose up --build
```

## 📈 Usage
1. **Login**: Use `admin` / `admin123`.
2. **Data Center**: Upload your operational CSV or use the pre-generated sample data.
3. **Trigger Engines**: Click "Update All Analytics" to run the ML and KPI modules.
4. **Analysis**: Navigate through the Executive Summary and Forecasting pages to view insights.

## 🛠 Future Roadmap
- [ ] Integration with OpenAI/Gemini for advanced LLM insights.
- [ ] Real-time data streaming support.
- [ ] Automated PDF report generation and email distribution.
- [ ] Role-Based Access Control (RBAC).

---
*Built with ❤️ for Business Intelligence and Data Engineering Excellence.*
