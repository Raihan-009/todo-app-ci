FROM node:16-alpine
WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy public and src directories
COPY public/ public/
COPY src/ src/

# Build the app
RUN npm run build

EXPOSE 3000

# Start the service
CMD ["npx", "serve", "-s", "build", "-l", "3000"]