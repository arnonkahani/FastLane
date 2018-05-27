FROM python:3.5-slim
COPY . .
RUN pip3 install -r ./DB/requirements.txt
ENTRYPOINT ["python"]
CMD ["./DB/app.py"]