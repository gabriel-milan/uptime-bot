FROM node:lts-alpine as build-stage
WORKDIR /app
COPY package*.json ./
RUN npm ci 
RUN npm audit fix
COPY . ./
RUN npm run lint
RUN npm run build

FROM nginx:stable-alpine as production-stage
COPY --from=build-stage /app/dist /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
