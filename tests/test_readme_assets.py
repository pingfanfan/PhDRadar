"""首页 SVG 生成的离线测试：必须是合法 XML，且包含最新统计数字。"""
import sys
import xml.etree.ElementTree as ET
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
from readme_assets import TILES, readme_nav, render_assets  # noqa: E402


def test_assets_are_valid_svg_with_stats():
    st = {"total": 4763, "regions": Counter({"US": 834, "UK": 825, "GLOBAL": 298}),
          "disciplines": Counter({"cs": 1}), "levels": Counter({"phd": 3, "postdoc": 2, "both": 1}),
          "eligible": Counter({"yes": 12})}
    out = render_assets(st)
    assert len(out) == 1 + len(TILES)
    for svg in out.values():
        ET.fromstring(svg)
    banner = out[Path("docs/assets/banner.svg")]
    assert "4,763" in banner and ">US<" in banner and ">GLOBAL<" not in banner
    assert all(f'src="docs/assets/{name}"' in readme_nav() for name, *_ in TILES)
