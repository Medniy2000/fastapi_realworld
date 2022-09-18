FROM python:3.9.10
ENV PYTHONUNBUFFERED 1
RUN mkdir /app
WORKDIR /app
COPY . /app/
RUN pip install --upgrade pip
RUN pip install poetry
RUN poetry config virtualenvs.create false
RUN poetry install
CMD alembic upgrade head
CMD exec uvicorn src.app.main:app --reload --port 82 --workers 2

