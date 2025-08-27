# LLM-Enhanced Broadly Data Cleaner Setup Guide

## Overview

The LLM-enhanced version uses OpenAI's GPT models to intelligently parse names from complex data, providing much better accuracy than rule-based approaches.

## Quick Start

### 1. Install Dependencies

```bash
pip install pandas openpyxl openai
```

### 2. Set Up OpenAI API Key

**Option A: Environment Variable (Recommended)**
```bash
# Windows PowerShell
$env:OPENAI_API_KEY="your-api-key-here"

# Windows Command Prompt
set OPENAI_API_KEY=your-api-key-here

# Linux/Mac
export OPENAI_API_KEY="your-api-key-here"
```

**Option B: Direct in Script**
Edit `broadly_data_cleaner_llm.py` and add:
```python
import openai
openai.api_key = "your-api-key-here"
```

### 3. Run the Enhanced Cleaner

```bash
python broadly_data_cleaner_llm.py "Broadly RAW/12.04.24 - 01.07.25 (1).xlsx"
```

## Configuration Options

### LLM Settings (in `broadly_data_cleaner_llm.py`)

```python
# Enable/disable LLM processing
LLM_ENABLED = True  # Set to False for rule-based only

# Choose model (faster/cheaper vs more accurate)
LLM_MODEL = "gpt-4o-mini"  # Fast and cheap
# LLM_MODEL = "gpt-4o"      # More accurate but slower

# Response settings
MAX_TOKENS = 150
TEMPERATURE = 0.1  # Lower = more consistent
```

## Cost Estimates

| Model | Cost per 1000 rows | Speed | Accuracy |
|-------|-------------------|-------|----------|
| gpt-4o-mini | ~$0.15 | Fast | High |
| gpt-4o | ~$0.60 | Medium | Very High |
| gpt-3.5-turbo | ~$0.10 | Very Fast | Good |

For your 679 rows: ~$0.10-0.40 total cost.

## How It Works

### 1. Hybrid Approach
- **Simple cases**: Rule-based processing (fast, free)
- **Complex cases**: LLM processing (accurate, paid)

### 2. LLM Intelligence
The LLM analyzes:
- Contact Name field
- Customer Name field  
- Email address
- Context clues

And returns:
```json
{"first_name": "John", "last_name": "Smith"}
```

### 3. Smart Fallbacks
- If LLM fails → Rule-based processing
- If no API key → Rule-based only
- If network error → Rule-based only

## Example Improvements

### Before (Rule-based)
```
Email: eatonmonday@gmail.com
Contact: Carol
Customer: On Monday
Output: Carol | On Monday ❌
```

### After (LLM-enhanced)
```
Email: eatonmonday@gmail.com
Contact: Carol
Customer: On Monday
Output: Carol | (empty) ✅
```

## Troubleshooting

### API Key Issues
```
⚠️  OPENAI_API_KEY not found in environment variables
```
**Solution**: Set your API key as shown above.

### Network Issues
```
⚠️  LLM call failed: [error]
```
**Solution**: The script automatically falls back to rule-based processing.

### Cost Concerns
**Solution**: 
1. Use `gpt-4o-mini` model (cheapest)
2. Set `LLM_ENABLED = False` for rule-based only
3. Process in smaller batches

## Performance Tips

### For Large Datasets
1. **Batch Processing**: Process 100-200 rows at a time
2. **Caching**: Save LLM responses to avoid re-processing
3. **Parallel Processing**: Use multiple API calls (with rate limits)

### For Cost Optimization
1. **Pre-filter**: Use rules to identify complex cases first
2. **Model Selection**: Use `gpt-4o-mini` for speed/cost
3. **Temperature**: Keep at 0.1 for consistency

## Expected Results

### Accuracy Improvement
- **Rule-based**: ~70% accuracy on complex cases
- **LLM-enhanced**: ~95% accuracy on complex cases

### Processing Time
- **Rule-based**: ~30 seconds for 679 rows
- **LLM-enhanced**: ~2-3 minutes for 679 rows

### Cost
- **Rule-based**: Free
- **LLM-enhanced**: ~$0.10-0.40 for 679 rows

## Alternative Approaches

### 1. Manual Review
Export problematic cases for manual review:
```python
# Add to script
problematic_cases = df[df['First Name'].isna() | df['Last Name'].isna()]
problematic_cases.to_excel('manual_review.xlsx')
```

### 2. Enhanced Rules
Add more sophisticated pattern matching:
```python
# Add more company indicators
company_indicators.extend(['PRODUCTIONS', 'RESTAURANT', 'STEAKHOUSE'])
```

### 3. Hybrid Processing
Use LLM only for cases that fail rule-based processing:
```python
if not rule_based_result:
    llm_result = llm_parse_name(...)
```

## Support

For issues with:
- **API setup**: Check OpenAI documentation
- **Script errors**: Check Python dependencies
- **Cost concerns**: Use rule-based mode
- **Accuracy issues**: Try different models or manual review 