FROM python:3.7-slim

WORKDIR /secretpruner
COPY requirements.txt  /secretpruner/
RUN pip install -r requirements.txt
COPY secretpruner.py /secretpruner/
CMD ["python", "./secretpruner.py"]
