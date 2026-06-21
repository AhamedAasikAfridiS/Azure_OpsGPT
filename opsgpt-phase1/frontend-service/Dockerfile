FROM node:20-alpine AS builder

WORKDIR /app

ARG VITE_CORE_API_URL=/api/core
ARG VITE_AUTH_PROVIDER=entra
ARG VITE_AZURE_TENANT_ID
ARG VITE_AZURE_CLIENT_ID
ARG VITE_AZURE_REDIRECT_URI
ARG VITE_AZURE_POST_LOGOUT_REDIRECT_URI
ARG VITE_AZURE_API_SCOPE

COPY package*.json ./
RUN if [ -f package-lock.json ]; then npm ci; else npm install; fi

COPY . ./
RUN npm run build

FROM nginx:1.27-alpine AS runtime

COPY frontend-nginx.conf /etc/nginx/nginx.conf
COPY --from=builder /app/dist /usr/share/nginx/html

RUN mkdir -p /tmp/nginx/client_temp /tmp/nginx/proxy_temp /tmp/nginx/fastcgi_temp /tmp/nginx/uwsgi_temp /tmp/nginx/scgi_temp \
    && chown -R nginx:nginx /tmp/nginx /usr/share/nginx/html

USER nginx

EXPOSE 3000

ENTRYPOINT ["nginx"]
CMD ["-g", "daemon off;"]
