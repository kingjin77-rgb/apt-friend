"""아파트친구 — 검색 노출용 메타와 구조화 데이터를 각 페이지에 넣는다.

법무법인 홈페이지의 tools/seo.py 와 같은 방식이다.
<!-- SEO:AUTO --> 와 <!-- /SEO:AUTO --> 사이만 다시 쓰므로
본문을 건드리지 않는다. 표시가 없으면 </head> 앞에 만들어 넣는다.

실행:  python tools/seo.py
"""

from __future__ import annotations

import io
import json
import re
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

for _s in ("stdout", "stderr"):
    _st = getattr(sys, _s)
    if hasattr(_st, "buffer"):
        setattr(sys, _s, io.TextIOWrapper(_st.buffer, encoding="utf-8", errors="replace"))

ROOT = Path(__file__).resolve().parent.parent
KST = timezone(timedelta(hours=9))

# 도메인을 옮길 때 이 값만 바꾸면 전부 따라온다
SITE = "https://kingjin77-rgb.github.io/apt-friend"
SITE_NAME = "아파트친구"
OPERATOR = "법무법인 제이엘"
OPERATOR_URL = "https://kingjin77-rgb.github.io/jl-lawfirm-homepage/"
TEL = "+82-1899-4252"
EMAIL = "jllaw2020@naver.com"
OG_IMAGE = SITE + "/assets/img/og-default.png"

# 페이지별 제목·설명·우선순위. 설명은 검색 결과에 그대로 나가므로
# 마케팅 수식어 없이 무엇을 하는 곳인지만 적는다.
PAGES = {
    "index.html": {
        "title": "아파트친구 | 입주예정자협의회 지원센터",
        "desc": "입주예정자협의회 결성부터 입주자대표회의 인계까지. 위임장 전자접수, 회칙·소집공고문 서식 생성, 단체등기 접수를 무료로 제공합니다. 법무법인 제이엘 운영.",
        "priority": "1.0",
        "changefreq": "weekly",
    },
    "roadmap.html": {
        "title": "협의회 전 과정 26단계 | 아파트친구",
        "desc": "입주예정자협의회 발족부터 해체까지 26단계. 각 단계에서 법무법인이 수행하는 일과 협의회가 준비할 일을 나눠 정리했습니다.",
        "priority": "0.9",
        "changefreq": "monthly",
    },
    "group-registration.html": {
        "title": "단체등기 접수 | 아파트친구",
        "desc": "입주 아파트 단체 소유권이전등기 접수. 단지 단위로 진행하며 아파트명과 연락처만 남기면 법무법인 제이엘 담당 변호사가 절차·일정·비용을 안내합니다.",
        "priority": "0.9",
        "changefreq": "monthly",
    },
    "poa-system.html": {
        "title": "위임장 전자접수 | 아파트친구",
        "desc": "총회 불참 세대의 의결권 위임장을 온라인으로 받습니다. 단지별 접수 페이지를 만들고 세대별 접수 현황을 확인할 수 있습니다.",
        "priority": "0.8",
        "changefreq": "monthly",
    },
    "document-center.html": {
        "title": "협의회 서식 생성 | 아파트친구",
        "desc": "위임장, 회칙, 창립총회 소집공고문, 임원 선출 결과 통지문, 협의회 결성 통지서를 입력만 하면 완성해 드립니다.",
        "priority": "0.8",
        "changefreq": "monthly",
    },
    "start-association.html": {
        "title": "협의회 시작하기 | 아파트친구",
        "desc": "입주예정자협의회가 아직 없는 단지에서 처음 시작하는 방법. 발기인 모집부터 창립총회 소집까지 실무 순서를 정리했습니다.",
        "priority": "0.8",
        "changefreq": "monthly",
    },
    "handover-checklist.html": {
        "title": "입대의 인계 체크리스트 | 아파트친구",
        "desc": "입주예정자협의회가 입주자대표회의로 넘길 때 빠뜨리면 안 되는 조직 서류, 재정 서류, 협상 기록, 운영 자료 목록.",
        "priority": "0.7",
        "changefreq": "monthly",
    },
    "concierge-request.html": {
        "title": "상담 신청 | 아파트친구",
        "desc": "협의회 운영 중 막히는 문제를 법무법인 제이엘 담당 변호사가 검토해 드립니다. 단지 단위 상담은 비용이 발생하지 않습니다.",
        "priority": "0.7",
        "changefreq": "monthly",
    },
}

CRUMBS = {
    "roadmap.html": [("홈", "/"), ("전 과정 26단계", "/roadmap.html")],
    "group-registration.html": [("홈", "/"), ("단체등기 접수", "/group-registration.html")],
    "poa-system.html": [("홈", "/"), ("위임장 접수", "/poa-system.html")],
    "document-center.html": [("홈", "/"), ("서식 생성", "/document-center.html")],
    "start-association.html": [("홈", "/"), ("협의회 시작하기", "/start-association.html")],
    "handover-checklist.html": [("홈", "/"), ("인계 체크리스트", "/handover-checklist.html")],
    "concierge-request.html": [("홈", "/"), ("상담 신청", "/concierge-request.html")],
}

BEGIN, END = "<!-- SEO:AUTO -->", "<!-- /SEO:AUTO -->"


def esc(s: str) -> str:
    return (
        str(s).replace("&", "&amp;").replace("<", "&lt;")
        .replace(">", "&gt;").replace('"', "&quot;")
    )


def url_for(name: str) -> str:
    return SITE + "/" if name == "index.html" else f"{SITE}/{name}"


