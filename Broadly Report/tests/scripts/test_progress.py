import time
import sys

print("Testing progress indicators...")
print("🔄 Starting test...")

for i in range(10):
    print(f"   Progress: {i+1}/10...")
    time.sleep(0.5)
    sys.stdout.flush()  # Force output to display immediately

print("✅ Test completed!") 