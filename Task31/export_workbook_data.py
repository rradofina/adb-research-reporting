import json
from pathlib import Path

from evidence_data import EVIDENCE, REFERENCES
from build_figures import region_links

root = Path(__file__).resolve().parent
payload = {
    "evidence": EVIDENCE,
    "references": REFERENCES,
    "key_ids": ["C01", "C02", "C03", "C12", "C08", "E01", "E05", "E06", "E10", "N14", "N16", "N17", "N10", "N21", "N02"],
    "figure2": [
        ["A. Short-run economic welfare", "Viet Nam inflation purchasing power", 2.0, "%"],
        ["A. Short-run economic welfare", "COVID-19 2020 regional GDP", 7.75, "% midpoint"],
        ["A. Short-run economic welfare", "Mongolia inflation purchasing power", 11.0, "%"],
        ["A. Short-run economic welfare", "Sri Lanka poverty-rate change", 11.9, "percentage points"],
        ["B. Population-scale burdens", "COVID jobs lost, Asia-Pacific", 81.0, "million jobs"],
        ["B. Population-scale burdens", "Additional extreme poor, developing Asia", 77.5, "million people; midpoint"],
        ["B. Population-scale burdens", "Pakistan flood additional poor", 8.75, "million people; midpoint"],
        ["B. Population-scale burdens", "COVID excess deaths, India", 4.07, "million people"],
        ["C. Human-capital effects", "EAP annual earnings loss per student", 3.8, "%"],
        ["C. Human-capital effects", "South Asia future earnings loss", 14.4, "%"],
        ["C. Human-capital effects", "South Asia learning poverty increase", 18.0, "percentage points"],
        ["C. Human-capital effects", "Food price to child wasting risk", 9.0, "% relative risk"],
        ["D. Disaster and climate burden", "Tonga eruption", 18.5, "% of GDP"],
        ["D. Disaster and climate burden", "Fiji TC Winston", 31.0, "% of GDP"],
        ["D. Disaster and climate burden", "Vanuatu TC Pam", 64.0, "% of GDP"],
        ["D. Disaster and climate burden", "ADB climate 2100 high-end scenario", 41.0, "% GDP gap"],
    ],
    "figure3": {
        "domains": ["Mortality & morbidity", "Income & employment", "Learning & skills", "Nutrition", "Mental health", "Care & social inclusion", "Lifetime persistence"],
        "groups": ["Children 0-17", "Working age 18-64", "Older persons 65+"],
        "scores": [[1,2,3],[2,3,2],[3,2,1],[3,2,2],[2,3,3],[2,3,3],[3,3,2]],
    },
    "figure4": region_links(),
    "search_log": [
        ["Cross-disciplinary journals", "Nature; Science; Nature Climate Change; Nature Food; Nature Sustainability; The Lancet; PNAS", "shock + welfare outcome + Asia/country", "2026-08-04", "Peer-reviewed priority set"],
        ["Economics journals", "JDE; World Development; QJE; JPE; REStat; JEEM; JHE", "income/consumption/employment/health/learning + shock", "2026-08-04", "Causal and quasi-experimental priority"],
        ["Institutional repositories", "ADB; World Bank; IMF; ILO; WHO; UNICEF; UNDP; ESCAP", "regional/country shock + quantitative loss", "2026-08-04", "Official assessments and grey literature"],
        ["Citation chaining", "Backward and forward chaining from influential studies", "mechanism, comparator, critique, update", "2026-08-04", "Used to locate methods and validation evidence"],
        ["Cutoff", "All sources", "Publication available by 2026-07-31", "2026-08-04", "Retracted evidence excluded"],
    ],
}

out = root / "tmp" / "workbook_data.json"
out.parent.mkdir(exist_ok=True)
out.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
print(out)
