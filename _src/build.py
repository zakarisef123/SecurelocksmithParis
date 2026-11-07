# -*- coding: utf-8 -*-
"""Générateur du site Secure Locksmith Paris (site en anglais, Paris 75, 20 arrondissements).

Usage : python3 _src/build.py
Écrit toutes les pages HTML, le sitemap, robots.txt, llms.txt et les redirections (_redirects)
à la racine du dépôt. Aucune dépendance : Python 3.12+.

Photos : déposez vos vraies photos (JPG ou WebP, ~1600 px de large) dans assets/img/photos/
avec ces noms ; elles apparaissent automatiquement au prochain build :
  home.jpg                        grande photo de l'accueil (vous, votre véhicule, une intervention)
  team.jpg                        bloc « Why trust us »
  <slug du service>.jpg           photo d'un service (ex. door-opening.jpg, armored-door.jpg)
"""
import datetime
import html
import json
import os
import re

from data import (ARRONDISSEMENTS, ARTICLES, ASSUREURS, AVIS, CHARTE, COMPARATIF, INCLUS, INTERVENTIONS, MARQUES, REALISATIONS,
                  SERVICES, TARIFS, URGENCES)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Emergency services first, then works & installation
SERVICES = [s for s in SERVICES if s["cat"] == "urgence"] + [s for s in SERVICES if s["cat"] != "urgence"]
SVC_URG = [s for s in SERVICES if s["cat"] == "urgence"]
SVC_TRAV = [s for s in SERVICES if s["cat"] != "urgence"]
SVC_BY_SLUG = {s["slug"]: s for s in SERVICES}

# ---------------------------------------------------------------------------
# Configuration : à vérifier avant mise en ligne
# ---------------------------------------------------------------------------
CONFIG = {
    "site_url": "https://securelockserrurerie.com",  # nom de domaine, sans / final
    "nom": "Secure Locksmith Paris",
    "slogan": "Your trusted locksmith",
    "tel": "+33 6 67 96 96 20",
    "tel_intl": "+33667969620",
    "wa": "33667969620",
    "email": "securelockserrurerie@gmail.com",
    "instagram": "https://www.instagram.com/securelockserrurerie/",
    # Fiche Google Business Profile
    "maps_url": "https://www.google.com/maps/place/Secure+Lock+Serrurerie/@48.870843,1.155034,9z/data=!4m10!1m2!2m1!1sSecure+Lock+Serrurerie+Paris!3m6!1s0x267653ac7048cd93:0x27df91bfb8a939fd!8m2!3d48.870843!4d2.3745164!15sChxTZWN1cmUgTG9jayBTZXJydXJlcmllIFBhcmlzWh4iHHNlY3VyZSBsb2NrIHNlcnJ1cmVyaWUgcGFyaXOSAQlsb2Nrc21pdGiaAURDaTlEUVVsUlFVTnZaRU5vZEhsalJqbHZUMnhDZDAxR2EzaFNWV1IyVlRCU05GZFZZelJSVlhSMVkyeENNVk5yUlJBQuABAPoBBAg4EEc!16s%2Fg%2F11yz6fjq73",
    # Position de la fiche Google (carte et données structurées)
    "lat": 48.870843,
    "lng": 2.3745164,
    # Lien « Demander des avis » de la fiche Google (ex. https://g.page/r/XXXX/review) ; vide = lien de la fiche
    "avis_url": "",
    # Note Google affichée sur le site : à tenir à jour (laisser vide pour ne rien afficher)
    "avis_note": "5.0",
    "avis_nombre": 101,
    # Mesure d'audience (chargée seulement après accord du visiteur)
    "gtm_id": "GTM-N742H7F8",
    "ga_id": "G-GL99Q7CQKN",
    "ads_id": "AW-17925645444",
    "ads_conv": {"call": "pIa-CPq274YcEITJzuNC", "wa": "", "form": ""},
    "google_verification": "26oalrhYl1sf4O17TalfT0E-_m-pbH7o4PDT2PE984Q",
    # Widget d'avis Google qui se met à jour tout seul (Trustindex, Elfsight, EmbedSocial…) :
    # collez ici le code d'intégration fourni par le service ; il remplace le carrousel ci-dessous.
    "reviews_widget": "",
    # Entreprise (affichée sur le site et dans les mentions légales)
    "raison_sociale": "Secure Lock Serrurerie",
    "adresse": {"rue": "5 rue Camille du Gast", "cp": "92390", "ville": "Villeneuve-la-Garenne"},
    "siren": "",   # 9 chiffres
    "siret": "",   # 14 chiffres
    "responsable": "",
    "mediateur": "",  # nom et site du médiateur de la consommation
    # Facultatif, affiché seulement si rempli (informations exactes et vérifiables uniquement)
    "experience": "",  # ex. "Locksmiths since 2015"
    "assurance_rc": "",  # ex. "Professional liability insurance: AXA, policy no. …"
}

TODAY = datetime.date.today().isoformat()
E = html.escape
URL = CONFIG["site_url"]
NOM = CONFIG["nom"]
TEL = CONFIG["tel"]
TEL_HREF = "tel:" + CONFIG["tel_intl"]
WA = "https://wa.me/" + CONFIG["wa"]
MAPS = CONFIG["maps_url"]
AVIS_URL = CONFIG["avis_url"] or MAPS
BID = URL + "/#locksmith"
WA_MSG = "Hello, I need a locksmith in Paris."


def wa_link(text):
    from urllib.parse import quote
    return WA + "?text=" + quote(text)


def fmt_int(n):
    return f"{n:,}"


def eur(n):
    return f"€{n:,}"


def siret_fmt():
    s = CONFIG["siret"]
    return f"{s[:3]} {s[3:6]} {s[6:9]} {s[9:]}" if len(s) == 14 else s


def adresse_txt():
    a = CONFIG["adresse"]
    return ", ".join(v for v in (a["rue"], f'{a["cp"]} {a["ville"]}'.strip()) if v) + ", France"


# ---------------------------------------------------------------------------
# Icons
# ---------------------------------------------------------------------------
_S = 'fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"'
ICONS = {
    "i-phone": f'<symbol id="i-phone" viewBox="0 0 24 24" {_S}><path d="M5 3h3.5l1.8 4.6-2.3 1.5a11 11 0 0 0 6 6l1.5-2.3L20 14.5V18a2 2 0 0 1-2 2A16 16 0 0 1 3 5a2 2 0 0 1 2-2z"/></symbol>',
    "i-wa": '<symbol id="i-wa" viewBox="0 0 24 24" fill="currentColor"><path d="M12 1.8A10.2 10.2 0 0 0 3.2 17.1L1.8 22.2l5.2-1.4A10.2 10.2 0 1 0 12 1.8zm0 18.6a8.4 8.4 0 0 1-4.3-1.2l-.3-.2-3.1.8.8-3-.2-.3A8.4 8.4 0 1 1 12 20.4zm4.6-6.3c-.3-.1-1.5-.7-1.7-.8-.2-.1-.4-.1-.6.1l-.8 1c-.1.2-.3.2-.5.1a6.9 6.9 0 0 1-3.4-3c-.3-.4.3-.4.7-1.3.1-.2 0-.3 0-.4l-.8-1.8c-.2-.5-.4-.4-.6-.4h-.5a1 1 0 0 0-.7.3 3 3 0 0 0-.9 2.2 5.2 5.2 0 0 0 1.1 2.7c.1.2 1.9 2.8 4.5 3.9 1.7.7 2.3.8 3.2.6.5-.1 1.5-.6 1.7-1.2.2-.6.2-1.1.1-1.2l-.4-.3z"/></symbol>',
    "i-check": f'<symbol id="i-check" viewBox="0 0 24 24" {_S} stroke-width="2.4"><path d="m5 12.5 4.5 4.5L19 7"/></symbol>',
    "i-clock": f'<symbol id="i-clock" viewBox="0 0 24 24" {_S}><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3.5 2"/></symbol>',
    "i-shield": f'<symbol id="i-shield" viewBox="0 0 24 24" {_S}><path d="M12 2.5 4.5 5.5v6c0 4.7 3.2 8.6 7.5 10 4.3-1.4 7.5-5.3 7.5-10v-6z"/><circle cx="12" cy="10.5" r="2"/><path d="M12 12.5v3"/></symbol>',
    "i-euro": f'<symbol id="i-euro" viewBox="0 0 24 24" {_S}><path d="M17.5 6.5a6.5 6.5 0 1 0 0 11"/><path d="M4.5 10.5h9M4.5 13.5h8"/></symbol>',
    "i-pin": f'<symbol id="i-pin" viewBox="0 0 24 24" {_S}><path d="M12 21.5s-7-6-7-11.5a7 7 0 0 1 14 0c0 5.5-7 11.5-7 11.5z"/><circle cx="12" cy="10" r="2.5"/></symbol>',
    "i-mail": f'<symbol id="i-mail" viewBox="0 0 24 24" {_S}><rect x="3" y="5" width="18" height="14" rx="2.5"/><path d="m3.5 7 8.5 6 8.5-6"/></symbol>',
    "i-door": f'<symbol id="i-door" viewBox="0 0 24 24" {_S}><path d="M6 21V4.5A1.5 1.5 0 0 1 7.5 3h9A1.5 1.5 0 0 1 18 4.5V21"/><path d="M3.5 21h17"/><circle cx="14.5" cy="12.5" r="1"/></symbol>',
    "i-lock": f'<symbol id="i-lock" viewBox="0 0 24 24" {_S}><rect x="4.5" y="10.5" width="15" height="10.5" rx="2.5"/><path d="M8 10.5V7.5a4 4 0 0 1 8 0v3"/><path d="M12 14.5v2.5"/></symbol>',
    "i-key": f'<symbol id="i-key" viewBox="0 0 24 24" {_S}><circle cx="7.5" cy="15.5" r="4"/><path d="m10.5 12.5 9-9M16.5 6.5l2.5 2.5M14 9l2 2"/></symbol>',
    "i-cyl": f'<symbol id="i-cyl" viewBox="0 0 24 24" {_S}><circle cx="12" cy="9.5" r="5.5"/><path d="M9.5 14v6.5h5V14"/><path d="M12 7.5v4"/></symbol>',
    "i-smart": f'<symbol id="i-smart" viewBox="0 0 24 24" {_S}><rect x="6.5" y="2.5" width="11" height="19" rx="2.5"/><path d="M10 6.5h4"/><circle cx="12" cy="13" r="2.5"/><path d="M12 15.5v2"/></symbol>',
    "i-tool": f'<symbol id="i-tool" viewBox="0 0 24 24" {_S}><path d="M14.5 6.5a4 4 0 0 0 5 5L21 13l-8 8-2-2 8-8"/><path d="M14.5 6.5 8 13l-2.5-.5L3 15l6 6 2.5-2.5L11 16"/></symbol>',
    "i-award": f'<symbol id="i-award" viewBox="0 0 24 24" {_S}><circle cx="12" cy="9" r="6"/><path d="m8.5 14 -1.5 7.5 5-3 5 3-1.5-7.5"/></symbol>',
    "i-star": '<symbol id="i-star" viewBox="0 0 24 24" fill="currentColor"><path d="m12 2.5 2.9 6 6.6.8-4.9 4.6 1.3 6.6L12 17.3l-5.9 3.2 1.3-6.6-4.9-4.6 6.6-.8z"/></symbol>',
    "i-arrow": f'<symbol id="i-arrow" viewBox="0 0 24 24" {_S} stroke-width="2"><path d="M5 12h14M13 6l6 6-6 6"/></symbol>',
    "i-sun": f'<symbol id="i-sun" viewBox="0 0 24 24" {_S}><circle cx="12" cy="12" r="4"/><path d="M12 2.5v2M12 19.5v2M2.5 12h2M19.5 12h2M5.3 5.3l1.4 1.4M17.3 17.3l1.4 1.4M5.3 18.7l1.4-1.4M17.3 6.7l1.4-1.4"/></symbol>',
    "i-sunset": f'<symbol id="i-sunset" viewBox="0 0 24 24" {_S}><path d="M7 16a5 5 0 0 1 10 0"/><path d="M2.5 19.5h19M12 3.5v5M8.5 6.5 12 3l3.5 3.5M4.5 12.5l1.4 1M19.5 12.5l-1.4 1"/></symbol>',
    "i-moon": f'<symbol id="i-moon" viewBox="0 0 24 24" {_S}><path d="M20 14.5A8 8 0 1 1 9.5 4a6.5 6.5 0 0 0 10.5 10.5z"/></symbol>',
    "i-file": f'<symbol id="i-file" viewBox="0 0 24 24" {_S}><path d="M14 3H7a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V8z"/><path d="M14 3v5h5M9 13h6M9 17h4"/></symbol>',
    "i-insta": f'<symbol id="i-insta" viewBox="0 0 24 24" {_S}><rect x="3" y="3" width="18" height="18" rx="5"/><circle cx="12" cy="12" r="4"/><circle cx="17.3" cy="6.7" r=".6" fill="currentColor"/></symbol>',
    "i-metro": f'<symbol id="i-metro" viewBox="0 0 24 24" {_S}><circle cx="12" cy="12" r="9"/><path d="M8 16V8.5l4 5 4-5V16"/></symbol>',
    "i-home": f'<symbol id="i-home" viewBox="0 0 24 24" {_S}><path d="M3.5 11 12 4l8.5 7"/><path d="M6 9.5V20h12V9.5"/><path d="M10 20v-5h4v5"/></symbol>',
}
SPRITE = '<svg width="0" height="0" style="position:absolute" aria-hidden="true"><defs>' + "".join(ICONS.values()) + "</defs></svg>"

ICONS.update({
    "i-building": f'<symbol id="i-building" viewBox="0 0 24 24" {_S}><rect x="4" y="3" width="16" height="18" rx="1.5"/><path d="M8 7h2M14 7h2M8 11h2M14 11h2M8 15h2M14 15h2M10 21v-3h4v3"/></symbol>',
    "i-card": f'<symbol id="i-card" viewBox="0 0 24 24" {_S}><rect x="2.5" y="5" width="19" height="14" rx="2.5"/><path d="M2.5 10h19M6.5 15h4"/></symbol>',
    "i-badge": f'<symbol id="i-badge" viewBox="0 0 24 24" {_S}><path d="m12 2.5 2.4 1.8 3 .1.9 2.9 2.4 1.8-.9 2.9.9 2.9-2.4 1.8-.9 2.9-3 .1L12 21.5l-2.4-1.8-3-.1-.9-2.9L3.3 15l.9-2.9-.9-2.9 2.4-1.8.9-2.9 3-.1z"/><path d="m8.5 12 2.5 2.5 4.5-5"/></symbol>',
    "i-chev": f'<symbol id="i-chev" viewBox="0 0 24 24" {_S} stroke-width="2.2"><path d="m9 6 6 6-6 6"/></symbol>',
})
SPRITE = '<svg width="0" height="0" style="position:absolute" aria-hidden="true"><defs>' + "".join(ICONS.values()) + "</defs></svg>"

