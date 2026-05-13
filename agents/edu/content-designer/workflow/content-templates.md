# Content Templates

## PPT JSON 結構
```json
{
  "title": "簡報標題",
  "subtitle": "副標題",
  "audience": "executive | developer | power-user",
  "slides": [
    {
      "type": "title",
      "title": "標題",
      "subtitle": "副標題"
    },
    {
      "type": "content",
      "title": "頁面標題",
      "bullets": ["重點 1", "重點 2"],
      "notes": "講者備註"
    },
    {
      "type": "table",
      "title": "表格頁",
      "headers": ["欄位1", "欄位2"],
      "rows": [["值1", "值2"]]
    }
  ]
}
```

## Word/PDF Markdown 結構
- H1: 文件標題
- H2: 章節
- H3: 子章節
- 表格用 Markdown 表格語法
- 程式碼用 fenced code blocks（developer profile 限定）

## 標準開頭結構（每份教材必備）
```markdown
# [教材標題]

**受眾**：[executive / developer / power-user]
**學習目標**：
- 學完後能做到 X
- 學完後能理解 Y

---

## 大綱
1. [章節一]
2. [章節二]
3. [章節三]
```
