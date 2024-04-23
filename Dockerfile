# Use Python 3.12.3 as a parent image
FROM python:3.12.3-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /app

# Install Python dependencies
COPY CN_Auction/requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the Django project files into the container
COPY CN_Auction /app/CN_Auction/

# Run Django migrations (assuming you're using SQLite for development)
RUN python manage.py migrate

# Collect static files
RUN python manage.py collectstatic --no-input

# Expose port 8000
EXPOSE 8000

# Run the Django development server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]