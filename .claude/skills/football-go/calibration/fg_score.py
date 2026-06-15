#!/usr/bin/env python3
"""FG-Score v0.2 — 從 4 場實戰（3 正 1 反）歸納的足球走地進球評分公式。
v0.1 → v0.2 關鍵修正：加入「2.0 分水嶺停損」P。
反例桑德尼斯（HT 0-0）讓我們發現：降盤+大球升水的型態在『要進球』與『快死掉』的 0-0
盤面上完全相同，唯一分水嶺是 —— 破蛋前盤口若跌破 2.0 仍 0-0，等於市場把進球定價出去了。
仍為原型，於 tuq_log 暫存；驗證後再考慮正式併入 football-go skill。"""
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

    # NEW v0.2 ── 2.0 分水嶺停損：破蛋前 0-0 時盤口最低降到哪
    scoreless_lines = [s["line"] for s in snaps if goals(s["score"]) == 0]
    min_sl = min(scoreless_lines) if scoreless_lines else 99
    if   min_sl >= 2.0:  pen = 0      # 卡在 2.0 以上 → 進球將至，不罰
    elif min_sl >= 1.75: pen = -25    # 跌破 2.0 到 1.75 → 警訊
    else:                pen = -45    # 跌到 1.5 以下 → 市場已放棄首半球

    raw = c1 + c2 + c3 + c4 + ref
    total = raw + pen
    if not gate:        verdict = "🔴 SKIP (選場不過)"
    elif total >= 70:   verdict = "🟢 STRONG GO"
    elif total >= 50:   verdict = "🟡 GO"
    elif total >= 30:   verdict = "⚪ WAIT/ABORT"
    else:               verdict = "🔴 SKIP"
    return dict(match=d["match"][:24], tl=tl, hcap=hcap, c1=c1, c2=c2, c3=c3, c4=c4,
                ref=ref, hits=",".join(hits) or "-", min_sl=min_sl, pen=pen,
                raw=raw, total=total, verdict=verdict)

rows = [score_match(p) for p in sys.argv[1:]]
print(f"{'賽事':<26}{'線':>4}{'讓':>5} | C1 C2 C3 C4 ref | 最低線  停損 | v0.1 → v0.2  結論")
print("-" * 100)
for r in rows:
    print(f"{r['match']:<24}{r['tl']:>5}{r['hcap']:>5} | "
          f"{r['c1']:>2} {r['c2']:>2} {r['c3']:>2} {r['c4']:>2} {r['ref']:>3} | "
          f"{r['min_sl']:>5}  {r['pen']:>4} | {r['raw']:>3} → {r['total']:>3}   {r['verdict']}")
