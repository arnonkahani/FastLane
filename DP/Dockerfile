FROM ubuntu:latest
RUN apt-get update -y
RUN apt-get install -y python-pip python-dev build-essential
COPY . /app
WORKDIR /app
RUN pip install -r ./DP/requirements.txt
ENTRYPOINT ["python"]
CMD ["./DP/app.py"]
