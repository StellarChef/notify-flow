# Obraz TWOJEJ apki FastAPI. (Postgres ma własny, gotowy obraz w docker-compose.yml.)
FROM python:3.14-slim

# Katalog roboczy wewnątrz kontenera
WORKDIR /app

# 1) Najpierw SAM requirements.txt + instalacja.
#    Dzięki tej kolejności Docker zapamiętuje (cache'uje) warstwę z zależnościami:
#    jak zmienisz tylko kod, pip install NIE wykona się ponownie -> szybszy build.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 2) Dopiero teraz reszta kodu (zmienia się często, więc jest na końcu)
COPY . .

# Dokumentuje, że apka nasłuchuje na 8000
EXPOSE 8000

# 0.0.0.0 (NIE localhost!) - inaczej apka byłaby widoczna tylko wewnątrz kontenera
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]