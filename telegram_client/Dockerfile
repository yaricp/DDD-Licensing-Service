FROM python:3.12

RUN apt update && apt upgrade -y
RUN apt install -y protobuf-compiler

RUN curl -sSL https://install.python-poetry.org | POETRY_HOME=/opt/poetry python3 && \
    cd /usr/local/bin && \
    ln -s /opt/poetry/bin/poetry && \
    poetry config virtualenvs.create true && \
    poetry config virtualenvs.in-project true

COPY pyproject.toml /
COPY poetry.lock /

RUN poetry install

WORKDIR /

RUN mkdir -p /protobuf_types

COPY / /telegram_client
COPY /protobuf_types /protobuf_types
COPY /scripts /scripts
COPY start.sh /

# Changing permissions for correct work inside docker:
RUN chmod +x /start.sh
RUN chmod +x /scripts/*

ENTRYPOINT [ "/bin/bash", "-l", "-c" ]
