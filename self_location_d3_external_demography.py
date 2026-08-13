"""SELF-LOCATION D3 — external demographic convergence test.

See SELF_LOCATION_D3_PREREGISTRATION.md.
The demographic trajectory is built first from published UN anchors, then compared
with previously obtained D2 cumulative-birth targets. This is an order-of-magnitude
independence check, not an extinction forecast.
"""
import math

CUM_BIRTHS_2100 = 127.036804776e9
P2100 = 10.180160751e9
L2100 = 81.7342
L2300 = 95.0
SCENARIOS = {
    'LOW_2300': 2.3e9,
    'MEDIUM_2300': 9.0e9,
    'HIGH_2300': 36.4e9,
}
TARGETS = {
    'EXACT_2R': 225.960076712e9,
    'D2_LOGUNIFORM_SSA_MEDIAN': 225.957e9,
    'D2_LOGNORMAL_SSA_MEDIAN': 265.100e9,
}


def lerp(a,b,u):
    return a+(b-a)*u


def build_trajectory(p2300):
    cum=CUM_BIRTHS_2100
    rows=[]
    for year in range(2101,2301):
        u=(year-2100)/200.0
        p=lerp(P2100,p2300,u)
        L=lerp(L2100,L2300,u)
        births=p/L
        cum+=births
        rows.append((year,p,L,births,cum))
    return rows


def cross_post2300(cum2300,p2300,target):
    if target<=cum2300:return 2300
    annual=p2300/L2300
    if annual<=0:return None
    years=math.ceil((target-cum2300)/annual)
    return 2300+years


def fmt_b(x):return f'{x/1e9:.3f}B'


def main():
    print('='*84)
    print('SELF-LOCATION D3 — EXTERNAL DEMOGRAPHIC CONVERGENCE TEST')
    print('='*84)
    print(f'fixed cumulative births through 2100 = {fmt_b(CUM_BIRTHS_2100)}')
    print(f'2100 population anchor = {P2100/1e9:.6f}B; turnover/L = {L2100:.4f} y')
    print('2300 endpoints are external UN long-range scenario anchors; D2 targets are unopened until after trajectory construction.\n')

    outputs={}
    for name,p2300 in SCENARIOS.items():
        rows=build_trajectory(p2300)
        cum2300=rows[-1][4]
        births_2101_2300=cum2300-CUM_BIRTHS_2100
        annual2300=p2300/L2300
        outputs[name]=(cum2300,annual2300)
        print(f'[{name}]')
        print(f' population_2300 = {p2300/1e9:.3f}B')
        print(f' approximate births 2101-2300 = {fmt_b(births_2101_2300)}')
        print(f' cumulative births by 2300 = {fmt_b(cum2300)}')
        print(f' stationary post-2300 births/year diagnostic = {annual2300/1e6:.3f}M')
        print()

    print('TARGET COMPARISON — demographic curves above were fixed first')
    overlap=[]
    for name,(cum2300,annual2300) in outputs.items():
        print(f'[{name}]')
        for tname,target in TARGETS.items():
            y=cross_post2300(cum2300,SCENARIOS[name],target)
            print(f' {tname:28s} target={fmt_b(target)} crossing_year={y}')
            if tname=='D2_LOGUNIFORM_SSA_MEDIAN' and y is not None and 2300<=y<=5000:
                overlap.append((name,y))
        print()

    verdict='SCALE_OVERLAP' if overlap else 'NO_NEAR_TERM_SCALE_OVERLAP'
    print('PREDECLARED D3 VERDICT =',verdict)
    if overlap:
        print('scenarios reaching D2 log-uniform+SSA median during 2300-5000 =',', '.join(f'{n}@{y}' for n,y in overlap))
    print('\nINTERPRETATION LOCK:')
    print('- D3 is an order-of-magnitude comparison, not an extinction forecast.')
    print('- B=P/L is an approximate turnover bridge, not official UN births after 2100.')
    print('- The 2300 long-range scenarios are old and strongly fertility-sensitive.')
    print('- SCALE_OVERLAP would show only that the two independent constructions occupy a similar scale.')
    print('- It would not validate SSA, SIA, Canevas, or an exact median-birth hypothesis.')
    print('- No scenario may be preferred post hoc because it matches a target.')
    print('\nFINISHED D3 v1')

if __name__=='__main__':main()
