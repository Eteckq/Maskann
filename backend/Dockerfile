FROM node:16-alpine

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

COPY package.json ./
RUN npm i

COPY . /usr/src/app/
RUN npm run build

CMD [ "npm", "run", "start:prod" ]