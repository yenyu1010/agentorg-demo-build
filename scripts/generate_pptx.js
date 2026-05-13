const PptxGenJS = require("pptxgenjs");

// 創建簡報
const pres = new PptxGenJS();
pres.defineLayout({ name: 'LAYOUT1', master: 'MASTER1' });

// 設定基礎配置
pres.defineLayout({ name: 'MASTER1', master: 'MASTER1' });

// 定義色彩方案（深藍 + 冰藍 + 白色）
const colors = {
  darkBlue: "1E2761",    // 深藍（主色）
  iceBlue: "CADCFC",     // 冰藍（輔色）
  white: "FFFFFF",       // 白色
  darkText: "2C3E50",    // 深灰（文字）
  accent: "0066CC"       // 亮藍（強調）
};

// 配置簡報屬性
pres.defineLayout({
  name: 'MASTER1',
  master: 'MASTER1'
});

pres.layout = 'MASTER1';
pres.theme = { colors: [colors.darkBlue, colors.iceBlue, colors.white] };

// ==================== 投影片生成 ====================

// 1. 開場投影片
let slide = pres.addSlide();
slide.background = { color: colors.darkBlue };
slide.addText("AI 虛擬組織", {
  x: 0.5, y: 1.5, w: 9, h: 1.5,
  fontSize: 54, bold: true, color: colors.white,
  align: "left", fontFace: "Calibri"
});
slide.addText("讓 Agent 團隊替你工作", {
  x: 0.5, y: 3, w: 9, h: 0.8,
  fontSize: 32, color: colors.iceBlue,
  align: "left", fontFace: "Calibri"
});
slide.addText("AI 實戰進階課程", {
  x: 0.5, y: 5, w: 9, h: 0.5,
  fontSize: 18, color: colors.white, italic: true,
  align: "left"
});
slide.addText("• 為主管和決策者設計\n• 3.5 小時完整課程\n• 涵蓋概念、架構、工作流程、ROI", {
  x: 0.5, y: 5.8, w: 9, h: 1.2,
  fontSize: 14, color: colors.iceBlue,
  align: "left"
});

// 2. 課程目標
slide = pres.addSlide();
slide.background = { color: colors.white };
slide.addText("課程目標", {
  x: 0.5, y: 0.3, w: 9, h: 0.6,
  fontSize: 40, bold: true, color: colors.darkBlue,
  align: "left"
});
slide.addShape(pres.ShapeType.rect, {
  x: 0.5, y: 1.1, w: 9, h: 0.08,
  fill: { color: colors.accent }, line: { type: "none" }
});

const goals = [
  "✓ 理解 Agent 組織的核心概念和優勢",
  "✓ 認識典型的 Agent 組織結構和角色分工",
  "✓ 掌握 Agent 組織的工作流程和協調機制",
  "✓ 評估自己公司是否適合導入 Agent 組織",
  "✓ 規劃導入 Agent 組織的初期步驟和 ROI"
];

goals.forEach((goal, idx) => {
  slide.addText(goal, {
    x: 1.2, y: 1.5 + (idx * 0.65), w: 8.3, h: 0.55,
    fontSize: 16, color: colors.darkText,
    align: "left", valign: "top"
  });
});

// 3. 課程概述
slide = pres.addSlide();
slide.background = { color: colors.white };
slide.addText("課程概述", {
  x: 0.5, y: 0.3, w: 9, h: 0.6,
  fontSize: 40, bold: true, color: colors.darkBlue,
  align: "left"
});
slide.addShape(pres.ShapeType.rect, {
  x: 0.5, y: 1.1, w: 9, h: 0.08,
  fill: { color: colors.accent }, line: { type: "none" }
});

const sections = [
  { title: "第一單元", content: "為什麼需要 Agent 團隊？", time: "35 分鐘" },
  { title: "第二單元", content: "認識 Agent 組織架構", time: "45 分鐘" },
  { title: "休息", content: "", time: "15 分鐘" },
  { title: "第三單元", content: "工作流動 - 六步驟自動化", time: "45 分鐘" },
  { title: "第四單元", content: "效益試算與導入計畫", time: "35 分鐘" }
];

