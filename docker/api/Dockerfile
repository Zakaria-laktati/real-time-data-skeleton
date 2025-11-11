# Stage de build
FROM python:3.9-slim

WORKDIR /app

# Installation des dépendances
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Le code source sera monté via un volume
EXPOSE 5000

CMD ["python", "api/app.py"]