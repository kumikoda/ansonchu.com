#!/usr/bin/env python3
"""Bake Python syntax highlighting into <pre><code> blocks.

The site ships plain static HTML — no JS, no external requests — so the
highlighting is pre-rendered into spans here rather than done in the browser.

Idempotent: existing spans are stripped before re-highlighting, so it is safe
to run again after editing code in a post.

    python3 tools/highlight.py            # rewrite writing/*.html in place
    python3 tools/highlight.py --check    # report only, change nothing
"""

import argparse
import glob
import html
import re
import sys

from pygments import lex
from pygments.lexers import PythonLexer
from pygments.token import Comment, Keyword, Name, Number, Operator, Punctuation, String

BLOCK = re.compile(r"<pre><code(?P<attrs>[^>]*)>(?P<body>.*?)</code></pre>", re.S)
SPAN = re.compile(r"</?span[^>]*>")

# Pygments token -> short class name. Anything unlisted renders unwrapped, which
# keeps the markup small: plain identifiers are the bulk of the text.
CLASSES = [
    (Comment, "c"),
    (Keyword, "k"),
    (String, "s"),
    (Number, "m"),
    (Name.Function, "f"),
    (Name.Class, "f"),
    (Name.Builtin, "b"),
    (Name.Builtin.Pseudo, "b"),
    (Name.Decorator, "d"),
    (Operator, "o"),
    (Punctuation, "o"),
]


def class_for(token):
    """Most specific matching class, or None to leave the text unwrapped."""
    best = None
    for ttype, cls in CLASSES:
        if token in ttype and (best is None or len(ttype) >= best[0]):
            best = (len(ttype), cls)
    return best[1] if best else None


def highlight(source):
    out = []
    for token, text in lex(source, PythonLexer()):
        if not text:
            continue
        escaped = html.escape(text, quote=False)
        cls = class_for(token)
        out.append(f'<span class="{cls}">{escaped}</span>' if cls else escaped)
    return "".join(out).rstrip("\n")


def normalize(source):
    """Notion exports mixed tabs and spaces, which renders as ragged indent."""
    return "\n".join(line.replace("\t", "    ") for line in source.split("\n"))


def process(path, check):
    original = open(path, encoding="utf-8").read()
    count = 0

    def replace(match):
        nonlocal count
        count += 1
        code = html.unescape(SPAN.sub("", match.group("body")))
        return f'<pre><code class="py">{highlight(normalize(code))}</code></pre>'

    updated = BLOCK.sub(replace, original)
    changed = updated != original
    if changed and not check:
        open(path, "w", encoding="utf-8").write(updated)
    return count, changed


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    parser.add_argument("paths", nargs="*", default=None)
    args = parser.parse_args()

    paths = args.paths or sorted(glob.glob("writing/*.html"))
    total = 0
    dirty = []
    for path in paths:
        count, changed = process(path, args.check)
        if count:
            total += count
            status = "changed" if changed else "up to date"
            print(f"  {path:<48} {count:>3} blocks  {status}")
            if changed:
                dirty.append(path)

    print(f"\n{total} blocks across {len(paths)} files; {len(dirty)} file(s) "
          f"{'would change' if args.check else 'rewritten'}")
    if args.check and dirty:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
