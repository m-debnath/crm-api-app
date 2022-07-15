FROM nginxinc/nginx-unprivileged:1.23-alpine

COPY ./default.conf /etc/nginx/conf.d/default.conf
COPY ./crm-app-selfsigned.crt /etc/ssl/certs/crm-app-selfsigned.crt
COPY ./crm-app-selfsigned.key /etc/ssl/private/crm-app-selfsigned.key

USER root

RUN chmod 644 /etc/ssl/certs/crm-app-selfsigned.crt
RUN chown nginx:nginx /etc/ssl/certs/crm-app-selfsigned.crt
RUN chmod 600 /etc/ssl/private/crm-app-selfsigned.key
RUN chown nginx:nginx /etc/ssl/private/crm-app-selfsigned.key

RUN mkdir -p /vol/static
RUN chmod 755 /vol/static

USER nginx