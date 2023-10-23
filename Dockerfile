
FROM bufbuild/buf AS buf
FROM dart:stable AS dart
COPY ./static/scss /app/scss
COPY --from=buf /usr/local/bin/buf /usr/local/bin/

WORKDIR /dart-sass/scss /app
RUN git clone https://github.com/sass/dart-sass.git . && \
    dart pub get && \
    dart run grinder protobuf
RUN mkdir -p /app/css
RUN dart ./bin/sass.dart /app/scss/style.scss /app/css/style.css --source-map

FROM python:3.11-alpine as compiler
ENV PYTHONUNBUFFERED 1
WORKDIR /app
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
RUN pip install --upgrade pip --no-cache-dir
COPY ./requirements.txt /app/requirements.txt
RUN pip install -Ur requirements.txt
RUN pip install gunicorn

FROM python:3.11-alpine as runner
WORKDIR /app
COPY --from=compiler /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
COPY . /app/
RUN mkdir -p /app/static/css
COPY --from=dart /app/css /app/static/css
RUN chmod +x /app/cmd.sh
CMD ["/app/cmd.sh"]