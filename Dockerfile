FROM python:3.10.2

WORKDIR /usr/src/mai

RUN apt-get update && apt-get install -y git
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

RUN scripts/linux/build_database.sh

ENTRYPOINT ["python3", "mai.py"]
