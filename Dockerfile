FROM python:3.8.1-alpine3.11

COPY includes/requirements.txt /
RUN pip install -r /requirements.txt \
    && addgroup -g 1000 holiday \
    && adduser -D -u 1000 -G holiday holiday \ 
    && rm requirements.txt

COPY includes/*.py /usr/bin/
COPY includes/*.yaml /etc
USER holiday

ENTRYPOINT ["python", "/usr/bin/holiday_exporter.py"]
