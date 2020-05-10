FROM node:10
WORKDIR /usr/src/app
COPY package*.json ./
RUN npm install
RUN npm install pm2 -g
COPY . .

EXPOSE 3000
EXPOSE 3001
CMD ["npm", "start",">","npm_app.log", "2>", "npm_error.log"]