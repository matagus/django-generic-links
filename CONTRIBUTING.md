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

```bash
hatch run project:migrate
hatch run project:createsuperuser
hatch run project:runserver
```

Visit http://127.0.0.1:8000/admin/ to test the app with a populated admin.

### Running Tests

```bash
# All Python + Django combinations
hatch run test:test

# Specific versions: Python 3.14 and Django 5.2
hatch run test.py3.14-5.2:test

# With coverage
hatch run test:cov
```

### Code Style

We use Ruff and Black. Pre-commit hooks will automatically format your code.

```bash
# Install pre-commit
pip install pre-commit

# Set up git hooks
pre-commit install

# Run hooks manually on all files
pre-commit run --all-files
```

## Pull Request Guidelines

1. **Fork and branch**: Create a feature branch from `main`
2. **Write tests**: Add tests for new features or bug fixes
3. **Update docs**: Update README.md if adding features
4. **Keep it focused**: One feature/fix per PR
5. **Test thoroughly**: Ensure tests pass for all Python/Django versions

## Useful Links

- **Repository**: https://github.com/matagus/django-generic-links
- **Issues**: https://github.com/matagus/django-generic-links/issues
- **Discussions**: https://github.com/matagus/django-generic-links/discussions

## Questions?

Open an issue for discussion before starting major changes. We're here to help!
