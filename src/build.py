# -*- coding: utf-8 -*-
"""Builder for the B1 English Speaking Topics resource (bilingual EN/AR).

Reorganizes vocabulary from three source PDFs into thematic speaking topics
for a B1 learner. Emits a single static, theme-aware, responsive HTML file.
"""
import html
from content import (TOPICS, VERBS3, TENSES, TO_INF, GERUND, BOTH_PATTERN,
                     EXPRESSIONS, PHRASE_SITUATIONS, SYNONYMS)


def e(s):
    return html.escape(str(s), quote=True)


def render_vocab_item(en, arb):
    return (
        '<div class="voc s-item" data-text="%s %s">'
        '<span class="voc-en">%s</span>'
        '<span class="voc-ar" dir="rtl" lang="ar">%s</span>'
        '</div>'
    ) % (e(en.lower()), e(arb), e(en), e(arb))


def render_topic(t):
    p = []
    level_badge = ('<span class="chip-level">%s</span>' % e(t["level"])) if t.get("level") else ""
    p.append('<details class="topic" id="%s" open>' % e(t["id"]))
    p.append('<summary class="topic-head">')
    p.append('<span class="topic-num">%02d</span>' % t["num"])
    p.append('<span class="topic-titles">')
    p.append('<span class="topic-en">%s %s</span>' % (e(t["en"]), level_badge))
    p.append('<span class="topic-ar" dir="rtl" lang="ar">%s</span>' % e(t["ar"]))
    p.append('</span>')
    p.append('<span class="topic-toggle" aria-hidden="true">+</span>')
    p.append('</summary>')
    p.append('<div class="topic-body">')
    p.append('<p class="talk" dir="rtl" lang="ar"><span class="talk-ic" aria-hidden="true">🗣️</span>%s</p>' % e(t["talk"]))

    for label_en, label_ar, items in t["groups"]:
        pos = label_en.split()[0].lower()
        p.append('<div class="vgroup">')
        p.append(
            '<h4 class="vgroup-h"><span class="pos-dot pos-%s"></span>'
            '%s <span class="vgroup-ar" dir="rtl" lang="ar">%s</span></h4>'
            % (pos, e(label_en), e(label_ar))
        )
        p.append('<div class="voc-grid">')
        for en, arb in items:
            p.append(render_vocab_item(en, arb))
        p.append('</div></div>')

    p.append('<div class="block block-phrase">')
    p.append('<h4 class="block-h"><span class="block-ic">💬</span>Useful phrases '
             '<span class="block-ar" dir="rtl" lang="ar">جُمل مفيدة</span></h4>')
    p.append('<ul class="phrase-list">')
    for en, arb in t["phrases"]:
        p.append(
            '<li class="s-item" data-text="%s %s"><span class="ph-en">%s</span>'
            '<span class="ph-ar" dir="rtl" lang="ar">%s</span></li>'
            % (e(en.lower()), e(arb), e(en), e(arb))
        )
    p.append('</ul></div>')

    p.append('<div class="block block-practice">')
    p.append('<h4 class="block-h"><span class="block-ic">🎯</span>Speaking practice '
             '<span class="block-ar" dir="rtl" lang="ar">تدرَّب على الكلام</span></h4>')
    p.append('<ol class="q-list">')
    for en, arb in t["questions"]:
        p.append(
            '<li class="s-item" data-text="%s %s"><span class="q-en">%s</span>'
            '<span class="q-ar" dir="rtl" lang="ar">%s</span></li>'
            % (e(en.lower()), e(arb), e(en), e(arb))
        )
    p.append('</ol></div>')

    p.append('</div></details>')
    return "\n".join(p)


def render_verbs3():
    rows = []
    for base, past, pp, arb in VERBS3:
        rows.append(
            '<tr class="s-item" data-text="%s %s %s %s">'
            '<td class="vb">%s</td><td>%s</td><td>%s</td>'
            '<td class="vb-ar" dir="rtl" lang="ar">%s</td></tr>'
            % (e(base), e(past), e(pp), e(arb), e(base), e(past), e(pp), e(arb))
        )
    return (
        '<div class="table-wrap"><table class="vtable">'
        '<thead><tr><th>Base</th><th>Past</th><th>Past participle</th>'
        '<th dir="rtl" lang="ar">المعنى</th></tr></thead>'
        '<tbody>%s</tbody></table></div>'
    ) % "".join(rows)


def render_tenses():
    cards = []
    for en, arb, use, struct, exs in TENSES:
        ex_html = "".join('<code>%s</code>' % e(x) for x in exs)
        cards.append(
            '<div class="tense s-item" data-text="%s %s %s">'
            '<div class="tense-top"><h4>%s</h4>'
            '<span class="tense-ar" dir="rtl" lang="ar">%s</span></div>'
            '<p class="tense-use" dir="rtl" lang="ar">%s</p>'
            '<p class="tense-struct">%s</p>'
            '<div class="tense-ex">%s</div></div>'
            % (e(en.lower()), e(struct.lower()), e(arb),
               e(en), e(arb), e(use), e(struct), ex_html)
        )
    return '<div class="tense-grid">%s</div>' % "".join(cards)


def render_pattern_list(items, cls):
    lis = []
    for verb, ex in items:
        lis.append(
            '<li class="s-item" data-text="%s %s"><span class="pat-v">%s</span>'
            '<code>%s</code></li>' % (e(verb.lower()), e(ex.lower()), e(verb), e(ex))
        )
    return '<ul class="pat-list %s">%s</ul>' % (cls, "".join(lis))


