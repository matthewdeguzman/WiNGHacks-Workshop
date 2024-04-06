From node:20.11.1

WORKDIR /app

COPY package*.json ./

RUN npm install

COPY . . 

RUN npm run build

EXPOSE 5173

CMD ["npm", "run", "dev", "--", "--host", "--port", "5173"]
