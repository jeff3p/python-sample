FROM registry.access.redhat.com/ubi9/ubi-minimal:latest
RUN microdnf -y install python3 python3-pip && microdnf -y clean all
WORKDIR /opt/app
COPY app.py .
ENV PORT=8080
CMD ["python3", "app.py"]