ICONS.update({
    "i-building": f'<symbol id="i-building" viewBox="0 0 24 24" {_S}><rect x="4" y="3" width="16" height="18" rx="1.5"/><path d="M8 7h2M14 7h2M8 11h2M14 11h2M8 15h2M14 15h2M10 21v-3h4v3"/></symbol>',
    "i-card": f'<symbol id="i-card" viewBox="0 0 24 24" {_S}><rect x="2.5" y="5" width="19" height="14" rx="2.5"/><path d="M2.5 10h19M6.5 15h4"/></symbol>',
    "i-badge": f'<symbol id="i-badge" viewBox="0 0 24 24" {_S}><path d="m12 2.5 2.4 1.8 3 .1.9 2.9 2.4 1.8-.9 2.9.9 2.9-2.4 1.8-.9 2.9-3 .1L12 21.5l-2.4-1.8-3-.1-.9-2.9L3.3 15l.9-2.9-.9-2.9 2.4-1.8.9-2.9 3-.1z"/><path d="m8.5 12 2.5 2.5 4.5-5"/></symbol>',
    "i-chev": f'<symbol id="i-chev" viewBox="0 0 24 24" {_S} stroke-width="2.2"><path d="m9 6 6 6-6 6"/></symbol>',
})
SPRITE = '<svg width="0" height="0" style="position:absolute" aria-hidden="true"><defs>' + "".join(ICONS.values()) + "</defs></svg>"


def ico(name, cls="ic"):
    return f'<svg class="{cls}" aria-hidden="true"><use href="#{name}"/></svg>'


def photo(name, alt, cls="", sizes="(max-width: 760px) 100vw, 600px", eager=False):
    """Photo in assets/img/photos/<name>.(webp|jpg|jpeg|png), else empty string."""
    for ext in ("webp", "jpg", "jpeg", "png"):
        if os.path.exists(os.path.join(ROOT, "assets", "img", "photos", f"{name}.{ext}")):
            load = 'fetchpriority="high"' if eager else 'loading="lazy"'
            return f'<img class="{cls}" src="/assets/img/photos/{name}.{ext}" alt="{E(alt)}" sizes="{sizes}" {load} decoding="async">'
    return ""


# ---------------------------------------------------------------------------
# Arrondissements
# ---------------------------------------------------------------------------
def ordinal(n):
    return "st" if n % 10 == 1 and n != 11 else "nd" if n % 10 == 2 and n != 12 else "rd" if n % 10 == 3 and n != 13 else "th"


def build_arr():
    out = []
    for n, (surnom, pop, cps, quartiers, reperes, metros, habitat) in ARRONDISSEMENTS.items():
        suf = ordinal(n)
        out.append({
            "n": n, "suf": suf, "num": f"{n}{suf}", "slug": f"locksmith-paris-{n}{suf}",
            "fr_slug": f"serrurier-paris-{n}{'er' if n == 1 else 'e'}",
            "court": f"Paris {n}{suf}", "nom": f"Paris {n}{suf} arrondissement", "surnom": surnom,
            "a": f"in the {n}{suf} arrondissement", "a_court": f"in Paris {n}{suf}",
            "pop": pop, "cp": cps, "quartiers": quartiers, "reperes": reperes, "metros": metros, "habitat": habitat,
        })
    for i, z in enumerate(out):
        z["url"] = f"/{z['slug']}/"
        z["prev"] = out[i - 1] if i > 0 else None
        z["next"] = out[i + 1] if i < len(out) - 1 else None
    return out


ARR = build_arr()


def et(lst):
    return lst[0] if len(lst) == 1 else ", ".join(lst[:-1]) + " and " + lst[-1]


def svc_url(s):
    return f"/services/{s['slug']}/"


def combo_url(s, z):
    return f"/{z['slug']}/{s['slug']}/"


def prix_txt(s, strong=False):
    if not s["prix_num"]:
        return "<strong>free quote</strong>" if strong else "free quote"
    p = eur(s["prix_num"])
    return f"from <strong>{p} incl. VAT</strong>" if strong else f"from {p} incl. VAT"


# ---------------------------------------------------------------------------
# Components
# ---------------------------------------------------------------------------
def btn_call(label=None, cls="btn btn-gold", track="call"):
    return f'<a class="{cls}" href="{TEL_HREF}" data-track="{track}">{ico("i-phone")}<span>{E(label or TEL)}</span></a>'


def btn_wa(text=WA_MSG, label="WhatsApp", cls="btn btn-outline-light", track="wa"):
    return f'<a class="{cls}" href="{E(wa_link(text))}" target="_blank" rel="noopener" data-track="{track}">{ico("i-wa")}<span>{E(label)}</span></a>'


def ticks(items, cls="ticks"):
    return f'<ul class="{cls}">' + "".join(f"<li>{ico('i-check')}<span>{E(i)}</span></li>" for i in items) + "</ul>"


def crumbs(items):
    parts = ['<a href="/">Home</a>']
    for label, url in items:
        parts.append(f'<a href="{url}">{E(label)}</a>' if url else f'<span aria-current="page">{E(label)}</span>')
    return '<nav class="crumbs" aria-label="Breadcrumb">' + ico("i-chev", "sep").join(parts) + "</nav>"


def stars(n=5, cls="st"):
    return '<span class="stars">' + "".join(ico("i-star", cls) for _ in range(n)) + "</span>"


G_LOGO = ('<svg class="g-logo" viewBox="0 0 48 48" aria-hidden="true"><path fill="#FFC107" d="M43.6 20.5H42V20H24v8h11.3C33.7 32.7 29.2 36 24 36c-6.6 0-12-5.4-12-12s5.4-12 12-12c3.1 0 5.8 1.2 7.9 3.1l5.7-5.7C34 6.1 29.3 4 24 4 12.9 4 4 12.9 4 24s8.9 20 20 20 20-8.9 20-20c0-1.3-.1-2.4-.4-3.5z"/>'
          '<path fill="#FF3D00" d="M6.3 14.7l6.6 4.8C14.7 15.1 19 12 24 12c3.1 0 5.8 1.2 7.9 3.1l5.7-5.7C34 6.1 29.3 4 24 4 16.3 4 9.7 8.3 6.3 14.7z"/>'
          '<path fill="#4CAF50" d="M24 44c5.2 0 9.9-2 13.4-5.2l-6.2-5.2C29.2 35.1 26.7 36 24 36c-5.2 0-9.6-3.3-11.3-8l-6.5 5C9.5 39.6 16.2 44 24 44z"/>'
          '<path fill="#1976D2" d="M43.6 20.5H42V20H24v8h11.3c-.8 2.2-2.2 4.2-4.1 5.6l6.2 5.2C37 39.2 44 34 44 24c0-1.3-.1-2.4-.4-3.5z"/></svg>')


def google_badge(cls="g-badge"):
    if not CONFIG["avis_note"]:
        return ""
    return (f'<a class="{cls}" href="{E(MAPS)}" target="_blank" rel="noopener">{G_LOGO}'
            f'<span><b>{CONFIG["avis_note"]}</b>{stars()}<small>{CONFIG["avis_nombre"]} Google reviews</small></span></a>')


def faq_html(faq):
    return '<div class="faq">' + "".join(
        f'<details{" open" if i == 0 else ""}><summary>{E(q)}<i aria-hidden="true"></i></summary><div><p>{a}</p></div></details>'
        for i, (q, a) in enumerate(faq)) + "</div>"


