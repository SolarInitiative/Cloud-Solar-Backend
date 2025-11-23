import sys
import os

# Add the project root to the python path
sys.path.append(os.getcwd())

try:
    from app.main import app
    print("Successfully imported app.main")
except Exception as e:
    print(f"Error importing app.main: {e}")
    sys.exit(1)
