import csv
import json
import platform
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
from barra_mef import resolver_barra
from analisis import error_puntos_medios

ROOT = Path(__file__).resolve().parents[1]
def main():
    p=json.loads((ROOT/'datos/barra.json').read_text())
    kw=dict(L=p['L_mm'],E=p['E_MPa'],A=p['A_mm2'],P=p['P_N'],q=p['q_N_mm'])
    rows=[]
    for n in p['mallas']:
        r=resolver_barra(n,**kw)
        err=float(error_puntos_medios(r,**kw))
        if not np.isfinite(err) or err <= 0:
            raise ValueError("El error de campo de este caso debe ser finito y positivo")
        rows.append(dict(caso=f'M{n}',n=n,u_L_mm=r.u[-1],R_izq_N=r.reacciones[0],
                         R_der_N=0.,error_medio_mm=err,
                         balance_N=float(r.reacciones[r.fijos].sum()+r.f.sum())))
    # Modelo deliberadamente alterado: se agrega u(L)=0, manteniendo las cargas.
    r=resolver_barra(8,**kw,extremo_derecho_fijo=True)
    rows.append(dict(caso='BC_ALTERADO',n=8,u_L_mm=r.u[-1],R_izq_N=r.reacciones[0],
                     R_der_N=r.reacciones[-1],error_medio_mm='',
                     balance_N=float(r.reacciones[r.fijos].sum()+r.f.sum())))
    out=ROOT/'salidas'; out.mkdir(exist_ok=True)
    with (out/'resultados.csv').open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
    fig,ax=plt.subplots()
    ax.loglog([r['n'] for r in rows[:3]],[r['error_medio_mm'] for r in rows[:3]],'o-')
    ax.set(xlabel='Numero de elementos [-]',ylabel='Error maximo en puntos medios [mm]')
    ax.grid(True,which='both');fig.tight_layout();fig.savefig(out/'convergencia.png',dpi=180)
    (out/'versiones.txt').write_text(f'Python={platform.python_version()}\nNumPy={np.__version__}\n')
    print('CSV y figura generados. Interprete tambien el caso de contorno alterado.')
if __name__=='__main__':main()
