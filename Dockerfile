FROM python:3.11

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["sh", "-c", "python init_db.py && gunicorn -w 4 -b 0.0.0.0:5000 --timeout 120 app:app"]