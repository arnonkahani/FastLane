FROM node:slim
COPY UI/package.json .
RUN npm install
COPY /UI .
CMD node app.js
#EXPOSE 8080