def ld_faq(faq):
    return {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": re.sub("<[^>]+>", "", a)}} for q, a in faq]}


def ld_crumbs(items):
    lst = [{"@type": "ListItem", "position": 1, "name": "Home", "item": URL + "/"}]
    for i, (label, url) in enumerate(items, start=2):
        lst.append({"@type": "ListItem", "position": i, "name": label, "item": URL + url})
    return {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": lst}


def ld_business(full=False):
    a = CONFIG["adresse"]
    d = {
        "@context": "https://schema.org", "@type": "Locksmith", "@id": BID, "name": NOM,
        "alternateName": CONFIG["raison_sociale"], "slogan": CONFIG["slogan"],
        "url": URL + "/", "telephone": CONFIG["tel_intl"], "email": CONFIG["email"],
        "image": URL + "/assets/img/og.jpg", "logo": URL + "/assets/img/icon-512.png",
        "priceRange": "€€", "currenciesAccepted": "EUR", "paymentAccepted": "Credit card, Cash, Bank transfer",
        "knowsLanguage": ["en", "fr"],
        "address": {"@type": "PostalAddress", "streetAddress": a["rue"], "postalCode": a["cp"], "addressLocality": a["ville"],
                    "addressRegion": "Île-de-France", "addressCountry": "FR"},
        "geo": {"@type": "GeoCoordinates", "latitude": CONFIG["lat"], "longitude": CONFIG["lng"]},
        "hasMap": MAPS, "sameAs": [CONFIG["instagram"]],
        "openingHoursSpecification": {"@type": "OpeningHoursSpecification",
                                      "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
                                      "opens": "00:00", "closes": "23:59"},
        "areaServed": [{"@type": "City", "name": "Paris"}],
    }
    if CONFIG["siret"]:
        d["identifier"] = {"@type": "PropertyValue", "propertyID": "SIRET", "value": CONFIG["siret"]}
    if full:
        d["areaServed"] += [{"@type": "AdministrativeArea", "name": z["nom"]} for z in ARR]
        d["hasOfferCatalog"] = {"@type": "OfferCatalog", "name": "Locksmith services in Paris", "itemListElement": [
            {"@type": "Offer", "itemOffered": {"@type": "Service", "name": s["nom"], "url": URL + svc_url(s)},
             **({"priceSpecification": {"@type": "PriceSpecification", "minPrice": s["prix_num"], "priceCurrency": "EUR"}} if s["prix_num"] else {})}
            for s in SERVICES]}
    return d


FORM_N = [0]


def lead_form(source, service=None, titre="Request a free quote", sous="We call you back quickly, 7 days a week.", arr="", hid=""):
    FORM_N[0] += 1
    n = FORM_N[0]
    opts = "".join(f'<option{" selected" if service == s["court"] else ""}>{E(s["court"])}</option>' for s in SERVICES)
    arr_opts = "".join(f'<option{" selected" if arr == z["court"] else ""}>{E(z["court"])}</option>' for z in ARR)
    return f'''<form class="lead-form" name="quote" method="POST" action="/thank-you/" data-netlify="true" netlify-honeypot="bot-field">
  <input type="hidden" name="form-name" value="quote"><input type="hidden" name="page" value="{E(source)}">
  <p hidden><label>Leave empty <input name="bot-field"></label></p>
  <div class="form-head"><h3{f' id="{hid}"' if hid else ""}>{E(titre)}</h3><p>{E(sous)}</p></div>
  <div class="grid2">
    <label for="n{n}">Name<input id="n{n}" name="name" autocomplete="name" required placeholder="Your name"></label>
    <label for="t{n}">Phone<input id="t{n}" name="phone" type="tel" inputmode="tel" autocomplete="tel" required pattern="[0-9+ .()-]{{8,}}" placeholder="+33 6 00 00 00 00"></label>
  </div>
  <div class="grid2">
    <label for="s{n}">What do you need?<select id="s{n}" name="service">{opts}<option{" selected" if not service else ""}>Other request</option></select></label>
    <label for="a{n}">Arrondissement<select id="a{n}" name="arrondissement"><option value="">Choose…</option>{arr_opts}</select></label>
  </div>
  <label for="m{n}">Message<textarea id="m{n}" name="message" rows="3" placeholder="Type of door, situation, preferred time…"></textarea></label>
  <button class="btn btn-navy btn-block btn-lg" type="submit">{ico("i-mail")}<span>Send my request</span></button>
  <p class="form-legal">{ico("i-lock", "ic xs")}Your details are only used to reply to you. <a href="/privacy/">Privacy</a></p>
  <div class="form-ok" role="status" hidden>{ico("i-check")}<div><strong>Request received.</strong> We will call you back very soon. Emergency: <a href="{TEL_HREF}">{TEL}</a></div></div>
</form>'''


def btn_quote(service, label="Get a free quote", cls="btn btn-quote"):
    return f'<button type="button" class="{cls}" data-quote="{E(service)}">{ico("i-mail")}<span>{E(label)}</span></button>'


def quote_modal():
    """Fenêtre de devis, présente une fois par page ; ouverte par n'importe quel bouton [data-quote]."""
    return f'''<dialog class="qm" id="quote-modal" aria-labelledby="qm-title">
  <button type="button" class="qm-close" data-qm-close aria-label="Close">×</button>
  <div class="qm-side"><span class="live"><i></i>Available 24/7</span><p class="qm-svc" data-qm-service></p>
    <ul class="ticks small light"><li>{ico("i-check")}<span>Free quote, no obligation</span></li><li>{ico("i-check")}<span>Price confirmed before any work</span></li><li>{ico("i-check")}<span>English spoken</span></li></ul>
    <a class="qm-call" href="{TEL_HREF}" data-track="call_modal">{ico("i-phone")}<span><small>In a hurry? Call</small><b>{TEL}</b></span></a></div>
  {lead_form("popup", titre="Get your free quote", sous="Leave your number: we call you back within minutes, 24/7.", hid="qm-title")}
</dialog>'''


def contact_band(titre="Need a locksmith in Paris?", texte="Call us: a locksmith answers directly and gives you the price before travelling.",
                 source="/", service=None, arr=""):
    return f'''<section class="band" id="quote">
  <div class="wrap band-grid">
    <div class="band-text">
      <span class="eyebrow light">Immediate answer · 24/7</span>
      <h2>{E(titre)}</h2>
      <p>{E(texte)}</p>
      <a class="band-phone" href="{TEL_HREF}" data-track="call_band"><span class="ring">{ico("i-phone")}</span><span><small>Direct line, no call center</small><b>{TEL}</b></span></a>
      {ticks(["Price given before we travel", "Written quote signed before any work", "Detailed invoice for your insurer", "Card, cash or bank transfer"], "ticks light")}
    </div>
    {lead_form(source, service, arr=arr)}
  </div>
</section>'''


def side_box(titre="A locksmith available now", texte="Describe your situation on the phone: you get the price before anyone travels.", quote=None):
    return f'''<aside class="side-box">
  <div class="side-head"><span class="live"><i></i>Available 24/7</span><h3>{E(titre)}</h3></div>
  <div class="side-body">
    <p>{E(texte)}</p>
    {btn_call(cls="btn btn-gold btn-block btn-lg", track="call_side")}
    {btn_quote(quote, "Free quote: " + quote, "btn btn-navy btn-block") if quote else ""}
    {btn_wa(label="Send a photo", cls="btn btn-outline btn-block", track="wa_side")}
    {ticks(["Free quote, no obligation", "Damage-free opening in most cases", "Invoice accepted by insurers"], "ticks small")}
    {google_badge("g-badge compact")}
  </div>
</aside>'''


SLOTS = [("jour", "i-sun", "Day", "8am – 6pm"), ("soir", "i-sunset", "Evening", "6pm – 10pm"), ("nuit", "i-moon", "Night", "10pm – 8am")]


def tarif_table():
    urg = [t for t in TARIFS if all(t[1:])]
    trav = [t for t in TARIFS if not all(t[1:])]

    def prix_html(v):
        apd = v.startswith("From ")
        m = v[5:] if apd else v
        return f'<span class="pv-from">{"from" if apd else ""}</span><b class="pv-num">{E(m)}</b>'
    tabs = "".join(f'<button type="button" role="tab" data-slot="{k}" aria-selected="{"true" if k == "jour" else "false"}">{ico(i)}<span><b>{l}</b><small>{h}</small></span></button>'
                   for k, i, l, h in SLOTS)
    rows = "".join(f'<li><span class="pl-name">{E(p)}</span><span class="pl-price">'
                   + "".join(f'<span class="pv" data-slot="{k}"{"" if k == "jour" else " hidden"}>{prix_html(v)}</span>' for (k, _, _, _), v in zip(SLOTS, prix))
                   + "</span></li>" for p, *prix in urg)
    trv = "".join(f'<li><span class="pl-name">{E(p)}</span><span class="pl-price"><span class="pv">{prix_html(j)}</span></span></li>' for p, j, *_ in trav)
    return f'''<div class="tarifs">
  <div class="tarif-card main" data-tarifs>
    <div class="tc-head"><div><span class="eyebrow light">24/7 emergency call-outs</span><h3>Prices depend on the time of day</h3></div><span class="tc-ttc">Incl. VAT</span></div>
    <div class="slot-tabs" role="tablist" aria-label="Time of call-out">{tabs}</div>
    <p class="slot-now" hidden></p>
    <ul class="price-list">{rows}</ul>
  </div>
  <div class="tarif-card">
    <div class="tc-head light"><div><span class="eyebrow">By appointment</span><h3>Works &amp; installation</h3></div></div>
    <ul class="price-list">{trv}</ul>
    <p class="tarif-foot">Daytime starting prices. Free detailed quote after a visit.</p>
  </div>
</div>
<p class="tarif-note">{ico("i-file")}<span>Prices include VAT and labor. The exact price depends on your door and lock: it is given on the phone, then confirmed by a written, signed quote before any work, as required by French regulations (decree of 24 January 2017).</span></p>'''


def logo_tile(nom, slug, folder):
    if slug and os.path.exists(os.path.join(ROOT, "assets", "img", folder, f"{slug}.webp")):
        return f'<li class="logo"><img src="/assets/img/{folder}/{slug}.webp" alt="{E(nom)}" title="{E(nom)}" loading="lazy" decoding="async" height="48"></li>'
    return ""


# Couleur de marque des assureurs affichés sans logo
INS_COLORS = {"GMF": "#00529b", "MMA": "#e30613", "Crédit Agricole Assurances": "#007d8f", "BNP Paribas Cardif": "#00915a",
              "Société Générale Assurances": "#e60028", "LCL": "#002f6c", "Crédit Mutuel": "#0060a9", "CIC": "#00a0e1",
              "La Banque Postale": "#003da5", "Banque Populaire": "#0065b1", "Allianz Direct": "#003781", "Leocare": "#1e1e50",
              "Mutuelle de Poitiers Assurances": "#003f7d"}


def insurer_item(nom, slug, hidden=False):
    ah = ' aria-hidden="true"' if hidden else ""
    if slug and os.path.exists(os.path.join(ROOT, "assets", "img", "assureurs", f"{slug}.webp")):
        return f'<li class="ins"{ah}><img src="/assets/img/assureurs/{slug}.webp" alt="{"" if hidden else E(nom)}" title="{E(nom)}" loading="lazy" decoding="async" height="40"></li>'
    col = INS_COLORS.get(nom, "#1c3168")
    return f'<li class="ins ins-name"{ah}><span style="color:{col}">{E(nom)}</span></li>'


def assureurs_strip(titre=True):
    # Deux bandes qui défilent en sens inverse (chaque bande est doublée pour une boucle continue)
    half = (len(ASSUREURS) + 1) // 2
    rows = ""
    for i, part in enumerate((ASSUREURS[:half], ASSUREURS[half:])):
        items = "".join(insurer_item(n, s) for n, s in part) + "".join(insurer_item(n, s, True) for n, s in part)
        rows += f'<div class="ins-row{" rev" if i else ""}" style="--n:{len(part)}"><ul class="ins-track">{items}</ul></div>'
    head = f'''<div class="strip-head"><p><b>Invoices recognized by French home insurers</b><span>Reimbursement depends on your policy · <a href="/insurance/">learn more</a></span></p></div>''' if titre else ""
    return f'''<section class="strip">
  <div class="wrap">{head}</div>
  <div class="ins-marquee" aria-label="Home insurers">{rows}</div>
  <div class="wrap"><p class="fine">{E(NOM)} is an independent company with no partnership with these insurers; names and logos belong to their respective owners.</p></div>
</section>'''


def marques_block():
    def item(nom, slug, hidden=False):
        ah = ' aria-hidden="true"' if hidden else ""
        if slug and os.path.exists(os.path.join(ROOT, "assets", "img", "marques", f"{slug}.webp")):
            return f'<li class="ins"{ah}><img src="/assets/img/marques/{slug}.webp" alt="{"" if hidden else E(nom)}" title="{E(nom)}" loading="lazy" decoding="async" height="40"></li>'
        return f'<li class="ins ins-name"{ah}><span>{E(nom)}</span></li>'
    half = (len(MARQUES) + 1) // 2
    rows = ""
    for i, part in enumerate((MARQUES[:half], MARQUES[half:])):
        items = "".join(item(n, s) for n, s, _ in part) + "".join(item(n, s, True) for n, s, _ in part)
        rows += f'<div class="ins-row{" rev" if i else ""}" style="--n:{len(part)}"><ul class="ins-track">{items}</ul></div>'
    cats = {}
    for n, _, c in MARQUES:
        cats.setdefault(c, []).append(n)
    txt = " · ".join(f"<b>{E(c)}</b>: {E(', '.join(l))}" for c, l in cats.items())
    return f'''<div class="brands">
  <div class="ins-marquee brands-marquee" aria-label="Lock and door brands">{rows}</div>
  <p class="fine">{txt}.</p>
</div>'''


def arr_grid(link=lambda z: z["url"], label=lambda z: z["surnom"], cls="arr-grid"):
    return f'<div class="{cls}">' + "".join(
        f'<a href="{link(z)}"><span class="thumb"><img src="/assets/img/arr/{z["n"]}.webp" alt="" width="64" height="64" loading="lazy" decoding="async">'
        f'<b>{z["n"]}<span>{z["suf"]}</span></b></span><span class="t"><strong>Paris {z["num"]}</strong><small>{E(label(z))}</small></span>{ico("i-chev", "ic go")}</a>'
        for z in ARR) + "</div>"


def load_reviews():
    """Avis : _src/reviews.json (mis à jour automatiquement si un script le remplit) + liste AVIS de data.py."""
    lst = list(AVIS)
    path = os.path.join(ROOT, "_src", "reviews.json")
    if os.path.exists(path):
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
        lst += data.get("reviews", data) if isinstance(data, dict) else data
    return [r for r in lst if r.get("texte") or r.get("text")]


REVIEWS = load_reviews()


def review_card(r, hidden=False):
    auteur = r.get("auteur") or r.get("author") or "Google user"
    texte = r.get("texte") or r.get("text") or ""
    note = int(r.get("note") or r.get("rating") or 5)
    meta = " · ".join(x for x in (r.get("date", ""), r.get("arr", "")) if x)
    return (f'<article class="review"{" aria-hidden=\"true\"" if hidden else ""}><header><span class="av">{E(auteur[:1].upper())}</span>'
            f'<div><b>{E(auteur)}</b><small>{E(meta)}</small></div>{G_LOGO}</header>{stars(note)}<p>{E(texte)}</p></article>')


def review_cards():
    if not REVIEWS:
        return ""
    # Deux rangées qui défilent en sens inverse ; chaque rangée est doublée pour une boucle continue
    half = (len(REVIEWS) + 1) // 2
    rows = [REVIEWS[:half], REVIEWS[half:]] if len(REVIEWS) > 6 else [REVIEWS]
    out = ""
    for i, row in enumerate(rows):
        cards = "".join(review_card(r) for r in row)
        dup = "".join(review_card(r, True) for r in row)
        out += f'<div class="rv-row{" rev" if i else ""}" style="--n:{len(row)}"><div class="rv-track">{cards}{dup}</div></div>'
    return f'<div class="rv-marquee" aria-label="Google reviews">{out}</div>'


def reviews_block(titre="What our customers say"):
    note = ""
    if CONFIG["avis_note"]:
        note = f'''<div class="score-card">
  <div class="score-top">{G_LOGO}<span>Google reviews</span></div>
  <div class="score"><b>{CONFIG["avis_note"]}</b><span>/5</span></div>
  {stars(5, "st lg")}
  <p>Average rating from <b>{CONFIG["avis_nombre"]} reviews</b> posted by our customers</p>
  <a class="btn btn-navy btn-block" href="{E(MAPS)}" target="_blank" rel="noopener">Read our Google reviews</a>
  <a class="btn btn-outline btn-block" href="{E(AVIS_URL)}" target="_blank" rel="noopener">Leave a review</a>
</div>'''
    if CONFIG["reviews_widget"]:
        return f'''<section class="sec soft" id="reviews">
  <div class="wrap">
    <div class="sec-head"><span class="eyebrow">Customer reviews</span><h2>{E(titre)}</h2></div>
    <div class="reviews-widget">{CONFIG["reviews_widget"]}</div>
  </div>
</section>'''
    cards = review_cards()
    if cards:
        return f'''<section class="sec soft" id="reviews">
  <div class="wrap">
    <div class="sec-head split"><div><span class="eyebrow">Customer reviews</span><h2>{E(titre)}</h2></div>
    <div class="rv-summary">{note}</div></div>
  </div>
  {cards}
</section>'''
    side = f'''<div class="review-promise">
  <h3>Public, verifiable reviews</h3>
  <p>We don't publish anonymous testimonials on our website: our reviews are posted by customers directly on our Google Business Profile. They are public and dated, and we can neither edit nor delete them.</p>
  <ul class="ticks">
    <li>{ico("i-check")}<span>Posted directly by our customers on Google</span></li>
    <li>{ico("i-check")}<span>Available to read before you even call us</span></li>
    <li>{ico("i-check")}<span>Price, speed, tidiness: judge for yourself before calling</span></li>
  </ul>
</div>'''
    return f'''<section class="sec soft" id="reviews">
  <div class="wrap">
    <div class="sec-head"><span class="eyebrow">Customer reviews</span><h2>{E(titre)}</h2></div>
    <div class="reviews">{note}{side}</div>
  </div>
</section>'''


def map_embed():
    from urllib.parse import quote
    q = quote(f"Secure Lock Serrurerie @{CONFIG['lat']},{CONFIG['lng']}")
    return (f'<div class="map"><iframe title="{E(NOM)} on Google Maps" loading="lazy" referrerpolicy="no-referrer-when-downgrade" '
            f'src="https://maps.google.com/maps?q={q}&amp;z=14&amp;hl=en&amp;output=embed"></iframe>'
            f'<a class="map-link" href="{E(MAPS)}" target="_blank" rel="noopener">{G_LOGO}See our Google profile</a></div>')


def comparatif_block():
    rows = "".join(f'<li><div class="cmp-bad"><span class="cmp-ic">×</span><p>{E(b)}</p></div><div class="cmp-good">{ico("i-check")}<p>{E(g)}</p></div></li>'
                   for b, g in COMPARATIF)
    return f'''<div class="cmp">
  <div class="cmp-head"><span>Abusive practices to avoid</span><span>At {E(NOM)}</span></div>
  <ul>{rows}</ul>
</div>'''


def inclus_block(titre="What the price includes"):
    lis = "".join(f"<li>{ico('i-check')}<span>{E(i)}</span></li>" for i in INCLUS)
    return f'<div class="inclus"><h3>{E(titre)}</h3><ul>{lis}</ul></div>'


def engagements_short():
    lis = "".join(f'<li>{ico(i)}<span><b>{E(t.split(". ", 1)[1])}</b></span></li>' for i, t, _ in CHARTE[:6])
    return f'''<div class="eng-short"><h3>Our commitments, in writing</h3><ul>{lis}</ul>
  <a class="text-link" href="/our-commitments/">Read our trust charter {ico("i-arrow", "ic sm")}</a></div>'''


def company_card():
    rows = [("i-building", "Company", f"{E(CONFIG['raison_sociale'])}")]
    if CONFIG["siret"]:
        rows.append(("i-file", "SIRET (company no.)", siret_fmt()))
    rows += [("i-pin", "Registered office", E(adresse_txt())), ("i-phone", "Phone", f'<a href="{TEL_HREF}">{TEL}</a>'),
             ("i-mail", "Email", f'<a href="mailto:{CONFIG["email"]}">{CONFIG["email"]}</a>'),
             ("i-card", "Payment", "Card, cash, bank transfer")]
    if CONFIG["experience"]:
        rows.insert(1, ("i-award", "Experience", E(CONFIG["experience"])))
    if CONFIG["assurance_rc"]:
        rows.append(("i-shield", "Insurance", E(CONFIG["assurance_rc"])))
    lis = "".join(f'<li>{ico(i)}<span><small>{l}</small>{v}</span></li>' for i, l, v in rows)
    return f'''<div class="company">
  <div class="company-head"><img src="/assets/img/logo-112.webp" width="56" height="56" alt=""><div><b>{E(NOM)}</b><small>Company details</small></div></div>
  <ul>{lis}</ul>
  <a class="company-link" href="/legal-notice/">Full legal notice {ico("i-arrow", "ic sm")}</a>
</div>'''


# ---------------------------------------------------------------------------
# Page template
# ---------------------------------------------------------------------------
NAV = [("Emergency", "/emergency/"), ("Services", "/services/"), ("Prices", "/prices/"), ("Our commitments", "/our-commitments/"),
       ("Arrondissements", "/locksmith-paris/"), ("Contact", "/contact/")]
SITEMAP = []


def asset_v(rel):
    import hashlib
    try:
        with open(os.path.join(ROOT, rel), "rb") as f:
            return hashlib.md5(f.read()).hexdigest()[:10]
    except FileNotFoundError:
        return TODAY


def logo_html(cls="brand"):
    return (f'<a href="/" class="{cls}" aria-label="{E(NOM)} – home"><picture><source type="image/webp" srcset="/assets/img/logo-112.webp">'
            f'<img src="/assets/img/logo-112.png" width="52" height="52" alt=""></picture>'
            f'<span class="wordmark"><b>Secure Locksmith</b><small>Locksmith · Paris</small></span></a>')


def footer():
    svc = "".join(f'<li><a href="{svc_url(s)}">{E(s["nom"])}</a></li>' for s in SERVICES)
    arr = "".join(f'<a href="{z["url"]}">{z["n"]}<sup>{z["suf"]}</sup></a>' for z in ARR)
    siret = f"<br>SIRET {siret_fmt()}" if CONFIG["siret"] else ""
    return f'''<footer class="foot">
  <div class="wrap">
    <div class="foot-cta">
      <div><b>An emergency? A locksmith answers right away.</b><span>24/7 · Sundays and public holidays included</span></div>
      {btn_call(cls="btn btn-gold btn-lg", track="call_footer_cta")}
    </div>
    <div class="foot-grid">
      <div class="foot-brand">
        {logo_html("brand brand-foot")}
        <p>Locksmith in Paris, across all 20 arrondissements. 24/7 call-outs, price given before we travel, signed quote before any work, invoice for your insurer. English-speaking service.</p>
        <p class="foot-id">{E(CONFIG["raison_sociale"])}<br>{E(adresse_txt())}{siret}</p>
      </div>
      <div><h4>Services</h4><ul>{svc}</ul></div>
      <div><h4>Information</h4><ul><li><a href="/our-commitments/">Our commitments</a></li><li><a href="/prices/">Prices</a></li><li><a href="/insurance/">Insurance &amp; reimbursement</a></li><li><a href="/reviews/">Customer reviews</a></li><li><a href="/faq/">FAQ</a></li><li><a href="/advice/">Advice</a></li><li><a href="/contact/">Contact</a></li></ul></div>
      <div><h4>Contact</h4><ul class="foot-contact"><li><a href="{TEL_HREF}" data-track="call_footer">{ico("i-phone", "ic sm")}{TEL}</a></li><li><a href="mailto:{CONFIG["email"]}">{ico("i-mail", "ic sm")}{CONFIG["email"]}</a></li><li><a href="{CONFIG["instagram"]}" target="_blank" rel="noopener me">{ico("i-insta", "ic sm")}Instagram</a></li></ul>
        <h4 class="mt">Arrondissements</h4><div class="arr-mini">{arr}</div></div>
    </div>
    <div class="foot-bottom">
      <span>© {TODAY[:4]} {E(NOM)} – {E(CONFIG["raison_sociale"])}</span>
      <nav><a href="/legal-notice/">Legal notice</a><a href="/privacy/">Privacy</a><a href="/site-map/">Site map</a><button type="button" class="linklike" data-open-consent>Cookies</button></nav>
    </div>
  </div>
</footer>'''


def page(path, title, desc, body, ld=(), active=None, robots="index, follow", og_type="website"):
    canonical = URL + path
    nav = "".join(f'<a href="{u}"{" class=\"nav-urg\"" if u == "/emergency/" else ""}{" aria-current=\"page\"" if u == active else ""}>{"<i></i>" if u == "/emergency/" else ""}{E(l)}</a>' for l, u in NAV)
    ld_html = "".join(f'<script type="application/ld+json">{json.dumps(d, ensure_ascii=False)}</script>\n' for d in ld)
    ads = CONFIG["ads_id"]
    conv = json.dumps({k: f"{ads}/{v}" for k, v in CONFIG["ads_conv"].items() if v}) if ads else "{}"
    ads_js = f"gtag('config','{ads}');" if ads else ""
    note = (f'<a class="tb-rating" href="{E(MAPS)}" target="_blank" rel="noopener">{stars(5, "st xs")}<b>{CONFIG["avis_note"]}/5</b> on Google ({CONFIG["avis_nombre"]} reviews)</a>'
            if CONFIG["avis_note"] else "")
    doc = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<script>
window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}
gtag('consent','default',{{ad_storage:'denied',analytics_storage:'denied',ad_user_data:'denied',ad_personalization:'denied',functionality_storage:'granted',security_storage:'granted',wait_for_update:500}});
window.SLP_CONV={conv};
(function(){{
  var c=null;try{{c=JSON.parse(localStorage.getItem('slp_cookies'));}}catch(e){{}}
  window.SLP_CHOICE=(c&&c.v&&Date.now()-c.t<15552000000)?c.v:null;
  window.slpTags=function(){{
    if(window.slpTagsOn)return;window.slpTagsOn=true;
    gtag('consent','update',{{ad_storage:'granted',analytics_storage:'granted',ad_user_data:'granted',ad_personalization:'granted'}});
    (function(w,d,s,l,i){{w[l]=w[l]||[];w[l].push({{'gtm.start':new Date().getTime(),event:'gtm.js'}});var f=d.getElementsByTagName(s)[0],j=d.createElement(s);j.async=true;j.src='https://www.googletagmanager.com/gtm.js?id='+i;f.parentNode.insertBefore(j,f);}})(window,document,'script','dataLayer','{CONFIG["gtm_id"]}');
    var g=document.createElement('script');g.async=true;g.src='https://www.googletagmanager.com/gtag/js?id={CONFIG["ga_id"]}';document.head.appendChild(g);
    gtag('js',new Date());gtag('config','{CONFIG["ga_id"]}');{ads_js}
  }};
  if(window.SLP_CHOICE==='granted')window.slpTags();
}})();
</script>
<title>{E(title)}</title>
<meta name="description" content="{E(desc)}">
<meta name="robots" content="{robots}, max-image-preview:large">
<link rel="canonical" href="{canonical}">
<meta name="google-site-verification" content="{CONFIG["google_verification"]}">
<meta name="theme-color" content="#0d1233">
<meta name="geo.region" content="FR-75">
<meta name="geo.placename" content="Paris">
<meta name="geo.position" content="48.8566;2.3522">
<meta property="og:type" content="{og_type}">
<meta property="og:locale" content="en_GB">
<meta property="og:site_name" content="{E(NOM)}">
<meta property="og:title" content="{E(title)}">
<meta property="og:description" content="{E(desc)}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{URL}/assets/img/og.jpg">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="/favicon.ico" sizes="48x48">
<link rel="icon" href="/assets/img/logo-112.png" type="image/png">
<link rel="apple-touch-icon" href="/assets/img/apple-touch-icon.png">
<link rel="manifest" href="/site.webmanifest">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Archivo:wght@600;700;800&family=Manrope:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/assets/css/main.css?v={asset_v("assets/css/main.css")}">
{ld_html}</head>
<body>
{SPRITE}
<div class="topbar">
  <div class="wrap tb-in">
    <span class="tb-live"><i></i>Locksmiths available now in Paris</span>
    <span class="tb-items"><span>{ico("i-file", "ic xs")}Signed quote before any work</span><span>{ico("i-shield", "ic xs")}Invoices accepted by insurers</span></span>
    {note}
  </div>
</div>
<header class="top" id="top">
  <div class="wrap top-in">
    {logo_html()}
    <nav class="menu" aria-label="Main navigation">{nav}</nav>
    <div class="top-cta">
      <a class="top-tel" href="{TEL_HREF}" data-track="call_header"><span class="ring">{ico("i-phone")}</span><span><small>24/7 emergency</small><b>{TEL}</b></span></a>
      <button class="burger" type="button" aria-label="Menu" aria-expanded="false" aria-controls="drawer"><i></i><i></i><i></i></button>
    </div>
  </div>
  <nav class="drawer" id="drawer" aria-label="Mobile navigation"><a href="/">Home</a>{nav}<a class="btn btn-gold" href="{TEL_HREF}" data-track="call_drawer">{ico("i-phone")}<span>Call {TEL}</span></a></nav>
</header>
<main>
{body}
</main>
{footer()}
{quote_modal()}
<div class="cookies" id="cookies" role="dialog" aria-label="Cookies" hidden>
  <p><strong>Your privacy</strong> With your consent, we measure website traffic (Google Analytics, Google Tag Manager) to improve it. Nothing is loaded without your consent. <a href="/privacy/#cookies">Learn more</a></p>
  <div><button type="button" class="btn btn-outline btn-sm" data-cookies="denied">Decline</button><button type="button" class="btn btn-navy btn-sm" data-cookies="granted">Accept</button></div>
</div>
<div class="dock">
  <a class="btn btn-gold" href="{TEL_HREF}" data-track="call_dock">{ico("i-phone")}<span>Call now · 24/7</span></a>
  <a class="btn btn-wa" href="{WA}" target="_blank" rel="noopener" data-track="wa_dock" aria-label="WhatsApp">{ico("i-wa")}</a>
</div>
<script src="/assets/js/main.js?v={asset_v("assets/js/main.js")}" defer></script>
</body>
</html>
'''
    out = os.path.join(ROOT, path.lstrip("/"), "index.html") if path.endswith("/") else os.path.join(ROOT, path.lstrip("/"))
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "w", encoding="utf-8") as f:
        f.write(doc)
    if robots.startswith("index"):
        SITEMAP.append(path)


PARIS_BG = {
    "tour-eiffel": "The Eiffel Tower at sunset", "toits-de-paris": "The rooftops of Paris",
    "notre-dame": "Notre-Dame de Paris and the Seine", "pantheon": "The Panthéon", "conciergerie": "The Conciergerie on the Seine",
    "place-des-victoires": "Place des Victoires", "sacre-coeur": "The Sacré-Cœur in Montmartre",
    "vue-sacre-coeur": "View of Montmartre", "avenue-etoile": "Parisian avenue seen from the Arc de Triomphe", "mairie": "A Paris town hall",
}
BG_BY_ARR = {1: "conciergerie", 2: "place-des-victoires", 4: "notre-dame", 5: "pantheon", 7: "tour-eiffel", 8: "toits-de-paris",
             16: "tour-eiffel", 17: "avenue-etoile", 18: "sacre-coeur", 19: "vue-sacre-coeur"}
BG_ROTATION = ["toits-de-paris", "avenue-etoile", "notre-dame", "pantheon", "conciergerie", "place-des-victoires", "vue-sacre-coeur", "mairie", "sacre-coeur"]
_BG_N = [0]


def zone_bg(z):
    return BG_BY_ARR.get(z["n"]) or BG_ROTATION[z["n"] % len(BG_ROTATION)]


def bg_img(name, eager=True):
    if not name or not os.path.exists(os.path.join(ROOT, "assets", "img", "paris", f"{name}.webp")):
        return ""
    return (f'<picture class="bg"><source media="(max-width: 760px)" srcset="/assets/img/paris/{name}-m.webp">'
            f'<img src="/assets/img/paris/{name}.webp" alt="{E(PARIS_BG.get(name, "Paris"))}" {"fetchpriority=\"high\"" if eager else "loading=\"lazy\""} decoding="async"></picture>')


def hero(crumb_items, h1, lead, extra="", kicker=None, card=None, bg=None, quote=None):
    k = f'<span class="eyebrow light">{E(kicker)}</span>' if kicker else ""
    card = card if card is not None else hero_card()
    if bg is None:
        bg = BG_ROTATION[_BG_N[0] % len(BG_ROTATION)]
        _BG_N[0] += 1
    return f'''<section class="phero has-bg">
  {bg_img(bg)}
  <div class="wrap phero-grid">
    <div class="phero-text">
      {crumbs(crumb_items)}
      {k}
      <h1>{h1}</h1>
      <p class="lead">{lead}</p>
      <div class="cta-row">{btn_call(cls="btn btn-gold btn-lg", track="call_hero")}{btn_quote(quote, cls="btn btn-quote btn-lg") if quote else btn_wa(cls="btn btn-outline-light btn-lg", track="wa_hero")}</div>
      {extra}
    </div>
    {card}
  </div>
</section>'''


def hero_card(prix="from €110 incl. VAT", label="Door opening"):
    return f'''<aside class="hcard">
  <ul>
    <li>{ico("i-euro")}<span><small>{E(label)}</small><b>{E(prix)}</b></span></li>
    <li>{ico("i-clock")}<span><small>Average arrival time in Paris</small><b>≈ 30 minutes</b></span></li>
    <li>{ico("i-file")}<span><small>Quote</small><b>Free, signed before any work</b></span></li>
  </ul>
  {google_badge("g-badge compact")}
</aside>'''


# ---------------------------------------------------------------------------
# Home
# ---------------------------------------------------------------------------
HOME_FAQ = [
    ("How much does it cost to open a door in Paris?", "A slammed door is opened for €110 incl. VAT during the day (8am–6pm), €150 in the evening and €220 at night. The price is given on the phone, then confirmed in a written quote before any work."),
    ("Do you cover the whole of Paris?", "Yes, all 20 arrondissements, from the 1st to the 20th, 24/7, public holidays included. Our locksmiths are spread across the city so they can get to you quickly."),
    ("How quickly can you get here?", "About 30 minutes on average within Paris. The exact time depends on traffic and is given on the phone before the locksmith sets off."),
    ("Is the quote free?", "Yes, free and with no obligation. Nothing is done without your signature, and you remain free to say no."),
    ("Do you speak English?", "Yes. You can call us or message us on WhatsApp in English, and the quote and invoice are explained to you clearly."),
    ("Can my insurance reimburse me?", "Often, yes: break-in, theft or loss of keys, depending on your policy. Our detailed invoice is accepted by French home insurers."),
    ("How can I pay?", "By card, cash or bank transfer. You always receive an invoice."),
]

MOIS = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]


def fr_date(iso):
    y, m, d = iso.split("-")
    return f"{int(d)} {MOIS[int(m) - 1]} {y}"


def svc_rows(lst, tag="h3", link=svc_url):
    return '<div class="svc-rows">' + "".join(f'''<div class="svc-row"><span class="svc-ic">{ico(s["icon"])}</span>
  <div><{tag}><a class="svc-link" href="{link(s)}">{E(s["nom"])}</a></{tag}><p>{E(s["resume"])}</p></div><span class="svc-prix">{E(s["prix"])}{ico("i-chev", "ic go")}</span>{btn_quote(s["court"], "Quote", "btn-q")}</div>''' for s in lst) + "</div>"


def urgences_block(light=False):
    cards = "".join(f'''<a class="urg" href="{svc_url(SVC_BY_SLUG[slug])}">
  <span class="urg-ic">{ico(SVC_BY_SLUG[slug]["icon"])}</span>
  <span class="urg-t"><b>{E(t)}</b><small>{E(conseil)}</small></span>
  <span class="urg-p"><small>{"daytime" if prix != "quote" else "price"}</small>{E("free quote" if prix == "quote" else prix)}</span>
</a>''' for t, slug, prix, conseil in URGENCES)
    return f'''<div class="urg-grid{" light" if light else ""}">{cards}</div>'''


def urgence_section():
    return f'''<section class="urgence" id="emergency">
  <div class="wrap">
    <div class="urg-head">
      <div>
        <span class="urg-badge"><i></i>Emergency 24/7</span>
        <h2>An emergency? A locksmith at your door in about 30 minutes</h2>
        <p>Night, weekend, public holiday: a locksmith answers and sets off right away. The price is given on the phone, before anyone travels.</p>
      </div>
      <a class="urg-call" href="{TEL_HREF}" data-track="call_urgence"><span class="ring">{ico("i-phone")}</span><span><small>Direct line</small><b>{TEL}</b></span></a>
    </div>
    {urgences_block()}
    <p class="urg-foot">Daytime prices (8am–6pm) shown as a guide. Evening and night: see the <a href="/prices/">full price list</a>. <a href="/emergency/">What to do in an emergency</a></p>
  </div>
</section>'''


def svc_cards(lst=None):
    out = []
    for s in (lst if lst is not None else SVC_URG):
        prix = f'<small>from (incl. VAT)</small><b>{eur(s["prix_num"])}</b>' if s["prix_num"] else "<small>price</small><b>Free quote</b>"
        ph = photo(s["slug"], s["nom"], "svc-photo", "(max-width: 760px) 100vw, 380px")
        out.append(f'''<article class="svc{" has-photo" if ph else ""}">
  {ph}
  <div class="svc-body">
    <span class="svc-ic">{ico(s["icon"])}</span>
    <h3><a class="svc-link" href="{svc_url(s)}">{E(s["nom"])}</a></h3>
    <p>{E(s["resume"])}</p>
    <div class="svc-foot"><span class="svc-prix">{prix}</span><span class="svc-acts">{btn_quote(s["court"], "Quote", "btn-q")}<a class="svc-go" href="{svc_url(s)}">Details {ico("i-arrow", "ic sm")}</a></span></div>
  </div>
</article>''')
    if len(out) % 3:
        out.append(f'''<a class="svc svc-cta" href="{TEL_HREF}" data-track="call_svc_grid">
  <div class="svc-body"><span class="svc-ic">{ico("i-phone")}</span><h3>Another emergency?</h3>
  <p>Garage door, shop, old lock… Describe the situation and we'll tell you straight away whether we can help, and at what price.</p>
  <div class="svc-foot"><span class="svc-prix"><small>direct line 24/7</small><b>{TEL}</b></span><span class="svc-go">Call {ico("i-arrow", "ic sm")}</span></div></div>
</a>''')
    return '<div class="svc-grid">' + "".join(out) + "</div>"


def svc_tiles():
    """Accueil : grille compacte des 10 services (icône, nom, prix), un clic mène à la page du service."""
    tiles = "".join(f'''<a class="stile" href="{svc_url(s)}">
  <span class="svc-ic">{ico(s["icon"])}</span>
  <b>{E(s["court"])}</b>
  <span class="stile-p">{("from " + eur(s["prix_num"])) if s["prix_num"] else "Free quote"}</span>
  {'<span class="stile-tag">24/7</span>' if s["cat"] == "urgence" else ""}
</a>''' for s in SERVICES)
    return f'<div class="stiles">{tiles}</div><p class="stiles-more"><a class="text-link" href="/services/">All services, prices and details {ico("i-arrow", "ic sm")}</a></p>'


def articles_cards(lst):
    return '<div class="posts">' + "".join(f'''<article class="post">
  <div class="post-top"><span class="post-ic">{ico(a["icon"])}</span><span class="post-cat">{E(a["cat"])}</span></div>
  <h3><a href="/advice/{a["slug"]}/">{E(a["court"])}</a></h3>
  <p>{E(a["desc"])}</p>
  <span class="post-more"><time datetime="{a["date"]}">{fr_date(a["date"])}</time><span>Read {ico("i-arrow", "ic sm")}</span></span>
</article>''' for a in lst) + "</div>"


def engagements():
    items = [
        ("i-euro", "Price given before we travel", "You describe the situation and we give you the price including VAT. It doesn't change on the way."),
        ("i-file", "Signed quote before any work", "As required by French regulations: nothing starts without your written agreement."),
        ("i-door", "Damage-free opening first", "Shims, picking, cylinder bypass: we preserve your lock whenever possible."),
        ("i-shield", "Leading brands", "Cylinders and locks from recognized manufacturers, A2P-certified models on request."),
        ("i-card", "Transparent payment", "Card, cash or bank transfer, with a detailed invoice every time."),
        ("i-phone", "A locksmith on the line", "No call center: a professional answers, day and night, in English or French."),
    ]
    return '<div class="engage">' + "".join(f'<div>{ico(i)}<h3>{E(t)}</h3><p>{E(d)}</p></div>' for i, t, d in items) + "</div>"


def build_home():
    visual = photo("home", f"{NOM}, locksmith in Paris", "hero-photo", "(max-width: 1100px) 100vw, 560px", eager=True)
    if not visual and os.path.exists(os.path.join(ROOT, "assets", "img", "photos", "hero-round.webp")):
        visual = '<picture class="emblem photo-round"><img src="/assets/img/photos/hero-round.webp" width="440" height="440" alt="Locksmith opening a front door in Paris" fetchpriority="high"></picture>'
    if not visual:
        visual = '<picture class="emblem"><source type="image/webp" srcset="/assets/img/logo-512.webp"><img src="/assets/img/icon-512.png" width="440" height="440" alt="Secure Locksmith Paris logo" fetchpriority="high"></picture>'
    equipe = photo("team", "Locksmith advising customers at their front door", "about-photo")
    about_visual = equipe or company_card()
    body = f'''<section class="hero has-bg">
  {bg_img("tour-eiffel")}
  <div class="wrap hero-grid">
    <div class="hero-text">
      <span class="eyebrow light">Locksmith in Paris · all 20 arrondissements</span>
      <h1>Locksmith in Paris,<br><span class="gold">24/7</span></h1>
      <p class="lead">Locked out, jammed lock, broken key, break-in: a qualified, English-speaking locksmith comes to you in about 30 minutes on average. The price is given on the phone and the quote is signed before any work.</p>
      <div class="cta-row">{btn_call(cls="btn btn-gold btn-xl", track="call_hero")}<a class="btn btn-outline-light btn-xl" href="#quote">{ico("i-mail")}<span>Free quote</span></a></div>
      <div class="hero-proof">
        {google_badge("g-badge dark")}
        <ul class="proof-list"><li>{ico("i-check")}Door opening from €110</li><li>{ico("i-check")}No hidden fees</li><li>{ico("i-check")}Invoice for your insurer</li></ul>
      </div>
    </div>
    <div class="hero-visual">
      {visual}
      <div class="float f1"><span class="live"><i></i>Available now</span><b>Arrival ≈ 30 min</b></div>
      <div class="float f2">{ico("i-shield")}<span><b>Signed quote</b><small>before every job</small></span></div>
    </div>
  </div>
</section>
{urgence_section()}
{assureurs_strip()}
<section class="sec" id="services">
  <div class="wrap">
    <div class="sec-head split">
      <div><span class="eyebrow">Our services</span><h2>Every locksmith service, everywhere in Paris</h2></div>
      <p>Apartment, townhouse, shop, cellar or storage room: we work on every type of door and lock, from old Parisian landing doors to multi-point armored doors.</p>
    </div>
    {svc_tiles()}
  </div>
</section>
<section class="sec soft">
  <div class="wrap about">
    <div class="about-text">
      <span class="eyebrow">Why trust us</span>
      <h2>An identified Paris locksmith who commits in writing</h2>
      <p class="lead-dark">Emergency locksmiths have a bad reputation, often for good reason. At {E(NOM)}, we have chosen the opposite approach: an identified company, published prices and commitments you can check.</p>
      <p class="about-p">When you are stuck outside your door, often late at night, you have neither the time nor the energy to compare offers. That is exactly when nasty surprises happen, especially if you don't speak French. Our answer is simple: you know the price before the locksmith sets off, you sign a quote before he starts, and you receive a detailed invoice at the end. No "extra charges" discovered on site, no lock replaced for no reason.</p>
      <p class="about-p">We work only in Paris. That focus lets us arrive quickly and know Parisian doors well: landing doors in Haussmann buildings, multi-point armored doors, old locks and modern badge-access residences.</p>
      {engagements()}
      <a class="btn btn-navy" style="margin-top:34px" href="/our-commitments/">{ico("i-file")}<span>Read our trust charter</span></a>
    </div>
    <div class="about-side">{about_visual}{company_card() if equipe else ""}</div>
  </div>
</section>
<section class="sec">
  <div class="wrap">
    <div class="sec-head split">
      <div><span class="eyebrow">Locksmith scams</span><h2>What you will never see from us</h2></div>
      <p>Emergency locksmith services are among the sectors generating the most complaints to the French consumer protection authority (DGCCRF). Here, point by point, are the most common abusive practices and how we work instead.</p>
    </div>
    {comparatif_block()}
    <p class="cmp-foot">Unsure about a locksmith? Read our guide <a href="/advice/spot-an-honest-locksmith/">How to spot an honest locksmith</a>.</p>
  </div>
</section>
<section class="sec" id="prices">
  <div class="wrap">
    <div class="sec-head split">
      <div><span class="eyebrow">Prices</span><h2>Clear prices, published before any work</h2></div>
      <p>Our prices depend on the time of the call-out. They are shown here, given on the phone and confirmed in writing: you know what you will pay before the locksmith sets off.</p>
    </div>
    {tarif_table()}
  </div>
</section>
<section class="sec navy">
  <div class="wrap">
    <div class="sec-head center"><span class="eyebrow light">How it works</span><h2>What happens when you call us</h2></div>
    <ol class="steps">
      <li><b>1</b><h3>You call</h3><p>You describe the door and the situation, or send a photo on WhatsApp.</p></li>
      <li><b>2</b><h3>Price given</h3><p>You get the price including VAT straight away, before the locksmith sets off.</p></li>
      <li><b>3</b><h3>Signed quote</h3><p>On site, the price is confirmed in writing. Nothing starts without your signature.</p></li>
      <li><b>4</b><h3>Work &amp; invoice</h3><p>Careful work and a detailed invoice to send to your insurer.</p></li>
    </ol>
    <div class="steps-cta">{btn_call("Call a locksmith", cls="btn btn-gold btn-lg", track="call_steps")}<span>or send a photo on <a href="{E(wa_link(WA_MSG))}" target="_blank" rel="noopener" data-track="wa_steps">WhatsApp</a></span></div>
  </div>
</section>
{reviews_block()}
<section class="sec">
  <div class="wrap">
    <div class="sec-head split">
      <div><span class="eyebrow">Brands</span><h2>We work on all the major brands</h2></div>
      <p>Locks, cylinders, armored doors and smart locks: our locksmiths know the main manufacturers and carry common parts in their van.</p>
    </div>
    {marques_block()}
  </div>
</section>
<section class="sec soft" id="arrondissements">
  <div class="wrap">
    <div class="sec-head split">
      <div><span class="eyebrow">Service area</span><h2>A locksmith in every Paris arrondissement</h2></div>
      <p>We work exclusively within Paris. Choose your arrondissement to see the neighborhoods we cover and our services near you.</p>
    </div>
    {arr_grid()}
  </div>
</section>
<section class="sec" id="faq">
  <div class="wrap faq-wrap">
    <div class="sec-head">
      <span class="eyebrow">FAQ</span>
      <h2>Your questions, our answers</h2>
      <p>Another question? Call us, we answer 24/7.</p>
      <a class="btn btn-outline" href="/faq/">All questions</a>
    </div>
    {faq_html(HOME_FAQ)}
  </div>
</section>
<section class="sec soft">
  <div class="wrap">
    <div class="sec-head split">
      <div><span class="eyebrow">Advice</span><h2>Practical guides from our locksmiths</h2></div>
      <p><a class="text-link" href="/advice/">See all our advice {ico("i-arrow", "ic sm")}</a></p>
    </div>
    {articles_cards(ARTICLES[:4])}
  </div>
</section>
{contact_band()}'''
    ld = [ld_business(full=True), ld_faq(HOME_FAQ),
          {"@context": "https://schema.org", "@type": "WebSite", "name": NOM, "url": URL + "/", "inLanguage": "en", "publisher": {"@id": BID}}]
    page("/", f"Locksmith Paris 24/7 – English-speaking – {TEL} | {NOM}",
         f"English-speaking locksmith in Paris, 24/7 across all 20 arrondissements. Door opening from €110 incl. VAT, price given before we travel, signed quote, invoice for your insurer. ☎ {TEL}",
         body, ld)


# ---------------------------------------------------------------------------
# Services
# ---------------------------------------------------------------------------
def before_after(s):
    """Curseur avant / après pour chaque réalisation fournie (assets/img/realisations/)."""
    items = []
    for r in REALISATIONS.get(s["slug"], []):
        b, a = (f"/assets/img/realisations/{r[k]}" for k in ("before", "after"))
        if not all(os.path.exists(os.path.join(ROOT, x.lstrip("/"))) for x in (b, a)):
            continue
        items.append(f'''<figure class="ba">
  <div class="ba-frame" style="--pos:50%">
    <img src="{a}" alt="After: {E(r.get("caption", s["nom"]))}" loading="lazy" decoding="async">
    <div class="ba-before"><img src="{b}" alt="Before" loading="lazy" decoding="async"></div>
    <span class="ba-tag l">Before</span><span class="ba-tag r">After</span>
    <span class="ba-handle" aria-hidden="true"></span>
    <input class="ba-range" type="range" min="0" max="100" value="50" aria-label="Compare before and after">
  </div>
  <figcaption>{E(r.get("caption", ""))}</figcaption>
</figure>''')
    if not items:
        return ""
    return f'<h2>Before &amp; after: our recent work</h2><p>Slide to compare. These are real jobs carried out by our team in Paris.</p><div class="ba-grid">{"".join(items)}</div>'


def build_services():
    items = (f'<h2 class="group-title">{ico("i-clock")}Emergency call-outs <small>24/7</small></h2>' + svc_rows(SVC_URG, "h3")
             + f'<h2 class="group-title">{ico("i-shield")}Works, armored doors &amp; installation <small>by appointment</small></h2>' + svc_rows(SVC_TRAV, "h3"))
    body = hero([("Services", None)], "Our locksmith services in Paris",
                "24/7 emergency call-outs (lockouts, jammed locks, broken keys, break-ins) and works by appointment (door armoring, armored doors, cellar doors, smart locks, mailbox locks), with their starting prices.",
                kicker="24/7")
    body += f'<section class="sec"><div class="wrap layout"><div>{items}</div>{side_box()}</div></section>'
    body += assureurs_strip() + f'<section class="sec"><div class="wrap"><div class="sec-head"><span class="eyebrow">Brands</span><h2>All the major brands</h2></div>{marques_block()}</div></section>' + contact_band(source="/services/")
    page("/services/", f"Locksmith services in Paris 24/7 | {NOM}",
         "All our locksmith services in Paris: door opening from €110, jammed locks, broken keys, lock replacement, smart locks, break-in repair, armored doors.",
         body, [ld_business(), ld_crumbs([("Services", "/services/")])], active="/services/")

    for s in SERVICES:
        path = svc_url(s)
        secs = "".join(f"<h2>{E(t)}</h2><p>{c}</p>" for t, c in s["sections"])
        others = "".join(f'<a class="chip" href="{svc_url(o)}">{ico(o["icon"])}{E(o["court"])}</a>' for o in SERVICES if o is not s)
        ph = photo(s["slug"], s["nom"], "prose-photo", "(max-width: 1100px) 100vw, 760px")
        content = f'''<article class="prose">
  <p class="intro">{s["intro"]}</p>
  {ph}
  {before_after(s)}
  <div class="note-box">{ico("i-euro")}<p>Price: {prix_txt(s, True)}. The exact price is given on the phone and confirmed in a written quote before any work. <a href="/prices/">Day, evening and night prices</a></p></div>
  {secs}
  <h2>{E(s["court"])}: choose your arrondissement</h2>
  {arr_grid(link=lambda z: f"{z['url']}#{s['slug']}", cls="arr-grid compact")}
  <h2>A clear, all-inclusive price</h2>
  <p>The price you are given on the phone includes VAT and labor. It is confirmed in a written quote before any work: if the situation on site turns out to be different from what you described, the locksmith explains why and offers a new quote, which you are free to refuse.</p>
  <div class="trust-duo">{inclus_block()}{engagements_short()}</div>
  <h2>Frequently asked questions</h2>
  {faq_html(s["faq"])}
  <h2>Our other services</h2><div class="chips">{others}</div>
</article>'''
        card = hero_card(prix_txt(s), s["court"])
        body = hero([("Services", "/services/"), (s["court"], None)], f'{E(s["nom"])} in Paris',
                    f'{E(s["resume"])} Anywhere in Paris, 24/7.',
                    ticks(["Price given before we travel", "Signed quote before any work", "Invoice for your insurer"], "ticks light inline"), kicker="Service", card=card, quote=s["court"])
        body += f'<section class="sec"><div class="wrap layout">{content}{side_box(quote=s["court"])}</div></section>'
        body += assureurs_strip() + reviews_block() + contact_band(f"{s['court']}? We'll be there fast.", "Call us or leave your details: we call you back with a clear price.", source=path, service=s["court"])
        ld = [ld_business(), ld_crumbs([("Services", "/services/"), (s["court"], path)]), ld_faq(s["faq"]),
              {"@context": "https://schema.org", "@type": "Service", "name": s["nom"], "serviceType": s["nom"], "url": URL + path,
               "provider": {"@id": BID}, "areaServed": {"@type": "City", "name": "Paris"},
               **({"offers": {"@type": "Offer", "priceSpecification": {"@type": "PriceSpecification", "minPrice": s["prix_num"], "priceCurrency": "EUR"}}} if s["prix_num"] else {})}]
        page(path, f'{s["nom"]} Paris 24/7 – {s["prix"]} | {NOM}',
             f'{s["nom"]} in Paris, 24/7. {s["resume"]} Price given before we travel. ☎ {TEL}', body, ld, active="/services/")


# ---------------------------------------------------------------------------
# Arrondissements
# ---------------------------------------------------------------------------
ARR_INTROS = [
    "Locked out {a}? {nom} sends a qualified locksmith to your door, day or night, usually within about thirty minutes. The price is given on the phone before he sets off.",
    "From {r0} to the quieter streets of the {num}, our locksmiths work 24/7 on lockouts, jammed locks and broken keys, with a signed quote before any work.",
    "With {pop} residents, the {num} arrondissement ({surnom}) sees its share of lockouts and lost keys every day. Our locksmiths know its buildings and the locks fitted in them.",
    "A locksmith emergency {a}? From the {q} neighborhoods to the area around {r1}, we come quickly, at a price agreed in advance, with an invoice your insurer will accept.",
]


def arr_faq(z):
    return [
        (f"How much does a locksmith cost {z['a_court']}?", f"Opening a slammed door {z['a']} costs €110 incl. VAT during the day, €150 in the evening and €220 at night. A cylinder replacement starts at €160. The price is always given before we travel and confirmed in writing."),
        (f"How quickly can you get here {z['a']}?", "About 30 minutes on average. The exact time depends on Paris traffic and is given on the phone before the locksmith sets off."),
        (f"Do you work at night {z['a_court']}?", "Yes, 24/7, including Sundays and public holidays, with a night rate given in advance."),
        ("Will my invoice be reimbursed?", "Our detailed invoice is accepted by French home insurers. Reimbursement depends on your policy (break-in, theft or loss of keys)."),
    ]


def local_services(z, i, lst):
    cards = []
    for s in lst:
        k = i + SERVICES.index(s)
        loc = SVC_LOCAL[s["slug"]]
        intro = loc["intros"][k % 3].format(a=z["a"], nom=E(NOM))
        prix = f'from <b>{eur(s["prix_num"])}</b>' if s["prix_num"] else "<b>free quote</b>"
        cards.append(f'''<article class="svc-local" id="{s["slug"]}">
  <div class="sl-head"><span class="svc-ic">{ico(s["icon"])}</span><div><h3>{E(s["nom"])}</h3><span class="sl-price">{prix}</span></div></div>
  <p>{intro}</p>
  <p class="sl-tip"><strong>Tip:</strong> {E(loc["conseil"])}</p>
  <div class="sl-acts">{btn_quote(s["court"], "Get a quote", "btn-q")}<a class="text-link" href="{svc_url(s)}">How we work {ico("i-arrow", "ic sm")}</a></div>
</article>''')
    return '<div class="sl-grid">' + "".join(cards) + "</div>"


def recent_jobs(z):
    jobs = INTERVENTIONS.get(z["n"], [])
    if not jobs:
        return ""
    lis = "".join(f'<li><small>{E(d)} · {E(rue)}</small><b>{E(txt)}</b></li>' for d, rue, txt in jobs)
    return f'<h2>Recent jobs {E(z["a"])}</h2><ul class="jobs">{lis}</ul>'


def build_arr_pages():
    body = hero([("Arrondissements", None)], "Locksmith in all <em>20 Paris arrondissements</em>",
                "Choose your arrondissement: prices, neighborhoods covered and services available near you.", kicker="Paris 75")
    body += f'''<section class="sec"><div class="wrap">
  {arr_grid(label=lambda z: z["surnom"])}
  <div class="prose narrow">
    <h2>A Paris locksmith, not a call center</h2>
    <p>{E(NOM)} works exclusively within Paris. That focus lets us arrive quickly and know Parisian buildings well: landing doors in Haussmann buildings, multi-point armored doors, old mortise locks and modern badge-access residences.</p>
    <p class="note-box">{ico("i-pin")}Just outside Paris? Call us on <a href="{TEL_HREF}">{TEL}</a>: depending on availability, we can sometimes come, with travel costs given in advance.</p>
  </div>
</div></section>''' + reviews_block() + contact_band(source="/locksmith-paris/")
    page("/locksmith-paris/", f"Locksmith Paris: all 20 arrondissements 24/7 | {NOM}",
         f"Locksmith everywhere in Paris, from the 1st to the 20th arrondissement, 24/7. Door opening from €110 incl. VAT, price given before we travel. ☎ {TEL}",
         body, [ld_business(full=True), ld_crumbs([("Arrondissements", "/locksmith-paris/")])], active="/locksmith-paris/")

    for i, z in enumerate(ARR):
        path = z["url"]
        intro = ARR_INTROS[i % 4].format(a=z["a"], nom=E(NOM), num=z["num"], r0=z["reperes"][0], r1=z["reperes"][1],
                                         pop=fmt_int(z["pop"]), surnom=z["surnom"], q=et(z["quartiers"][:2]))
        facts = f'''<div class="facts">
  <div><small>Postcode</small><b>{E(" / ".join(z["cp"]))}</b></div>
  <div><small>Door opening</small><b>from €110</b></div>
  <div><small>Availability</small><b>24/7</b></div>
  <div><small>Average arrival</small><b>≈ 30 min</b></div>
</div>'''
        nav_arr = ""
        if z["prev"]:
            nav_arr += f'<a href="{z["prev"]["url"]}">← Locksmith {E(z["prev"]["court"])}</a>'
        if z["next"]:
            nav_arr += f'<a href="{z["next"]["url"]}">Locksmith {E(z["next"]["court"])} →</a>'
        faq = arr_faq(z)
        content = f'''<article class="prose">
  <p class="intro">{intro}</p>
  {facts}
  <h2>Our services {E(z["a"])}</h2>
  <h3 class="group-title">{ico("i-clock")}Emergency call-outs <small>24/7</small></h3>
  {local_services(z, i, SVC_URG)}
  <h3 class="group-title">{ico("i-shield")}Works, armored doors &amp; installation <small>by appointment</small></h3>
  {local_services(z, i, SVC_TRAV)}
  {recent_jobs(z)}
  <h2>Neighborhoods covered in the {z["num"]}</h2>
  <p>We cover the arrondissement's four administrative quarters: <strong>{E(et(z["quartiers"]))}</strong>. Whether you live near {E(et(z["reperes"]))}, a locksmith can be with you quickly.</p>
  <div class="local">
    <div>{ico("i-metro")}<h3>Landmarks</h3><p>Metro: {E(et(z["metros"]))}</p></div>
    <div>{ico("i-home")}<h3>Buildings</h3><p>{E(z["habitat"][0].upper() + z["habitat"][1:])}.</p></div>
    <div>{ico("i-pin")}<h3>Population</h3><p>{fmt_int(z["pop"])} residents (INSEE)</p></div>
  </div>
  <h2>Why call us {E(z["a"])}?</h2>
  <p>When you need an emergency locksmith {E(z["a_court"])}, you often come across anonymous numbers and unrealistic teaser prices. With {E(NOM)}, you know who you are dealing with: an identified company, published prices, a signed quote before every job and public customer reviews on Google.</p>
  <ul class="check-list">
    <li>{ico("i-check")}<span><strong>Price given on the phone</strong>, then a written quote signed before any work.</span></li>
    <li>{ico("i-check")}<span><strong>Damage-free opening</strong> in the vast majority of cases.</span></li>
    <li>{ico("i-check")}<span><strong>Detailed invoice</strong> accepted by French home insurers.</span></li>
    <li>{ico("i-check")}<span><strong>Public reviews</strong> you can check on <a href="{E(MAPS)}" target="_blank" rel="noopener">our Google profile</a>.</span></li>
  </ul>
  <h2>Frequently asked questions {E(z["a_court"])}</h2>
  {faq_html(faq)}
  <nav class="prev-next" aria-label="Neighboring arrondissements">{nav_arr}</nav>
</article>'''
        h1 = f'Locksmith {E(z["court"])} <em>24/7</em>'
        lead = f'Door opening from €110 incl. VAT, jammed locks, broken keys, lock replacement {E(z["a"])} ({E(z["surnom"])}). Price given before we travel, free quote.'
        crumb_items = [("Arrondissements", "/locksmith-paris/"), (f"Paris {z['num']}", None)]
        body = hero(crumb_items, h1, lead, ticks(["Free quote", "No hidden fees", "Nights, weekends, holidays"], "ticks light inline"),
                    kicker=f"{z['cp'][0]} · {z['surnom']}", bg=zone_bg(z))
        body += f'<section class="sec"><div class="wrap layout">{content}{side_box(f"Locksmith {z["court"]}")}</div></section>'
        body += assureurs_strip() + contact_band(f"Locked out {z['a_court']}?", "Call us: price given on the phone, locksmith on the way straight away.", source=path, arr=z["court"])
        ld = [ld_business(), ld_crumbs([("Arrondissements", "/locksmith-paris/"), (f"Paris {z['num']}", path)]), ld_faq(faq),
              {"@context": "https://schema.org", "@type": "Service", "name": f"Locksmith {z['nom']}", "serviceType": "24/7 locksmith services",
               "url": URL + path, "provider": {"@id": BID},
               "areaServed": {"@type": "AdministrativeArea", "name": z["nom"], "postalCode": z["cp"][0]},
               "offers": {"@type": "Offer", "priceSpecification": {"@type": "PriceSpecification", "minPrice": 110, "priceCurrency": "EUR"}}}]
        page(path, f"Locksmith {z['court']} ({z['cp'][0]}) 24/7 – {TEL}",
             f"Locksmith {z['court']} ({z['cp'][0]}), 24/7: door opening from €110 incl. VAT, jammed locks, broken keys, lock replacement. Price given before we travel. ☎ {TEL}",
             body, ld, active="/locksmith-paris/")


# ---------------------------------------------------------------------------
# Service × arrondissement
# ---------------------------------------------------------------------------
SVC_LOCAL = {
    "door-opening": {
        "intros": [
            "Locked out {a} with your keys inside? A {nom} locksmith sets off right away to open your door gently, often in a few minutes and without touching the lock. You get the price before he leaves.",
            "Don't panic if the door has slammed shut behind you {a}: a slammed door can almost always be opened without damage. We come day and night, at a price agreed in advance.",
            "Stuck on the landing {a}? Call us: you know the price before the locksmith arrives, and your door is opened without damage in the vast majority of cases.",
        ],
        "conseil": "Avoid the credit-card trick and screwdrivers: they damage the strike plate and the seal, which makes the job longer.",
    },
    "jammed-lock": {
        "intros": [
            "Key won't turn {a}? Our locksmiths find the cause and fix it on site: cleaning, adjusting the strike plate or replacing the cylinder if needed. Price given before we travel.",
            "Stiff lock, a door that won't open or won't lock {a}: a locksmith arrives with common parts to sort it out in a single visit in most cases.",
            "A rubbing bolt, a clogged cylinder, a door that has shifted: jammed locks are common {a}. We repair first, and only replace when it is really necessary.",
        ],
        "conseil": "Don't force the key and forget about cooking oil: a dry lubricant (graphite or PTFE) works much better.",
    },
    "broken-key": {
        "intros": [
            "Key broken in the lock {a}? Our locksmiths remove the piece with dedicated extractors, usually without taking the lock apart, 24/7, on a free quote.",
            "A piece of key stuck in the cylinder {a}: a locksmith comes to extract it, checks the cylinder and only replaces it on the spot if that is useful.",
            "An old key snapping in the lock is common {a}. We remove the piece cleanly, then advise you: get a new key cut or replace a worn cylinder.",
        ],
        "conseil": "No glue, no paper clip: you could push the piece further in and ruin the cylinder.",
    },
    "lock-replacement": {
        "intros": [
            "Lost keys, moving in or a worn lock {a}: we replace cylinders and locks, from standard models to A2P-certified multi-point locks. Free quote, signed before any work.",
            "Lock replacement {a}: the locksmith arrives with a choice of cylinders in stock, shows you the options and their prices, then fits the one you choose the same day.",
            "Just moved {a} or lost your keys? Replacing the cylinder is the simplest way to take back control of who can get in. Certified equipment, detailed invoice.",
        ],
        "conseil": "Look at the number of A2P stars (1 to 3): it rates break-in resistance and is sometimes required by insurers.",
    },
    "smart-lock": {
        "intros": [
            "Want to open your door with your phone {a}? We install and set up smart locks compatible with your door, and repair those that stop responding.",
            "Smart lock {a}: installation, setup, and repair when the batteries are flat or the motor is stuck. We check your cylinder's compatibility before installing anything.",
            "Smart lock failure or an installation project {a}: we open doors fitted with a stuck smart lock 24/7, and install by appointment.",
        ],
        "conseil": "Keep a mechanical backup key and watch the batteries: they are the number one cause of stuck smart locks.",
    },
    "break-in-repair": {
        "intros": [
            "Burglary or attempted break-in {a}? We secure your door as an emergency, 24/7, then repair or reinforce it. Detailed invoice for your insurer.",
            "Door forced open {a}: a locksmith comes day or night to fit a temporary or permanent lock and replace the damaged cylinder.",
            "After a break-in {a}, the priority is being able to lock up tonight. We come quickly, on a free quote, and advise you on the right reinforcements.",
        ],
        "conseil": "Photograph the damage and file a police report before permanent repairs: your insurer will ask for the receipt.",
    },
    "door-armoring": {
        "intros": [
            "Want to secure your front door {a} without replacing it? Armoring reinforces your existing door with a steel plate, a multi-point lock and anti-jemmy bars, while keeping its look from the landing.",
            "Door armoring {a}: we come to measure your door, check the frame and present several levels of protection, with a free, detailed quote. Fitting usually takes one day.",
            "An old landing door, a basic lock, a tired frame: that's the case in many apartments {a}. Armoring is often the most effective way to deter burglars without major works.",
        ],
        "conseil": "Check your building's co-ownership rules: armoring that keeps the door's outside appearance is usually accepted without formalities.",
    },
    "armored-door": {
        "intros": [
            "Armored door installation {a}: we fit A2P BP1, BP2 or BP3 certified door sets, made to measure and matched to your landing. Free quote after a visit.",
            "Damaged frame, a door that's too light, an exposed home {a}: a complete armored door set replaces the door and frame with a closure designed to resist break-ins.",
            "Looking for the most complete protection for your apartment {a}? An armored door set combines steel, a multi-point lock and insulation, in a finish suited to your building.",
        ],
        "conseil": "Ask your insurer which certification level it requires (BP1, BP2 or BP3) before choosing your model.",
    },
    "cellar-door": {
        "intros": [
            "Cellar broken into or poorly protected {a}? We fit steel cellar door sets with a security lock, made to the size of your opening.",
            "Building cellars are often targeted {a}. A steel cellar door with a proper security lock puts an end to weak padlocks and wooden doors that give way at the first push.",
            "Cellar door {a}: emergency securing after a break-in, then a permanent door on a free quote.",
        ],
        "conseil": "Inform your building manager before replacing your cellar door, and report any break-in: other cellars may have been hit.",
    },
    "mailbox-lock": {
        "intros": [
            "Lost your mailbox key {a}? We replace the lock with a compatible model and new keys, for €110 incl. VAT on a standard model.",
            "Just moved in {a} and don't know who has the mailbox key? Changing the lock takes little time and protects your mail.",
            "Mailbox lock forced or jammed {a}: we open it without damaging the flap and fit a new lock.",
        ],
        "conseil": "If your whole key ring is gone, have your front-door cylinder and cellar lock checked during the same visit.",
    },
}

# ---------------------------------------------------------------------------
# Simple pages
# ---------------------------------------------------------------------------
def simple(path, crumb, h1, lead, prose, title, desc, extra_ld=(), active=None, after="", aside=True, robots="index, follow"):
    body = hero([(crumb, None)], h1, lead)
    inner = f'<article class="prose">{prose}</article>' + (side_box() if aside else "")
    body += f'<section class="sec"><div class="wrap{" layout" if aside else " narrow"}">{inner}</div></section>' + after
    page(path, title, desc, body, [ld_business(), ld_crumbs([(crumb, path)]), *extra_ld], active=active, robots=robots)


def ld_tarifs():
    offers = []
    for p, jour, *_ in TARIFS:
        m = re.search(r"€([\d,]+)", jour)
        if not m:
            continue
        val = int(m.group(1).replace(",", ""))
        spec = {"@type": "PriceSpecification", "priceCurrency": "EUR", "valueAddedTaxIncluded": True}
        spec.update({"minPrice": val} if jour.startswith("From") else {"price": val})
        offers.append({"@type": "Offer", "name": p, "priceSpecification": spec, "itemOffered": {"@type": "Service", "name": p}, "seller": {"@id": BID}})
    return {"@context": "https://schema.org", "@type": "OfferCatalog", "name": f"{NOM} prices", "url": URL + "/prices/", "itemListElement": offers}


def build_static():
    # Prices
    body = hero([("Prices", None)], "Our prices, <em>in black and white</em>",
                "Prices per service and per time of day. Everything is given before we travel and nothing is added on the way.", kicker="Transparency")
    body += f'''<section class="sec"><div class="wrap">
  {tarif_table()}
  <div class="layout" style="margin-top:56px">
    <article class="prose">
      <h2>What the price includes</h2>
      <ul><li>The locksmith's labor.</li><li>Travel within Paris, free if work is carried out.</li><li>VAT: all our prices include VAT.</li><li>A detailed invoice suitable for your insurer.</li></ul>
      <h2>Our commitments</h2>
      <ul><li><strong>Price given</strong> before the locksmith sets off.</li><li><strong>Written, signed quote</strong> before any work.</li><li><strong>No surprise surcharge</strong>: the evening or night rate is given on the phone.</li><li><strong>Certified equipment</strong> from recognized brands.</li></ul>
      <h2>Broken keys, smart locks, break-ins</h2>
      <p>These jobs depend heavily on the situation: they come with a <strong>free quote</strong>, given on the phone and then confirmed in writing.</p>
      <h2>Payment</h2><p>Card, cash or bank transfer.</p>
    </article>
    {side_box("Your price on the phone", "Describe the situation: you know the exact price before we set off.")}
  </div>
</div></section>''' + assureurs_strip() + contact_band(source="/prices/")
    page("/prices/", f"Locksmith prices Paris – day, evening, night | {NOM}",
         "Locksmith prices in Paris: slammed door opening €110 incl. VAT during the day, locked door from €180, cylinder replacement from €160. Evening and night rates shown.",
         body, [ld_business(), ld_crumbs([("Prices", "/prices/")]), ld_tarifs()], active="/prices/")

    # Insurance
    simple("/insurance/", "Insurance", "Locksmith &amp; insurance: <em>getting reimbursed</em>",
           "Our invoices are accepted by French home insurers. Here is how to get a locksmith call-out reimbursed.",
           f'''<h2>When does insurance pay?</h2>
<p>Most French home insurance policies (multirisque habitation) cover locksmith costs after a <strong>burglary or attempted break-in</strong>. Some also cover <strong>theft</strong> or <strong>loss of keys</strong>, sometimes as an option. A door that has simply slammed shut is rarely covered, unless you have an assistance guarantee: check your policy. If you are a visitor, your travel insurance may also include assistance.</p>
<h2>Documents to provide</h2>
<ul><li>The <strong>police report receipt</strong> in case of break-in or theft.</li><li>Our <strong>detailed invoice</strong> (work done, parts fitted, price including VAT).</li><li>The <strong>signed quote</strong> and, on request, <strong>before/after photos</strong>.</li></ul>
<h2>Deadlines</h2>
<p>After a theft or burglary, you usually have <strong>2 working days</strong> to notify your insurer. For other claims, the deadline is often 5 working days. Your policy is the reference.</p>
<h2>How we help</h2>
<p>We give you all the supporting documents and can temporarily secure your door until the insurance assessor visits.</p>
<p class="note-box">{ico("i-shield")}{E(NOM)} is an independent company with no partnership with insurance companies. Reimbursement depends on your policy.</p>''',
           f"Locksmith &amp; home insurance: reimbursable invoice | {NOM}".replace("&amp;", "&"),
           "How to get a locksmith reimbursed by your home insurance in France: guarantees, documents, deadlines. Our invoices are accepted by insurers.",
           after=assureurs_strip() + contact_band(source="/insurance/"))

    # FAQ
    allfaq = HOME_FAQ + [q for s in SERVICES for q in s["faq"]]
    simple("/faq/", "FAQ", "Frequently asked <em>questions</em>",
           "Prices, arrival times, insurance, opening techniques: everything we are asked most often.",
           "<h2>General</h2>" + faq_html(HOME_FAQ) + "".join(f'<h2>{E(s["court"])}</h2>' + faq_html(s["faq"]) for s in SERVICES),
           f"FAQ – locksmith Paris | {NOM}",
           "Door opening prices, arrival times, insurance reimbursement, damage-free opening: our answers.",
           extra_ld=[ld_faq(allfaq)], after=contact_band(source="/faq/"))

    # Reviews
    body = hero([("Customer reviews", None)], "Customer reviews <em>on Google</em>",
                "Our customers post their reviews on our Google Business Profile: they are public and verifiable.", google_badge("g-badge dark"))
    body += reviews_block("Our reputation, fully transparent") + contact_band(source="/reviews/")
    page("/reviews/", f"Customer reviews – locksmith Paris | {NOM}", "Read our customers' Google reviews and leave your own. Locksmith in Paris, 24/7.",
         body, [ld_business(), ld_crumbs([("Customer reviews", "/reviews/")])], active="/reviews/")

    # Contact
    body = hero([("Contact", None)], "Contact <em>your locksmith</em>",
                "For an emergency, calling is fastest. For a quote or planned work, write to us.")
    body += f'''<section class="sec cream"><div class="wrap contact-grid">
  <div class="contact-card">
    <h2>{E(NOM)}</h2>
    <p>{E(CONFIG["slogan"])} in all 20 Paris arrondissements, 24/7. We speak English and French.</p>
    <a class="c-line" href="{TEL_HREF}" data-track="call_contact">{ico("i-phone")}<span><small>Phone 24/7</small><b>{TEL}</b></span></a>
    <a class="c-line" href="{E(wa_link(WA_MSG))}" target="_blank" rel="noopener" data-track="wa_contact">{ico("i-wa")}<span><small>WhatsApp</small><b>Send a photo</b></span></a>
    <a class="c-line" href="mailto:{CONFIG["email"]}">{ico("i-mail")}<span><small>Email</small><b>{CONFIG["email"]}</b></span></a>
    <a class="c-line" href="{CONFIG["instagram"]}" target="_blank" rel="noopener me">{ico("i-insta")}<span><small>Instagram</small><b>@securelockserrurerie</b></span></a>
    <div class="c-line">{ico("i-pin")}<span><small>Service area</small><b>Paris, 1st to 20th arrondissement</b></span></div>
  </div>
  {lead_form("/contact/", titre="Write to us", sous="Quote, call-back, question: quick reply, 7 days a week.")}
</div></section>
<section class="sec"><div class="wrap"><div class="sec-head"><span class="eyebrow">Google Business Profile</span><h2>Find us</h2></div>{map_embed()}</div></section>''' + reviews_block()
    page("/contact/", f"Contact – locksmith Paris 24/7 | {NOM}",
         f"Contact {NOM} on {TEL}, 24/7, by phone, WhatsApp or email. Free quote, fast call-out anywhere in Paris. English spoken.",
         body, [ld_business(full=True), ld_crumbs([("Contact", "/contact/")])], active="/contact/")

    # Legal notice
    lignes = [E(CONFIG["raison_sociale"]) + (f" (trading as {E(NOM)})" if NOM != CONFIG["raison_sociale"] else "")]
    if CONFIG["responsable"]:
        lignes.append(f"Publication director: {E(CONFIG['responsable'])}")
    if CONFIG["siren"]:
        lignes.append(f"SIREN: {CONFIG['siren']}")
    if CONFIG["siret"]:
        lignes.append(f"SIRET: {CONFIG['siret']}")
    lignes += [f"Address: {E(adresse_txt())}", f"Phone: {TEL}", f"Email: {CONFIG['email']}"]
    mediateur = E(CONFIG["mediateur"]) or "their contact details are available on request at " + CONFIG["email"]
    simple("/legal-notice/", "Legal notice", "Legal notice", "Legal information about this website and the company.",
           f'''<h2>Website publisher</h2><p>{"<br>".join(lignes)}</p>
<h2>Hosting</h2><p>Netlify, Inc. – 44 Montgomery Street, Suite 300, San Francisco, CA 94104, United States.</p>
<h2>Intellectual property</h2><p>The texts, logo and graphic elements of this website belong to {E(NOM)}, unless otherwise stated. Insurance company and brand names are mentioned for information only and do not imply any partnership.</p>
<h2>Consumer mediation</h2><p>In accordance with article L612-1 of the French Consumer Code, you may use a consumer mediator free of charge: {mediateur}.</p>
<h2>Prices and quotes</h2><p>Prices shown are starting prices including VAT. In accordance with the French decree of 24 January 2017 on repair and maintenance call-outs in the building sector, a free, detailed quote is given and signed before any work, and a detailed invoice is provided at the end.</p>
<h2>Liability</h2><p>The information on this website is provided for guidance and may change.</p>''',
           f"Legal notice | {NOM}", f"Legal notice of the {NOM} website, locksmith in Paris.", aside=False)

    simple("/privacy/", "Privacy", "Privacy policy", "How we handle your personal data.",
           f'''<h2>Data collected</h2><p>When you contact us (phone, WhatsApp, email or form), we only collect what is needed to handle your request: name, phone number, call-out address and description of the problem.</p>
<h2>Purpose</h2><p>This data is used to organize the call-out and to issue the quote and invoice. It is never sold or passed on.</p>
<h2>Form and WhatsApp</h2><p>Requests sent through the form are processed by Netlify Forms (our website host). WhatsApp messages are subject to WhatsApp's (Meta's) terms.</p>
<h2 id="cookies">Cookies and analytics</h2><p>Only with your consent, this website uses <strong>Google Tag Manager</strong> and <strong>Google Analytics</strong> (Google Ireland Ltd) to measure traffic and the use of the call, WhatsApp and form buttons. Without consent, none of these tools is loaded.</p>
<p>Your choice is stored for 6 months in your browser and can be changed at any time with the "Cookies" link at the bottom of each page.</p>
<h2>Retention</h2><p>Billing data is kept for 10 years (legal requirement). Other data is deleted no later than 3 years after the last contact.</p>
<h2>Your rights</h2><p>Under the GDPR, you have the right to access, correct, delete and object to the processing of your data. Write to {CONFIG["email"]}. You may also contact the French data protection authority (CNIL).</p>''',
           f"Privacy policy | {NOM}", f"Privacy policy of the {NOM} website.", aside=False)


URG_FAQ = [
    ("Do you really come at night and on Sundays?", "Yes, 24/7, public holidays included. The night rate (10pm–8am) is given on the phone before the locksmith sets off."),
    ("How quickly can you get here?", "About 30 minutes on average within Paris. The exact time depends on traffic and is given on the phone."),
    ("How much does an emergency door opening cost?", "€110 incl. VAT during the day, €150 in the evening and €220 at night for a slammed door. A locked door starts at €180 during the day."),
    ("What should I have ready when the locksmith arrives?", "If possible, an ID or proof of address: the locksmith must make sure you are the occupant. If your documents are inside, a neighbor, the caretaker or your host can vouch for you."),
    ("Can I refuse the quote on site?", "Yes. The quote is free and with no obligation: if you refuse it, nothing is done."),
]


# Guide d'urgence : situation -> prix par tranche horaire (None = sur devis), service lié, conseil
GUIDE = [
    ("slammed", "Door slammed shut, keys inside", "door-opening", (110, 150, 220), False,
     "Don't try a credit card or screwdriver on the latch: you would damage the strike plate. Most slammed doors open in minutes with no damage."),
    ("locked", "Door locked with a key, keys lost", "door-opening", (180, 240, 280), True,
     "Ask the caretaker (gardien) or a neighbor whether they keep a spare. Opening without damage is still possible in many cases."),
    ("jammed", "Lock jammed, key won't turn", "jammed-lock", (180, 240, 280), False,
     "Stop forcing the key: you could snap it inside the cylinder. Don't spray oil into the lock."),
    ("broken", "Key broken in the lock", "broken-key", None, False,
     "Don't push the piece further in and never use glue. If it sticks out, pull it straight out with fine pliers."),
    ("burglary", "Burglary, door forced open", "break-in-repair", None, False,
     "Don't go in if someone may still be inside: call the police (17). Don't touch anything before they come."),
    ("stolen", "Keys stolen, change the cylinder", "lock-replacement", (160, 200, 230), True,
     "If your ID or address was stolen with the keys, have the cylinder changed today."),
    ("smart", "Smart lock not responding", "smart-lock", None, False,
     "Look for your mechanical backup key and check whether the app shows a low battery."),
    ("cellar", "Cellar broken into", "cellar-door", None, False,
     "Tell the building manager (syndic): other cellars may have been hit too."),
]


def guide_block():
    data = {k: {"label": l, "url": svc_url(SVC_BY_SLUG[slug]), "service": SVC_BY_SLUG[slug]["court"], "prices": p, "from": f, "tip": t}
            for k, l, slug, p, f, t in GUIDE}
    opts = "".join(f'<button type="button" class="gd-opt" data-sit="{k}" aria-pressed="false">{ico(SVC_BY_SLUG[slug]["icon"])}<span>{E(l)}</span></button>'
                   for k, l, slug, *_ in GUIDE)
    slots = "".join(f'<button type="button" class="gd-slot" data-slot="{k}" aria-pressed="{"true" if k == "jour" else "false"}">{ico(i)}<span><b>{l}</b><small>{h}</small></span></button>'
                    for k, i, l, h in SLOTS)
    return f'''<div class="guide" data-guide>
  <div class="gd-step">
    <p class="gd-q"><b>1</b>What happened?</p>
    <div class="gd-opts">{opts}</div>
  </div>
  <div class="gd-step">
    <p class="gd-q"><b>2</b>When do you need us? <small class="gd-auto" hidden></small></p>
    <div class="gd-slots">{slots}</div>
  </div>
  <div class="gd-result" aria-live="polite">
    <div class="gd-empty">{ico("i-arrow")}<span>Choose your situation above to see your price and what to do now.</span></div>
    <div class="gd-out" hidden>
      <div class="gd-price"><small data-g="slotlabel"></small><b data-g="price"></b><span data-g="note"></span></div>
      <div class="gd-tip">{ico("i-award")}<p><strong>What to do now:</strong> <span data-g="tip"></span></p></div>
      <div class="gd-acts">{btn_call("Call now · " + TEL, cls="btn btn-gold btn-lg", track="call_guide")}<button type="button" class="btn btn-navy btn-lg" data-quote="" data-g="quote">{ico("i-mail")}<span>Call me back</span></button><a class="btn btn-outline btn-lg" data-g="more" href="/services/">{ico("i-file")}<span>How we handle it</span></a></div>
    </div>
  </div>
  <script type="application/json" id="guide-data">{json.dumps(data, ensure_ascii=False)}</script>
