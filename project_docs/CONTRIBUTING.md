# Contributing to Stuart Data Cleaning System

## 🤝 **Welcome Contributors!**

Thank you for your interest in contributing to the Stuart Data Cleaning System! This document provides guidelines and information for developers, testers, and users who want to contribute to the project.

## 📋 **Table of Contents**

- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Code Standards](#code-standards)
- [Testing Requirements](#testing-requirements)
- [Documentation Standards](#documentation-standards)
- [Contribution Workflow](#contribution-workflow)
- [Issue Reporting](#issue-reporting)
- [Feature Requests](#feature-requests)
- [Code Review Process](#code-review-process)
- [Release Process](#release-process)

## 🚀 **Getting Started**

### **Who Can Contribute?**
- **Developers**: Python developers, frontend developers, DevOps engineers
- **Testers**: QA engineers, test automation specialists
- **Users**: Data operators, analysts, system administrators
- **Documentation**: Technical writers, user experience specialists

### **Areas for Contribution**
- **Core Engine**: LLM integration, data processing, error handling
- **Interactive Learning**: Uncertainty detection, pattern learning, user interface
- **User Interface**: Web interface, CLI tools, user experience
- **Testing**: Test automation, edge case coverage, performance testing
- **Documentation**: User guides, technical documentation, examples
- **DevOps**: Deployment, monitoring, CI/CD pipeline

## 🔧 **Development Setup**

### **Prerequisites**
- **Python**: 3.9 or higher
- **Git**: For version control
- **IDE**: VS Code, PyCharm, or your preferred editor
- **Ollama**: Local installation for fallback testing
- **OpenAI API**: Access for primary LLM testing

### **Environment Setup**
```bash
# Clone the project (when repository is available)
git clone <repository-url>
cd stuart-data-cleaning-system

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Install development dependencies
pip install -r requirements-dev.txt

# Set up pre-commit hooks
pre-commit install
```

### **Configuration Setup**
```bash
# Create environment file
cp .env.example .env

# Edit .env with your configuration
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-4o-mini
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=qwen2.5:7b-instruct-q4_K_M
```

## 📝 **Code Standards**

### **Python Code Style**
- **PEP 8**: Follow Python style guide
- **Line Length**: Maximum 88 characters (Black formatter)
- **Type Hints**: Use type hints for all function signatures
- **Docstrings**: Comprehensive docstrings for all public APIs

### **Code Formatting**
```bash
# Format code with Black
black core/ tests/ cli/

# Sort imports with isort
isort core/ tests/ cli/

# Check code style with flake8
flake8 core/ tests/ cli/
```

### **Code Quality Tools**
```bash
# Run all quality checks
pre-commit run --all-files

# Individual checks
black --check core/ tests/ cli/
isort --check-only core/ tests/ cli/
flake8 core/ tests/ cli/
mypy core/ cli/
```

### **Example Code Structure**
```python
from typing import Optional, Tuple, Dict, Any
import logging
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass
class NameParseResult:
    """Result of name parsing operation."""
    
    first_name: Optional[str]
    last_name: Optional[str]
    confidence: float
    processing_method: str
    metadata: Dict[str, Any]


class NameParser:
    """Parser for extracting names from contact information."""
    
    def __init__(self, config: Dict[str, Any]) -> None:
        """Initialize the name parser.
        
        Args:
            config: Configuration dictionary for the parser
        """
        self.config = config
        self.logger = logging.getLogger(self.__class__.__name__)
    
    def parse_name(
        self, 
        contact_name: str, 
        customer_name: str, 
        email: str
    ) -> NameParseResult:
        """Parse name from contact information.
        
        Args:
            contact_name: Contact name field
            customer_name: Customer name field
            email: Email address field
            
        Returns:
            NameParseResult with parsed name information
            
        Raises:
            ValueError: If input validation fails
            ProcessingError: If name parsing fails
        """
        # Input validation
        if not self._validate_input(contact_name, customer_name, email):
            raise ValueError("Invalid input parameters")
        
        try:
            # Parse name using LLM
            result = self._parse_with_llm(contact_name, customer_name, email)
            return result
        except Exception as e:
            self.logger.error(f"LLM parsing failed: {e}")
            # Fallback to rule-based parsing
            return self._parse_with_rules(contact_name, customer_name, email)
```

## 🧪 **Testing Requirements**

### **Test Coverage Requirements**
- **Minimum Coverage**: 90% code coverage
- **Test Types**: Unit, integration, and system tests
- **Edge Cases**: Comprehensive edge case coverage
- **Performance**: Performance testing for large datasets

### **Running Tests**
```bash
# Run all tests
python -m pytest

# Run with coverage
python -m pytest --cov=core --cov-report=html

# Run specific test categories
python -m pytest tests/unit/
python -m pytest tests/integration/
python -m pytest tests/system/

# Run performance tests
python -m pytest tests/performance/ -m "performance"

# Run edge case tests
python -m pytest tests/edge_cases/ -m "edge_cases"
```

### **Test Structure**
```
tests/
├── unit/                    # Unit tests
│   ├── test_llm_engine.py
│   ├── test_name_parser.py
│   └── test_data_processor.py
├── integration/             # Integration tests
│   ├── test_llm_pipeline.py
│   └── test_data_flow.py
├── system/                  # System tests
│   ├── test_survey_process.py
│   └── test_contact_export.py
├── performance/             # Performance tests
│   ├── test_large_datasets.py
│   └── test_memory_usage.py
├── edge_cases/              # Edge case tests
│   ├── test_complex_names.py
│   └── test_business_names.py
└── conftest.py             # Test configuration
```

### **Test Writing Guidelines**
```python
import pytest
from unittest.mock import Mock, patch
from core.llm_engine import LLMEngine


class TestLLMEngine:
    """Test suite for LLM engine."""
    
    @pytest.fixture
    def llm_engine(self):
        """Create LLM engine instance for testing."""
        config = {
            "openai": {"api_key": "test_key", "model": "gpt-4o-mini"},
            "ollama": {"base_url": "http://localhost:11434", "model": "test-model"}
        }
        return LLMEngine(config)
    
    def test_openai_integration_success(self, llm_engine):
        """Test successful OpenAI integration."""
        with patch('openai_client.chat.completions.create') as mock_openai:
            mock_openai.return_value.choices[0].message.content = '{"first_name": "John", "last_name": "Smith"}'
            
            result = llm_engine.parse_name("JOHN SMITH", "TEST CORP", "test@test.com")
            
            assert result.first_name == "John"
            assert result.last_name == "Smith"
            assert result.confidence > 0.8
    
    def test_ollama_fallback_on_openai_failure(self, llm_engine):
        """Test Ollama fallback when OpenAI fails."""
        with patch('openai_client.chat.completions.create', side_effect=Exception("API Error")):
            with patch('ollama_client.generate') as mock_ollama:
                mock_ollama.return_value = {"response": '{"first_name": "Jane", "last_name": "Doe"}'}
                
                result = llm_engine.parse_name("JANE DOE", "TEST CORP", "test@test.com")
                
                assert result.first_name == "Jane"
                assert result.last_name == "Doe"
                assert result.processing_method == "ollama"
    
    @pytest.mark.performance
    def test_large_dataset_performance(self, llm_engine):
        """Test performance with large datasets."""
        large_dataset = self._create_large_test_dataset(10000)
        
        start_time = time.time()
        results = llm_engine.process_batch(large_dataset)
        processing_time = time.time() - start_time
        
        assert processing_time < 300  # 5 minutes
        assert len(results) == 10000
        assert all(result.success for result in results)
```

## 📚 **Documentation Standards**

### **Documentation Requirements**
- **Code Documentation**: Docstrings for all public APIs
- **User Documentation**: Clear user guides and examples
- **Technical Documentation**: Architecture and design documents
- **API Documentation**: Comprehensive API reference

### **Documentation Structure**
```
docs/
├── user/                    # User documentation
│   ├── getting_started.md
│   ├── user_guide.md
│   └── troubleshooting.md
├── technical/               # Technical documentation
│   ├── architecture.md
│   ├── api_reference.md
│   └── deployment.md
├── development/             # Development documentation
│   ├── contributing.md
│   ├── testing.md
│   └── release_process.md
└── examples/                # Code examples
    ├── basic_usage.py
    ├── advanced_features.py
    └── integration_examples.py
```

### **Documentation Writing Guidelines**
- **Clear Structure**: Use consistent headings and organization
- **Code Examples**: Provide working code examples
- **Screenshots**: Include relevant screenshots and diagrams
- **Regular Updates**: Keep documentation current with code changes

## 🔄 **Contribution Workflow**

### **1. Issue Identification**
- **Bug Reports**: Clear description of the problem
- **Feature Requests**: Detailed requirements and use cases
- **Improvement Suggestions**: Specific areas for enhancement

### **2. Development Process**
```bash
# Create feature branch
git checkout -b feature/your-feature-name

# Make changes and commit
git add .
git commit -m "FEATURE: Add new name parsing algorithm

- Implemented advanced cultural name recognition
- Added support for hyphenated last names
- Improved confidence scoring for edge cases

Closes #123"

# Push branch and create pull request
git push origin feature/your-feature-name
```

### **3. Commit Message Format**
```
TYPE: Brief description of change

- Detailed bullet point of what was changed
- Another detailed bullet point
- Additional context if needed

Closes #issue-number
```

**Types:**
- **FEATURE**: New functionality
- **ENHANCEMENT**: Improvements to existing features
- **FIX**: Bug fixes
- **REFACTOR**: Code restructuring
- **DOCS**: Documentation updates
- **TEST**: Testing additions
- **CONFIG**: Configuration changes

### **4. Pull Request Process**
- **Description**: Clear description of changes
- **Testing**: Evidence that tests pass
- **Documentation**: Updated documentation if needed
- **Review**: Address review comments promptly

## 🐛 **Issue Reporting**

### **Bug Report Template**
```markdown
## Bug Description
Brief description of the bug

## Steps to Reproduce
1. Step one
2. Step two
3. Step three

## Expected Behavior
What should happen

## Actual Behavior
What actually happens

## Environment
- OS: [e.g., Windows 10, macOS 12]
- Python Version: [e.g., 3.9.7]
- Project Version: [e.g., 1.0.0]

## Additional Information
Screenshots, logs, or other relevant information
```

### **Feature Request Template**
```markdown
## Feature Description
Brief description of the requested feature

## Use Case
Why this feature is needed

## Proposed Solution
How you think this should work

## Alternatives Considered
Other approaches you've considered

## Additional Context
Any other relevant information
```

## 👀 **Code Review Process**

### **Review Guidelines**
- **Code Quality**: Ensure code meets quality standards
- **Functionality**: Verify the feature works as intended
- **Testing**: Confirm adequate test coverage
- **Documentation**: Check documentation updates
- **Performance**: Consider performance implications

### **Review Checklist**
- [ ] Code follows style guidelines
- [ ] Tests are included and pass
- [ ] Documentation is updated
- [ ] No security vulnerabilities
- [ ] Performance impact is acceptable
- [ ] Error handling is appropriate

## 🚀 **Release Process**

### **Release Preparation**
1. **Feature Complete**: All planned features implemented
2. **Testing Complete**: All tests pass, including performance tests
3. **Documentation Updated**: All documentation current
4. **Security Review**: Security assessment completed

### **Release Steps**
```bash
# Update version numbers
# Update CHANGELOG.md
# Create release branch
git checkout -b release/v1.1.0

# Final testing and validation
python -m pytest --cov=core --cov-fail-under=90
python -m pytest tests/performance/
python -m pytest tests/edge_cases/

# Create release tag
git tag -a v1.1.0 -m "Release version 1.1.0"
git push origin v1.1.0

# Merge to main branch
git checkout main
git merge release/v1.1.0
git push origin main

# Delete release branch
git branch -d release/v1.1.0
```

## 🏆 **Recognition and Rewards**

### **Contributor Recognition**
- **Contributor List**: Recognition in project documentation
- **Code Attribution**: Credit in code comments and documentation
- **Community Recognition**: Acknowledgment in release notes
- **Professional Development**: Experience with modern development practices

### **Contribution Levels**
- **Bronze**: 1-5 contributions
- **Silver**: 6-20 contributions
- **Gold**: 21+ contributions
- **Platinum**: Major architectural contributions

## 📞 **Getting Help**

### **Communication Channels**
- **Project Issues**: GitHub issues for bugs and features
- **Discussion Forum**: Community discussions and questions
- **Documentation**: Comprehensive project documentation
- **Team Meetings**: Regular development team meetings

### **Mentorship**
- **New Contributors**: Mentorship for first-time contributors
- **Code Reviews**: Detailed feedback and guidance
- **Pair Programming**: Collaborative development sessions
- **Training Sessions**: Regular training and skill development

## 📋 **Contribution Checklist**

Before submitting your contribution, ensure:

- [ ] Code follows style guidelines
- [ ] Tests are written and pass
- [ ] Documentation is updated
- [ ] No security vulnerabilities introduced
- [ ] Performance impact is acceptable
- [ ] Error handling is appropriate
- [ ] Commit messages follow format
- [ ] Pull request description is clear
- [ ] All review comments addressed

---

**Thank you for contributing to the Stuart Data Cleaning System!**

Your contributions help make this project better for everyone. Whether you're fixing bugs, adding features, improving documentation, or providing feedback, your work is valued and appreciated.

---

**Document Version**: 1.0  
**Last Updated**: 2025-01-08  
**Document Owner**: Stuart Project Team