def organization() -> dict:
    return {
        "@type": "Organization",
        "@id": SITE + "/#organization",
        "name": SITE_NAME,
        "alternateName": "APT FRIEND",
        "url": SITE + "/",
        "image": OG_IMAGE,
        "email": EMAIL,
        "telephone": TEL,
        "description": "입주예정자협의회의 결성과 운영을 돕는 지원센터입니다. 법무법인 제이엘이 운영합니다.",
        "parentOrganization": {"@type": "LegalService", "name": OPERATOR, "url": OPERATOR_URL},
        "areaServed": {"@type": "Country", "name": "대한민국"},
    }


def graph(name: str, conf: dict) -> dict:
    nodes = [
        {
            "@type": "WebSite",
            "@id": SITE + "/#website",
            "url": SITE + "/",
            "name": SITE_NAME,
            "publisher": {"@id": SITE + "/#organization"},
            "inLanguage": "ko-KR",
        },
        organization(),
        {
            "@type": "WebPage",
            "@id": url_for(name) + "#webpage",
            "url": url_for(name),
            "name": conf["title"],
            "description": conf["desc"],
            "isPartOf": {"@id": SITE + "/#website"},
            "about": {"@id": SITE + "/#organization"},
            "inLanguage": "ko-KR",
        },
    ]
    crumbs = CRUMBS.get(name)
    if crumbs:
        nodes.append({
            "@type": "BreadcrumbList",
            "itemListElement": [
                {"@type": "ListItem", "position": i, "name": t,
                 "item": SITE + ("" if u == "/" else u) + ("/" if u == "/" else "")}
                for i, (t, u) in enumerate(crumbs, 1)
            ],
        })
    return {"@context": "https://schema.org", "@graph": nodes}


def block(name: str, conf: dict) -> str:
    u, title, desc = url_for(name), conf["title"], conf["desc"]
    ld = json.dumps(graph(name, conf), ensure_ascii=False, indent=2)
    return "\n".join([
        BEGIN,
        f'<link rel="canonical" href="{u}">',
        '<meta name="robots" content="index, follow, max-image-preview:large">',
        f'<meta property="og:type" content="{"website" if name == "index.html" else "article"}">',
        f'<meta property="og:site_name" content="{esc(SITE_NAME)}">',
        '<meta property="og:locale" content="ko_KR">',
        f'<meta property="og:url" content="{u}">',
        f'<meta property="og:title" content="{esc(title)}">',
        f'<meta property="og:description" content="{esc(desc)}">',
        f'<meta property="og:image" content="{OG_IMAGE}">',
        '<meta name="twitter:card" content="summary_large_image">',
        f'<meta name="twitter:title" content="{esc(title)}">',
        f'<meta name="twitter:description" content="{esc(desc)}">',
        f'<meta name="twitter:image" content="{OG_IMAGE}">',
        f'<meta name="author" content="{esc(OPERATOR)}">',
        '<link rel="icon" href="assets/img/favicon.svg" type="image/svg+xml">',
        '<script type="application/ld+json">',
        ld,
        "</script>",
        END,
    ])


def strip_managed(html: str) -> str:
    """직접 적어 둔 메타는 자동 블록과 겹치므로 걷어낸다."""
    pats = [
        r'\s*<link rel="canonical"[^>]*>',
        r'\s*<meta name="robots"[^>]*>',
        r'\s*<meta property="og:[^"]*"[^>]*>',
        r'\s*<meta name="twitter:[^"]*"[^>]*>',
        r'\s*<meta name="author"[^>]*>',
        r'\s*<link rel="icon"[^>]*>',
    ]
    for p in pats:
        html = re.sub(p, "", html)
    return html


def apply(path: Path, name: str, conf: dict) -> bool:
    html = path.read_text(encoding="utf-8")

    # 제목과 설명은 표준값으로 맞춘다
    html = re.sub(r"<title>.*?</title>", f"<title>{esc(conf['title'])}</title>", html, flags=re.S)
    if re.search(r'<meta name="description"[^>]*>', html):
        html = re.sub(r'<meta name="description"[^>]*>',
                      f'<meta name="description" content="{esc(conf["desc"])}">', html)
    else:
        html = html.replace("</title>",
                            f'</title>\n<meta name="description" content="{esc(conf["desc"])}">', 1)

    new = block(name, conf)
    if BEGIN in html and END in html:
        out = re.sub(re.escape(BEGIN) + r".*?" + re.escape(END), lambda _: new, html, flags=re.S)
    else:
        out = strip_managed(html).replace("</head>", new + "\n</head>", 1)

    if out != html:
        path.write_text(out, encoding="utf-8")
        return True
    return False


def sitemap() -> None:
    today = datetime.now(KST).strftime("%Y-%m-%d")
    rows = []
    for name, conf in PAGES.items():
        rows.append(
            "  <url>\n"
            f"    <loc>{url_for(name)}</loc>\n"
            f"    <lastmod>{today}</lastmod>\n"
            f"    <changefreq>{conf['changefreq']}</changefreq>\n"
            f"    <priority>{conf['priority']}</priority>\n"
            "  </url>"
        )
    (ROOT / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        + "\n".join(rows) + "\n</urlset>\n",
        encoding="utf-8",
    )
    (ROOT / "robots.txt").write_text(
        "User-agent: *\nAllow: /\n\n" f"Sitemap: {SITE}/sitemap.xml\n", encoding="utf-8"
    )


def main() -> int:
    n = 0
    for name, conf in PAGES.items():
        p = ROOT / name
        if not p.exists():
            print(f"건너뜀 — {name} 없음", file=sys.stderr)
            continue
        if apply(p, name, conf):
            print(f"주입 — {name}")
            n += 1
    sitemap()
    print(f"sitemap.xml {len(PAGES)}건 · robots.txt 생성 · 기준 주소 {SITE}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
