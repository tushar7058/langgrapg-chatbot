# Use a lightweight Python image
FROM python:3.11-slim

# Prevent Python from writing .pyc files and enable unbuffered logging
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# Install uv for faster dependency installation
RUN pip install --no-cache-dir uv

# Set the working directory
WORKDIR /app

# Copy dependency definitions
COPY pyproject.toml ./

# Install dependencies into the system environment
RUN uv pip install --system -r pyproject.toml

# Copy the rest of the application
COPY . /app

# Streamlit runs on 8501 by default
EXPOSE 8501

# Command to run the application
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
