# Use an official Python runtime as a parent image
FROM python:3.10

# Set the working directory to /app
WORKDIR /app

# Copy the requirements file into the container at /app
COPY requirements.txt /app/
# Udating pip
RUN pip install --upgrade pip
# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code into the container
COPY . /app/

# Expose port 8000 for the Django app
EXPOSE 8000

# Define environment variable for Django settings module (optional, but recommended)
# If you're using a specific settings file, replace 'your_project.settings'
# ENV DJANGO_SETTINGS_MODULE=your_project.settings

# # Run migrations
# RUN  python manage.py makemigrations
# RUN  python manage.py migrate

# # Start the Django development server (you might need to adjust the command for production)
CMD ["./wait-for-it.sh", "db:3306", "--","python", "manage.py", "runserver", "0.0.0.0:8000"]
