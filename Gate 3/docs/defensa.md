# Guion de Defensa Técnica — Gate 3 / Capstone (CENABAST)

## 1. Problema (1 min)

Los analistas de adquisiciones de CENABAST revisan ofertas de medicamentos esenciales cruzando manualmente bases administrativas, precios de referencia y precedentes hospitalarios. Ese proceso tarda en promedio treinta y cinco minutos por renglón licitado y expone al presupuesto público a adjudicar ofertas con sobreprecio superior al quince por ciento o incumplir reglas de cadena de frío.

Nuestra solución entrega pre-auditoría asistida en menos de dos segundos por consulta, citando exactamente el documento normativo y clasificando desvíos de precio antes de comprometer gasto fiscal. Queda explícitamente fuera del alcance emitir órdenes de compra en Mercado Público o firmar adjudicaciones sin supervisión humana.

## 2. Arquitectura (2 min)

La plataforma corre en dos contenedores Docker orquestados mediante Docker Compose: una interfaz web liviana en el puerto ocho mil ochenta y la API principal construida con FastAPI, pydantic y uvicorn en el puerto ocho mil. Ambos contenedores usan imágenes con versión fija, usuario sin privilegios y chequeo de salud automático, manteniendo las credenciales de Gemini fuera de la imagen y de Git.

Cada consulta recorre cuatro capas secuenciales: primero, un filtro de seguridad bloquea inyecciones de prompt; segundo, un recuperador léxico determinista busca en cinco documentos oficiales de CENABAST; tercero, un adaptador dual construye el prompt versionado y ejecuta el modelo simulado o real; cuarto, un verificador de fundamentación bloquea fuentes inventadas, cifras falsas o contradicciones críticas.

Se registran 6 decisiones de arquitectura en docs/decisiones.md. Destacan D-01, que prioriza arranque reproducible sin descargas de red al costo de no traducir otros idiomas; D-02, que devuelve error quinientos tres honesto cuando falta clave del modelo real; D-04, que desacopla interfaz y API; D-05, que verifica fundamentación sin duplicar latencia; y D-06, que separa el cálculo determinista de sobreprecio del motor generativo.

## 3. Riesgos y límites (2 min)

Nuestros dos mayores riesgos residuales en la matriz de 9 riesgos son R-01, con residual diez, y R-09, con residual nueve. En R-01, aunque bloqueamos fuentes inventadas, cifras ajenas al contexto y contradicciones directas, dos sondas semánticas sutiles escapan a reglas deterministas; por eso declaramos LIM-03 y exigimos revisión humana del auditor antes de cualquier adjudicación.

En R-09, durante la prueba de transferencia registramos T-05 y T-06: consultas en inglés o con sinónimos coloquiales ausentes del glosario oficial provocan abstención segura sin fuentes. En vez de ocultarlo, fijamos esa conducta como LIM-02 con pruebas de regresión y exigimos usar principios activos oficiales en español.

Finalmente, en R-02 nuestro filtro bloquea seis ataques de inyección, pero el escenario hipotético A-07 evade patrones de texto y queda registrado en LIM-01. Así, nuestras 3 limitaciones declaradas están trazadas de punta a punta entre código, pruebas y riesgos, respaldadas por 6 ejemplos verificados de la API y 83 pruebas automatizadas en verde.

## 4. Demo (2 min)

- PASO-1 Servicio vivo
- PASO-2 Una respuesta con su fuente
- PASO-3 Un expediente de licitacion
- PASO-4 Un error uniforme
- PASO-5 Un ataque rechazado
- PASO-6 Una limitacion a la vista
- PASO-7 Una falla honesta sin modelo

## 5. Cierre (1 min)

Hemos integrado de punta a punta el trabajo de los tres módulos en una aplicación contenerizada, observable y auditable para CENABAST, con pruebas parciales, matriz de calidad, verificación de mitigaciones y documentación comprobada en frío.

Con una semana adicional, integraría un índice vectorial multilingüe para cerrar LIM-02 y un verificador semántico para reducir aún más el residual de R-01. Lo que no cambiaría son los pilares que dieron confiabilidad a la solución: el contrato uniforme de errores de D-03, la falla honesta de D-02 y la separación determinista de reglas de sobreprecio de D-06. Quedo atento a sus preguntas respaldadas en nuestra documentación verificada.

## Diapositivas

| # | Sección | Mensaje clave y evidencia en pantalla |
|---|---|---|
| 1 | Problema | Cuello de botella manual en CENABAST (35 min/renglón), promesa <2 s y límite de alcance |
| 2 | Arquitectura | Diagrama de contenedores Docker Compose (Interfaz :8080 -> API FastAPI :8000) |
| 3 | Arquitectura | Flujo de 4 capas y decisiones D-01, D-02, D-05 y D-06 con sus costos |
| 4 | Riesgos | Matriz de 9 riesgos: R-01 (residual 10), R-09 (residual 9) y R-02 |
| 5 | Riesgos | 3 limitaciones declaradas (LIM-01, LIM-02, LIM-03) y hallazgos T-05, T-06 y A-07 |
| 6 | Demo | Guion en vivo de 7 pasos en menos de 2 minutos (con plan B verificado) |
| 7 | Cierre | Resumen de calidad verificada, hoja de ruta de 1 semana y cierre para preguntas |
