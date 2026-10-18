"""README 首页的 SVG 横幅与导航卡片（由 build_sources.py 随数据一起生成）。

GitHub 的 Markdown 不支持自定义 CSS，所以首页的视觉部分做成 SVG 图片：
深墨蓝底 + 金色点缀，在 GitHub 浅色与深色主题下都清晰可读。
SVG 作为 <img> 渲染时无法加载网络字体，因此只用系统字体栈。
"""
from __future__ import annotations

from collections import Counter
from pathlib import Path
from xml.sax.saxutils import escape

INK = "#13263A"
GOLD = "#E3A93B"
PAPER = "#F4F1E8"
MUTED = "#A9B6C2"
SANS = "'PingFang SC','Hiragino Sans GB','Microsoft YaHei','Noto Sans CJK SC','Source Han Sans SC',sans-serif"
MONO = "'SFMono-Regular',Consolas,'Liberation Mono',Menlo,monospace"

ASSET_DIR = Path("docs/assets")

# (文件名, 链接目标, 标题, 副标题模板)；副标题里的 {regions} {disciplines} 由统计数字填充
TILES = [
    ("tile-catalog.svg", "SOURCES.md", "信源总目录", "按类型浏览全部 {total} 条信源"),
    ("tile-regions.svg", "SOURCES.md#按国家--地区", "按国家 / 地区", "{regions} 个国家与地区"),
    ("tile-disciplines.svg", "SOURCES.md#按学科", "按学科", "{disciplines} 个学科方向"),
    ("tile-jobs.svg", "data/jobs.md", "今日新岗位", "每天从十余个职位库抓取"),
    ("tile-faculty.svg", "reports/discovery.md", "在招导师", "导师主页 · Bluesky · 招生表"),
    ("tile-guide.svg", "docs/guide-cn.md", "申请指南", "资助模式 · 时间线 · CSC 与签证"),
]


def _fmt(n: int) -> str:
    return f"{n:,}"


def banner_svg(st: dict) -> str:
    total = st["total"]
    regions: Counter = st["regions"]
    postdoc = st["levels"].get("postdoc", 0) + st["levels"].get("both", 0)
    figures = [
        (_fmt(total), "带资助信源"),
        (_fmt(len(regions)), "国家与地区"),
        (_fmt(st["eligible"].get("yes", 0)), "大陆生明确可申"),
        (_fmt(postdoc), "含博士后机会"),
    ]
    w, h = 1280, 420
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" '
        f'aria-label="海外带奖博士/博士后信源库：{total} 条信源，覆盖 {len(regions)} 个国家与地区">',
        f'<defs><clipPath id="card"><rect width="{w}" height="{h}" rx="20"/></clipPath></defs>',
        f'<rect width="{w}" height="{h}" rx="20" fill="{INK}"/>',
        # 右上角的“印章”同心圆
        f'<g fill="none" stroke="{GOLD}" clip-path="url(#card)"><circle cx="1150" cy="70" r="150" stroke-opacity=".32"/>'
        f'<circle cx="1150" cy="70" r="118" stroke-opacity=".24" stroke-dasharray="2 7"/>'
        f'<circle cx="1150" cy="70" r="86" stroke-opacity=".18"/></g>',
        f'<text x="56" y="78" font-family="{MONO}" font-size="16" letter-spacing="3" fill="{GOLD}">FUNDED PHD · POSTDOC · 每日更新</text>',
        f'<text x="56" y="140" font-family="{SANS}" font-size="54" font-weight="900" fill="{PAPER}">海外带奖博士 / 博士后信源库</text>',
        f'<text x="56" y="184" font-family="{SANS}" font-size="20" fill="#C9D3DC">为中国学生收集国外有奖学金或带薪资助的博士与博后机会——'
        f'聚合平台、各国门户、奖学金、导师主页与招生帖</text>',
    ]
    col = (w - 112) / 4
    for i, (value, label) in enumerate(figures):
        x = 56 + i * col
        parts += [
            f'<line x1="{x:.0f}" y1="226" x2="{x + col - 24:.0f}" y2="226" stroke="{PAPER}" stroke-opacity=".18"/>',
            f'<text x="{x:.0f}" y="280" font-family="{MONO}" font-size="44" font-weight="600" fill="#FFFFFF">{escape(value)}</text>',
            f'<text x="{x:.0f}" y="310" font-family="{SANS}" font-size="18" fill="{MUTED}">{escape(label)}</text>',
        ]
    # 底部“航班牌”：信源最多的地区
    parts.append(f'<line x1="56" y1="350" x2="{w - 56}" y2="350" stroke="{PAPER}" stroke-opacity=".12"/>')
    x = 56
    for code, n in regions.most_common(14):
        if code == "GLOBAL":
            continue
        item_w = (len(code) + len(str(n)) + 1) * 9.6 + 26
        if x + item_w > w - 56:
            break
        parts.append(f'<text x="{x:.0f}" y="384" font-family="{MONO}" font-size="16">'
                     f'<tspan fill="{GOLD}" font-weight="600">{escape(code)}</tspan><tspan fill="#8FA0AF"> {n}</tspan></text>')
        x += item_w
    parts.append("</svg>")
    return "\n".join(parts) + "\n"


def tile_svg(no: int, title: str, sub: str) -> str:
    w, h = 400, 132
    return "\n".join([
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="{escape(title)}：{escape(sub)}">',
        f'<rect width="{w}" height="{h}" rx="14" fill="{INK}"/>',
        f'<text x="24" y="36" font-family="{MONO}" font-size="15" fill="{GOLD}">{no:02d}</text>',
        f'<path d="M{w - 44} 31h16m-6-6 6 6-6 6" fill="none" stroke="{GOLD}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>',
        f'<text x="24" y="80" font-family="{SANS}" font-size="27" font-weight="700" fill="{PAPER}">{escape(title)}</text>',
        f'<text x="24" y="110" font-family="{SANS}" font-size="17" fill="{MUTED}">{escape(sub)}</text>',
        "</svg>",
    ]) + "\n"


def render_assets(st: dict) -> dict[Path, str]:
    fill = {"total": _fmt(st["total"]), "regions": len(st["regions"]), "disciplines": len(st["disciplines"])}
    out = {ASSET_DIR / "banner.svg": banner_svg(st)}
    for i, (name, _, title, sub) in enumerate(TILES, start=1):
        out[ASSET_DIR / name] = tile_svg(i, title, sub.format(**fill))
    return out


def readme_nav() -> str:
    """README 中的导航卡片（三列两行，每张卡片是一个链接）。"""
    imgs = [f'<a href="{href}"><img src="{ASSET_DIR / name}" width="32%" alt="{title}"></a>'
            for name, href, title, _ in TILES]
    return "<p align=\"center\">\n" + "\n".join(imgs[:3]) + "\n<br>\n" + "\n".join(imgs[3:]) + "\n</p>"
