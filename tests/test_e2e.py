# tests/test_e2e.py
import os
import requests

# URL de l'API (pointe vers localhost en local, ou vers le service en CI)
BASE_URL = os.getenv("API_URL", "http://localhost:5000")

def test_app_availability():
    """Vérifie la disponibilité de l'application via /health"""
    response = requests.get(f"{BASE_URL}/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_clients_functionality():
    """Vérifie la fonctionnalité métier /clients (au-delà de /health)"""
    response = requests.get(f"{BASE_URL}/clients")
    assert response.status_code == 200
    # On s'attend à récupérer une liste (provenant de MySQL / init.sql)
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0  # S'assure que les données initialisées sont présentes