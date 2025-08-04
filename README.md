# Air Demo - Address Management Application

A demonstration application showcasing the [Air web framework](https://github.com/air-framework/air) with FastAPI integration, built with Python and managed with [uv](https://github.com/astral-sh/uv).

## Features

- 📝 **Address Form** with Pydantic validation
- 📋 **Address List** with live search functionality
- 🔄 **HTMX Integration** for dynamic updates without page reloads
- 🎨 **Clean UI** with PicoCSS styling
- 🚀 **FastAPI Integration** for REST API endpoints
- 💾 **In-memory storage** for demo purposes

## Prerequisites

- Python 3.8 or higher
- [uv](https://github.com/astral-sh/uv) - Fast Python package installer and resolver

## Installation with uv

### 1. Install uv (if not already installed)

```bash
# On macOS and Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# On Windows
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# Or using pip
pip install uv
```

### 2. Clone the repository

```bash
git clone https://github.com/ndanielsen/air-address-demo.git
cd air-address-demo
```

### 3. Create a virtual environment with uv

```bash
uv venv
```

### 4. Activate the virtual environment

```bash
# On macOS and Linux
source .venv/bin/activate

# On Windows
.venv\Scripts\activate
```

### 5. Install dependencies

```bash
uv pip install -r pyproject.toml
```

Or if you're using a requirements.txt:

```bash
uv pip install -r requirements.txt
```

## Running the Application

### Development Server

```bash
uvicorn main:app --reload
```

The application will be available at `http://localhost:8000`

### Production Server

```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

## Application Structure

```
air_demo/
├── main.py              # Main application file
├── pyproject.toml       # Project configuration and dependencies
├── README.md           # This file
└── templates/          # Jinja2 templates (if any)
    └── home.html
```

## Usage

### Web Interface

1. **Home Page** (`/`): Welcome page with navigation to all features
2. **Address Form** (`/address`): Add new addresses with validation
3. **Address List** (`/addresses`): View, search, and delete addresses
4. **API Root** (`/api`): Access the REST API

### API Endpoints

- `GET /api/` - API welcome message
- `GET /api/addresses` - Get all addresses in JSON format
- `POST /api/addresses` - Create a new address via API
- `GET /api/docs` - FastAPI automatic documentation

### Features Demonstration

#### Adding an Address
1. Navigate to "Address Form" from the navigation menu
2. Fill in all required fields:
   - Street Address
   - City
   - State/Province
   - ZIP/Postal Code
   - Country (defaults to "USA")
3. Click "Submit" - the form uses HTMX for seamless submission

#### Searching Addresses
1. Go to "Address List"
2. Type in the search box - results filter in real-time
3. Search works across all address fields

#### Deleting Addresses
1. Click the "Delete" button next to any address
2. Confirm the deletion when prompted

## Development with uv

### Adding new dependencies

```bash
# Add a new package
uv pip install package-name

# Add to pyproject.toml or requirements.txt
uv pip freeze > requirements.txt
```

### Updating dependencies

```bash
# Update all packages
uv pip install --upgrade-package package-name

# Or update all
uv pip install -r requirements.txt --upgrade
```

### Creating a lock file

```bash
# Generate uv.lock for reproducible installs
uv pip compile pyproject.toml -o requirements.txt
```

## Project Dependencies

The project uses the following main dependencies:
- **air**: The web framework for building HTML with Python
- **fastapi**: Modern web API framework
- **uvicorn**: ASGI server for running the application
- **pydantic**: Data validation using Python type annotations

## Tips for Development

1. **Hot Reload**: Use `--reload` flag with uvicorn during development
2. **API Documentation**: Visit `/api/docs` for interactive API documentation
3. **HTMX Debugging**: Check browser console for HTMX events
4. **Form Validation**: All fields are required with minimum length validation

## Troubleshooting

### Common Issues

1. **Port already in use**
   ```bash
   # Use a different port
   uvicorn main:app --port 8001
   ```

2. **Module not found errors**
   ```bash
   # Ensure virtual environment is activated
   # Reinstall dependencies
   uv pip install -r pyproject.toml
   ```

3. **Static files not loading**
   - Check that PicoCSS CDN is accessible
   - Verify HTMX CDN is not blocked

## Contributing

Feel free to submit issues and enhancement requests!

## License

This is a demo project for educational purposes.
