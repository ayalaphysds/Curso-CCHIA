"""Suite pytest de la API FastAPI parametrizada sobre CASOS (Bloque 36.3)."""

import pytest
from fastapi.testclient import TestClient

from casos import CASOS, ejecutar_caso
from servicio.main import app

cliente = TestClient(app, raise_server_exceptions=False)


@pytest.mark.parametrize("caso", CASOS, ids=[c["id"] for c in CASOS])
def test_api_casos(caso):
    ok, obtenido, cuerpo = ejecutar_caso(cliente, caso)
    assert ok, (
        f"Caso {caso['id']} fallo: esperado={caso['estado']} contiene={caso['contiene']!r}, "
        f"obtenido={obtenido}, cuerpo={cuerpo!r}"
    )
