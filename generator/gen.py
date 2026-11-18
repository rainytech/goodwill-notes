import os, sys, json, shutil, html, datetime
sys.path.insert(0, os.path.dirname(__file__))
from data import COURSES, CH

BASE = "https://notes.goodwillonlinetuition.com"
OUT = sys.argv[1]
GULF_URL = "https://goodwill-plus-two-gulf.netlify.app/"
WA = "https://wa.me/919567902805"
MONTHS = "January February March April May June July August September October November December".split()
e = html.escape

def nice(d):
    y, m, dd = d.split("-")
    return f"{int(dd)} {MONTHS[int(m)-1]} {y}"
def short(d):
    y, m, dd = d.split("-")
    return f"{int(dd)} {MONTHS[int(m)-1][:3]} {y}"
def drive(i): return f"https://drive.google.com/file/d/{i}/view"

course_by = {c["slug"]: c for c in COURSES}
for c in COURSES:
    c["chapters"] = [x for x in CH if x["course"] == c["slug"]]
    c["npdf"] = sum(len(x["pdfs"]) for x in c["chapters"]) + len(c["extras"])

CSS = open(os.path.join(os.path.dirname(__file__), "style.css")).read()

def page(path, title, desc, body, crumbs, depth, ld_extra=None):
    """path: '' for home or 'a/b/' ; depth: number of dirs below root"""
    up = "../" * depth
    canon = BASE + "/" + path
    ld = [{"@context": "https://schema.org", "@type": "BreadcrumbList",
           "itemListElement": [{"@type": "ListItem", "position": i+1, "name": n, "item": BASE + "/" + p}
                               for i, (n, p) in enumerate(crumbs)]}]
    if ld_extra: ld.append(ld_extra)
    nav = ""
    if len(crumbs) > 1:
        parts = []
        for i, (n, p) in enumerate(crumbs):
            if i == len(crumbs) - 1: parts.append(f'<span aria-current="page">{e(n)}</span>')
            else: parts.append(f'<a href="{up}{p}index.html">{e(n)}</a>')
        nav = '<nav class="crumbs" aria-label="Breadcrumb">' + " › ".join(parts) + "</nav>"
    return f"""<!doctype html>
<html lang="en-IN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{e(title)}</title>
<meta name="claude:viewport-fit-sides" content="cover">
<meta name="description" content="{e(desc)}">
<link rel="canonical" href="{canon}">
<meta property="og:type" content="website">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:url" content="{canon}">
<meta property="og:site_name" content="Goodwill Tuition Centre – Study Materials">
<link rel="stylesheet" href="{up}style.css">
<script type="application/ld+json">{json.dumps(ld if len(ld) > 1 else ld[0], ensure_ascii=False)}</script>
</head>
<body>
<div class="wrap">
<header class="site">
  <a class="brand" href="{up}index.html">Goodwill Tuition Centre <span>Study Materials</span></a>
  <a class="main" href="https://www.goodwillonlinetuition.com/">goodwillonlinetuition.com</a>
</header>
{nav}
{body}
<div class="cta">
  <h2>Want this explained one-to-one?</h2>
  <p>Live online classes with Rainy Sir on Zoom. Book a paid demo class on WhatsApp.</p>
  <a class="wa" href="{WA}" target="_blank" rel="noopener">Chat on WhatsApp</a>
  <small>WhatsApp: +91 95679 02805</small>
</div>
<footer>Goodwill Tuition Centre for Accountancy &amp; Income Tax Online · Thevara, Ernakulam, Kerala · Since 1999<br>
<a href="https://www.goodwillonlinetuition.com/">Main website</a> · <a href="{up}index.html">All study materials</a></footer>
</div>
</body>
</html>
"""

def pdf_list(pdfs):
    out = ['<ul class="pdfs">']
    newest = max(p[3] for p in pdfs) if pdfs else ""
    for (i, t, d, dt, tag) in sorted(pdfs, key=lambda p: p[3], reverse=True):
        tags = ""
        if tag: tags += f' <span class="tag">{e(tag)}</span>'
        out.append(f"""<li><div><h3>{e(t)}{tags}</h3><p>{e(d)} <span class="date">Added {short(dt)}</span></p></div>
<a class="open" href="{drive(i)}" target="_blank" rel="noopener">Open PDF</a></li>""")
    out.append("</ul>")
    return "\n".join(out)

