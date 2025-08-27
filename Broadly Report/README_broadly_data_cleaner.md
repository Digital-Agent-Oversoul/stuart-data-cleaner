# Broadly Data Cleaner

A Python script to clean and process Broadly contract data for strategic survey outreach.

## Overview

This script processes "dirty" spreadsheet data from Broadly contracts and outputs a cleaned version based on the structure of an example cleaned file. The output is designed to support personalized post-contract survey delivery.

## Features

- **Email Filtering**: Removes invalid and generic emails (info@, sales@, etc.)
- **Name Processing**: Extracts and splits names from Contact Name, Customer Name, or email addresses
- **Phone Number Cleaning**: Formats phone numbers as digits only
- **Location Segmentation**: Creates separate tabs for different locations
- **Team Member Assignment**: Assigns assisting team members based on salesperson
- **Duplicate Removal**: Removes duplicate entries
- **Data Sorting**: Sorts by Assisting Team Member

## Usage

```bash
python broadly_data_cleaner.py <input_file.xlsx>
```

### Example

```bash
python broadly_data_cleaner.py "Broadly RAW/12.04.24 - 01.07.25 (1).xlsx"
```

## Output

The script generates an Excel file with the naming schema: `Clean - MM.DD.YYYY.xlsx` where the date is today's local time.

### Output Structure

The output Excel file contains three tabs:
- **South Bay - Milpitas**: Contains the cleaned data
- **East Bay - Castro Valley**: Empty (template for future data)
- **Peninsula - Mountain View**: Empty (template for future data)

### Output Columns

Each tab contains the following columns:
- `Email`: Valid personal email addresses only
- `First Name`: Extracted first name
- `Last Name`: Extracted last name (may be NaN for single names)
- `Phone`: Phone number as digits only
- `Assisting Team Member`: Assigned team member

## Data Processing Rules

### Email Cleaning
- Removes rows with missing or blank emails
- Filters out generic department emails (info@, sales@, ap@, admin@, contact@, support@, help@)
- Removes invalid emails (fff, nan, none, null, error, test)
- Handles multiple emails separated by semicolons or commas
- Keeps the first valid personal email
- Removes rows with "Accounts Receivable" as Salesperson
- **Duplicate Removal**: Removes duplicate entries based on email address (keeps first occurrence)

### Name Processing
- **Intelligent Multi-Source Combination**: Extracts and combines names from all available sources
- **First Name Priority**: Contact Name > Customer Name > Email extraction
- **Last Name Priority**: Contact Name > Customer Name (only if Customer is a person name) > Email extraction
- **Cross-Reference Logic**: Combines partial information from multiple sources (e.g., first name from Contact, last name from Customer)
- **Company Name Detection**: Automatically detects and ignores company names (hospitals, universities, organizations, etc.)
- **Number Removal**: Automatically removes numbers from names (e.g., "Javiercastellanos2" → "Javiercastellanos")
- **Invalid Name Filtering**: Removes single characters, dots, and other invalid last names
- **Email Detection**: If Contact Name contains an email, extracts name from it
- **Multiple Email Handling**: Selects the most relevant email when multiple are present
- **Special Character Handling**: Fixes encoding issues and special characters
- **Conservative Parsing**: Single names are treated as first name only
- **Proper Case Formatting**: Applied to all extracted names

### Phone Number Processing
- Extracts digits only
- Returns None for invalid or zero values
- Applies custom cell formatting: `(000) 000-0000`
- Displays as: `(415) 203-5389`

### Location Assignment
- Based on Salesperson and DEL/PU fields
- Default locations: Milpitas, Dublin, San Jose
- Currently all data goes to Milpitas tab

### Team Member Assignment
- Preserves original Salesperson names as Assisting Team Member
- No mapping - uses actual salesperson names from source data

## Requirements

- Python 3.x
- pandas
- openpyxl

## Dependencies

```bash
pip install pandas openpyxl
```

## Notes

- The script is designed to match the structure of the example cleaned file
- Phone numbers are stored as integers to match the example format
- Name parsing is conservative to match the example's approach
- Location distribution logic can be refined based on actual business rules
- Team member mapping can be updated based on actual assignments 