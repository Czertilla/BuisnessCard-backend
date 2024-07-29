FROM python:3.12

# TODO replace all "fastapi_app" by dir name

RUN mkdir /BuisnessCard-backend

WORKDIR /BuisnessCard-backend

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

RUN chmod a+x docker/*.sh
