FROM node:7
WORKDIR /UI
COPY package.json /UI
RUN npm install
COPY . /UI
CMD node app.js
EXPOSE 3000