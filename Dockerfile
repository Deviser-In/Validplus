# Use an official Python runtime as the base image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install dependencies in the system first
RUN pip install --no-cache-dir -r requirements.txt

# Create a virtual environment
RUN python -m venv /venv

# Set the virtual environment's bin directory to be the default for Python
ENV PATH="/venv/bin:$PATH"

# Copy the rest of the application code into the container
COPY . .

# Expose the port the app runs on
EXPOSE 80

# Command to run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
