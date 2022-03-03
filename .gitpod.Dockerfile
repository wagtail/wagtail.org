FROM gitpod/workspace-full

# Use Buildkit
# This allows us to use a 'dev' target in the Dockerfile to skip production-only tasks such as compressing static
ENV COMPOSE_DOCKER_CLI_BUILD=1
ENV DOCKER_BUILDKIT=1
