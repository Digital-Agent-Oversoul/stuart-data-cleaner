# Configuration Troubleshooting Guide

## 🚨 **Common Configuration Issues & Solutions**

## **1. OpenAI API Key Issues**

### **Problem: "OpenAI API key not configured"**
**Symptoms:**
- OpenAI processing fails immediately
- Error: "OpenAI API key not configured"
- LLM engine falls back to Ollama only

**Causes:**
1. API key exposed in public repository (automatically disabled by OpenAI)
2. Environment variable not set
3. Configuration file structure mismatch
4. API key expired or invalid

**Solutions:**
```bash
# ✅ Set environment variable (Windows PowerShell)
$env:OPENAI_API_KEY="sk-proj-your-actual-key-here"

# ✅ Set environment variable (Linux/Mac)
export OPENAI_API_KEY="sk-proj-your-actual-key-here"

# ✅ Verify environment variable is set
echo $env:OPENAI_API_KEY  # Windows
echo $OPENAI_API_KEY       # Linux/Mac
```

**Prevention:**
- Never commit API keys to version control
- Use `.env` files (not committed) or system environment variables
- Regular key rotation and monitoring

### **Problem: "OpenAI API key is None"**
**Symptoms:**
- Configuration loads but API key is None
- OpenAI processor initialization fails

**Causes:**
1. Configuration file has `"openai_api_key": null`
2. Environment variable not loaded by Config class
3. Configuration structure mismatch

**Solutions:**
```python
# ✅ Check configuration structure
from config.config import Config
config = Config('config.json')
print(f"API Key: {config.llm.openai_api_key}")

# ✅ Verify environment variable loading
import os
print(f"ENV API Key: {os.getenv('OPENAI_API_KEY')}")
```

## **2. Configuration Structure Issues**

### **Problem: "AttributeError: 'Config' object has no attribute 'openai'"**
**Symptoms:**
- Configuration object structure mismatch
- Processors fail to initialize

**Causes:**
1. Different configuration file formats
2. Configuration class structure changes
3. Incorrect attribute access

**Solutions:**
```python
# ✅ Correct configuration access
config = Config('config.json')

# For main config.json structure:
api_key = config.llm.openai_api_key
model = config.llm.openai_model

# For test_config.json structure:
api_key = config.llm.openai.api_key
model = config.llm.openai.model
```

### **Problem: "config.__dict__ flattening issues"**
**Symptoms:**
- Nested configuration structures flattened incorrectly
- Processors receive wrong configuration format

**Causes:**
1. Using `config.__dict__` instead of config object
2. Nested structures become flattened keys

**Solutions:**
```python
# ✅ Correct - pass config object directly
data_processor = DataProcessor(config)
export_processor = ExportProcessor(config)

# ❌ Incorrect - flattens nested structures
data_processor = DataProcessor(config.__dict__)
export_processor = ExportProcessor(config.__dict__)
```

## **3. Ollama Configuration Issues**

### **Problem: "Ollama connection failed"**
**Symptoms:**
- Ollama processor fails to connect
- Error: "Connection refused" or timeout

**Causes:**
1. Ollama service not running
2. Wrong base URL
3. Firewall blocking connection
4. Ollama not installed

**Solutions:**
```bash
# ✅ Check if Ollama is running
ollama list

# ✅ Start Ollama service
ollama serve

# ✅ Verify connection
curl http://localhost:11434/api/tags

# ✅ Check configuration
# config.json should have:
"ollama": {
  "base_url": "http://localhost:11434",
  "model": "qwen2.5:7b-instruct-q4_K_M"
}
```

### **Problem: "Ollama model not found"**
**Symptoms:**
- Ollama connects but model fails to load
- Error: "model not found"

**Causes:**
1. Model not installed
2. Wrong model name
3. Model corrupted

**Solutions:**
```bash
# ✅ List available models
ollama list

# ✅ Install specific model
ollama pull qwen2.5:7b-instruct-q4_K_M

# ✅ Verify model
ollama run qwen2.5:7b-instruct-q4_K_M "Hello"
```

## **4. Data Processing Configuration Issues**

### **Problem: "Column names not found"**
**Symptoms:**
- KeyError when accessing columns
- Columns transformed during data loading

**Causes:**
1. Header detection issues
2. Column name transformation by pandas
3. Configuration mismatch between test and production

