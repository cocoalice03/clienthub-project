# tests/test_unit.py

def add_numbers(a, b):
    """Fonction utilitaire simple à tester unitairement"""
    return a + b

def test_add():
    assert add_numbers(2, 3) == 5
    assert add_numbers(-1, 1) == 0