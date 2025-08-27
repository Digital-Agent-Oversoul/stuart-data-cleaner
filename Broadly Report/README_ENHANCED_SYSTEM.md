# Enhanced Stuart Data Cleaning System

## Overview

The Enhanced Stuart Data Cleaning System is a unified, intelligent data processing solution that combines the power of OpenAI's GPT-4o-mini with local Ollama fallback capabilities. This system provides robust, cost-effective data cleaning for both **Broadly Survey** and **Contact Export** processes while maintaining complete process independence.

## 🚀 Key Features

### **Unified Core Engine**
- **Single LLM engine** serving both Survey and Contact Export processes
- **OpenAI + Ollama fallback** system for maximum reliability
- **Budget monitoring** with automatic cost controls
- **Interactive learning framework** for continuous improvement

### **Process Independence**
- **Survey Process**: Location-segmented daily processing
- **Contact Export Process**: Aggregated monthly/quarterly processing
- **Complete isolation**: Failure in one process doesn't affect the other
- **Separate configurations** for each process

### **Intelligent Data Processing**
- **Advanced name parsing** using LLM reasoning
- **Business vs. person detection** with high accuracy
- **Cultural/ethnic name handling** better than rule-based systems
- **Email validation and cleaning** with pattern recognition

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Enhanced Scripts                        │
│  ┌─────────────────┐  ┌─────────────────┐                │
│  │ Broadly Survey  │  │ Contact Export  │                │
│  │   Enhanced      │  │   Enhanced      │                │
│  └─────────────────┘  └─────────────────┘                │
├─────────────────────────────────────────────────────────────┤
│                    Unified Core Engine                     │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────┐ │
│  │   OpenAI LLM    │  │  Ollama LLM     │  │ Rule-Based  │ │
│  │   (Primary)     │  │  (Fallback)     │  │ (Emergency) │ │
│  └─────────────────┘  └─────────────────┘  └─────────────┘ │
├─────────────────────────────────────────────────────────────┤
│                Interactive Learning System                 │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────┐ │
│  │   Uncertainty   │  │  Pattern        │  │ Knowledge   │ │
│  │   Detection     │  │  Learning       │  │ Storage     │ │
│  └─────────────────┘  └─────────────────┘  └─────────────┘ │
├─────────────────────────────────────────────────────────────┤
│                    Configuration & Logging                 │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────┐ │
│  │  JSON Config    │  │  Budget Monitor │  │  Logging    │ │
│  │  Management     │  │  & Cost Control │  │  System     │ │
│  └─────────────────┘  └─────────────────┘  └─────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

## 📁 File Structure

```
Broadly Report/
├── core_llm_engine.py              # Unified LLM engine
├── config.json                     # Configuration file
├── broadly_survey_enhanced.py      # Enhanced Survey script
├── contact_export_enhanced.py      # Enhanced Contact Export script
├── test_unified_engine.py          # Test script
├── requirements.txt                 # Python dependencies
├── README_ENHANCED_SYSTEM.md       # This file
├── project_docs/                   # Project documentation
│   ├── PRD.md                     # Product Requirements
│   ├── TECHNICAL_ARCHITECTURE.md  # Technical design
│   ├── DEVELOPMENT_ROADMAP.md     # Implementation plan
│   └── ...
└── [Original scripts remain unchanged]
```

## 🛠️ Installation & Setup

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. OpenAI API Setup (Optional but Recommended)
```bash
# Set environment variable
set OPENAI_API_KEY=sk-proj-your-key-here

# Or use command line argument
python script.py --openai-key=sk-proj-your-key-here
```

### 3. Ollama Setup (Required for Fallback)
```bash
# Install Ollama from https://ollama.ai/
# Pull the required model
ollama pull qwen2.5:7b-instruct-q4_K_M
```

### 4. Verify Installation
```bash
python test_unified_engine.py
```

## 🚀 Usage

### Broadly Survey Processing
```bash
# Basic usage
python broadly_survey_enhanced.py "path/to/raw_data.xlsx"

# With custom output directory
python broadly_survey_enhanced.py "path/to/raw_data.xlsx" --output-dir "custom/output"

# With OpenAI API key
python broadly_survey_enhanced.py "path/to/raw_data.xlsx" --openai-key "your-api-key"
```

### Contact Export Processing
```bash
# Basic usage
python contact_export_enhanced.py "path/to/raw_data.xlsx"

# With custom configuration
python contact_export_enhanced.py "path/to/raw_data.xlsx" --config "custom_config.json"
```

### Configuration
The system uses `config.json` for all settings:

```json
{
  "llm": {
    "openai": {
      "enabled": true,
      "model": "gpt-4o-mini",
      "monthly_budget": 10.0
    },
    "ollama": {
      "enabled": true,
      "model": "qwen2.5:7b-instruct-q4_K_M"
    }
  },
  "processing": {
    "batch_size": 500,
    "max_rows_for_llm": 1000
  }
}
```

## 🔧 Configuration Options

### LLM Settings
- **OpenAI Model**: Choose between gpt-4o-mini, gpt-4, etc.
- **Ollama Model**: Local model for fallback processing
- **Budget Limits**: Monthly spending caps with alerts
- **Confidence Thresholds**: When to use fallback systems

### Processing Settings
- **Batch Sizes**: Memory and API usage optimization
- **Row Limits**: When to switch to batch processing
- **Error Handling**: Graceful degradation strategies

