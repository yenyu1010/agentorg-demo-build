#!/usr/bin/env python3
"""FG-Score v0.3 — 從 6 場實戰（3 正 3 反）歸納的足球走地進球評分公式。
v0.1: C1-C5 加權計分 → 被反例完全騙過（0-0 將死的盤面型態與將進球者相同）。
v0.2: 加「2.0 分水嶺」軟罰分 → 仍漏掉 min 線=1.75 的反例（印尼U19）。
v0.3: 改為「2.0 硬閘」—— 破蛋前(仍 0-0)盤口只要跌破 2.0 就 ABORT，無視其他分數。
      6 場樣本上達到 3 正 / 3 反「完美二分」：正樣本最低線皆 ≥2.0、反樣本皆 <2.0。
仍為原型；於 calibration 暫存；驗證更多場、邊界(剛好卡2.0卻槓龜)未被證偽前不併入 analyzer。"""
import json, sys

def goals(score):
    try:
        h, a = score.split("-"); return int(h) + int(a)
    except Exception:
        return 0

def score_match(path):
    d = json.load(open(path, encoding="utf-8"))
    pm, snaps = d["pre_match"], d["snapshots"]
    hcap, tl = abs(pm.get("handicap", 0)), pm.get("total_line", 0)
    gate = (hcap >= 0.5) and (tl >= 2.5)

    fg = next((i for i, s in enumerate(snaps) if goals(s["score"]) > 0), len(snaps))
    pre = snaps[: fg] if fg < len(snaps) else snaps

    c1 = 20 if tl >= 3.5 else 15 if tl >= 3.0 else 12 if tl >= 2.75 else 8 if tl >= 2.5 else 0
    drops = sum(1 for i in range(1, len(pre)) if pre[i]["line"] < pre[i-1]["line"])
    c2 = min(drops * 10, 30)
    cyc = sum(1 for i in range(1, len(pre))
              if pre[i]["line"] < pre[i-1]["line"] and pre[i-1].get("over_odds", 0) >= 0.95)
    c3 = min(cyc * 8, 25)
    waves = sum(1 for i in range(1, len(pre))
                if pre[i].get("under_odds", 0) - pre[i-1].get("under_odds", 0) >= 0.07)
    c4 = min(waves * 4, 15)
    gm = [(s["minute"], goals(s["score"])) for s in snaps]
    ref, hits = 0, []
    if any(m <= 20 and g >= 2 for m, g in gm): ref += 6; hits.append("223")
    if any(m <= 30 and g >= 3 for m, g in gm): ref += 3; hits.append("334")
    if any(m <= 75 and g >= 6 for m, g in gm): ref += 3; hits.append("757")
    ref = min(ref, 10)
    raw = c1 + c2 + c3 + c4 + ref

    # v0.3 ── 2.0 硬閘：破蛋前 0-0 盤口最低線
    scoreless = [s["line"] for s in snaps if goals(s["score"]) == 0]
    min_sl = min(scoreless) if scoreless else 99
    floor_ok = min_sl >= 2.0

    if not gate:        verdict = "🔴 SKIP (選場不過)"
    elif not floor_ok:  verdict = "🔴 ABORT (跌破2.0)"
    elif raw >= 70:     verdict = "🟢 STRONG GO"
    elif raw >= 50:     verdict = "🟡 GO"
    elif raw >= 30:     verdict = "⚪ WAIT"
    else:               verdict = "🔴 SKIP"
    return dict(match=d["match"][:22], tl=tl, hcap=hcap, c1=c1, c2=c2, c3=c3, c4=c4,
                ref=ref, min_sl=min_sl, floor="✅" if floor_ok else "❌", raw=raw, verdict=verdict)

rows = [score_match(p) for p in sys.argv[1:]]
print(f"{'賽事':<24}{'線':>4}{'讓':>5} | C1 C2 C3 C4 ref | raw | 最低線 2.0閘 | v0.3 結論")
print("-" * 96)
for r in rows:
    print(f"{r['match']:<22}{r['tl']:>5}{r['hcap']:>5} | "
          f"{r['c1']:>2} {r['c2']:>2} {r['c3']:>2} {r['c4']:>2} {r['ref']:>3} | {r['raw']:>3} | "
          f"{r['min_sl']:>5}  {r['floor']:>3}  | {r['verdict']}")
