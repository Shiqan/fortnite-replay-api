FROM python:3.7-slim

WORKDIR /app

RUN pip install pipenv  
COPY  Pipfile Pipfile.lock /app/
RUN pipenv install --system --deploy
COPY . /app

EXPOSE 5000

ENTRYPOINT ["sh", "entrypoint.sh"]