def gulf_box(depth):
    return f"""<aside class="gulf"><b>Studying in a CBSE school in the UAE, Qatar, Saudi Arabia, Kuwait, Oman or Bahrain?</b>
<p>Rainy Sir teaches Gulf students live on Zoom, one-to-one, from 4:30 to 8:30 pm IST (3:00 to 7:00 pm UAE time). <a href="{GULF_URL}" target="_blank" rel="noopener">See classes for Gulf students</a></p></aside>"""

CASHFLOW_EX = open(os.path.join(os.path.dirname(__file__), "ex_cashflow.html")).read()

files = {}
# ---------- chapter pages ----------
for x in CH:
    c = course_by[x["course"]]
    path = f'{c["slug"]}/{x["slug"]}/'
    last = max(p[3] for p in x["pdfs"])
    siblings = [y for y in c["chapters"] if y is not x]
    sib = "".join(f'<li><a href="../{y["slug"]}/index.html">{e(y["h1"].split(" – ",1)[-1].replace(" (PDF)",""))}</a></li>' for y in siblings)
    body = f"""<h1>{e(x["h1"])}</h1>
<p class="lede">{e(x["intro"])} Each PDF was prepared by Rainy Sir from real one-to-one online classes. No sign-in is needed.</p>
<div class="facts">
  <div><span>Course</span><b>{e(c["short"])}</b></div>
  <div><span>Solved PDFs</span><b>{len(x["pdfs"])}</b></div>
  <div><span>Prepared by</span><b>Rainy Sir, Goodwill</b></div>
  <div><span>Last updated</span><b>{nice(last)}</b></div>
</div>
<h2>Solved PDFs in this chapter</h2>
{pdf_list(x["pdfs"])}
{CASHFLOW_EX if x.get("example") == "cashflow" else ""}
<section class="miss"><h2>Points students often miss</h2><ul>{"".join(f"<li>{e(p)}</li>" for p in x["points"])}</ul></section>
{gulf_box(2) if c["gulf"] else ""}
{f'<h2>Other chapters in {e(c["name"])}</h2><ul class="chapters">{sib}</ul>' if sib else ""}
<p class="back"><a href="../index.html">← All {e(c["name"])} materials</a></p>"""
    ld = {"@context": "https://schema.org", "@type": "CollectionPage", "name": x["h1"], "description": x["desc"],
          "url": BASE + "/" + path, "inLanguage": "en-IN", "dateModified": last,
          "publisher": {"@type": "EducationalOrganization", "name": "Goodwill Tuition Centre for Accountancy & Income Tax Online",
                        "url": "https://www.goodwillonlinetuition.com/", "telephone": "+91-9567902805"},
          "hasPart": [{"@type": "LearningResource", "name": t, "url": drive(i), "encodingFormat": "application/pdf",
                       "learningResourceType": "Solved questions", "educationalLevel": c["short"]} for (i, t, d, dt, tag) in x["pdfs"]]}
    files[path + "index.html"] = (page(path, x["title"] + " | Goodwill", x["desc"], body,
        [("Study Materials", ""), (c["name"], c["slug"] + "/"), (x["h1"].split(" – ", 1)[-1].replace(" (PDF)", ""), path)], 2, ld), last)

