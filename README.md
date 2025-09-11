# FastAPI FS Router

A library for automatically loading routers in FastAPI applications based on file system structure.

English | [한국어](README_ko.md)

## Features

- 📁 Automatically loads routers based on the file system structure
- 🔗 Maps directory structure directly to API paths
- 🎯 Detects and registers APIRouter instances automatically
- ⚙️ Supports custom prefixes for all routes
- 🚀 Prevents duplicate router registration
- 🛣️ Supports path parameters and route groups

## Installation

```bash
pip install fastapi-fs-router
```

## Usage

### Basic Usage

```python
from fastapi import FastAPI
from fastapi_fs_router import load_fs_router

app = FastAPI()

# Automatically load all routers from the routers directory
load_fs_router(app, "routers")
```

### Directory Structure Example

```
routers/
├── users.py          # Maps to /users path
├── items.py          # Maps to /items path
└── v1/
    └── admin/
        └── users.py  # Maps to /v1/admin/users path
```

### Router File Example

```python
# routers/users.py
from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def get_users():
    return {"users": []}

@router.get("/{user_id}")
def get_user(user_id: int):
    return {"user_id": user_id}
```

### Using Custom Prefix

```python
from fastapi import FastAPI
from fastapi_fs_router import load_fs_router

app = FastAPI()

# Add /api/v1 prefix to all routers
load_fs_router(app, "routers", prefix="/api/v1")
```

In this case, routers will be mapped as follows:
- `routers/users.py` → `/api/v1/users`
- `routers/v1/admin/users.py` → `/api/v1/v1/admin/users`
- `routers/(empty)/admin/users.py` → `/api/admin/users`
- `routers/hello_world/admin/hello_world.py` → `/hello-world/admin/hello-world`
- `routers/{path_param}/admin.py` → `/{path_param}/admin`

### Path Transformation Rules

- Underscores (`_`) are converted to hyphens (`-`) except for path parameters
- Square brackets are converted to curly braces (e.g., `[id]` → `{id}`)
- Parentheses are ignored (e.g., `(empty)`)

## API Reference

### `load_fs_router(app, route_dir, *, prefix="")`

Loads file system-based routers into a FastAPI application.

**Parameters:**
- `app` (FastAPI): FastAPI application instance
- `route_dir` (Path | str): Directory path containing router files (default: "routers")
- `prefix` (str): Prefix to add to all routers (default: "")

**Behavior:**
1. Recursively traverses the specified directory
2. Finds `APIRouter` instances in `.py` files
3. Generates API paths based on directory structure
4. Registers routers with the FastAPI app

## Development

### Install Dependencies

```bash
# Install development dependencies
uv sync
```

### Run Tests

```bash
# Run all tests
uv run pytest
```

### Code Quality Checks

```bash
# Linting
ruff check src/ tests/

# Formatting
ruff format src/ tests/
```

## License

This project is licensed under the Apache License 2.0. See the [LICENSE](LICENSE) file for details.

## Contributing

Bug reports, feature requests, and pull requests are welcome! Please create an issue first before contributing.

## Author

- **owjs3901** - *Initial work* - [owjs3901@gmail.com](mailto:owjs3901@gmail.com)