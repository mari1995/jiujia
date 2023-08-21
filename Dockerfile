FROM python:3.11
MAINTAINER mario
WORKDIR /jiujia_work

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "main.py"]
