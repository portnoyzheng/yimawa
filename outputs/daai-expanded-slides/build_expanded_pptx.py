import html
import re
import zipfile
from pathlib import Path

BASE = Path("/Users/kuo-weicheng/Documents/mycodex/daai_center_focus_story.pptx")
SOURCE = Path("/Users/kuo-weicheng/Documents/mycodex/daai_source.pptx")
SCRIPT = Path("/private/tmp/daai_final_speech.txt")
OUT = Path("/Users/kuo-weicheng/Documents/mycodex/outputs/daai-expanded-slides/daai_expanded_prompt_slides.pptx")

NS_P = "http://schemas.openxmlformats.org/presentationml/2006/main"
NS_A = "http://schemas.openxmlformats.org/drawingml/2006/main"
NS_R = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
NS_REL = "http://schemas.openxmlformats.org/package/2006/relationships"
NS_CT = "http://schemas.openxmlformats.org/package/2006/content-types"


def parse_sections():
    text = SCRIPT.read_text(encoding="utf-8-sig")
    parts = re.split(r"^【投影片\s*(\d+)：[^】]+】\s*$", text, flags=re.M)
    sections = {}
    for i in range(1, len(parts), 2):
        n = int(parts[i])
        body = parts[i + 1]
        body = "\n".join(line for line in body.splitlines() if not re.fullmatch(r"_+", line.strip()))
        paras = [p.strip() for p in body.strip().split("\n") if p.strip()]
        sections[n] = paras
    return sections


def split_notes(sections, threshold=180):
    slides = []
    for sec, paras in sections.items():
        cur = []
        chars = 0
        for para in paras:
            if cur and chars + len(para) > threshold and (len(cur) >= 2 or chars > 80):
                slides.append((sec, cur))
                cur = []
                chars = 0
            cur.append(para)
            chars += len(para)
        if cur:
            slides.append((sec, cur))
    return slides


TITLE_OVERRIDES = [
    "先看一個畫面",
    "低成本犯罪現場",
    "我討厭讀書",
    "兩個荒謬畫面",
    "知識何時變刑具",
    "數學沒有霸凌我",
    "局部失敗變判決",
    "不在乎也是防禦",
    "成績只是測量",
    "不要用低品質證據判自己",
    "轉折在研究所",
    "站隊很快，理解很慢",
    "正義感不能被代管",
    "知識會進入生活",
    "無知保護膜",
    "學習型態翻轉",
    "思想的修羅場",
    "攻擊論證，不是人格",
    "不是為了證明好學生",
    "知識不會因討厭而消失",
    "好奇心被現實逼出來",
    "科學素養不是背答案",
    "先停一下再判斷",
    "科學的脾氣",
    "熱情需要煞車",
    "開始做科學傳播",
    "替觀眾找到入口",
    "不要從名詞開始",
    "門在哪裡",
    "知識有不同速度",
    "什麼速度適合理解",
    "15 分鐘抓大脈絡",
    "把點連成線",
    "3 分鐘掌握新研究",
    "短內容不是比較簡單",
    "科學也需要慢",
    "慢下來才能看見方法",
    "一整套理解工具箱",
    "不同知識，不同容器",
    "比喻是鷹架",
    "會講故事，也要會拆故事",
    "注意力與準確性的拉扯",
    "故事要有證據龍骨",
    "幽默降低摩擦",
    "幽默要服務理解",
    "不知道不可恥",
    "流暢不等於正確",
    "我需要查",
    "把門重新打開",
    "從粗糙問題開始",
    "科學素養的肌肉",
    "回到那場火",
    "判決，證據不足",
    "世界不附標準答案",
    "火變成追問世界的火",
    "把火留給好奇心",
]


def esc(text):
    return html.escape(text, quote=False)


