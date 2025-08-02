# Use official Python 3.12 Alpine base image for small size and latest Python version
FROM python:3.12-alpine

# Set the working directory inside the container
WORKDIR /app

# Install system build dependencies required for installing packages
RUN apk add --no-cache build-base gcc libffi-dev musl-dev curl jq

# Install PDM (Python Development Master) globally
RUN pip install pdm

# Copy the full project into the container
COPY . /app

# Install only production dependencies
RUN pdm install --prod

# Set environment variables for module resolution and virtual environment
ENV PYTHONPATH=/app
ENV PATH="/app/.venv/bin:$PATH"

# Expose port 8000 for the FastAPI app
EXPOSE 8000

# Default command to run the FastAPI application with uvicorn
CMD ["pdm", "run", "uvicorn", "bowie_api_rest.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
