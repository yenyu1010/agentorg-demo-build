#!/usr/bin/env python3
"""
water_level_analyzer.py — 足球走地進球水位分析器

輸入 JSON 檔案格式：
{
  "match": "TeamA vs TeamB",
  "league": "Premier League",
  "pre_match": {
    "handicap": -0.75,       // 讓球數，負=主讓，正=客讓；選場看 abs(handicap) >= 0.5
    "total_line": 2.5,       // 開賽大小球線；選場看 >= 2.5
    "over_odds_open": 0.90   // 開賽大球水位（選用，供參考）
  },
  "snapshots": [
    {
      "minute": 5,           // 比賽分鐘
      "score": "0-0",        // 當前比分 "主隊-客隊"
      "line": 2.5,           // 當前大小球線
      "over_odds": 0.95,     // 大球水位
      "under_odds": 0.85,    // 小球水位
      "sot": 1               // 累計射正次數（選填）
    }
  ]
}

注意：snapshots 必須依 minute 升序排列。
"""

import json
import sys
import argparse


DIVIDER = "=" * 60
SUB_DIV = "-" * 40


def require(snap, key, idx):
    """取得 snapshot 必填欄位；若欄位不存在則印出繁體中文錯誤並結束。"""
    if key not in snap:
        print(f"錯誤：第 {idx} 筆 snapshot 缺少必填欄位 '{key}'", file=sys.stderr)
        sys.exit(1)
    return snap[key]


def validate_snapshots(snapshots):
    """驗證每筆 snapshot 的必填欄位（under_odds / over_odds / line）。sot 為選填。"""
    required_keys = ("under_odds", "over_odds", "line")
    for idx, snap in enumerate(snapshots):
        for key in required_keys:
            require(snap, key, idx)


def load_json(path):
    """載入並驗證 JSON 檔案。"""
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"[錯誤] 找不到檔案：{path}", file=sys.stderr)
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"[錯誤] JSON 解析失敗：{e}", file=sys.stderr)
        sys.exit(1)

    # 基本欄位驗證
    if "pre_match" not in data:
        print("[錯誤] JSON 缺少 'pre_match' 欄位。", file=sys.stderr)
        sys.exit(1)
    if "snapshots" not in data:
        print("[錯誤] JSON 缺少 'snapshots' 欄位。", file=sys.stderr)
        sys.exit(1)

    # 驗證每筆 snapshot 必填欄位
    validate_snapshots(data["snapshots"])

    return data


def check_pre_match(pre_match):
    """A. 選場檢核。"""
    handicap = pre_match.get("handicap", 0)
    total_line = pre_match.get("total_line", 0)

    abs_handicap = abs(handicap)
    hc_pass = abs_handicap >= 0.5
    tl_pass = total_line >= 2.5

    return {
        "handicap": handicap,
        "abs_handicap": abs_handicap,
        "hc_pass": hc_pass,
        "total_line": total_line,
        "tl_pass": tl_pass,
        "all_pass": hc_pass and tl_pass,
    }


def analyze_under_raises(snapshots):
    """B. 小球升水次數計算。"""
    raises = []
    for i in range(1, len(snapshots)):
        prev = snapshots[i - 1]
        curr = snapshots[i]
        if curr["under_odds"] > prev["under_odds"]:
            raises.append({
                "minute": curr["minute"],
                "from_odds": prev["under_odds"],
                "to_odds": curr["under_odds"],
            })
    return raises


def analyze_over_before_line_drop(snapshots):
    """C. 降盤前大球升水檢查：每個降盤點前的 over_odds 是否持續上漲（無降水）。"""
    results = []
    for i in range(1, len(snapshots)):
        prev_snap = snapshots[i - 1]
        curr_snap = snapshots[i]
        if curr_snap["line"] < prev_snap["line"]:
            # 找降盤點；檢查從頭到此降盤點之前的 over_odds 序列
            segment = snapshots[:i]
            if len(segment) < 2:
                results.append({
                    "at_minute": curr_snap["minute"],
                    "line_change": f"{prev_snap['line']} → {curr_snap['line']}",
                    "consistent_rise": None,
                    "detail": "快照數量不足，無法判斷",
                })
                continue

            # 檢查 segment 中 over_odds 是否每次都上升（允許持平，不允許下降）
            any_drop = False
            drop_at = None
            for j in range(1, len(segment)):
                if segment[j]["over_odds"] < segment[j - 1]["over_odds"]:
                    any_drop = True
                    drop_at = segment[j]["minute"]
                    break

            consistent_rise = not any_drop
            detail = (
                "降盤前 over_odds 持續上漲，無降水 ✓"
                if consistent_rise
                else f"第 {drop_at} 分鐘出現大球降水，訊號減弱"
            )
            results.append({
                "at_minute": curr_snap["minute"],
                "line_change": f"{prev_snap['line']} → {curr_snap['line']}",
                "consistent_rise": consistent_rise,
                "detail": detail,
            })
    return results