sections.forEach((sec, idx) => {
  const yPos = 1.5 + (idx * 0.65);
  
  slide.addShape(pres.ShapeType.rect, {
    x: 1, y: yPos, w: 8, h: 0.55,
    fill: { color: idx === 2 ? colors.iceBlue : colors.white },
    line: { color: colors.iceBlue, width: 2 }
  });
  
  slide.addText(sec.title, {
    x: 1.2, y: yPos + 0.05, w: 3, h: 0.25,
    fontSize: 14, bold: true, color: colors.darkBlue
  });
  
  if (sec.content) {
    slide.addText(sec.content, {
      x: 1.2, y: yPos + 0.3, w: 5, h: 0.2,
      fontSize: 12, color: colors.darkText
    });
  }
  
  slide.addText(sec.time, {
    x: 7.2, y: yPos + 0.15, w: 1.5, h: 0.25,
    fontSize: 12, color: colors.accent, align: "right", bold: true
  });
});

// ========== 單元一：為什麼需要 Agent ========== 

// 4. 單元一開場
slide = pres.addSlide();
slide.background = { color: colors.darkBlue };
slide.addText("第一單元", {
  x: 0.5, y: 1.5, w: 9, h: 0.8,
  fontSize: 48, bold: true, color: colors.iceBlue,
  align: "left"
});
slide.addText("為什麼需要 Agent 團隊？", {
  x: 0.5, y: 2.5, w: 9, h: 1,
  fontSize: 40, bold: true, color: colors.white,
  align: "left"
});
slide.addText("一個 AI 不夠用的時代", {
  x: 0.5, y: 3.8, w: 9, h: 0.6,
  fontSize: 24, color: colors.iceBlue, italic: true,
  align: "left"
});

// 5. 三大痛點
slide = pres.addSlide();
slide.background = { color: colors.white };
slide.addText("企業的三大痛點", {
  x: 0.5, y: 0.3, w: 9, h: 0.6,
  fontSize: 40, bold: true, color: colors.darkBlue,
  align: "left"
});
slide.addShape(pres.ShapeType.rect, {
  x: 0.5, y: 1.1, w: 9, h: 0.08,
  fill: { color: colors.accent }, line: { type: "none" }
});

const painPoints = [
  {
    title: "痛點一：任務太複雜",
    desc: "多人協調浪費時間，溝通成本高，容易出現協調失敗"
  },
  {
    title: "痛點二：容易出錯",
    desc: "沒有人驗收，品質難以保證，錯誤流向用戶才被發現"
  },
  {
    title: "痛點三：重複說明",
    desc: "每次都要重新解釋背景，同樣的信息被問多次"
  }
];

painPoints.forEach((point, idx) => {
  const yPos = 1.5 + (idx * 1.8);
  
  slide.addShape(pres.ShapeType.rect, {
    x: 0.7, y: yPos, w: 8.6, h: 1.5,
    fill: { color: idx === 0 ? "#FFE6E6" : idx === 1 ? "#FFF4E6" : "#E6F2FF" },
    line: { color: colors.iceBlue, width: 1 }
  });
  
  slide.addText(point.title, {
    x: 1, y: yPos + 0.15, w: 8, h: 0.35,
    fontSize: 16, bold: true, color: colors.darkBlue
  });
  
  slide.addText(point.desc, {
    x: 1, y: yPos + 0.55, w: 8, h: 0.8,
    fontSize: 13, color: colors.darkText
  });
});

// 6. Agent 解法
slide = pres.addSlide();
slide.background = { color: colors.white };
slide.addText("Agent 組織的解法", {
  x: 0.5, y: 0.3, w: 9, h: 0.6,
  fontSize: 40, bold: true, color: colors.darkBlue,
  align: "left"
});
slide.addShape(pres.ShapeType.rect, {
  x: 0.5, y: 1.1, w: 9, h: 0.08,
  fill: { color: colors.accent }, line: { type: "none" }
});

const solutions = [
  { pain: "任務複雜", solution: "自動分派給對應專家", benefit: "⬇ 時間 -50%" },
  { pain: "容易出錯", solution: "三層驗收把關", benefit: "⬇ 出錯 -80%" },
  { pain: "重複說明", solution: "共用記憶系統", benefit: "⬆ 效率 +70%" }
];

