FROM python:3
COPY ./requirements.txt .
RUN pip install -r requirements.txt
COPY . /opt/app
WORKDIR /opt/app
ENTRYPOINT ["python", "./catseaice.py"]