def render_both():
    lis = []
    for label, ex, arb in BOTH_PATTERN:
        lis.append(
            '<li class="s-item" data-text="%s %s"><code>%s</code>'
            '<span class="both-ar" dir="rtl" lang="ar">%s</span></li>'
            % (e(ex.lower()), e(arb), e(ex), e(arb))
        )
    return '<ul class="both-list">%s</ul>' % "".join(lis)


def render_expressions():
    lis = []
    for en, arb in EXPRESSIONS:
        lis.append('<li><code>%s</code><span dir="rtl" lang="ar">%s</span></li>' % (e(en), e(arb)))
    return '<ul class="expr-list">%s</ul>' % "".join(lis)


def render_phrase_situations():
    out = []
    for en, arb, items in PHRASE_SITUATIONS:
        out.append('<div class="sit">')
        out.append('<h4 class="sit-h">%s <span dir="rtl" lang="ar">%s</span></h4>' % (e(en), e(arb)))
        out.append('<ul class="phrase-list">')
        for pe, pa in items:
            out.append(
                '<li class="s-item" data-text="%s %s"><span class="ph-en">%s</span>'
                '<span class="ph-ar" dir="rtl" lang="ar">%s</span></li>'
                % (e(pe.lower()), e(pa), e(pe), e(pa))
            )
        out.append('</ul></div>')
    return "".join(out)


def render_synonyms():
    rows = []
    for word, syn, arb in SYNONYMS:
        rows.append(
            '<tr class="s-item" data-text="%s %s %s">'
            '<td class="syn-w">%s</td><td class="syn-s">%s</td>'
            '<td class="syn-ar" dir="rtl" lang="ar">%s</td></tr>'
            % (e(word), e(syn.lower()), e(arb), e(word), e(syn), e(arb))
        )
    return (
        '<div class="table-wrap"><table class="vtable syn-table">'
        '<thead><tr><th>Word</th><th>Synonyms</th>'
        '<th dir="rtl" lang="ar">المعنى</th></tr></thead>'
        '<tbody>%s</tbody></table></div>'
    ) % "".join(rows)


def render_toc():
    toc = []
    for t in TOPICS:
        lvl = ' <em>%s</em>' % e(t["level"]) if t.get("level") else ""
        toc.append(
            '<a class="toc-chip" href="#%s"><span class="toc-num">%02d</span>'
            '<span class="toc-tt"><span class="toc-en">%s%s</span>'
            '<span class="toc-ar" dir="rtl" lang="ar">%s</span></span></a>'
            % (e(t["id"]), t["num"], e(t["en"]), lvl, e(t["ar"]))
        )
    ref_chips = [
        ('ref-verbs', 'Essential Verbs', 'أهم الأفعال'),
        ('ref-tenses', 'Tenses', 'الأزمنة'),
        ('ref-patterns', 'Verb Patterns', 'to + فعل / ‏ing'),
        ('ref-phrases', 'Speaking Phrases', 'جُمل للتحدث'),
        ('ref-synonyms', 'Synonyms', 'المترادفات'),
    ]
    for rid, ren, rar in ref_chips:
        toc.append(
            '<a class="toc-chip toc-ref" href="#%s">'
            '<span class="toc-tt"><span class="toc-en">%s</span>'
            '<span class="toc-ar" dir="rtl" lang="ar">%s</span></span></a>'
            % (e(rid), e(ren), e(rar))
        )
    return "\n".join(toc)


def build():
    with open("assets/style.css", encoding="utf-8") as f:
        css = f.read()
    with open("assets/app.js", encoding="utf-8") as f:
        js = f.read()
    with open("assets/template.html", encoding="utf-8") as f:
        tpl = f.read()

    total_words = sum(len(items) for t in TOPICS for _, _, items in t["groups"])

    repl = {
        "__CSS__": css,
        "__JS__": js,
        "__TOC__": render_toc(),
        "__TOPICS__": "\n".join(render_topic(t) for t in TOPICS),
        "__VERBS3__": render_verbs3(),
        "__TENSES__": render_tenses(),
        "__TO_INF__": render_pattern_list(TO_INF, "pat-to"),
        "__GERUND__": render_pattern_list(GERUND, "pat-ing"),
        "__BOTH__": render_both(),
        "__EXPR__": render_expressions(),
        "__PHRASES__": render_phrase_situations(),
        "__SYNONYMS__": render_synonyms(),
        "__TOTAL_WORDS__": str(total_words),
        "__N_TOPICS__": str(len(TOPICS)),
    }
    out = tpl
    for k, v in repl.items():
        out = out.replace(k, v)
    return out


STANDALONE_HEAD = (
    '<!doctype html>\n'
    '<html lang="en" dir="ltr">\n<head>\n'
    '<meta charset="utf-8">\n'
    '<meta name="viewport" content="width=device-width, initial-scale=1">\n'
    '<meta name="description" content="B1 English speaking topics — all your '
    'vocabulary organized into themes (English + Arabic), with phrases, '
    'questions, verbs, tenses and synonyms.">\n'
    '<title>Speak B1 — English Speaking Topics (EN/AR)</title>\n'
    '<style>*{margin:0}</style>\n'
    '</head>\n<body>\n'
)
STANDALONE_TAIL = '\n</body>\n</html>\n'

if __name__ == "__main__":
    doc = build()
    # Artifact version: content-only (Artifact provides the html/head/body shell).
    with open("B1_Speaking_Topics.html", "w", encoding="utf-8") as f:
        f.write(doc)
    # Standalone version for the repo: a complete, openable HTML document.
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(STANDALONE_HEAD + doc + STANDALONE_TAIL)
    print("Wrote B1_Speaking_Topics.html (%d bytes) + index.html" % len(doc))