</div>'''


def build_urgence():
    steps = "".join(f"<li><b>{i}</b><div><h3>{E(t)}</h3><p>{E(d)}</p></div></li>" for i, (t, d) in enumerate([
        ("Stay calm and safe", "If someone may still be inside after a break-in, don't go in and call the police (17)."),
        ("Call us", f"On {TEL}, 24/7. Describe the door and the situation, or send a photo on WhatsApp."),
        ("You get the price", "Before the locksmith sets off, depending on the time of day. It doesn't change on the way."),
        ("Signed quote, then the work", "On site, the price is confirmed in writing. The locksmith only starts once you have signed."),
    ], start=1))
    body = hero([("Emergency 24/7", None)], "Emergency locksmith in Paris, <em>24/7</em>",
                "Lockout, broken key, jammed lock, burglary: a locksmith comes right away anywhere in the 20 arrondissements, at night, at weekends and on public holidays. Price given before we travel.",
                ticks(["Arrival ≈ 30 min", "Price given on the phone", "Signed quote before work"], "ticks light inline"), kicker="Immediate call-out", bg="tour-eiffel")
    body += f'''<section class="sec"><div class="wrap">
  <div class="sec-head split"><div><span class="eyebrow">Your price in 2 clicks</span><h2>What is your emergency?</h2></div>
  <p>Answer two questions: you get the price that applies right now and what to do while you wait. Then call us, or leave your number and we call you back.</p></div>
  {guide_block()}
