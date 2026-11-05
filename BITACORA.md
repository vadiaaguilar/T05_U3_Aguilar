# Bitácora

| Fecha | Predicción / decisión | Cambio | Prueba y evidencia | Commit |
|---|---|---|---|---|
| 2026-11-05 (antes de ejecutar) | Predicción 1, mallas 2/4/8: con E·A constante, q uniforme y cargas nodales consistentes, el MEF lineal 1D da valores nodales exactos; espero u(L) = (P·L + q·L²/2)/(E·A) = 0,300 mm en las tres mallas, sin cambio al refinar. | Ninguno (solo predicción). | Pendiente: comparar con `salidas/resultados.csv`. | COMPLETAR |
| 2026-11-05 (antes de ejecutar) | Predicción 2, error entre nodos: la solución exacta es cuadrática y el campo MEF es lineal por tramos; espero error máximo en el punto medio = q·h²/(8·E·A), que cae ×4 al duplicar n (pendiente −2 en log-log): 6,25e-3, 1,56e-3 y 3,91e-4 mm para n = 2, 4, 8. | Ninguno (solo predicción). | Pendiente: comparar con `salidas/resultados.csv` y `convergencia.png`. | COMPLETAR |
| 2026-11-05 (antes de ejecutar) | Predicción 3, BC_ALTERADO (n = 8, u(L)=0 añadido, mismas cargas): u(L)=0; el balance sigue cerrando (R_izq + R_der = −(P+qL) = −40000 N) porque la reacción adicional absorbe la carga, pero el problema es otro (hiperestático). Espero R_izq ≈ −q·L/2 = −10000 N y R_der ≈ −(P + q·L/2) = −30000 N. | Ninguno (solo predicción). | Pendiente: comparar con `salidas/resultados.csv`. | COMPLETAR |
| 2026-11-05 | Decisión: conservar `src/barra_mef.py` sin cambios; completar solo `src/analisis.py` (referencia analítica y error en puntos medios). | `src/analisis.py` | `python -m pytest -q` y `python src/ejecutar.py` | COMPLETAR |
