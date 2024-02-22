FROM nginx:mainline-alpine

RUN apk add --update --no-cache \
  bash \
  supervisor \
  fcgiwrap

RUN addgroup nginx www-data

COPY supervisord.conf /etc/
COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY proxy.cgi /etc/nginx/

CMD ["/usr/bin/supervisord", "-c", "/etc/supervisord.conf"]
