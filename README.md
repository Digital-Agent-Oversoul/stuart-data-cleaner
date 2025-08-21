# Stuart Data Cleaner

A unified data processing engine for the Stuart project, featuring LLM-powered name parsing and intelligent data cleaning.

## 🚀 **Recent Updates**

- **Git Integration**: ✅ Successfully integrated with GitHub repository
- **Unified Architecture**: ✅ Core logic shared between workflows
- **Professional Workflow**: ✅ Git branching strategy implemented

## 🏗️ **Architecture**

### **Core Modules** (`core/`)
- **`data_processor.py`**: Unified data cleaning logic used by both workflows
- **`llm_engine.py`**: LLM integration (OpenAI + Ollama fallback)
- **`name_parser.py`**: Intelligent name parsing and validation
- **`uncertainty_detector.py`**: Human-in-the-loop learning system

### **Workflow Processors** (`workflows/`)
- **`broadly_survey/`**: Daily location-segmented survey processing
- **`contact_export/`**: Monthly/quarterly aggregated contact export

### **Key Benefits**
- **No Code Duplication**: Both workflows use the same core logic
- **Maintainable**: Single source of truth for cleaning algorithms
- **Testable**: Core logic can be tested independently
- **Scalable**: Easy to add new workflows

## 🚀 **Getting Started**

### **Prerequisites**
- Python 3.8+
- OpenAI API key (or Ollama for local processing)
- Required packages: `pandas`, `openpyxl`, `openai`

### **Installation**
```bash
# Clone the repository
git clone https://github.com/Digital-Agent-Oversoul/stuart-data-cleaner.git
cd stuart-data-cleaner

# Install dependencies
pip install pandas openpyxl openai

# Set up configuration
cp test_config.json config.json
# Edit config.json with your API keys
```

### **Configuration**
Edit `config.json` with your settings:
```json
{
  "openai": {
    "api_key": "your-openai-api-key",
    "model": "gpt-4o-mini",
    "max_tokens": 150,
    "temperature": 0.1
  },
  "ollama": {
    "base_url": "http://localhost:11434",
    "model": "qwen2.5:7b-instruct-q4_K_M"
  }
}
```

## 🔄 **Usage**

### **Contact Export Workflow**
```bash
python main.py contact --input "path/to/input.xlsx" --output "path/to/output.xlsx"
```

### **Survey Workflow**
```bash
python main.py survey --input "path/to/input.xlsx" --output "path/to/output.xlsx" --location "Dublin"
```

## 🧪 **Testing**

Run the test suite:
```bash
python tests/run_tests.py
```

Or run individual tests:
```bash
python tests/test_full_dataset.py
```

## 📊 **Output Structure**

### **Contact Export**
- **Main Sheet**: "Contact Export" with cleaned, validated data
- **Removed Sheet**: Original source data for removed rows
- **Columns**: Email, Business type, First name, Last name, Customer name, Phone number, Sales person, Address, City, State, Zip

### **Survey Output**
- **Location-segmented**: Separate files per location
- **Daily processing**: Optimized for frequent, smaller datasets
- **Same core logic**: Uses identical cleaning algorithms

## 🔧 **Development**

### **Git Workflow**
- **`main`**: Production-ready code
- **`develop`**: Integration branch
- **`feature/*`**: Feature development branches
- **`hotfix/*`**: Critical production fixes

### **Adding New Workflows**
1. Create new processor in `workflows/`
2. Import and use `DataProcessor` from core
3. Implement workflow-specific logic
4. Add tests and documentation

## 📈 **Performance**

- **Small datasets** (<1000 rows): ~2-5 minutes
- **Large datasets** (>10,000 rows): ~15-30 minutes
- **LLM processing**: ~1-2 seconds per row
- **Fallback processing**: Rule-based when LLM fails

## 🚨 **Error Handling**

- **LLM failures**: Automatic fallback to rule-based processing
- **Data validation**: Comprehensive error checking and reporting
- **Transparency**: Complete audit trail of all changes and removals
- **Recovery**: Ability to reprocess failed records

## 📚 **Documentation**

- **`GIT_WORKFLOW.md`**: Complete Git workflow and branching strategy
- **`DEVELOPMENT_GUIDELINES.md`**: Development standards and practices
- **`project_docs/`**: Technical specifications and architecture

## 🤝 **Contributing**

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Make your changes and commit: `git commit -m 'feat: add amazing feature'`
4. Push to your fork: `git push origin feature/amazing-feature`
5. Create a Pull Request

## 📄 **License**

This project is proprietary to the Stuart project.

## 🆘 **Support**

For issues and questions:
1. Check existing documentation
2. Review test cases for examples
3. Create an issue on GitHub
4. Contact the development team

---

**Last Updated**: August 21, 2025  
**Version**: 1.0.0  
**Maintainer**: Development Team
