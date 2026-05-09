from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED
from xml.sax.saxutils import escape

OUT = Path("/Users/kuo-weicheng/Documents/mycodex/daai_center_focus_story.pptx")
W, H = 12192000, 6858000

slides = [
    ("15 歲，\n我燒掉考卷", "一小團火", "fire"),
    ("我以為自己\n討厭知識", "其實我討厭的是判決", "dark"),
    ("成績是測量，\n不是身分證", "測量結果不該變成人的身分", "measure"),
    ("真正的轉折，\n在研究所", "社會現場逼我重新面對知識", "turn"),
    ("站隊很快，\n理解很慢", "情緒很滿，證據很薄", "warning"),
    ("學習型態翻轉", "從被判分，到提出問題", "light"),
    ("我重新拾回\n學習動力", "問題變多，世界反而打開", "light"),
    ("科學素養：\n面對未知的方法", "不是背答案，是處理不確定", "science"),
    ("科學的脾氣：\n晚一點下結論", "先觀察，再推論，再修正", "science"),
    ("從理解世界，\n到把世界講清楚", "科學傳播，是把問題變成入口", "bridge"),
    ("知識有不同速度", "長文、短片、社群、活動，各有任務", "media"),
    ("15 分鐘，\n抓住大脈絡", "先讓觀眾知道自己正在看什麼", "media"),
    ("3 分鐘，\n掌握新研究", "快速不等於草率", "media"),
    ("慢下來，\n也是一種科學態度", "讓資訊沉澱成判斷", "slow"),
    ("內容格式，\n其實是理解工具", "形式不是包裝，是認知路徑", "tool"),
    ("比喻是鷹架", "站穩之後，鷹架就該拆掉", "bridge"),
    ("故事是船，\n證據是龍骨", "沒有證據，故事會漏水", "evidence"),
    ("幽默降低摩擦", "讓人靠近，不讓知識變形", "humor"),
    ("承認不知道，\n是判斷力的開始", "流暢不等於正確", "ai"),
    ("重新取得\n提問的權利", "你可以從粗糙的問題開始", "question"),
    ("回到那個房間", "你對自己的判決，證據不足", "fire"),
    ("回到那場火", "燒掉考卷的火，後來變成我追問世界的火", "final"),
]

themes = {
    "fire": ("07111F", "F8FBFF", "FF7A1A"),
    "dark": ("0B1726", "F8FBFF", "1D4ED8"),
    "measure": ("F8FBFF", "0F2133", "0A5FB4"),
    "turn": ("0A4F9E", "FFFFFF", "9BE8FF"),
    "warning": ("061B33", "FFFFFF", "FFB020"),
    "light": ("F8FBFF", "0F2133", "0A5FB4"),
    "science": ("FFFFFF", "0F2133", "00A7C4"),
    "bridge": ("EFF7FF", "0F2133", "0069C9"),
    "media": ("FFFFFF", "0F2133", "1D4ED8"),
    "slow": ("061B33", "FFFFFF", "18A0D8"),
    "tool": ("F8FBFF", "0F2133", "00A7C4"),
    "evidence": ("061B33", "FFFFFF", "18A0D8"),
    "humor": ("FFFFFF", "0F2133", "0A5FB4"),
    "ai": ("061B33", "FFFFFF", "18A0D8"),
    "question": ("F8FBFF", "0F2133", "0A5FB4"),
    "final": ("0A4F9E", "FFFFFF", "FFFFFF"),
}


def rect(idn, x, y, w, h, color, alpha=None):
    alpha_xml = f'<a:alpha val="{int(alpha*100000)}"/>' if alpha is not None else ""
    return f'''<p:sp><p:nvSpPr><p:cNvPr id="{idn}" name="shape{idn}"/><p:cNvSpPr/><p:nvPr/></p:nvSpPr><p:spPr><a:xfrm><a:off x="{x}" y="{y}"/><a:ext cx="{w}" cy="{h}"/></a:xfrm><a:prstGeom prst="rect"><a:avLst/></a:prstGeom><a:solidFill><a:srgbClr val="{color}">{alpha_xml}</a:srgbClr></a:solidFill><a:ln><a:noFill/></a:ln></p:spPr><p:txBody><a:bodyPr/><a:lstStyle/><a:p/></p:txBody></p:sp>'''


def ellipse(idn, x, y, w, h, color, alpha=1):
    alpha_xml = f'<a:alpha val="{int(alpha*100000)}"/>'
    return f'''<p:sp><p:nvSpPr><p:cNvPr id="{idn}" name="focus{idn}"/><p:cNvSpPr/><p:nvPr/></p:nvSpPr><p:spPr><a:xfrm><a:off x="{x}" y="{y}"/><a:ext cx="{w}" cy="{h}"/></a:xfrm><a:prstGeom prst="ellipse"><a:avLst/></a:prstGeom><a:solidFill><a:srgbClr val="{color}">{alpha_xml}</a:srgbClr></a:solidFill><a:ln><a:noFill/></a:ln></p:spPr><p:txBody><a:bodyPr/><a:lstStyle/><a:p/></p:txBody></p:sp>'''


