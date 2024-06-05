FROM nginx:alpine

COPY  ./src/main/nginx/registry.password /etc/nginx/conf.d/registry.password
COPY ./src/main/nginx/default.conf /etc/nginx/conf.d/default.conf
