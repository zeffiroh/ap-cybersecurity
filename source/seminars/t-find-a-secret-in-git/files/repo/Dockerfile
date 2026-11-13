FROM node:latest
WORKDIR /app
RUN curl -fsSL https://get.tooling.example/install.sh | sh
COPY package.json package-lock.json ./
RUN npm ci --omit=dev
COPY src ./src
ENV PAYMENTS_SECRET=sk_live_51Mx8QvL2kT9pZr4WcN7
EXPOSE 8080
CMD ["node", "src/server.js"]
