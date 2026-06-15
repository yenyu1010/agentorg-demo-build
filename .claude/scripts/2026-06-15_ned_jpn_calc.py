import math
def pois(k,l): return l**k*math.exp(-l)/math.factorial(k)
def matrix(lh,la,n=8):
    M=[[pois(i,lh)*pois(j,la) for j in range(n)] for i in range(n)]
    ph=sum(M[i][j] for i in range(n) for j in range(n) if i>j)
    pd=sum(M[i][j] for i in range(n) for j in range(n) if i==j)
    pa=sum(M[i][j] for i in range(n) for j in range(n) if i<j)
    tot=[0]*9
    for i in range(n):
        for j in range(n):
            s=i+j
            if s<=8: tot[s]+=M[i][j]
    return ph,pd,pa,tot
# 殘陣+日本強防→荷蘭攻下修;競爭場
for lh,la,tag in [(1.35,1.15,'基準'),(1.5,1.0,'偏荷蘭'),(1.2,1.25,'偏日本/熱門回歸')]:
    ph,pd,pa,tot=matrix(lh,la)
    over25=sum(tot[3:]); under25=tot[0]+tot[1]+tot[2]
    print(f'[{tag}] λ荷={lh} λ日={la} E[G]={lh+la:.2f}')
    print(f'  荷勝={ph*100:.0f}% 和={pd*100:.0f}% 日勝/不敗={pa*100:.0f}%/{(pd+pa)*100:.0f}%')
    print(f'  大2.5={over25*100:.0f}% 小2.5={under25*100:.0f}%  眾數={tot.index(max(tot))}球')
print()
print('市場去水: 荷46.1/和26.8/日27.1 ; 大2.5@2.04(去水~47%) 小2.5@1.86(~53%)')
print('EV: 日本+0.5@(主流-0.5下盤,約0.82港水=1.82小數)  小2.5@1.86')
# 日本+0.5 = 日不敗 = 和+日勝
for lh,la,tag in [(1.35,1.15,'基準'),(1.2,1.25,'偏日本')]:
    ph,pd,pa,tot=matrix(lh,la)
    p_jp_nl=pd+pa  # 日本+0.5覆蓋
    ev_jp05=p_jp_nl*1.82-1
    under25=tot[0]+tot[1]+tot[2]; ev_u25=under25*1.86-1
    print(f'[{tag}] 日本+0.5@1.82 p={p_jp_nl*100:.0f}% EV={ev_jp05*100:+.0f}% | 小2.5@1.86 p={under25*100:.0f}% EV={ev_u25*100:+.0f}%')
