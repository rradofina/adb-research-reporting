from __future__ import annotations

import base64
import html
import re
from datetime import date
from pathlib import Path

from evidence_data import ANNOTATED_IDS, EVIDENCE, REFERENCES


ROOT = Path(__file__).resolve().parent
MANUSCRIPT = ROOT / "review_manuscript.md"
FIGURE_DIR = ROOT / "figures"
OUTPUT = (
    ROOT
    / "outputs"
    / "task31_welfare_review_20260804"
    / "Asia_Pacific_Welfare_Losses_Review_2026.html"
)

NAVY = "#12345b"


def slugify(value: str) -> str:
    value = value.lower().replace("&", " and ")
    value = re.sub(r"[^a-z0-9]+", "-", value).strip("-")
    return value or "section"


def inline_markup(value: str) -> str:
    escaped = html.escape(value, quote=False)
    escaped = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", escaped)
    escaped = re.sub(
        r"(https?://[^\s<]+)",
        lambda match: (
            '<a href="{0}" target="_blank" rel="noopener">{0}</a>'.format(
                match.group(1).rstrip(".,);")
            )
            + match.group(1)[len(match.group(1).rstrip(".,);")) :]
        ),
        escaped,
    )
    return escaped


def embedded_image(filename: str) -> str:
    raw = (FIGURE_DIR / filename).read_bytes()
    return "data:image/png;base64," + base64.b64encode(raw).decode("ascii")


FIGURES = {
    "1": (
        "figure_1_conceptual_pathways.png",
        "Conceptual pathways linking aggregate shocks to welfare losses",
        "Aggregate shocks propagate through markets, public services, assets, and household responses before becoming losses in capabilities.",
    ),
    "2": (
        "figure_2_comparative_magnitude.png",
        "Comparative magnitude of selected welfare losses",
        "Panels deliberately retain their original units; they are comparisons of scale, not additive components of one welfare total.",
    ),
    "3": (
        "figure_3_lifecycle_impacts.png",
        "Life-cycle impacts among children, working-age adults, and older persons",
        "The same shock produces different welfare losses by age, biological sensitivity, labour-market position, and care dependence.",
    ),
    "4": (
        "figure_4_geographic_distribution.png",
        "Geographic distribution of reviewed evidence and representative losses",
        "Study density is uneven across subregions and should not be interpreted as a ranking of underlying vulnerability.",
    ),
}


def figure_html(number: str) -> str:
    filename, title, note = FIGURES[number]
    return f"""
    <figure class="report-figure" aria-labelledby="figure-{number}-caption">
      <div class="figure-kicker">Figure {number}</div>
      <div class="figure-frame">
        <img src="{embedded_image(filename)}" alt="{html.escape(title)}" loading="lazy">
      </div>
      <figcaption id="figure-{number}-caption">
        <strong>{html.escape(title)}.</strong> {html.escape(note)}
        <span>Source: authors' synthesis of the study-level evidence register.</span>
      </figcaption>
    </figure>
    """


def rows_for(ids: list[str]) -> list[dict]:
    by_id = {record["id"]: record for record in EVIDENCE}
    return [by_id[item] for item in ids]


def table_shell(number: str, title: str, headers: list[str], rows: list[list[str]], note: str) -> str:
    head = "".join(f"<th scope=\"col\">{html.escape(item)}</th>" for item in headers)
    body = []
    for row in rows:
        cells = "".join(f"<td>{inline_markup(str(item))}</td>" for item in row)
        body.append(f"<tr>{cells}</tr>")
    label = "Key estimates" if number == "KEY" else f"Table {number}"
    return f"""
    <section class="table-block" aria-labelledby="table-{number.lower()}-title">
      <div class="table-heading">
        <div><span>{label}</span><h4 id="table-{number.lower()}-title">{html.escape(title)}</h4></div>
        <p>Scroll horizontally to inspect all fields.</p>
      </div>
      <div class="table-scroll" tabindex="0">
        <table>
          <thead><tr>{head}</tr></thead>
          <tbody>{''.join(body)}</tbody>
        </table>
      </div>
      <p class="table-note">{html.escape(note)}</p>
    </section>
    """


