# Stuart Data Cleaning System

## 🚀 **Project Overview**

The **Stuart Data Cleaning System** is a unified data processing engine that combines advanced LLM technology with interactive learning to provide intelligent, accurate data cleaning for customer contact information. The system supports two primary processes: **Broadly Survey** (daily, location-segmented outputs) and **Contact Export** (monthly/quarterly, aggregated outputs).

## ✨ **Key Features**

### **🤖 Multi-Tier LLM Processing**
- **Primary**: OpenAI API (gpt-4o-mini) for high-quality name parsing
- **Fallback**: Ollama local (qwen2.5:7b) for reliability
- **Emergency**: Rule-based processing for complete coverage
- **Budget Monitoring**: Cost tracking and automatic fallback triggers

### **🧠 Interactive Learning Framework**
- **Uncertainty Detection**: Identifies edge cases requiring human guidance
- **Human-in-the-Loop**: Prompts users for decisions on complex scenarios
- **Pattern Learning**: Builds knowledge base from user decisions
- **Continuous Improvement**: System gets smarter with each interaction

### **🏗️ Modular Architecture**
- **Process Independence**: Survey and Contact Export operate completely separately
- **Shared Core Engine**: Consistent data cleaning logic across both processes
- **Error Isolation**: Failure in one process doesn't affect the other
- **Scalable Design**: Ready for future automation and workflow integration

### **🎨 Modern Interface**
- **Archon-Style UX**: Modern, intuitive interface design
- **Real-time Progress**: Live processing visualization and monitoring
- **File Management**: Drag & drop, browsing, and content viewing
- **Process Selection**: Clear choice between Survey and Contact Export

## 📋 **Process Overview**

### **📊 Broadly Survey Process**
- **Purpose**: Generate location-segmented data for customer surveys
- **Frequency**: Daily execution on smaller datasets
- **Output**: Separate files for Dublin and Milpitas locations
- **Use Case**: Customer survey distribution and outreach

### **📧 Contact Export Process**
- **Purpose**: Generate comprehensive contact lists for analysis
- **Frequency**: Monthly/quarterly execution on larger datasets
- **Output**: Single aggregated file with removed items tracking
- **Use Case**: Detailed customer contact analysis and management

## 🏗️ **System Architecture**

```
┌─────────────────────────────────────────────────────────────┐
│                    Data Processing Engine                   │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────┐ │
│  │   OpenAI LLM    │  │  Ollama LLM     │  │ Rule-Based  │ │
│  │   (Primary)     │  │  (Fallback)     │  │ (Emergency) │ │
│  └─────────────────┘  └─────────────────┘  └─────────────┘ │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────┐ │
│  │  Survey Output  │  │ Contact Export  │  │   Quality   │ │
│  │   Processor     │  │   Processor     │  │  Monitor    │ │
│  └─────────────────┘  └─────────────────┘  └─────────────┘ │
├─────────────────────────────────────────────────────────────┤
│                    Output Management                       │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────┐ │
│  │  Location-Based │  │  Aggregated     │  │  Validation │ │
│  │     Files       │  │     Files       │  │   Reports   │ │
│  └─────────────────┘  └─────────────────┘  └─────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

## 🚀 **Quick Start**

### **Prerequisites**
- Python 3.9+ installed
- OpenAI API key (for primary LLM processing)
- Ollama local installation (for fallback processing)
- Access to raw data files (Excel format)

### **Installation**
```bash
# Clone or download the project
cd "C:\LocalAI\!projects\Stuart"

# Install Python dependencies
pip install -r requirements.txt

# Set up environment variables
export OPENAI_API_KEY="your_openai_api_key_here"
export OPENAI_MODEL="gpt-4o-mini"
export OLLAMA_BASE_URL="http://localhost:11434"
export OLLAMA_MODEL="qwen2.5:7b-instruct-q4_K_M"
```

### **Basic Usage**
```bash
# Process data for Survey (location-segmented)
python main.py survey "path/to/raw_data.xlsx"

# Process data for Contact Export (aggregated)
python main.py contact "path/to/raw_data.xlsx"

