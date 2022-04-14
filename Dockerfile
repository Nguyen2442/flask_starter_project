FROM python:3.10-slim

COPY Pipfile Pipfile.lock

WORKDIR /app
COPY . .

RUN pip install pipenv
RUN pipenv install --system --deploy

CMD ["flask", "run"]

EXPOSE 5000

