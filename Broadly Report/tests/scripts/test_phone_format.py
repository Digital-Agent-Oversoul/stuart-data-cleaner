import pandas as pd

def test_phone_formatting():
    print("🔍 Testing phone number formatting...")
    
    # Test different phone number formats
    test_phones = [
        "4085063875",
        4085063875,
        "408-506-3875",
        "(408) 506-3875",
        "408.506.3875",
        None,
        "",
        "0",
        "0000000000"
    ]
    
    for phone in test_phones:
        print(f"\n📞 Testing: {phone} (type: {type(phone)})")
        
        # Test the Excel formatting logic
        if phone is not None and phone != '':
            try:
                # Convert to integer and apply custom formatting
                phone_int = int(float(phone))
                print(f"   ✅ Converted to int: {phone_int}")
                print(f"   ✅ Would format as: (*{phone_int//1000000:03d}){phone_int%1000000:03d}-{phone_int%10000:04d}")
            except (ValueError, TypeError) as e:
                print(f"   ❌ Conversion failed: {e}")
        else:
            print(f"   ⚠️  Empty/null value")

if __name__ == "__main__":
    test_phone_formatting() 