</div></section>
<section class="sec soft"><div class="wrap layout"><article class="prose">
  <h2>What to do in an emergency</h2>
  <ol class="urg-steps">{steps}</ol>
  <h2>Our emergency prices</h2>
  <p>Our prices depend on the time of day: day (8am–6pm), evening (6pm–10pm) and night (10pm–8am). The current time slot is selected automatically.</p>
</article>{side_box("Emergency: call now", "A locksmith answers directly and gives you the price before setting off.")}</div>
<div class="wrap" style="margin-top:28px">{tarif_table()}</div></section>
<section class="sec"><div class="wrap faq-wrap"><div class="sec-head"><span class="eyebrow">Questions</span><h2>Emergencies: your questions</h2></div>{faq_html(URG_FAQ)}</div></section>'''
    body += assureurs_strip() + contact_band("Locked out? Call us.", "A locksmith answers right away and gives you the price before travelling.", source="/emergency/")
    page("/emergency/", f"Emergency locksmith Paris 24/7 – {TEL} | {NOM}",
         f"Emergency locksmith in Paris, 24/7: lockouts from €110 incl. VAT, broken keys, jammed locks, burglaries. Arrival in about 30 min, price given before we travel. English spoken. ☎ {TEL}",
         body, [ld_business(full=True), ld_crumbs([("Emergency 24/7", "/emergency/")]), ld_faq(URG_FAQ)], active="/emergency/")


def build_charte():
    items = "".join(f'<div class="charte-item">{ico(i)}<div><h2>{E(t)}</h2><p>{E(d)}</p></div></div>' for i, t, d in CHARTE)
    body = hero([("Our commitments", None)], "Our trust charter",
                "Eight concrete commitments, applied to every job, day and night. Feel free to remind us of them at any time.",
                kicker="Transparency")
    body += f'''<section class="sec"><div class="wrap layout"><article class="prose">
  <p class="intro">Emergency locksmiths suffer from a bad reputation: misleading teaser prices, inflated invoices, locks replaced for no reason. We built {E(NOM)} on the opposite principle. Here, in black and white, is what we commit to for every customer.</p>
  <div class="charte">{items}</div>
  <h2>What you will never see from us</h2>
  {comparatif_block()}
  <h2>Your rights with a locksmith in France</h2>
  <p>For a home call-out, the professional must inform you of their prices and give you a detailed quote before the work (decree of 24 January 2017). You can refuse the quote. At the end, a detailed invoice must be given to you. In the event of a dispute, you can contact the consumer mediator named in our <a href="/legal-notice/">legal notice</a> free of charge, or report a practice on the government's SignalConso website.</p>
  <h2>Check for yourself</h2>
  <p>Before calling us, read <a href="{E(MAPS)}" target="_blank" rel="noopener">our {CONFIG["avis_nombre"]} Google reviews</a>, our <a href="/prices/">price list</a> and our <a href="/legal-notice/">legal information</a>. And if any point of this charter were not respected, tell us: it's the only way to stay up to standard.</p>
