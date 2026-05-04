import streamlit as st
import folium
from streamlit_folium import st_folium
import random
import requests

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Licht uit het Zuiden — Islamitisch Spanje",
    page_icon="🌙",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── CSS ───────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Amiri:ital,wght@0,400;0,700;1,400&family=Nunito:wght@400;600;700;800&display=swap');

:root {
    --gold:       #C9973A;
    --gold-lt:    #E8C87A;
    --gold-pale:  #FDF0D5;
    --terracotta: #9B4A1B;
    --deep:       #120800;
    --ink:        #2C1A0E;
    --cream:      #FEFAF2;
    --teal:       #1D6B5F;
    --teal-lt:    #2E9B8A;
    --pattern: repeating-linear-gradient(
        45deg, transparent, transparent 12px,
        rgba(201,151,58,.05) 12px, rgba(201,151,58,.05) 24px);
}

html, body, [class*="css"] {
    font-family: 'Nunito', sans-serif;
    background-color: var(--cream);
    color: var(--ink);
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: var(--deep) !important;
    border-right: 3px solid var(--gold);
}
[data-testid="stSidebar"] * { color: var(--cream) !important; }
[data-testid="stSidebar"] .stRadio > label { display:none; }
[data-testid="stSidebar"] .stRadio label {
    font-size: 1.05rem;
    padding: 8px 4px;
    border-radius: 8px;
    transition: background .2s;
}
[data-testid="stSidebar"] hr { border-color: rgba(201,151,58,.3) !important; }

