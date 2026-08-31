import sys
import os

# Add repository root directory to sys.path so modules under scripts/ can be imported in tests
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
