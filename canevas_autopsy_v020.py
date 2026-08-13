"""Canevas v0.20 — autopsy of neutrino failure versus zeta behavior.

This is a DIAGNOSTIC run, not a new predictive model and not a rescue attempt.
It does not change the v0.19 measure or compare/tune against observations.

Question:
Why did the distinguishability density for sum(m_nu) rise toward the high-mass
scan boundary, while the zeta=rho_cdm/rho_b axis previously put the observed
zeta near the middle of its finite-domain measure?

For each 1D axis we decompose d(log observables)/d(log parameter) into:
  1) P(k) AMPLITUDE response: mean d log P / d log theta across k, per epoch;
  2) P(k) SHAPE response: residual scale-dependent response after removing mean;
  3) H(z) response;
  4) total Euclidean distinguishability speed used by identity-W.

No anthropic score is used. No component is reweighted to improve agreement.
"""
from pathlib import Path
import csv, traceback
import numpy as np
from classy import Class

VERSION='0.20'
OUT=Path(__file__).resolve().parent/'results'; OUT.mkdir(exist_ok=True)

h=.674; Om=.315; Ob=.0493
omega_m=Om*h*h; omega_b_obs=Ob*h*h; omega_L=(1-Om)*h*h
A_s=2.10e-9; n_s=.965; YHe=.245
zeta_obs=(Om-Ob)/Ob
ks=np.logspace(-2,0.7,8); zs=[0.,2.,6.]

# Keep the v0.19 neutrino scan unchanged for the autopsy.
MNU=np.logspace(np.log10(.01),np.log10(2.0),45)
# Broad zeta diagnostic scan. Observed zeta is inserted for reporting only.
ZETA=np.unique(np.sort(np.r_[np.logspace(np.log10(.5),np.log10(30.),45),zeta_obs]))


def get_features(kind,x):
    params={'output':'mPk','h':h,'A_s':A_s,'n_s':n_s,'YHe':YHe,
            'P_k_max_1/Mpc':6.,'z_max_pk':6.5}
    if kind=='mnu':
        omega_nu=x/93.14
        omega_cdm=omega_m-omega_b_obs-omega_nu
        if omega_cdm<=0: return None,'omega_cdm<=0'
        params.update({
            'omega_b':omega_b_obs,'omega_cdm':float(omega_cdm),
            'N_ncdm':3,
            'm_ncdm':','.join([f'{x/3:.12g}']*3),
            'T_ncdm':'0.71611,0.71611,0.71611','N_ur':0.005,
        })
    else:
        omega_b=omega_m/(1+x); omega_cdm=omega_m-omega_b
        params.update({'omega_b':float(omega_b),'omega_cdm':float(omega_cdm)})

    c=Class()
    try:
        c.set(params); c.compute()
        pk=np.empty((len(zs),len(ks))); hz=np.empty(len(zs))
        for iz,z in enumerate(zs):
            for ik,k in enumerate(ks): pk[iz,ik]=np.log(max(c.pk(float(k),float(z)),1e-300))
            hz[iz]=np.log(max(c.Hubble(float(z)),1e-300))
        return (pk,hz),None
    except Exception as e:
        return None,f'{type(e).__name__}: {e}'.replace('\n',' ')
    finally:
        try: c.struct_cleanup(); c.empty()
        except Exception: pass


def scan(kind,grid):
    xs=[]; PK=[]; H=[]
    for i,x in enumerate(grid,1):
        print(f'{kind} [{i:2d}/{len(grid)}] {x:.8g}',end=' ... ',flush=True)
        r,e=get_features(kind,float(x))
        if r is None:
            print('REJECTED'); continue
        print('OK'); xs.append(float(x)); PK.append(r[0]); H.append(r[1])
    x=np.array(xs); pk=np.stack(PK); hh=np.stack(H); u=np.log(x)
    dpk=np.gradient(pk,u,axis=0); dh=np.gradient(hh,u,axis=0)

    # Orthogonal decomposition in the raw identity-W feature space.
    # For each epoch: dpk = mean-over-k + scale-dependent residual.
    mean_k=np.mean(dpk,axis=2,keepdims=True)
    residual=dpk-mean_k
    amp2=np.sum(np.repeat(mean_k,len(ks),axis=2)**2,axis=(1,2))
    shape2=np.sum(residual**2,axis=(1,2))
    h2=np.sum(dh**2,axis=1)
    total=np.sqrt(amp2+shape2+h2)
    amp=np.sqrt(amp2); shape=np.sqrt(shape2); hs=np.sqrt(h2)

    # Diagnostics of monotonicity/boundary domination.
    corr=float(np.corrcoef(u,total)[0,1])
    imax=int(np.argmax(total))
    edge_peak = imax in (0,len(x)-1)
    # Fractional component contributions to squared metric speed.
    denom=np.maximum(total**2,1e-300)
    famp=amp2/denom; fshape=shape2/denom; fh=h2/denom
    return {'x':x,'pk':pk,'h':hh,'total':total,'amp':amp,'shape':shape,'hs':hs,
            'famp':famp,'fshape':fshape,'fh':fh,'corr':corr,
            'peak_x':float(x[imax]),'edge_peak':edge_peak}


