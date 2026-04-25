from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from .routes import health, analysis


def create_app() -> FastAPI:
    app = FastAPI(title="Resume Analyzer API", version="0.1.0")

    app.include_router(health.router, prefix="/health", tags=["health"])
    app.include_router(analysis.router, prefix="/analysis", tags=["analysis"])

    @app.get("/")
    async def root():
        return {"message": "Resume Analyzer API running"}

    @app.get("/ui", response_class=HTMLResponse)
    async def simple_ui():
        # Simple HTML frontend without any external JS framework.
        return """
        <!doctype html>
        <html lang="en">
        <head>
          <meta charset="utf-8" />
          <title>Resume Analyzer</title>
          <style>
            body { font-family: system-ui, sans-serif; margin: 20px; background: #0f172a; color: #e5e7eb; }
            h1 { color: #38bdf8; }
            textarea { width: 100%; min-height: 140px; padding: 8px; border-radius: 6px; border: 1px solid #4b5563; background: #020617; color: #e5e7eb; }
            label { font-weight: 600; display: block; margin-top: 12px; margin-bottom: 4px; }
            input[type="file"] { width: 100%; padding: 10px; border-radius: 8px; border: 1px dashed #334155; background: #020617; color: #e5e7eb; }
            button { margin-top: 16px; padding: 10px 18px; border-radius: 9999px; border: none; background: #38bdf8; color: #020617; font-weight: 700; cursor: pointer; }
            button:disabled { opacity: 0.6; cursor: not-allowed; }
            .card { max-width: 900px; margin: 0 auto; padding: 20px; border-radius: 12px; background: #020617; box-shadow: 0 20px 40px rgba(15,23,42,0.8); }
            .row { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; }
            .result { margin-top: 20px; padding: 12px; border-radius: 8px; background: #020617; border: 1px solid #1f2937; }
            .hint { color: #94a3b8; font-size: 13px; margin-top: 6px; }
          </style>
        </head>
        <body>
          <div class="card">
            <h1>Resume Analyzer (Local Model)</h1>
            <p>Paste your resume text or upload a PDF, add the job description, then click Analyze.</p>
            <div class="row">
              <div>
                <label for="resume">Resume Text</label>
                <textarea id="resume" placeholder="Paste your resume text here..."></textarea>
                <div class="hint">Tip: If you upload a PDF below, you can leave this empty.</div>
              </div>
              <div>
                <label for="job">Job Description</label>
                <textarea id="job" placeholder="Paste the job description here..."></textarea>
                <div class="hint">Tip: Paste the full job description for better matching.</div>
              </div>
            </div>
            <label for="pdf">Or Upload Resume PDF</label>
            <input id="pdf" type="file" accept="application/pdf" />
            <button id="analyzeBtn">Analyze</button>
            <div id="result" class="result"></div>
          </div>
          <script>
            const btn = document.getElementById('analyzeBtn');
            const resultDiv = document.getElementById('result');
            btn.addEventListener('click', async () => {
              const resume = document.getElementById('resume').value.trim();
              const job = document.getElementById('job').value.trim();
              const fileInput = document.getElementById('pdf');
              const pdfFile = fileInput.files[0];
              if (!job) {
                resultDiv.textContent = 'Please enter a job description.';
                return;
              }
              btn.disabled = true;
              resultDiv.textContent = pdfFile ? 'Uploading PDF and analyzing...' : 'Analyzing...';
              try {
                let resp;
                if (pdfFile) {
                  const formData = new FormData();
                  formData.append('file', pdfFile);
                  formData.append('job_text', job);
                  resp = await fetch('/analysis/pdf', {
                    method: 'POST',
                    body: formData
                  });
                } else {
                  if (!resume) {
                    resultDiv.textContent = 'Please either paste resume text or upload a PDF.';
                    btn.disabled = false;
                    return;
                  }
                  resp = await fetch('/analysis/simple', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ resume_text: resume, job_text: job })
                  });
                }
                if (!resp.ok) {
                  const err = await resp.json().catch(() => ({}));
                  throw new Error(err.detail || 'Request failed');
                }
                const data = await resp.json();
                const score = Number(data.score);
                let label = 'Low';
                if (score >= 75) label = 'High';
                else if (score >= 50) label = 'Medium';
                resultDiv.textContent = `Match score: ${score.toFixed(2)} / 100 (${label} match)`;
              } catch (e) {
                resultDiv.textContent = 'Error: ' + e.message;
              } finally {
                btn.disabled = false;
              }
            });
          </script>
        </body>
        </html>
        """

    return app


app = create_app()
