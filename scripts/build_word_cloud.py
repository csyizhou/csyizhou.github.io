"""Regenerate the SVG from the publication title corpus with Python 3."""
from collections import Counter
from html import escape
from pathlib import Path
import math
import re

ROOT = Path(__file__).resolve().parents[1]
CORPUS = ROOT / "scripts/paper-titles.tsv"
OUTPUT = ROOT / "assets/word-cloud.svg"
# Merge spelling variants and keep terms that describe research problems or methods.
TERMS = {
    "Segmentation": r"segmentation",
    "Medical Imaging": r"medical image(?:s| analysis)?",
    "Semi-supervised": r"semi[- ]supervised",
    "Vision–Language": r"vision[- ]language|image[- ]text",
    "Multimodal": r"multi[- ]?modal(?:ity|ities)?",
    "Retinal": r"retinal|fundus|ophthalmic",
    "Reasoning": r"reasoning",
    "Domain Adaptation": r"domain adaptation",
    "Pretraining": r"pre[- ]?training",
    "Continual Learning": r"continual|incremental",
    "Knowledge": r"knowledge",
    "Image Synthesis": r"(?:image|angiography) synthesis|synthesizing|portrait synthesis",
    "Uncertainty": r"uncertainty",
    "Generative Models": r"generative|generation",
    "Polyp": r"polyp",
    "Talking Heads": r"talking (?:heads?|portrait)",
    "Foundation Models": r"foundation(?:al)?(?: pretraining| models?)",
    "MRI": r"mri|mr image",
    "Contrastive Learning": r"contrastive learning",
    "Reinforcement Learning": r"reinforcement learning",
    "Normalization": r"normalization",
    "Prototypes": r"(?:sub[- ])?prototypes?",
    "Open Set": r"open[- ]set",
    "Text Cues": r"(?:text|visual) cues",
    "Cross-domain": r"cross[- ]domain|domain (?:shift|transformation)",
    "Distillation": r"distillation",
    "OCT": r"oct",
    "Prompting": r"prompt(?:ing)?",
}
records = [line.split("\t", 1) for line in CORPUS.read_text().splitlines() if line]
counts = Counter({
    label: sum(bool(re.search(r"\b(?:" + pattern + r")\b", title, re.I)) for _, title in records)
    for label, pattern in TERMS.items()
})
ranked = [(label, n) for label, n in counts.most_common() if n][:25]
assert ranked and ranked[0][1] > 1
max_count = ranked[0][1]
width, height = 540, 350
boxes = []
pieces = []
palette = ["#e2edba", "#b9d6ab", "#d2e3bf", "#9bc9a8", "#c7dfbd"]

for i, (label, count) in enumerate(ranked):
    font = 13 + 44 * ((count - 1) / (max_count - 1)) ** 0.68
    length = font * sum(0.3 if c in " ilI–-" else 0.73 if c in "MWm" else 0.56 for c in label)
    w, h = length + 9, font * 1.16 + 3
    for step in range(6000):
        angle = step * .31 + (0 if i % 2 else math.pi)
        radius = step * .17
        x = width / 2 + math.cos(angle) * radius * 1.65
        y = height / 2 + math.sin(angle) * radius
        box = (x - w / 2, y - h / 2, x + w / 2, y + h / 2)
        l, t, r, b = box
        if l < 19 or r > width - 19 or t < 19 or b > height - 19:
            continue
        if any(l < br and r > bl and t < bb and b > bt for bl, bt, br, bb in boxes):
            continue
        boxes.append(box)
        pieces.append(
            f'<text x="{x:.2f}" y="{y+font*.32:.2f}" font-size="{font:.2f}" '
            f'textLength="{length:.2f}" lengthAdjust="spacingAndGlyphs" '
            f'fill="{palette[i % len(palette)]}">{escape(label)}</text>'
        )
        break

min_year, max_year = min(year for year, _ in records), max(year for year, _ in records)
OUTPUT.write_text(f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}">
<title>Publication title word cloud, {min_year}–{max_year}</title>
<desc>Common terms from {len(records)} titles. {escape(", ".join(f"{term}: {n}" for term, n in ranked[:8]))}.</desc>
<defs><radialGradient id="paper"><stop stop-color="#284b39"/><stop offset="1" stop-color="#142f26"/></radialGradient>
<pattern id="grid" width="18" height="18" patternUnits="userSpaceOnUse"><path d="M0 18V0h18" fill="none" stroke="#a8caa1" stroke-opacity=".10" stroke-width=".7"/></pattern></defs>
<path d="M0 0h540v350H0z" fill="url(#paper)"/><path d="M0 0h540v350H0z" fill="url(#grid)"/>
<path d="M13 29V13h16m482 0h16v16M13 321v16h16m482 0h16v-16" fill="none" stroke="#9fbe91" stroke-opacity=".58"/>
<g font-family="system-ui,sans-serif" font-weight="650" text-anchor="middle">
{chr(10).join(pieces)}
</g>
</svg>
''', encoding="utf-8")
print(f"{len(records)} titles; {len(pieces)} terms placed. Leading terms:", ranked[:8])
