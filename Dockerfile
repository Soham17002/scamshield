
FROM python:3.11-slim
LABEL org.opencontainers.image.title="SCAMSHIELD"

LABEL org.opencontainers.image.description="AI-powered scam and phishing detection platform with URL scanning, phishing message analysis, email security checks, AI assistance, and cybersecurity awareness."

LABEL org.opencontainers.image.source="https://github.com/Soham17002/scamshield"
WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.address=0.0.0.0", "--server.port=8501", "--server.headless=true"]
