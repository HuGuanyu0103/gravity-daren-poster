#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
引力专项达人档案 — KV 头图合成脚本
用途：把某个达人的方形头像裁成圆形，贴进「引力专项」KV 星系光环中心，
      并写上 达人名 / 赛道 / 人设，输出头图 kv_head.png（供模板 HTML 顶部引用）。

只用 Pillow（编码手段），不涉及任何 AI 生图。
星系光效/蓝紫渐变/logo/「引力专项」立体字 全部来自真实 KV 底图 assets/kv_clean_base.png。

用法：
    python3 build_kv_head.py \
        --avatar 达人头像.png \
        --name "@Fandeee" \
        --track "时尚 · 服饰穿搭赛道" \
        --persona "抖红双栖时尚穿搭作者，主打上班族女性通勤穿搭" \
        --out kv_head.png

说明：
- KV 底图为 941x1672。头像光环中心约 (470, 832)，可放直径约 328 的圆。
- 名字行基线 y≈1210，人设行 y≈1290（相对 941 宽底图坐标）。
- 若换新的 KV 底图，请同步更新下方 LAYOUT 里的坐标。
"""
import argparse
from PIL import Image, ImageDraw, ImageFont

# ===== 布局参数（基于 941x1672 的 KV 底图，如换底图需同步调整）=====
LAYOUT = {
    "canvas": (941, 1672),
    "avatar_center": (470, 832),   # 光环圆心
    "avatar_diameter": 328,        # 头像圆直径
    "name_xy": (62, 1200),         # 名字行左上
    "track_gap": 22,               # 名字与竖线/赛道间距
    "persona_xy": (62, 1288),      # 人设行左上
    "name_color": (22, 51, 126),   # 深蓝
    "track_color": (28, 71, 160),
    "persona_color": (51, 56, 63),
    "name_size": 54,
    "track_size": 36,
    "persona_size": 26,
}

# 中文字体候选（矢量思源宋/黑，回退系统字体）
FONT_CANDIDATES = [
    "/root/.fonts/NotoSansSC-Bold.otf",
    "/root/.fonts/NotoSansSC-Regular.otf",
    "/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc",
]


def load_font(size, bold=True):
    for p in FONT_CANDIDATES:
        try:
            return ImageFont.truetype(p, size)
        except Exception:
            continue
    return ImageFont.load_default()


def circle_avatar(avatar_path, diameter):
    im = Image.open(avatar_path).convert("RGBA")
    w, h = im.size
    side = min(w, h)
    im = im.crop(((w - side) // 2, (h - side) // 2,
                  (w + side) // 2, (h + side) // 2)).resize((diameter, diameter), Image.LANCZOS)
    mask = Image.new("L", (diameter, diameter), 0)
    ImageDraw.Draw(mask).ellipse((0, 0, diameter, diameter), fill=255)
    out = Image.new("RGBA", (diameter, diameter), (0, 0, 0, 0))
    out.paste(im, (0, 0), mask)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--base", default="assets/kv_clean_base.png", help="KV 干净底图（已抹除原达人信息）")
    ap.add_argument("--avatar", required=True, help="达人头像（方图/任意，自动裁圆）")
    ap.add_argument("--name", required=True, help="达人名，如 @Fandeee")
    ap.add_argument("--track", required=True, help="赛道，如 时尚 · 服饰穿搭赛道")
    ap.add_argument("--persona", required=True, help="一句话人设")
    ap.add_argument("--out", default="kv_head.png")
    args = ap.parse_args()

    base = Image.open(args.base).convert("RGBA")
    L = LAYOUT

    # 贴圆形头像
    d = L["avatar_diameter"]
    av = circle_avatar(args.avatar, d)
    cx, cy = L["avatar_center"]
    base.alpha_composite(av, (cx - d // 2, cy - d // 2))

    draw = ImageDraw.Draw(base)
    # 名字
    fn = load_font(L["name_size"])
    nx, ny = L["name_xy"]
    draw.text((nx, ny), args.name, font=fn, fill=L["name_color"])
    nw = draw.textlength(args.name, font=fn)
    # 竖线 + 赛道
    bar_x = nx + nw + L["track_gap"]
    draw.rectangle([bar_x, ny + 4, bar_x + 3, ny + 46], fill=(125, 146, 196))
    ft = load_font(L["track_size"])
    draw.text((bar_x + L["track_gap"], ny + 6), args.track, font=ft, fill=L["track_color"])
    # 人设
    fp = load_font(L["persona_size"])
    draw.text(L["persona_xy"], args.persona, font=fp, fill=L["persona_color"])

    # 裁到数据框上方（y≈1360），只保留 logo→人设 的头部
    head = base.convert("RGB").crop((0, 0, L["canvas"][0], 1360))
    head.save(args.out)
    print(f"[OK] 头图已生成: {args.out}  尺寸 {head.size}")


if __name__ == "__main__":
    main()