def required_table(number: str) -> str:
    if number == "1":
        ids = ["C01", "C02", "C03", "C04", "C05", "C06", "C07", "C08", "C09", "C10", "C11", "C12", "C14", "C15"]
        records = rows_for(ids)
        rows = [[e["study"], e["geography"], e["population"], e["welfare_indicator"], e["estimate"], e["methodology"]] for e in records]
        return table_shell(number, "Major studies on COVID-19 welfare losses in Asia and the Pacific", ["Study", "Geography", "Population", "Welfare indicator", "Estimated loss", "Methodology"], rows, "Source: authors' synthesis of cited studies.")
    if number == "2":
        records = [e for e in EVIDENCE if e["category"] == "Economic shock"]
        rows = [[e["study"], e["shock"], e["geography"], e["welfare_indicator"], e["estimate"]] for e in records]
        return table_shell(number, "Major studies on economic shocks, 2015-present", ["Study", "Shock type", "Geography", "Welfare measure", "Magnitude"], rows, "Source: authors' synthesis of cited studies.")
    if number == "3":
        ids = ["N01", "N02", "N03", "N04", "N06", "N07", "N08", "N09", "N10", "N12", "N13", "N14", "N15", "N16", "N17", "N18", "N19", "N21", "N22", "N23", "N24"]
        records = rows_for(ids)
        rows = [[e["study"], e["shock"], e["geography"], e["welfare_indicator"], e["estimate"]] for e in records]
        return table_shell(number, "Major studies on environmental and climate shocks", ["Study", "Hazard type", "Geography", "Welfare outcome", "Magnitude of loss"], rows, "Exposure and scenario estimates are labelled and are not treated as realized loss.")
    if number == "4":
        rows = [
            ["Children (0-17)", "Learning, nutrition, service disruption, protection, and psychosocial development", "Learning poverty 60%→78% in South Asia; future earnings −up to 14.4%; wasting risk +9% after a 5% real food-price increase", "South Asia; disaster-prone Southeast Asia and Pacific; pastoral Central/East Asia"],
            ["Working-age adults (18-64)", "Jobs, hours, earnings, informality, migration, debt, care, and mental health", "81 million Asia-Pacific jobs lost in 2020; women +8 pp work stoppage; Lao real wages about −33% in 2023", "Region-wide; tourism-dependent Southeast Asia and Pacific; crisis economies"],
            ["Older persons (65+)", "Mortality, chronic disease, care access, isolation, fixed-income erosion, and evacuation", "Pre-vaccine IFR 8.29% at 80+; pandemic mortality concentrated at older ages; non-fatal Asia-specific estimates sparse", "All subregions; largest gaps in low-capacity and conflict settings"],
        ]
        return table_shell(number, "Welfare losses by demographic group", ["Group", "Primary welfare impacts", "Quantitative estimates", "Regions most affected"], rows, "Age-group burdens are compared across different welfare domains and are not additive.")
    if number == "5":
        rows = [
            ["COVID-19", "Very high and region-wide: GDP, jobs, poverty, mortality, food security, and services", "High: excess mortality, learning, nutrition, debt, and scarring", "Large regional models, surveys, mortality, and learning evidence", "High for direction and ranking; medium for exact totals"],
            ["Inflation and food/energy prices", "Moderate regionally; very high for poor net consumers and crisis countries", "Medium-high when nutrition, schooling, or assets deteriorate", "Good microsimulation; strong child-nutrition micro evidence", "High for regressivity/mechanism; medium for national totals"],
            ["Macro, debt, currency, and trade shocks", "Highly heterogeneous; severe in Sri Lanka, Afghanistan, Myanmar, and Lao PDR", "High if investment, services, female work, and institutions remain impaired", "Good crisis monitoring; attribution usually weak", "Medium; low in conflict/data-collapse settings"],
            ["Disasters and environmental degradation", "Extreme locally; event effects up to 31%-64% of GDP in Pacific cases", "High through assets, displacement, health, nutrition, and repeated exposure", "Strong PDNAs and causal health/productivity evidence; welfare aggregation sparse", "High for event damage and key mechanisms"],
            ["Long-run climate change", "Already visible in heat mortality, productivity, and disaster risk", "Potentially the largest cumulative burden; ADB high-end GDP gap 41% by 2100", "Multiple models agree on direction; magnitude varies with adaptation and damage functions", "Medium for broad order; low for distant point estimates"],
        ]
        return table_shell(number, "Comparative ranking of shocks", ["Shock category", "Short-term welfare losses", "Long-term welfare losses", "Evidence strength", "Confidence assessment"], rows, "Rankings are ordinal and preserve differences in unit, horizon, and counterfactual.")
    if number == "KEY":
        ids = ["C01", "C02", "C03", "C12", "C08", "E01", "E05", "E06", "E10", "N14", "N16", "N17", "N10", "N21", "N02"]
        records = rows_for(ids)
        rows = [[e["study"], e["estimate"], e["evidence_type"], e["confidence"]] for e in records]
        return table_shell(number, "Selected quantitative anchors", ["Study", "Key estimate", "Estimate type", "Confidence"], rows, "Units, baselines, and horizons follow the original sources; estimates are not additive.")
    raise ValueError(f"Unknown table {number}")


def manuscript_html() -> tuple[str, list[tuple[str, str]]]:
    lines = MANUSCRIPT.read_text(encoding="utf-8").splitlines()
    parts: list[str] = []
    toc: list[tuple[str, str]] = []
    started = False
    section_open = False
    for raw in lines:
        line = raw.strip()
        if not started:
            if line == "## Abstract":
                started = True
            else:
                continue
        if not line:
            continue
        if line.startswith("<FIGURE:"):
            parts.append(figure_html(line.split(":", 1)[1].rstrip(">")))
            continue
        if line.startswith("<TABLE:"):
            parts.append(required_table(line.split(":", 1)[1].rstrip(">")))
            continue
        if line.startswith("## ") or line == "## Abstract":
            if section_open:
                parts.append("</section>")
            title = "Abstract" if line == "## Abstract" else line[3:]
            section_id = slugify(title)
            tone = " abstract-section" if title == "Abstract" else ""
            number_match = re.match(r"^(\d+)\.\s+(.+)$", title)
            section_label = f"Section {number_match.group(1)}" if number_match else ""
            display_title = number_match.group(2) if number_match else title
            parts.append(f'<section class="report-section{tone}" id="{section_id}">')
            label_html = f'<span class="section-index">{html.escape(section_label)}</span>' if section_label else ""
            parts.append(f'<h2>{label_html}{html.escape(display_title)}</h2>')
            if title != "Abstract":
                toc.append((section_id, title))
            section_open = True
            continue
        if line.startswith("### "):
            title = line[4:]
            parts.append(f'<h3 id="{slugify(title)}">{html.escape(title)}</h3>')
            continue
        if line.startswith("#### "):
            parts.append(f'<h4>{html.escape(line[5:])}</h4>')
            continue
        if line.startswith("**Keywords:**"):
            parts.append(f'<p class="keywords">{inline_markup(line)}</p>')
            parts.append(
                '<aside class="reading-note"><strong>How to read the estimates</strong><p>Ranges preserve the original scenario or uncertainty interval. GDP gaps, asset losses, poverty changes, deaths, exposure counts, and lifetime earnings are not summed. Confidence applies to the estimate’s use in this review.</p></aside>'
            )
            continue
        parts.append(f"<p>{inline_markup(line)}</p>")
    if section_open:
        parts.append("</section>")
    return "\n".join(parts), toc


