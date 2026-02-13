FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y \
    libpq-dev gcc && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY backend .

ENV SECRET_KEY=dummy-build-key
ENV DATABASE_URL=sqlite:///buildtime.db
ENV DEBUG=False

RUN python manage.py collectstatic --noinput

EXPOSE 8000

CMD sh -c "python manage.py migrate && python manage.py create_admin && daphne skillconnect.asgi:application --bind 0.0.0.0 --port $PORT"
