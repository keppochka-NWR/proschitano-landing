# -*- coding: utf-8 -*-
"""Сборка статического Pages-лендинга «Просчитано» из mvp/web/index.html:
относительные пути, CTA -> форма заявки (FormSubmit), без ссылок на /app."""
import re, pathlib

MVP = pathlib.Path(r"C:\Users\My PC\Desktop\Claude Project\Агрегатор\mvp\web")
LAND = pathlib.Path(r"C:\Users\My PC\Desktop\Claude Project\Агрегатор\лендинг")

html = (MVP / "index.html").read_text(encoding="utf-8")
# форма заявки берётся из текущего index.html лендинга (FormSubmit), чтобы её не потерять при пересборке
_cur = (LAND / "index.html").read_text(encoding="utf-8")
_fs = _cur.index('<form id="f"'); _fe = _cur.index("</form>", _fs) + 7
form = _cur[_fs:_fe].strip()
# копируем ассеты из mvp
import shutil
(LAND / "assets" / "img").mkdir(parents=True, exist_ok=True)
for n in ("tokens.css", "landing.css", "landing.js"):
    shutil.copy(MVP / "assets" / n, LAND / "assets" / n)
for p in (MVP / "assets" / "img").glob("*.jpg"):
    shutil.copy(p, LAND / "assets" / "img" / p.name)

html = html.replace('"/assets/', '"assets/')
html = html.replace('href="/"', 'href="#top"')
html = html.replace('href="/app"', 'href="#apply"')
html = html.replace("<body>", '<body id="top">', 1)

# финальный блок -> форма заявки
final_re = re.compile(r'<section class="final">.*?</section>', re.S)
final_new = '''<section class="final" id="apply">
  <div class="wrap">
    <h2 class="rv">Отдайте расчёт нам</h2>
    <p class="rv">Первая заявка бесплатная. Оставьте контакт, мы напишем в течение рабочего дня, пришлём анкету и соберём предложения цехов.</p>
    ''' + form + '''
    <p class="form-ok rv" id="formOk" hidden>Заявка ушла. Ответим в течение рабочего дня.</p>
  </div>
</section>'''
html, n = final_re.subn(lambda m: final_new, html, count=1)
assert n == 1, "final section not found"

# подписи ссылок на кабинет
html = html.replace(">Войти в кабинет<", ">Оставить заявку<")
html = html.replace('<a href="#apply">Кабинет</a>', '<a href="#apply">Заявка</a>')

# FormSubmit: после отправки вернуть на страницу с якорем
if "_next" not in html:
    html = html.replace('<input type="hidden" name="_captcha" value="false">',
                        '<input type="hidden" name="_captcha" value="false">\n      <input type="hidden" name="_next" value="https://keppochka-nwr.github.io/proschitano-landing/?sent=1#apply">')

# показать «заявка ушла» по ?sent=1
html = html.replace('<script src="assets/landing.js"></script>',
                    '<script src="assets/landing.js"></script>\n<script>if(location.search.includes("sent=1")){var f=document.getElementById("f"),o=document.getElementById("formOk");if(f)f.hidden=true;if(o)o.hidden=false;}</script>')

assert "/app" not in html, "leftover /app link"
(LAND / "index.html").write_text(html, encoding="utf-8")

# CSS: относительные пути + стили формы под светлую тему
css = (LAND / "assets" / "landing.css").read_text(encoding="utf-8")
css = css.replace('url("/assets/img/', 'url("img/')
if ".final form" not in css:
    css += '''
/* форма заявки (Pages-версия без кабинета) */
.final form{max-width:520px;margin:0 auto;display:grid;gap:16px;text-align:left;
  background:var(--card);border:1px solid var(--line);border-radius:18px;padding:28px;
  box-shadow:0 18px 50px -30px rgba(26,24,21,.35)}
.final .field{display:flex;flex-direction:column;gap:7px}
.final .field label{font-size:14px;color:var(--muted)}
.final .field input,.final .field select{font:inherit;font-size:16px;color:var(--ink);
  background:var(--bg);border:1px solid var(--line);border-radius:10px;padding:12px 14px}
.final .field input:focus,.final .field select:focus{outline:none;border-color:var(--accent)}
.final form .btn{justify-content:center}
.final .form-note{font-size:13px;color:var(--muted);margin:0}
.final .form-ok{font-size:18px;color:var(--accent);font-weight:600}
'''
(LAND / "assets" / "landing.css").write_text(css, encoding="utf-8")
print("ok", len(html))
