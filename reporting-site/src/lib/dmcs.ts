// ADB regional DMC roster with subregion grouping for the Atlas page.

export interface DMC {
  iso3: string;
  iso2: string;
  name: string;
  subregion:
    | "South Asia"
    | "Southeast Asia"
    | "East Asia"
    | "Central Asia"
    | "Caucasus"
    | "Pacific";
  population_2024?: number;
}

export const DMCS: DMC[] = [
  // South Asia
  { iso3: "AFG", iso2: "AF", name: "Afghanistan", subregion: "South Asia" },
  { iso3: "BGD", iso2: "BD", name: "Bangladesh", subregion: "South Asia" },
  { iso3: "BTN", iso2: "BT", name: "Bhutan", subregion: "South Asia" },
  { iso3: "IND", iso2: "IN", name: "India", subregion: "South Asia" },
  { iso3: "MDV", iso2: "MV", name: "Maldives", subregion: "South Asia" },
  { iso3: "NPL", iso2: "NP", name: "Nepal", subregion: "South Asia" },
  { iso3: "PAK", iso2: "PK", name: "Pakistan", subregion: "South Asia" },
  { iso3: "LKA", iso2: "LK", name: "Sri Lanka", subregion: "South Asia" },

  // Southeast Asia
  { iso3: "BRN", iso2: "BN", name: "Brunei Darussalam", subregion: "Southeast Asia" },
  { iso3: "KHM", iso2: "KH", name: "Cambodia", subregion: "Southeast Asia" },
  { iso3: "IDN", iso2: "ID", name: "Indonesia", subregion: "Southeast Asia" },
  { iso3: "LAO", iso2: "LA", name: "Lao PDR", subregion: "Southeast Asia" },
  { iso3: "MYS", iso2: "MY", name: "Malaysia", subregion: "Southeast Asia" },
  { iso3: "MMR", iso2: "MM", name: "Myanmar", subregion: "Southeast Asia" },
  { iso3: "PHL", iso2: "PH", name: "Philippines", subregion: "Southeast Asia" },
  { iso3: "THA", iso2: "TH", name: "Thailand", subregion: "Southeast Asia" },
  { iso3: "TLS", iso2: "TL", name: "Timor-Leste", subregion: "Southeast Asia" },
  { iso3: "VNM", iso2: "VN", name: "Viet Nam", subregion: "Southeast Asia" },

  // East Asia
  { iso3: "CHN", iso2: "CN", name: "China", subregion: "East Asia" },
  { iso3: "HKG", iso2: "HK", name: "Hong Kong, China", subregion: "East Asia" },
  { iso3: "MNG", iso2: "MN", name: "Mongolia", subregion: "East Asia" },
  { iso3: "TPE", iso2: "TW", name: "Taipei,China", subregion: "East Asia" },

  // Central Asia
  { iso3: "KAZ", iso2: "KZ", name: "Kazakhstan", subregion: "Central Asia" },
  { iso3: "KGZ", iso2: "KG", name: "Kyrgyz Republic", subregion: "Central Asia" },
  { iso3: "TJK", iso2: "TJ", name: "Tajikistan", subregion: "Central Asia" },
  { iso3: "TKM", iso2: "TM", name: "Turkmenistan", subregion: "Central Asia" },
  { iso3: "UZB", iso2: "UZ", name: "Uzbekistan", subregion: "Central Asia" },

  // Caucasus
  { iso3: "ARM", iso2: "AM", name: "Armenia", subregion: "Caucasus" },
  { iso3: "AZE", iso2: "AZ", name: "Azerbaijan", subregion: "Caucasus" },
  { iso3: "GEO", iso2: "GE", name: "Georgia", subregion: "Caucasus" },

  // Pacific
  { iso3: "COK", iso2: "CK", name: "Cook Islands", subregion: "Pacific" },
  { iso3: "FJI", iso2: "FJ", name: "Fiji", subregion: "Pacific" },
  { iso3: "KIR", iso2: "KI", name: "Kiribati", subregion: "Pacific" },
  { iso3: "MHL", iso2: "MH", name: "Marshall Islands", subregion: "Pacific" },
  { iso3: "FSM", iso2: "FM", name: "Micronesia, Fed. Sts.", subregion: "Pacific" },
  { iso3: "NRU", iso2: "NR", name: "Nauru", subregion: "Pacific" },
  { iso3: "NIU", iso2: "NU", name: "Niue", subregion: "Pacific" },
  { iso3: "PLW", iso2: "PW", name: "Palau", subregion: "Pacific" },
  { iso3: "PNG", iso2: "PG", name: "Papua New Guinea", subregion: "Pacific" },
  { iso3: "WSM", iso2: "WS", name: "Samoa", subregion: "Pacific" },
  { iso3: "SLB", iso2: "SB", name: "Solomon Islands", subregion: "Pacific" },
  { iso3: "TON", iso2: "TO", name: "Tonga", subregion: "Pacific" },
  { iso3: "TUV", iso2: "TV", name: "Tuvalu", subregion: "Pacific" },
  { iso3: "VUT", iso2: "VU", name: "Vanuatu", subregion: "Pacific" },
];

export const SUBREGIONS = [
  "South Asia",
  "Southeast Asia",
  "East Asia",
  "Central Asia",
  "Caucasus",
  "Pacific",
] as const;

export const dmcByIso = new Map(DMCS.map((d) => [d.iso3, d]));
export const dmcName = (iso3: string) => dmcByIso.get(iso3)?.name ?? iso3;
