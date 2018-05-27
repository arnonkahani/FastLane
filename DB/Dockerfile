FROM ubuntu:latest
RUN apt-get update -y
RUN apt-get install -y python3-pip python3-dev
COPY . /DB
WORKDIR /DB
RUN pip3 install -r requirements.txt
EXPOSE 3001
ENTRYPOINT ["python"]
CMD ["./app.py"]