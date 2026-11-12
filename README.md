# SCAMSHIELD — AI-assisted scam & phishing detection

A Python + Streamlit cybersecurity prototype inspired by the supplied dark SaaS dashboard reference. It provides URL pattern analysis, message and email screening, local scan history, analytics, learning content and an optional Groq-powered assistant.

> **Safety notice:** scores are heuristic estimates, not proof that a site or message is safe or malicious. No suspicious URL is opened. Email authentication (SPF/DKIM/DMARC) and external reputation feeds are not checked in this build.

## Features
- Dark responsive dashboard with Material icons, active navigation states, reduced-motion option, subtle page/card animations and mobile layout adjustments.
- URL checks: HTTPS, raw IP hosts, subdomain depth, suspicious keywords, URL length, shortening services and URL structure.
- Message and email checks for urgency, credential requests, payment pressure, prize bait, links and impersonation patterns; scanner examples, clear controls and persistent latest results.
- Explainable risk score (0–29 Low, 30–69 Medium, 70–100 High).
- SQLite scan history with search, risk/type filters, deletion, clear confirmation and filtered CSV export.
- Analytics generated from saved scans (no invented activity).
- Optional Shield AI via Groq API; graceful fallback if not configured.
- Cybersecurity learning and threat-awareness content.

## Run locally
Python 3.10+ is recommended.

```bash
python -m venv .venv
# Windows PowerShell
.venv\\Scripts\\Activate.ps1
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

Open the local URL printed by Streamlit (usually http://localhost:8501).

## Enable Shield AI (optional)
Set `GROQ_API_KEY` in your environment, or create `.streamlit/secrets.toml`:

```toml
GROQ_API_KEY = "your-key-here"
```

Optional model override: `GROQ_MODEL=llama-3.3-70b-versatile`.
Never commit secrets. For Streamlit Community Cloud, add the key in **App settings → Secrets**.

## Deploy to Streamlit Community Cloud
1. Push this folder to a GitHub repository.
2. Visit https://share.streamlit.io/ and sign in with GitHub.
3. Select the repository, branch and `app.py` as the main file.
4. Add `GROQ_API_KEY` under Advanced settings → Secrets if you want live AI.
5. Deploy. The free hosted filesystem may not be durable across app restarts; use a managed database for persistent production history.

## Project structure
```text
SCAMSHIELD/
├── app.py
├── url_analyzer.py
├── message_analyzer.py
├── email_analyzer.py
├── ai_assistant.py
├── database.py
├── requirements.txt
├── .env.example
├── .gitignore
├── README.md
└── screenshots/reference-ui.png
```

## Privacy and limitations
- Scan history stores a short input summary (up to 120 characters), risk score, result and indicators; full message bodies are not saved.
- Data is local in `scamshield.db`. Delete records from Scan History or Settings.
- The current detectors use transparent rules, not a trained machine-learning classifier.
- Do not use this as the sole basis for financial, legal or incident-response decisions.
## 🐳 Run SCAMSHIELD with Docker

SCAMSHIELD is available as a Docker image through GitHub Container Registry.

### Requirements
- Docker Desktop installed and running.

### Download the image

```bash
docker pull ghcr.io/soham17002/scamshield:1.0.0
```

### Run SCAMSHIELD

```bash
docker run --rm -p 8501:8501 ghcr.io/soham17002/scamshield:1.0.0
```

### Open the application

Visit: http://localhost:8501

### Stop the application

Press `Ctrl + C` in the terminal.

### Docker image

`ghcr.io/soham17002/scamshield:1.0.0`

### Live Demo

https://scamshield-soham.streamlit.app/

### Windows Download

Visit the [GitHub Releases](https://github.com/Soham17002/scamshield/releases) page to download the Windows package.
