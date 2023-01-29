# Webpage crawler

## Running

1. Install Docker Compose

2. Initialize the app:
    ```bash
    docker-compose run app ./manage.py migrate
    ```
3. Start the application:
    ```bash
    docker-compose up
    ```

4. Crawler interface will be available at http://localhost:8000/

## Running tests

```bash
docker-compose run app pytest --cov
```
