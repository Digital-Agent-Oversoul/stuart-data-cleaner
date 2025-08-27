# Ollama Integration for Broadly Data Cleaner

## Overview

The `broadly_data_cleaner_llm.py` script has been successfully updated to use Ollama as the LLM provider instead of OpenAI. This provides a local, private, and cost-effective solution for intelligent data cleaning.

## Changes Made

### 1. LLM Provider Switch
- **Before**: OpenAI GPT-4o-mini (requires API key and internet)
- **After**: Ollama with `phi3:mini` model (local, private, no API costs)

### 2. Configuration Updates
```python
# LLM Configuration
LLM_ENABLED = True
LLM_MODEL = "phi3:mini"  # Fast, efficient model for data cleaning
OLLAMA_BASE_URL = "http://localhost:11434"
MAX_TOKENS = 150
TEMPERATURE = 0.1
```

### 3. API Integration
- Replaced OpenAI API calls with Ollama REST API
- Added connection testing and error handling
- Implemented fallback to rule-based processing if LLM fails

## Model Selection

**Selected Model**: `phi3:mini`
- **Size**: 2.2 GB (fast loading)
- **Performance**: Excellent for structured data tasks
- **Speed**: Quick response times for data cleaning
- **Capability**: Good at JSON generation and reasoning

**Alternative Models Available**:
- `qwen2.5:7b-instruct-q4_K_M` (4.7 GB) - More capable but slower
- `mistral:7b-instruct-q4_K_M` (4.4 GB) - Good balance
- `gemma:2b` (1.7 GB) - Very fast but less capable

## Prerequisites

1. **Ollama Running**: Ensure Ollama is running in Docker
   ```bash
   # Check if Ollama container is running
   docker ps | grep ollama
   ```

2. **Model Available**: The `phi3:mini` model should be available
   ```bash
   # Check available models
   docker exec ollama ollama list
   ```

3. **Network Access**: Script connects to `http://localhost:11434`

## Usage

### Basic Usage
```bash
python broadly_data_cleaner_llm.py input_file.xlsx
```

### Testing Connection
```bash
python test_ollama_connection.py
```

### Testing Name Parsing
```bash
python test_name_parsing.py
```

## Features

### 1. Intelligent Name Parsing
- Uses LLM to distinguish between person names and company names
- Extracts first/last names from various formats
- Handles complex cases like "John Smith - ABC Company"

### 2. Fallback Mechanism
- If LLM fails, automatically falls back to rule-based processing
- No data loss if Ollama is unavailable
- Graceful error handling

### 3. Performance Optimizations
- Fast model (`phi3:mini`) for quick processing
- Efficient prompt design for structured output
- Timeout handling to prevent hanging

## Error Handling

The script includes comprehensive error handling:

1. **Connection Issues**: Tests Ollama connection before processing
2. **Model Loading**: Handles model loading delays
3. **API Errors**: Graceful fallback to rule-based processing
4. **JSON Parsing**: Validates LLM responses

## Performance Comparison

| Aspect | OpenAI GPT-4o-mini | Ollama phi3:mini |
|--------|-------------------|------------------|
| **Speed** | ~2-5 seconds | ~1-3 seconds |
| **Cost** | ~$0.01-0.05 per call | Free |
| **Privacy** | Data sent to OpenAI | Completely local |
| **Reliability** | Requires internet | Works offline |
| **Setup** | API key required | Docker container |

## Troubleshooting

### Common Issues

1. **Connection Refused**
   ```
   ⚠️ Cannot connect to Ollama at http://localhost:11434
   ```
   **Solution**: Ensure Ollama Docker container is running

2. **Model Not Found**
   ```
   ❌ Target model 'phi3:mini' not found
   ```
   **Solution**: Pull the model: `docker exec ollama ollama pull phi3:mini`

3. **Timeout Errors**
   ```
   ⚠️ LLM call failed: Read timed out
   ```
   **Solution**: Model is loading, wait a moment and retry

### Debugging

1. **Test Connection**: Run `python test_ollama_connection.py`
2. **Check Models**: `docker exec ollama ollama list`
3. **View Logs**: `docker logs ollama`

## Benefits

1. **Cost Savings**: No API costs for LLM calls
2. **Privacy**: All data processing happens locally
3. **Reliability**: No dependency on internet connectivity
4. **Speed**: Faster processing with local model
5. **Control**: Full control over model selection and configuration

## Future Enhancements

1. **Model Selection**: Add command-line option to choose different models
2. **Batch Processing**: Optimize for large datasets
3. **Caching**: Cache LLM responses for repeated patterns
4. **Parallel Processing**: Process multiple records simultaneously

## Files Modified

- `broadly_data_cleaner_llm.py` - Main script with Ollama integration
- `test_ollama_connection.py` - Connection testing utility
- `test_name_parsing.py` - Name parsing functionality test
- `README_Ollama_Integration.md` - This documentation 