# -*- coding: utf-8 -*-
"""Sinh website tĩnh Vitamin Bắc Ninh. Chạy: python3 gen.py <thư mục ra>"""
import json, os, sys, html
from urllib.parse import quote

DOMAIN = "https://vitaminbacninh.github.io"   # đổi thành tên miền riêng khi có
BRAND = "Vitamin Bắc Ninh"
LEGAL = "Công ty Cổ phần Vitamin Bắc Ninh"
MST = "0111272601"
ADDR = "Số 118 Phương Vỹ, phường Vũ Ninh, tỉnh Bắc Ninh"
STREET = "Số 118 Phương Vỹ, phường Vũ Ninh"
PHONE = "0389 799 192"
PHONE_INTL = "+84389799192"
ZALO = "https://zalo.me/0389799192"
EMAIL = "thodia.bn99@gmail.com"   # email nhận hồ sơ ứng tuyển
MAPS = "https://www.google.com/maps/search/?api=1&query=118+Ph%C6%B0%C6%A1ng+V%E1%BB%B9+V%C5%A9+Ninh+B%E1%BA%AFc+Ninh"
SAME_AS = [  # thêm link Fanpage khi có
    "https://www.tiktok.com/@thodia.bn",
    "https://www.youtube.com/@Thodiabacninh",
    "https://www.facebook.com/Thodiabacninh99/",
    "https://www.tiktok.com/@bacninhangii",
]
TODAY = "2026-11-05"

E = html.escape

PACKAGES = [
    dict(name="Gói Trải nghiệm", price=8_000_000, n=3, views="50.000+",
         channels=["Thổ Địa Bắc Ninh", "U50 Bắc Ninh", "Người Bắc Ninh Chất"], sat=[],
         note="Hợp quán nhỏ, quán mới mở muốn thử TikTok."),
    dict(name="Gói Tạo độ phủ", price=17_000_000, n=4, views="300.000+",
         channels=["Thổ Địa Bắc Ninh", "U50 Bắc Ninh", "Xoài Trứng Nướng", "Bắc Ninh Ăn Gì?"],
         sat=["La Cà Bắc Ninh", "Một Ngày Bắc Ninh", "Bắc Ninh Đi Đâu?", "Bắc Ninh Chill"],
         note="Phủ nhanh tên quán trên nhiều kênh cùng lúc."),
    dict(name="Gói Chuyển đổi cao", price=25_000_000, n=7, views="500.000+", hot=True,
         channels=["Thổ Địa Bắc Ninh", "U50 Bắc Ninh", "Quang Châu Ăn Gì", "Xoài Trứng Nướng", "Bắc Ninh Ăn Gì?", "Độc Lạ Bắc Ninh", "Lang Thang Bắc Ninh"],
         sat=["La Cà Bắc Ninh", "Một Ngày Bắc Ninh", "Bắc Ninh Đi Đâu?", "Bắc Ninh Chill"],
         note="Được khách chọn nhiều nhất, cân bằng giữa độ phủ và chi phí."),
    dict(name="Gói Phủ sóng toàn diện", price=40_000_000, n=11, views="1.000.000+",
         channels=["Thổ Địa Bắc Ninh", "U50 Bắc Ninh", "Quang Châu Ăn Gì", "Xoài Trứng Nướng", "Bắc Ninh Ăn Gì?", "Độc Lạ Bắc Ninh", "Lang Thang Bắc Ninh", "Thổ Địa Từ Sơn", "Hương Trố Từ Sơn", "Bánh Mỳ Cô Phượng", "Mai Mai Bắc Ninh"],
         sat=["La Cà Bắc Ninh", "Một Ngày Bắc Ninh", "Bắc Ninh Đi Đâu?", "Bắc Ninh Chill"],
         note="Chiến dịch khai trương, ra mắt thương hiệu, chuỗi cửa hàng."),
]

# tên, giá thấp, giá cao, nhóm, follower (TikTok/Facebook/YouTube) nếu có, link
CHANNELS = [
    ("Thổ Địa Bắc Ninh", 6_000_000, None, "Kênh chủ lực", None, None),
    ("Xoài Trứng Nướng", 6_000_000, 8_000_000, "Kênh chủ lực", None, None),
    ("Su Con Mẹ Xoài", 6_000_000, 10_000_000, "Kênh chủ lực", None, None),
    ("Mai Mai Bắc Ninh", 6_000_000, None, "Kênh chủ lực", None, None),
    ("Bánh Mỳ Cô Phượng", 5_000_000, None, "Kênh chủ lực", None, None),
    ("Hương Trố Từ Sơn", 5_000_000, None, "Kênh khu vực Từ Sơn", None, None),
    ("U50 Bắc Ninh", 3_000_000, None, "Kênh chủ lực", None, None),
    ("Bắc Ninh Ăn Gì?", 3_000_000, None, "Kênh ẩm thực", None, None),
    ("Quang Châu Ăn Gì", 2_000_000, None, "Kênh khu công nghiệp", None, None),
    ("Thổ Địa Từ Sơn", 2_000_000, None, "Kênh khu vực Từ Sơn", None, None),
    ("Độc Lạ Bắc Ninh", 1_500_000, None, "Kênh hỗ trợ độ phủ", None, None),
    ("Lang Thang Bắc Ninh", 1_500_000, None, "Kênh hỗ trợ độ phủ", None, None),
    ("Người Bắc Ninh Chất", 1_000_000, None, "Kênh hỗ trợ độ phủ", None, None),
    ("Thổ Địa Quế Võ", 1_000_000, None, "Kênh khu vực Quế Võ", None, None),
    ("La Cà Bắc Ninh", 800_000, None, "Kênh vệ tinh", None, None),
    ("Bắc Ninh Đi Đâu?", 800_000, None, "Kênh vệ tinh", None, None),
    ("Bắc Ninh Chill", 800_000, None, "Kênh vệ tinh", None, None),
    ("Một Ngày Bắc Ninh", 800_000, None, "Kênh vệ tinh", None, None),
]