def get_line_sequence(snapshots):
    """D. 降盤序列。"""
    sequence = []
    for snap in snapshots:
        sequence.append({"minute": snap["minute"], "line": snap["line"]})
    return sequence


def parse_score(score_str):
    """解析比分字串 'H-A'，回傳總進球數。"""
    try:
        parts = score_str.split("-")
        return int(parts[0]) + int(parts[1])
    except (ValueError, IndexError, AttributeError):
        return 0


def check_reference_rules(snapshots):
    """E. 參考規則 223 / 334 / 757 命中檢查。"""
    hits = []
    hit_223 = hit_334 = hit_757 = False

    for snap in snapshots:
        minute = snap.get("minute", 0)
        goals = parse_score(snap.get("score", "0-0"))

        if not hit_223 and minute <= 20 and goals >= 2:
            hit_223 = True
            hits.append({
                "rule": "223",
                "minute": minute,
                "goals": goals,
                "suggestion": "【223命中】建議追上半場第3球（下注上半 2.5 大）",
            })

        if not hit_334 and minute <= 30 and goals >= 3:
            hit_334 = True
            hits.append({
                "rule": "334",
                "minute": minute,
                "goals": goals,
                "suggestion": "【334命中】建議追上半場第4球（下注上半 3.5 大）",
            })

        if not hit_757 and minute <= 75 and goals >= 6:
            hit_757 = True
            hits.append({
                "rule": "757",
                "minute": minute,
                "goals": goals,
                "suggestion": "【757命中】建議追全場第7球（下注全場 6.5 大）",
            })

    return hits


def compute_signal(pre_check, under_raises, over_before_drop, ref_hits):
    """F. 綜合訊號判斷。"""
    UNDER_THRESHOLD = 4

    if not pre_check["all_pass"]:
        reason_parts = []
        if not pre_check["hc_pass"]:
            reason_parts.append(f"讓球盤 |{pre_check['abs_handicap']}| < 0.5")
        if not pre_check["tl_pass"]:
            reason_parts.append(f"大小球開賽線 {pre_check['total_line']} < 2.5")
        return {
            "signal": "SKIP",
            "reason": "選場條件不通過：" + "；".join(reason_parts),
            "ref_hit_note": "",
        }

    count = len(under_raises)
    # 判斷升水是否在上半場範圍（分鐘 ≤ 45）
    first_half_raises = [r for r in under_raises if r["minute"] <= 45]

    if count >= UNDER_THRESHOLD:
        if len(first_half_raises) >= UNDER_THRESHOLD:
            signal = "GO_FIRST_HALF"
            reason = (
                f"小球升水達 {count} 次（門檻 {UNDER_THRESHOLD}），"
                f"且 {len(first_half_raises)} 次發生在上半場（≤45分）。"
                "上半場有球機率高，可於破蛋盤入手 / 追上半大。"
            )
        else:
            signal = "GO_FULL"
            reason = (
                f"小球升水達 {count} 次（門檻 {UNDER_THRESHOLD}），"
                "強進球訊號，建議追全場大。"
            )
    else:
        signal = "WAIT"
        reason = (
            f"小球升水僅 {count} 次，未達門檻 {UNDER_THRESHOLD}，"
            "訊號不足，繼續觀察走地變化。"
        )

    ref_hit_note = ""
    if ref_hits:
        ref_hit_note = " +參考規則命中：" + "、".join(h["rule"] for h in ref_hits)

    return {
        "signal": signal,
        "reason": reason,
        "ref_hit_note": ref_hit_note,
    }