def explorer_html() -> str:
    categories = sorted({e["category"] for e in EVIDENCE})
    subregions = sorted({e["subregion"] for e in EVIDENCE})
    category_options = "".join(f'<option value="{html.escape(x)}">{html.escape(x)}</option>' for x in categories)
    subregion_options = "".join(f'<option value="{html.escape(x)}">{html.escape(x)}</option>' for x in subregions)
    cards = []
    for record in EVIDENCE:
        cards.append(
            f"""
            <article class="study-card" data-category="{html.escape(record['category'])}" data-confidence="{html.escape(record['confidence'])}" data-subregion="{html.escape(record['subregion'])}" data-search="{html.escape(' '.join(str(v) for v in record.values()).lower())}">
              <div class="study-meta"><span>{html.escape(record['id'])}</span><span>{html.escape(record['category'])}</span><span class="confidence confidence-{record['confidence'].lower()}">{html.escape(record['confidence'])} confidence</span></div>
              <h3>{html.escape(record['study'])}</h3>
              <p class="study-place">{html.escape(record['geography'])} · {html.escape(record['population'])}</p>
              <p class="study-estimate">{html.escape(record['estimate'])}</p>
              <dl><div><dt>Outcome</dt><dd>{html.escape(record['welfare_indicator'])}</dd></div><div><dt>Method</dt><dd>{html.escape(record['methodology'])}</dd></div><div><dt>Limitation</dt><dd>{html.escape(record['limitations'])}</dd></div></dl>
              <a class="source-link" href="{html.escape(record['url'])}" target="_blank" rel="noopener">Open source <span aria-hidden="true">↗</span></a>
            </article>
            """
        )
    return f"""
    <section class="report-section explorer-section" id="study-browser">
      <div class="eyebrow">Interactive evidence register</div>
      <h2>Browse the 52-study evidence base</h2>
      <p class="section-lead">Search by country, author, shock, population, outcome, or method. Filters operate entirely in this file.</p>
      <div class="explorer-controls">
        <label class="search-control"><span>Search studies</span><input id="study-search" type="search" placeholder="Try ‘learning’, ‘Fiji’, or ‘food prices’"></label>
        <label><span>Shock category</span><select id="category-filter"><option value="">All categories</option>{category_options}</select></label>
        <label><span>Subregion</span><select id="subregion-filter"><option value="">All subregions</option>{subregion_options}</select></label>
        <label><span>Confidence</span><select id="confidence-filter"><option value="">All ratings</option><option>High</option><option>Medium</option><option>Low</option></select></label>
      </div>
      <div class="result-line"><strong id="study-count">52 studies</strong><button id="clear-filters" type="button">Clear filters</button></div>
      <div class="study-grid" id="study-grid">{''.join(cards)}</div>
      <button class="load-more" id="load-more" type="button">Show more studies</button>
    </section>
    """


def references_html() -> str:
    references = sorted(dict.fromkeys(REFERENCES), key=lambda item: re.sub(r"^[^A-Za-z]+", "", item).lower())
    items = "".join(f"<li>{inline_markup(reference)}</li>" for reference in references)
    return f"""
    <section class="report-section references-section" id="references">
      <div class="eyebrow">Source record</div>
      <h2>References</h2>
      <ol class="references-list">{items}</ol>
    </section>
    """


def annotations_html() -> str:
    by_id = {record["id"]: record for record in EVIDENCE}
    items = []
    for number, study_id in enumerate(ANNOTATED_IDS, start=1):
        record = by_id[study_id]
        items.append(
            f"""
            <details class="annotation-card" {'open' if number <= 2 else ''}>
              <summary><span>{number:02d}</span><div><strong>{html.escape(record['study'])}</strong><small>{html.escape(record['source'])}</small></div></summary>
              <div class="annotation-body">
                <p><strong>Coverage and finding.</strong> {html.escape(record['geography'])}; {html.escape(record['population'])}. The study reports {html.escape(record['estimate'])}.</p>
                <p><strong>Method and identification.</strong> {html.escape(record['methodology'])}. The identifying basis is {html.escape(record['identification'].lower())}.</p>
                <p><strong>Use and caution.</strong> It supplies a {html.escape(record['evidence_type'].lower())} for {html.escape(record['welfare_indicator'].lower())}. Principal limitation: {html.escape(record['limitations'])}. Confidence: {html.escape(record['confidence'])}.</p>
                <a href="{html.escape(record['url'])}" target="_blank" rel="noopener">Read source ↗</a>
              </div>
            </details>
            """
        )
    return f"""
    <section class="report-section annotations-section" id="annotated-bibliography">
      <div class="eyebrow">Critical reading list</div>
      <h2>Annotated bibliography: 20 influential studies</h2>
      <p class="section-lead">Selected for regional reach, empirical credibility, methodological influence, or importance to cross-shock comparison.</p>
      <div class="annotation-grid">{''.join(items)}</div>
    </section>
    """