# Hồ sơ từng kênh trên 3 nền tảng. Số TikTok, YouTube lấy trực tiếp ngày 04/11/2026; Facebook ngày 05/11/2026.
# tt = (handle TikTok, follower), fb = (link hoặc None, follower), yt = (handle YouTube, người đăng ký), av = ảnh đại diện trong img/kenh
PROFILES = {
    "Thổ Địa Bắc Ninh":    dict(tt=("thodia.bn", "203K"), fb=("https://www.facebook.com/Thodiabacninh99/", "246K"), yt=("Thodiabacninh", "21,2K"), av="thodia.bn"),
    "Xoài Trứng Nướng":    dict(tt=("xoaitrungnuong", "309K"), fb=("https://www.facebook.com/p/Xo%C3%A0i-Tr%E1%BB%A9ng-N%C6%B0%E1%BB%9Bng-61550546369947/", "104K"), yt=("XoàiTrứngNướng", "213K"), av="xoaitrungnuong"),
    "Su Con Mẹ Xoài":      dict(tt=("suconmexoai", "162K"), fb=("https://www.facebook.com/Suconmexoai/", "31K"), yt=("SuconmẹXoài", "31,1K"), av="suconmexoai"),
    "Mai Mai Bắc Ninh":    dict(tt=("maimaibacninh", "9,3K"), av="maimaibacninh"),
    "Bánh Mỳ Cô Phượng":   dict(tt=("banhmycophuong", "40,1K"), yt=("BánhMỳCôPhượng", "48,3K"), av="banhmycophuong"),
    "Hương Trố Từ Sơn":    dict(tt=("huongtrotuson", "8,5K"), fb=("https://www.facebook.com/huongtrotuson/", "7,8K"), av="huongtrotuson"),
    "U50 Bắc Ninh":        dict(tt=("u50bacninh", "27,2K"), fb=("https://www.facebook.com/U50bacninh/", "43K"), av="u50bacninh"),
    "Bắc Ninh Ăn Gì?":     dict(tt=("bacninhangii", "27,7K"), fb=("https://www.facebook.com/bacninhangi/", "5,5K"), av="bacninhangii"),
    "Quang Châu Ăn Gì":    dict(tt=("quangchauangi", "1,3K"), av="quangchauangi"),
    "Độc Lạ Bắc Ninh":     dict(tt=("doclabacninh", "22K"), av="doclabacninh"),
    "Lang Thang Bắc Ninh": dict(tt=("langthang.bacninh", "20,4K"), av="langthang.bacninh"),
    "Người Bắc Ninh Chất": dict(tt=("nguoibacninhchat", "12,3K"), av="nguoibacninhchat"),
    "La Cà Bắc Ninh":      dict(tt=("lacabacninh7", "1,2K"), av="lacabacninh7"),
    "Một Ngày Bắc Ninh":   dict(tt=("motngaybacninh", "10,9K"), av="motngaybacninh"),
    "Thổ Địa Từ Sơn":      dict(av="thodiatuson"),
    "Thổ Địa Quế Võ":      dict(av="thodiaquevo"),
    "Bắc Ninh Đi Đâu?":    dict(av="bacninhdidau"),
    "Bắc Ninh Chill":      dict(av="bacninhchill"),
}

def links_of(n):
    """Danh sách (nền tảng, url hoặc None, số follower) của một kênh."""
    p = PROFILES.get(n, {})
    out = []
    if p.get("tt"): out.append(("TikTok", f"https://www.tiktok.com/@{p['tt'][0]}", p["tt"][1]))
    if p.get("fb"): out.append(("Facebook", p["fb"][0], p["fb"][1]))
    if p.get("yt"): out.append(("YouTube", "https://www.youtube.com/@" + quote(p["yt"][0]), p["yt"][1]))
    return out

CLIENTS = [
    ("Ngân hàng, y tế", "MB Bank, Bệnh viện Thu Cúc TCI, Bệnh viện Quốc tế Luxdefa"),
    ("Ô tô, điện tử, gia dụng", "VinFast, Xiaomi, Hoàng Hà Mobile, Honor, Lock&Lock, Kingsport"),
    ("Thời trang, mỹ phẩm", "Atino, KRIK, Cocolux, F5 Sport"),
    ("Ẩm thực, đồ uống", "Manwah, Jollibee, Bia Hà Nội (Hanoi Premium), Kinh Đô, Aice"),
    ("Bất động sản, xây dựng", "Viettel Construction, Ecolife Yên Trung"),
    ("Khác", "MadeMade và nhiều doanh nghiệp Trung Quốc tại Bắc Ninh"),
]

# Đối tác hiển thị dạng lưới logo. Có file img/doitac/<slug>.png (hoặc .svg) thì hiện logo, chưa có thì hiện ô tên.
# Chỉ thêm logo khi nhãn hàng đồng ý cho dùng logo trong hồ sơ năng lực.
PARTNERS = [
    ("Ngân hàng, y tế", [("MB Bank", "mbbank"), ("Bệnh viện Thu Cúc TCI", "thucuc"), ("Bệnh viện Quốc tế Luxdefa", "luxdefa")]),
    ("Ô tô, điện tử, gia dụng", [("VinFast", "vinfast"), ("Xiaomi", "xiaomi"), ("Hoàng Hà Mobile", "hoangha"), ("Honor", "honor"), ("Lock&Lock", "locknlock"), ("Kingsport", "kingsport")]),
    ("Thời trang, mỹ phẩm", [("Atino", "atino"), ("KRIK", "krik"), ("Cocolux", "cocolux"), ("F5 Sport", "f5sport")]),
    ("Ẩm thực, đồ uống", [("Manwah", "manwah"), ("Jollibee", "jollibee"), ("Bia Hà Nội", "biahanoi"), ("Kinh Đô", "kinhdo"), ("Aice", "aice")]),
    ("Bất động sản, xây dựng", [("Viettel Construction", "viettelconstruction"), ("Ecolife Yên Trung", "ecolife")]),
    ("Khác", [("MadeMade", "mademade")]),
]
HOME_PARTNERS = ["mbbank", "vinfast", "thucuc", "atino", "krik", "xiaomi", "jollibee", "manwah", "viettelconstruction", "locknlock", "kinhdo", "biahanoi"]

def logo_tile(name, slug):
    here = os.path.dirname(os.path.abspath(__file__))
    for ext in ("svg", "png", "webp", "jpg"):
        if os.path.exists(os.path.join(here, "img", "doitac", f"{slug}.{ext}")):
            return f'<li class="lg"><img src="img/doitac/{slug}.{ext}" alt="{E(name)}" loading="lazy"></li>'
    return f'<li class="lg lg-txt"><span>{E(name)}</span></li>'

def logo_wall(slugs=None):
    allp = {s: n for _, items in PARTNERS for n, s in items}
    pick = slugs or list(allp)
    return '<ul class="logos">' + "".join(logo_tile(allp[s], s) for s in pick) + "</ul>"

