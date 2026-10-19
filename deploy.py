"""Turns the artifact pages into a standalone static site for Render.
Output: deploy/ with index.html, john-doe/index.html, jane-doe/index.html, richard-roe/index.html, assets/
"""
import pathlib, shutil, subprocess, sys, re

ROOT = pathlib.Path(__file__).parent
SITE, OUT = ROOT / "site", ROOT / "deploy"
EXT = 'target="_blank" rel="noopener"'

subprocess.run([sys.executable, str(ROOT / "build.py"), "/"], check=True)

if OUT.exists():
    for p in OUT.iterdir():
        if p.name != ".git":
            shutil.rmtree(p) if p.is_dir() else p.unlink()
else:
    OUT.mkdir()
shutil.copytree(SITE / "assets", OUT / "assets")

PAGES = {"index.html": "index.html", "john-doe.html": "john-doe/index.html",
         "jane-doe.html": "jane-doe/index.html", "richard-roe.html": "richard-roe/index.html"}

for src, dst in PAGES.items():
    html = (SITE / src).read_text()
    title = re.search(r"<title>.*?</title>", html, re.S).group(0)
    html = html.replace(title, "", 1)
    html = html.replace('<meta name="claude:viewport-fit-sides" content="cover">\n', "")
    html = html.replace('src="assets/', 'src="/assets/')
    html = html.replace('href="assets/', 'href="/assets/')
    html = html.replace(f'href="/" {EXT}', 'href="/"')  # links back home stay in the same tab
    if src != "index.html":
        title = title.replace("</title>", " | Kenny's International</title>")
    doc = ('<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n'
           '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
           f'{title}\n<link rel="icon" href="/assets/emblem.png">\n</head>\n<body>\n{html}</body>\n</html>\n')
    out = OUT / dst
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(doc)

(OUT / "README.md").write_text(
    "# Kenny's International leadership site\n\n"
    "Static site: a homepage plus one page per director. No build step.\n\n"
    "- `/` homepage\n- `/john-doe/` Marketing Director\n- `/jane-doe/` Sales Director\n- `/richard-roe/` Operations Director\n\n"
    "Render static site settings: build command `echo static`, publish directory `.`\n")
print("deploy ready:", sorted(str(p.relative_to(OUT)) for p in OUT.rglob("*") if p.is_file() and ".git" not in p.parts))
