FROM node:lts-alpine AS vue

WORKDIR /app

COPY client/package*.json ./
RUN npm install
COPY client/. .
RUN npm run build

FROM python:3-buster

WORKDIR /server

COPY server/requirements.txt ./
RUN apt-get update && apt install -y --no-install-recommends cmake && pip install --no-cache-dir -r requirements.txt

COPY server/. ./

COPY --from=vue /app/dist ./public

CMD [ "python", "./main.py" ]