FAQ = [
    ("Booking review TikTok ở Bắc Ninh giá bao nhiêu?",
     "Tại Vitamin Bắc Ninh, booking lẻ một kênh từ 800.000đ đến 10.000.000đ/video tùy độ lớn của kênh. Kênh lớn nhất là Thổ Địa Bắc Ninh, 6.000.000đ/video. Gói nhiều kênh cùng đăng từ 8.000.000đ (3 kênh) đến 40.000.000đ (11 kênh chính và 4 kênh vệ tinh)."),
    ("Kênh review nào ở Bắc Ninh có nhiều người xem?",
     "Hệ thống Vitamin Bắc Ninh có các kênh Thổ Địa Bắc Ninh (203K follower TikTok, 246K Facebook), Xoài Trứng Nướng (309K TikTok, 213K YouTube), Su Con Mẹ Xoài (162K TikTok) và U50 Bắc Ninh. Thổ Địa Bắc Ninh có 25 video trên 1 triệu lượt xem, video cao nhất 7,7 triệu lượt xem."),
    ("Book review có cam kết lượt xem không?",
     "Có, với booking theo gói. Lượt xem cam kết là tổng của tất cả kênh trong gói, tính sau 1 tuần: gói 8 triệu từ 50.000 view, gói 17 triệu từ 300.000 view, gói 25 triệu từ 500.000 view, gói 40 triệu từ 1.000.000 view."),
    ("Video review có bị gỡ sau một thời gian không?",
     "Không. Video đăng trên kênh được giữ lâu dài, người xem vẫn tìm thấy quán qua video sau nhiều tháng."),
    ("Ai sẽ đến quay ở quán?",
     "Đội quay của Vitamin Bắc Ninh đến tận quán, quay món ăn, không gian, giá và đường đến, sau đó dựng video và đăng lên các kênh đã chọn. Chủ quán duyệt video trước khi đăng."),
    ("Ngoài review quán ăn còn làm dịch vụ gì?",
     "Vitamin Bắc Ninh nhận booking KOL/KOC cho nhãn hàng, xây kênh TikTok cho doanh nghiệp và sản xuất video quảng cáo (TVC). Liên hệ hotline/Zalo 0389 799 192 để nhận báo giá."),
]

def vnd(n):
    return f"{n:,.0f}".replace(",", ".") + "đ"

def price_range(lo, hi):
    return vnd(lo) if not hi else f"{vnd(lo)} – {vnd(hi)}"

FONTS = '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Be+Vietnam+Pro:wght@400;500;600;800&display=swap">'

CSS = open(os.path.join(os.path.dirname(__file__), "style.css"), encoding="utf-8").read()

def org_ld():
    return {
        "@context": "https://schema.org",
        "@type": ["LocalBusiness", "ProfessionalService"],
        "@id": DOMAIN + "/#org",
        "name": BRAND,
        "legalName": LEGAL,
        "taxID": MST,
        "url": DOMAIN + "/",
        "telephone": PHONE_INTL,
        "description": "Vitamin Bắc Ninh vận hành hệ thống 18 kênh review TikTok, Facebook, YouTube tại Bắc Ninh, nhận booking review quán ăn, cửa hàng, booking KOL/KOC, xây kênh và sản xuất video quảng cáo.",
        "address": {"@type": "PostalAddress", "streetAddress": STREET, "addressRegion": "Bắc Ninh", "addressCountry": "VN"},
        "areaServed": ["Bắc Ninh", "Từ Sơn", "Tiên Du", "Yên Phong", "Quế Võ", "Việt Yên"],
        "priceRange": "800.000đ – 40.000.000đ",
        "sameAs": SAME_AS,
    }

NAV = [("index.html", "Trang chủ"), ("bang-gia.html", "Bảng giá"), ("he-thong-kenh.html", "Hệ thống kênh"), ("khach-hang.html", "Khách hàng"), ("tuyen-dung.html", "Tuyển dụng"), ("lien-he.html", "Liên hệ")]

def page(fname, title, desc, body, extra_ld=None, full=True):
    canon = DOMAIN + "/" + ("" if fname == "index.html" else fname)
    lds = [org_ld()] + (extra_ld or [])
    ld = "\n".join(f'<script type="application/ld+json">{json.dumps(x, ensure_ascii=False)}</script>' for x in lds)
    nav = "".join(f'<a href="{h}"{" aria-current=\"page\"" if h == fname else ""}>{E(t)}</a>' for h, t in NAV)
    head = f"""<title>{E(title)}</title>
<meta name="description" content="{E(desc)}">
<meta name="claude:viewport-fit-sides" content="cover">
<link rel="canonical" href="{canon}">
<meta property="og:type" content="website"><meta property="og:title" content="{E(title)}"><meta property="og:description" content="{E(desc)}"><meta property="og:url" content="{canon}"><meta property="og:locale" content="vi_VN">
{FONTS}
<style>{CSS}</style>
{ld}"""
    content = f"""<header class="top"><div class="wrap top-in">
<a class="logo" href="index.html"><span class="dot" aria-hidden="true"></span>Vitamin <b>Bắc Ninh</b></a>
<nav aria-label="Menu chính">{nav}</nav>
<a class="btn btn-sm" href="{ZALO}" rel="noopener">Zalo {PHONE}</a>
</div></header>
<main>{body}</main>
<footer class="foot"><div class="wrap foot-in">
<div><p class="logo">Vitamin <b>Bắc Ninh</b></p><p>Hệ thống 18 kênh review TikTok, Facebook, YouTube tại Bắc Ninh.</p></div>
<div><p><b>{E(LEGAL)}</b></p><p>MST: {MST}</p><p>{E(ADDR)}</p><p>Hotline/Zalo: <a href="tel:{PHONE_INTL}">{PHONE}</a></p></div>
<div><p><b>Dịch vụ</b></p><p><a href="bang-gia.html">Booking review Bắc Ninh</a></p><p><a href="bang-gia.html#goi">Gói truyền thông nhiều kênh</a></p><p><a href="he-thong-kenh.html">Danh sách kênh review</a></p><p><a href="tuyen-dung.html">Tuyển dụng</a></p></div>
</div><p class="wrap fine">Cập nhật {TODAY[8:10]}/{TODAY[5:7]}/{TODAY[:4]}. Bảng giá chưa gồm VAT.</p></footer>"""
    if full:
        return f"""<!doctype html>
<html lang="vi"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
{head}
</head><body>
{content}
</body></html>"""
    return head + "\n" + content

def stat_strip():
    return """<ul class="stats">
<li><b>18</b><span>kênh review trong hệ thống</span></li>
<li><b>1,3 triệu+</b><span>lượt theo dõi TikTok, Facebook, YouTube</span></li>
<li><b>500+</b><span>đối tác đã hợp tác</span></li>
<li><b>7,7 triệu</b><span>view, video cao nhất của Thổ Địa Bắc Ninh</span></li>
</ul>"""

