#!/usr/bin/env python3
"""
Large Dataset Chunking Script for Edge Case Testing

This script analyzes the large Broadly dataset and creates targeted chunks
for testing different edge cases and patterns in name parsing.
"""

import os
import sys
import json
from pathlib import Path
from datetime import datetime

def analyze_dataset_structure(file_path):
    """Analyze the structure of the large dataset"""
    print(f"🔍 Analyzing dataset: {file_path}")
    
    if not os.path.exists(file_path):
        print(f"❌ File not found: {file_path}")
        return None
    
    # Get file size
    file_size = os.path.getsize(file_path)
    file_size_mb = file_size / (1024 * 1024)
    print(f"📊 File size: {file_size_mb:.2f} MB")
    
    # Try to read with different methods
    try:
        # Try to read as Excel
        import pandas as pd
        df = pd.read_excel(file_path, header=2)  # Row 3 (0-indexed = 2)
        print(f"✅ Successfully read with pandas")
        print(f"📋 Dataset shape: {df.shape}")
        print(f"📝 Columns: {list(df.columns)}")
        return df
    except ImportError:
        print("⚠️  pandas not available, trying alternative methods")
        try:
            # Try openpyxl directly
            from openpyxl import load_workbook
            wb = load_workbook(file_path, read_only=True)
            ws = wb.active
            print(f"✅ Successfully read with openpyxl")
            print(f"📋 Worksheet: {ws.title}")
            print(f"📝 Dimensions: {ws.dimensions}")
            return wb
        except ImportError:
            print("⚠️  openpyxl not available")
            return None

def identify_edge_case_patterns(data):
    """Identify patterns that represent different edge cases"""
    print("\n🔍 Identifying edge case patterns...")
    
    edge_case_patterns = {
        'business_names': [],
        'partial_names': [],
        'complex_names': [],
        'multiple_names': [],
        'hyphenated_names': [],
        'initials_only': [],
        'cultural_names': [],
        'ambiguous_cases': []
    }
    
    if hasattr(data, 'columns'):  # pandas DataFrame
        # Analyze contact names for patterns
        contact_names = data.get('Contact Name', [])
        customer_names = data.get('Customer Name', [])
        
        for i, (contact, customer) in enumerate(zip(contact_names, customer_names)):
            if pd.isna(contact) or str(contact).strip() == '':
                continue
                
            contact_str = str(contact).strip()
            
            # Business name detection
            if any(word in contact_str.upper() for word in ['LLC', 'INC', 'CORP', 'RESTAURANT', 'SCHOOL', 'CHURCH']):
                edge_case_patterns['business_names'].append({
                    'row': i,
                    'contact_name': contact_str,
                    'customer_name': str(customer) if not pd.isna(customer) else '',
                    'pattern': 'business_indicators'
                })
            
            # Partial names (single word)
            elif len(contact_str.split()) == 1:
                edge_case_patterns['partial_names'].append({
                    'row': i,
                    'contact_name': contact_str,
                    'customer_name': str(customer) if not pd.isna(customer) else '',
                    'pattern': 'single_word_name'
                })
            
            # Multiple names (with &, and, +)
            elif any(separator in contact_str for separator in ['&', 'AND', '+']):
                edge_case_patterns['multiple_names'].append({
                    'row': i,
                    'contact_name': contact_str,
                    'customer_name': str(customer) if not pd.isna(customer) else '',
                    'pattern': 'multiple_people'
                })
            
            # Hyphenated names
            elif '-' in contact_str:
                edge_case_patterns['hyphenated_names'].append({
                    'row': i,
                    'contact_name': contact_str,
                    'customer_name': str(customer) if not pd.isna(customer) else '',
                    'pattern': 'hyphenated_name'
                })
            
            # Initials only
            elif all(len(word) <= 2 for word in contact_str.split()):
                edge_case_patterns['initials_only'].append({
                    'row': i,
                    'contact_name': contact_str,
                    'customer_name': str(customer) if not pd.isna(customer) else '',
                    'pattern': 'initials_only'
                })
    
    return edge_case_patterns

def create_targeted_chunks(data, edge_case_patterns, output_dir):
    """Create targeted chunks based on identified patterns"""
    print(f"\n✂️  Creating targeted chunks in: {output_dir}")
    
    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)
    
    chunks_created = []
    
    for pattern_type, cases in edge_case_patterns.items():
        if not cases:
            continue
            
        print(f"\n📁 Creating chunk for: {pattern_type}")
        print(f"   Found {len(cases)} cases")
        
        # Create chunk file
        chunk_filename = f"test_chunk_{pattern_type}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
        chunk_path = os.path.join(output_dir, chunk_filename)
        
        try:
            # Extract rows for this pattern
            if hasattr(data, 'iloc'):  # pandas DataFrame
                chunk_data = data.iloc[[case['row'] for case in cases]]
                chunk_data.to_excel(chunk_path, index=False)
                
                chunks_created.append({
                    'pattern_type': pattern_type,
                    'filename': chunk_filename,
                    'row_count': len(cases),
                    'file_path': chunk_path,
                    'cases': cases[:5]  # First 5 cases for reference
                })
                
                print(f"   ✅ Created: {chunk_filename} ({len(cases)} rows)")
                
        except Exception as e:
            print(f"   ❌ Error creating chunk: {e}")
    
    return chunks_created

