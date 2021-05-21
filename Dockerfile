FROM python:3.9

LABEL author='Talpa Vladimir' version=1 about='shorty_url'

# System environments
ENV LANG=C.UTF-8 \
    PYTHONUNBUFFERED=1

WORKDIR /code

COPY . .

RUN /usr/local/bin/python -m pip install --upgrade pip
RUN pip install -r /code/requirements.txt

CMD gunicorn shorty_url.wsgi:application --bind 0.0.0.0:8000