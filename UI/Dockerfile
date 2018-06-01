FROM node:slim
WORKDIR /UI
COPY UI/package.json /UI
RUN npm install
RUN cd /UI
COPY . /UI
CMD node app.js
#EXPOSE 8080