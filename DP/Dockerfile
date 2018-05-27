FROM ubuntu:latest
RUN apt-get update -y
RUN apt-get install -y python3-pip python3-dev
COPY . /DP
WORKDIR /DP
RUN pip3 install -r requirements.txt
EXPOSE 3000
ENTRYPOINT ["python"]
CMD ["./app.py"]