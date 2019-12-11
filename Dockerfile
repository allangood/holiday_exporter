FROM alpine:3.10

COPY includes/requirements.txt /

RUN apk add --no-cache \
	python3 \
    && pip3 install --upgrade pip \
    && pip3 install -r /requirements.txt

COPY includes/*.py /usr/bin/
COPY includes/*.yaml /etc

ENTRYPOINT ["/usr/bin/holiday_exporter.py"]
