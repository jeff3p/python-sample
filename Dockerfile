FROM quay.io/hummingbird/python:latest-builder
USER 0
RUN microdnf -y install python3 python3-pip && microdnf -y clean all
USER ${CONTAINER_DEFAULT_USER}
WORKDIR /opt/app
COPY app.py .
ENV PORT=8080
CMD ["python3", "app.py"]
