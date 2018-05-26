FROM node:7
WORKDIR /app
COPY package.json /ui
RUN npm install
COPY . /ui
CMD node app.js
EXPOSE 3000