def paragraph_xml(text, font_size=1500, color="111827", bold=False, align="ctr"):
    return (
        f'<a:p><a:pPr algn="{align}"><a:buNone/></a:pPr>'
        f'<a:r><a:rPr lang="zh-TW" sz="{font_size}" b="{1 if bold else 0}">'
        f'<a:solidFill><a:srgbClr val="{color}"/></a:solidFill>'
        f'<a:latin typeface="Noto Sans TC"/><a:ea typeface="Noto Sans TC"/><a:cs typeface="Noto Sans TC"/>'
        f'</a:rPr><a:t>{esc(text)}</a:t></a:r><a:endParaRPr/></a:p>'
    )


def slide_xml(idx, title, dark=False, flame=False):
    bg = "061526" if dark else ("FFFFFF" if idx % 2 else "F4F9FF")
    fg = "F8FBFF" if dark else "0F172A"
    accent = "FF7A1A" if flame else "1D4ED8"
    title_lines = title.split("，")
    if len(title_lines) == 2 and len(title) <= 14:
        rendered = title_lines
    else:
        rendered = [title]
    text_paras = "".join(paragraph_xml(line, 4100 if len(line) <= 12 else 3400, fg, True) for line in rendered)
    return f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<p:sld xmlns:a="{NS_A}" xmlns:r="{NS_R}" xmlns:p="{NS_P}">
<p:cSld><p:spTree>
<p:nvGrpSpPr><p:cNvPr id="1" name=""/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr>
<p:grpSpPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="0" cy="0"/><a:chOff x="0" y="0"/><a:chExt cx="0" cy="0"/></a:xfrm></p:grpSpPr>
<p:sp><p:nvSpPr><p:cNvPr id="2" name="bg"/><p:cNvSpPr/><p:nvPr/></p:nvSpPr>
<p:spPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="12192000" cy="6858000"/></a:xfrm><a:prstGeom prst="rect"><a:avLst/></a:prstGeom><a:solidFill><a:srgbClr val="{bg}"/></a:solidFill><a:ln><a:noFill/></a:ln></p:spPr><p:txBody><a:bodyPr/><a:lstStyle/><a:p/></p:txBody></p:sp>
<p:sp><p:nvSpPr><p:cNvPr id="3" name="accent"/><p:cNvSpPr/><p:nvPr/></p:nvSpPr>
<p:spPr><a:xfrm><a:off x="4850000" y="1220000"/><a:ext cx="2220000" cy="90000"/></a:xfrm><a:prstGeom prst="rect"><a:avLst/></a:prstGeom><a:solidFill><a:srgbClr val="{accent}"/></a:solidFill><a:ln><a:noFill/></a:ln></p:spPr><p:txBody><a:bodyPr/><a:lstStyle/><a:p/></p:txBody></p:sp>
<p:sp><p:nvSpPr><p:cNvPr id="4" name="cue"/><p:cNvSpPr txBox="1"/><p:nvPr/></p:nvSpPr>
<p:spPr><a:xfrm><a:off x="1250000" y="2050000"/><a:ext cx="9700000" cy="1850000"/></a:xfrm><a:prstGeom prst="rect"><a:avLst/></a:prstGeom><a:noFill/><a:ln><a:noFill/></a:ln></p:spPr>
<p:txBody><a:bodyPr anchor="mid" wrap="square" lIns="0" rIns="0" tIns="0" bIns="0"><a:noAutofit/></a:bodyPr><a:lstStyle/>{text_paras}</p:txBody></p:sp>
<p:sp><p:nvSpPr><p:cNvPr id="5" name="safe"/><p:cNvSpPr/><p:nvPr/></p:nvSpPr>
<p:spPr><a:xfrm><a:off x="0" y="5900000"/><a:ext cx="12192000" cy="958000"/></a:xfrm><a:prstGeom prst="rect"><a:avLst/></a:prstGeom><a:solidFill><a:srgbClr val="EAF3FF"><a:alpha val="14000"/></a:srgbClr></a:solidFill><a:ln><a:noFill/></a:ln></p:spPr><p:txBody><a:bodyPr/><a:lstStyle/><a:p/></p:txBody></p:sp>
</p:spTree></p:cSld><p:clrMapOvr><a:masterClrMapping/></p:clrMapOvr></p:sld>'''


def notes_xml(idx, note_text):
    paras = "".join(paragraph_xml(line, 1200, "000000", False, "l") for line in note_text.split("\n") if line.strip())
    return f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<p:notes xmlns:a="{NS_A}" xmlns:r="{NS_R}" xmlns:p="{NS_P}" showMasterPhAnim="0" showMasterSp="0">
<p:cSld><p:spTree>
<p:nvGrpSpPr><p:cNvPr id="1" name=""/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr>
<p:grpSpPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="0" cy="0"/><a:chOff x="0" y="0"/><a:chExt cx="0" cy="0"/></a:xfrm></p:grpSpPr>
<p:sp><p:nvSpPr><p:cNvPr id="2" name="slide image"/><p:cNvSpPr/><p:nvPr><p:ph idx="2" type="sldImg"/></p:nvPr></p:nvSpPr>
<p:spPr><a:xfrm><a:off x="685800" y="1143000"/><a:ext cx="5486400" cy="3086100"/></a:xfrm><a:prstGeom prst="rect"><a:avLst/></a:prstGeom><a:noFill/><a:ln><a:solidFill><a:srgbClr val="000000"/></a:solidFill></a:ln></p:spPr></p:sp>
<p:sp><p:nvSpPr><p:cNvPr id="3" name="notes"/><p:cNvSpPr txBox="1"/><p:nvPr><p:ph idx="1" type="body"/></p:nvPr></p:nvSpPr>
<p:spPr><a:xfrm><a:off x="685800" y="4400550"/><a:ext cx="5486400" cy="3600600"/></a:xfrm><a:prstGeom prst="rect"><a:avLst/></a:prstGeom><a:noFill/><a:ln><a:noFill/></a:ln></p:spPr>
<p:txBody><a:bodyPr wrap="square" lIns="91425" rIns="91425" tIns="45700" bIns="45700"><a:noAutofit/></a:bodyPr><a:lstStyle/>{paras}</p:txBody></p:sp>
</p:spTree></p:cSld><p:clrMapOvr><a:masterClrMapping/></p:clrMapOvr></p:notes>'''


