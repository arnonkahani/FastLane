FROM python:3.4-alpine
ADD . /DP
WORKDIR /DP
CMD ["ls"]
RUN pip install -r DP/requirements.txt
CMD ["python", "app.py"]