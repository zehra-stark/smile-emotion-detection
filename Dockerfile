# Use official Python base image
FROM python:3.11-slim

# Set working directory inside the container
WORKDIR /app

# Copy requirements.txt and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all project files into the container
COPY . .

# Expose the port that Streamlit will run on
EXPOSE 8080

# Run Streamlit app
CMD ["streamlit", "run", "main.py", "--server.port=8080", "--server.address=0.0.0.0"]