# Interactive mode with learning prompts
python main.py interactive "path/to/raw_data.xlsx"
```

## 📁 **Project Organization**

### **Production Root (Keep Clean)**
```
data_cleaner/
├── core/                           # Core processing engine
├── workflows/                      # Workflow processors  
├── config/                         # Configuration management
├── cli/                           # Command-line interface
├── processors/                     # Data processors
├── main.py                        # 🎯 MAIN ENTRY POINT
├── workflows/contact_export/export_processor.py  # 🎯 PRODUCTION Contact Export processor
├── test_config.json               # 🎯 PRODUCTION Configuration
├── README.md                      # 🎯 PROJECT DOCUMENTATION
├── DEVELOPMENT_GUIDELINES.md      # Development standards
└── .project_root                  # Project root marker
```

### **Test Folder (🧪 Testing & Validation)**
```
test/
├── test_output/                   # Test output files
├── test_*.py                      # Test scripts
├── check_*.py                     # Output validation scripts
├── analyze_*.py                   # Data analysis scripts
└── run_tests.py                   # 🎯 TEST RUNNER
```

### **Development Folder (🛠️ Development & Documentation)**
```
dev/
├── archon_project.json            # Task tracking
├── SESSION_SUMMARY_20250821.md   # Session documentation
├── archon_tasks.py                # Local task management
├── dev_setup.ps1                  # Development environment setup
└── setup_archon_project.py        # Project setup utilities
```

### **Documentation Folder (📚 Project Documentation)**
```
project_docs/
├── README.md                      # This file - comprehensive project overview
├── DEVELOPMENT_GUIDELINES.md      # Development standards and file location rules
├── GIT_WORKFLOW.md               # Git workflow and branching strategy
├── TASK_STATUS.md                # Current task status and progress
├── CHANGELOG.md                  # Version history and changes
├── TECHNICAL_ARCHITECTURE.md     # System design and architecture
├── DEVELOPMENT_ROADMAP.md        # Implementation plan and milestones
├── TESTING_STRATEGY.md           # Testing approach and quality gates
├── CONTRIBUTING.md               # Contribution guidelines
└── PRD.md                        # Product requirements document
```

## 🎯 **Benefits of Organization**

### **Production Readiness**
- **Clean Root**: Only production files in main directory
- **Easy Deployment**: Clear separation of concerns
- **Professional Structure**: Industry-standard organization

### **Development Efficiency**
- **Test Runner**: Easy access to all tests via `test/run_tests.py`
- **Organized Scripts**: Logical grouping by purpose
- **Clear Documentation**: Development files separated from production

### **Maintenance**
- **Easy Testing**: All test scripts in one location
- **Clear Dependencies**: Production vs. development separation
- **Scalable Structure**: Easy to add new tests and utilities

### **Documentation Benefits**
- **Single Source of Truth**: Each type of information has one authoritative location
- **Easy Navigation**: Clear hierarchy and cross-references between documents
- **Professional Structure**: Industry-standard documentation organization
- **Better Collaboration**: Team members can easily find and update documentation

## 🚀 **How to Use**

### **Running Tests**
```bash
# From project root
python test/run_tests.py

# Or run individual tests
python test/test_full_dataset.py
python test/check_sheet_name_change.py
```

### **Development Work**
```bash
# Access development utilities
python dev/archon_tasks.py
python dev/setup_archon_project.py
```

### **Production Use**
```bash
# Main entry point
python main.py contact <input_file.xlsx>

# Direct processor access
python workflows/contact_export/export_processor.py
```

## 📚 **Documentation**

### **Project Documentation**
- **[PRD.md](PRD.md)**: Product Requirements Document
- **[TECHNICAL_ARCHITECTURE.md](TECHNICAL_ARCHITECTURE.md)**: System design and architecture
- **[DEVELOPMENT_ROADMAP.md](DEVELOPMENT_ROADMAP.md)**: Implementation plan and phases
- **[TESTING_STRATEGY.md](TESTING_STRATEGY.md)**: Testing approach and validation
- **[CHANGELOG.md](CHANGELOG.md)**: Project progress and change tracking

### **User Guides**
- **Getting Started**: Basic setup and first run
- **Process Selection**: Choosing between Survey and Contact Export
- **Interactive Learning**: Using the human-in-the-loop system
- **Configuration**: Setting up API keys and system preferences
- **Troubleshooting**: Common issues and solutions

## 🔧 **Configuration**

### **Environment Variables**
```bash
# OpenAI Configuration
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-4o-mini
OPENAI_MAX_TOKENS=150
OPENAI_TEMPERATURE=0.1

# Ollama Configuration
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=qwen2.5:7b-instruct-q4_K_M
OLLAMA_FALLBACK_ENABLED=true

