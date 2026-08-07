# 引力专项达人档案 · 复用模板

把「引力专项」KV 主视觉 + 达人引入档案内容，合成为一张**蓝紫科技风竖版长图**。
纯编码实现（Pillow + HTML/CSS + 无头 Chromium 截图），**无 AI 生图**，内容可精确修改、秒级重出。

---

## 目录结构

```
引力专项档案模板/
├── README.md              ← 本说明
├── build_kv_head.py       ← ① 合成头图：贴圆头像 + 写达人名/赛道/人设
├── template.html          ← ② 长图模板：换达人只改文件顶部 DATA 对象
├── shot.js                ← ③ 截图脚本：把 template.html 渲成长图 PNG
└── assets/
    ├── kv_clean_base.png  ← KV 干净底图（已抹除原达人信息，941x1672）
    └── kv_original.png    ← KV 原始底图（备份参考）
```

---

## 换一个新达人，三步出图

### Step 1 — 生成头图（贴头像 + 名字/赛道/人设）

```bash
cd 引力专项档案模板
python3 build_kv_head.py \
  --avatar /path/达人头像.png \
  --name "@达人名" \
  --track "时尚 · 服饰穿搭赛道" \
  --persona "一句话人设" \
  --out kv_head.png
```
> 头像任意尺寸都行，脚本自动居中裁圆。输出 `kv_head.png`（头部：logo+引力专项标题+星系头像+名字赛道人设）。

### Step 2 — 填内容

复制一份模板改数据：
```bash
cp template.html 引力专项档案·某达人.html
```
打开该 HTML，**只改顶部 `const DATA = {...}`**：chips（赛道标签）、四个 section 的数据、引入结论、footer。
富文本支持：`<b>加粗</b>`、`<span class="rn">蓝色数字</span>`。数据块 `dk:true` = 深蓝、缺省 = 亮蓝（用于突出亮点）。

> ⚠️ `kv_head.png` 需和 HTML 放同一目录（HTML 里 `<img src="kv_head.png">`）。

### Step 3 — 截图出长图

```bash
xvfb-run -a node shot.js 引力专项档案·某达人.html 引力专项档案·某达人.png
```

---

## 环境依赖（首次准备）

- **中文矢量字体**（清晰关键）：思源黑体，装在 `/root/.fonts/`（`NotoSansSC-*.otf`）。
- **playwright-core + chromium**：
  ```bash
  cd /tmp && npm install playwright-core@1.48.0
  PLAYWRIGHT_DOWNLOAD_HOST=https://cdn.npmmirror.com/binaries/playwright \
    npx -y playwright@1.48.0 install chromium
  ```
  chromium 路径默认 `/opt/playwright/chromium-1234/chrome-linux64/chrome`，可用环境变量 `CHROME_PATH` 覆盖。

---

## 换 KV 底图（可选）

若日后 KV 主视觉更新：把新版海报去掉达人信息后存为 `assets/kv_clean_base.png`，
并在 `build_kv_head.py` 的 `LAYOUT` 里同步头像圆心/名字坐标即可。
（抹字方法：用 Pillow 按行取背景色填充名字区、按列取框顶色填充数据框数字区。）

---

## 设计规范速记（蓝紫科技风）

| 角色 | 色值 |
|---|---|
| 深蓝主色/标题 | `#1e3a84` |
| 亮蓝（亮点数字/引导词） | `#2f6cf0` |
| 紫（序号渐变起点） | `#6c62e9` |
| 短板警示（▲） | `#d98324` |
| 结论带高亮 | `#7fd0ff` |
| 卡片 | 白 72% 透明玻璃拟态 + 蓝边 |
