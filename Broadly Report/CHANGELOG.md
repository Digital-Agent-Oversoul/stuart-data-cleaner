# Broadly Data Cleaner - Changelog

## Version 2.0 - Location-Based Output with Date Extraction

### New Features

#### 📅 Date Range Extraction
- **Automatic Detection**: Extracts date ranges from source filenames
- **Multiple Patterns**: Supports various date formats:
  - `7.29.25-8.04.25`
  - `12.04.24 - 01.07.25`
  - `MM.DD.YY MM.DD.YY` (space separated)
- **Fallback**: Uses today's date if no date range found

#### 📍 Location-Based Output
- **Separate Files**: Creates distinct output files for Dublin and Milpitas
- **Smart Classification**: 
  - Dublin: DEL/PU contains "DUBLIN" OR Salesperson is "Mark Pringle" or "Cindy Foster"
  - Milpitas: All other records
- **Naming Convention**: `<Location> - <DateRange> - Clean.xlsx`

### File Structure Changes

#### Before
```
Input: "Broadly RAW/12.04.24 - 01.07.25 (1).xlsx"
Output: "Clean - 08.05.2025.xlsx" (single file with tabs)
```

#### After
```
Input: "Broadly RAW/12.04.24 - 01.07.25 (1).xlsx"
Output: 
- "Dublin - 12.04.24-01.07.25 - Clean.xlsx"
- "Milpitas - 12.04.24-01.07.25 - Clean.xlsx"
```

### Updated Functions

#### `extract_date_range_from_filename(filename)`
- Extracts date ranges from source filenames
- Supports multiple date formats
- Returns formatted date string

#### `generate_output_filename(input_filename, location)`
- Creates location-specific output filenames
- Incorporates extracted date range
- Format: `<Location> - <DateRange> - Clean.xlsx`

#### `determine_location(row)`
- Simplified logic for Dublin/Milpitas classification
- Dublin: DEL/PU contains "DUBLIN" OR Salesperson is "Mark Pringle" or "Cindy Foster"
- Milpitas: All other records

#### `clean_data(input_file)`
- Now returns tuple of output filenames
- Creates separate files for each location
- Removed multi-tab workbook approach

#### `create_excel_file(data, filename)`
- New helper function for creating Excel files
- Handles phone number formatting
- Applies proper styling

### Scripts Updated

1. **`broadly_data_cleaner.py`** - Rule-based version
2. **`broadly_data_cleaner_llm.py`** - LLM-enhanced version

### Example Output

```
📁 Input file: Broadly RAW/12.04.24 - 01.07.25 (1).xlsx
📅 Date range detected: 12.04.24-01.07.25
📍 Dublin records: 75
📍 Milpitas records: 604
💾 Dublin data saved to: Dublin - 12.04.24-01.07.25 - Clean.xlsx
💾 Milpitas data saved to: Milpitas - 12.04.24-01.07.25 - Clean.xlsx
```

### Benefits

1. **Better Organization**: Separate files for different locations
2. **Clear Naming**: Date ranges in filenames for easy identification
3. **Location Logic**: Automated classification based on DEL/PU and Salesperson
4. **Consistency**: Both rule-based and LLM versions use same approach

### Backward Compatibility

- Scripts still accept same input format
- Same cleaning logic and data processing
- Only output structure has changed 