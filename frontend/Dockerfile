# Dockerfile
FROM node:16-alpine

# create destination directory
RUN mkdir -p /usr/src/nuxt-app
WORKDIR /usr/src/nuxt-app

COPY package.json ./
RUN npm i

COPY . /usr/src/nuxt-app/
RUN npm run build

ENV NUXT_HOST=0.0.0.0
ENV NUXT_PORT=80

CMD [ "npm", "dev" ]