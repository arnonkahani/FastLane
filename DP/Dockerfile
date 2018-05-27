FROM python:3.5-slim
COPY . /dp
RUN pip3 install -r ./DP/requirements.txt
EXPOSE 3002
ENTRYPOINT ["python"]
CMD ["./DP/app.py"]