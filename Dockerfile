FROM alpine:3.10

RUN apk add --no-cache \
	python3 \
    && pip3 install --upgrade pip \
    && pip3 install pyyaml \
    && pip3 install holidays \
    && pip3 install prometheus_client

COPY includes/*.py /usr/bin/
COPY includes/*.yaml /etc

ENTRYPOINT ["/usr/bin/holiday_exporter.py"]
