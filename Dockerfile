# Use official Python 3.12 Alpine base image for a small size and the latest Python version
FROM python:3.12-alpine

# Set the working directory inside the container
WORKDIR /app

# Install system build dependencies required for installing packages
RUN apk add --no-cache build-base gcc libffi-dev musl-dev curl

# Install PDM (Python Development Master) globally
RUN pip install pdm

# Install all dependencies, including both production and development (test) dependencies
RUN pdm install --prod --dev

# Set environment variables for module resolution and virtual environment
ENV PYTHONPATH=/app
ENV PATH="/app/.venv/bin:$PATH"

# Expose port 8000 for the FastAPI app (this is the port that uvicorn will bind to)
EXPOSE 8000

# Default command to run the FastAPI application using uvicorn with hot reloading enabled
CMD ["pdm", "run", "uvicorn", "bowie_api_rest.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