**Solutions:**
```python
# ✅ Check actual column names
df = pd.read_excel('data.xlsx')
print("Columns:", df.columns.tolist())

# ✅ Use transformed names consistently
# 'Contact Name' becomes 'contact_name'
contact_name = row.get('contact_name', '')
customer_name = row.get('customer_name', '')
email = row.get('email', '')

# ✅ Handle both original and transformed names
email_column = 'email' if 'email' in df.columns else 'Email'
```

### **Problem: "Header detection failed"**
**Symptoms:**
- Wrong row identified as header
- Data starts from wrong row

**Causes:**
1. Inconsistent data formats
2. Header detection logic too rigid
3. Mixed data types in header row

**Solutions:**
```python
# ✅ Enable debug logging
# In header_detector.py, add debug prints

# ✅ Check header detection results
print(f"Detected header on row: {header_row}")

# ✅ Verify expected columns found
expected_columns = ['Contact Name', 'Customer Name', 'Email']
found_columns = df.iloc[header_row].tolist()
print(f"Expected: {expected_columns}")
print(f"Found: {found_columns}")
```

## **5. Environment-Specific Issues**

### **Problem: "Different behavior in test vs production"**
**Symptoms:**
- Tests pass but production fails
- Different configuration loading behavior

**Causes:**
1. Different configuration files
2. Environment variable differences
3. Path resolution issues

**Solutions:**
```python
# ✅ Use consistent configuration loading
# In test scripts:
config = Config('test_config.json')

# In production:
config = Config('config/config.json')

# ✅ Verify configuration consistency
print(f"Test config: {config.llm.openai_api_key}")
print(f"Prod config: {Config('config/config.json').llm.openai_api_key}")
```

### **Problem: "Path resolution issues"**
**Symptoms:**
- File not found errors
- Wrong working directory

**Causes:**
1. Relative vs absolute paths
2. Working directory changes
3. Path separator differences (Windows vs Unix)

**Solutions:**
```python
# ✅ Use pathlib for cross-platform compatibility
from pathlib import Path

# ✅ Resolve paths relative to script location
script_dir = Path(__file__).parent
config_path = script_dir / "config" / "config.json"

# ✅ Handle Windows/Unix path differences
data_path = Path("tests/test_datasets/data.xlsx").resolve()
```

## **6. Debugging Configuration Issues**

### **Configuration Validation Commands**
```python
# ✅ Validate configuration loading
from config.config import Config
config = Config('config.json')
print(f"Config loaded: {config is not None}")

# ✅ Check configuration structure
print(f"Config attributes: {dir(config)}")
print(f"LLM config: {hasattr(config, 'llm')}")

# ✅ Verify API keys
print(f"OpenAI key: {config.llm.openai_api_key[:20] if config.llm.openai_api_key else 'None'}...")
print(f"Ollama URL: {config.llm.ollama.base_url}")

# ✅ Test processor initialization
from core.llm_engine import LLMEngine
try:
    engine = LLMEngine(config)
    print("✅ LLM Engine initialized successfully")
except Exception as e:
    print(f"❌ LLM Engine failed: {e}")
```

### **Environment Variable Debugging**
```bash
# ✅ Check all environment variables
Get-ChildItem Env: | Where-Object {$_.Name -like "*OPENAI*"}

# ✅ Check specific variables
echo $env:OPENAI_API_KEY
echo $env:OLLAMA_BASE_URL

# ✅ Set and verify variables
$env:OPENAI_API_KEY="test_key"
echo $env:OPENAI_API_KEY
```

## **7. Prevention Checklist**

### **Before Committing Code:**
- [ ] No API keys in configuration files
- [ ] No hardcoded paths or credentials
- [ ] Configuration files use placeholders or null values
- [ ] Environment variables documented in README

### **Before Running Tests:**
- [ ] Environment variables set correctly
- [ ] Configuration files exist and are valid JSON
- [ ] Ollama service running (if testing Ollama)
- [ ] Test datasets available in correct location

### **Before Production Deployment:**
- [ ] Environment variables configured on production system
- [ ] Configuration files validated
- [ ] All dependencies installed
- [ ] Paths resolved correctly for production environment

## **8. Quick Fix Reference**

| Issue | Quick Fix | Command |
|-------|-----------|---------|
| OpenAI API key missing | Set environment variable | `$env:OPENAI_API_KEY="key"` |
| Ollama not connecting | Start Ollama service | `ollama serve` |
| Column names wrong | Check transformed names | `print(df.columns.tolist())` |
| Config structure error | Pass config object directly | `DataProcessor(config)` |
| Path issues | Use pathlib | `Path(__file__).parent` |
| Model not found | Install model | `ollama pull model_name` |
