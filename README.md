# Recipe App API

This project is a Recipe App API built using Python, Django, Django REST Framework, and Docker. It provides a backend for managing recipes, including functionalities like user authentication, recipe creation, and more.

## Features

- **User Authentication**: Secure user registration and login functionalities.
- **Recipe Management**: Create, read, update, and delete recipes.
- **Ingredient Management**: Manage ingredients associated with recipes.
- **Tagging**: Categorize recipes using tags.
- **Image Upload**: Upload images for recipes.

## Getting Started

### Prerequisites

Ensure you have the following installed:

- [Docker](https://www.docker.com/get-started)
- [Docker Compose](https://docs.docker.com/compose/install/)

### Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/Rabiya-Kamran/Recipe-App-Api.git
   cd Recipe-App-Api
   ```

2. **Build and Start the Docker Containers**:
   ```bash
   docker-compose up --build
   ```

3. **Apply Migrations**:
   ```bash
   docker-compose run --rm app sh -c "python manage.py migrate"
   ```

4. **Create a Superuser** (Optional):
   ```bash
   docker-compose run --rm app sh -c "python manage.py createsuperuser"
   ```

5. **Collect Static Files**:
   ```bash
   docker-compose run --rm app sh -c "python manage.py collectstatic --noinput"
   ```

6. **Access the Application**:
   - API: `http://127.0.0.1:8000/`
   - Admin Panel: `http://127.0.0.1:8000/admin/`
   - API Endpoints are prefixed with `/api/`

## Running Tests

To run the test suite:
```bash
docker-compose run --rm app sh -c "python manage.py test"
```

## Project Structure

- **app/**: Main application code (models, views, serializers, URLs, etc.).
- **Dockerfile**: Defines the Docker image configuration.
- **docker-compose.yml**: Configures the Docker services.
- **requirements.txt**: Lists project dependencies.

## Environment Variables

Set up a `.env` file with:
```ini
DEBUG=1
SECRET_KEY=your_secret_key
DB_HOST=db
DB_NAME=your_db_name
DB_USER=your_db_user
DB_PASS=your_db_password
```

## Contributing

Contributions are welcome! Open an issue or submit a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
