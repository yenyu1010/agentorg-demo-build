"""即場估算：捷U19 布迪祖懷斯(10th) 1-1 柏辛域陀尼亞(4th) @67'
方法：剩餘時間 Poisson。捷克 U19 聯賽場均總進球約 3.2-3.6（青年賽偏高），
取每分鐘總進球率 3.4/95，剩餘 ~28 分鐘（23'+傷停5'）。
實力拆分：客隊第4 vs 主隊第10 → 客隊較強；青年賽主場優勢弱。
三組情境做敏感度。"""
import math

def pois(k, lam): return lam**k * math.exp(-lam) / math.factorial(k)

def outcome(lh, la, maxg=6):
    ph = sum(pois(i,lh)*pois(j,la) for i in range(maxg+1) for j in range(maxg+1) if i>j)
    pd = sum(pois(i,lh)*pois(j,la) for i in range(maxg+1) for j in range(maxg+1) if i==j)
    pa = sum(pois(i,lh)*pois(j,la) for i in range(maxg+1) for j in range(maxg+1) if i<j)
    return ph, pd, pa

minutes_left = 28
rate = 3.4/95
total_rem = rate*minutes_left
print(f"剩餘預期總進球: {total_rem:.3f}")

scenarios = {
    "基準（客隊較強 55/45）": (total_rem*0.45, total_rem*0.55),
    "客隊明顯較強 40/60":     (total_rem*0.40, total_rem*0.60),
    "勢均力敵 50/50":         (total_rem*0.50, total_rem*0.50),
}
print(f"{'情境':<22} {'主再勝':>8} {'維持和局':>8} {'客再勝':>8}")
for name,(lh,la) in scenarios.items():
    ph,pd,pa = outcome(lh,la)
    print(f"{name:<22} {ph*100:>7.1f}% {pd*100:>7.1f}% {pa*100:>7.1f}%")

avg = [sum(outcome(lh,la)[i] for lh,la in scenarios.values())/3 for i in range(3)]
print(f"\n三情境平均: 布迪祖懷斯勝 {avg[0]*100:.1f}% | 和局 {avg[1]*100:.1f}% | 柏辛域陀尼亞勝 {avg[2]*100:.1f}%")
