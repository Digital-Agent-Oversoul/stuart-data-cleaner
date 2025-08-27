#!/usr/bin/env python3
"""
Simple Dataset Chunking Script

This script efficiently chunks the large Broadly dataset into smaller pieces
about the size of the small dataset, preserving column headers from row 3.
"""

import os
import pandas as pd
from pathlib import Path
from datetime import datetime

def get_dataset_info(file_path, header_row=2):
    """Get basic info about a dataset"""
    try:
        # Read just the first few rows to get column info
        df_sample = pd.read_excel(file_path, header=header_row, nrows=5)
        print(f"📊 {Path(file_path).name}:")
        print(f"   Columns: {len(df_sample.columns)}")
        print(f"   Sample columns: {list(df_sample.columns)[:5]}...")
        
        # Get total row count efficiently
        df_full = pd.read_excel(file_path, header=header_row)
        total_rows = len(df_full)
        print(f"   Total rows: {total_rows}")
        return total_rows, df_full.columns.tolist()
        
    except Exception as e:
        print(f"❌ Error reading {file_path}: {e}")
        return 0, []

def create_chunks(large_file, small_file, output_dir, header_row=2):
    """Create chunks from large dataset based on small dataset size"""
    print(f"\n🔍 Analyzing datasets...")
    
    # Get info about both datasets
    small_rows, small_columns = get_dataset_info(small_file, header_row)
    large_rows, large_columns = get_dataset_info(large_file, header_row)
    
    if small_rows == 0 or large_rows == 0:
        print("❌ Could not read one or both datasets")
        return
    
    # Calculate chunk size (target size of small dataset)
    chunk_size = small_rows
    num_chunks = (large_rows + chunk_size - 1) // chunk_size  # Ceiling division
    
    print(f"\n✂️  Creating chunks:")
    print(f"   Target chunk size: {chunk_size} rows")
    print(f"   Number of chunks: {num_chunks}")
    print(f"   Output directory: {output_dir}")
    
    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)
    
    # Read large dataset in chunks to avoid memory issues
    chunks_created = []
    
    for chunk_num in range(num_chunks):
        start_row = chunk_num * chunk_size
        end_row = min(start_row + chunk_size, large_rows)
        
        print(f"\n📁 Creating chunk {chunk_num + 1}/{num_chunks} (rows {start_row + 1}-{end_row})")
        
        try:
            # Read this chunk from the large dataset
            df_chunk = pd.read_excel(
                large_file, 
                header=header_row,
                skiprows=range(header_row + 1, start_row + header_row + 1),  # Skip rows before this chunk
                nrows=end_row - start_row
            )
            
            # Create filename
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            chunk_filename = f"test_chunk_{chunk_num + 1:02d}_{timestamp}.xlsx"
            chunk_path = os.path.join(output_dir, chunk_filename)
            
            # Save chunk
            df_chunk.to_excel(chunk_path, index=False)
            
            chunks_created.append({
                'chunk_number': chunk_num + 1,
                'filename': chunk_filename,
                'rows': len(df_chunk),
                'file_path': chunk_path,
                'row_range': f"{start_row + 1}-{end_row}"
            })
            
            print(f"   ✅ Saved: {chunk_filename} ({len(df_chunk)} rows)")
            
        except Exception as e:
            print(f"   ❌ Error creating chunk {chunk_num + 1}: {e}")
    
    # Create summary
    if chunks_created:
        summary_file = os.path.join(output_dir, "chunking_summary.json")
        summary = {
            'created_at': datetime.now().isoformat(),
            'source_files': {
                'large_dataset': large_file,
                'small_dataset': small_file
            },
            'chunking_config': {
                'header_row': header_row + 1,  # Convert to 1-based for user reference
                'target_chunk_size': chunk_size,
                'total_chunks': num_chunks
            },
            'chunks_created': chunks_created
        }
        
        import json
        with open(summary_file, 'w') as f:
            json.dump(summary, f, indent=2)
        
        print(f"\n🎉 Chunking complete!")
        print(f"📊 Total chunks created: {len(chunks_created)}")
        print(f"📁 All chunks saved to: {output_dir}")
        print(f"📋 Summary file: chunking_summary.json")
        
        print(f"\n🧪 Ready for testing:")
        print(f"   Each chunk is approximately {chunk_size} rows")
        print(f"   Test each chunk individually with the Contact Export workflow")
        print(f"   Review results and identify edge cases")
        
    else:
        print("❌ No chunks were created")

def main():
    """Main function"""
    print("🚀 Simple Dataset Chunking for Testing")
    print("=" * 50)
    
    # File paths
    large_dataset = r"C:\LocalAI\!projects\Stuart\Broadly Report\Broadly RAW\Broadly - 01.01.25-8.04.25 - RawData.xlsx"
    small_dataset = r"C:\LocalAI\!projects\Stuart\Broadly Report\Broadly RAW\Broadly - 7.29.25-8.04.25 - RawData.xlsx"
    output_dir = r"C:\LocalAI\!projects\Stuart\data_cleaner\tests\test_datasets"
    
    # Verify files exist
    if not os.path.exists(large_dataset):
        print(f"❌ Large dataset not found: {large_dataset}")
        return
    
    if not os.path.exists(small_dataset):
        print(f"❌ Small dataset not found: {small_dataset}")
        return
    
    print(f"📁 Large dataset: {Path(large_dataset).name}")
    print(f"📁 Small dataset: {Path(small_dataset).name}")
    print(f"📁 Output directory: {output_dir}")
    
    # Create chunks
    create_chunks(large_dataset, small_dataset, output_dir, header_row=2)

if __name__ == "__main__":
    main()