def text_box(text, size, color, bold, x, y, w, h, align="ctr", name="text"):
    parts = text.split("\n")
    runs = []
    for idx, line in enumerate(parts):
        br = "" if idx == len(parts) - 1 else "<a:br/>"
        runs.append(
            f'<a:r><a:rPr lang="zh-TW" sz="{size*100}" b="{1 if bold else 0}">'
            f'<a:solidFill><a:srgbClr val="{color}"/></a:solidFill>'
            f'<a:latin typeface="Noto Sans TC"/><a:ea typeface="Noto Sans TC"/></a:rPr>'
            f'<a:t>{escape(line)}</a:t></a:r>{br}'
        )
    return f'''<p:sp><p:nvSpPr><p:cNvPr id="{abs(hash((text,x,y)))%100000+20}" name="{name}"/><p:cNvSpPr txBox="1"/><p:nvPr/></p:nvSpPr><p:spPr><a:xfrm><a:off x="{x}" y="{y}"/><a:ext cx="{w}" cy="{h}"/></a:xfrm><a:prstGeom prst="rect"><a:avLst/></a:prstGeom><a:noFill/><a:ln><a:noFill/></a:ln></p:spPr><p:txBody><a:bodyPr wrap="square" anchor="mid"/><a:lstStyle/><a:p><a:pPr algn="{align}"/>{''.join(runs)}</a:p></p:txBody></p:sp>'''


def symbol(kind, accent, fg):
    cx, cy = W // 2, 3140000
    # Keep geometry outside the main reading zone; the previous central mark
    # competed with the title text after import into Google Slides.
    shapes = [
        ellipse(6, -1150000, -1050000, 3000000, 3000000, accent, 0.06),
        ellipse(7, W - 1850000, H - 1950000, 2700000, 2700000, accent, 0.07),
    ]
    if kind in {"fire", "final"}:
        shapes += [
            ellipse(8, 5600000, 850000, 520000, 520000, accent, 0.95),
            ellipse(9, 5450000, 1180000, 820000, 820000, accent, 0.22),
        ]
    elif kind in {"science", "ai", "evidence"}:
        shapes += [
            rect(8, 5050000, 1040000, 2100000, 36000, accent, 0.65),
            rect(9, 6080000, 620000, 36000, 860000, accent, 0.65),
            ellipse(10, 5930000, 900000, 330000, 330000, accent, 0.9),
        ]
    elif kind in {"bridge", "media", "tool"}:
        shapes += [
            rect(8, 5000000, 1060000, 2200000, 180000, accent, 0.45),
            rect(9, 5450000, 760000, 1300000, 780000, accent, 0.08),
        ]
    else:
        shapes += [
            ellipse(8, 5750000, 900000, 620000, 620000, accent, 0.16),
            ellipse(9, 5960000, 1110000, 200000, 200000, accent, 0.9),
        ]
    return shapes


def slide_xml(i, title, subtitle, mood):
    bg, fg, accent = themes[mood]
    title_y = 1850000 if "\n" in title else 2100000
    title_size = 56 if len(title.replace("\n", "")) <= 12 else 48
    shapes = [
        rect(2, 0, 0, W, H, bg),
        rect(3, 0, 5900000, W, 958000, "EAF3FF" if bg != "F8FBFF" and bg != "FFFFFF" else "DCEBFF", 0.18),
        *symbol(mood, accent, fg),
        rect(18, 1320000, 1600000, 9552000, 3000000, bg, 0.92),
        text_box(title, title_size, fg, True, 1450000, title_y, 9300000, 1550000, "ctr", "title"),
        text_box(subtitle, 22, fg, False, 2400000, 4240000, 7400000, 780000, "ctr", "subtitle"),
        text_box(f"{i:02d}/22", 12, accent, True, 10300000, 450000, 900000, 300000, "r", "num"),
    ]
    return f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?><p:sld xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main"><p:cSld><p:spTree><p:nvGrpSpPr><p:cNvPr id="1" name=""/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr><p:grpSpPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="0" cy="0"/><a:chOff x="0" y="0"/><a:chExt cx="0" cy="0"/></a:xfrm></p:grpSpPr>{''.join(shapes)}</p:spTree></p:cSld><p:clrMapOvr><a:masterClrMapping/></p:clrMapOvr></p:sld>'''


content_types = ['''<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="xml" ContentType="application/xml"/><Override PartName="/ppt/presentation.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.presentation.main+xml"/><Override PartName="/ppt/slideMasters/slideMaster1.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.slideMaster+xml"/><Override PartName="/ppt/slideLayouts/slideLayout1.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.slideLayout+xml"/><Override PartName="/ppt/theme/theme1.xml" ContentType="application/vnd.openxmlformats-officedocument.theme+xml"/>''']
for i in range(1, len(slides) + 1):
    content_types.append(f'<Override PartName="/ppt/slides/slide{i}.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.slide+xml"/>')
content_types.append("</Types>")

