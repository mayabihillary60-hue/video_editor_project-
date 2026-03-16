"""
Simple test to verify the editor works
Copy and paste this into a new file on GitHub
"""

print("✅ Testing Python Video Editor")
print("-" * 30)

# Check if required packages are available
try:
    import cv2
    print("✅ OpenCV is available")
except:
    print("❌ OpenCV not available")

try:
    import numpy
    print("✅ NumPy is available")
except:
    print("❌ NumPy not available")

try:
    import moviepy
    print("✅ MoviePy is available")
except:
    print("❌ MoviePy not available")

print("\n📝 Next steps:")
print("1. Download the code to your computer")
print("2. Install requirements: pip install -r requirements.txt")
print("3. Run: python main.py")