slide.addText("痛點", {
  x: 0.7, y: 1.3, w: 2.5, h: 0.35,
  fontSize: 13, bold: true, color: colors.darkText
});
slide.addText("Agent 解法", {
  x: 3.5, y: 1.3, w: 3, h: 0.35,
  fontSize: 13, bold: true, color: colors.darkText
});
slide.addText("效益", {
  x: 7, y: 1.3, w: 2.5, h: 0.35,
  fontSize: 13, bold: true, color: colors.darkText
});

solutions.forEach((sol, idx) => {
  const yPos = 1.9 + (idx * 1.5);
  
  slide.addText(sol.pain, {
    x: 0.7, y: yPos, w: 2.5, h: 1.3,
    fontSize: 14, color: colors.darkText, align: "left", valign: "top"
  });
  
  slide.addText(sol.solution, {
    x: 3.5, y: yPos, w: 3, h: 1.3,
    fontSize: 14, color: colors.darkBlue, bold: true, align: "left", valign: "top"
  });
  
  slide.addText(sol.benefit, {
    x: 7, y: yPos, w: 2.5, h: 1.3,
    fontSize: 14, color: colors.accent, bold: true, align: "left", valign: "top"
  });
});

// ========== 單元二：Agent 組織架構 ==========

// 7. 單元二開場
slide = pres.addSlide();
slide.background = { color: colors.darkBlue };
slide.addText("第二單元", {
  x: 0.5, y: 1.5, w: 9, h: 0.8,
  fontSize: 48, bold: true, color: colors.iceBlue,
  align: "left"
});
slide.addText("認識 Agent 組織架構", {
  x: 0.5, y: 2.5, w: 9, h: 1,
  fontSize: 40, bold: true, color: colors.white,
  align: "left"
});
slide.addText("12 位虛擬員工的協作模式", {
  x: 0.5, y: 3.8, w: 9, h: 0.6,
  fontSize: 24, color: colors.iceBlue, italic: true,
  align: "left"
});

// 8. Agent 組織結構概览
slide = pres.addSlide();
slide.background = { color: colors.white };
slide.addText("Agent 組織的三層結構", {
  x: 0.5, y: 0.3, w: 9, h: 0.6,
  fontSize: 40, bold: true, color: colors.darkBlue,
  align: "left"
});
slide.addShape(pres.ShapeType.rect, {
  x: 0.5, y: 1.1, w: 9, h: 0.08,
  fill: { color: colors.accent }, line: { type: "none" }
});

const layers = [
  { name: "共用資源層", count: "2 位", roles: "意圖分析師、研究員" },
  { name: "軟體開發部", count: "6 位", roles: "經理、架構師、工程師、測試員、審查員、維運員" },
  { name: "營運管理部", count: "4 位", roles: "經理、Agent 建置師、治理官、演化師" },
  { name: "教育訓練部", count: "4 位", roles: "經理、研究員、內容設計師、生成師" }
];

layers.forEach((layer, idx) => {
  const yPos = 1.5 + (idx * 1.6);
  
  slide.addShape(pres.ShapeType.rect, {
    x: 0.7, y: yPos, w: 8.6, h: 1.4,
    fill: { color: colors.iceBlue }, 
    line: { color: colors.darkBlue, width: 2 }
  });
  
  slide.addText(layer.name, {
    x: 1, y: yPos + 0.15, w: 6, h: 0.35,
    fontSize: 16, bold: true, color: colors.darkBlue
  });
  
  slide.addText(layer.count, {
    x: 7, y: yPos + 0.15, w: 1.3, h: 0.35,
    fontSize: 14, bold: true, color: colors.darkBlue, align: "right"
  });
  
  slide.addText(layer.roles, {
    x: 1, y: yPos + 0.55, w: 7.3, h: 0.7,
    fontSize: 12, color: colors.darkText
  });
});

