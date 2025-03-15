# Use an official Python runtime as a parent image
FROM python:3.10.12-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install dependencies
RUN pip install -r requirements.txt

# Copy the project files into the container
COPY . .

# Expose the port the app runs on
EXPOSE 8000


# Run migrations and collect static files (if applicable)
RUN python3 manage.py makemigrations
RUN python3 manage.py migrate

# Start the application
CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]

