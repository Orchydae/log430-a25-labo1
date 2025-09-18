# src/tests/conftest.py
import sys, os
# Ajoute le dossier "src" au PYTHONPATH pour que "daos", "models", etc. soient importables
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
