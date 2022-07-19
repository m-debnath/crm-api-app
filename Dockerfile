FROM python:3.9-alpine

ENV PYTHONUNBUFFERED 1
ENV PATH="/app/scripts:${PATH}"

WORKDIR /app

RUN apk update \
    && apk add --virtual build-deps linux-headers gcc python3-dev libc-dev musl-dev \
    && apk add bash postgresql-dev libffi-dev

COPY ./requirements.txt /app
RUN pip install --no-cache-dir --upgrade -r requirements.txt

RUN apk del build-deps

COPY . /app

RUN mkdir -p /vol/web/media
RUN mkdir -p /vol/web/static
RUN adduser -D user
RUN chown -R user:user /vol
RUN chmod -R 755 /vol/web
RUN chown -R user:user wait-for
RUN chmod 755 /app/wait-for
RUN chmod -R 755 /app/scripts
USER user

CMD ["./wait-for", "crm-api-app-db:5432", "--", "entrypoint.sh"]