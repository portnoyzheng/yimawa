from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED
from xml.sax.saxutils import escape

OUT = Path("/Users/kuo-weicheng/Documents/mycodex/daai_hard_science_story.pptx")
W, H = 12192000, 6858000

slides = [
    ("我曾經燒掉考卷", "鄭國威｜泛科學共同創辦人\n大愛人文講堂", "cover"),
    ("15 歲的我，正在燒考卷", "我站在旁邊，看著那個瞬間發生。\n不是青春叛逆，是信任斷線。", "dark"),
    ("那不是浪漫畫面", "那是一個人對數學、科學、學習，\n以及被評量的人生失去信任。", "dark"),
    ("我以為自己討厭知識", "後來才知道，我討厭的是\n只能用單一標準證明自己的系統。", "dark"),
    ("第一個問題", "人為什麼會討厭學習？", "chapter"),
    ("我不是不會學", "我是不知道，為什麼要學。", "light"),
    ("知識被切碎後", "就會失去意義。\n剩下答案、分數、排名，沒有世界。", "light"),
    ("科學素養不是背答案", "知道很多答案，仍可能不知道\n如何面對一件不確定的事。", "light"),
    ("科學素養是面對未知的方法", "先問問題，再看證據。\n再允許自己修正。", "light"),
    ("轉折", "世界開始露出裂縫。", "chapter2"),
    ("我的非正規教材", "動漫、遊戲、科幻、網路、科技新聞、社會議題。\n它們沒有考我，卻開始逼我提問。", "aqua"),
    ("原來知識可以破解世界", "不是課本突然變可愛。\n是我發現它能解釋事情怎麼運作。", "aqua"),
    ("好奇不是天賦", "好奇是被問題點燃。\n一個好問題，比標準答案更有價值。", "aqua"),
    ("從理解世界", "到想把世界講清楚。", "chapter3"),
    ("泛科學的開始", "全台最大科學社群之一。\nYouTube、網站、社群、活動，都是不同入口。", "white"),
    ("科學傳播不是把知識講簡單", "真正困難的是：\n不背叛知識，又讓人願意靠近。", "white"),
    ("科學傳播是在找入口", "把專業知識翻譯成一般人\n已經在乎、願意進入的問題。", "white"),
    ("技巧一：從衝突開始", "不要從名詞開始。\n先讓觀眾看見：這裡有矛盾。", "white"),
    ("技巧二：從觀眾在乎的事開始", "健康、AI、食安、能源、演算法。\n入口通常在生活，不在術語。", "white"),
    ("技巧三：比喻是臨時鷹架", "好比喻不是裝飾。\n它只是幫人先站上去，看見結構。", "white"),
    ("技巧四：幽默降低摩擦", "幽默不是稀釋知識。\n它只是讓人願意多停留一分鐘。", "white"),
    ("技巧五：保留不確定性", "科學傳播不能只追求有趣。\n也要讓限制、誤差、例外有位置。", "white"),
    ("AI 時代", "知識更便宜，判斷更昂貴。", "chapter4"),
    ("現代人每天都在做測驗", "不是考卷，是資訊流。\n健康建議、投資話術、AI 生成內容、社群怒氣。", "signal"),
    ("你怎麼知道這是真的？", "證據在哪裡？誰說的？怎麼知道的？\n有沒有反例？能不能被推翻？", "signal"),
    ("我是不是只是在找", "自己想相信的東西？", "signal"),
    ("懷疑不是否定一切", "懷疑是給證據一個上場的機會。", "signal"),
    ("回到 15 歲那個房間", "那個人手上還拿著考卷。\n火已經點起來了。", "chapter5"),
    ("我不會阻止他", "我不會說：不要放棄。\n我大概也不會急著安慰他。", "light"),
    ("我只會問他一個問題", "你真正討厭的是知識，\n還是那個只准你用分數理解自己的世界？", "light"),
    ("科學素養不是把人變成科學家", "它讓人不那麼容易被答案馴服。", "light"),
    ("好的學習", "不是讓人更會考試。\n是讓人重新取得提問的權利。", "light"),
]

styles = {
    "cover": ("07285A", "FFFFFF", "0A5FB4"),
    "dark": ("0B1726", "F8FBFF", "1D4ED8"),
    "chapter": ("0A4F9E", "FFFFFF", "FFFFFF"),
    "chapter2": ("00A7C4", "FFFFFF", "FFFFFF"),
    "chapter3": ("0069C9", "FFFFFF", "FFFFFF"),
    "chapter4": ("061B33", "FFFFFF", "18A0D8"),
    "chapter5": ("0A4F9E", "FFFFFF", "FFFFFF"),
    "light": ("F8FBFF", "102033", "0A4F9E"),
    "aqua": ("EFF7FF", "102033", "00A7C4"),
    "white": ("FFFFFF", "102033", "0069C9"),
    "signal": ("061B33", "FFFFFF", "18A0D8"),
}

