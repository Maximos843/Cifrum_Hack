FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1

RUN mkdir /app

COPY ./requirements.txt ./requirements-dev.txt /app/

WORKDIR /app

RUN python -m pip install --no-cache-dir -r requirements.txt -r requirements-dev.txt

RUN pip install flake8

COPY . /app

EXPOSE 8000
CMD ["fastapi", "run", "./src/app.py", "--port", "8000", "--proxy-headers"]
