# Quick Start Guide: Edge Case Testing

## 🚀 **Get Started in 3 Steps**

### **Step 1: Install Dependencies**
```bash
# Install testing dependencies
pip install -r tests/requirements_testing.txt
```

### **Step 2: Create Test Chunks**
```bash
# Run from data_cleaner directory
python tests/chunk_large_dataset.py
```

This will:
- Analyze the large dataset at `C:\LocalAI\!projects\Stuart\Broadly Report\Broadly RAW\Broadly - 01.01.25-8.04.25 - RawData.xlsx`
- Create targeted chunks for different edge case patterns
- Save chunks in `tests/test_datasets/` folder
- Generate a summary in `chunking_summary.json`

### **Step 3: Run Edge Case Tests**
```bash
# Run from data_cleaner directory
python tests/run_edge_case_tests.py
```

This will:
- Test each chunk with the Contact Export workflow
- Generate test outputs in `tests/test_outputs/` folder
- Create comprehensive test reports
- Save results in JSON format

## 📁 **Expected Output Structure**

```
tests/
├── test_datasets/                    # Input chunks
│   ├── test_chunk_business_names_YYYYMMDD_HHMMSS.xlsx
│   ├── test_chunk_partial_names_YYYYMMDD_HHMMSS.xlsx
│   ├── test_chunk_multiple_names_YYYYMMDD_HHMMSS.xlsx
│   ├── test_chunk_hyphenated_names_YYYYMMDD_HHMMSS.xlsx
│   ├── test_chunk_initials_only_YYYYMMDD_HHMMSS.xlsx
│   ├── test_chunk_random_1_YYYYMMDD_HHMMSS.xlsx
│   └── chunking_summary.json
├── test_outputs/                     # Test results
│   ├── test_output_*.xlsx            # Generated files
│   ├── edge_case_test_results_*.json # Detailed results
│   └── edge_case_test_report_*.md    # Test reports
└── requirements_testing.txt           # Dependencies
```

## 🎯 **Testing Strategy**

### **Phase 1: Pattern-Based Testing**
Test specific edge case patterns:
- **Business Names**: LLC, INC, CORP patterns
- **Partial Names**: Single word names
- **Multiple Names**: "JOHN & JANE SMITH"
- **Hyphenated Names**: "EWING - ERVIN"
- **Initials Only**: "J K" or "A B C"

### **Phase 2: Random Testing**
Test general data quality:
- **Random Chunks**: 100 rows each for variety
- **Chronological Chunks**: Time-based variations

## 📊 **Success Metrics**

- **Pattern Testing**: >95% accuracy for each pattern type
- **Random Testing**: >90% accuracy across random samples
- **Overall Goal**: >95% accuracy for production readiness

## 🔧 **Troubleshooting**

### **Common Issues**

1. **"No test chunks found"**
   - Run `chunk_large_dataset.py` first
   - Check file paths in the script

2. **"main.py not found"**
   - Ensure you're in the `data_cleaner` directory
   - Check that `main.py` exists

3. **Import errors**
   - Install dependencies: `pip install -r tests/requirements_testing.txt`
   - Check Python version compatibility

4. **File permission errors**
   - Ensure write access to output directories
   - Check file paths for special characters

### **Performance Tips**

- Start with smaller chunks (50-100 rows) for initial testing
- Use Ollama for development testing to reduce costs
- Monitor processing time and memory usage
- Test one pattern type at a time for focused debugging

## 📈 **Next Steps After Testing**

1. **Review Test Results**
   - Check success rates for each pattern type
   - Identify failed tests and investigate causes

2. **Analyze Output Quality**
   - Examine generated Excel files
   - Verify name extraction accuracy
   - Check for data quality issues

3. **Document Edge Cases**
   - Record any new edge cases discovered
   - Document LLM behavior patterns
   - Note areas needing prompt refinement

4. **Refine LLM Logic**
   - Update prompts based on test results
   - Optimize for common failure patterns
   - Improve confidence scoring

5. **Iterate and Retest**
   - Make improvements to the system
   - Run tests again to validate fixes
   - Continue until >95% accuracy is achieved

## 🎉 **Expected Outcomes**

By following this testing process, you will:

- **Identify all major edge cases** in your data
- **Achieve >95% accuracy** in name extraction
- **Optimize LLM prompts** for real-world data
- **Build confidence** in production readiness
- **Create comprehensive documentation** of edge case handling

---

**Ready to start?** Run `python tests/chunk_large_dataset.py` to begin! 🚀
