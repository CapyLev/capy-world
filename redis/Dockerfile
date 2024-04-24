FROM redis:7

COPY ./redis.conf /usr/local/etc/redis/redis.conf
COPY ./sysctl.conf /etc/sysctl.conf

CMD ["redis-server"]
