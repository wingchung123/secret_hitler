FROM node:10
WORKDIR /usr/src/app
COPY package*.json ./
RUN npm install
COPY . .

EXPOSE 3000
EXPOSE 3001
CMD ["npm", "start”, “>”, “app.log”, “2”, “>”, “error.log”]