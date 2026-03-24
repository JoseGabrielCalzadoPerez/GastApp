import pytest
from gastapp import GastApp, CATEGORIAS
from database import DatabaseManager
import os

@pytest.fixture
def app():
    db = DatabaseManager("test_gastapp.db")
    app = GastApp()
    app.db = db
    yield app
    os.remove("test_gastapp.db")

def test_registrar_gasto_valido(app):
    resultado = app.registrar_gasto(500.0, "Alimentación", "Supermercado", "2026-02-15")
    assert resultado == True

def test_monto_negativo_lanza_error(app):
    with pytest.raises(ValueError):
        app.registrar_gasto(-100, "Ocio", "Cine", "2026-02-15")

def test_categoria_invalida_lanza_error(app):
    with pytest.raises(ValueError):
        app.registrar_gasto(200, "Videojuegos", "Steam", "2026-02-15")

def test_resumen_mensual(app):
    app.registrar_gasto(300.0, "Transporte", "Gasolina", "2026-02-10")
    app.registrar_gasto(150.0, "Salud", "Farmacia", "2026-02-12")
    resumen = app.obtener_resumen_mensual(2, 2026)
    categorias = [r[0] for r in resumen]
    assert "Transporte" in categorias
    assert "Salud" in categorias