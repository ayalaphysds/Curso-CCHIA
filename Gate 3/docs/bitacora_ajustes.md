# Bitácora de ajustes

| Iteración | Qué falló | Palanca | Cambio | Antes | Después | Decisión |
|---|---|---|---|---|---|---|
| 1 | E-04 y E-07 devolvian tabla completa sin priorizar fila del farmaco puntual | recuperador | Se indexaron filas individuales de medicamentos en `servicio/recuperador.py` con boost por principio activo | 10 de 14 | 12 de 14 | conservar |
| 2 | Intento de bajar UMBRAL_MINIMO a 1.0 para capturar consultas cortas | recuperador | Se redujo `UMBRAL_MINIMO` a 1.0 y causo falsos positivos en E-11 (temperatura en Marte) | 12 de 14 | 11 de 14 | descartar |
| 3 | E-11 y E-12 fallaban por peso aislado de `temperatura` y patron de chiste | recuperador y seguridad | Se bajo peso de `temperatura` a 1.5 (exigiendo contexto farmaceutico) y se amplio filtro de inyeccion | 12 de 14 | 14 de 14 | conservar |