def simple_rels(entries):
    body = "".join(
        f'<Relationship Id="{rid}" Type="{typ}" Target="{target}"/>'
        for rid, typ, target in entries
    )
    return f'<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Relationships xmlns="{NS_REL}">{body}</Relationships>'


def presentation_xml(count):
    slide_ids = "".join(f'<p:sldId id="{255+i}" r:id="rId{i}"/>' for i in range(1, count + 1))
    return f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<p:presentation xmlns:a="{NS_A}" xmlns:r="{NS_R}" xmlns:p="{NS_P}">
<p:sldMasterIdLst><p:sldMasterId id="2147483648" r:id="rIdMaster"/></p:sldMasterIdLst>
<p:notesMasterIdLst><p:notesMasterId r:id="rIdNotesMaster"/></p:notesMasterIdLst>
<p:sldIdLst>{slide_ids}</p:sldIdLst>
<p:sldSz cx="12192000" cy="6858000" type="wide"/><p:notesSz cx="6858000" cy="9144000"/>
</p:presentation>'''


def content_types(count, base_ct):
    # Preserve non-slide defaults and master/theme/layout overrides from base; rebuild slide/note overrides.
    defaults = re.findall(r"<Default [^>]*/>", base_ct)
    overrides = [
        '<Override PartName="/ppt/presentation.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.presentation.main+xml"/>',
        '<Override PartName="/ppt/slideMasters/slideMaster1.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.slideMaster+xml"/>',
        '<Override PartName="/ppt/slideLayouts/slideLayout1.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.slideLayout+xml"/>',
        '<Override PartName="/ppt/theme/theme1.xml" ContentType="application/vnd.openxmlformats-officedocument.theme+xml"/>',
        '<Override PartName="/ppt/theme/theme2.xml" ContentType="application/vnd.openxmlformats-officedocument.theme+xml"/>',
        '<Override PartName="/ppt/notesMasters/notesMaster1.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.notesMaster+xml"/>',
    ]
    overrides += [
        f'<Override PartName="/ppt/slides/slide{i}.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.slide+xml"/>'
        for i in range(1, count + 1)
    ]
    overrides += [
        f'<Override PartName="/ppt/notesSlides/notesSlide{i}.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.notesSlide+xml"/>'
        for i in range(1, count + 1)
    ]
    # Keep docProps overrides.
    overrides += re.findall(r'<Override PartName="/docProps/[^"]+" [^>]*/>', base_ct)
    return f'<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Types xmlns="{NS_CT}">{"".join(defaults + overrides)}</Types>'


def main():
    sections = parse_sections()
    chunks = split_notes(sections)
    if len(chunks) != len(TITLE_OVERRIDES):
        raise RuntimeError(f"title count {len(TITLE_OVERRIDES)} != chunk count {len(chunks)}")
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(BASE) as base, zipfile.ZipFile(SOURCE) as source, zipfile.ZipFile(OUT, "w", zipfile.ZIP_DEFLATED) as out:
        skip_prefixes = (
            "ppt/slides/",
            "ppt/notesSlides/",
            "ppt/notesMasters/",
        )
        skip_names = {"ppt/presentation.xml", "ppt/_rels/presentation.xml.rels", "[Content_Types].xml"}
        for info in base.infolist():
            name = info.filename
            if name in skip_names or name.startswith(skip_prefixes):
                continue
            out.writestr(info, base.read(name))
        # Add notes master from source.
        for name in ["ppt/notesMasters/notesMaster1.xml", "ppt/notesMasters/_rels/notesMaster1.xml.rels", "ppt/theme/theme2.xml"]:
            out.writestr(name, source.read(name))
        count = len(chunks)
        out.writestr("ppt/presentation.xml", presentation_xml(count))
        pres_rels = [(f"rId{i}", "http://schemas.openxmlformats.org/officeDocument/2006/relationships/slide", f"slides/slide{i}.xml") for i in range(1, count + 1)]
        pres_rels.append(("rIdMaster", "http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideMaster", "slideMasters/slideMaster1.xml"))
        pres_rels.append(("rIdNotesMaster", "http://schemas.openxmlformats.org/officeDocument/2006/relationships/notesMaster", "notesMasters/notesMaster1.xml"))
        out.writestr("ppt/_rels/presentation.xml.rels", simple_rels(pres_rels))
        base_ct = base.read("[Content_Types].xml").decode("utf-8")
        out.writestr("[Content_Types].xml", content_types(count, base_ct))
        for i, ((sec, paras), title) in enumerate(zip(chunks, TITLE_OVERRIDES), 1):
            dark = i in {1, 5, 11, 22, 26, 30, 40, 46, 52, 55, 56}
            flame = i in {1, 2, 52, 55, 56}
            out.writestr(f"ppt/slides/slide{i}.xml", slide_xml(i, title, dark=dark, flame=flame))
            out.writestr(
                f"ppt/slides/_rels/slide{i}.xml.rels",
                simple_rels([
                    ("rId1", "http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideLayout", "../slideLayouts/slideLayout1.xml"),
                    ("rId2", "http://schemas.openxmlformats.org/officeDocument/2006/relationships/notesSlide", f"../notesSlides/notesSlide{i}.xml"),
                ]),
            )
            note_text = "\n".join(paras)
            out.writestr(f"ppt/notesSlides/notesSlide{i}.xml", notes_xml(i, note_text))
            out.writestr(
                f"ppt/notesSlides/_rels/notesSlide{i}.xml.rels",
                simple_rels([
                    ("rId1", "http://schemas.openxmlformats.org/officeDocument/2006/relationships/notesMaster", "../notesMasters/notesMaster1.xml"),
                ]),
            )
    print(OUT)
    print(f"slides={len(chunks)}")


if __name__ == "__main__":
    main()
