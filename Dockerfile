FROM python:3.11-slim

RUN pip3 install flask requests yarl

WORKDIR /src

COPY src/state_app.py /src
COPY src/consumers /src/consumers
COPY src/utils /src/utils
ENTRYPOINT ["python3", "state_app.py"]