// 9. Agent 的「靈魂」
slide = pres.addSlide();
slide.background = { color: colors.white };
slide.addText("每個 Agent 都有『靈魂』", {
  x: 0.5, y: 0.3, w: 9, h: 0.6,
  fontSize: 40, bold: true, color: colors.darkBlue,
  align: "left"
});
slide.addShape(pres.ShapeType.rect, {
  x: 0.5, y: 1.1, w: 9, h: 0.08,
  fill: { color: colors.accent }, line: { type: "none" }
});

slide.addText("『靈魂』= 職位說明書，包括：", {
  x: 0.7, y: 1.5, w: 8.6, h: 0.3,
  fontSize: 14, bold: true, color: colors.darkText
});

const soulPoints = [
  "🎯 職責：這個 Agent 負責什麼工作",
  "📋 原則：核心決策標準（例如：風險最小化、客戶第一）",
  "🚫 邊界：這個 Agent 絕對不做什麼事"
];

soulPoints.forEach((point, idx) => {
  slide.addText(point, {
    x: 1.2, y: 2 + (idx * 0.7), w: 8, h: 0.55,
    fontSize: 14, color: colors.darkText
  });
});

slide.addShape(pres.ShapeType.rect, {
  x: 0.7, y: 4.2, w: 8.6, h: 1.5,
  fill: { color: "#F0F4FF" },
  line: { color: colors.iceBlue, width: 1 }
});

slide.addText("💡 為什麼重要？", {
  x: 1, y: 4.35, w: 8, h: 0.3,
  fontSize: 13, bold: true, color: colors.darkBlue
});

slide.addText("『靈魂』確保所有 Agent 有『同樣的價值觀』，所以他們即使『獨立工作』也能『步調一致』，不會相互矛盾。", {
  x: 1, y: 4.7, w: 8, h: 1,
  fontSize: 12, color: colors.darkText
});

// 10. 共用記憶系統
slide = pres.addSlide();
slide.background = { color: colors.white };
slide.addText("共用記憶系統", {
  x: 0.5, y: 0.3, w: 9, h: 0.6,
  fontSize: 40, bold: true, color: colors.darkBlue,
  align: "left"
});
slide.addShape(pres.ShapeType.rect, {
  x: 0.5, y: 1.1, w: 9, h: 0.08,
  fill: { color: colors.accent }, line: { type: "none" }
});

slide.addText("所有 Agent 都看得到的『公司知識庫』：", {
  x: 0.7, y: 1.5, w: 8.6, h: 0.3,
  fontSize: 14, bold: true, color: colors.darkText
});

const memoryItems = [
  "📌 公司的願景和使命",
  "✅ 已做過的決策和為什麼做",
  "👥 客戶資訊和市場情報",
  "📁 過去的專案檔案和經驗"
];

memoryItems.forEach((item, idx) => {
  slide.addText(item, {
    x: 1.2, y: 2 + (idx * 0.65), w: 8, h: 0.55,
    fontSize: 14, color: colors.darkText
  });
});

slide.addShape(pres.ShapeType.rect, {
  x: 0.7, y: 4.8, w: 8.6, h: 1.2,
  fill: { color: "#E6F2FF" },
  line: { color: colors.accent, width: 1 }
});

slide.addText("💡 效益：不用『每次重新解釋』，Agent 自動看到背景信息，效率提升 70%", {
  x: 1, y: 4.95, w: 8.2, h: 1,
  fontSize: 13, color: colors.darkText, bold: true
});

// ========== 單元三：六步驟工作流程 ==========

// 11. 單元三開場
slide = pres.addSlide();
slide.background = { color: colors.darkBlue };
slide.addText("第三單元", {
  x: 0.5, y: 1.5, w: 9, h: 0.8,
  fontSize: 48, bold: true, color: colors.iceBlue,
  align: "left"
});
slide.addText("工作流動 - 六步驟自動化", {
  x: 0.5, y: 2.5, w: 9, h: 1,
  fontSize: 40, bold: true, color: colors.white,
  align: "left"
});
slide.addText("從需求到完成的完整流程", {
  x: 0.5, y: 3.8, w: 9, h: 0.6,
  fontSize: 24, color: colors.iceBlue, italic: true,
  align: "left"
});

