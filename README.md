# E-commerce Hybrid API

A professional, production-ready REST API for e-commerce platforms built with FastAPI, supporting both SQL (SQLite/PostgreSQL) and MongoDB databases.

## Tech Stack

- **Framework**: FastAPI 0.124.0
- **Web Server**: Uvicorn 0.38.0
- **SQL Database**: SQLAlchemy 2.0.44 (SQLite/PostgreSQL)
- **NoSQL Database**: MongoDB with Motor async driver
- **Authentication**: JWT with python-jose and bcrypt
- **File Storage**: AWS S3 integration via boto3
- **Email**: FastAPI-Mail for email notifications
- **Validation**: Pydantic 2.12.5

## Features

- ✅ User authentication with JWT tokens
- ✅ Product management with image uploads
- ✅ Shopping cart with order management
- ✅ Product categories and filtering
- ✅ Email notifications
- ✅ AWS S3 file storage support
- ✅ SQL and MongoDB database support
- ✅ RESTful API with OpenAPI documentation
- ✅ CORS enabled for frontend integration

## Project Structure

```
├── app/
│   ├── crud/              # Database operations
│   ├── models/            # SQLAlchemy models
│   ├── routers/           # API endpoints
│   ├── schemas/           # Pydantic schemas
│   └── utils/             # Utility functions
├── uploads/               # User-uploaded files directory
├── database.py            # SQL database configuration
├── mongo_database.py      # MongoDB configuration
├── main.py                # Application entry point
├── requirements.txt       # Python dependencies
├── Dockerfile             # Docker configuration
└── .env                   # Environment variables (create this)
```

## Installation

### Prerequisites

- Python 3.9+
- MongoDB (optional, for NoSQL features)
- AWS credentials (optional, for S3 uploads)

### Setup

1. **Clone and navigate to project**
   ```bash
   cd CRUD
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Create `.env` file** with required variables:
   ```env
   DATABASE_URL=sqlite:///./ecommerce.db
   MONGO_URL=mongodb://localhost:27017
   
   # Email configuration
   MAIL_USERNAME=your-email@gmail.com
   MAIL_PASSWORD=your-app-password
   MAIL_FROM=noreply@ecommerce.com
   
   # AWS S3 (optional)
   AWS_ACCESS_KEY_ID=your-key
   AWS_SECRET_ACCESS_KEY=your-secret
   REGION=us-east-1
   
   # JWT
   SECRET_KEY=your-secret-key-here-change-in-production
   ALGORITHM=HS256
   ```

## Running the Application

### Development

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Production

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

### Docker

```bash
docker build -t ecommerce-api .
docker run -p 8000:8000 --env-file .env ecommerce-api
```

## API Documentation

Once running, access:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## API Endpoints

### Products
- `GET /products/` - List all products
- `GET /products/search/` - Search products
- `GET /products/filter/` - Filter products
- `GET /products/{id}` - Get product details
- `POST /products/` - Create product
- `PUT /products/{id}` - Update product
- `DELETE /products/{id}` - Delete product

### Users
- `POST /users/register` - Register new user
- `POST /users/login` - Login user
- `GET /users/me` - Get current user
- `PUT /users/{id}` - Update user
- `DELETE /users/{id}` - Delete user

### Cart
- `GET /cart/` - Get cart items
- `POST /cart/add-item` - Add item to cart
- `PUT /cart/update-item/{item_id}` - Update item quantity
- `DELETE /cart/remove-item/{item_id}` - Remove item from cart
- `POST /cart/checkout` - Checkout and create order

### Categories
- `GET /catgory/` - List all categories
- `POST /catgory/` - Create category
- `PUT /catgory/{id}` - Update category
- `DELETE /catgory/{id}` - Delete category

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `DATABASE_URL` | SQL database connection string | `sqlite:///./ecommerce.db` |
| `MONGO_URL` | MongoDB connection string | `mongodb://localhost:27017` |
| `SECRET_KEY` | JWT secret key | Required for production |
| `ALGORITHM` | JWT algorithm | `HS256` |
| `AWS_ACCESS_KEY_ID` | AWS access key | Optional |
| `AWS_SECRET_ACCESS_KEY` | AWS secret key | Optional |
| `MAIL_USERNAME` | Email sender username | Optional |
| `MAIL_PASSWORD` | Email sender password | Optional |

## Development

### Code Quality

- Follows PEP 8 style guidelines
- Type hints throughout the codebase
- Clean separation of concerns
- RESTful API design patterns

### Database Migrations

For SQLAlchemy models, ensure models are imported in `app/models/__init__.py` before running the app. Database tables are created automatically on startup.

## Troubleshooting

### Port Already in Use
```bash
lsof -i :8000
kill -9 <PID>
```

### Database Connection Issues
- Verify `DATABASE_URL` in `.env`
- For SQLite: ensure `uploads/` directory exists
- For MongoDB: verify MongoDB is running

### Import Errors
```bash
pip install -r requirements.txt --upgrade
```

## License

Proprietary - Internal Use Only

## Support

For issues or questions, contact the development team.
