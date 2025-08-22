#!/usr/bin/env python3
"""
Edge Case Test Runner for Contact Export Workflow

This script runs the Contact Export workflow against chunked test datasets
and analyzes the results for edge case handling and accuracy.
"""

import os
import sys
import json
import time
import subprocess
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any

class EdgeCaseTestRunner:
    """Runs edge case tests against chunked datasets"""
    
    def __init__(self, test_datasets_dir: str, test_outputs_dir: str):
        self.test_datasets_dir = Path(test_datasets_dir)
        self.test_outputs_dir = Path(test_outputs_dir)
        self.results = []
        
        # Ensure directories exist
        self.test_outputs_dir.mkdir(parents=True, exist_ok=True)
    
    def get_test_chunks(self) -> List[Path]:
        """Get all test chunk files"""
        chunk_files = []
        if self.test_datasets_dir.exists():
            for file_path in self.test_datasets_dir.glob("test_chunk_*.xlsx"):
                chunk_files.append(file_path)
        
        # Sort by pattern type for organized testing
        chunk_files.sort(key=lambda x: x.name)
        return chunk_files
    
    def run_contact_export_test(self, chunk_file: Path) -> Dict[str, Any]:
        """Run Contact Export workflow against a test chunk"""
        print(f"\n🧪 Testing chunk: {chunk_file.name}")
        
        # Create output filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_filename = f"test_output_{chunk_file.stem}_{timestamp}.xlsx"
        output_path = self.test_outputs_dir / output_filename
        
        # Extract pattern type from filename
        pattern_type = chunk_file.stem.replace("test_chunk_", "").split("_")[0]
        
        start_time = time.time()
        
        try:
            # Run the Contact Export workflow
            cmd = [
                sys.executable, "main.py",
                "contact", str(chunk_file),
                "--output-dir", str(self.test_outputs_dir)
            ]
            
            print(f"   📥 Input: {chunk_file}")
            print(f"   📤 Output: {output_path}")
            print(f"   🔄 Running Contact Export workflow...")
            
            # Execute the command
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                cwd=Path.cwd()  # Run from current directory (data_cleaner)
            )
            
            end_time = time.time()
            processing_time = end_time - start_time
            
            # Analyze results
            test_result = {
                'chunk_file': chunk_file.name,
                'pattern_type': pattern_type,
                'output_file': output_filename,
                'processing_time': processing_time,
                'success': result.returncode == 0,
                'stdout': result.stdout,
                'stderr': result.stderr,
                'return_code': result.returncode,
                'timestamp': datetime.now().isoformat()
            }
            
            if result.returncode == 0:
                print(f"   ✅ Test completed successfully in {processing_time:.2f}s")
                print(f"   📊 Output: {output_filename}")
            else:
                print(f"   ❌ Test failed with return code {result.returncode}")
                print(f"   📝 Error: {result.stderr[:200]}...")
            
            return test_result
            
        except Exception as e:
            end_time = time.time()
            processing_time = end_time - start_time
            
            error_result = {
                'chunk_file': chunk_file.name,
                'pattern_type': pattern_type,
                'output_file': None,
                'processing_time': processing_time,
                'success': False,
                'stdout': '',
                'stderr': str(e),
                'return_code': -1,
                'timestamp': datetime.now().isoformat()
            }
            
            print(f"   ❌ Test failed with exception: {e}")
            return error_result
    
    def analyze_test_results(self, test_result: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze the results of a single test"""
        analysis = {
            'chunk_file': test_result['chunk_file'],
            'pattern_type': test_result['pattern_type'],
            'success': test_result['success'],
            'processing_time': test_result['processing_time'],
            'issues_found': [],
            'recommendations': []
        }
        
        if not test_result['success']:
            analysis['issues_found'].append("Workflow execution failed")
            
            if test_result['stderr']:
                # Analyze error patterns
                stderr = test_result['stderr'].lower()
                if 'file not found' in stderr:
                    analysis['issues_found'].append("Input file not found")
                elif 'permission' in stderr:
                    analysis['issues_found'].append("Permission denied")
                elif 'memory' in stderr:
                    analysis['issues_found'].append("Memory allocation error")
                elif 'timeout' in stderr:
                    analysis['issues_found'].append("Processing timeout")
                else:
                    analysis['issues_found'].append("Unknown error occurred")
            
            analysis['recommendations'].append("Check input file path and permissions")
            analysis['recommendations'].append("Verify Contact Export workflow configuration")
            
        else:
            # Check for warnings or issues in stdout
            stdout = test_result['stdout'].lower()
            if 'warning' in stdout:
                analysis['issues_found'].append("Warnings detected in output")
            if 'error' in stdout:
                analysis['issues_found'].append("Errors detected in output")
            
            # Performance analysis
            if test_result['processing_time'] > 60:  # More than 1 minute
                analysis['recommendations'].append("Consider optimizing processing performance")
            
            if test_result['processing_time'] < 1:  # Less than 1 second
                analysis['recommendations'].append("Very fast processing - verify all data was processed")
        
        return analysis
    
    def run_all_tests(self) -> List[Dict[str, Any]]:
        """Run tests against all available chunks"""
        print("🚀 Edge Case Testing Suite for Contact Export Workflow")
        print("=" * 70)
        
        chunk_files = self.get_test_chunks()
        
        if not chunk_files:
            print("❌ No test chunks found!")
            print(f"   Expected location: {self.test_datasets_dir}")
            print("   Run chunk_large_dataset.py first to create test files")
            return []
        
        print(f"📁 Found {len(chunk_files)} test chunks:")
        for chunk_file in chunk_files:
            print(f"   • {chunk_file.name}")
        
        print(f"\n🎯 Starting edge case testing...")
        print(f"   Output directory: {self.test_outputs_dir}")
        
        # Run tests for each chunk
        for i, chunk_file in enumerate(chunk_files, 1):
            print(f"\n📋 Test {i}/{len(chunk_files)}")
            
            # Run the test
            test_result = self.run_contact_export_test(chunk_file)
            
            # Analyze results
            analysis = self.analyze_test_results(test_result)
            
            # Combine results
            full_result = {**test_result, 'analysis': analysis}
            self.results.append(full_result)
            
            # Brief pause between tests
            if i < len(chunk_files):
                time.sleep(1)
        
        return self.results
    
    def generate_test_report(self) -> str:
        """Generate a comprehensive test report"""
        if not self.results:
            return "No test results to report"
        
        # Calculate summary statistics
        total_tests = len(self.results)
        successful_tests = sum(1 for r in self.results if r['success'])
        failed_tests = total_tests - successful_tests
        
        total_processing_time = sum(r['processing_time'] for r in self.results)
        avg_processing_time = total_processing_time / total_tests if total_tests > 0 else 0
        
        # Group by pattern type
        pattern_results = {}
        for result in self.results:
            pattern = result['pattern_type']
            if pattern not in pattern_results:
                pattern_results[pattern] = []
            pattern_results[pattern].append(result)
        
        # Generate report
        report = f"""# Edge Case Testing Report
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## 📊 Test Summary

- **Total Tests**: {total_tests}
- **Successful**: {successful_tests}
- **Failed**: {failed_tests}
- **Success Rate**: {(successful_tests/total_tests*100):.1f}%
- **Total Processing Time**: {total_processing_time:.2f}s
- **Average Processing Time**: {avg_processing_time:.2f}s

## 🧪 Test Results by Pattern Type

"""
        
        for pattern, results in pattern_results.items():
            pattern_success = sum(1 for r in results if r['success'])
            pattern_total = len(results)
            pattern_success_rate = (pattern_success/pattern_total*100) if pattern_total > 0 else 0
            
            report += f"""### {pattern.replace('_', ' ').title()}
- **Tests**: {pattern_total}
- **Success Rate**: {pattern_success_rate:.1f}%
- **Files Tested**: {', '.join(r['chunk_file'] for r in results)}

"""
        
        # Add detailed results
        report += "## 📋 Detailed Test Results\n\n"
        
        for i, result in enumerate(self.results, 1):
            status = "✅ PASS" if result['success'] else "❌ FAIL"
            report += f"""### Test {i}: {result['chunk_file']}
- **Status**: {status}
- **Pattern Type**: {result['pattern_type']}
- **Processing Time**: {result['processing_time']:.2f}s
- **Output File**: {result['output_file'] or 'N/A'}

"""
            
            if result['analysis']['issues_found']:
                report += "- **Issues Found**:\n"
                for issue in result['analysis']['issues_found']:
                    report += f"  - {issue}\n"
            
            if result['analysis']['recommendations']:
                report += "- **Recommendations**:\n"
                for rec in result['analysis']['recommendations']:
                    report += f"  - {rec}\n"
            
            report += "\n"
        
        # Add recommendations
        report += """## 🎯 Recommendations

"""
        
        if failed_tests > 0:
            report += f"- **Immediate Action Required**: {failed_tests} tests failed - investigate and fix issues\n"
        
        if avg_processing_time > 30:
            report += "- **Performance Optimization**: Average processing time is high - consider optimization\n"
        
        if successful_tests == total_tests:
            report += "- **All Tests Passed**: Ready for next phase of testing\n"
        
        report += f"""
## 📁 Files Generated

All test outputs are available in: {self.test_outputs_dir}

## 🔄 Next Steps

1. **Review Failed Tests**: Investigate and resolve any test failures
2. **Analyze Output Quality**: Examine generated files for data quality issues
3. **Edge Case Documentation**: Document any new edge cases discovered
4. **LLM Logic Refinement**: Update prompts based on test results
5. **Performance Optimization**: Address any performance issues identified

---
*Report generated automatically by Edge Case Test Runner*
"""
        
        return report
    
    def save_results(self, output_file: str = None):
        """Save test results and report"""
        if not output_file:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_file = f"edge_case_test_results_{timestamp}.json"
        
        # Save detailed results
        results_file = self.test_outputs_dir / output_file
        with open(results_file, 'w', encoding='utf-8') as f:
            json.dump(self.results, f, indent=2)
        
        # Generate and save report
        report = self.generate_test_report()
        report_file = self.test_outputs_dir / f"edge_case_test_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(report)
        
        print(f"\n📊 Test results saved to: {results_file}")
        print(f"📋 Test report saved to: {report_file}")
        
        return results_file, report_file

def main():
    """Main function to run edge case tests"""
    # Configuration
    test_datasets_dir = "tests/test_datasets"
    test_outputs_dir = "tests/test_outputs"
    
    print("🚀 Edge Case Test Runner for Contact Export Workflow")
    print("=" * 70)
    
    # Check if we're in the right directory
    if not Path("main.py").exists():
        print("❌ Error: main.py not found in current directory")
        print("   Please run this script from the data_cleaner directory")
        return
    
    # Check if test datasets exist
    if not Path(test_datasets_dir).exists():
        print(f"❌ Error: Test datasets directory not found: {test_datasets_dir}")
        print("   Please run chunk_large_dataset.py first to create test files")
        return
    
    # Create test runner
    runner = EdgeCaseTestRunner(test_datasets_dir, test_outputs_dir)
    
    # Run all tests
    results = runner.run_all_tests()
    
    if results:
        # Save results and generate report
        runner.save_results()
        
        print(f"\n🎉 Edge case testing complete!")
        print(f"📊 Results: {len(results)} tests executed")
        print(f"📁 Outputs saved to: {test_outputs_dir}")
        
        # Show summary
        successful = sum(1 for r in results if r['success'])
        print(f"✅ Successful: {successful}/{len(results)}")
        print(f"❌ Failed: {len(results) - successful}/{len(results)}")
        
    else:
        print("\n❌ No tests were executed")

if __name__ == "__main__":
    main()
