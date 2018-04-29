FROM ubuntu:latest
RUN apt-get update -y
RUN apt-get install -y python3-pip python3-dev build-essential
COPY . /app
WORKDIR /app
RUN pip install -r ./DP/requirements.txt
EXPOSE 3000
ENTRYPOINT ["python"]
CMD ["./DP/app.py"]