# Budget Configuration
OPENAI_MONTHLY_BUDGET=10.00
OPENAI_ALERT_THRESHOLD=0.8
```

### **JSON Configuration**
```json
{
  "llm": {
    "openai": {
      "model": "gpt-4o-mini",
      "max_tokens": 150,
      "temperature": 0.1
    },
    "ollama": {
      "base_url": "http://localhost:11434",
      "model": "qwen2.5:7b-instruct-q4_K_M"
    }
  },
  "processing": {
    "batch_size": 500,
    "max_rows_for_llm": 1000,
    "confidence_thresholds": {
      "high": 0.7,
      "medium": 0.5,
      "low": 0.3
    }
  }
}
```

## 🧪 **Testing**

### **Test Datasets**
The system includes comprehensive test datasets for validation:
- **Simple Names**: Basic name parsing scenarios
- **Complex Names**: Hyphenated names, multiple people, cultural names
- **Edge Cases**: Business names, incomplete data, malformed information
- **Large Datasets**: Performance testing with realistic data volumes

### **Running Tests**
```bash
# Run all tests
python -m pytest tests/

# Run specific test categories
python -m pytest tests/test_llm_engine.py
python -m pytest tests/test_data_processing.py
python -m pytest tests/test_interactive_learning.py

# Run with coverage
python -m pytest --cov=core tests/
```

## 📊 **Performance**

### **Processing Targets**
- **Small Datasets** (<1K rows): <5 minutes processing time
- **Medium Datasets** (1K-10K rows): <15 minutes processing time
- **Large Datasets** (>10K rows): <30 minutes processing time
- **LLM Response Time**: <10 seconds per name parsing request

### **Quality Metrics**
- **Name Extraction Accuracy**: >95% for person names vs business names
- **Edge Case Coverage**: Handle 90%+ of complex name scenarios
- **Processing Reliability**: <1% failure rate for both processes
- **Learning Efficiency**: System improves with each user interaction

## 🔒 **Security & Privacy**

### **Data Security**
- **Local Processing**: Data processed locally, not sent to external services
- **API Key Management**: Secure storage and rotation of OpenAI keys
- **Audit Logging**: Complete tracking of all processing decisions
- **Data Validation**: Input validation and sanitization

### **Privacy Considerations**
- **Customer Data**: Sensitive information handled securely
- **Learning Data**: User decisions stored locally
- **No External Sharing**: Data not shared with third parties
- **Compliance**: Maintain data integrity and audit trails

## 🚀 **Development Roadmap**

### **Phase 1: Core LLM Engine (Weeks 1-2)**
- [x] Project documentation and planning
- [ ] Unified core engine development
- [ ] OpenAI + Ollama integration
- [ ] Basic CLI interface
- [ ] Core logic validation

### **Phase 2: Interactive Learning (Weeks 3-4)**
- [ ] Uncertainty detection system
- [ ] Human-in-the-loop interface
- [ ] Pattern learning framework
- [ ] Learning validation

### **Phase 3: Modern Interface (Weeks 5-6)**
- [ ] React-based web interface
- [ ] Archon-style UX design
- [ ] Real-time progress visualization
- [ ] File management system

### **Phase 4: Automation Ready (Weeks 7-8)**
- [ ] API endpoints for headless operation
- [ ] Scheduling and batch processing
- [ ] Monitoring and alerting
- [ ] Production deployment

## 🤝 **Contributing**

### **Development Setup**
1. **Fork the repository** or set up local development environment
2. **Install dependencies** and configure environment
3. **Create feature branch** for your changes
4. **Write tests** for new functionality
5. **Submit pull request** or document changes

### **Code Standards**
- **Python**: Follow PEP 8 style guidelines
- **Testing**: Maintain >90% test coverage
- **Documentation**: Update relevant documentation
- **Quality**: Pass all automated quality checks

## 📞 **Support & Contact**

### **Getting Help**
- **Documentation**: Check the project documentation first
- **Issues**: Report bugs and feature requests through project tracking
- **Questions**: Use project discussion channels
- **Training**: Request training sessions for your team

### **Project Team**
- **Project Owner**: Stuart Project Team
- **Development Lead**: AI Development Team
- **Quality Assurance**: QA Team
- **User Experience**: UX Team

## 📄 **License**

This project is proprietary software developed for internal use. All rights reserved.

---

**Project Version**: 1.0.0  
**Last Updated**: 2025-01-08  
**Document Owner**: Stuart Project Team
