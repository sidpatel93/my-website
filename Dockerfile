FROM python:3.9.6-buster

WORKDIR /usr/local/app

COPY requirements.txt .

RUN pip3 install -r requirements.txt

COPY . .

EXPOSE 5000

ENV "SECRET_KEY"="a66091b86cdc29fe0c984b07dd582274"

ENV "SQLALCHEMY_DATABASE_URI"="sqlite:///site.db"

ENV "FLASK_APP"="run.py"

CMD ["flask", "run", "--host=0.0.0.0"]