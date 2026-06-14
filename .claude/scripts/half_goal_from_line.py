"""即場進球機率公式(Goal-from-Line)。用市場即時大小線L推某時段再進球機率。
用法概念: P = 1-exp(-λ), λ=(L-G)*(T_end-m)/(90-m)*0.9 (上半T_end=45,全場後續=90)。
源自2026-06-14愛沙甲MISS反推:禁止用射正眼球覆蓋市場線。"""
import math
def p_goal(L, G, m, half=True):
    T_end = 45 if half else 90
    k = 0.9 if half else 1.0
    lam = max(0.0, (L - G) * (T_end - m) / (90 - m) * k)
    return 1 - math.exp(-lam), lam
if __name__ == "__main__":
    for name,L,G,m,h in [("愛沙甲0-0@32",2.5,0,32,True),("西澳0-1@43",1.3,1,43,True),
                          ("科威特0-0@36",2.0,0,36,True),("荷日0-0@17",2.4,0,17,True)]:
        p,lam=p_goal(L,G,m,h); print(f"{name}: λ={lam:.2f} P(進球)={p*100:.0f}%")
