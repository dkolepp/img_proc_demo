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

RUN curl -L -o yolo.h5 \
  https://github.com/OlafenwaMoses/ImageAI/releases/download/1.0/yolo.h5

ADD img_lib.py img_worker.py rediswq.py /app-root/src/


CMD ["python3", "img_worker.py"]

