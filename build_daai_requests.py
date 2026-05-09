import json

W, H = 12192000, 6858000
SLIDES = [
    ("我曾經燒掉考卷", "鄭國威｜泛科學共同創辦人\n大愛人文講堂", "00"),
    ("15 歲的我，正在燒考卷", "我站在旁邊，看著那個瞬間發生。\n不是青春叛逆，是信任斷線。", "01"),
    ("那不是浪漫畫面", "那是一個人對數學、科學、學習，\n以及被評量的人生失去信任。", "01"),
    ("我以為自己討厭知識", "後來才知道，我討厭的是\n只能用單一標準證明自己的系統。", "01"),
    ("第一個問題", "人為什麼會討厭學習？", "02"),
    ("我不是不會學", "我是不知道，為什麼要學。", "02"),
    ("知識被切碎後", "就會失去意義。\n剩下答案、分數、排名，沒有世界。", "02"),
    ("科學素養不是背答案", "知道很多答案，仍可能不知道\n如何面對一件不確定的事。", "02"),
    ("科學素養是面對未知的方法", "先問問題，再看證據。\n再允許自己修正。", "02"),
    ("轉折", "世界開始露出裂縫。", "03"),
    ("我的非正規教材", "動漫、遊戲、科幻、網路、科技新聞、社會議題。\n它們沒有考我，卻開始逼我提問。", "03"),
    ("原來知識可以破解世界", "不是課本突然變可愛。\n是我發現它能解釋事情怎麼運作。", "03"),
    ("好奇不是天賦", "好奇是被問題點燃。\n一個好問題，比標準答案更有價值。", "03"),
    ("從理解世界", "到想把世界講清楚。", "04"),
    ("泛科學的開始", "全台最大科學社群之一。\nYouTube、網站、社群、活動，都是不同入口。", "04"),
    ("科學傳播不是把知識講簡單", "真正困難的是：\n不背叛知識，又讓人願意靠近。", "04"),
    ("科學傳播是在找入口", "把專業知識翻譯成一般人\n已經在乎、願意進入的問題。", "04"),
    ("技巧一：從衝突開始", "不要從名詞開始。\n先讓觀眾看見：這裡有矛盾。", "04"),
    ("技巧二：從觀眾在乎的事開始", "健康、AI、食安、能源、演算法。\n入口通常在生活，不在術語。", "04"),
    ("技巧三：比喻是臨時鷹架", "好比喻不是裝飾。\n它只是幫人先站上去，看見結構。", "04"),
    ("技巧四：幽默降低摩擦", "幽默不是稀釋知識。\n它只是讓人願意多停留一分鐘。", "04"),
    ("技巧五：保留不確定性", "科學傳播不能只追求有趣。\n也要讓限制、誤差、例外有位置。", "04"),
    ("AI 時代", "知識更便宜，判斷更昂貴。", "05"),
    ("現代人每天都在做測驗", "不是考卷，是資訊流。\n健康建議、投資話術、AI 生成內容、社群怒氣。", "05"),
    ("你怎麼知道這是真的？", "證據在哪裡？誰說的？怎麼知道的？\n有沒有反例？能不能被推翻？", "05"),
    ("我是不是只是在找", "自己想相信的東西？", "05"),
    ("懷疑不是否定一切", "懷疑是給證據一個上場的機會。", "05"),
    ("回到 15 歲那個房間", "那個人手上還拿著考卷。\n火已經點起來了。", "06"),
    ("我不會阻止他", "我不會說：不要放棄。\n我大概也不會急著安慰他。", "06"),
    ("我只會問他一個問題", "你真正討厭的是知識，\n還是那個只准你用分數理解自己的世界？", "06"),
    ("科學素養不是把人變成科學家", "它讓人不那麼容易被答案馴服。", "06"),
    ("好的學習", "不是讓人更會考試。\n是讓人重新取得提問的權利。", "06"),
]

PALETTES = {
    "00": ("07285a", "0a5fb4", "ffffff"),
    "01": ("0b1726", "1d4ed8", "f8fbff"),
    "02": ("f8fbff", "0a4f9e", "102033"),
    "03": ("eff7ff", "00a7c4", "102033"),
    "04": ("ffffff", "0069c9", "102033"),
    "05": ("061b33", "18a0d8", "ffffff"),
    "06": ("f8fbff", "0a4f9e", "102033"),
}


def rgb(hexstr):
    return {
        "red": int(hexstr[0:2], 16) / 255,
        "green": int(hexstr[2:4], 16) / 255,
        "blue": int(hexstr[4:6], 16) / 255,
    }


