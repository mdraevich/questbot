FROM fsfe/pipenv:alpine-3.13 AS pipenv-env

WORKDIR /srv/team_quest_bot

COPY Pipfile ./
COPY Pipfile.lock ./
RUN pipenv lock -r -d > requirements.txt



FROM python:3.9-alpine

LABEL MAINTAINER=github.com/mdraevich
LABEL SERVICE=team_quest_bot

WORKDIR /srv/team_quest_bot

COPY --from=pipenv-env /srv/team_quest_bot/requirements.txt ./
RUN pip3 install -r requirements.txt

COPY ./src .

CMD ["python3", "main.py"]