def tx(text, font_size, color, bold=True, x=850000, y=850000, w=9800000, h=1500000, name="title"):
    runs = []
    for idx, line in enumerate(text.split("\n")):
        br = "" if idx == len(text.split("\n")) - 1 else "<a:br/>"
        runs.append(
            f'<a:r><a:rPr lang="zh-TW" sz="{font_size*100}" b="{1 if bold else 0}">'
            f'<a:solidFill><a:srgbClr val="{color}"/></a:solidFill>'
            f'<a:latin typeface="Noto Sans TC"/><a:ea typeface="Noto Sans TC"/></a:rPr>'
            f'<a:t>{escape(line)}</a:t></a:r>{br}'
        )
    body = "".join(runs)
    return f'''<p:sp><p:nvSpPr><p:cNvPr id="{abs(hash((text,x,y)))%100000+10}" name="{name}"/><p:cNvSpPr txBox="1"/><p:nvPr/></p:nvSpPr><p:spPr><a:xfrm><a:off x="{x}" y="{y}"/><a:ext cx="{w}" cy="{h}"/></a:xfrm><a:prstGeom prst="rect"><a:avLst/></a:prstGeom><a:noFill/><a:ln><a:noFill/></a:ln></p:spPr><p:txBody><a:bodyPr wrap="square"/><a:lstStyle/><a:p>{body}</a:p></p:txBody></p:sp>'''

def rect(idn, x, y, w, h, color, alpha=None):
    alpha_xml = f'<a:alpha val="{int(alpha*100000)}"/>' if alpha is not None else ""
    return f'''<p:sp><p:nvSpPr><p:cNvPr id="{idn}" name="shape{idn}"/><p:cNvSpPr/><p:nvPr/></p:nvSpPr><p:spPr><a:xfrm><a:off x="{x}" y="{y}"/><a:ext cx="{w}" cy="{h}"/></a:xfrm><a:prstGeom prst="rect"><a:avLst/></a:prstGeom><a:solidFill><a:srgbClr val="{color}">{alpha_xml}</a:srgbClr></a:solidFill><a:ln><a:noFill/></a:ln></p:spPr><p:txBody><a:bodyPr/><a:lstStyle/><a:p/></p:txBody></p:sp>'''

def slide_xml(i, title, body, style):
    bg, fg, accent = styles[style]
    title_size = 54 if style in {"cover", "dark"} or i == 32 else 46
    body_size = 25 if style in {"cover", "dark"} or i == 32 else 23
    shapes = [
        rect(2, 0, 0, W, H, bg),
        rect(3, 0, 5900000, W, 958000, "EAF3FF", 0.35),
        rect(4, 520000, 520000, 140000, 4760000, accent),
        rect(5, 880000, 2320000, 2100000, 38000, accent),
        tx(title, title_size, fg, True, 860000, 880000, 9500000, 1500000, "title"),
        tx(body, body_size, fg, False, 880000, 2800000, 9300000, 1900000, "body"),
        tx(f"{i:02d}/32", 12, accent, True, 10700000, 520000, 900000, 300000, "num"),
    ]
    if style.startswith("chapter"):
        shapes.append(rect(9, 0, 0, W, H, bg, 0.18))
    return f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?><p:sld xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main"><p:cSld><p:spTree><p:nvGrpSpPr><p:cNvPr id="1" name=""/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr><p:grpSpPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="0" cy="0"/><a:chOff x="0" y="0"/><a:chExt cx="0" cy="0"/></a:xfrm></p:grpSpPr>{''.join(shapes)}</p:spTree></p:cSld><p:clrMapOvr><a:masterClrMapping/></p:clrMapOvr></p:sld>'''

def write(path, data):
    z.writestr(path, data)

content_types = ['''<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="xml" ContentType="application/xml"/><Override PartName="/ppt/presentation.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.presentation.main+xml"/><Override PartName="/ppt/slideMasters/slideMaster1.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.slideMaster+xml"/><Override PartName="/ppt/slideLayouts/slideLayout1.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.slideLayout+xml"/><Override PartName="/ppt/theme/theme1.xml" ContentType="application/vnd.openxmlformats-officedocument.theme+xml"/>''']
for i in range(1, 33):
    content_types.append(f'<Override PartName="/ppt/slides/slide{i}.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.slide+xml"/>')
content_types.append("</Types>")