// 12. 六步驟流程
slide = pres.addSlide();
slide.background = { color: colors.white };
slide.addText("六步驟自動化流程", {
  x: 0.5, y: 0.3, w: 9, h: 0.6,
  fontSize: 40, bold: true, color: colors.darkBlue,
  align: "left"
});
slide.addShape(pres.ShapeType.rect, {
  x: 0.5, y: 1.1, w: 9, h: 0.08,
  fill: { color: colors.accent }, line: { type: "none" }
});

const steps = [
  "1. 分類\n意圖分析師判斷『這應該給誰』",
  "2. 評估\n經理評估『需要什麼資源』",
  "3. 分派\n清楚的指令發給每個人",
  "4. 執行\n各司其職，並行工作",
  "5. 驗收\n三層把關，確保品質",
  "6. 彙整\n經理回報最終成果"
];

steps.forEach((step, idx) => {
  const col = idx % 3;
  const row = Math.floor(idx / 3);
  const xPos = 0.6 + (col * 3.1);
  const yPos = 1.5 + (row * 2.8);
  
  slide.addShape(pres.ShapeType.rect, {
    x: xPos, y: yPos, w: 2.9, h: 2.5,
    fill: { color: colors.iceBlue },
    line: { color: colors.darkBlue, width: 2 }
  });
  
  slide.addText(step, {
    x: xPos + 0.15, y: yPos + 0.2, w: 2.6, h: 2.1,
    fontSize: 12, bold: true, color: colors.darkBlue, align: "center", valign: "middle"
  });
});

// 13. 三層驗收
slide = pres.addSlide();
slide.background = { color: colors.white };
slide.addText("三層驗收 - 品質保障", {
  x: 0.5, y: 0.3, w: 9, h: 0.6,
  fontSize: 40, bold: true, color: colors.darkBlue,
  align: "left"
});
slide.addShape(pres.ShapeType.rect, {
  x: 0.5, y: 1.1, w: 9, h: 0.08,
  fill: { color: colors.accent }, line: { type: "none" }
});

const layers3 = [
  { name: "層一：測試員", desc: "功能測試\n有沒有符合需求？" },
  { name: "層二：審查員", desc: "程式碼審查\n安全、效能、可維護性？" },
  { name: "層三：維運員", desc: "部署檢查\n上線會不會出問題？" }
];

layers3.forEach((layer, idx) => {
  const yPos = 1.6 + (idx * 2.2);
  
  slide.addShape(pres.ShapeType.rect, {
    x: 0.7, y: yPos, w: 8.6, h: 1.9,
    fill: { color: colors.white },
    line: { color: colors.accent, width: 2 }
  });
  
  slide.addShape(pres.ShapeType.rect, {
    x: 0.7, y: yPos, w: 0.15, h: 1.9,
    fill: { color: colors.accent },
    line: { type: "none" }
  });
  
  slide.addText(layer.name, {
    x: 1, y: yPos + 0.15, w: 8.3, h: 0.35,
    fontSize: 15, bold: true, color: colors.darkBlue
  });
  
  slide.addText(layer.desc, {
    x: 1, y: yPos + 0.55, w: 8.3, h: 1.2,
    fontSize: 13, color: colors.darkText
  });
});

// ========== 單元四：效益試算與導入 ==========

// 14. 單元四開場
slide = pres.addSlide();
slide.background = { color: colors.darkBlue };
slide.addText("第四單元", {
  x: 0.5, y: 1.5, w: 9, h: 0.8,
  fontSize: 48, bold: true, color: colors.iceBlue,
  align: "left"
});
slide.addText("效益試算與導入計畫", {
  x: 0.5, y: 2.5, w: 9, h: 1,
  fontSize: 40, bold: true, color: colors.white,
  align: "left"
});
slide.addText("值不值得？怎樣開始？", {
  x: 0.5, y: 3.8, w: 9, h: 0.6,
  fontSize: 24, color: colors.iceBlue, italic: true,
  align: "left"
});

// 15. 成本對比
slide = pres.addSlide();
slide.background = { color: colors.white };
slide.addText("成本對比：傳統 vs Agent 組織", {
  x: 0.5, y: 0.3, w: 9, h: 0.6,
  fontSize: 40, bold: true, color: colors.darkBlue,
  align: "left"
});
slide.addShape(pres.ShapeType.rect, {
  x: 0.5, y: 1.1, w: 9, h: 0.08,
  fill: { color: colors.accent }, line: { type: "none" }
});