</article>{side_box("A clear price from the first call", "Describe your situation: you get the price before anyone travels.")}</div></section>'''
    body += reviews_block() + contact_band(source="/our-commitments/")
    page("/our-commitments/", f"Our commitments: trust charter | {NOM}",
         "Price given before we travel, signed quote before any work, no unnecessary damage, detailed invoice: the trust charter of our Paris locksmith company.",
         body, [ld_business(), ld_crumbs([("Our commitments", "/our-commitments/")])], active="/our-commitments/")


def build_conseils():
    body = hero([("Advice", None)], "Locksmith advice <em>for Paris residents and visitors</em>",
                "Practical guides to react in an emergency, secure your home and avoid nasty surprises.")
    body += f'<section class="sec"><div class="wrap">{articles_cards(ARTICLES)}</div></section>' + contact_band(source="/advice/")
    page("/advice/", f"Locksmith & security advice in Paris | {NOM}",
         "Lost keys, armored doors in Parisian buildings, locksmith scams, after a burglary: our practical guides.",
         body, [ld_business(), ld_crumbs([("Advice", "/advice/")])], active="/advice/")
    for a in ARTICLES:
        path = f"/advice/{a['slug']}/"
        parts = []
        for kind, val in a["corps"]:
            if kind in ("ul", "ol"):
                parts.append(f"<{kind}>" + "".join(f"<li>{v}</li>" for v in val) + f"</{kind}>")
            else:
                parts.append(f"<{kind}>{val}</{kind}>")
        prose = "".join(parts) + (f'<div class="note-box">{ico("i-phone")}<p><strong>Need a locksmith now?</strong> {E(NOM)} works 24/7 across Paris. '
                                  f'Call <a href="{TEL_HREF}">{TEL}</a>: the price is given on the phone. See also our <a href="/services/">services</a> and <a href="/prices/">prices</a>.</p></div>')
        rel = articles_cards([o for o in ARTICLES if o is not a][:3])
        body = hero([("Advice", "/advice/"), (a["court"], None)], E(a["titre"]), E(a["desc"]),
                    f'<p class="post-by">{E(a["cat"])} · {fr_date(a["date"])} · by the {E(NOM)} team</p>')
        body += f'<section class="sec"><div class="wrap layout"><article class="prose">{prose}</article>{side_box()}</div></section>'
        body += f'<section class="sec cream"><div class="wrap"><div class="sec-head"><h2>Read next</h2></div>{rel}</div></section>' + contact_band(source=path)
        ld = [ld_business(), ld_crumbs([("Advice", "/advice/"), (a["court"], path)]),
              {"@context": "https://schema.org", "@type": "BlogPosting", "headline": a["titre"], "description": a["desc"],
               "datePublished": a["date"], "dateModified": a["date"], "inLanguage": "en", "mainEntityOfPage": URL + path,
               "author": {"@type": "Organization", "name": NOM, "url": URL + "/"}, "publisher": {"@id": BID}, "image": URL + "/assets/img/og.jpg"}]
        page(path, f'{a["titre"]} | {NOM}', a["desc"], body, ld, active="/advice/", og_type="article")


def build_misc():
    conv = CONFIG["ads_conv"].get("form")
    body = f'''<section class="phero center-page"><div class="wrap">
  <span class="big-ic">{ico("i-check")}</span>
  <h1>Thank you, your request has been sent</h1>
  <p class="lead">We will call you back very soon. For an emergency (lockout, break-in), call us directly: it's the fastest way.</p>
  <div class="cta-row center">{btn_call(cls="btn btn-gold btn-lg", track="call_merci")}<a class="btn btn-outline-light btn-lg" href="/">Back to home</a></div>
