FROM python:3-slim as build
WORKDIR /app
ADD requirements.txt .
RUN pip install -r requirements.txt
ADD . .
FROM build as service
EXPOSE 8080
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "wsgi:server"]
