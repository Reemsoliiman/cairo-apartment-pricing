# Cairo Apartment Pricing Engine 🏙️💰

**Predicts fair market value for 2–3 bedroom apartments in New Cairo within ±EGP 108,000**

Auto-scrapes **sold prices** from PropertyFinder, Bayut, OLX → adjusts for **EGP devaluation** → trains **5 models** → picks best via **MLflow** → deploys via **Streamlit**.

**Current Best MAE**: `108,420 EGP` (CatBoost + sold prices + compound tier)

### Features
- Live scraping (daily)
- Inflation-adjusted USD pricing
- Compound reputation ranking
- Auto model selection (XGBoost, CatBoost, LightGBM, RF, TabNet)
- MLflow experiment tracking
- Streamlit UI with manual model override
- GitHub Actions auto-retrain

### Quick Start
```bash
pip install -r requirements.txt
playwright install chromium
python -m scraper.run_all
python src/pipeline.py
streamlit run streamlit_app.py