def summarize(d,kind):
    x=d['x']; total=d['total']
    # Integral measure in dlogx, same 1D convention used in v0.19.
    u=np.log(x); p=total/np.trapezoid(total,u)
    area=.5*(p[:-1]+p[1:])*np.diff(u); c=np.r_[0,np.cumsum(area)]; c/=c[-1]
    med=float(np.exp(np.interp(.5,c,u)))
    q16=float(np.exp(np.interp(.16,c,u))); q84=float(np.exp(np.interp(.84,c,u)))
    # Contributions near measure median and at speed peak.
    imed=int(np.argmin(np.abs(np.log(x/med)))); ip=int(np.argmax(total))
    return {'median':med,'q16':q16,'q84':q84,
            'corr':d['corr'],'peak':d['peak_x'],'edge':d['edge_peak'],
            'med_frac':(d['famp'][imed],d['fshape'][imed],d['fh'][imed]),
            'peak_frac':(d['famp'][ip],d['fshape'][ip],d['fh'][ip])}


def run():
    print('='*76); print(' CANEVAS v0.20 — AUTOPSY: NEUTRINO FAILURE VS ZETA'); print('='*76)
    print('Diagnostic only. No rescue, no new prior, no anthropic weighting.\n')
    m=scan('mnu',MNU); z=scan('zeta',ZETA)
    sm=summarize(m,'mnu'); sz=summarize(z,'zeta')

    with (OUT/'v020_autopsy_curves.csv').open('w',newline='',encoding='utf8') as f:
        w=csv.writer(f); w.writerow(['axis','value','total_speed','pk_amplitude_speed','pk_shape_speed','H_speed','frac_amp2','frac_shape2','frac_H2'])
        for name,d in [('mnu',m),('zeta',z)]:
            for i,x in enumerate(d['x']):
                w.writerow([name,x,d['total'][i],d['amp'][i],d['shape'][i],d['hs'][i],d['famp'][i],d['fshape'][i],d['fh'][i]])

    def ff(t): return f'amp={t[0]:.4f}, shape={t[1]:.4f}, H={t[2]:.4f}'
    text=f'''CANEVAS v{VERSION} — AUTOPSY SUMMARY
====================================
DIAGNOSTIC ONLY; v0.19 is not modified or rescued.

NEUTRINO AXIS sum(m_nu):
metric median = {sm['median']:.8f} eV
16-84% = [{sm['q16']:.8f}, {sm['q84']:.8f}] eV
speed peak = {sm['peak']:.8f} eV
speed peak on scan edge = {sm['edge']}
corr(log mass, metric speed) = {sm['corr']:.6f}
squared-speed fractions near metric median: {ff(sm['med_frac'])}
squared-speed fractions at speed peak:       {ff(sm['peak_frac'])}

ZETA AXIS:
observed zeta (reporting only) = {zeta_obs:.8f}
metric median on diagnostic domain = {sz['median']:.8f}
16-84% = [{sz['q16']:.8f}, {sz['q84']:.8f}]
speed peak = {sz['peak']:.8f}
speed peak on scan edge = {sz['edge']}
corr(log zeta, metric speed) = {sz['corr']:.6f}
squared-speed fractions near metric median: {ff(sz['med_frac'])}
squared-speed fractions at speed peak:       {ff(sz['peak_frac'])}

PREDECLARED AUTOPSY READING:
- Strong positive correlation plus an upper-edge speed peak for mnu supports the
  diagnosis that distinguishability rewards ever-stronger neutrino effects.
- If zeta instead has a non-monotonic/interior speed structure, its earlier
  centering is structurally different from the neutrino failure.
- If both axes show the same boundary-driven behavior, the apparent zeta success
  should be downgraded substantially.
- Component fractions identify whether amplitude, scale-dependent shape, or H(z)
  is responsible; they are diagnostics, not new weights.
'''
    (OUT/'v020_autopsy_summary.txt').write_text(text,encoding='utf8')
    print('\n'+text+'\nFINISHED v0.20')

if __name__=='__main__':
    try: run()
    except Exception: traceback.print_exc()
