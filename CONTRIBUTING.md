# Contributing to django-generic-links

Thank you for considering contributing! ❤️

## Getting Started

**Prerequisites:** Python 3.10+ and [Hatch](https://hatch.pypa.io/)

```bash
# Clone the repository
git clone https://github.com/matagus/django-generic-links.git
cd django-generic-links

# Install Hatch
pip install hatch

# Install pre-commit hooks
pip install pre-commit
pre-commit install
```

## Development Workflow

### Running the Example Project

The example project demonstrates how to integrate django-generic-links with a music app (Artist and Album models).

```bash
# Run migrations
hatch run project:migrate

# Start the development server
hatch run project:server
```

Visit http://127.0.0.1:8000/admin/ to test the app with a populated admin.

### Interactive Shell

```bash
hatch run project:shell
```

This uses `django-extensions` shell_plus for an enhanced interactive experience.

### Running Tests

```bash
# All Python + Django combinations
hatch run test:test

# Specific version
hatch run test.py3.14-5.2:test

# With coverage
hatch run test:cov
```

**Available test environments:**

- Python 3.10-3.12 with Django 4.2
- Python 3.10-3.13 with Django 5.0
- Python 3.10-3.14 with Django 5.1
- Python 3.10-3.14 with Django 5.2

View all environments: `hatch env show test`

### Code Style

We use Ruff for linting and Black for formatting. Pre-commit hooks will automatically format your code.

**Line length:** 120 characters

**Install pre-commit:**
```bash
pip install pre-commit

# Set up git hooks
pre-commit install

# Run hooks manually on all files
pre-commit run --all-files
```

**Pre-commit checks include:**
- Ruff (linting with auto-fix)
- Black (formatting)
- Standard checks (trailing whitespace, YAML validation, etc.)
- Codespell
- Pyupgrade (Python 3.10+ syntax)

## Pull Request Guidelines

1. **Fork and branch**: Create a feature branch from `main`
2. **Write tests**: Add tests for new features or bug fixes
3. **Update docs**: Update README.md and docs/ if adding features
4. **Keep it focused**: One feature/fix per PR
5. **Test thoroughly**: Ensure tests pass for all Python/Django versions
6. **Follow code style**: Pre-commit hooks will help with this

## Project Structure

```
generic_links/              # Main app package
├── models.py              # GenericLink model
├── managers.py            # Custom QuerySet
├── admin.py               # Admin classes and inlines
├── forms.py               # Forms (if needed)
├── utils.py               # Helper functions
├── templatetags/          # Template tag library
│   └── generic_links_tags.py
├── migrations/            # Database migrations
└── urls.py                # URL patterns (if any)

tests/                     # Test suite
├── settings.py            # Test settings
├── test_models.py         # Model tests
├── test_managers.py       # Manager/QuerySet tests
├── test_forms.py          # Form tests
└── test_templatetags.py   # Template tag tests

example_project/           # Working example
└── music_app/             # Example integration (Artist/Album models)

docs/                      # MkDocs documentation
└── *.md                   # Documentation pages
```

## Useful Links

- **Repository**: https://github.com/matagus/django-generic-links
- **Issues**: https://github.com/matagus/django-generic-links/issues
- **PyPI**: https://pypi.org/project/django-generic-links/

## Questions?

Open an issue for discussion before starting major changes. We're here to help!
