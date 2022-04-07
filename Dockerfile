FROM alpine:3.5
RUN apk add --no-cache python3 curl && \
    python3 -m ensurepip && \
    rm -r /usr/lib/python*/ensurepip && \
    pip3 install --upgrade pip prometheus_client requests\
    && rm -rf /var/cache/apk/*

WORKDIR /app
COPY storm-exporter.py /app

EXPOSE 9095

ENTRYPOINT [ "/bin/sh", "-c", "python3 /app/storm-exporter.py $STORM_UI_HOST 9095 $REFRESH_RATE" ]