def reproducibility_html() -> str:
    return """
    <section class="report-section methods-footer" id="review-protocol">
      <div class="eyebrow">Reproducibility</div>
      <h2>Review protocol and release note</h2>
      <div class="protocol-grid">
        <p>The companion workbook contains one row per quantitative source, the required extraction fields, confidence coding, source URLs, and the data used for Figures 2–4. The manuscript and figures were generated from the same structured register.</p>
        <p>This is a structured rapid evidence review with systematic-scoping elements, not a registered systematic review. Before external journal submission, subscribed databases should be refreshed and records should be dual-screened and independently extracted.</p>
        <p><strong>Version:</strong> 4 August 2026<br><strong>Evidence cutoff:</strong> 31 July 2026<br><strong>Main narrative:</strong> approximately 9,655 words</p>
      </div>
    </section>
    """


TEMPLATE = """<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="description" content="A multidimensional review of welfare losses from COVID-19, economic crises, disasters, environmental degradation, and climate change in Asia and the Pacific.">
  <meta name="theme-color" content="#12345b">
  <title>Welfare Losses from Aggregate Shocks | Asia and the Pacific</title>
  <style>
    :root {
      --navy: #12345b;
      --navy-deep: #092541;
      --teal: #007f86;
      --teal-bright: #0ea5a8;
      --gold: #d79a16;
      --red: #a8434b;
      --green: #3d7b5d;
      --ink: #24313d;
      --muted: #64717d;
      --line: #d9e1e6;
      --pale: #f4f7f9;
      --paper: #fffefd;
      --serif: Charter, "Iowan Old Style", "Palatino Linotype", Georgia, serif;
      --sans: Aptos, Inter, "Segoe UI", Arial, sans-serif;
      --shadow: 0 24px 70px rgba(9, 37, 65, .12);
      --article-size: 18px;
    }
    * { box-sizing: border-box; }
    html { scroll-behavior: smooth; scroll-padding-top: 88px; }
    body { margin: 0; color: var(--ink); background: #edf2f5; font-family: var(--sans); line-height: 1.55; }
    a { color: var(--teal); text-decoration-thickness: 1px; text-underline-offset: 3px; }
    a:hover { color: var(--navy); }
    button, input, select { font: inherit; }
    button { cursor: pointer; }
    .skip-link { position: fixed; left: 12px; top: -80px; z-index: 1000; background: #fff; color: var(--navy); padding: 10px 14px; border-radius: 8px; }
    .skip-link:focus { top: 12px; }
    .reading-progress { position: fixed; inset: 0 0 auto; height: 4px; z-index: 999; background: linear-gradient(90deg, var(--gold) var(--progress, 0%), transparent 0); pointer-events: none; }
    .topbar { position: sticky; top: 0; z-index: 50; height: 72px; display: flex; align-items: center; justify-content: space-between; gap: 20px; padding: 0 clamp(20px, 4vw, 64px); background: rgba(255,254,253,.94); border-bottom: 1px solid rgba(18,52,91,.12); backdrop-filter: blur(16px); }
    .brand { display: flex; align-items: center; gap: 12px; color: var(--navy); font-weight: 760; letter-spacing: -.01em; }
    .brand-mark { display: grid; grid-template-columns: 18px 10px 7px; align-items: end; gap: 4px; height: 26px; }
    .brand-mark i { display: block; background: var(--navy); border-radius: 2px 2px 0 0; }
    .brand-mark i:nth-child(1) { height: 26px; }
    .brand-mark i:nth-child(2) { height: 18px; background: var(--teal); }
    .brand-mark i:nth-child(3) { height: 11px; background: var(--gold); }
    .top-actions { display: flex; gap: 8px; align-items: center; }
    .utility-button { border: 1px solid var(--line); background: white; color: var(--navy); padding: 8px 12px; border-radius: 999px; font-size: 13px; font-weight: 700; }
    .utility-button:hover { border-color: var(--teal); background: #f2fbfb; }
    .hero { position: relative; overflow: hidden; background: var(--navy-deep); color: white; padding: clamp(72px, 10vw, 132px) clamp(20px, 6vw, 88px) 88px; }
    .hero::before { content: ""; position: absolute; width: 780px; aspect-ratio: 1; right: -180px; top: -300px; border-radius: 50%; background: radial-gradient(circle at 35% 40%, rgba(14,165,168,.6), rgba(14,165,168,0) 64%); }
    .hero::after { content: ""; position: absolute; width: 420px; height: 420px; right: 10%; bottom: -340px; border: 70px solid rgba(215,154,22,.22); border-radius: 50%; }
    .hero-inner { position: relative; z-index: 2; max-width: 1320px; margin: auto; display: grid; grid-template-columns: minmax(0, 1.45fr) minmax(300px, .55fr); gap: clamp(40px, 7vw, 100px); align-items: end; }
    .eyebrow { color: var(--teal); text-transform: uppercase; letter-spacing: .16em; font-size: 12px; font-weight: 800; }
    .hero .eyebrow { color: #72d5d7; }
    h1 { max-width: 900px; margin: 18px 0 24px; font-family: var(--serif); font-size: clamp(42px, 6.5vw, 84px); line-height: .99; letter-spacing: -.055em; font-weight: 700; }
    .deck { max-width: 780px; margin: 0; color: #d7e3ed; font-family: var(--serif); font-size: clamp(19px, 2.1vw, 27px); line-height: 1.4; }
    .hero-meta { display: flex; flex-wrap: wrap; gap: 10px; margin-top: 34px; }
    .hero-meta span { padding: 8px 12px; border: 1px solid rgba(255,255,255,.22); border-radius: 999px; color: #dce7ef; font-size: 12px; }
    .hero-summary { border-top: 4px solid var(--gold); background: rgba(255,255,255,.08); padding: 26px; box-shadow: inset 0 0 0 1px rgba(255,255,255,.1); backdrop-filter: blur(12px); }
    .hero-summary h2 { margin: 0 0 18px; font-size: 14px; letter-spacing: .1em; text-transform: uppercase; color: #f1c968; }
    .hero-summary ol { list-style: none; margin: 0; padding: 0; counter-reset: summary; }
    .hero-summary li { counter-increment: summary; display: grid; grid-template-columns: 34px 1fr; gap: 12px; padding: 15px 0; border-top: 1px solid rgba(255,255,255,.14); color: #e8f0f5; font-size: 14px; }
    .hero-summary li::before { content: "0" counter(summary); color: #6fd3d5; font-weight: 800; }
    .metric-band { max-width: 1320px; margin: -38px auto 0; position: relative; z-index: 4; display: grid; grid-template-columns: repeat(4, 1fr); background: var(--paper); box-shadow: var(--shadow); }
    .metric { min-height: 128px; padding: 26px 30px; border-right: 1px solid var(--line); }
    .metric:last-child { border-right: 0; }
    .metric strong { display: block; color: var(--navy); font-family: var(--serif); font-size: 38px; line-height: 1; }
    .metric span { display: block; margin-top: 10px; color: var(--muted); font-size: 13px; }
    .page-shell { max-width: 1380px; margin: 56px auto 100px; padding: 0 28px; display: grid; grid-template-columns: 250px minmax(0, 930px); gap: clamp(36px, 5vw, 76px); justify-content: center; align-items: start; }
    .toc { position: sticky; top: 96px; max-height: calc(100vh - 120px); overflow: auto; padding-right: 12px; scrollbar-width: thin; }
    .toc h2 { margin: 0 0 16px; color: var(--navy); font-size: 12px; letter-spacing: .14em; text-transform: uppercase; }
    .toc a { display: block; padding: 7px 10px; border-left: 2px solid var(--line); color: var(--muted); text-decoration: none; font-size: 12px; line-height: 1.35; }
    .toc a:hover, .toc a.active { color: var(--navy); border-left-color: var(--teal); background: #f8fbfc; }
    .toc-tools { display: grid; grid-template-columns: 1fr 1fr; gap: 7px; margin-top: 20px; }
    .toc-tools button { border: 1px solid var(--line); border-radius: 8px; background: white; color: var(--navy); padding: 8px; font-size: 12px; font-weight: 700; }
    .article { min-width: 0; background: var(--paper); box-shadow: 0 18px 60px rgba(9,37,65,.08); }
    .article-intro { padding: 30px clamp(28px, 6vw, 72px); background: #f8fbfc; border-bottom: 1px solid var(--line); display: flex; align-items: center; justify-content: space-between; gap: 24px; }
    .article-intro p { margin: 0; font-size: 13px; color: var(--muted); }
    .status { display: inline-flex; align-items: center; gap: 8px; color: var(--green); font-size: 12px; font-weight: 800; text-transform: uppercase; letter-spacing: .08em; white-space: nowrap; }
    .status::before { content: ""; width: 8px; height: 8px; border-radius: 50%; background: var(--green); box-shadow: 0 0 0 4px rgba(61,123,93,.12); }
    .report-section { padding: clamp(54px, 7vw, 88px) clamp(28px, 7vw, 84px); border-bottom: 1px solid var(--line); }
    .report-section:last-child { border-bottom: 0; }
    .report-section > h2 { margin: 0 0 30px; color: var(--navy); font-family: var(--serif); font-size: clamp(30px, 4vw, 48px); line-height: 1.12; letter-spacing: -.03em; }
    .section-index { display: block; margin-bottom: 12px; color: var(--gold); font-family: var(--sans); font-size: 12px; letter-spacing: .14em; text-transform: uppercase; }
    .report-section h3 { margin: 52px 0 18px; color: var(--navy); font-family: var(--sans); font-size: 20px; line-height: 1.25; letter-spacing: -.015em; }
    .report-section h4 { color: var(--navy); font-size: 16px; }
    .report-section > p { max-width: 74ch; margin: 0 auto 22px; font-family: var(--serif); font-size: var(--article-size); line-height: 1.75; text-wrap: pretty; }
    .abstract-section { background: linear-gradient(135deg, #fbf8ef, #fffefd 54%); }
    .abstract-section > p:not(.keywords) { color: #263848; font-size: calc(var(--article-size) + 1px); }
    .keywords { padding-top: 20px; color: var(--muted); border-top: 1px solid #e7dec7; font-family: var(--sans) !important; font-size: 13px !important; }
    .reading-note { max-width: 74ch; margin: 38px auto 0; padding: 24px 26px; border-left: 5px solid var(--gold); background: white; box-shadow: 0 12px 35px rgba(9,37,65,.07); }
    .reading-note strong { color: var(--navy); font-size: 14px; text-transform: uppercase; letter-spacing: .08em; }
    .reading-note p { margin: 8px 0 0; color: var(--muted); font-size: 14px; }
    .report-figure { margin: 56px -22px; padding: 28px; background: #f5f8fa; border: 1px solid var(--line); }
    .figure-kicker { margin-bottom: 14px; color: var(--teal); font-size: 12px; font-weight: 800; text-transform: uppercase; letter-spacing: .12em; }
    .figure-frame { background: white; border: 1px solid #e3e8ec; }
    .figure-frame img { display: block; width: 100%; height: auto; }
    figcaption { margin-top: 14px; color: #4e5e6b; font-size: 13px; line-height: 1.55; }
    figcaption span { display: block; margin-top: 5px; color: var(--muted); font-size: 11px; }
    .table-block { margin: 60px -34px 10px; border: 1px solid var(--line); background: white; }
    .table-heading { padding: 22px 24px; display: flex; align-items: end; justify-content: space-between; gap: 20px; background: var(--navy); color: white; }
    .table-heading span { color: #79d1d3; font-size: 11px; font-weight: 800; letter-spacing: .14em; text-transform: uppercase; }
    .table-heading h4 { margin: 5px 0 0; color: white; font-family: var(--serif); font-size: 21px; }
    .table-heading p { margin: 0; color: #c7d5e0; font-size: 11px; white-space: nowrap; }
    .table-scroll { overflow-x: auto; outline: none; }
    .table-scroll:focus { box-shadow: inset 0 0 0 3px rgba(14,165,168,.32); }
    table { width: 100%; min-width: 900px; border-collapse: collapse; font-size: 12px; line-height: 1.45; }
    th { position: sticky; top: 71px; z-index: 2; padding: 13px 12px; background: #e9f1f4; color: var(--navy); text-align: left; vertical-align: bottom; font-size: 11px; }
    td { padding: 13px 12px; border-top: 1px solid var(--line); vertical-align: top; }
    tbody tr:nth-child(even) { background: #f8fafb; }
    tbody tr:hover { background: #eef7f7; }
    .table-note { margin: 0 !important; padding: 14px 22px; max-width: none !important; background: #f5f8fa; color: var(--muted); font-family: var(--sans) !important; font-size: 11px !important; }
    .section-lead { margin-left: 0 !important; color: var(--muted); font-family: var(--sans) !important; font-size: 16px !important; }
    .explorer-section { background: #f5f8fa; }
    .explorer-controls { display: grid; grid-template-columns: 1.5fr repeat(3, 1fr); gap: 12px; margin: 34px 0 18px; }
    .explorer-controls label { display: grid; gap: 7px; color: var(--navy); font-size: 11px; font-weight: 800; text-transform: uppercase; letter-spacing: .07em; }
    .explorer-controls input, .explorer-controls select { width: 100%; min-width: 0; height: 46px; padding: 0 12px; border: 1px solid #cbd6dd; border-radius: 8px; background: white; color: var(--ink); text-transform: none; letter-spacing: 0; font-weight: 500; font-size: 14px; }
    .explorer-controls input:focus, .explorer-controls select:focus { outline: 3px solid rgba(14,165,168,.18); border-color: var(--teal); }
    .result-line { display: flex; align-items: center; justify-content: space-between; margin: 14px 0 20px; color: var(--muted); font-size: 13px; }
    .result-line button { border: 0; background: transparent; color: var(--teal); font-weight: 700; }
    .study-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 16px; }
    .study-card { padding: 24px; background: white; border: 1px solid var(--line); box-shadow: 0 9px 24px rgba(9,37,65,.05); }
    .study-card[hidden] { display: none; }
    .study-meta { display: flex; flex-wrap: wrap; gap: 6px; }
    .study-meta span { padding: 4px 7px; border-radius: 4px; background: #edf2f5; color: var(--muted); font-size: 9px; font-weight: 800; text-transform: uppercase; letter-spacing: .06em; }
    .study-meta .confidence-high { color: #2e6b4e; background: #e4f1e9; }
    .study-meta .confidence-medium { color: #765911; background: #f7efd6; }
    .study-meta .confidence-low { color: #8f3740; background: #f8e2e4; }
    .study-card h3 { margin: 16px 0 5px; font-size: 17px; }
    .study-place { margin: 0 0 16px; color: var(--muted); font-size: 12px; }
    .study-estimate { margin: 0 0 18px; padding: 14px; border-left: 3px solid var(--teal); background: #f4fafa; color: var(--navy); font-family: var(--serif); font-size: 15px; line-height: 1.5; }
    .study-card dl { margin: 0; }
    .study-card dl div { display: grid; grid-template-columns: 70px 1fr; gap: 10px; padding: 8px 0; border-top: 1px solid #edf0f2; }
    .study-card dt { color: var(--muted); font-size: 10px; font-weight: 800; text-transform: uppercase; }
    .study-card dd { margin: 0; font-size: 12px; }
    .source-link { display: inline-block; margin-top: 16px; font-size: 12px; font-weight: 800; text-decoration: none; }
    .load-more { display: block; margin: 26px auto 0; padding: 12px 22px; border: 1px solid var(--navy); border-radius: 999px; background: var(--navy); color: white; font-weight: 800; }
    .references-list { margin: 36px 0 0; padding: 0; list-style: none; counter-reset: references; columns: 2; column-gap: 46px; }
    .references-list li { counter-increment: references; position: relative; break-inside: avoid; padding: 0 0 16px 34px; color: #46535e; font-family: var(--serif); font-size: 13px; line-height: 1.55; }
    .references-list li::before { content: counter(references, decimal-leading-zero); position: absolute; left: 0; top: 2px; color: var(--teal); font-family: var(--sans); font-size: 9px; font-weight: 800; }
    .annotation-grid { display: grid; gap: 10px; margin-top: 34px; }
    .annotation-card { border: 1px solid var(--line); background: white; }
    .annotation-card summary { list-style: none; display: grid; grid-template-columns: 50px 1fr; gap: 16px; padding: 18px 20px; cursor: pointer; }
    .annotation-card summary::-webkit-details-marker { display: none; }
    .annotation-card summary > span { display: grid; place-items: center; width: 40px; height: 40px; border-radius: 50%; background: var(--navy); color: white; font-weight: 800; }
    .annotation-card summary strong { display: block; color: var(--navy); font-size: 15px; }
    .annotation-card summary small { color: var(--muted); }
    .annotation-card[open] { border-left: 4px solid var(--teal); }
    .annotation-body { padding: 0 28px 24px 86px; }
    .annotation-body p { margin: 0 0 12px; font-family: var(--serif); font-size: 14px; line-height: 1.62; }
    .annotation-body a { font-size: 12px; font-weight: 800; }
    .methods-footer { background: var(--navy-deep); color: #dce7ef; }
    .methods-footer h2 { color: white; }
    .methods-footer .eyebrow { color: #74d2d4; }
    .protocol-grid { display: grid; grid-template-columns: 1fr 1fr .7fr; gap: 32px; }
    .protocol-grid p { margin: 0; color: #cbd8e2; font-size: 13px; }
    .site-footer { max-width: 1380px; margin: 0 auto; padding: 0 28px 70px; color: var(--muted); font-size: 12px; display: flex; justify-content: space-between; gap: 30px; }
    body.reading-large { --article-size: 20px; }
    @media (max-width: 980px) {
      .hero-inner { grid-template-columns: 1fr; }
      .hero-summary { max-width: 620px; }
      .metric-band { margin: 0; grid-template-columns: repeat(2, 1fr); }
      .page-shell { display: block; padding: 0; margin-top: 28px; }
      .toc { position: static; max-height: none; margin: 0 20px 24px; padding: 18px; background: white; }
      .toc nav { display: grid; grid-template-columns: repeat(2, 1fr); }
      .article { box-shadow: none; }
      .explorer-controls { grid-template-columns: 1fr 1fr; }
      .study-grid { grid-template-columns: 1fr; }
      .references-list { columns: 1; }
      .protocol-grid { grid-template-columns: 1fr; }
    }
    @media (max-width: 620px) {
      .topbar { height: 62px; padding: 0 16px; }
      .brand span:last-child { display: none; }
      .utility-button.font-button { display: none; }
      .hero { padding: 62px 20px 54px; }
      h1 { font-size: 44px; }
      .hero-summary { padding: 20px; }
      .metric-band { grid-template-columns: 1fr 1fr; }
      .metric { min-height: 108px; padding: 20px; }
      .metric strong { font-size: 31px; }
      .toc nav { grid-template-columns: 1fr; }
      .article-intro { display: block; }
      .status { margin-top: 12px; }
      .report-section { padding: 48px 20px; }
      .report-section > h2 { font-size: 34px; }
      .report-section > p { font-size: 17px; }
      .report-figure, .table-block { margin-left: 0; margin-right: 0; }
      .report-figure { padding: 12px; }
      .table-heading { align-items: start; }
      .table-heading p { display: none; }
      .explorer-controls { grid-template-columns: 1fr; }
      .annotation-card summary { grid-template-columns: 42px 1fr; padding: 15px; }
      .annotation-body { padding: 0 18px 20px; }
      .site-footer { display: block; padding: 0 20px 50px; }
    }
    @media print {
      @page { size: A4; margin: 16mm; }
      body { background: white; }
      .topbar, .reading-progress, .toc, .explorer-section, .utility-button, .load-more { display: none !important; }
      .hero { padding: 30mm 12mm; print-color-adjust: exact; -webkit-print-color-adjust: exact; }
      .hero-inner { display: block; }
      .hero-summary { margin-top: 24px; }
      .metric-band { box-shadow: none; border: 1px solid var(--line); }
      .page-shell { display: block; margin: 0; padding: 0; max-width: none; }
      .article { box-shadow: none; }
      .report-section { break-before: page; padding: 18mm 0 0; }
      .abstract-section { break-before: auto; }
      .report-figure, .table-block { margin-left: 0; margin-right: 0; break-inside: avoid; }
      .references-list { columns: 1; }
      a { color: inherit; text-decoration: none; }
      .site-footer { display: none; }
    }
  </style>
</head>
<body>
  <a class="skip-link" href="#report">Skip to report</a>
  <div class="reading-progress" aria-hidden="true"></div>
  <header class="topbar">
    <div class="brand"><span class="brand-mark" aria-hidden="true"><i></i><i></i><i></i></span><span>Evidence Review · Asia and the Pacific</span></div>
    <div class="top-actions"><button class="utility-button font-button" id="font-toggle" type="button">Larger text</button><button class="utility-button" type="button" onclick="window.print()">Print / Save PDF</button></div>
  </header>
  <section class="hero">
    <div class="hero-inner">
      <div>
        <div class="eyebrow">Multidimensional welfare · Evidence cutoff 31 July 2026</div>
        <h1>Welfare losses from aggregate shocks in Asia and the Pacific</h1>
        <p class="deck">A source-verified review of COVID-19, economic crises, disasters, environmental degradation, and climate change—measured beyond GDP.</p>
        <div class="hero-meta"><span>Internal review edition</span><span>Developing Asia and the Pacific</span><span>Observed and modelled losses separated</span></div>
      </div>
      <aside class="hero-summary">
        <h2>What the evidence says</h2>
        <ol>
          <li>COVID-19 produced the broadest synchronized welfare shock in the review period.</li>
          <li>National crises and Pacific disasters generated the largest proportional country setbacks.</li>
          <li>Children carry the longest loss horizon; older persons bore the steepest mortality risk.</li>
        </ol>
      </aside>
    </div>
  </section>
  <section class="metric-band" aria-label="Review summary">
    <div class="metric"><strong>52</strong><span>quantitative studies and assessments</span></div>
    <div class="metric"><strong>5</strong><span>comparative evidence tables</span></div>
    <div class="metric"><strong>4</strong><span>original synthesis figures</span></div>
    <div class="metric"><strong>20</strong><span>annotated influential studies</span></div>
  </section>
  <div class="page-shell">
    <aside class="toc" aria-label="Report navigation">
      <h2>In this review</h2>
      <nav>__TOC__</nav>
      <div class="toc-tools"><button type="button" data-jump="study-browser">Study browser</button><button type="button" data-jump="references">References</button></div>
    </aside>
    <main class="article" id="report">
      <div class="article-intro"><p>Economic Research and Development Impact Department · Working draft</p><span class="status">Source-linked</span></div>
      __ARTICLE__
      __EXPLORER__
      __REFERENCES__
      __ANNOTATIONS__
      __PROTOCOL__
    </main>
  </div>
  <footer class="site-footer"><span>Prepared as a near-publication-ready chapter for internal review.</span><span>Estimates are not summed across incompatible units or overlapping populations.</span></footer>
  <script>
    (function () {
      var root = document.documentElement;
      var progress = document.querySelector('.reading-progress');
      function updateProgress() {
        var max = document.documentElement.scrollHeight - window.innerHeight;
        var value = max > 0 ? Math.min(100, Math.max(0, window.scrollY / max * 100)) : 0;
        root.style.setProperty('--progress', value.toFixed(2) + '%');
      }
      window.addEventListener('scroll', updateProgress, { passive: true });
      updateProgress();

      document.getElementById('font-toggle').addEventListener('click', function () {
        document.body.classList.toggle('reading-large');
        this.textContent = document.body.classList.contains('reading-large') ? 'Standard text' : 'Larger text';
      });
      document.querySelectorAll('[data-jump]').forEach(function (button) {
        button.addEventListener('click', function () { document.getElementById(button.dataset.jump).scrollIntoView(); });
      });

      var navLinks = Array.from(document.querySelectorAll('.toc nav a'));
      var observed = navLinks.map(function (link) { return document.getElementById(link.getAttribute('href').slice(1)); }).filter(Boolean);
      var navObserver = new IntersectionObserver(function (entries) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) {
            navLinks.forEach(function (link) { link.classList.toggle('active', link.getAttribute('href') === '#' + entry.target.id); });
          }
        });
      }, { rootMargin: '-18% 0px -72% 0px' });
      observed.forEach(function (section) { navObserver.observe(section); });

      var search = document.getElementById('study-search');
      var category = document.getElementById('category-filter');
      var subregion = document.getElementById('subregion-filter');
      var confidence = document.getElementById('confidence-filter');
      var cards = Array.from(document.querySelectorAll('.study-card'));
      var count = document.getElementById('study-count');
      var loadMore = document.getElementById('load-more');
      var limit = 8;
      function applyFilters(resetLimit) {
        if (resetLimit) limit = 8;
        var query = search.value.trim().toLowerCase();
        var matches = cards.filter(function (card) {
          return (!query || card.dataset.search.indexOf(query) !== -1) &&
            (!category.value || card.dataset.category === category.value) &&
            (!subregion.value || card.dataset.subregion === subregion.value) &&
            (!confidence.value || card.dataset.confidence === confidence.value);
        });
        cards.forEach(function (card) { card.hidden = true; });
        matches.slice(0, limit).forEach(function (card) { card.hidden = false; });
        count.textContent = matches.length + (matches.length === 1 ? ' study' : ' studies');
        loadMore.hidden = matches.length <= limit;
      }
      [search, category, subregion, confidence].forEach(function (control) {
        control.addEventListener(control === search ? 'input' : 'change', function () { applyFilters(true); });
      });
      loadMore.addEventListener('click', function () { limit += 8; applyFilters(false); });
      document.getElementById('clear-filters').addEventListener('click', function () {
        search.value = ''; category.value = ''; subregion.value = ''; confidence.value = ''; applyFilters(true); search.focus();
      });
      applyFilters(true);
    }());
  </script>
</body>
</html>
"""


def build() -> Path:
    article, toc_items = manuscript_html()
    toc_items.extend(
        [
            ("study-browser", "Study browser"),
            ("references", "References"),
            ("annotated-bibliography", "Annotated bibliography"),
            ("review-protocol", "Review protocol"),
        ]
    )
    toc = "".join(f'<a href="#{section_id}">{html.escape(title)}</a>' for section_id, title in toc_items)
    output = (
        TEMPLATE.replace("__TOC__", toc)
        .replace("__ARTICLE__", article)
        .replace("__EXPLORER__", explorer_html())
        .replace("__REFERENCES__", references_html())
        .replace("__ANNOTATIONS__", annotations_html())
        .replace("__PROTOCOL__", reproducibility_html())
    )
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(output, encoding="utf-8")
    return OUTPUT


if __name__ == "__main__":
    path = build()
    print(path)
    print(f"bytes={path.stat().st_size:,}")
