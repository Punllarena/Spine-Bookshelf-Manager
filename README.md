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

<!-- Provide the API key in the `.env` file, it uses Google Books API -->

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

Update the version within the `docker-compose.yml` file

```yaml
VERSION=vYYMMDD.rX
```

YY = Year, MM = Month, DD = Day, X = Build Number

Build the image

Method 1

```bash
docker-compose build
```

Run the container

```bash
docker-compose up -d
```

To remove existing container(if it exists)

```bash
docker-compose down
```

Method 2: Rebuild and Restart Container (if it exists)

```bash
docker-compose up --build -d
```