with ZipFile(OUT, "w", ZIP_DEFLATED) as z:
    z.writestr("[Content_Types].xml", "".join(content_types))
    z.writestr("_rels/.rels", '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="ppt/presentation.xml"/></Relationships>''')
    sld_ids = "".join([f'<p:sldId id="{255+i}" r:id="rId{i}"/>' for i in range(1, len(slides)+1)])
    z.writestr("ppt/presentation.xml", f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?><p:presentation xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main"><p:sldMasterIdLst><p:sldMasterId id="2147483648" r:id="rId{len(slides)+1}"/></p:sldMasterIdLst><p:sldIdLst>{sld_ids}</p:sldIdLst><p:sldSz cx="{W}" cy="{H}" type="wide"/><p:notesSz cx="6858000" cy="9144000"/></p:presentation>''')
    rels = [f'<Relationship Id="rId{i}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slide" Target="slides/slide{i}.xml"/>' for i in range(1, len(slides)+1)]
    rels.append(f'<Relationship Id="rId{len(slides)+1}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideMaster" Target="slideMasters/slideMaster1.xml"/>')
    z.writestr("ppt/_rels/presentation.xml.rels", f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">{''.join(rels)}</Relationships>''')
    z.writestr("ppt/slideMasters/slideMaster1.xml", '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?><p:sldMaster xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main"><p:cSld><p:spTree><p:nvGrpSpPr><p:cNvPr id="1" name=""/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr><p:grpSpPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="0" cy="0"/><a:chOff x="0" y="0"/><a:chExt cx="0" cy="0"/></a:xfrm></p:grpSpPr></p:spTree></p:cSld><p:clrMap bg1="lt1" tx1="dk1" bg2="lt2" tx2="dk2" accent1="accent1" accent2="accent2" accent3="accent3" accent4="accent4" accent5="accent5" accent6="accent6" hlink="hlink" folHlink="folHlink"/><p:sldLayoutIdLst><p:sldLayoutId id="2147483649" r:id="rId1"/></p:sldLayoutIdLst><p:txStyles><p:titleStyle/><p:bodyStyle/><p:otherStyle/></p:txStyles></p:sldMaster>''')
    z.writestr("ppt/slideMasters/_rels/slideMaster1.xml.rels", '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideLayout" Target="../slideLayouts/slideLayout1.xml"/><Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/theme" Target="../theme/theme1.xml"/></Relationships>''')
    z.writestr("ppt/slideLayouts/slideLayout1.xml", '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?><p:sldLayout xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main" type="blank" preserve="1"><p:cSld name="Blank"><p:spTree><p:nvGrpSpPr><p:cNvPr id="1" name=""/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr><p:grpSpPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="0" cy="0"/><a:chOff x="0" y="0"/><a:chExt cx="0" cy="0"/></a:xfrm></p:grpSpPr></p:spTree></p:cSld><p:clrMapOvr><a:masterClrMapping/></p:clrMapOvr></p:sldLayout>''')
    z.writestr("ppt/slideLayouts/_rels/slideLayout1.xml.rels", '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideMaster" Target="../slideMasters/slideMaster1.xml"/></Relationships>''')
    z.writestr("ppt/theme/theme1.xml", '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?><a:theme xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" name="Central Science"><a:themeElements><a:clrScheme name="Central"><a:dk1><a:srgbClr val="0F2133"/></a:dk1><a:lt1><a:srgbClr val="FFFFFF"/></a:lt1><a:dk2><a:srgbClr val="061B33"/></a:dk2><a:lt2><a:srgbClr val="F8FBFF"/></a:lt2><a:accent1><a:srgbClr val="0A5FB4"/></a:accent1><a:accent2><a:srgbClr val="18A0D8"/></a:accent2><a:accent3><a:srgbClr val="FF7A1A"/></a:accent3><a:accent4><a:srgbClr val="00A7C4"/></a:accent4><a:accent5><a:srgbClr val="1D4ED8"/></a:accent5><a:accent6><a:srgbClr val="EAF3FF"/></a:accent6><a:hlink><a:srgbClr val="0069C9"/></a:hlink><a:folHlink><a:srgbClr val="0069C9"/></a:folHlink></a:clrScheme><a:fontScheme name="Noto"><a:majorFont><a:latin typeface="Noto Sans TC"/><a:ea typeface="Noto Sans TC"/></a:majorFont><a:minorFont><a:latin typeface="Noto Sans TC"/><a:ea typeface="Noto Sans TC"/></a:minorFont></a:fontScheme><a:fmtScheme name="clean"><a:fillStyleLst/><a:lnStyleLst/><a:effectStyleLst/><a:bgFillStyleLst/></a:fmtScheme></a:themeElements></a:theme>''')
    for i, (title, subtitle, mood) in enumerate(slides, 1):
        z.writestr(f"ppt/slides/slide{i}.xml", slide_xml(i, title, subtitle, mood))
        z.writestr(f"ppt/slides/_rels/slide{i}.xml.rels", '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideLayout" Target="../slideLayouts/slideLayout1.xml"/></Relationships>''')

print(OUT)
