FROM nginx:1.25-alpine AS dev
RUN rm /etc/nginx/conf.d/default.conf
COPY nginx.conf /etc/nginx/conf.d
WORKDIR /app/nginx

FROM nginx:1.25-alpine AS prod
RUN rm /etc/nginx/conf.d/default.conf
COPY nginx.conf /etc/nginx/conf.d
WORKDIR /app/nginx
