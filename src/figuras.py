"""Genera figura y tabla del informe a partir de salidas/resultados.csv."""
import csv
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

ROOT = Path(__file__).resolve().parents[1]
rows = list(csv.DictReader((ROOT / 'salidas/resultados.csv').open(encoding='utf-8')))
P, q, L = 20000., 10., 2000.
tot = P + q * L

# ---- tabla LaTeX (generada, no escrita a mano)
lines = []
for r in rows:
    bal = abs(float(r['balance_N'])) / tot
    err = r['error_medio_mm']
    err_s = f"{float(err):.3e}" if err else '--'
    lines.append(f"{r['caso'].replace('_', chr(92)+'_')} & {r['n']} & {float(r['u_L_mm']):.4f} & "
                 f"{float(r['R_izq_N']):.0f} & {float(r['R_der_N']):.0f} & {bal:.1e} & {err_s}")
(ROOT / 'informe/tabla_resultados.tex').write_text(' \\\\\n'.join(lines), encoding='utf-8')  # sin '\\\\' final: lo agrega main.tex

# ---- figura: (a) esquema del contorno, (b) error vs tamano de elemento
fig, (a, b) = plt.subplots(1, 2, figsize=(7.0, 2.5), gridspec_kw=dict(width_ratios=[1.15, 1]))
a.set_xlim(-0.12, 1.12); a.set_ylim(-0.9, 1.15); a.axis('off')
for y0, titulo, fijo_der in ((0.45, 'Base: u(0)=0, EA u\'(L)=P', False), (-0.55, 'BC\\_ALTERADO: u(0)=0 y u(L)=0', True)):
    a.add_patch(Rectangle((0, y0 - 0.06), 1, 0.12, fc='0.75', ec='k'))
    a.plot([0, 0], [y0 - 0.2, y0 + 0.2], 'k', lw=2)
    for k in range(5):
        a.plot([-0.05, 0], [y0 - 0.2 + 0.1 * k, y0 - 0.1 + 0.1 * k], 'k', lw=0.8)
    for xx in np.linspace(0.08, 0.92, 7):
        a.annotate('', xy=(xx + 0.06, y0 + 0.08), xytext=(xx, y0 + 0.08), arrowprops=dict(arrowstyle='->', lw=0.7, color='tab:blue'))
    a.annotate('', xy=(1.1, y0), xytext=(1.0, y0), arrowprops=dict(arrowstyle='->', lw=1.6, color='tab:red'))
    a.text(1.1, y0 + 0.1, 'P', color='tab:red', ha='center', fontsize=8)
    a.text(0.5, y0 + 0.28, 'q', color='tab:blue', ha='center', fontsize=8)
    if fijo_der:
        a.plot([1, 1], [y0 - 0.2, y0 + 0.2], 'k', lw=2)
    a.text(0.5, y0 - 0.32, titulo.replace('\\_', '_'), ha='center', fontsize=7.5)
a.text(0.5, 1.05, 'L = 2000 mm; E = 2e5 N/mm$^2$; A = 1000 mm$^2$', ha='center', fontsize=7)
a.set_title('(a) Contorno y cargas', fontsize=8)

base = [r for r in rows if r['caso'].startswith('M')]
h = np.array([L / int(r['n']) for r in base]); e = np.array([float(r['error_medio_mm']) for r in base])
b.loglog(h, e, 'o-', label='MEF (puntos medios)')
b.loglog(h, e[0] * (h / h[0]) ** 2, 'k--', lw=0.8, label='pendiente 2')
for hh, ee, r in zip(h, e, base):
    b.annotate(f"n={r['n']}", (hh, ee), textcoords='offset points', xytext=(4, 4), fontsize=7)
b.set_xlabel('Tamaño de elemento h [mm]', fontsize=8); b.set_ylabel('Error máx. en puntos medios [mm]', fontsize=8)
b.set_xticks([250, 500, 1000]); b.set_xticklabels(['250', '500', '1000']); b.minorticks_off(); b.tick_params(labelsize=7); b.grid(True, which='both', lw=0.3); b.legend(fontsize=7)
b.set_xlim(200, 1400); b.set_ylim(2.5e-4, 1.1e-2); b.set_title('(b) Error de campo vs. h', fontsize=8)
fig.tight_layout(); fig.savefig(ROOT / 'informe/figures/esquema_convergencia.pdf')
fig.savefig(ROOT / 'informe/figures/esquema_convergencia.png', dpi=200)
print('Figura y tabla generadas')