### Output Settings
- **File Formats**: Excel with formatting and multiple sheets
- **Location Segmentation**: Dublin/Milpitas for Survey process
- **Contact Validation**: Business vs. person detection

## 📊 Monitoring & Logging

### Real-time Statistics
- **Processing Progress**: Row-by-row and batch progress
- **LLM Usage**: OpenAI vs. Ollama vs. rule-based counts
- **Budget Status**: Current costs and remaining budget
- **Performance Metrics**: Processing time and throughput

### Logging
- **File Logs**: Detailed processing logs with timestamps
- **Console Output**: Real-time progress and status updates
- **Error Tracking**: Comprehensive error logging and recovery

### Budget Monitoring
- **Cost Tracking**: Per-request and cumulative costs
- **Automatic Alerts**: Budget threshold warnings
- **Fallback Triggers**: Automatic Ollama switching

## 🧪 Testing

### Test Script
```bash
python test_unified_engine.py
```

### Test Cases Included
1. **Simple person names**: Basic name extraction
2. **Business vs. person**: Complex edge case detection
3. **Hyphenated names**: Cultural name handling
4. **Multiple people**: Complex contact scenarios
5. **Incomplete data**: Fallback processing

### Sample Data Testing
```bash
# Test with small dataset
python broadly_survey_enhanced.py "tests/small_sample.xlsx"

# Test with large dataset
python contact_export_enhanced.py "tests/large_sample.xlsx"
```

## 🔄 Migration from Legacy Scripts

### What's Changed
- **Unified LLM Logic**: Both scripts now use the same core engine
- **Enhanced Error Handling**: Better fallback and recovery
- **Budget Management**: Cost controls and monitoring
- **Configuration**: Centralized settings management

### What's Preserved
- **Output Formats**: Same Excel structure and formatting
- **Directory Structure**: Existing output locations maintained
- **Processing Logic**: Core business rules preserved
- **File Naming**: Existing naming conventions maintained

### Migration Steps
1. **Backup** existing scripts and data
2. **Install** new dependencies
3. **Configure** OpenAI API key (optional)
4. **Test** with small datasets
5. **Validate** output matches expectations
6. **Deploy** enhanced scripts

## 🚨 Troubleshooting

### Common Issues

#### OpenAI API Errors
```bash
# Check API key
echo $OPENAI_API_KEY

# Verify budget
python test_unified_engine.py
```

#### Ollama Connection Issues
```bash
# Check Ollama service
ollama list

# Test connection
curl http://localhost:11434/api/tags
```

#### Memory Issues
```bash
# Reduce batch size in config.json
"batch_size": 250

# Process smaller files
python script.py "small_dataset.xlsx"
```

### Error Recovery
- **Automatic Fallbacks**: System switches to Ollama if OpenAI fails
- **Rule-based Processing**: Final fallback for complete reliability
- **Progress Preservation**: Batch processing saves progress
- **Detailed Logging**: Comprehensive error information

## 🔮 Future Enhancements

### Phase 2: Interactive Learning
- **Human-in-the-Loop**: User guidance for uncertain cases
- **Pattern Learning**: Automatic prompt improvement
- **Confidence Scoring**: Dynamic threshold adjustment

### Phase 3: Web Interface
- **Archon-style UI**: Modern, intuitive interface
- **Drag & Drop**: Easy file upload and processing
- **Real-time Monitoring**: Live progress and statistics
- **Interactive Learning**: Built-in uncertainty resolution

### Phase 4: Automation
- **Email Integration**: Automatic file processing
- **Scheduled Runs**: Cron-based automation
- **API Endpoints**: RESTful service integration
- **Workflow Management**: Multi-step processing pipelines

## 📚 Documentation

### Project Documentation
- **PRD.md**: Product requirements and specifications
- **TECHNICAL_ARCHITECTURE.md**: System design details
- **DEVELOPMENT_ROADMAP.md**: Implementation timeline
- **TESTING_STRATEGY.md**: Quality assurance approach

### Code Documentation
- **Inline Comments**: Comprehensive function documentation
- **Type Hints**: Full Python type annotations
- **Error Handling**: Detailed exception documentation
- **Configuration**: Complete settings reference

## 🤝 Support & Contributing

### Getting Help
1. **Check Logs**: Detailed error information in log files
2. **Run Tests**: Verify system functionality with test script
3. **Review Config**: Check configuration settings
4. **Check Dependencies**: Verify Python package versions

### Contributing
1. **Follow Patterns**: Maintain existing code structure
2. **Add Tests**: Include test cases for new features
3. **Update Docs**: Keep documentation current
4. **Log Changes**: Document all modifications

## 📄 License

This system is part of the Stuart Data Cleaning project. All rights reserved.

---

## 🎯 Quick Start Checklist

- [ ] Install Python dependencies: `pip install -r requirements.txt`
- [ ] Set OpenAI API key: `set OPENAI_API_KEY=your-key`
- [ ] Verify Ollama: `ollama list`
- [ ] Test system: `python test_unified_engine.py`
- [ ] Process sample data: `python broadly_survey_enhanced.py "sample.xlsx"`
- [ ] Check output and logs
- [ ] Configure settings in `config.json`
- [ ] Deploy to production

**Ready to revolutionize your data cleaning process! 🚀**