</div></section>'''
    if CONFIG["ads_id"] and conv:
        body += f"<script>gtag('event','conversion',{{'send_to':'{CONFIG['ads_id']}/{conv}','value':1.0,'currency':'EUR'}});</script>"
    page("/thank-you/", f"Request sent | {NOM}", "Your request has been sent.", body, robots="noindex, nofollow")

    body = f'''<section class="phero center-page"><div class="wrap">
  <p class="err">404</p>
  <h1>Page not found</h1>
  <p class="lead">It may have moved. Need a locksmith? We are available 24/7.</p>
  <div class="cta-row center">{btn_call(cls="btn btn-gold btn-lg", track="call_404")}<a class="btn btn-outline-light btn-lg" href="/">Back to home</a></div>
</div></section>'''
    page("/404.html", f"Page not found | {NOM}", "This page doesn't exist.", body, robots="noindex, follow")

    groups = [("Main pages", [("Home", "/"), ("Emergency 24/7", "/emergency/"), ("Services", "/services/"), ("Arrondissements", "/locksmith-paris/"), ("Prices", "/prices/"),
                              ("Our commitments", "/our-commitments/"), ("Insurance", "/insurance/"), ("Customer reviews", "/reviews/"), ("FAQ", "/faq/"),
                              ("Advice", "/advice/"), ("Contact", "/contact/")]),
              ("Services", [(s["nom"], svc_url(s)) for s in SERVICES]),
              ("Arrondissements", [(f"Locksmith {z['court']}", z["url"]) for z in ARR]),
              ("Advice", [(a["court"], f"/advice/{a['slug']}/") for a in ARTICLES])]
    prose = "".join(f'<h2>{E(t)}</h2><div class="chips">' + "".join(f'<a class="chip" href="{u}">{E(l)}</a>' for l, u in lst) + "</div>" for t, lst in groups)
    simple("/site-map/", "Site map", "Site map", f"Every page of the {NOM} website.", prose,
           f"Site map | {NOM}", f"Site map of {NOM}: services, arrondissements, advice.", aside=False)


# ---------------------------------------------------------------------------
# SEO files and redirects
# ---------------------------------------------------------------------------
def write(name, content):
    with open(os.path.join(ROOT, name), "w", encoding="utf-8") as f:
        f.write(content)


# Ancien site en français → nouvelles adresses en anglais (301)
FR_SVC = {"ouverture-de-porte": "door-opening", "serrure-bloquee": "jammed-lock", "cle-cassee": "broken-key",
          "changement-de-serrure": "lock-replacement", "serrure-connectee": "smart-lock", "apres-effraction": "break-in-repair",
          "blindage-de-porte": "door-armoring", "porte-blindee": "armored-door", "porte-de-cave": "cellar-door", "boite-aux-lettres": "mailbox-lock"}
FR_PAGES = {"/urgence/": "/emergency/", "/tarifs/": "/prices/", "/assurance/": "/insurance/", "/avis/": "/reviews/",
            "/questions-frequentes/": "/faq/", "/nos-engagements/": "/our-commitments/", "/conseils/": "/advice/",
            "/mentions-legales/": "/legal-notice/", "/confidentialite/": "/privacy/", "/merci/": "/thank-you/",
            "/plan-du-site/": "/site-map/", "/serrurier-paris/": "/locksmith-paris/",
            "/conseils/cles-perdues-paris/": "/advice/lost-keys-paris/",
            "/conseils/porte-blindee-immeuble-parisien/": "/advice/armored-door-paris-apartment/",
            "/conseils/reconnaitre-serrurier-honnete/": "/advice/spot-an-honest-locksmith/",
            "/conseils/apres-cambriolage-appartement/": "/advice/after-a-burglary/",
            "/english-locksmith-paris": "/", "/cerrajero-paris": "/"}


def build_redirects():
    rules = list(FR_PAGES.items())
    rules += [(f"/services/{fr}/", f"/services/{en}/") for fr, en in FR_SVC.items()]
    for z in ARR:
        rules.append((f"/{z['fr_slug']}/", z["url"]))
        rules += [(f"/{z['fr_slug']}/{fr}/", f"{z['url']}#{en}") for fr, en in FR_SVC.items()]
        # anciennes pages « service × arrondissement », fusionnées dans la page de l'arrondissement
        rules += [(combo_url(s, z), f"{z['url']}#{s['slug']}") for s in SERVICES]
    lines = []
    for old, new in rules:
        lines.append(f"{old}  {new}  301")
        if old.endswith("/"):
            lines.append(f"{old.rstrip('/')}  {new}  301")
    write("_redirects", "# Ancienne version française du site → version anglaise\n" + "\n".join(lines) + "\n")
    return len(rules)


def build_seo():
    def prio(p):
        if p == "/":
            return "1.0"
        if p in ("/locksmith-paris/", "/services/", "/prices/", "/contact/", "/emergency/"):
            return "0.9"
        if p.startswith("/services/") or (p.startswith("/locksmith-paris-") and p.count("/") == 2):
            return "0.8"
        if p.startswith("/locksmith-paris-"):
            return "0.7"
        return "0.5"
    urls = "".join(f"  <url><loc>{URL}{p}</loc><lastmod>{TODAY}</lastmod><priority>{prio(p)}</priority></url>\n" for p in SITEMAP)
    write("sitemap.xml", '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + urls + "</urlset>\n")
    write("robots.txt", f"User-agent: *\nAllow: /\nDisallow: /_src/\nDisallow: /thank-you/\n\nSitemap: {URL}/sitemap.xml\n")

    svc = "\n".join(f"- [{s['nom']}]({URL}{svc_url(s)}): {s['prix']}. {s['resume']}" for s in SERVICES)
    grille = "\n".join(f"- {t[0]}: " + " / ".join(v or "quote" for v in t[1:]) for t in TARIFS)
    arr = "\n".join(f"- [Locksmith {z['court']}]({URL}{z['url']}) – {z['cp'][0]}" for z in ARR)
    note = f"- Google rating: {CONFIG['avis_note']}/5 ({CONFIG['avis_nombre']} reviews)\n" if CONFIG["avis_note"] else ""
    write("llms.txt", f"""# {NOM}

> English-speaking locksmith in Paris (75), across all 20 arrondissements, 24/7. Slammed door opening from €110 incl. VAT, price given on the phone before travelling, written quote signed before any work, invoice accepted by French home insurers.

## Information
- Name: {NOM} ({CONFIG['raison_sociale']})
- Phone: {TEL}, 24/7
- WhatsApp: {WA}
- Email: {CONFIG['email']}
- Website: {URL}/
- Area: Paris only, 1st to 20th arrondissement
- Average arrival: about 30 minutes
- Languages: English, French
- Payment: card, cash, bank transfer
{note}
## Services
{svc}

## Prices incl. VAT (day 8am–6pm / evening 6pm–10pm / night 10pm–8am)
{grille}

## Arrondissements
{arr}

Each arrondissement page lists every service with its price and local details (e.g. {URL}{ARR[14]["url"]}#door-opening).
""")
    write("site.webmanifest", json.dumps({
        "name": f"{NOM} – 24/7 locksmith", "short_name": "Secure Locksmith", "lang": "en", "start_url": "/",
        "display": "standalone", "background_color": "#151335", "theme_color": "#151335",
        "icons": [{"src": "/assets/img/logo-240.png", "sizes": "240x240", "type": "image/png"},
                  {"src": "/assets/img/icon-512.png", "sizes": "512x512", "type": "image/png"}]}, ensure_ascii=False, indent=2))


def main():
    build_home()
    build_services()
    build_arr_pages()
    build_static()
    build_urgence()
    build_charte()
    build_conseils()
    build_misc()
    build_seo()
    n = build_redirects()
    print(f"{len(SITEMAP)} pages indexables générées, {n} redirections depuis l'ancienne version française.")


if __name__ == "__main__":
    main()
