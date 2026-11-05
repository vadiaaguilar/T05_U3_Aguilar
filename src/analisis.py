"""Referencia analitica y error de campo entre nodos para la barra axial.

Unidades: N y mm (u en mm).
"""
import numpy as np


def desplazamiento_referencia(x, L, E, A, P, q):
    """u(0)=0, EA*u'(L)=P, q uniforme. Devuelva un array en mm.

    De -(EA u')' = q con EA u'(L) = P se obtiene EA u'(x) = P + q (L - x);
    integrando con u(0) = 0:  u(x) = [(P + q L) x - q x^2 / 2] / (E A).
    """
    x = np.asarray(x, dtype=float)
    return ((P + q * L) * x - 0.5 * q * x**2) / (E * A)


def error_puntos_medios(resultado, L, E, A, P, q):
    """Devuelva el maximo error absoluto de u_h frente a u_ref en puntos medios.
    No basta comparar los nodos: interpole u_h linealmente en cada elemento.
    """
    x, u = resultado.x, resultado.u
    xm = 0.5 * (x[:-1] + x[1:])
    uh_m = 0.5 * (u[:-1] + u[1:])  # interpolacion lineal en el punto medio
    u_ref = desplazamiento_referencia(xm, L, E, A, P, q)
    return float(np.max(np.abs(uh_m - u_ref)))
