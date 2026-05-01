FROM python:3.11-slim

# Install system dependencies for OpenCV and MediaPipe
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

# Copy dependency files first for better caching
COPY pyproject.toml uv.lock ./

# Install dependencies using uv
RUN uv sync --frozen

# Copy the rest of the application
COPY src ./src
COPY yolov8n.pt .

# Ensure the logs directory exists
RUN mkdir -p logs

# Set the path to include uv's virtual environment
ENV PATH="/app/.venv/bin:$PATH"

# Run the application
CMD ["uv", "run", "src/main.py"]
