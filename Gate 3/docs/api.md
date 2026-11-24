# Referencia de Endpoints — API CENABAST

Huella de ejemplos ejecutados: `c9bda992ba8f`
Ejemplos verificados: 6 de 6

Documento generado automáticamente ejecutando `ejemplos_api.py` contra `servicio.main:app`.

## API-01 — Estado operativo del servicio

- **Petición:** `GET /salud`
- **Respuesta HTTP:** `200`

```json
{
  "estado": "ok",
  "entorno": "desarrollo",
  "modelo": "sin clave",
  "modelo_activo": "simulado",
  "respaldo_activo": false
}
```

## API-02 — Consulta normativa de precio de referencia (Paracetamol 500 mg)

- **Petición:** `POST /consultas`
- **Cuerpo JSON:** `{"pregunta": "Cual es el precio de referencia del Paracetamol 500 mg?"}`
- **Respuesta HTTP:** `200`

```json
{
  "respuesta": "Segun el catalogo oficial 2026 de CENABAST, PARACETAMOL 500 MG (Comprimido oral, codigo ONU 51181504) tiene una mediana historica de referencia de $22.40 CLP por unidad, con un rango aceptable de $20.00 - $25.00 CLP y un consumo anual estimado de 145.000.000 unidades [fuente: cenabast_catalogo_precios_referencia_2026.md].",
  "fuentes": [
    "cenabast_catalogo_precios_referencia_2026.md",
    "cenabast_historial_licitaciones_hospitalarias.md"
  ],
  "trace_id": "trace-ejemplo",
  "modo_modelo": "simulado",
  "advertencia_respaldo": null
}
```

## API-03 — Consulta fuera del corpus oficial (abstencion honesta)

- **Petición:** `POST /consultas`
- **Cuerpo JSON:** `{"pregunta": "Cual es la temperatura en Marte hoy?"}`
- **Respuesta HTTP:** `200`

```json
{
  "respuesta": "No encuentro esa informacion en la documentacion oficial de CENABAST.",
  "fuentes": [],
  "trace_id": "trace-ejemplo",
  "modo_modelo": "simulado",
  "advertencia_respaldo": null
}
```

## API-04 — Evaluacion determinista de sobreprecio critico (+50%)

- **Petición:** `POST /precios/evaluar`
- **Cuerpo JSON:** `{"codigo_onu": "51181504", "precio_ofertado": 33.6}`
- **Respuesta HTTP:** `200`

```json
{
  "codigo_onu": "51181504",
  "medicamento": "PARACETAMOL 500 MG",
  "precio_referencia": 22.4,
  "precio_ofertado": 33.6,
  "desviacion_pct": 50.0,
  "categoria": "SOBREPRECIO_CRITICO",
  "requiere_supervision": true,
  "recomendacion": "Sobreprecio critico (> 15.0%): prohibida adjudicacion automatica; activar supervision humana de Jefatura de Adquisiciones.",
  "fuente": "cenabast_catalogo_precios_referencia_2026.md"
}
```

## API-05 — Consulta de expediente precedente de licitacion (LIC-723)

- **Petición:** `GET /licitaciones/LIC-723`
- **Respuesta HTTP:** `200`

```json
{
  "licitacion_id": "LIC-723",
  "expediente_oficial": "723-14-LP24",
  "medicamento": "Paracetamol 500 mg comprimido oral",
  "proveedor": "Proveedor A",
  "precio_ofertado": 33.6,
  "precio_referencia": 22.4,
  "desviacion_pct": 50.0,
  "estado": "RECHAZAR",
  "dictamen": "Sobreprecio critico (+50.0%): vulnera umbral maximo (+15%). Se declaro desierto y se adjudico en $21.90 CLP.",
  "fuente": "cenabast_historial_licitaciones_hospitalarias.md"
}
```

## API-06 — Error uniforme 404 para expediente inexistente (LIC-999)

- **Petición:** `GET /licitaciones/LIC-999`
- **Respuesta HTTP:** `404`

```json
{
  "codigo": "no_encontrado",
  "mensaje": "Licitacion LIC-999 no encontrada."
}
```