with ZipFile(OUT, "w", ZIP_DEFLATED) as z:
    write("[Content_Types].xml", "".join(content_types))
    write("_rels/.rels", '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="ppt/presentation.xml"/></Relationships>''')
    sld_ids = "".join([f'<p:sldId id="{255+i}" r:id="rId{i}"/>' for i in range(1, 33)])
    write("ppt/presentation.xml", f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?><p:presentation xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main"><p:sldMasterIdLst><p:sldMasterId id="2147483648" r:id="rId33"/></p:sldMasterIdLst><p:sldIdLst>{sld_ids}</p:sldIdLst><p:sldSz cx="{W}" cy="{H}" type="wide"/><p:notesSz cx="6858000" cy="9144000"/></p:presentation>''')
    rels = [f'<Relationship Id="rId{i}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slide" Target="slides/slide{i}.xml"/>' for i in range(1, 33)]
    rels.append('<Relationship Id="rId33" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideMaster" Target="slideMasters/slideMaster1.xml"/>')
    write("ppt/_rels/presentation.xml.rels", f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">{''.join(rels)}</Relationships>''')
    write("ppt/slideMasters/slideMaster1.xml", '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?><p:sldMaster xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main"><p:cSld><p:spTree><p:nvGrpSpPr><p:cNvPr id="1" name=""/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr><p:grpSpPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="0" cy="0"/><a:chOff x="0" y="0"/><a:chExt cx="0" cy="0"/></a:xfrm></p:grpSpPr></p:spTree></p:cSld><p:clrMap bg1="lt1" tx1="dk1" bg2="lt2" tx2="dk2" accent1="accent1" accent2="accent2" accent3="accent3" accent4="accent4" accent5="accent5" accent6="accent6" hlink="hlink" folHlink="folHlink"/><p:sldLayoutIdLst><p:sldLayoutId id="2147483649" r:id="rId1"/></p:sldLayoutIdLst><p:txStyles><p:titleStyle/><p:bodyStyle/><p:otherStyle/></p:txStyles></p:sldMaster>''')
    write("ppt/slideMasters/_rels/slideMaster1.xml.rels", '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideLayout" Target="../slideLayouts/slideLayout1.xml"/><Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/theme" Target="../theme/theme1.xml"/></Relationships>''')
    write("ppt/slideLayouts/slideLayout1.xml", '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?><p:sldLayout xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main" type="blank" preserve="1"><p:cSld name="Blank"><p:spTree><p:nvGrpSpPr><p:cNvPr id="1" name=""/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr><p:grpSpPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="0" cy="0"/><a:chOff x="0" y="0"/><a:chExt cx="0" cy="0"/></a:xfrm></p:grpSpPr></p:spTree></p:cSld><p:clrMapOvr><a:masterClrMapping/></p:clrMapOvr></p:sldLayout>''')
    write("ppt/slideLayouts/_rels/slideLayout1.xml.rels", '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideMaster" Target="../slideMasters/slideMaster1.xml"/></Relationships>''')
    write("ppt/theme/theme1.xml", '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?><a:theme xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" name="PanSci Blue"><a:themeElements><a:clrScheme name="PanSci"><a:dk1><a:srgbClr val="102033"/></a:dk1><a:lt1><a:srgbClr val="FFFFFF"/></a:lt1><a:dk2><a:srgbClr val="061B33"/></a:dk2><a:lt2><a:srgbClr val="F8FBFF"/></a:lt2><a:accent1><a:srgbClr val="0A5FB4"/></a:accent1><a:accent2><a:srgbClr val="18A0D8"/></a:accent2><a:accent3><a:srgbClr val="00A7C4"/></a:accent3><a:accent4><a:srgbClr val="0A4F9E"/></a:accent4><a:accent5><a:srgbClr val="1D4ED8"/></a:accent5><a:accent6><a:srgbClr val="EAF3FF"/></a:accent6><a:hlink><a:srgbClr val="0069C9"/></a:hlink><a:folHlink><a:srgbClr val="0069C9"/></a:folHlink></a:clrScheme><a:fontScheme name="Noto"><a:majorFont><a:latin typeface="Noto Sans TC"/><a:ea typeface="Noto Sans TC"/></a:majorFont><a:minorFont><a:latin typeface="Noto Sans TC"/><a:ea typeface="Noto Sans TC"/></a:minorFont></a:fontScheme><a:fmtScheme name="clean"><a:fillStyleLst/><a:lnStyleLst/><a:effectStyleLst/><a:bgFillStyleLst/></a:fmtScheme></a:themeElements></a:theme>''')
    for i, (title, body, style) in enumerate(slides, 1):
        write(f"ppt/slides/slide{i}.xml", slide_xml(i, title, body, style))
        write(f"ppt/slides/_rels/slide{i}.xml.rels", '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideLayout" Target="../slideLayouts/slideLayout1.xml"/></Relationships>''')

print(OUT)
