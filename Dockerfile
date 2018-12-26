FROM python:3-alpine

RUN apk add poppler-utils \
            gcc \
            make \
            libc-dev \
            musl-dev \
            linux-headers \
            pcre-dev \
            postgresql-dev

WORKDIR /usr/src/app

COPY requirements.txt .

RUN pip install -r requirements.txt

CMD "luigi --local-scheduler --module cabure RunForYear"