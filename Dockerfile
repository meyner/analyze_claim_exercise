FROM python:3.12-slim-bookworm

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Set the working directory
WORKDIR /app

# Enable bytecode compilation
ENV UV_COMPILE_BYTECODE=1

# Copy from the cache instead of linking since it's a container
ENV UV_LINK_MODE=copy

# Install dependencies first to leverage Docker's cache
# We use --no-install-project because the source code isn't copied yet
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-install-project --no-dev

# Copy the rest of the application code
COPY src ./src
COPY README.md ./

# Now install the project itself
RUN uv sync --frozen --no-dev

# Place /app/src on the PYTHONPATH
ENV PYTHONPATH=/app/src

# Expose the port the app runs on
EXPOSE 8000

# Run the application
CMD ["uv", "run", "python", "src/main.py"]
