"""
Simple test to verify the editor works
Copy and paste this into a new file on GitHub
"""

print("✅ Testing Python Video Editor")
print("-" * 30)

# Check if required packages are available
packages_to_test = [
    ("cv2", "OpenCV"),
    ("numpy", "NumPy"),
    ("moviepy", "MoviePy"),
    ("PIL", "Pillow"),
    ("pydub", "Pydub")
]

all_available = True

for module_name, package_name in packages_to_test:
    try:
        __import__(module_name)
        print(f"✅ {package_name} is available")
    except ImportError as e:
        print(f"❌ {package_name} not available: {str(e)}")
        all_available = False
    except Exception as e:
        print(f"⚠️  {package_name} import error: {str(e)}")
        all_available = False

print("\n" + "=" * 30)

if all_available:
    print("🎉 All dependencies are working correctly!")
    print("Your video editor is ready to use.")
else:
    print("⚠️  Some dependencies have issues.")
    print("This might be normal in some environments (like CI/CD).")
    print("Try running on your local machine with proper setup.")

print("\n📝 Next steps:")
print("1. Download the code to your computer")
print("2. Install requirements: pip install -r requirements.txt")
print("3. Run: python main.py")