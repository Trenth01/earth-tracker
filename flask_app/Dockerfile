# Use the official Python image
FROM python:3.10-slim-bullseye

# Set the working directory
WORKDIR /app

# Copy the application code to the container
COPY . .

# Install dependencies
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt --progress-bar off

# Expose the port the app runs on
EXPOSE 5000

# Run the application
CMD ["python", "app.py"]