def print_report(data, pre_check, under_raises, over_before_drop,
                 line_seq, ref_hits, signal_result):
    """輸出完整繁體中文報告。"""
    match_name = data.get("match", "未知賽事")
    league = data.get("league", "未知聯賽")

    print(DIVIDER)
    print("  足球走地進球水位分析報告")
    print(DIVIDER)
    print(f"  賽事：{match_name}")
    print(f"  聯賽：{league}")
    print()

    # ── A. 選場檢核 ──────────────────────────────
    print("【A. 選場檢核】")
    print(SUB_DIV)
    hc_status = "✅ 通過" if pre_check["hc_pass"] else "❌ 不通過"
    tl_status = "✅ 通過" if pre_check["tl_pass"] else "❌ 不通過"
    print(f"  讓球盤  |handicap| = {pre_check['abs_handicap']}  (門檻 ≥ 0.5)  →  {hc_status}")
    print(f"  大小球線 total_line = {pre_check['total_line']}   (門檻 ≥ 2.5)  →  {tl_status}")
    overall = "✅ 進入走地監控" if pre_check["all_pass"] else "⛔ SKIP 此場"
    print(f"  綜合：{overall}")
    print()

    # ── B. 小球升水次數 ──────────────────────────
    print("【B. 小球升水次數】")
    print(SUB_DIV)
    count = len(under_raises)
    threshold_note = "✅ 達門檻（≥4次）" if count >= 4 else f"⚠️  未達門檻（需 ≥4 次，目前 {count} 次）"
    print(f"  總升水次數：{count} 次  →  {threshold_note}")
    if under_raises:
        print("  升水明細：")
        for r in under_raises:
            print(f"    第 {r['minute']:2d} 分鐘：小球水位 {r['from_odds']:.2f} → {r['to_odds']:.2f}")
    else:
        print("  （無升水記錄）")
    print()

    # ── C. 降盤前大球升水檢查 ─────────────────────
    print("【C. 降盤前大球升水檢查】")
    print(SUB_DIV)
    if not over_before_drop:
        print("  （本場無降盤事件）")
    else:
        for item in over_before_drop:
            status = "✅" if item["consistent_rise"] else "⚠️ "
            print(f"  第 {item['at_minute']} 分鐘降盤 ({item['line_change']})：{status} {item['detail']}")
    print()

    # ── D. 降盤序列 ──────────────────────────────
    print("【D. 降盤序列（大小球線變化）】")
    print(SUB_DIV)
    if not line_seq:
        print("  （無快照資料）")
    else:
        for item in line_seq:
            print(f"  第 {item['minute']:2d} 分鐘：line = {item['line']}")
    print()

    # ── E. 參考規則命中 ───────────────────────────
    print("【E. 參考規則命中（223 / 334 / 757）】")
    print(SUB_DIV)
    print("  ⚠️  以下為補充訊號，機率性參考，非穩贏判斷。")
    if ref_hits:
        for h in ref_hits:
            print(f"  ✅ {h['suggestion']}（第 {h['minute']} 分鐘，已進 {h['goals']} 球）")
    else:
        print("  （本場無參考規則命中）")
    print()

    # ── F. 綜合訊號 ──────────────────────────────
    print("【F. 綜合訊號】")
    print(DIVIDER)
    signal = signal_result["signal"]
    reason = signal_result["reason"]
    ref_note = signal_result["ref_hit_note"]

    signal_labels = {
        "GO_FIRST_HALF": "🟢 GO_FIRST_HALF — 上半場有球機率高",
        "GO_FULL":       "🟢 GO_FULL       — 強進球訊號（全場）",
        "WAIT":          "🟡 WAIT          — 訊號不足，持續觀察",
        "SKIP":          "🔴 SKIP          — 選場不通過，此場跳過",
    }
    print(f"  結論：{signal_labels.get(signal, signal)}")
    print(f"  理由：{reason}")
    if ref_note:
        print(f"  {ref_note}")
    print()

    # ── 免責聲明 ──────────────────────────────────
    print(DIVIDER)
    print("  ⚠️  免責聲明：本工具為機率性分析，非穩贏方法、非投資/博弈建議；")
    print("     運彩有風險，請依當地法律、理性娛樂、量力而為。")
    print(DIVIDER)


def main():
    parser = argparse.ArgumentParser(
        description="足球走地進球水位分析器 — 輸入走地盤口 JSON，輸出進球機率訊號報告"
    )
    parser.add_argument("json_path", help="走地盤口快照 JSON 檔案路徑")
    args = parser.parse_args()

    # 載入資料
    data = load_json(args.json_path)
    pre_match = data["pre_match"]
    snapshots = data.get("snapshots", [])

    if not snapshots:
        print("[警告] snapshots 為空，無走地資料可分析。", file=sys.stderr)

    # 各項分析
    pre_check = check_pre_match(pre_match)
    under_raises = analyze_under_raises(snapshots)
    over_before_drop = analyze_over_before_line_drop(snapshots)
    line_seq = get_line_sequence(snapshots)
    ref_hits = check_reference_rules(snapshots)
    signal_result = compute_signal(pre_check, under_raises, over_before_drop, ref_hits)

    # 輸出報告
    print_report(data, pre_check, under_raises, over_before_drop,
                 line_seq, ref_hits, signal_result)


if __name__ == "__main__":
    main()
