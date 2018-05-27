FROM node:slim
WORKDIR /UI
COPY package.json /UI
RUN npm install
COPY . /UI
CMD node app.js
EXPOSE 8080