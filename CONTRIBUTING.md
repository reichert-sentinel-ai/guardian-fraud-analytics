# Contributing Guidelines

**Repository**: Sentinel Analytics (Guardian, Foresight, Cipher)  
**Date**: December 2024  
**Status**: Complete

---

## Welcome Contributors! 🎉

Thank you for your interest in contributing to Sentinel Analytics projects. These guidelines will help you understand how to contribute effectively.

---

## Code of Conduct

### Our Pledge

We are committed to providing a welcoming and inclusive environment for all contributors, regardless of experience level, gender identity, nationality, personal appearance, race, religion, or sexual identity and orientation.

### Our Standards

- **Be respectful**: Treat others with respect and kindness
- **Be collaborative**: Work together to achieve common goals
- **Be constructive**: Provide helpful feedback and suggestions
- **Be professional**: Maintain professional communication

---

## How to Contribute

### Reporting Bugs

1. **Check existing issues**: Search GitHub issues to see if the bug has already been reported
2. **Create a new issue**: If not found, create a new issue with:
   - Clear title and description
   - Steps to reproduce
   - Expected vs actual behavior
   - Environment details (OS, Python version, etc.)
   - Screenshots/logs if applicable

### Suggesting Enhancements

1. **Check existing issues**: Search for similar enhancement requests
2. **Create an enhancement issue**: Include:
   - Clear description of the enhancement
   - Use cases and benefits
   - Implementation suggestions (if any)
   - Examples or mockups

### Code Contributions

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/amazing-feature`
3. **Make your changes**: Follow coding standards (see below)
4. **Write/update tests**: Ensure coverage is maintained
5. **Update documentation**: Update relevant docs
6. **Commit changes**: Use clear commit messages
7. **Push to branch**: `git push origin feature/amazing-feature`
8. **Create Pull Request**: Provide clear description

---

## Development Setup

### Prerequisites

- Python 3.11+
- Docker and Docker Compose
- Git
- PostgreSQL (for Guardian/Foresight)
- Neo4j (for Guardian/Cipher)
- Elasticsearch (for Cipher)

### Setup Steps

```bash
# Clone repository
git clone https://github.com/reichert-sentinel-ai/guardian-fraud-analytics.git
cd guardian-fraud-analytics

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Run tests
pytest tests/

# Run linter
flake8 src/
black --check src/
```

---

## Coding Standards

### Python Style Guide

- **PEP 8**: Follow PEP 8 style guide
- **Type Hints**: Use type hints for function signatures
- **Docstrings**: Use Google-style docstrings
- **Line Length**: Max 100 characters
- **Imports**: Organize imports (stdlib, third-party, local)

### Code Formatting

```bash
# Format with Black
black src/

# Sort imports
isort src/

# Check with Flake8
flake8 src/
```

### Example Code Style

```python
from typing import List, Optional

def predict_fraud(
    transaction: dict,
    model: Optional[object] = None
) -> dict:
    """
    Predict fraud probability for a transaction.
    
    Args:
        transaction: Transaction data dictionary
        model: Optional pre-trained model (defaults to default model)
        
    Returns:
        Dictionary with fraud probability and risk score
        
    Example:
        >>> predict_fraud({"amount": 1000, "merchant": "store"})
        {"fraud_probability": 0.05, "risk_score": "LOW"}
    """
    # Implementation here
    pass
```

---

## Testing Guidelines

### Test Requirements

- **Coverage**: Maintain 80%+ code coverage
- **Unit Tests**: Test individual functions and classes
- **Integration Tests**: Test API endpoints and workflows
- **Edge Cases**: Test boundary conditions and error cases

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html

# Run specific test file
pytest tests/test_models.py

# Run with verbose output
pytest -v
```

### Writing Tests

```python
import pytest
from src.models.predictor import FraudPredictor

def test_predictor_initialization():
    """Test predictor initialization."""
    predictor = FraudPredictor()
    assert predictor is not None
    
def test_predictor_with_invalid_input():
    """Test predictor handles invalid input."""
    predictor = FraudPredictor()
    with pytest.raises(ValueError):
        predictor.predict(None)
```

---

## Documentation Standards

### Code Documentation

- **Docstrings**: All public functions and classes need docstrings
- **Comments**: Explain complex logic, not obvious code
- **Type Hints**: Use type hints for clarity

### Documentation Updates

- Update README.md for new features
- Update API documentation for endpoint changes
- Update architecture docs for structural changes
- Add examples for new features

---

## Commit Message Guidelines

### Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Types

- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `test`: Test additions/changes
- `chore`: Maintenance tasks

### Examples

```
feat(models): add XGBoost ensemble model

Implement ensemble model combining XGBoost and LightGBM
for improved fraud detection accuracy.

Closes #123
```

```
fix(api): handle missing transaction data gracefully

Return 400 error with clear message when transaction
data is missing required fields.

Fixes #456
```

---

## Pull Request Process

### Before Submitting

1. **Update tests**: Ensure all tests pass
2. **Update documentation**: Update relevant docs
3. **Check coverage**: Maintain or improve coverage
4. **Run linters**: Fix any linting errors
5. **Rebase**: Rebase on latest main branch

### PR Description Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
- [ ] Tests added/updated
- [ ] All tests pass
- [ ] Manual testing completed

## Checklist
- [ ] Code follows style guidelines
- [ ] Documentation updated
- [ ] Tests added/updated
- [ ] No breaking changes (or documented)
```

### Review Process

1. **Automated Checks**: CI/CD runs tests and linting
2. **Code Review**: Maintainers review code
3. **Feedback**: Address review comments
4. **Approval**: After approval, PR is merged

---

## Project-Specific Guidelines

### Guardian (Fraud Detection)

- Focus on fraud detection accuracy
- Maintain <100ms latency requirements
- Ensure SHAP explainability preserved
- Test with synthetic fraud datasets

### Foresight (Crime Prediction)

- Maintain forecast accuracy (72.5%+)
- Ensure geospatial features work correctly
- Test with crime datasets
- Verify route optimization algorithms

### Cipher (Threat Intelligence)

- Maintain detection precision (95.3%+)
- Ensure MITRE ATT&CK mapping accuracy
- Test IOC collection from multiple sources
- Verify zero-day detection capabilities

---

## Questions?

- **GitHub Issues**: Open an issue for questions
- **Email**: reichert.sentinel.ai@gmail.com
- **Documentation**: Check docs/ directory

---

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

## Recognition

Contributors will be recognized in:
- README.md contributors section
- Release notes
- Project documentation

---

*Thank you for contributing to Sentinel Analytics!* 🇺🇸