/* ── Hero ── */
.hero {
    background: linear-gradient(135deg, #120800 0%, #3B1A06 55%, #120800 100%);
    border-radius: 22px;
    padding: 52px 44px 44px;
    text-align: center;
    position: relative;
    overflow: hidden;
    margin-bottom: 32px;
    border: 2px solid var(--gold);
    box-shadow: 0 12px 48px rgba(0,0,0,.25);
}
.hero::before {
    content:"";
    position:absolute; inset:0;
    background: var(--pattern);
}
.hero::after {
    content:"";
    position:absolute;
    bottom:-40px; left:50%; transform:translateX(-50%);
    width:300px; height:80px;
    background: radial-gradient(ellipse, rgba(201,151,58,.18), transparent 70%);
}
.hero-arabic {
    font-family:'Amiri',serif;
    font-size:2rem; color:var(--gold); opacity:.65;
    margin-bottom:8px; position:relative;
    letter-spacing: 4px;
}
.hero-title {
    font-family:'Amiri',serif;
    font-size:3.4rem; color:var(--gold-lt);
    margin:0; line-height:1.1; position:relative;
}
.hero-sub {
    font-size:1.1rem; color:#D4B896;
    margin-top:12px; position:relative;
}

/* ── Cards ── */
.card {
    background:white;
    border-radius:18px;
    padding:28px 32px;
    margin-bottom:22px;
    border-left:6px solid var(--gold);
    box-shadow:0 4px 24px rgba(0,0,0,.07);
}
.card h2 {
    font-family:'Amiri',serif;
    color:var(--terracotta);
    font-size:1.85rem; margin-bottom:10px;
}
.card p { line-height:1.8; font-size:1.05rem; }

/* ── Tijdlijn ── */
.timeline { padding-left:28px; border-left:3px solid var(--gold); margin:20px 0; }
.tl-item  { margin-bottom:26px; position:relative; }
.tl-item::before {
    content:"";
    position:absolute; left:-38px; top:7px;
    width:16px; height:16px;
    background:var(--gold); border-radius:50%;
    border:3px solid white;
    box-shadow:0 0 0 2px var(--gold);
}
.tl-year  { font-family:'Amiri',serif; font-size:1.4rem; color:var(--terracotta); font-weight:700; }
.tl-event { font-size:1rem; line-height:1.65; margin-top:4px; }

/* ── Weetje ── */
.weetje {
    background:linear-gradient(135deg,#FFF9EA,#FFF3D0);
    border:2px dashed var(--gold);
    border-radius:14px;
    padding:18px 24px;
    margin:16px 0;
    font-size:1rem; line-height:1.65;
}
.weetje span { font-size:1.4rem; margin-right:8px; }

/* ── Speurtocht ── */
.speur-card {
    background:linear-gradient(135deg,#0E1F1C,#163D36);
    border-radius:18px;
    padding:28px 32px;
    color:white;
    margin-bottom:20px;
    border:2px solid var(--teal-lt);
    box-shadow:0 6px 28px rgba(0,0,0,.18);
}
.speur-card h3 { font-family:'Amiri',serif; font-size:1.7rem; color:var(--gold-lt); margin:0 0 10px; }
.speur-card p  { opacity:.9; line-height:1.7; }
.speur-badge {
    display:inline-block;
    background:var(--gold);
    color:var(--deep);
    font-weight:800;
    font-size:.75rem;
    padding:3px 12px;
    border-radius:20px;
    margin-bottom:12px;
    letter-spacing:.5px;
    text-transform:uppercase;
}
.speur-clue {
    background:rgba(255,255,255,.08);
    border-radius:10px;
    padding:14px 18px;
    margin-top:14px;
    font-style:italic;
    border-left:4px solid var(--gold);
}

/* ── Quiz ── */
.quiz-q {
    font-size:1.15rem; font-weight:700;
    margin-bottom:14px; color:var(--ink);
}
.correct-banner {
    background:#D4EDDA; border:2px solid #28a745;
    border-radius:10px; padding:14px 20px;
    color:#155724; font-weight:700; margin-top:10px;
}
.wrong-banner {
    background:#F8D7DA; border:2px solid #dc3545;
    border-radius:10px; padding:14px 20px;
    color:#721c24; font-weight:700; margin-top:10px;
}
.score-box {
    background:linear-gradient(135deg,var(--deep),#3B1F0A);
    color:var(--gold-lt);
    border-radius:16px; padding:24px 32px;
    text-align:center;
    font-family:'Amiri',serif; font-size:1.5rem;
    border:2px solid var(--gold);
    margin-top:24px;
}

/* ── Stad detail ── */
.stad-header {
    background:linear-gradient(135deg,#1A0A00,#3D1F08);
    border-radius:18px 18px 0 0;
    padding:28px 32px 20px;
    color:var(--gold-lt);
    font-family:'Amiri',serif;
    font-size:2rem;
    border-bottom:3px solid var(--gold);
}
.stad-body {
    background:white;
    border-radius:0 0 18px 18px;
    padding:24px 32px 28px;
    margin-bottom:22px;
    box-shadow:0 6px 28px rgba(0,0,0,.09);
}
.beziensw-link {
    display:inline-block;
    background:var(--terracotta);
    color:white !important;
    font-weight:700;
    font-size:.9rem;
    padding:9px 20px;
    border-radius:10px;
    text-decoration:none;
    margin:6px 6px 6px 0;
    transition:opacity .2s;
}
.beziensw-link:hover { opacity:.85; }

/* ── Fotos grid ── */
.foto-grid {
    display:grid;
    grid-template-columns:1fr 1fr;
    gap:12px;
    margin:16px 0;
}
.foto-grid img {
    width:100%; height:180px;
    object-fit:cover;
    border-radius:12px;
    border:2px solid var(--gold-pale);
}

/* ── Thema blokken (klikbaar) ── */
.thema-blok {
    background:linear-gradient(135deg,#120800,#3B1A06);
    border-radius:20px;
    padding:36px 28px;
    text-align:center;
    border:2px solid #C9973A;
    color:#E8C87A;
    cursor:pointer;
    transition: transform 0.15s, box-shadow 0.15s, border-color 0.15s;
    height:100%;
    position:relative;
    overflow:hidden;
}
.thema-blok:hover {
    transform:translateY(-4px);
    box-shadow:0 12px 40px rgba(201,151,58,.3);
    border-color:#E8C87A;
}
.thema-blok .thema-icon { font-size:3rem; margin-bottom:14px; display:block; }
.thema-blok h3 {
    font-family:'Amiri',serif;
    font-size:1.5rem;
    margin:0 0 10px;
    color:var(--gold-lt);
}
.thema-blok p { font-size:.9rem; opacity:.85; margin:0 0 18px; line-height:1.6; color:#D4B896; }
.thema-blok .klik-badge {
    display:inline-block;
    background:rgba(201,151,58,.2);
    border:1px solid var(--gold);
    color:var(--gold-lt);
    font-size:.78rem;
    font-weight:700;
    padding:5px 14px;
    border-radius:20px;
    letter-spacing:.5px;
}

/* ── Niveau knoppen ── */
.niveau-card {
    border-radius:16px;
    padding:28px 24px;
    text-align:center;
    cursor:pointer;
    margin-bottom:12px;
    transition: transform 0.15s, box-shadow 0.15s;
}
.niveau-card:hover { transform:translateY(-3px); }
.niveau-makkelijk {
    background:linear-gradient(135deg,#1A4A2E,#2E7A4E);
    border:2px solid #4CAF82;
    color:white;
}
.niveau-moeilijk {
    background:linear-gradient(135deg,#4A1A1A,#7A2E2E);
    border:2px solid #CF6C6C;
    color:white;
}
.niveau-card h3 { font-family:'Amiri',serif; font-size:1.6rem; margin:0 0 8px; }
.niveau-card p  { font-size:.92rem; opacity:.85; margin:0; line-height:1.6; }

/* ── Galgje ── */
.galgje-letter {
    display:inline-block;
    width:44px; height:54px;
    border-bottom:3px solid var(--ink);
    text-align:center;
    font-size:1.6rem; font-weight:800;
    margin:0 4px;
    color:var(--terracotta);
    line-height:54px;
    transition: color 0.2s;
}
.galgje-toetsenbord {
    display:flex; flex-wrap:wrap; gap:8px;
    margin:20px 0;
}
.letter-btn {
    width:42px; height:42px;
    border-radius:8px;
    border:2px solid var(--gold);
    background:white;
    font-size:1rem; font-weight:700;
    cursor:pointer;
    transition:all .15s;
    color:var(--ink);
}
.letter-btn:hover { background:var(--gold); color:white; }
.letter-btn:disabled { opacity:.3; cursor:default; background:#eee; border-color:#ccc; }

/* ── Galg tekening ── */
.galg-svg { display:block; margin:0 auto; }

/* ── Rekensom ── */
.rekensom-card {
    background:linear-gradient(135deg,#0A1A2E,#1A3A5E);
    border-radius:18px;
    padding:32px 36px;
    color:white;
    border:2px solid #4A90D9;
    margin:20px 0;
    text-align:center;
}
.rekensom-card .som {
    font-family:'Amiri',serif;
    font-size:2.8rem;
    color:#90C8FF;
    margin:16px 0;
    letter-spacing:4px;
}
.rekensom-card .context {
    font-size:.95rem;
    opacity:.8;
    line-height:1.7;
    margin-bottom:16px;
}

/* ── Woordpuzzel ── */
.puzzel-raster {
    display:inline-block;
    border:2px solid var(--gold);
    border-radius:10px;
    overflow:hidden;
    margin:16px auto;
}
.puzzel-cel {
    width:44px; height:44px;
    border:1px solid #ddd;
    display:inline-flex;
    align-items:center; justify-content:center;
    font-size:1.1rem; font-weight:800;
    color:var(--ink);
}
.puzzel-cel.actief { background:var(--gold-pale); }
.puzzel-cel.gevonden { background:#D4EDDA; color:#155724; }

/* ── Terugknop ── */
.terug-knop {
    display:inline-flex;
    align-items:center;
    gap:8px;
    background:rgba(201,151,58,.15);
    border:2px solid var(--gold);
    color:var(--terracotta);
    font-weight:700;
    font-size:.95rem;
    padding:8px 18px;
    border-radius:10px;
    cursor:pointer;
    margin-bottom:20px;
    text-decoration:none;
}

/* ── Succes banner ── */
.succes-banner {
    background:linear-gradient(135deg,#1A4A2E,#2E7A4E);
    color:white;
    border-radius:14px;
    padding:20px 28px;
    text-align:center;
    font-family:'Amiri',serif;
    font-size:1.4rem;
    border:2px solid #4CAF82;
    margin:16px 0;
}
.verlies-banner {
    background:linear-gradient(135deg,#4A1A1A,#7A2E2E);
    color:white;
    border-radius:14px;
    padding:20px 28px;
    text-align:center;
    font-family:'Amiri',serif;
    font-size:1.4rem;
    border:2px solid #CF6C6C;
    margin:16px 0;
}
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# DATA
# ══════════════════════════════════════════════════════════════════════════════

@st.cache_data(ttl=3600, show_spinner=False)
def haal_wikipedia_fotos(zoektermen: list) -> list:
    resultaten = []
    headers = {"User-Agent": "IslamEuropaApp/2.0 (educatief project; geen commercieel doel)"}
    for zoekterm, caption in zoektermen:
        try:
            url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{zoekterm.replace(' ', '_')}"
            r = requests.get(url, headers=headers, timeout=6)
            if r.status_code == 200:
                data = r.json()
                img = data.get("originalimage", {}).get("source") or data.get("thumbnail", {}).get("source")
                if img:
                    resultaten.append((img, caption))
                    continue
        except Exception:
            pass
        try:
            api = "https://commons.wikimedia.org/w/api.php"
            params = {
                "action": "query", "generator": "search",
                "gsrnamespace": 6, "gsrsearch": zoekterm,
                "gsrlimit": 1, "prop": "imageinfo",
                "iiprop": "url", "format": "json"
            }
            r = requests.get(api, params=params, headers=headers, timeout=6)
            if r.status_code == 200:
                pages = r.json().get("query", {}).get("pages", {})
                for page in pages.values():
                    img_url = page.get("imageinfo", [{}])[0].get("url", "")
                    if img_url and img_url.lower().endswith((".jpg", ".jpeg", ".png")):
                        resultaten.append((img_url, caption))
                        break
        except Exception:
            pass
    return resultaten


STEDEN = {
    "Córdoba": {
        "emoji": "🕌",
        "lat": 37.8882, "lon": -4.7794,
        "kleur": "darkred",
        "beschrijving": (
            "Córdoba was in de 10e eeuw de grootste en rijkste stad van Europa. "
            "Meer dan 500.000 mensen woonden hier. Er waren meer dan 70 bibliotheken, "
            "300 openbare badhuizen en de beroemde Mezquita — de Grote Moskee. "
            "Geleerden uit heel Europa en de islamitische wereld kwamen naar Córdoba om te studeren."
        ),
        "weetjes": [
            "De Mezquita van Córdoba heeft 856 zuilen van marmer, jaspis en graniet!",
            "Kalief Al-Hakam II had een bibliotheek van 400.000 boeken — meer dan alle Europese kloosters bij elkaar.",
            "Córdoba had straatverlichting terwijl Parijs en Londen nog in het donker zaten.",
        ],
        "wikipedia_fotos": [
            ("Mezquita-Catedral de Córdoba", "De Mezquita van Córdoba"),
            ("Medina_Azahara", "Medina Azahara — de paleisstad"),
        ],
    },
    "Granada": {
        "emoji": "🏰",
        "lat": 37.1773, "lon": -3.5986,
        "kleur": "red",
        "beschrijving": (
            "Granada was het laatste islamitische koninkrijk van Spanje. Hier staat de beroemde "
            "Alhambra — een van de mooiste paleizen ter wereld. De stad lag hoog in de Sierra Nevada "
            "en hield stand tot 1492, toen sultan Boabdil de sleutels aan de Spaanse vorsten gaf. "
            "Volgens het verhaal keek hij voor het laatste om naar zijn stad en huilde."
        ),
        "weetjes": [
            "De Alhambra heeft meer dan 10.000 bezoekers per dag — boek altijd ver van tevoren!",
            "De naam 'Alhambra' betekent 'de rode' in het Arabisch, door de rode kleur van de lemen muren.",
            "'Seufzer des Mohren' (Zucht van de Moor) is de naam van de bergpas waar Boabdil voor het laatste omkeek.",
        ],
        "wikipedia_fotos": [
            ("Alhambra", "De Alhambra van Granada"),
            ("Palace_of_the_Lions,_Alhambra", "Patio de los Leones"),
        ],
    },
    "Sevilla": {
        "emoji": "🌹",
        "lat": 37.3886, "lon": -5.9823,
        "kleur": "orange",
        "beschrijving": (
            "Sevilla was een bloeiende havenstad en cultureel centrum. De Giralda, "
            "nu de klokkentoren van de kathedraal, was oorspronkelijk een islamitische minaret gebouwd in 1198. "
            "De toren was zo mooi dat de Spanjaarden hem spaarden toen ze de grote moskee sloopten. "
            "Ze bouwden er gewoon een enorme kerk omheen!"
        ),
        "weetjes": [
            "De Giralda-toren heeft geen trappen maar hellingen, zodat de muezzin te paard naar boven kon!",
            "In Sevilla stond een van de grootste moskeeën van Al-Andalus — nu is het de grootste gotische kathedraal ter wereld.",
            "Sevilla had prachtige tuinen met waterkanalen, gebaseerd op het paradijselijke ontwerp uit de Koran.",
        ],
        "wikipedia_fotos": [
            ("Giralda", "De Giralda — vroeger een minaret"),
            ("Alcázar_of_Seville", "Real Alcázar van Sevilla"),
        ],
    },
    "Toledo": {
        "emoji": "📚",
        "lat": 39.8628, "lon": -4.0273,
        "kleur": "blue",
        "beschrijving": (
            "Toledo was de 'Stad van de Drie Culturen' — moslims, christenen en joden leefden hier "
            "eeuwenlang samen. Het beroemde 'Vertaalschool van Toledo' zorgde ervoor dat Arabische "
            "boeken over wiskunde, astronomie en medicijnen werden vertaald naar het Latijn. "
            "Zonder Toledo was de Europese Renaissance misschien nooit gekomen."
        ),
        "weetjes": [
            "In Toledo werden werken van Aristoteles en Ibn Rushd (Averroës) vertaald — dit veranderde Europa voor altijd.",
            "Toledo staat bekend als 'La Ciudad Imperial' — de keizerlijke stad.",
            "De stad ligt op een rotsplateau, bijna geheel omringd door de rivier de Taag.",
        ],
        "wikipedia_fotos": [
            ("Toledo,_Spain", "Toledo vanuit de lucht"),
            ("Cristo_de_la_Luz_Mosque", "Moskee Cristo de la Luz — 1000 jaar oud"),
        ],
    },
    "Almería": {
        "emoji": "⚓",
        "lat": 36.8340, "lon": -2.4637,
        "kleur": "green",
        "beschrijving": (
            "Almería was een van de rijkste havensteden van Al-Andalus. De stad had een enorme "
            "haven van waaruit zijde, specerijen en edelstenen werden verhandeld. "
            "De Alcazaba van Almería — een enorm Moors fort op een heuvel — is een van de "
            "best bewaard gebleven islamitische vestingen van Europa."
        ),
        "weetjes": [
            "De naam 'Almería' komt van het Arabisch: 'al-Mariyya' betekent 'de wachttoren van de zee'.",
            "In de 10e eeuw had Almería meer dan 10.000 weefgetouwen voor zijde!",
            "De alcazaba van Almería was groter dan het Alhambra in zijn hoogtijdagen.",
        ],
        "wikipedia_fotos": [
            ("Alcazaba_of_Almería", "Alcazaba — het grote Moorse fort"),
            ("Almería", "Almería aan de Middellandse Zee"),
        ],
    },
}

TIJDLIJN = [
    ("711", "🚢", "Tariq ibn Ziyad steekt over vanuit Afrika naar Spanje met 7.000 man. De Visigoten worden verslagen bij de Slag bij Guadalete. De straat van Gibraltar is naar hem vernoemd: 'Jebel al-Tariq'."),
    ("718–750", "⚔️", "Moslimlegers veroveren het grootste deel van het Iberisch Schiereiland. Ze noemen het land 'Al-Andalus'."),
    ("756", "👑", "Abd al-Rahman I sticht het Emiraat Córdoba. Hij maakt van Córdoba een onafhankelijk moslimkoninkrijk — een van de machtigste ter wereld."),
    ("784", "🕌", "De bouw van de Mezquita (Grote Moskee) van Córdoba begint. Het wordt een van de mooiste gebouwen ooit gemaakt."),
    ("912–961", "✨", "Gouden Eeuw onder Abd al-Rahman III. Córdoba wordt de grootste stad van Europa. Hij roept zichzelf uit tot kalief."),
    ("936", "🏛️", "Bouw van de prachtige paleistad Medina Azahara bij Córdoba begint — een wonder van de middeleeuwse architectuur."),
    ("976–1009", "📖", "Hoogtepunt van islamitische wetenschap. Bibliotheken, ziekenhuizen en universiteiten bloeien. Geleerden als Ibn Hazm en Maimonides leven hier."),
    ("1031", "💔", "Het Califaat van Córdoba valt uiteen in kleine koninkrijkjes, de 'Taifa's'."),
    ("1085", "🏰", "Toledo, een grote stad, valt in handen van de christelijke koningen. De Reconquista begint serieus."),
    ("1236", "😢", "Córdoba wordt veroverd. De Grote Moskee wordt een kathedraal."),
    ("1492", "🔑", "Granada, het laatste islamitische koninkrijk, geeft zich over. Boabdil overhandigt de sleutels. Einde van Al-Andalus na 781 jaar."),
]

QUIZ_VRAGEN = [
    {
        "vraag": "Hoe noemden de moslims Spanje tijdens hun bestuur?",
        "opties": ["El Dorado", "Al-Andalus", "Arabistan", "Iberica"],
        "antwoord": 1,
        "uitleg": "Al-Andalus was de Arabische naam. Hiervan is ook de naam 'Andalusië' afgeleid die nog steeds bestaat!"
    },
    {
        "vraag": "In welk jaar staken de moslimlegers over naar Spanje?",
        "opties": ["500", "711", "900", "1000"],
        "antwoord": 1,
        "uitleg": "In 711 stak Tariq ibn Ziyad over. De Straat van Gibraltar is zelfs naar hem vernoemd: 'Jebel al-Tariq' = Berg van Tariq!"
    },
    {
        "vraag": "Wat betekent 'Alhambra' in het Arabisch?",
        "opties": ["Het paleis", "De rode", "Het paradijs", "De sterren"],
        "antwoord": 1,
        "uitleg": "Al-Hamra = 'de rode'. Door de rode kleur van de lemen muren in het zonlicht."
    },
    {
        "vraag": "Welke stad was in de 10e eeuw de grootste van Europa?",
        "opties": ["Parijs", "Rome", "Londen", "Córdoba"],
        "antwoord": 3,
        "uitleg": "Córdoba had meer dan 500.000 inwoners en 70 bibliotheken, terwijl Parijs maar een kleine stad was!"
    },
    {
        "vraag": "Hoelang duurde de islamitische aanwezigheid in Spanje?",
        "opties": ["100 jaar", "300 jaar", "500 jaar", "Bijna 800 jaar"],
        "antwoord": 3,
        "uitleg": "Van 711 tot 1492 — bijna 781 jaar! Ter vergelijking: Nederland bestaat nog geen 500 jaar als koninkrijk."
    },
    {
        "vraag": "Welke toren was oorspronkelijk een islamitische minaret in Sevilla?",
        "opties": ["Eiffeltoren", "De Giralda", "Torre del Oro", "Torre de Comares"],
        "antwoord": 1,
        "uitleg": "De Giralda in Sevilla was een minaret gebouwd in 1198. Hij was zo mooi dat de Spanjaarden hem bewaarden en er een kerk omheen bouwden!"
    },
    {
        "vraag": "In welke stad konden moslims, christenen en joden samen kennis uitwisselen?",
        "opties": ["Granada", "Almería", "Toledo", "Sevilla"],
        "antwoord": 2,
        "uitleg": "Toledo was beroemd om zijn 'Vertaalschool' waar de drie religies samenwerkten om Arabische boeken naar Latijn te vertalen."
    },
    {
        "vraag": "Wat betekent de naam 'Almería'?",
        "opties": ["De gouden stad", "De wachttoren van de zee", "Het rode fort", "De bloemengaard"],
        "antwoord": 1,
        "uitleg": "Al-Mariyya in het Arabisch betekent 'de wachttoren van de zee'. Almería was een enorm belangrijke havenstad."
    },
]

SPEURTOCHT = [
    {
        "stad": "Granada",
        "locatie": "Alhambra — Patio de los Leones",
        "moeilijkheid": "🟢 Makkelijk",
        "vraag": "Tel het aantal leeuwen dat de fontein in het midden ondersteunt. Hoeveel zijn het er?",
        "hint": "Kijk goed onder de grote ronde fontein in het midden van het plein.",
        "antwoord": "12",
        "uitleg": "De Leeuwenfontein heeft precies 12 leeuwen. Ze stellen de 12 maanden van het jaar voor!",
        "missie": "Maak een foto naast één van de leeuwen en schrijf op wat er uit hun mond komt.",
        "wikipedia_foto": ("Palace_of_the_Lions,_Alhambra", "Patio de los Leones — tel de leeuwen!"),
    },
    {
        "stad": "Granada",
        "locatie": "Alhambra — Muren en Torens",
        "moeilijkheid": "🟡 Gemiddeld",
        "vraag": "Hoeveel torens telt de buitenmuur van de Alhambra (globaal)?",
        "hint": "Je kunt de torens zien als je om het complex loopt of er op uitkijkt.",
        "antwoord": "30",
        "uitleg": "De Alhambra heeft ongeveer 30 torens langs de muren — ze dienden als uitkijkpost en verdediging.",
        "missie": "Zoek de Comares-toren — de hoogste toren. Hoe hoog voel jij je als je erboven staat?",
        "wikipedia_foto": ("Alhambra", "De muren en torens van de Alhambra"),
    },
    {
        "stad": "Córdoba",
        "locatie": "Mezquita — Gebedshal",
        "moeilijkheid": "🟢 Makkelijk",
        "vraag": "De Mezquita heeft honderden zuilen. Hoeveel zijn het er globaal?",
        "hint": "Je vindt dit getal ook op informatieborden binnen.",
        "antwoord": "856",
        "uitleg": "De Mezquita heeft 856 zuilen van marmer, graniet en jaspis — verzameld uit het hele Middellandse Zeegebied!",
        "missie": "Kijk omhoog naar een van de rood-witte bogen. Teken of beschrijf het patroon dat je ziet.",
        "wikipedia_foto": ("Mezquita-Catedral_de_Córdoba", "De zuilen en bogen van de Mezquita"),
    },
    {
        "stad": "Córdoba",
        "locatie": "Medina Azahara",
        "moeilijkheid": "🔴 Moeilijk",
        "vraag": "Medina Azahara lag op welke heuvel buiten Córdoba? Wat is de naam van de plek?",
        "hint": "Kijk op het informatiebord bij de ingang van het museum.",
        "antwoord": "Jabal al-Arus (Berg van de bruid)",
        "uitleg": "Kalief Abd al-Rahman III bouwde de stad op de 'Berg van de bruid' — vernoemd naar zijn geliefde.",
        "missie": "Zoek het mozaïek of het reliëf dat bloemen toont. Welke bloem herken je?",
        "wikipedia_foto": ("Medina_Azahara", "De ruïnes van Medina Azahara"),
    },
    {
        "stad": "Sevilla",
        "locatie": "Giralda-toren",
        "moeilijkheid": "🟢 Makkelijk",
        "vraag": "De Giralda heeft geen trappen maar iets anders. Wat vind je als je naar boven loopt?",
        "hint": "Kijk goed naar de vloer als je de toren beklimt.",
        "antwoord": "Hellingen (opritten)",
        "uitleg": "De muezzin reed op een ezel of paard naar boven! Hellingen waren makkelijker dan trappen voor dieren.",
        "missie": "Kijk vanuit de top van de Giralda. Welke rivier zie je slingeren door de stad?",
        "wikipedia_foto": ("Giralda", "De Giralda — vroeger een islamitische minaret"),
    },
    {
        "stad": "Toledo",
        "locatie": "Mezquita del Cristo de la Luz",
        "moeilijkheid": "🟡 Gemiddeld",
        "vraag": "In welk jaar werd de Mezquita del Cristo de la Luz gebouwd?",
        "hint": "Het staat op het informatiebord buiten — zoek naar een jaar rond het jaar 1000.",
        "antwoord": "999 of 1000",
        "uitleg": "De moskee werd gebouwd rond 999-1000 na Chr. — hij is dus meer dan 1000 jaar oud!",
        "missie": "Bestudeer de bogen van de moskee. Zijn ze anders dan de bogen in een gewone kerk? Beschrijf het verschil.",
        "wikipedia_foto": ("Cristo_de_la_Luz_Mosque", "Mezquita del Cristo de la Luz — meer dan 1000 jaar oud!"),
    },
]

# ══════════════════════════════════════════════════════════════════════════════
# SPELDATA — GALGJE & PUZZELS per thema
# ══════════════════════════════════════════════════════════════════════════════

GALGJE_WETENSCHAP = [
    ("ALGEBRA", "De wiskunde van vergelijkingen — een Arabisch woord!"),
    ("ALGORITME", "Een wiskundige stap-voor-stap methode — vernoemd naar de geleerde Al-Khwarizmi."),
    ("ASTRONOMIE", "De studie van sterren en planeten — Arabieren waren de beste sterrenkundigen."),
    ("NULPUNT", "Het getal nul — door Arabieren naar Europa gebracht."),
    ("OPTICA", "De wetenschap van licht — Ibn al-Haytham schreef het eerste boek hierover."),
    ("GENEESKUNDE", "De kunst van het genezen — Ibn Sina schreef een beroemde medische encyclopedie."),
    ("CHEMIE", "Wetenschap van stoffen — het woord 'chemie' komt van het Arabisch 'al-kimiya'."),
    ("KOFFIE", "Dit drankje komt uit Arabië en werd in Europa bekend via Al-Andalus!"),
]

GALGJE_ARCHITECTUUR = [
    ("MINARET", "De toren van een moskee waarvan de muezzin de gelovigen oproept tot gebed."),
    ("ALHAMBRA", "Het beroemde paleis van Granada, in het Arabisch: 'de rode'."),
    ("ALCAZABA", "Een Arabisch woord voor een fort of vesting op een heuvel."),
    ("MOZAIEK", "Kleurrijke tegeltjes die prachtige patronen vormen in islamitische gebouwen."),
    ("GEWELF", "De gebogen stenen dakconstructie boven een gang of zaal in een paleis."),
    ("FONTEIN", "Water in het midden van een binnenplaats — symbool van het paradijs."),
    ("MUQARNAS", "De honingraatachtige decoratie in Arabische plafonds en nissen."),
    ("GIRALDA", "De beroemde toren van Sevilla, ooit een islamitische minaret."),
]

GALGJE_SAMENLEVEN = [
    ("CONVIVENCIA", "Het Spaanse woord voor de vreedzame samenleving van moslims, christenen en joden."),
    ("VERTALING", "In Toledo werden Arabische boeken naar Latijn vertaald — dit redde de Europese wetenschap."),
    ("TOLERANCE", "Het respecteren van andere geloven en gewoonten — kenmerk van Al-Andalus op zijn best."),
    ("MARKTPLEIN", "De soek of bazaar — waar mensen van alle geloven handel dreven."),
    ("BIBLIOTHEEK", "Córdoba had er 70 — volgepropt met boeken uit de hele wereld."),
    ("DIALOOG", "Het gesprek tussen mensen van verschillende culturen en religies."),
    ("KALIEF", "De islamitische heerser van Al-Andalus — soms ook beschermheer van geleerden."),
    ("FILOSOFIE", "De liefde voor wijsheid — Ibn Rushd (Averroës) was de grootste filosoof van zijn tijd."),
]

REKENSOMMEN_WETENSCHAP = [
    {
        "context": "Ibn al-Haytham deed in de 11e eeuw onderzoek naar licht. Hij ontdekte dat licht reist in rechte lijnen. Als licht 300 meter aflegt in 1 microseconde...",
        "vraag": "Hoeveel meter legt licht af in 5 microseconden?",
        "berekening": "300 × 5",
        "antwoord": 1500,
        "uitleg": "300 × 5 = 1.500 meter. Ibn al-Haytham's werk over licht legde de basis voor de moderne optica!",
        "hint": "Vermenigvuldig 300 met 5.",
    },
    {
        "context": "Al-Khwarizmi (van wie 'algoritme' komt) schreef in Bagdad, maar zijn boeken werden in Toledo vertaald. Hij beschreef hoe je een rechthoek berekent.",
        "vraag": "Een Arabische tuin is 12 meter breed en 15 meter lang. Wat is de oppervlakte?",
        "berekening": "12 × 15",
        "antwoord": 180,
        "uitleg": "12 × 15 = 180 m². Al-Khwarizmi's algebra maakte dit soort berekeningen voor iedereen begrijpelijk.",
        "hint": "Lengte × breedte.",
    },
    {
        "context": "De bibliotheek van Kalief Al-Hakam II in Córdoba had maar liefst 400.000 boeken. Een bibliotheek in Parijs had er in dezelfde tijd maar 400.",
        "vraag": "Hoeveel keer meer boeken had Córdoba dan Parijs?",
        "berekening": "400.000 ÷ 400",
        "antwoord": 1000,
        "uitleg": "400.000 ÷ 400 = 1.000 keer meer! Córdoba was het intellectuele centrum van de wereld.",
        "hint": "Deel 400.000 door 400.",
    },
    {
        "context": "Een islamitische sterrenkundige in Córdoba berekende de omtrek van de aarde. Hij schatte deze op 40.000 km — bijna precies goed!",
        "vraag": "Als de aarde 40.000 km omtrek heeft, hoeveel km is dan een kwart van de aardbol?",
        "berekening": "40.000 ÷ 4",
        "antwoord": 10000,
        "uitleg": "40.000 ÷ 4 = 10.000 km. Arabische geleerden kenden de ware grootte van de aarde eeuwen voor Columbus!",
        "hint": "Deel 40.000 door 4.",
    },
]

REKENSOMMEN_ARCHITECTUUR = [
    {
        "context": "De Mezquita van Córdoba heeft 856 zuilen. Ze staan in rijen van 19 zuilen breed.",
        "vraag": "Hoeveel rijen zuilen zijn er dan (856 ÷ 19 = ?)",
        "berekening": "856 ÷ 19",
        "antwoord": 45,
        "uitleg": "856 ÷ 19 = 45 rijen (met 1 extra). De architect zorgde voor perfect symmetrische rijen!",
        "hint": "Deel 856 door 19. Rond af naar het dichtstbijzijnde getal.",
    },
    {
        "context": "De buitenmuur van de Alhambra is bijna 2.000 meter lang. Er staan 30 torens langs deze muur.",
        "vraag": "Gemiddeld hoeveel meter is er tussen elke toren? (2000 ÷ 30 = ?)",
        "berekening": "2000 ÷ 30",
        "antwoord": 67,
        "uitleg": "2000 ÷ 30 ≈ 67 meter tussen elke toren. Dit zorgde voor maximaal toezicht op de muren!",
        "hint": "Deel 2000 door 30 en rond af.",
    },
    {
        "context": "Medina Azahara werd gebouwd door 10.000 arbeiders gedurende 25 jaar.",
        "vraag": "Hoeveel arbeidersjaren (person-years) kostte de bouw in totaal?",
        "berekening": "10.000 × 25",
        "antwoord": 250000,
        "uitleg": "10.000 × 25 = 250.000 arbeidersjaren! Een onvoorstelbare bouwprestatie voor de 10e eeuw.",
        "hint": "Vermenigvuldig het aantal arbeiders met het aantal jaren.",
    },
    {
        "context": "De Giralda-toren in Sevilla is 98 meter hoog. De islamitische minaret was origineel 70 meter.",
        "vraag": "Hoeveel meter hebben de Spanjaarden bovenop gebouwd?",
        "berekening": "98 - 70",
        "antwoord": 28,
        "uitleg": "98 − 70 = 28 meter! De Spanjaarden bouwden een klokkentoren van 28 meter op de islamitische minaret.",
        "hint": "Trek de originele hoogte af van de huidige hoogte.",
    },
]

REKENSOMMEN_SAMENLEVEN = [
    {
        "context": "In Toledo werkten vertalers samen: 3 moslims, 4 christenen en 2 joodse geleerden vertaalden samen een boek van 270 pagina's.",
        "vraag": "Als ze elk evenveel pagina's vertaalden, hoeveel pagina's deed elke persoon?",
        "berekening": "270 ÷ 9",
        "antwoord": 30,
        "uitleg": "270 ÷ 9 = 30 pagina's per persoon. Samenwerking over religiegrenzen heen maakte Toledo uniek!",
        "hint": "Tel alle vertalers op en deel het aantal pagina's daardoor.",
    },
    {
        "context": "Córdoba had in de 10e eeuw meer dan 70 bibliotheken. Elke bibliotheek had gemiddeld 5.000 boeken.",
        "vraag": "Hoeveel boeken waren er in totaal in alle bibliotheken van Córdoba?",
        "berekening": "70 × 5.000",
        "antwoord": 350000,
        "uitleg": "70 × 5.000 = 350.000 boeken! Terwijl heel Noord-Europa nauwelijks kon lezen.",
        "hint": "Vermenigvuldig 70 met 5.000.",
    },
    {
        "context": "Al-Andalus bestond van 711 tot 1492. Daarna werden moslims en joden verdreven uit Spanje.",
        "vraag": "Hoeveel jaar duurde Al-Andalus precies?",
        "berekening": "1492 - 711",
        "antwoord": 781,
        "uitleg": "1492 − 711 = 781 jaar! Langer dan de VS nu bestaat (circa 250 jaar).",
        "hint": "Trek het beginjaar af van het eindjaar.",
    },
    {
        "context": "Een markt in Córdoba had 5 moslimhandelaren, 3 christelijke en 4 joodse. Elke handelaar verkocht gemiddeld 12 producten per dag.",
        "vraag": "Hoeveel producten werden er op de markt in totaal per dag verkocht?",
        "berekening": "(5 + 3 + 4) × 12",
        "antwoord": 144,
        "uitleg": "(5 + 3 + 4) × 12 = 12 × 12 = 144 producten. Een bruisende markt waar iedereen samenwerkte!",
        "hint": "Tel alle handelaren op en vermenigvuldig met 12.",
    },
]

THEMA_INFO = {
    "wetenschap": {
        "label": "Wetenschap",
        "emoji": "📚",
        "beschrijving": "Wiskunde, astronomie, geneeskunde — alles bloeide in Al-Andalus terwijl Europa sliep.",
        "kleur": "#1A3A5E",
        "galgje": GALGJE_WETENSCHAP,
        "rekensommen": REKENSOMMEN_WETENSCHAP,
        "galgje_intro": "Raad het wetenschappelijke woord dat samenhangt met de islamitische geleerdheid van Al-Andalus!",
        "rekensom_intro": "Gebruik wiskunde om te ontdekken hoe ver vooruit de islamitische geleerden waren!",
    },
    "architectuur": {
        "label": "Architectuur",
        "emoji": "🏛️",
        "beschrijving": "De Alhambra, Mezquita en Alcázar zijn nog steeds te bewonderen op jouw vakantie!",
        "kleur": "#3A1A5E",
        "galgje": GALGJE_ARCHITECTUUR,
        "rekensommen": REKENSOMMEN_ARCHITECTUUR,
        "galgje_intro": "Raad het woord dat hoort bij de prachtige islamitische bouwwerken van Spanje!",
        "rekensom_intro": "Bereken de indrukwekkende afmetingen en getallen van de beroemde islamitische bouwwerken!",
    },
    "samenleven": {
        "label": "Samenleven",
        "emoji": "🤝",
        "beschrijving": "Moslims, christenen en joden leefden samen en leerden van elkaar.",
        "kleur": "#1A4A2E",
        "galgje": GALGJE_SAMENLEVEN,
        "rekensommen": REKENSOMMEN_SAMENLEVEN,
        "galgje_intro": "Raad het woord over de unieke samenleving van moslims, christenen en joden in Al-Andalus!",
        "rekensom_intro": "Bereken hoe bijzonder en groot de samenleving van Al-Andalus werkelijk was!",
    },
}

# ══════════════════════════════════════════════════════════════════════════════
# SESSION STATE initialisatie
# ══════════════════════════════════════════════════════════════════════════════
def init_session():
    defaults = {
        "pagina": "🏠  Start",
        "thema_pagina": None,       # "wetenschap" / "architectuur" / "samenleven"
        "thema_niveau": None,       # "makkelijk" / "moeilijk"
        # galgje state
        "galgje_woord": None,
        "galgje_hint": None,
        "galgje_geraden": set(),
        "galgje_fouten": 0,
        "galgje_klaar": False,
        "galgje_gewonnen": False,
        # rekensom state
        "rekensom_index": 0,
        "rekensom_score": 0,
        "rekensom_ingediend": False,
        "rekensom_klaar": False,
        # quiz state
        "quiz_antwoorden": {},
        "quiz_ingediend": False,
        # speurtocht state
        "speur_score": 0,
        "speur_opgelost": set(),
        # stad state
        "geselecteerde_stad": None,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_session()

# ══════════════════════════════════════════════════════════════════════════════
# SIDEBAR
# ══════════════════════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("""
    <div style="text-align:center;padding:16px 0 8px;">
        <div style="font-size:2.5rem">🌙</div>
        <div style="font-family:'Amiri',serif;font-size:1.3rem;color:#E8C87A;">Licht uit het Zuiden</div>
        <div style="font-size:.8rem;opacity:.5;margin-top:4px;">Al-Andalus Reisgids</div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("---")
    pagina = st.radio(
        "nav",
        ["🏠  Start", "🗺️  Kaart & Steden", "⏳  Tijdlijn", "🔍  Speurtocht", "❓  Quiz"],
        label_visibility="collapsed",
        key="sidebar_nav",
    )
    # Sync pagina
    if pagina != st.session_state.pagina:
        st.session_state.pagina = pagina
        st.session_state.thema_pagina = None
        st.session_state.thema_niveau = None

    st.markdown("---")
    st.markdown("""
    <div style="font-size:.8rem;opacity:.45;text-align:center;line-height:1.7">
        Een app voor islamitische reizigers<br>in Spanje 🇪🇸
    </div>
    """, unsafe_allow_html=True)

# ── Hero ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <div class="hero-arabic">النور من الجنوب</div>
    <h1 class="hero-title">Licht uit het Zuiden</h1>
    <p class="hero-sub">Ontdek de islamitische erfenis van Spanje · Al-Andalus Reisgids ✨</p>
</div>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# HELPER: galg SVG
# ══════════════════════════════════════════════════════════════════════════════
def galg_svg(fouten: int) -> str:
    # Onderdelen: 0=niets, per fout 1 onderdeel erbij
    # Maximaal 7 fouten (hoofd, romp, l.arm, r.arm, l.been, r.been, gezicht)
    parts = []
    if fouten >= 1:
        parts.append('<circle cx="100" cy="60" r="20" stroke="#9B4A1B" stroke-width="4" fill="none"/>')  # hoofd
    if fouten >= 2:
        parts.append('<line x1="100" y1="80" x2="100" y2="150" stroke="#9B4A1B" stroke-width="4"/>')  # romp
    if fouten >= 3:
        parts.append('<line x1="100" y1="100" x2="65" y2="130" stroke="#9B4A1B" stroke-width="4"/>')  # l arm
    if fouten >= 4:
        parts.append('<line x1="100" y1="100" x2="135" y2="130" stroke="#9B4A1B" stroke-width="4"/>')  # r arm
    if fouten >= 5:
        parts.append('<line x1="100" y1="150" x2="70" y2="185" stroke="#9B4A1B" stroke-width="4"/>')  # l been
    if fouten >= 6:
        parts.append('<line x1="100" y1="150" x2="130" y2="185" stroke="#9B4A1B" stroke-width="4"/>')  # r been
    if fouten >= 7:
        # droevig gezichtje
        parts.append('<line x1="92" y1="55" x2="96" y2="59" stroke="#9B4A1B" stroke-width="2"/>')
        parts.append('<line x1="104" y1="55" x2="108" y2="59" stroke="#9B4A1B" stroke-width="2"/>')
        parts.append('<path d="M88 72 Q100 65 112 72" stroke="#9B4A1B" stroke-width="2" fill="none"/>')

    galg = """
    <line x1="20" y1="200" x2="180" y2="200" stroke="#C9973A" stroke-width="4"/>
    <line x1="60" y1="200" x2="60" y2="10" stroke="#C9973A" stroke-width="4"/>
    <line x1="60" y1="10" x2="100" y2="10" stroke="#C9973A" stroke-width="4"/>
    <line x1="100" y1="10" x2="100" y2="40" stroke="#C9973A" stroke-width="3"/>
    """
    return f'<svg width="200" height="210" class="galg-svg">{galg}{"".join(parts)}</svg>'


# ══════════════════════════════════════════════════════════════════════════════
# GALGJE PAGINA
# ══════════════════════════════════════════════════════════════════════════════
def toon_galgje(thema_key: str):
    thema = THEMA_INFO[thema_key]
    MAX_FOUTEN = 7

    # Initialiseer woord als nog niet gedaan of nieuw spel
    if st.session_state.galgje_woord is None:
        keuze = random.choice(thema["galgje"])
        st.session_state.galgje_woord = keuze[0]
        st.session_state.galgje_hint = keuze[1]
        st.session_state.galgje_geraden = set()
        st.session_state.galgje_fouten = 0
        st.session_state.galgje_klaar = False
        st.session_state.galgje_gewonnen = False

    woord = st.session_state.galgje_woord
    geraden = st.session_state.galgje_geraden
    fouten = st.session_state.galgje_fouten
    klaar = st.session_state.galgje_klaar

    st.markdown(f"""
    <div class="card">
        <h2>{thema['emoji']} Galgje — {thema['label']}</h2>
        <p>{thema['galgje_intro']}</p>
    </div>
    """, unsafe_allow_html=True)

    # Galg + woord naast elkaar
    col_galg, col_woord = st.columns([1, 2])

    with col_galg:
        st.markdown(galg_svg(fouten), unsafe_allow_html=True)
        st.markdown(f"<p style='text-align:center;color:#9B4A1B;font-weight:700'>{fouten}/{MAX_FOUTEN} fouten</p>", unsafe_allow_html=True)

    with col_woord:
        # Toon het woord
        woord_html = ""
        for letter in woord:
            if letter in geraden or klaar:
                woord_html += f'<span class="galgje-letter">{letter}</span>'
            else:
                woord_html += '<span class="galgje-letter"> </span>'
        st.markdown(f'<div style="margin:20px 0 10px">{woord_html}</div>', unsafe_allow_html=True)

        # Hint
        st.markdown(f"""
        <div class="weetje" style="margin-top:12px">
            <span>💡</span> <em>{st.session_state.galgje_hint}</em>
        </div>
        """, unsafe_allow_html=True)

        # Verkeerde letters
        if geraden - set(woord):
            verkeerd = ", ".join(sorted(geraden - set(woord)))
            st.markdown(f"<p style='color:#721c24;font-weight:700'>Fout geraden: {verkeerd}</p>", unsafe_allow_html=True)

    # Status
    if klaar:
        if st.session_state.galgje_gewonnen:
            st.markdown(f'<div class="succes-banner">🎉 Geweldig! Je hebt het woord geraden: <strong>{woord}</strong></div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="verlies-banner">😢 Helaas! Het woord was: <strong>{woord}</strong></div>', unsafe_allow_html=True)

        if st.button("🔄 Nieuw woord proberen!", use_container_width=True):
            st.session_state.galgje_woord = None
            st.rerun()
        return

    # Toetsenbord
    st.markdown("<br>**Kies een letter:**", unsafe_allow_html=True)
    alfabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    rijen = [alfabet[i:i+9] for i in range(0, len(alfabet), 9)]

    for rij in rijen:
        cols = st.columns(len(rij))
        for col, letter in zip(cols, rij):
            with col:
                al_geraden = letter in geraden
                if st.button(
                    letter,
                    key=f"galgje_btn_{letter}",
                    disabled=al_geraden,
                    use_container_width=True,
                ):
                    geraden.add(letter)
                    if letter not in woord:
                        st.session_state.galgje_fouten += 1
                    st.session_state.galgje_geraden = geraden

                    # Check winst/verlies
                    if all(l in geraden for l in woord):
                        st.session_state.galgje_klaar = True
                        st.session_state.galgje_gewonnen = True
                    elif st.session_state.galgje_fouten >= MAX_FOUTEN:
                        st.session_state.galgje_klaar = True
                        st.session_state.galgje_gewonnen = False
                    st.rerun()


# ══════════════════════════════════════════════════════════════════════════════
# REKENSOM PAGINA
# ══════════════════════════════════════════════════════════════════════════════
def toon_rekensom(thema_key: str):
    thema = THEMA_INFO[thema_key]
    sommen = thema["rekensommen"]
    totaal = len(sommen)

    # Init index als eerste keer
    if "rekensom_volgorde" not in st.session_state or st.session_state.get("rekensom_thema") != thema_key:
        volgorde = list(range(totaal))
        random.shuffle(volgorde)
        st.session_state.rekensom_volgorde = volgorde
        st.session_state.rekensom_thema = thema_key
        st.session_state.rekensom_index = 0
        st.session_state.rekensom_score = 0
        st.session_state.rekensom_ingediend = False
        st.session_state.rekensom_klaar = False

    idx = st.session_state.rekensom_index
    score = st.session_state.rekensom_score
    klaar = st.session_state.rekensom_klaar

    st.markdown(f"""
    <div class="card">
        <h2>{thema['emoji']} Rekenpuzzels — {thema['label']}</h2>
        <p>{thema['rekensom_intro']}</p>
    </div>
    """, unsafe_allow_html=True)

    if klaar:
        if score == totaal:
            label = "🏆 Perfect! Jij bent een echte Al-Andalus rekenkampioen!"
        elif score >= totaal * 0.75:
            label = "⭐ Uitstekend! Bijna alles goed!"
        elif score >= totaal * 0.5:
            label = "👍 Goed bezig! Probeer het nog een keer."
        else:
            label = "📚 Probeer het opnieuw — lees de hints goed!"
        st.markdown(f"""
        <div class="score-box">
            {label}<br>
            <span style="font-family:'Nunito',sans-serif;font-size:3rem;color:#C9973A">{score}</span>
            <span style="font-size:1.5rem;opacity:.6"> / {totaal}</span>
        </div>
        """, unsafe_allow_html=True)
        if st.button("🔄 Opnieuw proberen!", use_container_width=True):
            st.session_state.rekensom_thema = None
            st.rerun()
        return

    som_idx = st.session_state.rekensom_volgorde[idx]
    som = sommen[som_idx]

    st.markdown(f"**Vraag {idx + 1} van {totaal}** &nbsp;|&nbsp; Score: {score} punten", unsafe_allow_html=True)
    st.progress((idx) / totaal)

    st.markdown(f"""
    <div class="rekensom-card">
        <p class="context">{som['context']}</p>
        <p style="font-size:1.1rem;font-weight:700;color:white">{som['vraag']}</p>
        <p class="som">{som['berekening']} = ?</p>
    </div>
    """, unsafe_allow_html=True)

    ingediend = st.session_state.rekensom_ingediend

    if not ingediend:
        antwoord_input = st.number_input(
            "Jouw antwoord:",
            min_value=0,
            max_value=10000000,
            step=1,
            key=f"rekensom_input_{idx}",
        )
        col1, col2 = st.columns([2, 1])
        with col1:
            if st.button("✔️ Controleer mijn antwoord!", use_container_width=True):
                st.session_state[f"rekensom_antwoord_{idx}"] = antwoord_input
                st.session_state.rekensom_ingediend = True
                st.rerun()
        with col2:
            with st.expander("💡 Hint"):
                st.write(som["hint"])
    else:
        gegeven = st.session_state.get(f"rekensom_antwoord_{idx}", 0)
        correct = abs(gegeven - som["antwoord"]) <= 1  # 1 afwijking toegestaan (afronding)

        if correct:
            st.markdown(f'<div class="correct-banner">✅ Correct! {som["uitleg"]}</div>', unsafe_allow_html=True)
            if st.session_state.get(f"rekensom_gescoord_{idx}") != True:
                st.session_state.rekensom_score += 1
                st.session_state[f"rekensom_gescoord_{idx}"] = True
        else:
            st.markdown(f'<div class="wrong-banner">❌ Helaas! Het juiste antwoord was <strong>{som["antwoord"]}</strong>. {som["uitleg"]}</div>', unsafe_allow_html=True)

        if st.button("➡️ Volgende vraag", use_container_width=True):
            st.session_state.rekensom_ingediend = False
            if idx + 1 >= totaal:
                st.session_state.rekensom_klaar = True
            else:
                st.session_state.rekensom_index += 1
            st.rerun()


# ══════════════════════════════════════════════════════════════════════════════
# THEMA SUBPAGINA
# ══════════════════════════════════════════════════════════════════════════════
def toon_thema_subpagina(thema_key: str):
    thema = THEMA_INFO[thema_key]

    # Terugknop
    if st.button(f"← Terug naar Start", key="terug_thema"):
        st.session_state.thema_pagina = None
        st.session_state.thema_niveau = None
        st.session_state.galgje_woord = None
        st.session_state.rekensom_thema = None
        st.rerun()

    niveau = st.session_state.thema_niveau

    if niveau is None:
        # Niveaukeuze
        st.markdown(f"""
        <div class="card">
            <h2>{thema['emoji']} {thema['label']}</h2>
            <p>{thema['beschrijving']}</p>
            <p>Kies een niveau om te spelen!</p>
        </div>
        """, unsafe_allow_html=True)

        c1, c2 = st.columns(2)
        with c1:
            st.markdown("""
            <div class="niveau-card niveau-makkelijk">
                <h3>🟢 Makkelijk</h3>
                <p>Speel een galgje!<br>Raad het woord letter voor letter.</p>
            </div>
            """, unsafe_allow_html=True)
            if st.button("▶ Speel Galgje!", use_container_width=True, key="kies_makkelijk"):
                st.session_state.thema_niveau = "makkelijk"
                st.session_state.galgje_woord = None
                st.rerun()

        with c2:
            st.markdown("""
            <div class="niveau-card niveau-moeilijk">
                <h3>🔴 Moeilijk</h3>
                <p>Los rekenpuzzels op!<br>Gebruik wiskunde en historische kennis.</p>
            </div>
            """, unsafe_allow_html=True)
            if st.button("▶ Speel Rekenpuzzels!", use_container_width=True, key="kies_moeilijk"):
                st.session_state.thema_niveau = "moeilijk"
                st.session_state.rekensom_thema = None
                st.rerun()

    elif niveau == "makkelijk":
        if st.button("← Terug naar niveaukeuze", key="terug_niveau_m"):
            st.session_state.thema_niveau = None
            st.session_state.galgje_woord = None
            st.rerun()
        toon_galgje(thema_key)

    elif niveau == "moeilijk":
        if st.button("← Terug naar niveaukeuze", key="terug_niveau_h"):
            st.session_state.thema_niveau = None
            st.session_state.rekensom_thema = None
            st.rerun()
        toon_rekensom(thema_key)


# ══════════════════════════════════════════════════════════════════════════════
# PAGINA ROUTER
# ══════════════════════════════════════════════════════════════════════════════
pagina_actief = st.session_state.pagina

# ── STARTPAGINA (inclusief thema subpagina's) ─────────────────────────────────
if pagina_actief == "🏠  Start":

    # Als een thema geselecteerd is
    if st.session_state.thema_pagina is not None:
        toon_thema_subpagina(st.session_state.thema_pagina)

    else:
        # Normale startpagina
        st.markdown("""
        <div class="card">
            <h2>🌙 Welkom op jouw islamitische reis door Spanje!</h2>
            <p>
                Meer dan <strong>700 jaar lang</strong> was een groot deel van Spanje islamitisch.
                De moslims noemden dit land <strong>Al-Andalus</strong>. Terwijl de rest van Europa
                in de Middeleeuwen nauwelijks kon lezen of schrijven, bloeide Al-Andalus als het
                centrum van kennis, kunst, handel en cultuur van de hele wereld.
            </p>
            <p>
                Steden als Córdoba, Granada en Sevilla waren de rijkste en mooiste steden op aarde.
                Geleerden kwamen van heinde en verre. Arabische boeken werden vertaald naar Latijn,
                waardoor Europa uiteindelijk de Renaissance kon beleven. Zonder Al-Andalus had de
                wereld er heel anders uit kunnen zien.
            </p>
        </div>
        """, unsafe_allow_html=True)

        # ── Drie thema-blokken ──────────────────────────────────────────────
        st.markdown("### 🎮 Kies een thema om te spelen:")
        c1, c2, c3 = st.columns(3)

        for col, thema_key, emoji, titel, tekst in [
            (c1, "wetenschap", "📚", "Wetenschap", "Wiskunde, astronomie, geneeskunde — alles bloeide in Al-Andalus terwijl Europa sliep."),
            (c2, "architectuur", "🏛️", "Architectuur", "De Alhambra, Mezquita en Alcázar zijn nog steeds te bewonderen op jouw vakantie!"),
            (c3, "samenleven", "🤝", "Samenleven", "Moslims, christenen en joden leefden samen en leerden van elkaar."),
        ]:
            with col:
                st.markdown(f"""
                <div class="thema-blok">
                    <span class="thema-icon">{emoji}</span>
                    <h3>{titel}</h3>
                    <p>{tekst}</p>
                    <span class="klik-badge">▶ Klik om te spelen</span>
                </div>
                """, unsafe_allow_html=True)
                if st.button(f"▶ {titel}", key=f"thema_{thema_key}", use_container_width=True):
                    st.session_state.thema_pagina = thema_key
                    st.session_state.thema_niveau = None
                    st.rerun()

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("""
        <div class="weetje">
            <span>💡</span><strong>Wist je dat?</strong> Veel woorden die we dagelijks gebruiken komen uit het Arabisch!
            <em>Suiker</em> (sukkar), <em>alcohol</em> (al-kuḥl), <em>algebra</em> (al-jabr),
            <em>koffie</em> (qahwa), <em>nul</em> (sifr) — allemaal Arabisch! Zelfs het woord 'cijfer' komt van het Arabisch.
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="card">
            <h2>🧭 Hoe gebruik je deze app?</h2>
            <p>
                <strong>🎮 Thema's (hier boven)</strong> — Kies Wetenschap, Architectuur of Samenleven en speel galgje of rekenpuzzels!<br><br>
                <strong>🗺️ Kaart & Steden</strong> — Klik op steden op de interactieve kaart voor foto's en informatie<br><br>
                <strong>⏳ Tijdlijn</strong> — Bekijk alle belangrijke momenten van 711 tot 1492<br><br>
                <strong>🔍 Speurtocht</strong> — Op locatie: zoek aanwijzingen en beantwoord vragen!<br><br>
                <strong>❓ Quiz</strong> — Test hoeveel je weet over Al-Andalus
            </p>
        </div>
        """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# PAGINA: KAART & STEDEN
# ══════════════════════════════════════════════════════════════════════════════
elif pagina_actief == "🗺️  Kaart & Steden":
    st.markdown("""
    <div class="card">
        <h2>🗺️ Islamitisch Spanje — Klik op een stad!</h2>
        <p>Klik op een van de gekleurde markers op de kaart om een stad te ontdekken. Je kunt de kaart ook inzoomen!</p>
    </div>
    """, unsafe_allow_html=True)

    m = folium.Map(location=[38.5, -4.0], zoom_start=6, tiles="CartoDB positron")
    for naam, info in STEDEN.items():
        popup_html = f"""
        <div style="font-family:sans-serif;min-width:180px;">
            <b style="font-size:1.1rem">{info['emoji']} {naam}</b><br>
            <span style="font-size:.85rem;color:#555">{info['beschrijving'][:120]}…</span>
        </div>
        """
        folium.Marker(
            location=[info["lat"], info["lon"]],
            popup=folium.Popup(popup_html, max_width=220),
            tooltip=f"{info['emoji']} {naam}",
            icon=folium.Icon(color=info["kleur"], icon="star", prefix="fa"),
        ).add_to(m)

    kaart_result = st_folium(m, width="100%", height=450, returned_objects=["last_object_clicked_tooltip"])

    st.markdown("<br>", unsafe_allow_html=True)
    gekozen = None

    if kaart_result and kaart_result.get("last_object_clicked_tooltip"):
        tooltip = kaart_result["last_object_clicked_tooltip"]
        for naam in STEDEN:
            if naam in tooltip:
                gekozen = naam
                st.session_state.geselecteerde_stad = naam

    gekozen_drop = st.selectbox(
        "📍 Of kies direct een stad:",
        ["— Kies een stad —"] + list(STEDEN.keys()),
        format_func=lambda n: n if n == "— Kies een stad —" else f"{STEDEN[n]['emoji']} {n}",
        index=(list(STEDEN.keys()).index(st.session_state.geselecteerde_stad) + 1
               if st.session_state.geselecteerde_stad in STEDEN else 0)
    )
    if gekozen_drop != "— Kies een stad —":
        gekozen = gekozen_drop
        st.session_state.geselecteerde_stad = gekozen

    if gekozen and gekozen in STEDEN:
        info = STEDEN[gekozen]
        st.markdown(f'<div class="stad-header">{info["emoji"]} {gekozen}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="stad-body"><p style="line-height:1.8;font-size:1.05rem">{info["beschrijving"]}</p>', unsafe_allow_html=True)

        if info.get("wikipedia_fotos"):
            with st.spinner("📸 Foto's laden…"):
                fotos = haal_wikipedia_fotos(info["wikipedia_fotos"])
            if fotos:
                cols = st.columns(len(fotos))
                for col, (url, caption) in zip(cols, fotos):
                    with col:
                        st.image(url, caption=caption, use_container_width=True)

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("**💡 Weetjes:**")
        for w in info["weetjes"]:
            st.markdown(f'<div class="weetje" style="margin:8px 0"><span>✨</span> {w}</div>', unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# PAGINA: TIJDLIJN
# ══════════════════════════════════════════════════════════════════════════════
elif pagina_actief == "⏳  Tijdlijn":
    st.markdown("""
    <div class="card">
        <h2>⏳ Tijdlijn van Al-Andalus (711 – 1492)</h2>
        <p>Van de eerste oversteek tot het einde — bijna 800 jaar islamitische geschiedenis in Spanje.</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="timeline">', unsafe_allow_html=True)
    for jaar, emoji, tekst in TIJDLIJN:
        st.markdown(f"""
        <div class="tl-item">
            <div class="tl-year">{emoji} {jaar}</div>
            <div class="tl-event">{tekst}</div>
        </div>
        """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="weetje">
        <span>🌟</span> Al-Andalus duurde <strong>781 jaar</strong>. Ter vergelijking:
        de VS bestaat pas ~250 jaar. Islam in Spanje was dus meer dan 3x zo lang aanwezig
        als de hele geschiedenis van Amerika!
    </div>
    """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# PAGINA: SPEURTOCHT
# ══════════════════════════════════════════════════════════════════════════════
elif pagina_actief == "🔍  Speurtocht":
    st.markdown("""
    <div class="card">
        <h2>🔍 De Speurtocht van Al-Andalus</h2>
        <p>
            Op locatie! Kies de stad waar jullie nu zijn en los de uitdagingen op.
            Zoek de aanwijzingen, beantwoord de vragen en verdien punten!
        </p>
    </div>
    """, unsafe_allow_html=True)

    steden_speurtocht = sorted(set(s["stad"] for s in SPEURTOCHT))
    gekozen_stad = st.selectbox(
        "🏙️ In welke stad zijn jullie nu?",
        steden_speurtocht,
        format_func=lambda s: f"{STEDEN[s]['emoji']} {s}" if s in STEDEN else s
    )

    opdrachten = [s for s in SPEURTOCHT if s["stad"] == gekozen_stad]

    score_col, _ = st.columns([1, 3])
    with score_col:
        st.markdown(f"""
        <div style="background:linear-gradient(135deg,#120800,#3B1A06);
            border-radius:14px;padding:20px;text-align:center;border:2px solid #C9973A;color:#E8C87A;">
            <div style="font-size:.85rem;opacity:.7;margin-bottom:4px">SCORE</div>
            <div style="font-family:'Amiri',serif;font-size:2.5rem">{st.session_state.speur_score}</div>
            <div style="font-size:.8rem;opacity:.6">punten behaald</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    for i, opdracht in enumerate(opdrachten):
        opgelost = f"{gekozen_stad}_{i}" in st.session_state.speur_opgelost

        if opdracht.get("wikipedia_foto"):
            with st.spinner("📸 Foto laden…"):
                fotos = haal_wikipedia_fotos([opdracht["wikipedia_foto"]])
            if fotos:
                url, caption = fotos[0]
                st.image(url, caption=f"📍 {caption}", use_container_width=True)

        st.markdown(f"""
        <div class="speur-card">
            <div class="speur-badge">{opdracht['moeilijkheid']} · {opdracht['locatie']}</div>
            <h3>Opdracht {i+1}</h3>
            <p>{opdracht['vraag']}</p>
            <div class="speur-clue">💡 Hint: {opdracht['hint']}</div>
        </div>
        """, unsafe_allow_html=True)

        if opgelost:
            st.success(f"✅ Opgelost! {opdracht['uitleg']}")
            st.info(f"🎯 Missie: {opdracht['missie']}")
        else:
            with st.expander(f"📝 Geef je antwoord voor opdracht {i+1}"):
                antwoord_input = st.text_input(
                    "Jouw antwoord:",
                    key=f"speur_{gekozen_stad}_{i}",
                    placeholder="Typ hier je antwoord…"
                )
                if st.button("✔️ Controleer!", key=f"check_{gekozen_stad}_{i}"):
                    correcte = opdracht["antwoord"].lower().strip()
                    gegeven = antwoord_input.lower().strip()
                    if any(part in gegeven for part in correcte.split()):
                        st.session_state.speur_score += 10
                        st.session_state.speur_opgelost.add(f"{gekozen_stad}_{i}")
                        st.rerun()
                    else:
                        st.error("Dat klopt nog niet helemaal. Kijk nog eens goed!")

    if len(st.session_state.speur_opgelost) > 0:
        totaal_mogelijk = sum(10 for s in SPEURTOCHT)
        st.markdown(f"""
        <div class="score-box">
            🏆 Totale score: {st.session_state.speur_score} / {totaal_mogelijk} punten<br>
            <span style="font-size:1rem;opacity:.8">Opdrachten opgelost: {len(st.session_state.speur_opgelost)}</span>
        </div>
        """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# PAGINA: QUIZ
# ══════════════════════════════════════════════════════════════════════════════
elif pagina_actief == "❓  Quiz":
    st.markdown("""
    <div class="card">
        <h2>❓ Quiz: Hoe goed ken jij Al-Andalus?</h2>
        <p>8 vragen over de islamitische geschiedenis van Spanje. Hoeveel weet jij? 🌙</p>
    </div>
    """, unsafe_allow_html=True)

    score = 0
    for i, q in enumerate(QUIZ_VRAGEN):
        st.markdown(f'<div class="quiz-q">Vraag {i+1} van {len(QUIZ_VRAGEN)}: {q["vraag"]}</div>', unsafe_allow_html=True)
        gekozen_optie = st.radio(f"v{i}", q["opties"], key=f"q{i}", label_visibility="collapsed")
        st.session_state.quiz_antwoorden[i] = q["opties"].index(gekozen_optie)

        if st.session_state.quiz_ingediend:
            if st.session_state.quiz_antwoorden[i] == q["antwoord"]:
                score += 1
                st.markdown(f'<div class="correct-banner">✅ Goed! {q["uitleg"]}</div>', unsafe_allow_html=True)
            else:
                juist = q["opties"][q["antwoord"]]
                st.markdown(f'<div class="wrong-banner">❌ Helaas! Goed antwoord: <em>{juist}</em>. {q["uitleg"]}</div>', unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

    col_btn, col_rst = st.columns([2, 1])
    with col_btn:
        if st.button("🌙 Controleer mijn antwoorden!", use_container_width=True):
            st.session_state.quiz_ingediend = True
            st.rerun()
    with col_rst:
        if st.button("🔄 Opnieuw", use_container_width=True):
            st.session_state.quiz_ingediend = False
            st.session_state.quiz_antwoorden = {}
            st.rerun()

    if st.session_state.quiz_ingediend:
        totaal = len(QUIZ_VRAGEN)
        if score == totaal:
            label = "🏆 Perfect! Jij bent een echte kenner van Al-Andalus!"
        elif score >= totaal * 0.75:
            label = "⭐ Uitstekend! Je weet al heel veel over de islamitische geschiedenis!"
        elif score >= totaal * 0.5:
            label = "👍 Goed bezig! Lees de tijdlijn nog eens en probeer opnieuw."
        else:
            label = "📚 Begin met de tijdlijn en de steden — dan doe je het straks beter!"
        st.markdown(f"""
        <div class="score-box">
            {label}<br>
            <span style="font-family:'Nunito',sans-serif;font-size:3rem;color:#C9973A">{score}</span>
            <span style="font-size:1.5rem;opacity:.6"> / {totaal}</span>
        </div>
        """, unsafe_allow_html=True)
