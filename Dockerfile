FROM python:3.9-alpine
ARG machinepourpouse
WORKDIR "/$machinepourpouse"
COPY "./$machinepourpouse" .
RUN apk add gcc musl-dev python3-dev libffi-dev openssl-dev && \
    pip install -r  requirements.txt