def pkg_cards():
    out = []
    for p in PACKAGES:
        chans = "".join(f"<li>{E(c)}</li>" for c in p["channels"])
        sat = f'<p class="sat">Tặng kèm {len(p["sat"])} kênh vệ tinh: {E(", ".join(p["sat"]))}</p>' if p["sat"] else ""
        hot = '<span class="tag">Được chọn nhiều nhất</span>' if p.get("hot") else ""
        out.append(f"""<article class="pkg{' hot' if p.get('hot') else ''}">{hot}
<h3>{E(p['name'])}</h3>
<p class="price">{vnd(p['price'])}</p>
<p class="meta">{p['n']} kênh chính · cam kết <b>{p['views']} view</b> sau 1 tuần</p>
<ol class="chans">{chans}</ol>{sat}
<p class="note">{E(p['note'])}</p>
</article>""")
    return '<div class="pkgs">' + "".join(out) + "</div>"

def faq_html():
    return '<div class="faq">' + "".join(f"<details><summary>{E(q)}</summary><p>{E(a)}</p></details>" for q, a in FAQ) + "</div>"

def faq_ld():
    return {"@context": "https://schema.org", "@type": "FAQPage",
            "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQ]}

CTA = f"""<section class="cta"><div class="wrap cta-in">
<div><h2>Cần quảng bá quán hoặc thương hiệu ở Bắc Ninh?</h2><p>Gửi tên quán và ngân sách, Vitamin Bắc Ninh tư vấn kênh phù hợp trong ngày.</p></div>
<div class="cta-act"><a class="btn" href="{ZALO}" rel="noopener">Nhắn Zalo {PHONE}</a><a class="btn btn-ghost" href="tel:{PHONE_INTL}">Gọi ngay</a></div>
</div></section>"""

def avatar_strip():
    top = ["Thổ Địa Bắc Ninh", "Xoài Trứng Nướng", "Su Con Mẹ Xoài", "Bánh Mỳ Cô Phượng", "Bắc Ninh Ăn Gì?", "U50 Bắc Ninh", "Độc Lạ Bắc Ninh", "Lang Thang Bắc Ninh"]
    li = []
    for n in top:
        p = PROFILES[n]
        li.append(f'<li><a href="https://www.tiktok.com/@{p["tt"][0]}" rel="noopener" target="_blank"><img class="av" src="img/kenh/{p["av"]}.jpg" width="72" height="72" loading="lazy" alt="Kênh {E(n)}"><b>{E(n)}</b><span>{p["tt"][1]} TikTok</span></a></li>')
    return f'<ul class="strip">{"".join(li)}</ul>'

def index_page(full=True):
    body = f"""<section class="hero"><div class="wrap hero-in">
<div class="hero-copy">
<p class="eyebrow">Agency truyền thông · MCN TikTok · Bắc Ninh</p>
<h1>Booking review TikTok tại Bắc Ninh</h1>
<p class="lead">Vitamin Bắc Ninh vận hành 18 kênh review địa phương như Thổ Địa Bắc Ninh, Xoài Trứng Nướng, Su Con Mẹ Xoài, U50 Bắc Ninh. Đội quay đến tận quán, dựng video và đăng lên các kênh, giá từ 800.000đ/video.</p>
<div class="hero-act"><a class="btn" href="bang-gia.html">Xem bảng giá</a><a class="btn btn-ghost" href="{ZALO}" rel="noopener">Nhắn Zalo tư vấn</a></div>
</div>
<div class="phone" aria-hidden="true"><div class="phone-screen">
<p class="ph-handle">@thodia.bn</p>
<p class="ph-cap">Ăn gì, chơi đâu ở Bắc Ninh hôm nay?</p>
<p class="ph-loc">📍 Bắc Ninh</p>
<ul class="ph-side"><li>♥</li><li>💬</li><li>↗</li></ul>
<p class="ph-views">▶ 7,7 triệu lượt xem</p>
</div></div>
</div>{stat_strip()}</section>

<section class="sec"><div class="wrap">
<h2>Dịch vụ</h2>
<div class="svc">
<article><h3>Booking review quán ăn, cửa hàng</h3><p>Video review thật tại quán, có món, giá và địa chỉ trên màn hình. Booking lẻ từng kênh từ 800.000đ/video.</p><a href="bang-gia.html#le">Giá từng kênh</a></article>
<article><h3>Gói truyền thông nhiều kênh</h3><p>3 đến 11 kênh cùng đăng, cam kết từ 50.000 đến hơn 1.000.000 view sau 1 tuần. Từ 8.000.000đ.</p><a href="bang-gia.html#goi">Xem 4 gói</a></article>
<article><h3>Booking KOL/KOC cho nhãn hàng</h3><p>Chiến dịch cho ngân hàng, ô tô, điện tử, thời trang trên hệ thống kênh địa phương. Đã làm cho MB Bank, VinFast, Atino.</p><a href="khach-hang.html">Khách hàng</a></article>
<article><h3>Xây kênh TikTok và video quảng cáo</h3><p>Xây kênh TikTok cho doanh nghiệp, sản xuất video quảng cáo (TVC). Báo giá theo yêu cầu.</p><a href="lien-he.html">Liên hệ báo giá</a></article>
</div></div></section>

<section class="sec alt"><div class="wrap">
<h2>Hệ thống kênh</h2>
<p class="sub">Một số kênh review trong hệ thống Vitamin Bắc Ninh trên TikTok, Facebook, YouTube.</p>
{avatar_strip()}
<p><a href="he-thong-kenh.html">Xem đủ 18 kênh và số follower</a></p>
</div></section>

<section class="sec" id="goi"><div class="wrap">
<h2>Gói booking theo kênh</h2>
<p class="sub">Lượt xem cam kết là tổng của tất cả kênh trong gói, tính sau 1 tuần.</p>
{pkg_cards()}
</div></section>

<section class="sec alt"><div class="wrap">
<h2>Đã hợp tác</h2>
{logo_wall(HOME_PARTNERS)}
<p><a href="khach-hang.html">Xem tất cả đối tác theo lĩnh vực</a></p>
</div></section>

<section class="sec"><div class="wrap narrow">
<h2>Câu hỏi thường gặp</h2>
{faq_html()}
</div></section>
{CTA}"""
    return page("index.html", "Booking review TikTok tại Bắc Ninh | Vitamin Bắc Ninh",
                "Vitamin Bắc Ninh: hệ thống 18 kênh review TikTok tại Bắc Ninh (Thổ Địa Bắc Ninh, Xoài Trứng Nướng, U50). Booking review quán ăn từ 800.000đ, gói nhiều kênh từ 8 triệu. Zalo 0389 799 192.",
                body, [faq_ld()], full)

def price_page():
    rows = "".join(f"<tr><td>{i}</td><td>{E(n)}</td><td class='num'>{price_range(lo, hi)}</td><td>{E(g)}</td></tr>" for i, (n, lo, hi, g, f, l) in enumerate(CHANNELS, 1))
    offers = {"@context": "https://schema.org", "@type": "OfferCatalog", "name": "Bảng giá booking review Bắc Ninh",
              "itemListElement": [{"@type": "Offer", "name": p["name"], "price": p["price"], "priceCurrency": "VND",
                                   "description": f'{p["n"]} kênh chính, cam kết {p["views"]} view sau 1 tuần'} for p in PACKAGES] +
                                  [{"@type": "Offer", "name": f"Booking lẻ kênh {n}", "price": lo, "priceCurrency": "VND"} for (n, lo, hi, g, f, l) in CHANNELS]}
    body = f"""<section class="pagehead"><div class="wrap">
<p class="eyebrow">Bảng giá cập nhật tháng 11/2026</p>
<h1>Bảng giá booking review Bắc Ninh</h1>
<p class="lead">Hai cách book: theo gói nhiều kênh cùng đăng, hoặc lẻ từng kênh. Giá chưa gồm VAT. Video được giữ lâu dài trên kênh.</p>
</div></section>
<section class="sec" id="goi"><div class="wrap">
<h2>1. Booking theo gói</h2>
<p class="sub">Phù hợp khi cần nhiều người biết nhanh. Lượt xem cam kết là tổng tất cả kênh trong gói sau 1 tuần.</p>
{pkg_cards()}
</div></section>
<section class="sec alt" id="le"><div class="wrap">
<h2>2. Booking lẻ từng kênh</h2>
<p class="sub">Giá cho 1 video, gồm quay, dựng và đăng.</p>
<div class="tbl"><table><thead><tr><th>STT</th><th>Kênh</th><th class="num">Giá booking / video</th><th>Nhóm kênh</th></tr></thead><tbody>{rows}</tbody></table></div>
</div></section>
<section class="sec"><div class="wrap">
<h2>Quy trình booking</h2>
<ol class="steps">
<li><b>Gửi thông tin</b><span>Tên quán, địa chỉ, món nổi bật, ngân sách qua Zalo {PHONE}.</span></li>
<li><b>Chọn kênh, chốt lịch</b><span>Vitamin Bắc Ninh đề xuất kênh hoặc gói phù hợp, ký hợp đồng, hẹn ngày quay.</span></li>
<li><b>Quay và dựng</b><span>Đội quay đến tận quán. Video có món, giá, địa chỉ trên màn hình. Chủ quán duyệt trước khi đăng.</span></li>
<li><b>Đăng và báo cáo</b><span>Đăng lên các kênh đã chọn, gửi link và số liệu lượt xem.</span></li>
</ol>
</div></section>
{CTA}"""
    return page("bang-gia.html", "Bảng giá booking review TikTok Bắc Ninh 2026 | Vitamin Bắc Ninh",
                "Bảng giá booking review TikTok tại Bắc Ninh: lẻ từ 800.000đ/video, Thổ Địa Bắc Ninh 6 triệu/video; gói 3 kênh 8 triệu, 7 kênh 25 triệu, 11 kênh 40 triệu, cam kết view sau 1 tuần.",
                body, [offers])

def initials(n):
    w = [x for x in n.replace("?", "").split() if x]
    return (w[0][0] + w[-1][0]).upper() if len(w) > 1 else n[:2].upper()

def chan_card(n, lo, hi, g):
    p = PROFILES.get(n, {})
    if p.get("av"):
        av = f'<img class="av" src="img/kenh/{p["av"]}.jpg" width="72" height="72" loading="lazy" alt="Ảnh đại diện kênh {E(n)}">'
    else:
        av = f'<span class="av av-ph" aria-hidden="true">{E(initials(n))}</span>'
    plats = []
    for plat, url, cnt in links_of(n):
        cls = {"TikTok": "tt", "Facebook": "fb", "YouTube": "yt"}[plat]
        inner = f'<span class="pl {cls}">{plat}</span><b>{cnt}</b>'
        plats.append(f'<li><a href="{url}" rel="noopener" target="_blank">{inner}</a></li>' if url else f'<li><span class="nolink">{inner}</span></li>')
    plat_html = f'<ul class="plats">{"".join(plats)}</ul>' if plats else '<p class="soon">Kênh mới, đang cập nhật</p>'
    handle = f'<p class="handle">@{E(p["tt"][0])}</p>' if p.get("tt") else ""
    return f"""<article class="ch">
<div class="ch-top">{av}<div><h3>{E(n)}</h3>{handle}<p class="grp">{E(g)}</p></div></div>
{plat_html}
<p class="ch-price">{price_range(lo, hi)}<span> / video</span></p>
</article>"""

def channels_page():
    cards = "".join(chan_card(n, lo, hi, g) for (n, lo, hi, g, f, l) in CHANNELS)
    items = []
    for i, (n, *_r) in enumerate(CHANNELS, 1):
        it = {"@type": "ListItem", "position": i, "name": n}
        urls = [u for _, u, _c in links_of(n) if u]
        if urls: it["url"] = urls[0]
        items.append(it)
    il = {"@context": "https://schema.org", "@type": "ItemList", "name": "Hệ thống kênh review Vitamin Bắc Ninh", "itemListElement": items}
    body = f"""<section class="pagehead"><div class="wrap">
<p class="eyebrow">18 kênh · TikTok, Facebook, YouTube</p>
<h1>Hệ thống kênh review Bắc Ninh</h1>
<p class="lead">Các kênh review địa phương do Vitamin Bắc Ninh vận hành, phủ TP Bắc Ninh, Từ Sơn, Quế Võ và khu công nghiệp Quang Châu. Bấm vào từng nền tảng để xem kênh.</p>
</div></section>
<section class="sec"><div class="wrap">
<div class="feat">
<article><h3>Thổ Địa Bắc Ninh</h3><p class="big">203K</p><p>follower TikTok · 246K Facebook · 21,2K YouTube. 25 video trên 1 triệu view, cao nhất 7,7 triệu.</p></article>
<article><h3>Xoài Trứng Nướng</h3><p class="big">309K</p><p>follower TikTok · 213K YouTube (nút bạc) · 104K Facebook.</p></article>
<article><h3>Su Con Mẹ Xoài</h3><p class="big">162K</p><p>follower TikTok · 31,1K YouTube · 31K Facebook.</p></article>
<article><h3>Bánh Mỳ Cô Phượng</h3><p class="big">48,3K</p><p>người đăng ký YouTube · 40,1K follower TikTok.</p></article>
</div>
<h2>Danh sách 18 kênh</h2>
<p class="sub">Số follower cập nhật ngày 05/11/2026. Giá booking lẻ cho 1 video gồm quay, dựng và đăng.</p>
<div class="chs">{cards}</div>
</div></section>
{CTA}"""
    return page("he-thong-kenh.html", "Danh sách kênh review TikTok Bắc Ninh | Vitamin Bắc Ninh",
                "18 kênh review Bắc Ninh của Vitamin Bắc Ninh trên TikTok, Facebook, YouTube: Thổ Địa Bắc Ninh 203K follower TikTok, Xoài Trứng Nướng 309K TikTok và 213K YouTube, Su Con Mẹ Xoài 162K, Bánh Mỳ Cô Phượng, U50 Bắc Ninh.",
                body, [il])

def clients_page():
    groups = "".join(f'<div class="lg-group"><h3>{E(g)}</h3><ul class="logos">' + "".join(logo_tile(n, sl) for n, sl in items) + "</ul></div>" for g, items in PARTNERS)
    body = f"""<section class="pagehead"><div class="wrap">
<p class="eyebrow">500+ đối tác</p>
<h1>Khách hàng của Vitamin Bắc Ninh</h1>
<p class="lead">Từ quán chè, quán phở trong ngõ đến ngân hàng, hãng ô tô, chuỗi thời trang. Mỗi chiến dịch là video thật trên hệ thống kênh review Bắc Ninh.</p>
</div></section>
<section class="sec"><div class="wrap">
<h2>Nhãn hàng theo lĩnh vực</h2>
{groups}
</div></section>
<section class="sec alt"><div class="wrap">
<h2>Một số chiến dịch</h2>
<div class="svc">
<article><h3>MB Bank</h3><p>Chiến dịch giới thiệu thanh toán QR cho khách nước ngoài tại quán ăn, quán cà phê, cửa hàng tiện lợi ở Bắc Ninh.</p></article>
<article><h3>VinFast</h3><p>Video giới thiệu mẫu xe VF 8 trên hệ thống kênh, khách dùng lại video cho fanpage đại lý.</p></article>
<article><h3>Viettel Construction</h3><p>Chuỗi video theo tháng, mỗi đợt chốt chủ đề mới cùng khách.</p></article>
<article><h3>Quán ăn, cửa hàng địa phương</h3><p>Hơn 500 quán và cửa hàng tại Bắc Ninh đã book review: nhà hàng, quán ốc, quán chè, spa, shop thời trang.</p></article>
</div></div></section>
{CTA}"""
    return page("khach-hang.html", "Khách hàng và chiến dịch | Vitamin Bắc Ninh",
                "Vitamin Bắc Ninh đã làm video review cho MB Bank, VinFast, Bệnh viện Thu Cúc TCI, Atino, KRIK, Jollibee, Manwah và hơn 500 quán ăn, cửa hàng tại Bắc Ninh.",
                body)

# Vị trí tuyển dụng, theo mẫu form của Vitamin Network. kind: TTS = thực tập sinh, CTV = cộng tác viên, FULLTIME = toàn thời gian
JOBS = [
    dict(id="koc", title="KOC/KOL/VJ", kinds=["CTV", "FULLTIME"],
         desc="Tự tin giao tiếp, thoải mái đứng trước máy quay. Có lượng theo dõi trên mạng xã hội là lợi thế, chưa có vẫn ứng tuyển được.",
         work=["Làm chiến dịch cho quán ăn và nhãn hàng trên hệ thống kênh", "Livestream, quay video ngắn", "Được đào tạo cách lên hình, nói, bán hàng"]),
    dict(id="content", title="Content Creator", kinds=["TTS", "CTV", "FULLTIME"],
         desc="Không yêu cầu kinh nghiệm. Cần thái độ tốt và ham học hỏi.",
         work=["Hỗ trợ làm nội dung ngắn cho các kênh review", "Lên ý tưởng video, viết caption", "Viết nháp kịch bản cùng biên kịch"]),
    dict(id="video-editor", title="Video Editor", kinds=["TTS", "CTV", "FULLTIME"],
         desc="Thành thạo Premiere hoặc CapCut, có gu thẩm mỹ. Biết bắt trend, hiểu meme, có khiếu hài hước là điểm cộng.",
         work=["Dựng video dọc 9:16 từ cảnh quay có sẵn cho khoảng 4 kênh", "Làm hook, phụ đề, chữ giá và địa chỉ, nhạc nền, ảnh bìa", "Kiểm tra giá, tên quán, địa chỉ khớp brief trước khi nộp"],
         pay="Fulltime: lương cứng 10.000.000đ/tháng cho 60 video, từ video thứ 61 tính 200.000đ/video, video dạng TVC tính riêng 500.000đ/video. Đóng BHXH, BHYT, BHTN.",
         salary=10_000_000),
    dict(id="bien-kich", title="Biên kịch", kinds=["TTS", "CTV", "FULLTIME"],
         desc="Viết kịch bản video ngắn có hook, twist và câu chốt. Nhạy trend, biết kể chuyện. Gửi kèm 1 đến 2 kịch bản hoặc video đã làm là điểm cộng.",
         work=["Viết kịch bản video review, video tình huống cho các kênh", "Theo dõi trend TikTok, đề xuất format mới", "Làm việc cùng KOL và editor để video ra đúng ý"]),
    dict(id="tro-ly", title="Trợ lý Giám đốc Vận hành", kinds=["FULLTIME"],
         desc="Ngăn nắp, quản lý deadline tốt, dùng thành thạo Google Sheets, Docs và làm slide. Ưu tiên đã làm trợ lý, hành chính hoặc ở agency.",
         work=["Theo dõi lịch quay, lịch đăng, tiến độ của các kênh", "Làm báo cáo, tổng hợp số liệu, soạn tài liệu", "Hỗ trợ giám đốc làm việc với khách hàng và đối tác"]),
    dict(id="account", title="Account", kinds=["TTS", "CTV", "FULLTIME"],
         desc="Cầu nối giữa nhãn hàng, creator và đội sản xuất. Giao tiếp chuyên nghiệp, xử lý được báo giá và hợp đồng, chịu được áp lực. Biết booking KOL/KOC, quảng cáo TikTok và Facebook là điểm cộng lớn.",
         work=["Tiếp nhận yêu cầu của quán ăn, nhãn hàng, tư vấn kênh và gói", "Lập báo giá, hợp đồng, theo dõi thanh toán", "Điều phối KOL, đội quay, editor để giao video đúng hạn"]),
]
KIND_LABEL = {"TTS": "Thực tập sinh", "CTV": "Cộng tác viên", "FULLTIME": "Toàn thời gian"}
KIND_SCHEMA = {"TTS": "INTERN", "CTV": "CONTRACTOR", "FULLTIME": "FULL_TIME"}

def job_label(j):
    return f"{j['title']} ({'/'.join(j['kinds'])})"

KOL_BENEFITS = [
    ("Bảo trợ bởi MCN của TikTok", "Vitamin là MCN chính thức của TikTok, hỗ trợ bạn làm việc trực tiếp với nền tảng."),
    ("Job từ nhãn hàng lớn", "Kênh làm tốt được giới thiệu job từ các nhãn hàng Vitamin đang hợp tác."),
    ("Báo cáo và định hướng hằng tháng", "Nhận báo cáo số liệu kênh và định hướng nội dung mỗi tháng."),
    ("Sự kiện TikTok và MCN", "Tham gia các hoạt động, sự kiện của TikTok và của MCN."),
    ("Lo giấy tờ, hợp đồng", "Vitamin lo hợp đồng với nhãn hàng, bạn tập trung làm nội dung."),
    ("Hỗ trợ thuế", "Vitamin hỗ trợ kê khai, đóng thuế thu nhập từ job theo quy định."),
]

def job_ld(j):
    d = {"@context": "https://schema.org", "@type": "JobPosting", "title": j["title"],
         "description": "<p>" + E(j["desc"]) + "</p><ul>" + "".join(f"<li>{E(t)}</li>" for t in j["work"]) + "</ul>" + (f"<p>{E(j['pay'])}</p>" if j.get("pay") else ""),
         "datePosted": TODAY, "validThrough": "2026-12-31T23:59", "employmentType": [KIND_SCHEMA[k] for k in j["kinds"]],
         "hiringOrganization": {"@type": "Organization", "name": LEGAL, "sameAs": DOMAIN},
         "jobLocation": {"@type": "Place", "address": {"@type": "PostalAddress", "streetAddress": STREET, "addressLocality": "Bắc Ninh", "addressRegion": "Bắc Ninh", "addressCountry": "VN"}},
         "directApply": True, "url": f"{DOMAIN}/tuyen-dung.html#{j['id']}"}
    if j.get("salary"):
        d["baseSalary"] = {"@type": "MonetaryAmount", "currency": "VND", "value": {"@type": "QuantitativeValue", "value": j["salary"], "unitText": "MONTH"}}
    return d

def careers_page():
    jobs = "".join(f"""<article class="job" id="{j['id']}">
<h3>{E(j['title'])}</h3>
<p class="kinds">{''.join(f'<span>{KIND_LABEL[k]}</span>' for k in j['kinds'])}</p>
<p>{E(j['desc'])}</p>
<ul class="list">{''.join(f'<li>{E(t)}</li>' for t in j['work'])}</ul>
{f'<p class="job-pay"><b>Thu nhập:</b> {E(j["pay"])}</p>' if j.get('pay') else ''}
<p><a href="#ung-tuyen" class="job-apply" data-pos="{E(job_label(j))}">Ứng tuyển vị trí này →</a></p>
</article>""" for j in JOBS)
    kol = "".join(f"<article><h3>{E(t)}</h3><p>{E(d)}</p></article>" for t, d in KOL_BENEFITS)
    boxes = "".join(f'<label class="chk"><input type="checkbox" name="vitri" value="{E(job_label(j))}"> {E(job_label(j))}</label>' for j in JOBS)
    body = f"""<section class="pagehead"><div class="wrap">
<p class="eyebrow">Tuyển dụng · Thực tập sinh · Cộng tác viên · Toàn thời gian</p>
<h1>Ứng tuyển nhân sự và thực tập sinh Vitamin Bắc Ninh</h1>
<p class="lead">Vitamin Bắc Ninh là văn phòng tỉnh của Vitamin Network, MCN chính thức của TikTok, vận hành 18 kênh review tại Bắc Ninh. Làm việc tại văn phòng TP Bắc Ninh, được đào tạo và làm nội dung cho các nhãn hàng như MB Bank, VinFast, Atino.</p>
<p style="margin-top:20px"><a class="btn" href="#ung-tuyen">Ứng tuyển ngay</a></p>
</div></section>
<section class="sec"><div class="wrap">
<h2>Vị trí đang tuyển</h2>
<p class="sub">Chọn được nhiều vị trí trong cùng một hồ sơ.</p>
<div class="jobs jobs-grid">{jobs}</div>
</div></section>
<section class="sec alt" id="ung-tuyen"><div class="wrap narrow">
<h2>Form ứng tuyển</h2>
<p class="sub">Các mục có dấu * là bắt buộc. Bộ phận tuyển dụng phản hồi qua số điện thoại hoặc email trong 2 ngày làm việc.</p>
<form class="apply" id="apply" novalidate>
<label>Tên *<input name="ten" required autocomplete="name" placeholder="Họ và tên"></label>
<label>Email *<input name="email" type="email" required autocomplete="email"></label>
<label>Số điện thoại *<input name="sdt" required inputmode="tel" autocomplete="tel"></label>
<label>Ngày tháng năm sinh *<input name="ngaysinh" type="date" required></label>
<label>Link Facebook hoặc TikTok *<input name="mxh" required inputmode="url"></label>
<label>Sản phẩm mà bạn đã làm hoặc đã đứng hình để mình hiểu hơn về khả năng của bạn &lt;3 *<textarea name="sanpham" rows="3" required placeholder="Dán link video, kênh, bài viết..."></textarea></label>
<fieldset><legend>Bạn muốn ứng tuyển vào những vị trí nào *</legend>{boxes}</fieldset>
<label>CV nha các bạn &lt;3 (điền link drive) *<input name="cv" required inputmode="url" placeholder="Link Google Drive, nhớ mở quyền xem"></label>
<label>Kênh nào đưa bạn đến quyết định Apply vào Vitamin Bắc Ninh *<input name="nguon" required placeholder="TikTok, Facebook, bạn bè giới thiệu, Google..."></label>
<p class="err" id="apply-err" role="alert" hidden>Bạn điền đủ các mục có dấu * và chọn ít nhất một vị trí nhé.</p>
<div class="apply-act"><button type="submit" class="btn" value="mail">Gửi qua email</button><button type="submit" class="btn btn-ghost" value="zalo">Sao chép và gửi qua Zalo</button></div>
<p class="meta" id="apply-ok" role="status" hidden>Đã sao chép hồ sơ. Dán vào khung chat Zalo vừa mở rồi bấm gửi.</p>
<p class="meta">Hoặc gửi trực tiếp: Zalo <a href="{ZALO}" rel="noopener">{PHONE}</a> · Email <a href="mailto:{EMAIL}">{EMAIL}</a></p>
</form>
</div></section>
<section class="sec" id="kol"><div class="wrap">
<h2>Đã có kênh? Gia nhập MCN cùng Vitamin</h2>
<p class="sub">Dành cho Creator, KOL đang có kênh TikTok về ăn uống, đời sống ở Bắc Ninh và lân cận.</p>
<div class="svc svc3">{kol}</div>
</div></section>
<script>
(function(){{
  var f=document.getElementById('apply');
  document.querySelectorAll('[data-pos]').forEach(function(a){{a.addEventListener('click',function(){{
    f.querySelectorAll('input[name=vitri]').forEach(function(c){{if(c.value===a.getAttribute('data-pos'))c.checked=true;}});}});}});
  f.addEventListener('submit',function(e){{
    e.preventDefault();
    var d=new FormData(f), how=(e.submitter&&e.submitter.value)||'mail', pos=d.getAll('vitri');
    var need=['ten','email','sdt','ngaysinh','mxh','sanpham','cv','nguon'];
    var miss=need.some(function(k){{return !(d.get(k)||'').trim();}})||!pos.length;
    var err=document.getElementById('apply-err'); err.hidden=!miss; if(miss)return;
    var L=['ỨNG TUYỂN VITAMIN BẮC NINH','Tên: '+d.get('ten'),'Email: '+d.get('email'),'SĐT: '+d.get('sdt'),'Ngày sinh: '+d.get('ngaysinh'),'Facebook/TikTok: '+d.get('mxh'),'Sản phẩm: '+d.get('sanpham'),'Vị trí: '+pos.join(', '),'CV: '+d.get('cv'),'Biết đến qua: '+d.get('nguon')];
    var txt=L.join(String.fromCharCode(10));
    if(how==='zalo'){{
      var done=function(){{document.getElementById('apply-ok').hidden=false;window.open('{ZALO}','_blank','noopener');}};
      try{{navigator.clipboard.writeText(txt).then(done,done);}}catch(_){{done();}}
    }} else {{
      location.href='mailto:{EMAIL}?subject='+encodeURIComponent('Ứng tuyển '+pos.join(', ')+' - '+d.get('ten'))+'&body='+encodeURIComponent(txt);
    }}
  }});
}})();
</script>"""
    return page("tuyen-dung.html", "Tuyển dụng nhân sự, thực tập sinh tại Bắc Ninh | Vitamin Bắc Ninh",
                "Vitamin Bắc Ninh tuyển KOC/KOL, Content Creator, Video Editor, Biên kịch, Trợ lý Giám đốc Vận hành, Account. Nhận thực tập sinh, cộng tác viên, toàn thời gian tại TP Bắc Ninh.",
                body, [job_ld(j) for j in JOBS])

def contact_page():
    body = f"""<section class="pagehead"><div class="wrap">
<p class="eyebrow">Liên hệ</p>
<h1>Liên hệ booking review Bắc Ninh</h1>
<p class="lead">Nhắn Zalo tên quán, địa chỉ và ngân sách, Vitamin Bắc Ninh gửi đề xuất kênh trong ngày.</p>
</div></section>
<section class="sec"><div class="wrap">
<div class="contact">
<div class="card"><h3>Hotline / Zalo</h3><p class="big"><a href="tel:{PHONE_INTL}">{PHONE}</a></p><p><a class="btn" href="{ZALO}" rel="noopener">Nhắn Zalo</a></p></div>
<div class="card"><h3>Văn phòng</h3><p>{E(ADDR)}</p><p><a href="{MAPS}" rel="noopener">Mở Google Maps</a></p></div>
<div class="card"><h3>Pháp nhân</h3><p>{E(LEGAL)}</p><p>Mã số thuế: {MST}</p></div>
</div>
<h2>Cần gửi gì khi liên hệ</h2>
<ul class="list"><li>Tên quán hoặc thương hiệu, địa chỉ</li><li>Món, sản phẩm muốn giới thiệu</li><li>Ngân sách dự kiến và thời gian muốn đăng</li></ul>
</div></section>"""
    return page("lien-he.html", "Liên hệ Vitamin Bắc Ninh – Hotline 0389 799 192",
                "Liên hệ Vitamin Bắc Ninh: Số 118 Phương Vỹ, phường Vũ Ninh, tỉnh Bắc Ninh. Hotline/Zalo 0389 799 192. Booking review TikTok, KOL/KOC, xây kênh.",
                body)

def llms_txt():
    lines = [f"# {BRAND}", "",
             f"> {BRAND} ({LEGAL}, MST {MST}) vận hành hệ thống 18 kênh review TikTok, Facebook, YouTube tại Bắc Ninh, nhận booking review quán ăn, cửa hàng, booking KOL/KOC, xây kênh TikTok và sản xuất video quảng cáo. Địa chỉ: {ADDR}. Hotline/Zalo: {PHONE}.", "",
             "## Bảng giá booking theo gói (chưa VAT)"]
    for p in PACKAGES:
        lines.append(f"- {p['name']}: {vnd(p['price'])}, {p['n']} kênh chính" + (f" + {len(p['sat'])} kênh vệ tinh" if p['sat'] else "") + f", cam kết {p['views']} view sau 1 tuần. Kênh: {', '.join(p['channels'])}.")
    lines += ["", "## Booking lẻ từng kênh (giá/video)"]
    for (n, lo, hi, g, f, l) in CHANNELS:
        lines.append(f"- {n}: {price_range(lo, hi)}")
    lines += ["", "## Trang", f"- [Bảng giá]({DOMAIN}/bang-gia.html)", f"- [Hệ thống kênh]({DOMAIN}/he-thong-kenh.html)", f"- [Khách hàng]({DOMAIN}/khach-hang.html)", f"- [Tuyển dụng]({DOMAIN}/tuyen-dung.html)", f"- [Liên hệ]({DOMAIN}/lien-he.html)", ""]
    return "\n".join(lines)

def main(out):
    os.makedirs(out, exist_ok=True)
    pages = {"index.html": index_page(), "bang-gia.html": price_page(), "he-thong-kenh.html": channels_page(), "khach-hang.html": clients_page(), "tuyen-dung.html": careers_page(), "lien-he.html": contact_page()}
    for k, v in pages.items():
        open(os.path.join(out, k), "w", encoding="utf-8").write(v)
    open(os.path.join(out, "robots.txt"), "w").write(f"User-agent: *\nAllow: /\n\nSitemap: {DOMAIN}/sitemap.xml\n")
    urls = "".join(f"<url><loc>{DOMAIN}/{'' if k == 'index.html' else k}</loc><lastmod>{TODAY}</lastmod></url>" for k in pages)
    open(os.path.join(out, "sitemap.xml"), "w").write(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{urls}</urlset>\n')
    open(os.path.join(out, "llms.txt"), "w", encoding="utf-8").write(llms_txt())
    # bản xem trước cho Artifact: trang chủ không có khung doctype
    open(os.path.join(out, "_preview_index.html"), "w", encoding="utf-8").write(index_page(full=False))

if __name__ == "__main__":
    main(sys.argv[1])
