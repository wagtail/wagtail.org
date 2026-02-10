# Development Guide for Agentic Coding Agents

This guide provides essential information for agentic coding agents working on the wagtail.org repository. It covers build commands, testing procedures, and code style guidelines.

## Build Commands

### Frontend (JavaScript/CSS)

```bash
# Install dependencies
npm install

# Build for development
npm run build

# Build for production
npm run build:prod

# Start development server with watch mode
npm run start

# Start development server with hot reloading
npm run start:reload
```

### Backend (Python/Django)

```bash
# Install Python dependencies using Poetry
poetry install

# Build Docker containers
make build

# Setup the application (build + migrations)
make setup

# Start Docker containers
make start

# Run Django development server
make runserver
```

## Linting and Formatting Commands

### Pre-commit Hooks (Recommended)

```bash
# Run all pre-commit hooks on all files
pre-commit run --all-files

# Run specific hooks
pre-commit run ruff --all-files          # Python linting and formatting
pre-commit run prettier --all-files      # General file formatting
pre-commit run eslint --all-files        # JavaScript linting
pre-commit run stylelint --all-files     # CSS/Sass linting
pre-commit run djhtml --all-files        # Django template formatting
```

### Individual Linting Tools

```bash
# JavaScript/TypeScript linting
npm run lint:js
# or
eslint --ext .js,.ts,.tsx --report-unused-disable-directives .

# CSS/Sass linting
npm run lint:css
# or
stylelint --report-needless-disables './wagtailio/static/sass'

# General formatting check
npm run lint:format
# or
prettier --check '**/?(.)*.{md,css,scss,js,ts,tsx,json,yaml,yml}'

# Run all linting checks
npm run lint

# Apply formatting fixes
npm run format
# or
prettier --write '**/?(.)*.{md,css,scss,js,ts,tsx,json,yaml,yml}'
```

### Python Linting and Formatting

```bash
# Using Ruff for Python linting and fixing
ruff check .
ruff check --fix .

# Using Ruff for Python formatting
ruff format .

# Using pre-commit for Python
pre-commit run ruff --all-files
pre-commit run ruff-format --all-files
```

### Django Template Formatting

```bash
# Format Django templates
pre-commit run djhtml --all-files
# or
djhtml **/*.html
```

## Testing Commands

Testing in this codebase is primarily done through Django's testing framework:

```bash
# Run all tests (within Docker container)
docker-compose run web django-admin test

# Run tests for a specific app
docker-compose run web django-admin test blog
docker-compose run web django-admin test features
docker-compose run web django-admin test newsletter
docker-compose run web django-admin test standardpage

# Run a specific test file
docker-compose run web django-admin test blog.tests.BlogTests

# Run tests with coverage
docker-compose run web coverage run --source='.' manage.py test

# Run tests with verbosity
docker-compose run web django-admin test --verbosity=2
```

Note: Tests are executed within the Docker environment as configured in docker-compose.yml.

## Code Style Guidelines

### General Principles

-   Follow existing code patterns and conventions
-   Maintain consistency with the current codebase
-   Prioritize readability and maintainability
-   Write self-documenting code with descriptive names

### JavaScript/TypeScript

#### Imports

-   Use ES6 import/export syntax
-   Group imports in logical blocks (external libraries, internal modules)
-   Sort imports alphabetically within groups
-   Use absolute imports when possible for internal modules

#### Formatting

-   Follow Prettier configuration (single quotes, trailing commas, etc.)
-   Line width: 80 characters
-   Use semicolons
-   Consistent arrow function parentheses

#### Naming Conventions

-   camelCase for variables and functions
-   PascalCase for classes and constructors
-   UPPER_CASE for constants
-   Descriptive names that convey purpose

#### Error Handling

-   Use try/catch blocks appropriately
-   Prefer specific error handling over generic catches
-   Log meaningful error messages for debugging

### Python/Django

#### Imports

-   Follow isort configuration with section order:
    1. Future imports
    2. Standard library
    3. Django
    4. Wagtail
    5. Third-party
    6. First-party (wagtailio)
    7. Local folder
-   Separate import sections with two blank lines
-   Sort imports alphabetically within sections

#### Formatting

-   Use Ruff formatter for consistent Python code style
-   No line length restrictions (E501 disabled)
-   Use double quotes for strings unless single quotes are needed
-   Consistent spacing around operators

#### Naming Conventions

-   snake_case for variables, functions, and methods
-   PascalCase for classes
-   UPPER_CASE for constants
-   Descriptive variable names that explain their purpose

#### Type Hints

-   Use type hints for function parameters and return values
-   Include type hints for class attributes when beneficial
-   Follow PEP 484 guidelines

#### Error Handling

-   Handle exceptions with specific except blocks
-   Use Django's logging framework for error reporting
-   Provide meaningful error messages for debugging
-   Follow Django's exception handling patterns

### CSS/Sass

#### Organization

-   Follow BEM methodology for class naming
-   Organize styles by components/modules
-   Use Sass mixins and variables for reusable code
-   Keep specificity as low as possible

#### Formatting

-   Use SCSS syntax
-   One selector per line for comma-separated selectors
-   Consistent indentation (2 spaces)
-   Meaningful class names that describe purpose

#### Naming Conventions

-   kebab-case for class names
-   Use descriptive names that indicate purpose/function
-   Prefix utility classes with u-
-   Prefix component classes with c-
-   Prefix layout classes with l-

### Django Templates

#### Formatting

-   Use djhtml for consistent template formatting
-   Two space indentation
-   Logical grouping of blocks and includes
-   Comments for complex template logic

#### Best Practices

-   Use template tags and filters when possible
-   Minimize logic in templates
-   Use template inheritance for consistent layouts
-   Cache expensive template fragments

## Branching and Workflow

1. Create feature branches from main
2. Keep commits focused and atomic
3. Write meaningful commit messages
4. Run linting and formatting before committing
5. Ensure code passes existing tests
6. Submit pull requests for review

## Environment Setup

1. Use Docker for consistent development environment
2. Install pre-commit hooks for automated linting/formatting
3. Ensure all dependencies are properly installed
4. Follow README.md for initial setup instructions

## Additional Notes

-   This project uses both Python (Django/Wagtail) for backend and JavaScript/CSS for frontend
-   Development is containerized using Docker for consistency
-   Pre-commit hooks enforce code quality standards automatically
-   CI/CD pipelines will run all linting and tests on pull requests