def box(slide_id, obj_id, x, y, w, h, text, size, color, bold=True, align="START"):
    return [
        {"createShape": {"objectId": obj_id, "shapeType": "TEXT_BOX", "elementProperties": {"pageObjectId": slide_id, "size": {"width": {"magnitude": w, "unit": "EMU"}, "height": {"magnitude": h, "unit": "EMU"}}, "transform": {"scaleX": 1, "scaleY": 1, "translateX": x, "translateY": y, "unit": "EMU"}}}},
        {"insertText": {"objectId": obj_id, "insertionIndex": 0, "text": text}},
        {"updateTextStyle": {"objectId": obj_id, "textRange": {"type": "ALL"}, "style": {"foregroundColor": {"opaqueColor": {"rgbColor": rgb(color)}}, "fontFamily": "Noto Sans TC", "fontSize": {"magnitude": size, "unit": "PT"}, "bold": bold}, "fields": "foregroundColor,fontFamily,fontSize,bold"}},
        {"updateParagraphStyle": {"objectId": obj_id, "textRange": {"type": "ALL"}, "style": {"alignment": align, "lineSpacing": 112}, "fields": "alignment,lineSpacing"}},
    ]


def rect(slide_id, obj_id, x, y, w, h, fill, alpha=1):
    return {"createShape": {"objectId": obj_id, "shapeType": "RECTANGLE", "elementProperties": {"pageObjectId": slide_id, "size": {"width": {"magnitude": w, "unit": "EMU"}, "height": {"magnitude": h, "unit": "EMU"}}, "transform": {"scaleX": 1, "scaleY": 1, "translateX": x, "translateY": y, "unit": "EMU"}}}}, {"updateShapeProperties": {"objectId": obj_id, "shapeProperties": {"shapeBackgroundFill": {"solidFill": {"color": {"rgbColor": rgb(fill)}, "alpha": alpha}}, "outline": {"propertyState": "NOT_RENDERED"}}, "fields": "shapeBackgroundFill,outline"}}


requests = []
for i, (title, body, mood) in enumerate(SLIDES):
    sid = f"slide{i+1:02d}"
    bg, accent, text = PALETTES[mood]
    requests.append({"createSlide": {"objectId": sid, "insertionIndex": 25 + i, "slideLayoutReference": {"predefinedLayout": "BLANK"}}})
    requests.extend(rect(sid, f"{sid}_bg", 0, 0, W, H, bg))
    requests.extend(rect(sid, f"{sid}_safe", 0, 5900000, W, 958000, "eaf3ff" if bg != "061b33" else "0b2b4a", 0.35))
    requests.extend(rect(sid, f"{sid}_bar", 520000, 520000, 140000, 4760000, accent))
    if i in [4, 9, 13, 22, 27]:
        requests.extend(rect(sid, f"{sid}_wide", 0, 0, W, H, accent, 1))
        text = "ffffff"
        accent = "ffffff"
    if i in [0, 1, 2, 28, 29, 31]:
        title_size, body_size = 54, 25
    else:
        title_size, body_size = 46, 23
    requests.extend(box(sid, f"{sid}_title", 860000, 880000, 9500000, 1500000, title, title_size, text, True))
    requests.extend(box(sid, f"{sid}_body", 880000, 2800000, 9300000, 1900000, body, body_size, text, False))
    requests.extend(box(sid, f"{sid}_num", 10700000, 520000, 900000, 300000, f"{i+1:02d}/32", 12, accent, True, "END"))
    requests.extend(rect(sid, f"{sid}_line", 880000, 2320000, 2100000, 38000, accent))

for old in [f"p{i}" for i in range(1, 26)]:
    requests.append({"deleteObject": {"objectId": old}})

if __name__ == "__main__":
    import sys
    if len(sys.argv) == 1:
        print(json.dumps(requests, ensure_ascii=False, separators=(",", ":")))
    else:
        batch = int(sys.argv[1])
        # Eight content batches plus a cleanup batch.
        if 1 <= batch <= 8:
            start_slide = (batch - 1) * 4
            end_slide = start_slide + 4
            ids = {f"slide{i+1:02d}" for i in range(start_slide, end_slide)}
            out = []
            current = None
            for req in requests:
                key = next(iter(req))
                val = req[key]
                sid = None
                if key == "createSlide":
                    sid = val["objectId"]
                    current = sid
                elif key in {"createShape"}:
                    sid = val["elementProperties"]["pageObjectId"]
                    current = sid
                elif key in {"insertText", "updateTextStyle", "updateParagraphStyle", "updateShapeProperties"}:
                    obj = val["objectId"]
                    sid = obj.split("_", 1)[0]
                if sid in ids:
                    out.append(req)
            print(json.dumps(out, ensure_ascii=False, separators=(",", ":")))
        elif batch == 9:
            print(json.dumps([{"deleteObject": {"objectId": f"p{i}"}} for i in range(1, 26)], ensure_ascii=False, separators=(",", ":")))
