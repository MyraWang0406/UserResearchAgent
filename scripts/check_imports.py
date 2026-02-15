"""Quick import check for backend.api.main to catch import regressions."""
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from backend.api.main import app

if __name__ == "__main__":
    print("ok", app.title)