def create_random_chunks(data, output_dir, chunk_size=100, num_chunks=5):
    """Create random chunks for general testing"""
    print(f"\n🎲 Creating random chunks in: {output_dir}")
    
    if not hasattr(data, 'iloc'):
        print("⚠️  Cannot create random chunks - data not in expected format")
        return []
    
    total_rows = len(data)
    chunks_created = []
    
    for i in range(num_chunks):
        # Calculate start and end indices
        start_idx = (i * chunk_size) % total_rows
        end_idx = min(start_idx + chunk_size, total_rows)
        
        # Extract chunk
        chunk_data = data.iloc[start_idx:end_idx]
        
        # Create filename with timestamp
        chunk_filename = f"test_chunk_random_{i+1}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
        chunk_path = os.path.join(output_dir, chunk_filename)
        
        try:
            chunk_data.to_excel(chunk_path, index=False)
            chunks_created.append({
                'pattern_type': 'random',
                'filename': chunk_filename,
                'row_count': len(chunk_data),
                'file_path': chunk_path,
                'row_range': f"{start_idx+1}-{end_idx}"
            })
            print(f"   ✅ Created: {chunk_filename} (rows {start_idx+1}-{end_idx})")
        except Exception as e:
            print(f"   ❌ Error creating chunk: {e}")
    
    return chunks_created

def create_chunking_summary(chunks_created, output_dir):
    """Create a summary of all chunks created"""
    summary_file = os.path.join(output_dir, "chunking_summary.json")
    
    summary = {
        'created_at': datetime.now().isoformat(),
        'total_chunks': len(chunks_created),
        'chunks': chunks_created,
        'testing_notes': {
            'pattern_based_chunks': 'Target specific edge cases for focused testing',
            'random_chunks': 'General testing and validation',
            'naming_convention': 'test_chunk_<type>_<timestamp>.xlsx',
            'output_location': output_dir
        }
    }
    
    try:
        with open(summary_file, 'w') as f:
            json.dump(summary, f, indent=2)
        print(f"\n📋 Created chunking summary: {summary_file}")
    except Exception as e:
        print(f"❌ Error creating summary: {e}")
    
    return summary

def main():
    """Main function to chunk the large dataset"""
    print("🚀 Large Dataset Chunking for Edge Case Testing")
    print("=" * 60)
    
    # Configuration
    large_dataset_path = r"C:\LocalAI\!projects\Stuart\Broadly Report\Broadly RAW\Broadly - 01.01.25-8.04.25 - RawData.xlsx"
    output_dir = r"C:\LocalAI\!projects\Stuart\data_cleaner\tests\test_datasets"
    
    print(f"📁 Large dataset: {large_dataset_path}")
    print(f"📁 Output directory: {output_dir}")
    
    # Analyze dataset
    data = analyze_dataset_structure(large_dataset_path)
    if data is None:
        print("❌ Could not analyze dataset. Please check file path and dependencies.")
        return
    
    # Identify edge case patterns
    edge_case_patterns = identify_edge_case_patterns(data)
    
    # Create targeted chunks
    targeted_chunks = create_targeted_chunks(data, edge_case_patterns, output_dir)
    
    # Create random chunks
    random_chunks = create_random_chunks(data, output_dir)
    
    # Combine all chunks
    all_chunks = targeted_chunks + random_chunks
    
    # Create summary
    if all_chunks:
        summary = create_chunking_summary(all_chunks, output_dir)
        
        print(f"\n🎉 Dataset chunking complete!")
        print(f"📊 Total chunks created: {len(all_chunks)}")
        print(f"📁 All chunks saved to: {output_dir}")
        print(f"📋 Summary file: chunking_summary.json")
        
        print(f"\n🧪 Testing Strategy:")
        print(f"   1. Start with pattern-based chunks for edge case testing")
        print(f"   2. Use random chunks for general validation")
        print(f"   3. Test each chunk with the Contact Export workflow")
        print(f"   4. Document any new edge cases discovered")
        print(f"   5. Iterate and refine the LLM logic")
    else:
        print("❌ No chunks were created. Please check the dataset format.")

if __name__ == "__main__":
    main()
