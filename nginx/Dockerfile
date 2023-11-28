# Используйте официальный образ Nginx
FROM nginx:alpine

# Скопируйте конфигурацию Nginx
COPY nginx.conf /etc/nginx/nginx.conf

# Удалите конфигурацию по умолчанию
RUN rm /etc/nginx/conf.d/default.conf

# Порт, который будет прослушивать Nginx
EXPOSE 80