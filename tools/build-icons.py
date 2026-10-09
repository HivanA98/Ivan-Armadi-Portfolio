"""Rebuild the Font Awesome subset this site self-hosts.

Run after adding or removing an icon in index.html, 404.html or
assets/js/main.js, otherwise a new icon renders as a blank box:

    pip install "fonttools[woff]"
    python tools/build-icons.py

Writes assets/css/icons.css and assets/webfonts/*.subset.woff2.
"""
import io, os, re, urllib.request

os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
CDN = 'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/'


def get(url, binary=False):
    """Fetch url, retrying if the body comes back short of Content-Length."""
    for attempt in range(4):
        r = urllib.request.urlopen(urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'}), timeout=120)
        expected = r.headers.get('Content-Length')
        data = r.read()
        if expected is None or len(data) == int(expected):
            return data if binary else data.decode()
        print(f'    unduhan terpotong ({len(data)}/{expected}), ulangi...')
    raise IOError('gagal mengunduh utuh: ' + url)


css = get(CDN + 'css/all.min.css')

# name -> codepoint, from rules like .fa-wrench:before{content:"\f0ad"}
# selectors may be comma-separated, so grab the whole list then pull each name
name2cp = {}
for sel, cp in re.findall(r'([^{}]+)\{\s*content\s*:\s*"\\([0-9a-f]+)"\s*;?\s*\}', css):
    for n in re.findall(r'\.fa-([a-z0-9-]+):{1,2}before', sel):
        name2cp.setdefault(n, int(cp, 16))
print('peta ikon dari CSS:', len(name2cp))

# main.js injects icons at runtime (hamburger, back-to-top), so scan it too or
# those glyphs get subsetted away and render as blank boxes.
sources = ''.join(open(f, encoding='utf-8').read()
                  for f in ['index.html', '404.html', 'assets/js/main.js'])
used = re.findall(r'\bfa([sbr])\s+fa-([a-z0-9-]+)', sources)
style_family = {'s': 'solid', 'r': 'regular', 'b': 'brands'}

need = {'solid': set(), 'regular': set(), 'brands': set()}
missing = []
for sfx, name in used:
    cp = name2cp.get(name)
    if cp is None:
        missing.append(name)
        continue
    need[style_family[sfx]].add(cp)

# codepoints used by CSS pseudo-elements (Font Awesome 6 Free, weight 900 = solid)
for m in re.findall(r"content:\s*'\\([0-9a-f]+)'", open('assets/css/style.css', encoding='utf-8').read()):
    need['solid'].add(int(m, 16))

assert not missing, 'ikon tidak ditemukan: %s' % missing
for k, v in need.items():
    print(f'  {k}: {len(v)} glyph')

FONTS = {'solid': ('fa-solid-900', 'Font Awesome 6 Free', 900),
         'regular': ('fa-regular-400', 'Font Awesome 6 Free', 400),
         'brands': ('fa-brands-400', 'Font Awesome 6 Brands', 400)}

os.makedirs('assets/webfonts', exist_ok=True)
from fontTools import subset as fsubset
from fontTools.ttLib import TTFont

face_css = []
total_before = total_after = 0
for style, cps in need.items():
    if not cps:
        continue
    base, family, weight = FONTS[style]
    # fontTools cannot parse fa-regular-400.woff2 (same error from every CDN),
    # so fall back to the TTF, which carries the same glyphs.
    out = f'assets/webfonts/{base}.subset.woff2'
    font = raw = None
    for ext in ('woff2', 'ttf'):
        candidate = get(CDN + f'webfonts/{base}.{ext}', binary=True)
        try:
            font = TTFont(io.BytesIO(candidate))
            font['glyf']  # force decompile so a bad table fails here
            raw = candidate
            if ext != 'woff2':
                print(f'    {base}: woff2 tidak terbaca, memakai {ext}')
            break
        except Exception:
            font = None
    assert font is not None, 'tidak bisa membaca font sumber: ' + base
    opts = fsubset.Options()
    opts.layout_features = []
    opts.hinting = False
    opts.desubroutinize = True
    opts.notdef_outline = True
    opts.name_IDs = '*'
    opts.drop_tables += ['DSIG']
    subsetter = fsubset.Subsetter(options=opts)
    subsetter.populate(unicodes=sorted(cps))
    subsetter.subset(font)
    font.flavor = 'woff2'
    with open(out, 'wb') as fh:
        font.save(fh)
    font.close()

    # fail loudly rather than shipping a font that renders as blank boxes
    check = TTFont(out)
    have = set()
    for sub in check['cmap'].tables:
        if sub.isUnicode():
            have |= set(sub.cmap)
    check.close()
    assert cps <= have, 'glyph hilang di %s: %s' % (out, sorted(cps - have))

    before, after = len(raw), os.path.getsize(out)
    total_before += before
    total_after += after
    print(f'  {base}: {before/1024:.0f} KB -> {after/1024:.1f} KB')
    face_css.append(
        '@font-face {\n'
        f'  font-family: "{family}";\n'
        '  font-style: normal;\n'
        f'  font-weight: {weight};\n'
        '  font-display: block;\n'
        f'  src: url("../webfonts/{base}.subset.woff2") format("woff2");\n'
        '}')

# icon classes actually used
rules = []
for sfx, name in sorted(set(used)):
    rules.append('.fa-%s::before { content: "\\%x"; }' % (name, name2cp[name]))

out_css = '''/*!
 * Font Awesome Free 6.4.0 - https://fontawesome.com
 * Icons: CC BY 4.0 - Fonts: SIL OFL 1.1 - License: https://fontawesome.com/license/free
 *
 * Subset build: only the glyphs this site uses, self-hosted.
 * Regenerate after adding an icon, or it will render as a blank box.
 */
%s

.fa, .fas, .far, .fab {
  -moz-osx-font-smoothing: grayscale;
  -webkit-font-smoothing: antialiased;
  display: var(--fa-display, inline-block);
  font-style: normal;
  font-variant: normal;
  line-height: 1;
  text-rendering: auto;
}
.fa, .fas { font-family: "Font Awesome 6 Free"; font-weight: 900; }
.far { font-family: "Font Awesome 6 Free"; font-weight: 400; }
.fab { font-family: "Font Awesome 6 Brands"; font-weight: 400; }

%s
''' % ('\n'.join(face_css), '\n'.join(rules))
open('assets/css/icons.css', 'w', encoding='utf-8', newline='\n').write(out_css)

css_size = os.path.getsize('assets/css/icons.css')
print(f'\nwebfont  : {total_before/1024:.0f} KB -> {total_after/1024:.1f} KB')
print(f'CSS      : {len(css.encode())/1024:.0f} KB -> {css_size/1024:.1f} KB')
print(f'TOTAL    : {(total_before+len(css.encode()))/1024:.0f} KB -> {(total_after+css_size)/1024:.1f} KB')
print('aturan ikon:', len(rules))
