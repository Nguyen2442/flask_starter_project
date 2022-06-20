FROM python:3.10-slim

COPY Pipfile Pipfile.lock

WORKDIR /app
COPY . .

RUN pip install pipenv
RUN pipenv install --system --deploy

CMD ["flask", "run"]

EXPOSE 5000



FROM python:3.10

ADD ./ /src-backend

WORKDIR /src-backend

RUN python3 -m venv src-env && \
    . ./src-env/bin/activate && \
    pip install pipenv gunicorn gevent && \
    pipenv install --dev && \
    chmod +x ./start.sh && \
    cd src_api/docs && \
    make clean && \
    make html

CMD ["./start.sh"]

