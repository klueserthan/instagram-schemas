# Instagram Schemas

[![Python 3.13+](https://img.shields.io/badge/python-3.13+-blue.svg)](https://www.python.org/downloads/)
[![Pydantic v2](https://img.shields.io/badge/pydantic-v2-green.svg)](https://docs.pydantic.dev/)
[![Tests](https://img.shields.io/badge/tests-73%20passing-brightgreen.svg)](#testing)
[![Coverage](https://img.shields.io/badge/coverage-93%25-brightgreen.svg)](#testing)

A comprehensive Python package providing Pydantic v2 models for Instagram API data structures. Designed for robust data validation, type safety, and seamless MongoDB integration.

## 🚀 Features

- **🔍 Comprehensive Coverage**: Models for users, posts, stories, highlights, comments, media, and locations
- **🛡️ Type Safety**: Full Pydantic v2 validation with proper type hints
- **🗄️ MongoDB Ready**: Automatic `id` → `_id` field conversion for MongoDB compatibility
- **🔄 Flexible Input**: Accepts both camelCase (API) and snake_case data
- **📱 API Compatible**: Handles real Instagram API response formats
- **🧪 Well Tested**: 93% test coverage with unit and integration tests
- **🔧 Easy Integration**: Simple pip installation from GitHub

## 📦 Installation

### From GitHub (Recommended)

```bash
pip install git+https://github.com/yourusername/instagram-schemas.git
```

### Development Installation

```bash
git clone https://github.com/yourusername/instagram-schemas.git
cd instagram-schemas
pip install -e .[dev]
```

## 🏗️ Quick Start

### Basic Usage

```python
from instagram_schemas import InstagramUser, InstagramPost, InstagramComment

# Validate user data from Instagram API
user_data = {
    "id": "123456789",
    "username": "john_doe", 
    "full_name": "John Doe",
    "follower_count": 1250,
    "is_verified": True
}

user = InstagramUser.model_validate(user_data)
print(f"User: {user.username} ({user.follower_count} followers)")
```

### MongoDB Integration

The package automatically converts `id` fields to `_id` for MongoDB compatibility:

```python
from instagram_schemas import InstagramUserCore

# Input data (from API)
user_data = {"id": "user123", "username": "testuser"}
user = InstagramUserCore.model_validate(user_data)

# MongoDB storage (snake_case with _id)
mongodb_doc = user.model_dump()
# Output: {"username": "testuser", "full_name": "", "_id": "user123"}

# API response (camelCase with _id)
api_response = user.model_dump(by_alias=True)
# Output: {"username": "testuser", "fullName": "", "_id": "user123"}
```

### Flexible Input Formats

Models accept multiple input formats for maximum compatibility:

```python
from instagram_schemas import InstagramHighlight

# All of these work:
highlight1 = InstagramHighlight.model_validate({
    "highlight_id": "highlight123",  # Original API format
    "user": {"id": "user456", "username": "creator"}
})

highlight2 = InstagramHighlight.model_validate({
    "_id": "highlight456",  # MongoDB format
    "user": {"_id": "user789", "username": "creator2"}
})

highlight3 = InstagramHighlight.model_validate({
    "id": "highlight789",  # Standard format
    "user": {"id": "user123", "username": "creator3"}
})
```

## 📋 Available Models

### Core Models

- **`InstagramUserCore`** - Basic user information
- **`InstagramUser`** - Complete user profile with metrics
- **`InstagramPost`** - Post/feed content
- **`InstagramStory`** - Story containers
- **`InstagramStoryItem`** - Individual story media
- **`InstagramComment`** - Comments and replies
- **`InstagramHighlight`** - Story highlights
- **`InstagramMedia`** - Media items and carousels
- **`InstagramLocation`** - Location data

### Utility Models

- **`InstagramUserMetrics`** - Follower/following counts with timestamps
- **`InstagramMediaInfo`** - Media URLs and dimensions
- **`TaggedUser`** - Users tagged in media
- **`InstagramCaption`** - Post captions with entities

## 🔧 Advanced Usage

### Working with Real API Data

```python
from instagram_schemas import InstagramPost
import requests

# Fetch from Instagram API (example)
api_response = requests.get("https://api.instagram.com/posts/123")
post_data = api_response.json()

# Validate and parse
try:
    post = InstagramPost.model_validate(post_data)
    print(f"Post by {post.user.username}: {post.caption.text[:50]}...")
except ValidationError as e:
    print(f"Invalid data: {e}")
```

### Batch Processing for MongoDB

```python
from instagram_schemas import InstagramUserCore
from pymongo import MongoClient

# Process multiple users
api_users = [
    {"id": "user001", "username": "user1"},
    {"id": "user002", "username": "user2"},
    {"id": "user003", "username": "user3"}
]

# Validate and prepare for MongoDB
mongodb_docs = []
for user_data in api_users:
    user = InstagramUserCore.model_validate(user_data)
    mongodb_docs.append(user.model_dump())

# Insert into MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client.instagram_db
result = db.users.insert_many(mongodb_docs)
print(f"Inserted {len(result.inserted_ids)} users")
```

### Type Safety and IDE Support

```python
from instagram_schemas import InstagramUser

user = InstagramUser.model_validate(api_data)

# Full IDE autocomplete and type checking
if user.is_verified:
    print(f"✓ {user.username} is verified")

# Access metrics safely
latest_metrics = user.get_latest_metrics()
if latest_metrics:
    print(f"Followers: {latest_metrics.follower_count}")
```

## 🧪 Testing

The package includes comprehensive tests with high coverage:

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=instagram_schemas --cov-report=term-missing

# Run only MongoDB tests
pytest -m mongodb

# Run integration tests with real data
pytest -m integration
```

### Test Categories

- **Unit Tests**: Individual model validation (55 tests)
- **Integration Tests**: Real API data parsing (5 tests)
- **MongoDB Tests**: Serialization compatibility (18 tests)

## 🏗️ Architecture

### Base Model Design

All models inherit from `InstagramBase` which provides:

- Shared configuration (`ConfigDict`)
- Automatic `id` → `_id` serialization for MongoDB
- Consistent field naming conventions
- Common validation patterns

```python
from instagram_schemas.base import InstagramBase

class CustomModel(InstagramBase):
    # Inherits MongoDB serialization and config
    name: str = Field(..., description="Model name")
```

### Field Validation

Models include robust validation for common Instagram data patterns:

```python
# Automatic type conversion
user = InstagramUser.model_validate({
    "follower_count": "1250",  # String → int
    "is_verified": "true",     # String → bool
    "taken_at": 1640995200     # Timestamp → datetime
})
```

## 🔄 Migration Guide

### From v1 to v2

If upgrading from an earlier version:

1. **Import Changes**: All models now include MongoDB serialization
2. **Field Output**: `id` fields now serialize as `_id`
3. **Validation**: Enhanced type validation and error messages
4. **Configuration**: Shared base class with consistent settings

```python
# Before
user_dict = user.dict()  # Old method

# After  
user_dict = user.model_dump()  # New Pydantic v2 method
mongodb_doc = user.model_dump()  # Includes _id conversion
```

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/amazing-feature`)
3. **Add** tests for new functionality
4. **Ensure** all tests pass (`pytest`)
5. **Submit** a pull request

### Development Setup

```bash
git clone https://github.com/yourusername/instagram-schemas.git
cd instagram-schemas
pip install -e .[dev]
pre-commit install  # Optional: for code formatting
```

### Code Style

- Follow PEP 8
- Use type hints
- Add docstrings for public methods
- Maintain test coverage above 90%

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Pydantic**: For excellent data validation framework
- **Instagram**: For providing the API structure this models
- **Contributors**: Everyone who helped improve this package

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/yourusername/instagram-schemas/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/instagram-schemas/discussions)
- **Documentation**: [Full Documentation](https://yourusername.github.io/instagram-schemas/)

---

<div align="center">

**[⭐ Star this repository](https://github.com/yourusername/instagram-schemas)** if you find it useful!

Made with ❤️ for the Python community

</div>