// 成本對比表
const costData = [
  { label: "單個功能成本", traditional: "$22,000", agent: "$170" },
  { label: "月功能數", traditional: "4 個", agent: "4 個" },
  { label: "年度開發成本", traditional: "$1,056,000", agent: "$8,160" },
  { label: "額外成本（管理、維護）", traditional: "$50,000+", agent: "$10,000" },
  { label: "年度總成本", traditional: "$1.1M", agent: "$22.5K" }
];

slide.addText("指標", {
  x: 0.7, y: 1.3, w: 3.5, h: 0.35,
  fontSize: 13, bold: true, color: colors.darkBlue
});
slide.addText("傳統做法", {
  x: 4.3, y: 1.3, w: 2.5, h: 0.35,
  fontSize: 13, bold: true, color: colors.darkText, align: "center"
});
slide.addText("Agent 組織", {
  x: 7, y: 1.3, w: 2.5, h: 0.35,
  fontSize: 13, bold: true, color: colors.accent, align: "center"
});

costData.forEach((item, idx) => {
  const yPos = 1.8 + (idx * 0.6);
  
  slide.addText(item.label, {
    x: 0.7, y: yPos, w: 3.5, h: 0.5,
    fontSize: 12, color: colors.darkText
  });
  
  slide.addText(item.traditional, {
    x: 4.3, y: yPos, w: 2.5, h: 0.5,
    fontSize: 12, color: colors.darkText, align: "center", bold: true
  });
  
  slide.addText(item.agent, {
    x: 7, y: yPos, w: 2.5, h: 0.5,
    fontSize: 12, color: colors.accent, align: "center", bold: true
  });
});

// 16. ROI 計算
slide = pres.addSlide();
slide.background = { color: colors.white };
slide.addText("ROI 計算結果", {
  x: 0.5, y: 0.3, w: 9, h: 0.6,
  fontSize: 40, bold: true, color: colors.darkBlue,
  align: "left"
});
slide.addShape(pres.ShapeType.rect, {
  x: 0.5, y: 1.1, w: 9, h: 0.08,
  fill: { color: colors.accent }, line: { type: "none" }
});

slide.addShape(pres.ShapeType.rect, {
  x: 0.7, y: 1.5, w: 8.6, h: 3.5,
  fill: { color: "#E6F2FF" },
  line: { color: colors.accent, width: 2 }
});

slide.addText("年度節省成本", {
  x: 1, y: 1.8, w: 8, h: 0.4,
  fontSize: 16, bold: true, color: colors.darkText
});

slide.addText("$1,077,440", {
  x: 1, y: 2.3, w: 8, h: 0.6,
  fontSize: 48, bold: true, color: colors.accent
});

slide.addText("投資報酬率（ROI）", {
  x: 1, y: 3.1, w: 8, h: 0.4,
  fontSize: 16, bold: true, color: colors.darkText
});

slide.addText("47.7x", {
  x: 1, y: 3.6, w: 8, h: 0.6,
  fontSize: 48, bold: true, color: colors.accent
});

slide.addText("投資回本期：不到 1 個月", {
  x: 1, y: 4.4, w: 8, h: 0.5,
  fontSize: 14, color: colors.darkText, italic: true
});

// 17. 其他優勢
slide = pres.addSlide();
slide.background = { color: colors.white };
slide.addText("除了成本，還有什麼優勢？", {
  x: 0.5, y: 0.3, w: 9, h: 0.6,
  fontSize: 40, bold: true, color: colors.darkBlue,
  align: "left"
});
slide.addShape(pres.ShapeType.rect, {
  x: 0.5, y: 1.1, w: 9, h: 0.08,
  fill: { color: colors.accent }, line: { type: "none" }
});

const advantages = [
  { icon: "⚡", title: "時間優勢", desc: "快 3-4 倍，上市時間加速" },
  { icon: "✅", title: "品質優勢", desc: "出錯率從 10-15% 降到 1-2%" },
  { icon: "🎯", title: "一致性優勢", desc: "決策標準統一，減少內部衝突" },
  { icon: "📈", title: "可擴展性", desc: "成本幾乎不增，輕鬆擴展規模" }
];

