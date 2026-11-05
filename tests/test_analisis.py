import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
import numpy as np
from barra_mef import resolver_barra
from analisis import desplazamiento_referencia, error_puntos_medios

KW = dict(L=2000., E=200000., A=1000., P=20000., q=10.)


def test_referencia_condiciones_de_borde():
    assert desplazamiento_referencia(0., **KW) == 0.
    assert np.isclose(desplazamiento_referencia(KW['L'], **KW), 0.3)
    # EA u'(L) = P por diferencia centrada
    h = 1e-3
    du = (desplazamiento_referencia(KW['L'], **KW) - desplazamiento_referencia(KW['L'] - h, **KW)) / h
    assert np.isclose(KW['E'] * KW['A'] * du, KW['P'], rtol=1e-5)


def test_nodos_exactos_y_error_cuadratico():
    errs = []
    for n in (2, 4, 8):
        r = resolver_barra(n, **KW)
        assert np.allclose(r.u, desplazamiento_referencia(r.x, **KW), atol=1e-12)  # acuerdo nodal
        e = error_puntos_medios(r, **KW)
        assert np.isclose(e, KW['q'] * (KW['L'] / n) ** 2 / (8 * KW['E'] * KW['A']))  # q h^2 / (8 EA)
        errs.append(e)
    assert np.allclose(np.array(errs[:-1]) / np.array(errs[1:]), 4.0)


def test_balance_relativo_caso_base():
    r = resolver_barra(8, **KW)
    R = r.reacciones[r.fijos].sum()
    assert abs(R + KW['P'] + KW['q'] * KW['L']) / abs(KW['P'] + KW['q'] * KW['L']) <= 1e-8
    assert np.allclose(r.reacciones[r.libres], 0., atol=1e-6)  # residuo en grados libres
