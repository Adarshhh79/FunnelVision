# FunnelVision — Streamlit Web App

This is the Streamlit web version of FunnelVision using the weighted-scoring
questions, stages, products, and stage content from the supplied
`FunnelVision_Weighted_Scoring.py`.

## Structure

- `app.py` — Streamlit entry point
- `requirements.txt` — dependencies
- `.gitignore` — excludes local database/secrets
- `README.md` — deployment instructions

## Run locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Deploy with Streamlit Community Cloud

1. Create a GitHub repository.
2. Upload these files.
3. Select `app.py` as the main file when deploying.
4. Deploy.

## Demo admin

Username: `admin`  
Password: `admin123`

## Database note

The app uses SQLite (`funnelvision.db`). This is fine for a local/demo project.
For a hosted multi-user application where data must persist across restarts,
use a persistent hosted database.