# ---------- course pages ----------
for c in COURSES:
    path = c["slug"] + "/"
    rows = []
    lasts = []
    for x in c["chapters"]:
        last = max(p[3] for p in x["pdfs"]); lasts.append(last)
        name = x["h1"].split(" – ", 1)[-1].replace(" (PDF)", "")
        rows.append(f'<li><a href="{x["slug"]}/index.html"><b>{e(name)}</b><span>{len(x["pdfs"])} solved PDFs · updated {short(last)}</span></a></li>')
    extra = ""
    if c["extras"]:
        lasts += [p[3] for p in c["extras"]]
        extra = "<h2>More from this course</h2>" + pdf_list(c["extras"])
    links = ""
    if c.get("links"):
        links = '<h2>Related pages on the main website</h2><ul class="chapters">' + "".join(
            f'<li><a href="{u}" target="_blank" rel="noopener">{e(t)}</a></li>' for u, t in c["links"]) + "</ul>"
    body = f"""<h1>{e(c["name"])} – Solved Questions and Notes (PDF)</h1>
<p class="lede">{e(c["blurb"])} Pick a chapter below. Every PDF opens straight away, with no sign-in.</p>
<h2>Chapters</h2>
<ul class="chlist">{"".join(rows)}</ul>
{extra}
{links}
{gulf_box(1) if c["gulf"] else ""}"""
    desc = f'{c["name"]} solved questions PDF, chapter by chapter: {c["blurb"]}'
    files[path + "index.html"] = (page(path, f'{c["name"]} Solved Questions PDF | Goodwill', desc[:300], body,
        [("Study Materials", ""), (c["name"], path)], 1), max(lasts))

# ---------- home ----------
allp = []
for x in CH:
    for p in x["pdfs"]:
        allp.append((p, x, course_by[x["course"]]))
allp.sort(key=lambda r: r[0][3], reverse=True)
recent = "".join(f'<li><a href="{c["slug"]}/{x["slug"]}/index.html"><b>{e(p[1])}</b><span>{e(c["short"])} · {short(p[3])}</span></a></li>' for p, x, c in allp[:8])
cards = "".join(f'<li><a href="{c["slug"]}/index.html"><b>{e(c["name"])}</b><span>{e(c["blurb"])}</span><em>{len(c["chapters"])} chapters · {c["npdf"]} PDFs</em></a></li>' for c in COURSES)
total = sum(c["npdf"] for c in COURSES)
body = f"""<div class="hero">
<p class="eyebrow">Rainy Goodwill · Teaching accountancy since 1999</p>
<h1>Accountancy Study Materials – Solved Questions in PDF</h1>
<p>{total} solved PDFs from real one-to-one online classes, for CBSE Class 11 and 12, Kerala Plus Two, MGU B.Com Honours, Mumbai University B.Com and Amity BBA. New solutions are added every evening. No sign-in is needed.</p>
</div>
<h2>Choose your course</h2>
<ul class="courses">{cards}</ul>
<h2>Recently added</h2>
<ul class="chlist">{recent}</ul>
{gulf_box(0)}"""
files["index.html"] = (page("", "Accountancy Study Materials – Solved Questions PDF | Goodwill Tuition Centre",
    f"{total} solved accountancy PDFs for CBSE Class 11 and 12, Kerala Plus Two, MGU B.Com, Mumbai B.Com and Amity BBA, by Goodwill Tuition Centre, Ernakulam.",
    body, [("Study Materials", "")], 0), max(r[0][3] for r in allp))

# ---------- write ----------
if os.path.exists(OUT): shutil.rmtree(OUT)
for rel, (txt, _) in files.items():
    fp = os.path.join(OUT, rel); os.makedirs(os.path.dirname(fp), exist_ok=True)
    open(fp, "w").write(txt)
open(os.path.join(OUT, "style.css"), "w").write(CSS)
sm = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
for rel, (_, last) in sorted(files.items()):
    loc = BASE + "/" + rel.replace("index.html", "")
    sm.append(f"  <url><loc>{loc}</loc><lastmod>{last}</lastmod></url>")
sm.append("</urlset>")
open(os.path.join(OUT, "sitemap.xml"), "w").write("\n".join(sm) + "\n")
open(os.path.join(OUT, "robots.txt"), "w").write(f"User-agent: *\nAllow: /\nSitemap: {BASE}/sitemap.xml\n")
open(os.path.join(OUT, "404.html"), "w").write(page("404", "Page not found | Goodwill Study Materials", "Page not found.",
    '<h1>Page not found</h1><p class="lede">This page has moved. <a href="/index.html">Open all study materials</a>.</p>', [("Study Materials", "")], 0).replace('href="style.css"', 'href="/style.css"'))
open(os.path.join(OUT, "CNAME"), "w").write("notes.goodwillonlinetuition.com\n")
open(os.path.join(OUT, ".nojekyll"), "w").write("")
print(len(files), "pages,", total, "PDFs")
