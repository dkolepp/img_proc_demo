FROM registry.access.redhat.com/ubi8/ubi:8.2

ENV IMG_DIR=/data \
    QUEUE_NAME=uploads

ADD requirements.txt /app-root/src/
WORKDIR /app-root/src

RUN  yum install -y \
      python3 \
      libSM \
      libXext \
      libXext \
      libXrender && \
    pip3 install --upgrade pip setuptools && \
    pip3 install wheel

RUN pip3 install -r requirements.txt

ADD img_lib.py img_worker.py rediswq.py yolo.h5 /app-root/src/


CMD ["python3", "img_worker.py"]