advantages.forEach((adv, idx) => {
  const col = idx % 2;
  const row = Math.floor(idx / 2);
  const xPos = 0.6 + (col * 4.6);
  const yPos = 1.5 + (row * 2);
  
  slide.addShape(pres.ShapeType.rect, {
    x: xPos, y: yPos, w: 4.3, h: 1.8,
    fill: { color: colors.white },
    line: { color: colors.iceBlue, width: 2 }
  });
  
  slide.addText(adv.icon, {
    x: xPos + 0.15, y: yPos + 0.1, w: 0.6, h: 0.5,
    fontSize: 28, color: colors.accent
  });
  
  slide.addText(adv.title, {
    x: xPos + 0.9, y: yPos + 0.15, w: 3.2, h: 0.35,
    fontSize: 14, bold: true, color: colors.darkBlue
  });
  
  slide.addText(adv.desc, {
    x: xPos + 0.9, y: yPos + 0.55, w: 3.2, h: 1.1,
    fontSize: 11, color: colors.darkText
  });
});

// 18. 三個月導入計畫
slide = pres.addSlide();
slide.background = { color: colors.white };
slide.addText("三個月導入路線圖", {
  x: 0.5, y: 0.3, w: 9, h: 0.6,
  fontSize: 40, bold: true, color: colors.darkBlue,
  align: "left"
});
slide.addShape(pres.ShapeType.rect, {
  x: 0.5, y: 1.1, w: 9, h: 0.08,
  fill: { color: colors.accent }, line: { type: "none" }
});

const months = [
  { month: "第一個月", phase: "試驗", desc: "選定最簡單的流程，試驗 2-3 個週期" },
  { month: "第二個月", phase: "擴展", desc: "擴展到第二、第三個工作流程" },
  { month: "第三個月", phase: "規模化", desc: "將 Agent 組織應用到四個核心流程" }
];

months.forEach((item, idx) => {
  const yPos = 1.6 + (idx * 1.8);
  
  slide.addShape(pres.ShapeType.rect, {
    x: 0.7, y: yPos, w: 8.6, h: 1.5,
    fill: { color: colors.iceBlue },
    line: { color: colors.darkBlue, width: 2 }
  });
  
  slide.addText(item.month, {
    x: 1, y: yPos + 0.1, w: 2.5, h: 0.35,
    fontSize: 14, bold: true, color: colors.darkBlue
  });
  
  slide.addText(item.phase, {
    x: 3.8, y: yPos + 0.1, w: 1.5, h: 0.35,
    fontSize: 13, bold: true, color: colors.accent
  });
  
  slide.addText(item.desc, {
    x: 1, y: yPos + 0.55, w: 8, h: 0.85,
    fontSize: 12, color: colors.darkText
  });
});

// 19. 總結
slide = pres.addSlide();
slide.background = { color: colors.darkBlue };
slide.addText("課程總結", {
  x: 0.5, y: 1.2, w: 9, h: 0.8,
  fontSize: 48, bold: true, color: colors.iceBlue,
  align: "left"
});

const summary = [
  "✓ Agent 組織解決企業三大痛點",
  "✓ 12 位虛擬員工的協作模式已成熟",
  "✓ 自動化流程降低人工干預",
  "✓ 投資回本期不到 1 個月",
  "✓ 三個月導入計畫清晰可行"
];

summary.forEach((item, idx) => {
  slide.addText(item, {
    x: 1, y: 2.3 + (idx * 0.6), w: 8.5, h: 0.5,
    fontSize: 16, color: colors.white
  });
});

slide.addText("下一步：與我們討論你的具體場景", {
  x: 0.5, y: 5.5, w: 9, h: 0.6,
  fontSize: 18, bold: true, color: colors.iceBlue, italic: true,
  align: "center"
});

// ========== 保存檔案 ==========

pres.save({ fileName: "AI虛擬組織課程.pptx" });
console.log("✅ PPT 已成功生成：AI虛擬組織課程.pptx");
