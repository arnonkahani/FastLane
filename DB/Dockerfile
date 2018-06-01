FROM python:3.5-slim
COPY . /db
RUN pip3 install -r ./DB/requirements.txt
EXPOSE 3001
ENTRYPOINT ["python"]
CMD ["./db/app.py"]