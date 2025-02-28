# Spine-Bookshelf-Manager

 A Flask Web-App that collects book details from Google Books API and Saves them to a Collection

## Development

create a virtual environment

```bash
python3 -m venv venv
source venv/bin/activate
```

install dependencies

```bash
pip install -r requirements.txt
```

Provide the API key in the `.env` file, it uses Google Books API

Run the application

```bash
python app.py
```

## Dockerizing

Change the `app.run` contents to the following

```python
app.run(host='0.0.0.0', port=5000)
```

This will allow the container to listen on all interfaces

Build the docker image

```bash
docker build -t spine-bookshelf-manager .
```

To view the images

```bash
docker images
```

Create a Volume

```bash
docker volume create spine-bookshelf-manager
```

To run the container in the background with the volume attached

```bash
docker run -d -p 5000:5000 -v spine-bookshelf-manager:/src/instance --name spine-bookshelf-manager spine-bookshelf-manager 
```

To view if the container is currently running

```bash
docker ps
```

To stop the container

```bash
docker stop spine-bookshelf-manager
```

To remove the container

```bash
docker rm spine-bookshelf-manager
```

To remove the image

```bash
docker rmi spine-bookshelf-manager
```

Remove all unused containers, networks, images (both dangling and unused), and optionally, volumes.

```bash
docker container prune
```
