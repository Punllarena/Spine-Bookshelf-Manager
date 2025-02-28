# use a smaller base image
FROM python:3.12-alpine

# Set the working directory to /app
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install the dependencies
RUN pip install -r requirements.txt

# Copy the application code into the container
COPY . .

# Create the instance directory
VOLUME /src/instance

# Expose the port that your application will use
EXPOSE 5000

# Run the command to start the application when the container launches
CMD ["python", "main.py", "--host=0.0.0.0", "--port=5000"]