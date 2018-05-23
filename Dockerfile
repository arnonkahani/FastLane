FROM ubuntu:latest
RUN apt-get update -y
RUN apt-get install -y python-pip python-dev build-essential
COPY . /app
WORKDIR /app/DP
RUN pip install -r requirements.txt
EXPOSE 3000
ENTRYPOINT ["python"]
CMD ["app.py"]