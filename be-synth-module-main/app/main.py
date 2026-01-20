import os, sys
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.join(project_root))

from app import App

if __name__ == "__main__":
    
    App().run()