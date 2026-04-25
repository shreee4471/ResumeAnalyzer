# Resume Analyzer (Local Model)

This project is a **local resume analyzer** (no external “analysis APIs”). It supports:

- Paste resume text + job description → match score
- Upload resume **PDF** + job description → match score
- Train your **own model locally** using a CSV dataset

## Requirements

- Windows 10/11
- Python installed (your terminal should support `python --version`)

## 1) Setup (first time)

Open PowerShell in `C:\resumeanalyzer`:

```powershell
cd C:\resumeanalyzer
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

If activation is blocked:

```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

## 2) Build a training dataset

### Option A — Use your real `Resume.csv` or your own dataset (recommended)

This converts your resume CSV (with resume text + category) into our training file:
`ml_data\processed\train.csv` with columns `resume_text, job_text, label` or 'columns based on your dataset'.

```powershell
python -m backend.app.ml.import_resume_csv --input "path" --max_rows 2000 --rows_per_resume 2
```

You can increase `--max_rows` to generate a bigger dataset.

### Option B — Generate synthetic dataset

```powershell
python -m backend.app.ml.generate_dataset --rows 5000
```

## 3) Train the model (local)

Fast CPU training (recommended for demo):

```powershell
python -m backend.app.ml.train --epochs 1 --max_rows 2000
```

Full training (slower):

```powershell
python -m backend.app.ml.train --epochs 2
```

Model is saved to:

`backend\app\ml\model_artifacts\distilbert-base-uncased\`

## 4) Start the application

```powershell
uvicorn backend.app.main:app --reload --port 8000
```

Open the UI:

- `http://127.0.0.1:8000/ui`

## Troubleshooting

### “accelerate is missing”

Run:

```powershell
pip install -r requirements.txt
```

### PDF upload error / empty extraction

Some PDFs are images/scans. `pdfplumber` extracts text only if the PDF contains selectable text.
If it’s scanned, you’d need OCR (not included here).

