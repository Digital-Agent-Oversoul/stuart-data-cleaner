#!/usr/bin/env python3
"""
Test Runner for Stuart Data Cleaner

This script provides an easy way to run various tests and validations
from the test folder.
"""

import sys
import os
from pathlib import Path

# Add project root to path for imports
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

def show_test_menu():
    """Show available test options"""
    print("🧪 Stuart Data Cleaner - Test Runner")
    print("=" * 50)
    print()
    print("Available Tests:")
    print("  1. Full Dataset Test (Contact Export)")
    print("  2. OpenAI API Key Test")
    print("  3. Sample Data Test")
    print("  4. Export Output Test")
    print("  5. Sheet Name Validation")
    print("  6. Data Structure Analysis")
    print("  7. Expected Output Analysis")
    print("  8. Run All Tests")
    print("  0. Exit")
    print()

def run_full_dataset_test():
    """Run the full dataset test"""
    print("🚀 Running Full Dataset Test...")
    try:
        from test_full_dataset import test_full_dataset
        test_full_dataset()
        print("✅ Full dataset test completed successfully!")
    except Exception as e:
        print(f"❌ Full dataset test failed: {e}")

def run_api_key_test():
    """Run the API key test"""
    print("🔑 Running OpenAI API Key Test...")
    try:
        from test_api_key import test_api_key
        test_api_key()
        print("✅ API key test completed!")
    except Exception as e:
        print(f"❌ API key test failed: {e}")

def run_sample_data_test():
    """Run the sample data test"""
    print("📊 Running Sample Data Test...")
    try:
        from test_sample_data import test_sample_data
        test_sample_data()
        print("✅ Sample data test completed!")
    except Exception as e:
        print(f"❌ Sample data test failed: {e}")

def run_export_output_test():
    """Run the export output test"""
    print("📤 Running Export Output Test...")
    try:
        from test_corrected_output import test_corrected_output
        test_corrected_output()
        print("✅ Export output test completed!")
    except Exception as e:
        print(f"❌ Export output test failed: {e}")

def run_sheet_name_validation():
    """Run the sheet name validation"""
    print("📋 Running Sheet Name Validation...")
    try:
        from check_sheet_name_change import check_sheet_name_change
        check_sheet_name_change()
        print("✅ Sheet name validation completed!")
    except Exception as e:
        print(f"❌ Sheet name validation failed: {e}")

def run_data_structure_analysis():
    """Run the data structure analysis"""
    print("🔍 Running Data Structure Analysis...")
    try:
        from analyze_data_structure import analyze_data_structure
        analyze_data_structure()
        print("✅ Data structure analysis completed!")
    except Exception as e:
        print(f"❌ Data structure analysis failed: {e}")

def run_expected_output_analysis():
    """Run the expected output analysis"""
    print("📊 Running Expected Output Analysis...")
    try:
        from analyze_expected_output import analyze_expected_output
        analyze_expected_output()
        print("✅ Expected output analysis completed!")
    except Exception as e:
        print(f"❌ Expected output analysis failed: {e}")

def run_all_tests():
    """Run all available tests"""
    print("🔄 Running All Tests...")
    print()
    
    tests = [
        ("Full Dataset Test", run_full_dataset_test),
        ("API Key Test", run_api_key_test),
        ("Sample Data Test", run_sample_data_test),
        ("Export Output Test", run_export_output_test),
        ("Sheet Name Validation", run_sheet_name_validation),
        ("Data Structure Analysis", run_data_structure_analysis),
        ("Expected Output Analysis", run_expected_output_analysis)
    ]
    
    for test_name, test_func in tests:
        print(f"🧪 Running {test_name}...")
        try:
            test_func()
            print(f"✅ {test_name} completed successfully!")
        except Exception as e:
            print(f"❌ {test_name} failed: {e}")
        print("-" * 40)
    
    print("🎉 All tests completed!")

def main():
    """Main test runner function"""
    while True:
        show_test_menu()
        
        try:
            choice = input("Select test to run (0-8): ").strip()
            
            if choice == "0":
                print("👋 Exiting test runner...")
                break
            elif choice == "1":
                run_full_dataset_test()
            elif choice == "2":
                run_api_key_test()
            elif choice == "3":
                run_sample_data_test()
            elif choice == "4":
                run_export_output_test()
            elif choice == "5":
                run_sheet_name_validation()
            elif choice == "6":
                run_data_structure_analysis()
            elif choice == "7":
                run_expected_output_analysis()
            elif choice == "8":
                run_all_tests()
            else:
                print("❌ Invalid choice. Please select 0-8.")
            
            if choice != "0":
                input("\nPress Enter to continue...")
                print()
                
        except KeyboardInterrupt:
            print("\n👋 Exiting test runner...")
            break
        except Exception as e:
            print(f"❌ Error: {e}")
            input("\nPress Enter to continue...")

if __name__ == "__main__":
    main()
