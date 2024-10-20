FROM node:20-bookworm-slim as build

# Environment variables
ENV PNPM_HOME=/pnpm
ENV PATH=${PNPM_HOME}:${PATH}
RUN corepack enable

# Copy package.json and pnpm-lock.yaml
WORKDIR /app
COPY package.json pnpm-lock.yaml /app/

# Install node modules
RUN pnpm install --frozen-lockfile

# Environment variables for the vite build
ARG VITE_BACKEND_URL
ENV VITE_BACKEND_URL=${VITE_BACKEND_URL}

# Add the rest of the source code and build the app; this is done last to take
# advantage of Docker's layer caching mechanism
COPY . /app/
RUN pnpm build

# Nginx wrapper to serve static files
FROM nginx:stable
COPY --from=build /app/dist /usr/share/nginx/html
EXPOSE 80
CMD [ "nginx", "-g", "daemon off;" ]
