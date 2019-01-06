# base image
FROM node:10.15-alpine

# Create app directory
RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

COPY package.json /usr/src/app/

RUN npm install

CMD [ "npm", "start" ]
