# -*- coding: utf-8 -*-
"""Générateur du site Secure Locksmith Paris (serrurier Paris 75, 20 arrondissements).

Usage : python3 _src/build.py
Écrit toutes les pages HTML, le sitemap, robots.txt et llms.txt à la racine du dépôt.
Aucune dépendance : Python 3.12+.

Photos : déposez vos vraies photos (JPG ou WebP, ~1600 px de large) dans assets/img/photos/
avec ces noms ; elles apparaissent automatiquement au prochain build :
  accueil.jpg                     grande photo de l'accueil (vous, votre véhicule, une intervention)
  equipe.jpg                      bloc « Qui sommes-nous »
  ouverture-de-porte.jpg, serrure-bloquee.jpg, cle-cassee.jpg,
  changement-de-serrure.jpg, serrure-connectee.jpg, apres-effraction.jpg   photos des services
"""
import datetime
import html
import json
import os
import re

from data import ARRONDISSEMENTS, ARTICLES, ASSUREURS, AVIS, MARQUES, SERVICES, TARIFS

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ---------------------------------------------------------------------------
# Configuration : à vérifier avant mise en ligne
# ---------------------------------------------------------------------------
CONFIG = {
    "site_url": "https://securelockserrurerie.com",  # nom de domaine, sans / final
    "nom": "Secure Locksmith Paris",
    "slogan": "Votre serrurier de confiance",
    "tel": "06 67 96 96 20",
    "tel_intl": "+33667969620",
    "wa": "33667969620",
    "email": "securelockserrurerie@gmail.com",
    "instagram": "https://www.instagram.com/securelockserrurerie/",
    # Fiche Google Business Profile (remplacez par le lien exact de la fiche si besoin)
    "maps_url": "https://www.google.com/maps/place/Secure+Lock+Serrurerie/@48.870843,1.155034,9z/data=!4m10!1m2!2m1!1sSecure+Lock+Serrurerie+Paris!3m6!1s0x267653ac7048cd93:0x27df91bfb8a939fd!8m2!3d48.870843!4d2.3745164!15sChxTZWN1cmUgTG9jayBTZXJydXJlcmllIFBhcmlzWh4iHHNlY3VyZSBsb2NrIHNlcnJ1cmVyaWUgcGFyaXOSAQlsb2Nrc21pdGiaAURDaTlEUVVsUlFVTnZaRU5vZEhsalJqbHZUMnhDZDAxR2EzaFNWV1IyVlRCU05GZFZZelJSVlhSMVkyeENNVk5yUlJBQuABAPoBBAg4EEc!16s%2Fg%2F11yz6fjq73",
    # Position de la fiche Google (carte et données structurées)
    "lat": 48.870843,
    "lng": 2.3745164,
    # Lien « Demander des avis » de la fiche Google (ex. https://g.page/r/XXXX/review) ; vide = lien de la fiche
    "avis_url": "",
    # Note Google affichée sur le site : à tenir à jour (laisser vide pour ne rien afficher)
    "avis_note": "5,0",
    "avis_nombre": 95,
    # Mesure d'audience (chargée seulement après accord du visiteur)
    "gtm_id": "GTM-N742H7F8",
    "ga_id": "G-GL99Q7CQKN",
    "ads_id": "AW-17925645444",
    "ads_conv": {"call": "pIa-CPq274YcEITJzuNC", "wa": "", "form": ""},
    "google_verification": "26oalrhYl1sf4O17TalfT0E-_m-pbH7o4PDT2PE984Q",
    # Entreprise (affichée sur le site et dans les mentions légales)
    "raison_sociale": "Secure Lock Serrurerie",
    "adresse": {"rue": "5 rue Camille du Gast", "cp": "92390", "ville": "Villeneuve-la-Garenne"},
    "siren": "",   # 9 chiffres, ex. "123456789"
    "siret": "",   # 14 chiffres
    "responsable": "",
    "mediateur": "",  # nom et site du médiateur de la consommation
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
BID = URL + "/#serrurier"


def wa_link(text):
    from urllib.parse import quote
    return WA + "?text=" + quote(text)


def fmt_int(n):
    return f"{n:,}".replace(",", " ")


def siret_fmt():
    s = CONFIG["siret"]
    return f"{s[:3]} {s[3:6]} {s[6:9]} {s[9:]}" if len(s) == 14 else s


def adresse_txt():
    a = CONFIG["adresse"]
    return ", ".join(v for v in (a["rue"], f'{a["cp"]} {a["ville"]}'.strip()) if v)


# ---------------------------------------------------------------------------
# Icônes
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


def ico(name, cls="ic"):
    return f'<svg class="{cls}" aria-hidden="true"><use href="#{name}"/></svg>'


def photo(name, alt, cls="", sizes="(max-width: 760px) 100vw, 600px", eager=False):
    """Photo fournie dans assets/img/photos/<name>.(webp|jpg|jpeg|png), sinon chaîne vide."""
    for ext in ("webp", "jpg", "jpeg", "png"):
        if os.path.exists(os.path.join(ROOT, "assets", "img", "photos", f"{name}.{ext}")):
            load = 'fetchpriority="high"' if eager else 'loading="lazy"'
            return f'<img class="{cls}" src="/assets/img/photos/{name}.{ext}" alt="{E(alt)}" sizes="{sizes}" {load} decoding="async">'
    return ""


# ---------------------------------------------------------------------------
# Arrondissements
# ---------------------------------------------------------------------------
def build_arr():
    out = []
    for n, (surnom, pop, cps, quartiers, reperes, metros, habitat) in ARRONDISSEMENTS.items():
        suf = "er" if n == 1 else "e"
        out.append({
            "n": n, "suf": suf, "num": f"{n}{suf}", "slug": f"serrurier-paris-{n}{suf}",
            "court": f"Paris {n}{suf}", "nom": f"Paris {n}{suf} arrondissement", "surnom": surnom,
            "a": f"dans le {n}{suf} arrondissement", "a_court": f"à Paris {n}{suf}",
            "pop": pop, "cp": cps, "quartiers": quartiers, "reperes": reperes, "metros": metros, "habitat": habitat,
        })
    for i, z in enumerate(out):
        z["url"] = f"/{z['slug']}/"
        z["prev"] = out[i - 1] if i > 0 else None
        z["next"] = out[i + 1] if i < len(out) - 1 else None
    return out


ARR = build_arr()


def et(lst):
    return lst[0] if len(lst) == 1 else ", ".join(lst[:-1]) + " et " + lst[-1]


def de(x):
    """« de » + article contracté : de le → du, de les → des."""
    if x.startswith("le "):
        return "du " + x[3:]
    if x.startswith("les "):
        return "des " + x[4:]
    return "de " + x


def de_list(lst):
    return et([de(x) for x in lst])


def svc_url(s):
    return f"/services/{s['slug']}/"


def combo_url(s, z):
    return f"/{z['slug']}/{s['slug']}/"


# ---------------------------------------------------------------------------
# Composants
# ---------------------------------------------------------------------------
def btn_call(label=None, cls="btn btn-gold", track="call"):
    return f'<a class="{cls}" href="{TEL_HREF}" data-track="{track}">{ico("i-phone")}<span>{E(label or TEL)}</span></a>'


def btn_wa(text="Bonjour, j'ai besoin d'un serrurier à Paris.", label="WhatsApp", cls="btn btn-outline-light", track="wa"):
    return f'<a class="{cls}" href="{E(wa_link(text))}" target="_blank" rel="noopener" data-track="{track}">{ico("i-wa")}<span>{E(label)}</span></a>'


def ticks(items, cls="ticks"):
    return f'<ul class="{cls}">' + "".join(f"<li>{ico('i-check')}<span>{E(i)}</span></li>" for i in items) + "</ul>"


def crumbs(items):
    parts = ['<a href="/">Accueil</a>']
    for label, url in items:
        parts.append(f'<a href="{url}">{E(label)}</a>' if url else f'<span aria-current="page">{E(label)}</span>')
    return '<nav class="crumbs" aria-label="Fil d\'Ariane">' + ico("i-chev", "sep").join(parts) + "</nav>"


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
            f'<span><b>{CONFIG["avis_note"]}</b>{stars()}<small>{CONFIG["avis_nombre"]} avis Google</small></span></a>')


def faq_html(faq):
    return '<div class="faq">' + "".join(
        f'<details{" open" if i == 0 else ""}><summary>{E(q)}<i aria-hidden="true"></i></summary><div><p>{a}</p></div></details>'
        for i, (q, a) in enumerate(faq)) + "</div>"


def ld_faq(faq):
    return {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": re.sub("<[^>]+>", "", a)}} for q, a in faq]}


def ld_crumbs(items):
    lst = [{"@type": "ListItem", "position": 1, "name": "Accueil", "item": URL + "/"}]
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
        "priceRange": "€€", "currenciesAccepted": "EUR", "paymentAccepted": "Carte bancaire, Espèces, Virement",
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
        d["hasOfferCatalog"] = {"@type": "OfferCatalog", "name": "Serrurerie à Paris", "itemListElement": [
            {"@type": "Offer", "itemOffered": {"@type": "Service", "name": s["nom"], "url": URL + svc_url(s)},
             **({"priceSpecification": {"@type": "PriceSpecification", "minPrice": s["prix_num"], "priceCurrency": "EUR"}} if s["prix_num"] else {})}
            for s in SERVICES]}
    return d


FORM_N = [0]


def lead_form(source, service=None, titre="Demande de devis gratuit", sous="Nous vous rappelons rapidement, 7j/7.", arr=""):
    FORM_N[0] += 1
    n = FORM_N[0]
    opts = "".join(f'<option{" selected" if service == s["court"] else ""}>{E(s["court"])}</option>' for s in SERVICES)
    arr_opts = "".join(f'<option{" selected" if arr == z["court"] else ""}>{E(z["court"])}</option>' for z in ARR)
    return f'''<form class="lead-form" name="devis" method="POST" action="/merci/" data-netlify="true" netlify-honeypot="champ-robot">
  <input type="hidden" name="form-name" value="devis"><input type="hidden" name="page" value="{E(source)}">
  <p hidden><label>Laisser vide <input name="champ-robot"></label></p>
  <div class="form-head"><h3>{E(titre)}</h3><p>{E(sous)}</p></div>
  <div class="grid2">
    <label for="n{n}">Nom<input id="n{n}" name="nom" autocomplete="name" required placeholder="Votre nom"></label>
    <label for="t{n}">Téléphone<input id="t{n}" name="telephone" type="tel" inputmode="tel" autocomplete="tel" required pattern="[0-9+ .()-]{{10,}}" placeholder="06 00 00 00 00"></label>
  </div>
  <div class="grid2">
    <label for="s{n}">Votre besoin<select id="s{n}" name="service">{opts}<option{" selected" if not service else ""}>Autre demande</option></select></label>
    <label for="a{n}">Arrondissement<select id="a{n}" name="arrondissement"><option value="">Choisir…</option>{arr_opts}</select></label>
  </div>
  <label for="m{n}">Message<textarea id="m{n}" name="message" rows="3" placeholder="Type de porte, situation, horaire souhaité…"></textarea></label>
  <button class="btn btn-navy btn-block btn-lg" type="submit">{ico("i-mail")}<span>Envoyer ma demande</span></button>
  <p class="form-legal">{ico("i-lock", "ic xs")}Vos données servent uniquement à vous répondre. <a href="/confidentialite/">Confidentialité</a></p>
  <div class="form-ok" role="status" hidden>{ico("i-check")}<div><strong>Demande bien reçue.</strong> Nous vous rappelons très vite. Urgence : <a href="{TEL_HREF}">{TEL}</a></div></div>
</form>'''


def contact_band(titre="Besoin d'un serrurier à Paris ?", texte="Appelez-nous : un serrurier vous répond directement et vous annonce le prix avant de se déplacer.",
                 source="/", service=None, arr=""):
    return f'''<section class="band" id="devis">
  <div class="wrap band-grid">
    <div class="band-text">
      <span class="eyebrow light">Réponse immédiate · 24h/24</span>
      <h2>{E(titre).replace(" ?", "&nbsp;?")}</h2>
      <p>{E(texte)}</p>
      <a class="band-phone" href="{TEL_HREF}" data-track="call_band"><span class="ring">{ico("i-phone")}</span><span><small>Appel direct, sans plateforme</small><b>{TEL}</b></span></a>
      {ticks(["Prix annoncé avant le déplacement", "Devis écrit signé avant toute intervention", "Facture détaillée pour votre assurance", "Paiement CB, espèces ou virement"], "ticks light")}
    </div>
    {lead_form(source, service, arr=arr)}
  </div>
</section>'''


def side_box(titre="Un serrurier disponible maintenant", texte="Décrivez votre situation au téléphone : le prix vous est annoncé avant tout déplacement."):
    return f'''<aside class="side-box">
  <div class="side-head"><span class="live"><i></i>Disponible 24h/24</span><h3>{E(titre)}</h3></div>
  <div class="side-body">
    <p>{E(texte)}</p>
    {btn_call(cls="btn btn-gold btn-block btn-lg", track="call_side")}
    {btn_wa(label="Envoyer une photo", cls="btn btn-outline btn-block", track="wa_side")}
    {ticks(["Devis gratuit et sans engagement", "Ouverture sans casse dans la plupart des cas", "Facture acceptée par les assurances"], "ticks small")}
    {google_badge("g-badge compact")}
  </div>
</aside>'''


SLOTS = [("jour", "i-sun", "Journée", "8h – 18h"), ("soir", "i-sunset", "Soirée", "18h – 22h"), ("nuit", "i-moon", "Nuit", "22h – 8h")]


def tarif_table():
    urg = [t for t in TARIFS if all(t[1:])]
    trav = [t for t in TARIFS if not all(t[1:])]
    head = "".join(f'<th scope="col" data-slot="{k}">{ico(i)}<span>{l}</span><small>{h}</small></th>' for k, i, l, h in SLOTS)

    def cell(v):
        if v.startswith("À partir de"):
            return f'<small>dès</small>{E(v[12:])}'
        return E(v)
    rows = "".join(f'<tr><th scope="row">{E(p)}</th>' + "".join(f'<td data-slot="{k}" data-label="{l}">{cell(v)}</td>' for (k, _, l, _), v in zip(SLOTS, prix)) + "</tr>"
                   for p, *prix in urg)
    trv = "".join(f'<li><span>{E(p)}</span><b>{cell(j)}</b></li>' for p, j, *_ in trav)
    return f'''<div class="tarifs">
  <div class="tarif-card main">
    <div class="tc-head"><div><span class="eyebrow light">Dépannage 24h/24</span><h3>Tarifs selon l'heure d'intervention</h3></div><span class="tc-ttc">Prix TTC</span></div>
    <div class="table-wrap"><table class="tarif-table" data-tarifs><thead><tr><th scope="col">Prestation</th>{head}</tr></thead><tbody>{rows}</tbody></table></div>
    <p class="tarif-now" hidden></p>
  </div>
  <div class="tarif-card">
    <div class="tc-head light"><div><span class="eyebrow">Sur rendez-vous</span><h3>Travaux et pose</h3></div></div>
    <ul class="tarif-list">{trv}</ul>
    <p class="tarif-foot">Prix de départ en journée. Devis détaillé gratuit après visite.</p>
  </div>
</div>
<p class="tarif-note">{ico("i-file")}<span>Tarifs TTC, main d'œuvre comprise. Le prix exact dépend de votre porte et de votre serrure : il vous est annoncé au téléphone, puis confirmé par un devis écrit et signé avant l'intervention, conformément à l'arrêté du 24 janvier 2017.</span></p>'''


def logo_tile(nom, slug, folder):
    if slug and os.path.exists(os.path.join(ROOT, "assets", "img", folder, f"{slug}.webp")):
        return f'<li class="logo"><img src="/assets/img/{folder}/{slug}.webp" alt="{E(nom)}" title="{E(nom)}" loading="lazy" decoding="async" height="48"></li>'
    return ""


def assureurs_strip(titre=True):
    tiles = "".join(logo_tile(n, s, "assureurs") for n, s in ASSUREURS)
    autres = ", ".join(n for n, s in ASSUREURS if not s)
    head = f'''<div class="strip-head"><p><b>Factures reconnues par les assureurs habitation</b><span>Remboursement selon les garanties de votre contrat · <a href="/assurance/">en savoir plus</a></span></p></div>''' if titre else ""
    return f'''<section class="strip">
  <div class="wrap">
    {head}
    <ul class="logos">{tiles}</ul>
    <p class="fine">Et aussi : {E(autres)}. {E(NOM)} est une entreprise indépendante, sans partenariat avec ces compagnies ; les logos appartiennent à leurs propriétaires.</p>
  </div>
</section>'''


def marques_block():
    tiles = "".join(logo_tile(n, s, "marques") for n, s, _ in MARQUES)
    cats = {}
    for n, _, c in MARQUES:
        cats.setdefault(c, []).append(n)
    txt = " · ".join(f"<b>{E(c)}</b> : {E(', '.join(l))}" for c, l in cats.items())
    return f'''<div class="brands">
  <ul class="logos brands-logos">{tiles}</ul>
  <p class="fine">{txt}.</p>
</div>'''


def arr_grid(link=lambda z: z["url"], label=lambda z: z["surnom"], cls="arr-grid"):
    return f'<div class="{cls}">' + "".join(
        f'<a href="{link(z)}"><b>{z["n"]}<span>{z["suf"]}</span></b><span class="t"><strong>Paris {z["num"]}</strong><small>{E(label(z))}</small></span>{ico("i-chev", "ic go")}</a>'
        for z in ARR) + "</div>"


def review_cards():
    if not AVIS:
        return ""
    cards = "".join(f'''<article class="review">
  <header><span class="av">{E(r["auteur"][:1].upper())}</span><div><b>{E(r["auteur"])}</b><small>{E(r.get("date", ""))}{(" · " + E(r["arr"])) if r.get("arr") else ""}</small></div>{G_LOGO}</header>
  {stars(int(r.get("note", 5)))}
  <p>{E(r["texte"])}</p>
</article>''' for r in AVIS)
    return f'<div class="review-grid">{cards}</div>'


def reviews_block(titre="Ce que nos clients disent de nous"):
    note = ""
    if CONFIG["avis_note"]:
        note = f'''<div class="score-card">
  <div class="score-top">{G_LOGO}<span>Avis Google</span></div>
  <div class="score"><b>{CONFIG["avis_note"]}</b><span>/5</span></div>
  {stars(5, "st lg")}
  <p>Note moyenne sur <b>{CONFIG["avis_nombre"]} avis</b> publiés par nos clients</p>
  <a class="btn btn-navy btn-block" href="{E(MAPS)}" target="_blank" rel="noopener">Lire les avis sur Google</a>
  <a class="btn btn-outline btn-block" href="{E(AVIS_URL)}" target="_blank" rel="noopener">Laisser un avis</a>
</div>'''
    cards = review_cards()
    side = cards or f'''<div class="review-promise">
  <h3>Des avis publics et vérifiables</h3>
  <p>Nous ne publions pas de témoignages anonymes sur notre site : nos avis sont déposés par nos clients directement sur notre fiche Google. Ils sont publics, datés, et nous ne pouvons ni les modifier ni les supprimer.</p>
  <ul class="ticks">
    <li>{ico("i-check")}<span>Déposés directement par nos clients sur Google</span></li>
    <li>{ico("i-check")}<span>Consultables avant même de nous appeler</span></li>
    <li>{ico("i-check")}<span>Prix, délai, propreté : jugez sur pièces avant d'appeler</span></li>
  </ul>
</div>'''
    return f'''<section class="sec soft" id="avis">
  <div class="wrap">
    <div class="sec-head"><span class="eyebrow">Avis clients</span><h2>{E(titre)}</h2></div>
    <div class="reviews">{note}{side}</div>
  </div>
</section>'''


def map_embed():
    from urllib.parse import quote
    q = quote(f"Secure Lock Serrurerie @{CONFIG['lat']},{CONFIG['lng']}")
    return (f'<div class="map"><iframe title="{E(NOM)} sur Google Maps" loading="lazy" referrerpolicy="no-referrer-when-downgrade" '
            f'src="https://maps.google.com/maps?q={q}&amp;z=14&amp;hl=fr&amp;output=embed"></iframe>'
            f'<a class="map-link" href="{E(MAPS)}" target="_blank" rel="noopener">{G_LOGO}Voir notre fiche Google</a></div>')


def company_card():
    rows = [("i-building", "Entreprise", f"{E(CONFIG['raison_sociale'])}")]
    if CONFIG["siret"]:
        rows.append(("i-file", "SIRET", siret_fmt()))
    rows += [("i-pin", "Siège", E(adresse_txt())), ("i-phone", "Téléphone", f'<a href="{TEL_HREF}">{TEL}</a>'),
             ("i-mail", "E-mail", f'<a href="mailto:{CONFIG["email"]}">{CONFIG["email"]}</a>'),
             ("i-card", "Paiement", "Carte bancaire, espèces, virement")]
    lis = "".join(f'<li>{ico(i)}<span><small>{l}</small>{v}</span></li>' for i, l, v in rows)
    return f'''<div class="company">
  <div class="company-head"><img src="/assets/img/logo-112.webp" width="56" height="56" alt=""><div><b>{E(NOM)}</b><small>Fiche d'identité</small></div></div>
  <ul>{lis}</ul>
  <a class="company-link" href="/mentions-legales/">Mentions légales complètes {ico("i-arrow", "ic sm")}</a>
</div>'''


# ---------------------------------------------------------------------------
# Gabarit de page
# ---------------------------------------------------------------------------
NAV = [("Services", "/services/"), ("Tarifs", "/tarifs/"), ("Arrondissements", "/serrurier-paris/"),
       ("Avis", "/avis/"), ("Conseils", "/conseils/"), ("Contact", "/contact/")]
SITEMAP = []


def asset_v(rel):
    import hashlib
    try:
        with open(os.path.join(ROOT, rel), "rb") as f:
            return hashlib.md5(f.read()).hexdigest()[:10]
    except FileNotFoundError:
        return TODAY


def logo_html(cls="brand"):
    return (f'<a href="/" class="{cls}" aria-label="{E(NOM)} – accueil"><picture><source type="image/webp" srcset="/assets/img/logo-112.webp">'
            f'<img src="/assets/img/logo-112.png" width="52" height="52" alt=""></picture>'
            f'<span class="wordmark"><b>Secure Locksmith</b><small>Serrurier · Paris</small></span></a>')


def footer():
    svc = "".join(f'<li><a href="{svc_url(s)}">{E(s["nom"])}</a></li>' for s in SERVICES)
    arr = "".join(f'<a href="{z["url"]}">{z["n"]}<sup>{z["suf"]}</sup></a>' for z in ARR)
    siret = f"<br>SIRET {siret_fmt()}" if CONFIG["siret"] else ""
    return f'''<footer class="foot">
  <div class="wrap">
    <div class="foot-cta">
      <div><b>Une urgence ? Un serrurier vous répond tout de suite.</b><span>24h/24 · 7j/7 · dimanches et jours fériés</span></div>
      {btn_call(cls="btn btn-gold btn-lg", track="call_footer_cta")}
    </div>
    <div class="foot-grid">
      <div class="foot-brand">
        {logo_html("brand brand-foot")}
        <p>Serrurier à Paris, dans les 20 arrondissements. Dépannage 24h/24, prix annoncé avant le déplacement, devis signé avant travaux, facture pour votre assurance.</p>
        <p class="foot-id">{E(CONFIG["raison_sociale"])}<br>{E(adresse_txt())}{siret}</p>
      </div>
      <div><h4>Services</h4><ul>{svc}</ul></div>
      <div><h4>Informations</h4><ul><li><a href="/tarifs/">Tarifs</a></li><li><a href="/assurance/">Assurance et remboursement</a></li><li><a href="/avis/">Avis clients</a></li><li><a href="/questions-frequentes/">Questions fréquentes</a></li><li><a href="/conseils/">Conseils</a></li><li><a href="/contact/">Contact</a></li></ul></div>
      <div><h4>Contact</h4><ul class="foot-contact"><li><a href="{TEL_HREF}" data-track="call_footer">{ico("i-phone", "ic sm")}{TEL}</a></li><li><a href="mailto:{CONFIG["email"]}">{ico("i-mail", "ic sm")}{CONFIG["email"]}</a></li><li><a href="{CONFIG["instagram"]}" target="_blank" rel="noopener me">{ico("i-insta", "ic sm")}Instagram</a></li></ul>
        <h4 class="mt">Arrondissements</h4><div class="arr-mini">{arr}</div></div>
    </div>
    <div class="foot-bottom">
      <span>© {TODAY[:4]} {E(NOM)} – {E(CONFIG["raison_sociale"])}</span>
      <nav><a href="/mentions-legales/">Mentions légales</a><a href="/confidentialite/">Confidentialité</a><a href="/plan-du-site/">Plan du site</a><button type="button" class="linklike" data-open-consent>Cookies</button></nav>
    </div>
  </div>
</footer>'''


def page(path, title, desc, body, ld=(), active=None, robots="index, follow", og_type="website"):
    canonical = URL + path
    nav = "".join(f'<a href="{u}"{" aria-current=\"page\"" if u == active else ""}>{E(l)}</a>' for l, u in NAV)
    ld_html = "".join(f'<script type="application/ld+json">{json.dumps(d, ensure_ascii=False)}</script>\n' for d in ld)
    ads = CONFIG["ads_id"]
    conv = json.dumps({k: f"{ads}/{v}" for k, v in CONFIG["ads_conv"].items() if v}) if ads else "{}"
    ads_js = f"gtag('config','{ads}');" if ads else ""
    note = (f'<a class="tb-rating" href="{E(MAPS)}" target="_blank" rel="noopener">{stars(5, "st xs")}<b>{CONFIG["avis_note"]}/5</b> sur Google ({CONFIG["avis_nombre"]} avis)</a>'
            if CONFIG["avis_note"] else "")
    doc = f'''<!DOCTYPE html>
<html lang="fr">
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
<meta name="theme-color" content="#0d1a3a">
<meta name="geo.region" content="FR-75">
<meta name="geo.placename" content="Paris">
<meta name="geo.position" content="48.8566;2.3522">
<meta property="og:type" content="{og_type}">
<meta property="og:locale" content="fr_FR">
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
    <span class="tb-live"><i></i>Serruriers disponibles maintenant à Paris</span>
    <span class="tb-items"><span>{ico("i-file", "ic xs")}Devis signé avant intervention</span><span>{ico("i-shield", "ic xs")}Facture acceptée par les assurances</span></span>
    {note}
  </div>
</div>
<header class="top" id="top">
  <div class="wrap top-in">
    {logo_html()}
    <nav class="menu" aria-label="Navigation principale">{nav}</nav>
    <div class="top-cta">
      <a class="top-tel" href="{TEL_HREF}" data-track="call_header"><span class="ring">{ico("i-phone")}</span><span><small>Urgence 24h/24</small><b>{TEL}</b></span></a>
      <button class="burger" type="button" aria-label="Menu" aria-expanded="false" aria-controls="drawer"><i></i><i></i><i></i></button>
    </div>
  </div>
  <nav class="drawer" id="drawer" aria-label="Navigation mobile"><a href="/">Accueil</a>{nav}<a class="btn btn-gold" href="{TEL_HREF}" data-track="call_drawer">{ico("i-phone")}<span>Appeler le {TEL}</span></a></nav>
</header>
<main>
{body}
</main>
{footer()}
<div class="cookies" id="cookies" role="dialog" aria-label="Cookies" hidden>
  <p><strong>Votre vie privée</strong> Avec votre accord, nous mesurons l'audience du site (Google Analytics, Google Tag Manager) pour l'améliorer. Aucun outil n'est chargé sans votre accord. <a href="/confidentialite/#cookies">En savoir plus</a></p>
  <div><button type="button" class="btn btn-outline btn-sm" data-cookies="denied">Refuser</button><button type="button" class="btn btn-navy btn-sm" data-cookies="granted">Accepter</button></div>
</div>
<div class="dock">
  <a class="btn btn-gold" href="{TEL_HREF}" data-track="call_dock">{ico("i-phone")}<span>Appeler · 24h/24</span></a>
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
    "tour-eiffel": "La tour Eiffel au coucher du soleil", "toits-de-paris": "Les toits de Paris",
    "notre-dame": "Notre-Dame de Paris et la Seine", "pantheon": "Le Panthéon", "conciergerie": "La Conciergerie au bord de la Seine",
    "place-des-victoires": "La place des Victoires", "sacre-coeur": "Le Sacré-Cœur de Montmartre",
    "vue-sacre-coeur": "Vue sur Montmartre", "avenue-etoile": "Avenue parisienne vue de l'Arc de Triomphe", "mairie": "Une mairie d'arrondissement",
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


def hero(crumb_items, h1, lead, extra="", kicker=None, card=None, bg=None):
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
      <div class="cta-row">{btn_call(cls="btn btn-gold btn-lg", track="call_hero")}{btn_wa(cls="btn btn-outline-light btn-lg", track="wa_hero")}</div>
      {extra}
    </div>
    {card}
  </div>
</section>'''


def hero_card(prix="dès 110 € TTC", label="Ouverture de porte"):
    return f'''<aside class="hcard">
  <ul>
    <li>{ico("i-euro")}<span><small>{E(label)}</small><b>{E(prix)}</b></span></li>
    <li>{ico("i-clock")}<span><small>Délai moyen dans Paris</small><b>≈ 30 minutes</b></span></li>
    <li>{ico("i-file")}<span><small>Devis</small><b>Gratuit, signé avant travaux</b></span></li>
  </ul>
  {google_badge("g-badge compact")}
</aside>'''


# ---------------------------------------------------------------------------
# Accueil
# ---------------------------------------------------------------------------
HOME_FAQ = [
    ("Quel est le prix d'une ouverture de porte à Paris ?", "Une porte claquée est ouverte pour 110 € TTC en journée (8h–18h), 150 € en soirée et 220 € la nuit. Le tarif vous est annoncé au téléphone, puis confirmé par un devis écrit avant toute intervention."),
    ("Intervenez-vous dans tout Paris ?", "Oui, dans les 20 arrondissements, du 1er au 20e, 24h/24 et 7j/7, jours fériés compris. Nos serruriers sont répartis dans la capitale pour arriver vite."),
    ("En combien de temps arrivez-vous ?", "Comptez environ 30 minutes en moyenne dans Paris. Le délai précis dépend de la circulation : il vous est donné au téléphone avant le départ du serrurier."),
    ("Le devis est-il gratuit ?", "Oui, gratuit et sans engagement. Rien n'est fait sans votre signature, et vous restez libre de refuser."),
    ("Mon assurance peut-elle me rembourser ?", "Souvent, oui : effraction, vol ou perte de clés selon votre contrat. Notre facture détaillée est acceptée par les assureurs habitation."),
    ("Comment puis-je payer ?", "Par carte bancaire, en espèces ou par virement. Une facture vous est toujours remise."),
]

MOIS = ["janvier", "février", "mars", "avril", "mai", "juin", "juillet", "août", "septembre", "octobre", "novembre", "décembre"]


def fr_date(iso):
    y, m, d = iso.split("-")
    return f"{int(d)} {MOIS[int(m) - 1]} {y}"


def svc_cards():
    out = []
    for s in SERVICES:
        prix = f'<small>à partir de</small><b>{s["prix_num"]} € TTC</b>' if s["prix_num"] else "<small>tarif</small><b>Devis gratuit</b>"
        ph = photo(s["slug"], s["nom"], "svc-photo", "(max-width: 760px) 100vw, 380px")
        out.append(f'''<a class="svc{" has-photo" if ph else ""}" href="{svc_url(s)}">
  {ph}
  <div class="svc-body">
    <span class="svc-ic">{ico(s["icon"])}</span>
    <h3>{E(s["nom"])}</h3>
    <p>{E(s["resume"])}</p>
    <div class="svc-foot"><span class="svc-prix">{prix}</span><span class="svc-go">Détails {ico("i-arrow", "ic sm")}</span></div>
  </div>
</a>''')
    return '<div class="svc-grid">' + "".join(out) + "</div>"


def articles_cards(lst):
    return '<div class="posts">' + "".join(f'''<article class="post">
  <div class="post-top"><span class="post-ic">{ico(a["icon"])}</span><span class="post-cat">{E(a["cat"])}</span></div>
  <h3><a href="/conseils/{a["slug"]}/">{E(a["court"])}</a></h3>
  <p>{E(a["desc"])}</p>
  <span class="post-more"><time datetime="{a["date"]}">{fr_date(a["date"])}</time><span>Lire {ico("i-arrow", "ic sm")}</span></span>
</article>''' for a in lst) + "</div>"


def engagements():
    items = [
        ("i-euro", "Prix annoncé avant le déplacement", "Vous décrivez la situation, nous vous donnons le tarif TTC. Il ne change pas en route."),
        ("i-file", "Devis signé avant toute intervention", "Conformément à l'arrêté du 24 janvier 2017 : rien ne commence sans votre accord écrit."),
        ("i-door", "Ouverture sans casse en priorité", "Radio, crochetage, contournement : on préserve votre serrure chaque fois que c'est possible."),
        ("i-shield", "Matériel de grandes marques", "Cylindres et serrures de fabricants reconnus, modèles certifiés A2P sur demande."),
        ("i-card", "Paiement en toute transparence", "Carte bancaire, espèces ou virement, avec une facture détaillée à chaque fois."),
        ("i-phone", "Un serrurier au bout du fil", "Pas de centre d'appels : c'est un professionnel qui décroche, de jour comme de nuit."),
    ]
    return '<div class="engage">' + "".join(f'<div>{ico(i)}<h3>{E(t)}</h3><p>{E(d)}</p></div>' for i, t, d in items) + "</div>"


def build_home():
    visual = photo("accueil", f"{NOM}, serrurier à Paris", "hero-photo", "(max-width: 1100px) 100vw, 560px", eager=True)
    if not visual:
        visual = '<picture class="emblem"><source type="image/webp" srcset="/assets/img/logo-512.webp"><img src="/assets/img/icon-512.png" width="440" height="440" alt="Logo Secure Locksmith Paris" fetchpriority="high"></picture>'
    equipe = photo("equipe", "Serrurier qui conseille des clients devant leur porte", "about-photo")
    about_visual = equipe or company_card()
    body = f'''<section class="hero has-bg">
  {bg_img("tour-eiffel")}
  <div class="wrap hero-grid">
    <div class="hero-text">
      <span class="eyebrow light">Serrurier Paris 75 · 20 arrondissements</span>
      <h1>Serrurier à Paris,<br><span class="gold">24h/24 et 7j/7</span></h1>
      <p class="lead">Porte claquée, serrure bloquée, clé cassée, effraction : un serrurier qualifié intervient chez vous en 30 minutes en moyenne. Le prix vous est annoncé au téléphone et le devis est signé avant de commencer.</p>
      <div class="cta-row">{btn_call(cls="btn btn-gold btn-xl", track="call_hero")}<a class="btn btn-outline-light btn-xl" href="#devis">{ico("i-mail")}<span>Devis gratuit</span></a></div>
      <div class="hero-proof">
        {google_badge("g-badge dark")}
        <ul class="proof-list"><li>{ico("i-check")}Ouverture dès 110 € TTC</li><li>{ico("i-check")}Sans frais cachés</li><li>{ico("i-check")}Facture pour l'assurance</li></ul>
      </div>
    </div>
    <div class="hero-visual">
      {visual}
      <div class="float f1"><span class="live"><i></i>Disponible maintenant</span><b>Intervention ≈ 30 min</b></div>
      <div class="float f2">{ico("i-shield")}<span><b>Devis signé</b><small>avant chaque intervention</small></span></div>
    </div>
  </div>
</section>
{assureurs_strip()}
<section class="sec" id="services">
  <div class="wrap">
    <div class="sec-head split">
      <div><span class="eyebrow">Nos services</span><h2>Toutes les interventions de serrurerie, partout dans Paris</h2></div>
      <p>Appartement, maison de ville, commerce, cave ou local : nous intervenons sur tous les types de portes et de serrures, de la porte palière ancienne à la porte blindée multipoints.</p>
    </div>
    {svc_cards()}
  </div>
</section>
<section class="sec soft">
  <div class="wrap about">
    <div class="about-text">
      <span class="eyebrow">Pourquoi nous faire confiance</span>
      <h2>Un serrurier parisien identifié, qui s'engage par écrit</h2>
      <p class="lead-dark">Le dépannage en serrurerie a mauvaise réputation, souvent à juste titre. Chez {E(NOM)}, nous avons fait le choix inverse : une entreprise identifiée, des tarifs publics, et des engagements que vous pouvez vérifier.</p>
      {engagements()}
    </div>
    <div class="about-side">{about_visual}{company_card() if equipe else ""}</div>
  </div>
</section>
<section class="sec" id="tarifs">
  <div class="wrap">
    <div class="sec-head split">
      <div><span class="eyebrow">Tarifs</span><h2>Des prix clairs, publiés avant toute intervention</h2></div>
      <p>Nos tarifs dépendent de l'heure d'intervention. Ils sont affichés ici, annoncés au téléphone et confirmés par écrit : vous savez ce que vous allez payer avant que le serrurier ne parte.</p>
    </div>
    {tarif_table()}
  </div>
</section>
<section class="sec navy">
  <div class="wrap">
    <div class="sec-head center"><span class="eyebrow light">Déroulement</span><h2>Comment se passe une intervention</h2></div>
    <ol class="steps">
      <li><b>1</b><h3>Vous appelez</h3><p>Vous décrivez la porte et la situation, ou envoyez une photo sur WhatsApp.</p></li>
      <li><b>2</b><h3>Prix annoncé</h3><p>Le tarif TTC vous est donné immédiatement, avant le départ du serrurier.</p></li>
      <li><b>3</b><h3>Devis signé</h3><p>Sur place, le prix est confirmé par écrit. Rien ne commence sans votre signature.</p></li>
      <li><b>4</b><h3>Intervention et facture</h3><p>Travail soigné, facture détaillée à transmettre à votre assureur.</p></li>
    </ol>
    <div class="steps-cta">{btn_call("Appeler un serrurier", cls="btn btn-gold btn-lg", track="call_steps")}<span>ou envoyez une photo sur <a href="{E(wa_link("Bonjour, j'ai besoin d'un serrurier à Paris."))}" target="_blank" rel="noopener" data-track="wa_steps">WhatsApp</a></span></div>
  </div>
</section>
{reviews_block()}
<section class="sec">
  <div class="wrap">
    <div class="sec-head split">
      <div><span class="eyebrow">Marques</span><h2>Nous intervenons sur toutes les grandes marques</h2></div>
      <p>Serrures, cylindres, portes blindées et serrures connectées : nos serruriers connaissent les principaux fabricants et ont les pièces courantes dans leur véhicule.</p>
    </div>
    {marques_block()}
  </div>
</section>
<section class="sec soft" id="arrondissements">
  <div class="wrap">
    <div class="sec-head split">
      <div><span class="eyebrow">Zone d'intervention</span><h2>Un serrurier dans chaque arrondissement de Paris</h2></div>
      <p>Nous intervenons exclusivement dans Paris intra-muros. Choisissez votre arrondissement pour voir les quartiers desservis et nos services près de chez vous.</p>
    </div>
    {arr_grid()}
  </div>
</section>
<section class="sec" id="faq">
  <div class="wrap faq-wrap">
    <div class="sec-head">
      <span class="eyebrow">Questions fréquentes</span>
      <h2>Vos questions, nos réponses</h2>
      <p>Une autre question ? Appelez-nous, nous répondons 24h/24.</p>
      <a class="btn btn-outline" href="/questions-frequentes/">Toutes les questions</a>
    </div>
    {faq_html(HOME_FAQ)}
  </div>
</section>
<section class="sec soft">
  <div class="wrap">
    <div class="sec-head split">
      <div><span class="eyebrow">Conseils</span><h2>Guides pratiques de nos serruriers</h2></div>
      <p><a class="text-link" href="/conseils/">Voir tous les conseils {ico("i-arrow", "ic sm")}</a></p>
    </div>
    {articles_cards(ARTICLES[:4])}
  </div>
</section>
{contact_band()}'''
    ld = [ld_business(full=True), ld_faq(HOME_FAQ),
          {"@context": "https://schema.org", "@type": "WebSite", "name": NOM, "url": URL + "/", "inLanguage": "fr-FR", "publisher": {"@id": BID}}]
    page("/", f"Serrurier Paris 24h/24 – {TEL} | {NOM}",
         f"Serrurier à Paris (75), 24h/24 dans les 20 arrondissements. Ouverture de porte dès 110 € TTC, prix annoncé avant déplacement, devis signé, facture pour l'assurance. ☎ {TEL}",
         body, ld)


# ---------------------------------------------------------------------------
# Services
# ---------------------------------------------------------------------------
def build_services():
    items = "".join(f'''<a class="svc-row" href="{svc_url(s)}"><span class="svc-ic">{ico(s["icon"])}</span>
  <div><h2>{E(s["nom"])}</h2><p>{E(s["resume"])}</p></div><span class="svc-prix">{E(s["prix"])}{ico("i-chev", "ic go")}</span></a>''' for s in SERVICES)
    body = hero([("Services", None)], "Nos services de serrurerie à Paris",
                "Ouverture de porte, serrure bloquée, clé cassée, changement de serrure, serrure connectée, sécurisation après effraction : toutes nos interventions, avec leurs prix de départ.",
                kicker="24h/24 · 7j/7")
    body += f'<section class="sec"><div class="wrap layout"><div class="svc-rows">{items}</div>{side_box()}</div></section>'
    body += assureurs_strip() + f'<section class="sec"><div class="wrap"><div class="sec-head"><span class="eyebrow">Marques</span><h2>Toutes les grandes marques</h2></div>{marques_block()}</div></section>' + contact_band(source="/services/")
    page("/services/", f"Services de serrurerie à Paris 24h/24 | {NOM}",
         "Tous nos dépannages de serrurerie à Paris : ouverture de porte dès 110 €, serrure bloquée, clé cassée, changement de serrure, serrure connectée, après effraction.",
         body, [ld_business(), ld_crumbs([("Services", "/services/")])], active="/services/")

    for s in SERVICES:
        path = svc_url(s)
        secs = "".join(f"<h2>{E(t)}</h2><p>{c}</p>" for t, c in s["sections"])
        prix = f"dès <strong>{s['prix_num']} € TTC</strong>" if s["prix_num"] else "<strong>sur devis gratuit</strong>"
        others = "".join(f'<a class="chip" href="{svc_url(o)}">{ico(o["icon"])}{E(o["court"])}</a>' for o in SERVICES if o is not s)
        ph = photo(s["slug"], s["nom"], "prose-photo", "(max-width: 1100px) 100vw, 760px")
        content = f'''<article class="prose">
  <p class="intro">{s["intro"]}</p>
  {ph}
  <div class="note-box">{ico("i-euro")}<p>Tarif : {prix}. Le prix exact vous est annoncé au téléphone et confirmé par un devis écrit avant l'intervention. <a href="/tarifs/">Grille jour, soirée, nuit</a></p></div>
  {secs}
  <h2>{E(s["court"])} : choisissez votre arrondissement</h2>
  {arr_grid(link=lambda z: combo_url(s, z), cls="arr-grid compact")}
  <h2>Questions fréquentes</h2>
  {faq_html(s["faq"])}
  <h2>Nos autres services</h2><div class="chips">{others}</div>
</article>'''
        card = hero_card("dès %d € TTC" % s["prix_num"] if s["prix_num"] else "Devis gratuit", s["court"])
        body = hero([("Services", "/services/"), (s["court"], None)], f'{E(s["nom"])} à Paris',
                    f'{E(s["resume"])} Partout dans Paris, 24h/24.',
                    ticks(["Prix annoncé avant déplacement", "Devis signé avant travaux", "Facture pour l'assurance"], "ticks light inline"), kicker="Service", card=card)
        body += f'<section class="sec"><div class="wrap layout">{content}{side_box()}</div></section>'
        body += assureurs_strip() + reviews_block() + contact_band(f"{s['court']} ? Nous intervenons rapidement.", "Appelez ou laissez vos coordonnées : nous vous rappelons avec un prix clair.", source=path, service=s["court"])
        ld = [ld_business(), ld_crumbs([("Services", "/services/"), (s["court"], path)]), ld_faq(s["faq"]),
              {"@context": "https://schema.org", "@type": "Service", "name": s["nom"], "serviceType": s["nom"], "url": URL + path,
               "provider": {"@id": BID}, "areaServed": {"@type": "City", "name": "Paris"},
               **({"offers": {"@type": "Offer", "priceSpecification": {"@type": "PriceSpecification", "minPrice": s["prix_num"], "priceCurrency": "EUR"}}} if s["prix_num"] else {})}]
        page(path, f'{s["nom"]} Paris 24h/24 – {s["prix"].replace(" TTC", "").replace("sur devis gratuit", "devis gratuit")} | {NOM}',
             f'{s["nom"]} à Paris, 24h/24 et 7j/7. {s["resume"]} Prix annoncé avant déplacement. ☎ {TEL}', body, ld, active="/services/")


# ---------------------------------------------------------------------------
# Arrondissements
# ---------------------------------------------------------------------------
ARR_INTROS = [
    "Bloqué devant chez vous {a} ? {nom} envoie un serrurier qualifié à votre porte, jour et nuit, généralement en une trentaine de minutes. Le tarif vous est donné au téléphone avant son départ.",
    "Du côté {r0} comme dans les rues plus calmes du {num}, nos serruriers interviennent 24h/24 pour les portes claquées, les serrures bloquées et les clés cassées, avec un devis signé avant tout travail.",
    "Avec {pop} habitants, le {num} arrondissement ({surnom}) voit chaque jour son lot de portes claquées et de clés perdues. Nos serruriers connaissent ses immeubles et les serrures qui les équipent.",
    "Une urgence de serrurerie {a} ? Des quartiers {q} jusqu'aux abords {r1}, nous intervenons vite, à prix annoncé, avec une facture acceptée par votre assurance.",
]


def arr_faq(z):
    return [
        (f"Combien coûte un serrurier {z['a_court']} ?", f"Une ouverture de porte claquée {z['a']} coûte 110 € TTC en journée, 150 € en soirée et 220 € la nuit. Un changement de cylindre démarre à 160 €. Le prix est toujours annoncé avant le déplacement et confirmé par écrit."),
        (f"En combien de temps arrivez-vous {z['a']} ?", f"Environ 30 minutes en moyenne. Le délai exact dépend de la circulation dans Paris et vous est annoncé au téléphone avant le départ du serrurier."),
        (f"Intervenez-vous la nuit {z['a_court']} ?", "Oui, 24h/24 et 7j/7, y compris le dimanche et les jours fériés, avec un tarif de nuit annoncé à l'avance."),
        ("Ma facture sera-t-elle remboursée ?", "Notre facture détaillée est acceptée par les assureurs habitation. Le remboursement dépend des garanties de votre contrat (effraction, vol ou perte de clés)."),
    ]


def build_arr_pages():
    body = hero([("Arrondissements", None)], "Serrurier dans les <em>20 arrondissements de Paris</em>",
                "Choisissez votre arrondissement : tarifs, quartiers desservis et services disponibles près de chez vous.", kicker="Paris 75")
    body += f'''<section class="sec"><div class="wrap">
  {arr_grid(label=lambda z: z["surnom"])}
  <div class="prose narrow">
    <h2>Un serrurier parisien, pas une plateforme</h2>
    <p>{E(NOM)} intervient exclusivement dans Paris intra-muros. Cette spécialisation nous permet d'arriver vite et de bien connaître le bâti parisien : portes palières d'immeubles haussmanniens, portes blindées multipoints, serrures anciennes à gorges, résidences modernes à badge.</p>
    <p class="note-box">{ico("i-pin")}Vous êtes juste en dehors de Paris ? Appelez-nous au <a href="{TEL_HREF}">{TEL}</a> : selon la disponibilité de nos serruriers, nous pouvons parfois intervenir, avec des frais de déplacement annoncés à l'avance.</p>
  </div>
</div></section>''' + reviews_block() + contact_band(source="/serrurier-paris/")
    page("/serrurier-paris/", f"Serrurier Paris : les 20 arrondissements 24h/24 | {NOM}",
         f"Serrurier dans tout Paris, du 1er au 20e arrondissement, 24h/24. Ouverture de porte dès 110 € TTC, prix annoncé avant déplacement. ☎ {TEL}",
         body, [ld_business(full=True), ld_crumbs([("Arrondissements", "/serrurier-paris/")])], active="/serrurier-paris/")

    for i, z in enumerate(ARR):
        path = z["url"]
        intro = ARR_INTROS[i % 4].format(a=z["a"], nom=E(NOM), num=z["num"], r0=de(z["reperes"][0]), r1=de(z["reperes"][1]),
                                         pop=fmt_int(z["pop"]), surnom=z["surnom"], q=et(z["quartiers"][:2]))
        facts = f'''<div class="facts">
  <div><small>Code postal</small><b>{E(" / ".join(z["cp"]))}</b></div>
  <div><small>Ouverture de porte</small><b>dès 110 € TTC</b></div>
  <div><small>Disponibilité</small><b>24h/24 · 7j/7</b></div>
  <div><small>Délai moyen</small><b>≈ 30 min</b></div>
</div>'''
        svc = "".join(f'''<a class="svc-row" href="{combo_url(s, z)}"><span class="svc-ic">{ico(s["icon"])}</span>
  <div><h3>{E(s["nom"])} {E(z["a_court"])}</h3><p>{E(s["resume"])}</p></div><span class="svc-prix">{E(s["prix"])}</span></a>''' for s in SERVICES)
        nav_arr = ""
        if z["prev"]:
            nav_arr += f'<a href="{z["prev"]["url"]}">← Serrurier {E(z["prev"]["court"])}</a>'
        if z["next"]:
            nav_arr += f'<a href="{z["next"]["url"]}">Serrurier {E(z["next"]["court"])} →</a>'
        faq = arr_faq(z)
        content = f'''<article class="prose">
  <p class="intro">{intro}</p>
  {facts}
  <h2>Nos services {E(z["a"])}</h2>
  <div class="svc-rows">{svc}</div>
  <h2>Quartiers desservis dans le {z["num"]}</h2>
  <p>Nous couvrons les quatre quartiers administratifs de l'arrondissement : <strong>{E(et(z["quartiers"]))}</strong>. Que vous habitiez près {E(de_list(z["reperes"]))}, un serrurier peut être chez vous rapidement.</p>
  <div class="local">
    <div>{ico("i-metro")}<h3>Repères</h3><p>Stations {E(et(z["metros"]))}</p></div>
    <div>{ico("i-home")}<h3>Le bâti</h3><p>{E(z["habitat"][0].upper() + z["habitat"][1:])}.</p></div>
    <div>{ico("i-pin")}<h3>Population</h3><p>{fmt_int(z["pop"])} habitants (INSEE)</p></div>
  </div>
  <h2>Pourquoi nous appeler {E(z["a"])} ?</h2>
  <ul class="check-list">
    <li>{ico("i-check")}<span><strong>Prix annoncé au téléphone</strong>, puis devis écrit signé avant l'intervention.</span></li>
    <li>{ico("i-check")}<span><strong>Ouverture sans casse</strong> dans la grande majorité des cas.</span></li>
    <li>{ico("i-check")}<span><strong>Facture détaillée</strong> acceptée par les assureurs habitation.</span></li>
    <li>{ico("i-check")}<span><strong>Avis publics</strong> et vérifiables sur <a href="{E(MAPS)}" target="_blank" rel="noopener">notre fiche Google</a>.</span></li>
  </ul>
  <h2>Questions fréquentes {E(z["a_court"])}</h2>
  {faq_html(faq)}
  <nav class="prev-next" aria-label="Arrondissements voisins">{nav_arr}</nav>
</article>'''
        h1 = f'Serrurier {E(z["court"])} <em>24h/24</em>'
        lead = f'Ouverture de porte dès 110 € TTC, serrure bloquée, clé cassée, changement de serrure {E(z["a"])} ({E(z["surnom"])}). Prix annoncé avant déplacement, devis gratuit.'
        crumb_items = [("Arrondissements", "/serrurier-paris/"), (f"Paris {z['num']}", None)]
        body = hero(crumb_items, h1, lead, ticks(["Devis gratuit", "Sans frais cachés", "Nuit, week-end, jours fériés"], "ticks light inline"),
                    kicker=f"{z['cp'][0]} · {z['surnom']}", bg=zone_bg(z))
        body += f'<section class="sec"><div class="wrap layout">{content}{side_box(f"Serrurier {z["court"]}")}</div></section>'
        body += assureurs_strip() + contact_band(f"Bloqué dehors {z['a_court']} ?", "Appelez-nous : prix annoncé au téléphone, serrurier en route aussitôt.", source=path, arr=z["court"])
        ld = [ld_business(), ld_crumbs([("Arrondissements", "/serrurier-paris/"), (f"Paris {z['num']}", path)]), ld_faq(faq),
              {"@context": "https://schema.org", "@type": "Service", "name": f"Serrurier {z['nom']}", "serviceType": "Serrurerie, dépannage 24h/24",
               "url": URL + path, "provider": {"@id": BID},
               "areaServed": {"@type": "AdministrativeArea", "name": z["nom"], "postalCode": z["cp"][0]},
               "offers": {"@type": "Offer", "priceSpecification": {"@type": "PriceSpecification", "minPrice": 110, "priceCurrency": "EUR"}}}]
        page(path, f"Serrurier {z['court']} ({z['cp'][0]}) 24h/24 – {TEL}",
             f"Serrurier {z['court']} ({z['cp'][0]}), 24h/24 et 7j/7 : ouverture de porte dès 110 € TTC, serrure bloquée, clé cassée, changement de serrure. Prix annoncé avant déplacement. ☎ {TEL}",
             body, ld, active="/serrurier-paris/")


# ---------------------------------------------------------------------------
# Service × arrondissement
# ---------------------------------------------------------------------------
SVC_LOCAL = {
    "ouverture-de-porte": {
        "intros": [
            "Porte claquée {a} et clés restées à l'intérieur ? Un serrurier {nom} se met en route aussitôt pour l'ouvrir en douceur, souvent en quelques minutes et sans toucher à la serrure. Le prix vous est donné avant son départ.",
            "Pas de panique si la porte s'est refermée derrière vous {a} : une porte claquée s'ouvre presque toujours sans dégât, à la radio ou au crochetage. Nous intervenons jour et nuit, à tarif annoncé.",
            "Coincé sur le palier {a} ? Appelez : vous connaissez le prix avant l'arrivée du serrurier, et votre porte est ouverte sans casse dans la grande majorité des cas.",
        ],
        "conseil": "Évitez la carte bancaire ou le tournevis : ils abîment la gâche et le joint, ce qui rallonge l'intervention.",
    },
    "serrure-bloquee": {
        "intros": [
            "Votre clé refuse de tourner {a} ? Nos serruriers diagnostiquent le blocage et le règlent sur place : nettoyage, réglage de la gâche ou remplacement du cylindre s'il le faut. Prix annoncé avant le déplacement.",
            "Serrure grippée, porte qui ne s'ouvre plus ou ne se verrouille plus {a} : un serrurier arrive avec les pièces courantes pour tout régler en une seule visite dans la plupart des cas.",
            "Un pêne qui frotte, un cylindre encrassé, une porte qui a bougé : les serrures bloquées sont fréquentes {a}. Nous réparons d'abord, et ne remplaçons que si c'est vraiment nécessaire.",
        ],
        "conseil": "Ne forcez pas sur la clé et oubliez l'huile de cuisine : un lubrifiant sec (graphite, PTFE) est bien plus adapté.",
    },
    "cle-cassee": {
        "intros": [
            "Clé cassée dans la serrure {a} ? Nos serruriers retirent le morceau avec des extracteurs dédiés, sans démonter la serrure dans la plupart des cas, 24h/24, sur devis gratuit.",
            "Un fragment de clé coincé dans le cylindre {a} : un serrurier vient l'extraire, vérifie le cylindre et le remplace sur place seulement si c'est utile.",
            "Une vieille clé qui cède dans la serrure, c'est courant {a}. Nous retirons le morceau proprement, puis vous conseillons : refaire une clé ou changer un cylindre fatigué.",
        ],
        "conseil": "Ni colle, ni trombone : vous risquez d'enfoncer le morceau et de rendre le cylindre irrécupérable.",
    },
    "changement-de-serrure": {
        "intros": [
            "Clés perdues, emménagement ou serrure usée {a} : nous remplaçons cylindres et serrures, du modèle standard à la multipoints certifiée A2P. Devis gratuit et signé avant travaux.",
            "Changement de serrure {a} : le serrurier arrive avec un choix de cylindres en stock, vous présente les options et leurs prix, puis pose le modèle retenu le jour même.",
            "Vous venez d'emménager {a} ou vous avez perdu vos clés ? Remplacer le cylindre est la façon la plus simple de reprendre la main sur vos accès. Matériel certifié, facture détaillée.",
        ],
        "conseil": "Regardez le nombre d'étoiles A2P (de 1 à 3) : c'est le niveau de résistance à l'effraction, parfois exigé par l'assurance.",
    },
    "serrure-connectee": {
        "intros": [
            "Envie d'ouvrir votre porte avec votre téléphone {a} ? Nous installons et paramétrons des serrures connectées compatibles avec votre porte, et dépannons celles qui ne répondent plus.",
            "Serrure connectée {a} : pose, réglage, dépannage en cas de piles vides ou de moteur bloqué. Nous vérifions la compatibilité de votre cylindre avant toute installation.",
            "Smart lock en panne ou projet d'installation {a} : nous ouvrons 24h/24 une porte équipée d'une serrure connectée bloquée, et installons sur rendez-vous.",
        ],
        "conseil": "Gardez une clé mécanique de secours et surveillez les piles : c'est la première cause de serrure connectée bloquée.",
    },
    "apres-effraction": {
        "intros": [
            "Cambriolage ou tentative d'effraction {a} ? Nous sécurisons votre porte en urgence, 24h/24, puis la remettons en état ou la renforçons. Facture détaillée pour votre assurance.",
            "Porte forcée {a} : un serrurier se déplace jour et nuit pour poser une fermeture provisoire ou définitive et remplacer le cylindre abîmé.",
            "Après une effraction {a}, l'urgence est de pouvoir refermer dès ce soir. Nous intervenons vite, sur devis gratuit, et vous conseillons sur les renforts adaptés.",
        ],
        "conseil": "Photographiez les dégâts et déposez plainte avant les travaux définitifs : votre assureur demandera le récépissé.",
    },
}

ETAPES = [
    ("Appel", "vous décrivez la situation, le prix vous est annoncé"),
    ("Trajet", "le serrurier part vers votre adresse {a} et vous prévient de son arrivée"),
    ("Devis", "il confirme le prix par écrit, vous signez avant qu'il commence"),
    ("Intervention", "travail soigné, puis facture détaillée pour votre assureur"),
]


def combo_faq(s, z, k):
    prix = f"dès {s['prix_num']} € TTC" if s["prix_num"] else "sur devis gratuit"
    return [
        (f"Quel prix pour {s['phrase']} {z['a_court']} ?", f"Ce service est proposé {prix} {z['a']}. Le prix exact dépend de votre porte et de votre serrure : il est annoncé au téléphone puis confirmé par un devis signé."),
        (f"Pouvez-vous venir rapidement {z['a']} ?", "Oui, en environ 30 minutes en moyenne, 24h/24 et 7j/7, nuits, week-ends et jours fériés compris."),
        s["faq"][k % len(s["faq"])],
    ]


def build_combo_pages():
    for si, s in enumerate(SERVICES):
        loc = SVC_LOCAL[s["slug"]]
        for i, z in enumerate(ARR):
            k = i + si
            path = combo_url(s, z)
            intro = loc["intros"][k % 3].format(a=z["a"], nom=E(NOM))
            t1, c1 = s["sections"][k % 3]
            t2, c2 = s["sections"][(k + 1) % 3]
            etapes = "".join(f"<li><b>{E(t)}</b><span>{E(d.format(a=z['a']))}</span></li>" for t, d in ETAPES)
            faq = combo_faq(s, z, k)
            prix_txt = f"dès <strong>{s['prix_num']} € TTC</strong>" if s["prix_num"] else "<strong>sur devis gratuit</strong>"
            others = "".join(f'<a class="chip" href="{combo_url(o, z)}">{ico(o["icon"])}{E(o["court"])}</a>' for o in SERVICES if o is not s)
            voisins = [v for v in (z["prev"], z["next"]) if v]
            vlinks = "".join(f'<a class="chip" href="{combo_url(s, v)}">{ico(s["icon"])}{E(s["court"])} {E(v["court"])}</a>' for v in voisins)
            content = f'''<article class="prose">
  <p class="intro">{intro}</p>
  <div class="facts">
    <div><small>Tarif</small><b>{E(s["prix"].replace(" TTC", ""))}</b></div>
    <div><small>Code postal</small><b>{E(" / ".join(z["cp"]))}</b></div>
    <div><small>Disponibilité</small><b>24h/24 · 7j/7</b></div>
    <div><small>Délai moyen</small><b>≈ 30 min</b></div>
  </div>
  <div class="note-box">{ico("i-euro")}<p>Tarif {prix_txt}, annoncé au téléphone et confirmé par un devis signé. Aucun frais caché. <a href="/tarifs/">Voir tous nos tarifs →</a></p></div>
  <h2>{E(s["court"])} dans le {z["num"]} : où intervenons-nous ?</h2>
  <p>Partout dans l'arrondissement ({E(z["surnom"])}) : quartiers <strong>{E(et(z["quartiers"]))}</strong>, autour {E(de_list(z["reperes"]))} et des stations {E(et(z["metros"]))}. On y trouve surtout des {E(z["habitat"])} : nos serruriers sont équipés pour ces configurations, des portes anciennes aux portes blindées multipoints.</p>
  <h2>{E(t1)}</h2><p>{c1}</p>
  <h2>Déroulement de l'intervention</h2>
  <ol class="steps-list">{etapes}</ol>
  <h2>{E(t2)}</h2><p>{c2}</p>
  <div class="note-box tip">{ico("i-award")}<p><strong>Le conseil du serrurier :</strong> {E(loc["conseil"])}</p></div>
  <h2>Questions fréquentes</h2>
  {faq_html(faq)}
  <h2>Autres services {E(z["a_court"])}</h2>
  <div class="chips">{others}<a class="chip" href="{z["url"]}">{ico("i-pin")}Serrurier {E(z["court"])}</a></div>
  <h2>Arrondissements voisins</h2>
  <div class="chips">{vlinks}<a class="chip" href="{svc_url(s)}">{ico(s["icon"])}{E(s["court"])} dans tout Paris</a></div>
</article>'''
            h1 = f'{E(s["nom"])} <em>{E(z["a_court"])}</em>'
            lead = f'{E(s["resume"])} Intervention 24h/24 {E(z["a"])}, {"dès %d € TTC" % s["prix_num"] if s["prix_num"] else "sur devis gratuit"}.'
            crumb_items = [("Arrondissements", "/serrurier-paris/"), (f"Paris {z['num']}", z["url"]), (s["court"], None)]
            body = hero(crumb_items, h1, lead, ticks(["Prix annoncé avant déplacement", "Devis signé", "Nuit et week-end"], "ticks light inline"),
                        kicker=f"{z['cp'][0]} · {z['surnom']}", bg=zone_bg(z))
            body += f'<section class="sec"><div class="wrap layout">{content}{side_box(f"{s["court"]} {z["court"]}")}</div></section>'
            body += contact_band(f"{s['court']} {z['a_court']} ?", "Appelez-nous : prix annoncé au téléphone, serrurier en route aussitôt.",
                                 source=path, service=s["court"], arr=z["court"])
            prix_court = f"dès {s['prix_num']} €" if s["prix_num"] else "devis gratuit"
            title = f'{s["court"]} {z["court"]} ({z["cp"][0]}) – {prix_court}, 24h/24'
            desc = (f'{s["nom"]} {z["a_court"]} ({z["cp"][0]}), 24h/24 et 7j/7, {"dès %d € TTC" % s["prix_num"] if s["prix_num"] else "devis gratuit"}. '
                    f'Prix annoncé avant déplacement, devis signé, facture pour l\'assurance. ☎ {TEL}')
            ld = [ld_business(), ld_crumbs([("Arrondissements", "/serrurier-paris/"), (f"Paris {z['num']}", z["url"]), (s["court"], path)]), ld_faq(faq),
                  {"@context": "https://schema.org", "@type": "Service", "name": f"{s['nom']} {z['a_court']}", "serviceType": s["nom"],
                   "url": URL + path, "provider": {"@id": BID},
                   "areaServed": {"@type": "AdministrativeArea", "name": z["nom"], "postalCode": z["cp"][0]},
                   **({"offers": {"@type": "Offer", "priceSpecification": {"@type": "PriceSpecification", "minPrice": s["prix_num"], "priceCurrency": "EUR"}}} if s["prix_num"] else {})}]
            page(path, title, desc, body, ld, active="/serrurier-paris/")


# ---------------------------------------------------------------------------
# Pages simples
# ---------------------------------------------------------------------------
def simple(path, crumb, h1, lead, prose, title, desc, extra_ld=(), active=None, after="", aside=True, robots="index, follow"):
    body = hero([(crumb, None)], h1, lead)
    inner = f'<article class="prose">{prose}</article>' + (side_box() if aside else "")
    body += f'<section class="sec"><div class="wrap{" layout" if aside else " narrow"}">{inner}</div></section>' + after
    page(path, title, desc, body, [ld_business(), ld_crumbs([(crumb, path)]), *extra_ld], active=active, robots=robots)


def ld_tarifs():
    offers = []
    for p, jour, *_ in TARIFS:
        m = re.search(r"([\d  ]+)\s*€", jour)
        if not m:
            continue
        val = int(re.sub(r"\D", "", m.group(1)))
        spec = {"@type": "PriceSpecification", "priceCurrency": "EUR", "valueAddedTaxIncluded": True}
        spec.update({"minPrice": val} if jour.startswith("À partir") else {"price": val})
        offers.append({"@type": "Offer", "name": p, "priceSpecification": spec, "itemOffered": {"@type": "Service", "name": p}, "seller": {"@id": BID}})
    return {"@context": "https://schema.org", "@type": "OfferCatalog", "name": f"Tarifs {NOM}", "url": URL + "/tarifs/", "itemListElement": offers}


def build_static():
    # Tarifs
    body = hero([("Tarifs", None)], "Nos tarifs, <em>affichés noir sur blanc</em>",
                "Prix par prestation et par heure d'intervention. Tout est annoncé avant le déplacement, rien n'est ajouté en route.", kicker="Transparence")
    body += f'''<section class="sec"><div class="wrap">
  {tarif_table()}
  <div class="layout" style="margin-top:56px">
    <article class="prose">
      <h2>Ce que le prix comprend</h2>
      <ul><li>La main d'œuvre du serrurier.</li><li>Le déplacement dans Paris, offert si des travaux sont réalisés.</li><li>La TVA : tous nos prix sont TTC.</li><li>Une facture détaillée, conforme pour votre assurance.</li></ul>
      <h2>Nos engagements</h2>
      <ul><li><strong>Tarif annoncé</strong> avant le départ du technicien.</li><li><strong>Devis écrit et signé</strong> avant tout travail.</li><li><strong>Pas de majoration surprise</strong> : le tarif de soirée ou de nuit est donné au téléphone.</li><li><strong>Matériel certifié</strong> et garanti.</li></ul>
      <h2>Clé cassée, serrure connectée, après effraction</h2>
      <p>Ces interventions dépendent beaucoup de la situation : elles font l'objet d'un <strong>devis gratuit</strong>, donné au téléphone puis confirmé par écrit.</p>
      <h2>Paiement</h2><p>Carte bancaire, espèces ou virement.</p>
    </article>
    {side_box("Votre prix au téléphone", "Décrivez la situation : vous connaissez le tarif exact avant que nous partions.")}
  </div>
</div></section>''' + assureurs_strip() + contact_band(source="/tarifs/")
    page("/tarifs/", f"Tarifs serrurier Paris – jour, soirée, nuit | {NOM}",
         "Tarifs serrurier à Paris : ouverture de porte claquée 110 € TTC en journée, porte fermée à clé dès 180 €, changement de cylindre dès 160 €. Prix de soirée et de nuit affichés.",
         body, [ld_business(), ld_crumbs([("Tarifs", "/tarifs/")]), ld_tarifs()], active="/tarifs/")

    # Assurance
    simple("/assurance/", "Assurance", "Serrurier et assurance : <em>se faire rembourser</em>",
           "Nos factures sont acceptées par les assureurs habitation. Voici comment obtenir le remboursement d'une intervention.",
           f'''<h2>Dans quels cas l'assurance rembourse ?</h2>
<p>La plupart des contrats multirisques habitation couvrent les frais de serrurerie après un <strong>cambriolage ou une tentative d'effraction</strong>. Certains prennent aussi en charge le <strong>vol</strong> ou la <strong>perte des clés</strong>, parfois en option. Une porte simplement claquée est rarement couverte, sauf garantie d'assistance : relisez votre contrat.</p>
<h2>Les pièces à fournir</h2>
<ul><li>Le <strong>récépissé de plainte</strong> en cas d'effraction ou de vol.</li><li>Notre <strong>facture détaillée</strong> (intervention, matériel posé, prix TTC).</li><li>Le <strong>devis signé</strong> et, sur demande, des <strong>photos avant/après</strong>.</li></ul>
<h2>Les délais</h2>
<p>Après un vol ou un cambriolage, la déclaration doit en général être faite sous <strong>2 jours ouvrés</strong>. Pour les autres sinistres, le délai est souvent de 5 jours ouvrés. Votre contrat fait foi.</p>
<h2>Notre accompagnement</h2>
<p>Nous vous remettons tous les justificatifs et pouvons sécuriser provisoirement la porte en attendant le passage de l'expert.</p>
<p class="note-box">{ico("i-shield")}{E(NOM)} est une entreprise indépendante, sans partenariat avec les compagnies d'assurance. Le remboursement dépend des garanties de votre contrat.</p>''',
           f"Serrurier et assurance habitation : facture remboursable | {NOM}",
           "Faire rembourser un serrurier par son assurance habitation : garanties, documents, délais. Nos factures sont acceptées par les assureurs.",
           after=assureurs_strip() + contact_band(source="/assurance/"))

    # FAQ
    allfaq = HOME_FAQ + [q for s in SERVICES for q in s["faq"]]
    simple("/questions-frequentes/", "Questions fréquentes", "Questions <em>fréquentes</em>",
           "Prix, délais, assurance, techniques d'ouverture : tout ce que l'on nous demande le plus souvent.",
           "<h2>En général</h2>" + faq_html(HOME_FAQ) + "".join(f'<h2>{E(s["court"])}</h2>' + faq_html(s["faq"]) for s in SERVICES),
           f"Questions fréquentes – serrurier Paris | {NOM}",
           "Prix d'une ouverture de porte, délai d'intervention, remboursement par l'assurance, ouverture sans casse : nos réponses.",
           extra_ld=[ld_faq(allfaq)], after=contact_band(source="/questions-frequentes/"))

    # Avis
    body = hero([("Avis clients", None)], "Avis clients <em>sur Google</em>",
                "Nos clients publient leurs avis sur notre fiche Google : ils sont publics et vérifiables.", google_badge("g-badge dark"))
    body += reviews_block("Notre réputation, en toute transparence") + contact_band(source="/avis/")
    page("/avis/", f"Avis clients – serrurier Paris | {NOM}", "Consultez les avis Google de nos clients et laissez le vôtre. Serrurier à Paris 24h/24.",
         body, [ld_business(), ld_crumbs([("Avis clients", "/avis/")])], active="/avis/")

    # Contact
    body = hero([("Contact", None)], "Contacter <em>votre serrurier</em>",
                "Pour une urgence, le téléphone est le plus rapide. Pour un devis ou des travaux, écrivez-nous.")
    body += f'''<section class="sec cream"><div class="wrap contact-grid">
  <div class="contact-card">
    <h2>{E(NOM)}</h2>
    <p>{E(CONFIG["slogan"])}, dans les 20 arrondissements de Paris, 24h/24 et 7j/7.</p>
    <a class="c-line" href="{TEL_HREF}" data-track="call_contact">{ico("i-phone")}<span><small>Téléphone 24h/24</small><b>{TEL}</b></span></a>
    <a class="c-line" href="{E(wa_link("Bonjour, j'ai besoin d'un serrurier à Paris."))}" target="_blank" rel="noopener" data-track="wa_contact">{ico("i-wa")}<span><small>WhatsApp</small><b>Envoyer une photo</b></span></a>
    <a class="c-line" href="mailto:{CONFIG["email"]}">{ico("i-mail")}<span><small>E-mail</small><b>{CONFIG["email"]}</b></span></a>
    <a class="c-line" href="{CONFIG["instagram"]}" target="_blank" rel="noopener me">{ico("i-insta")}<span><small>Instagram</small><b>@securelockserrurerie</b></span></a>
    <div class="c-line">{ico("i-pin")}<span><small>Zone d'intervention</small><b>Paris, du 1<sup>er</sup> au 20<sup>e</sup> arrondissement</b></span></div>
  </div>
  {lead_form("/contact/", titre="Écrivez-nous", sous="Devis, rappel, question : réponse rapide, 7j/7.")}
</div></section>
<section class="sec"><div class="wrap"><div class="sec-head"><span class="eyebrow">Notre fiche Google</span><h2>Où nous trouver</h2></div>{map_embed()}</div></section>''' + reviews_block()
    page("/contact/", f"Contact – serrurier Paris 24h/24 | {NOM}",
         f"Contactez {NOM} au {TEL}, 24h/24 et 7j/7, par WhatsApp ou par e-mail. Devis gratuit, intervention rapide dans tout Paris.",
         body, [ld_business(full=True), ld_crumbs([("Contact", "/contact/")])], active="/contact/")

    # Mentions légales
    a = CONFIG["adresse"]
    adresse = ", ".join(v for v in (a["rue"], f'{a["cp"]} {a["ville"]}'.strip()) if v)
    lignes = [E(CONFIG["raison_sociale"]) + (f" ({E(NOM)})" if NOM != CONFIG["raison_sociale"] else "")]
    if CONFIG["responsable"]:
        lignes.append(f"Responsable de la publication : {E(CONFIG['responsable'])}")
    if CONFIG["siren"]:
        lignes.append(f"SIREN : {CONFIG['siren']}")
    if CONFIG["siret"]:
        lignes.append(f"SIRET : {CONFIG['siret']}")
    lignes += [f"Adresse : {E(adresse)}", f"Téléphone : {TEL}", f"E-mail : {CONFIG['email']}"]
    mediateur = E(CONFIG["mediateur"]) or "ses coordonnées vous sont communiquées sur simple demande à " + CONFIG["email"]
    simple("/mentions-legales/", "Mentions légales", "Mentions légales", "Informations légales relatives au site et à l'entreprise.",
           f'''<h2>Éditeur du site</h2><p>{"<br>".join(lignes)}</p>
<h2>Hébergement</h2><p>Netlify, Inc. – 44 Montgomery Street, Suite 300, San Francisco, CA 94104, États-Unis.</p>
<h2>Propriété intellectuelle</h2><p>Les textes, le logo et les éléments graphiques de ce site appartiennent à {E(NOM)}, sauf mention contraire. Les noms de compagnies d'assurance et de marques sont cités à titre informatif et n'impliquent aucun partenariat.</p>
<h2>Médiation de la consommation</h2><p>Conformément à l'article L612-1 du Code de la consommation, vous pouvez recourir gratuitement à un médiateur de la consommation : {mediateur}.</p>
<h2>Prix et devis</h2><p>Les prix affichés sont des prix de départ TTC. Conformément à l'arrêté du 24 janvier 2017 relatif aux prestations de dépannage, de réparation et d'entretien dans le secteur du bâtiment, un devis détaillé et gratuit est remis et signé avant toute intervention, et une note détaillée est remise à la fin de la prestation.</p>
<h2>Responsabilité</h2><p>Les informations de ce site sont données à titre indicatif et peuvent évoluer.</p>''',
           f"Mentions légales | {NOM}", f"Mentions légales du site {NOM}, serrurier à Paris.", aside=False)

    simple("/confidentialite/", "Confidentialité", "Politique de confidentialité", "Comment nous traitons vos données personnelles.",
           f'''<h2>Données collectées</h2><p>Quand vous nous contactez (téléphone, WhatsApp, e-mail ou formulaire), nous recueillons uniquement ce qui est nécessaire pour traiter votre demande : nom, téléphone, adresse d'intervention et description du problème.</p>
<h2>Finalité</h2><p>Ces données servent à organiser l'intervention et à établir le devis et la facture. Elles ne sont ni vendues ni cédées.</p>
<h2>Formulaire et WhatsApp</h2><p>Les demandes envoyées par formulaire transitent par Netlify Forms (hébergeur du site). Les messages WhatsApp sont soumis aux conditions de WhatsApp (Meta).</p>
<h2 id="cookies">Cookies et mesure d'audience</h2><p>Avec votre accord uniquement, ce site utilise <strong>Google Tag Manager</strong> et <strong>Google Analytics</strong> (Google Ireland Ltd) pour mesurer sa fréquentation et l'usage des boutons d'appel, de WhatsApp et du formulaire. Sans accord, aucun de ces outils n'est chargé.</p>
<p>Votre choix est conservé 6 mois dans votre navigateur et modifiable à tout moment via le lien « Cookies » en bas de page.</p>
<h2>Durée de conservation</h2><p>Les données de facturation sont conservées 10 ans (obligation légale). Les autres données sont supprimées au plus tard 3 ans après le dernier contact.</p>
<h2>Vos droits</h2><p>Vous disposez d'un droit d'accès, de rectification, d'effacement et d'opposition (RGPD). Écrivez à {CONFIG["email"]}. Vous pouvez aussi saisir la CNIL.</p>''',
           f"Politique de confidentialité | {NOM}", f"Politique de confidentialité du site {NOM}.", aside=False)


def build_conseils():
    body = hero([("Conseils", None)], "Conseils de serrurier <em>pour les Parisiens</em>",
                "Guides pratiques pour réagir en cas d'urgence, sécuriser votre logement et éviter les mauvaises surprises.")
    body += f'<section class="sec"><div class="wrap">{articles_cards(ARTICLES)}</div></section>' + contact_band(source="/conseils/")
    page("/conseils/", f"Conseils serrurerie et sécurité à Paris | {NOM}",
         "Clés perdues, porte blindée en copropriété, arnaques au serrurier, après un cambriolage : nos guides pratiques.",
         body, [ld_business(), ld_crumbs([("Conseils", "/conseils/")])], active="/conseils/")
    for a in ARTICLES:
        path = f"/conseils/{a['slug']}/"
        parts = []
        for kind, val in a["corps"]:
            if kind in ("ul", "ol"):
                parts.append(f"<{kind}>" + "".join(f"<li>{v}</li>" for v in val) + f"</{kind}>")
            else:
                parts.append(f"<{kind}>{val}</{kind}>")
        prose = "".join(parts) + (f'<div class="note-box">{ico("i-phone")}<p><strong>Besoin d\'un serrurier maintenant ?</strong> {E(NOM)} intervient 24h/24 dans tout Paris. '
                                  f'Appelez le <a href="{TEL_HREF}">{TEL}</a> : le prix est annoncé au téléphone. Voir aussi nos <a href="/services/">services</a> et nos <a href="/tarifs/">tarifs</a>.</p></div>')
        rel = articles_cards([o for o in ARTICLES if o is not a][:3])
        body = hero([("Conseils", "/conseils/"), (a["court"], None)], E(a["titre"]), E(a["desc"]),
                    f'<p class="post-by">{E(a["cat"])} · {fr_date(a["date"])} · par l\'équipe {E(NOM)}</p>')
        body += f'<section class="sec"><div class="wrap layout"><article class="prose">{prose}</article>{side_box()}</div></section>'
        body += f'<section class="sec cream"><div class="wrap"><div class="sec-head"><h2>À lire aussi</h2></div>{rel}</div></section>' + contact_band(source=path)
        ld = [ld_business(), ld_crumbs([("Conseils", "/conseils/"), (a["court"], path)]),
              {"@context": "https://schema.org", "@type": "BlogPosting", "headline": a["titre"], "description": a["desc"],
               "datePublished": a["date"], "dateModified": a["date"], "inLanguage": "fr-FR", "mainEntityOfPage": URL + path,
               "author": {"@type": "Organization", "name": NOM, "url": URL + "/"}, "publisher": {"@id": BID}, "image": URL + "/assets/img/og.jpg"}]
        page(path, f'{a["titre"]} | {NOM}', a["desc"], body, ld, active="/conseils/", og_type="article")


def build_misc():
    conv = CONFIG["ads_conv"].get("form")
    body = f'''<section class="phero center-page"><div class="wrap">
  <span class="big-ic">{ico("i-check")}</span>
  <h1>Merci, votre demande est bien partie</h1>
  <p class="lead">Nous vous rappelons très vite. Pour une urgence (porte claquée, effraction), appelez directement : c'est le plus rapide.</p>
  <div class="cta-row center">{btn_call(cls="btn btn-gold btn-lg", track="call_merci")}<a class="btn btn-outline-light btn-lg" href="/">Retour à l'accueil</a></div>
</div></section>'''
    if CONFIG["ads_id"] and conv:
        body += f"<script>gtag('event','conversion',{{'send_to':'{CONFIG['ads_id']}/{conv}','value':1.0,'currency':'EUR'}});</script>"
    page("/merci/", f"Demande envoyée | {NOM}", "Votre demande a bien été envoyée.", body, robots="noindex, nofollow")

    body = f'''<section class="phero center-page"><div class="wrap">
  <p class="err">404</p>
  <h1>Cette page est introuvable</h1>
  <p class="lead">Elle a peut-être été déplacée. Besoin d'un serrurier ? Nous sommes joignables 24h/24.</p>
  <div class="cta-row center">{btn_call(cls="btn btn-gold btn-lg", track="call_404")}<a class="btn btn-outline-light btn-lg" href="/">Retour à l'accueil</a></div>
</div></section>'''
    page("/404.html", f"Page introuvable | {NOM}", "Cette page n'existe pas.", body, robots="noindex, follow")

    groups = [("Pages principales", [("Accueil", "/"), ("Services", "/services/"), ("Arrondissements", "/serrurier-paris/"), ("Tarifs", "/tarifs/"),
                                     ("Assurance", "/assurance/"), ("Avis clients", "/avis/"), ("Questions fréquentes", "/questions-frequentes/"),
                                     ("Conseils", "/conseils/"), ("Contact", "/contact/")]),
              ("Services", [(s["nom"], svc_url(s)) for s in SERVICES]),
              ("Arrondissements", [(f"Serrurier {z['court']}", z["url"]) for z in ARR]),
              ("Conseils", [(a["court"], f"/conseils/{a['slug']}/") for a in ARTICLES])]
    for s in SERVICES:
        groups.append((s["nom"], [(f"{s['court']} {z['court']}", combo_url(s, z)) for z in ARR]))
    prose = "".join(f'<h2>{E(t)}</h2><div class="chips">' + "".join(f'<a class="chip" href="{u}">{E(l)}</a>' for l, u in lst) + "</div>" for t, lst in groups)
    simple("/plan-du-site/", "Plan du site", "Plan du site", f"Toutes les pages du site {NOM}.", prose,
           f"Plan du site | {NOM}", f"Plan du site {NOM} : services, arrondissements, conseils.", aside=False)


# ---------------------------------------------------------------------------
# Fichiers SEO
# ---------------------------------------------------------------------------
def write(name, content):
    with open(os.path.join(ROOT, name), "w", encoding="utf-8") as f:
        f.write(content)


def build_seo():
    def prio(p):
        if p == "/":
            return "1.0"
        if p in ("/serrurier-paris/", "/services/", "/tarifs/", "/contact/"):
            return "0.9"
        if p.startswith("/services/") or (p.startswith("/serrurier-paris-") and p.count("/") == 2):
            return "0.8"
        if p.startswith("/serrurier-paris-"):
            return "0.7"
        return "0.5"
    urls = "".join(f"  <url><loc>{URL}{p}</loc><lastmod>{TODAY}</lastmod><priority>{prio(p)}</priority></url>\n" for p in SITEMAP)
    write("sitemap.xml", '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + urls + "</urlset>\n")
    write("robots.txt", f"User-agent: *\nAllow: /\nDisallow: /_src/\nDisallow: /merci/\n\nSitemap: {URL}/sitemap.xml\n")

    svc = "\n".join(f"- [{s['nom']}]({URL}{svc_url(s)}) : {s['prix']}. {s['resume']}" for s in SERVICES)
    grille = "\n".join(f"- {t[0]} : " + " / ".join(v or "sur devis" for v in t[1:]) for t in TARIFS)
    arr = "\n".join(f"- [Serrurier {z['court']}]({URL}{z['url']}) – {z['cp'][0]}" for z in ARR)
    note = f"- Note Google : {CONFIG['avis_note']}/5 ({CONFIG['avis_nombre']} avis)\n" if CONFIG["avis_note"] else ""
    write("llms.txt", f"""# {NOM}

> Serrurier à Paris (75), dans les 20 arrondissements, 24h/24 et 7j/7. Ouverture de porte claquée dès 110 € TTC, prix annoncé au téléphone avant le déplacement, devis écrit signé avant l'intervention, facture acceptée par les assureurs habitation.

## Informations
- Nom : {NOM} ({CONFIG['raison_sociale']})
- Téléphone : {TEL} ({CONFIG['tel_intl']}), 24h/24, 7j/7
- WhatsApp : {WA}
- E-mail : {CONFIG['email']}
- Site : {URL}/
- Zone : Paris intra-muros uniquement, du 1er au 20e arrondissement
- Délai moyen : environ 30 minutes
- Paiement : carte bancaire, espèces, virement
{note}
## Services
{svc}

## Tarifs TTC (journée 8h–18h / soirée 18h–22h / nuit 22h–8h)
{grille}

## Arrondissements
{arr}

Chaque service a une page par arrondissement : {URL}/<arrondissement>/<service>/ (ex. {URL}{combo_url(SERVICES[0], ARR[14])}).
""")
    write("site.webmanifest", json.dumps({
        "name": f"{NOM} – serrurier 24h/24", "short_name": "Secure Locksmith", "lang": "fr", "start_url": "/",
        "display": "standalone", "background_color": "#151335", "theme_color": "#151335",
        "icons": [{"src": "/assets/img/logo-240.png", "sizes": "240x240", "type": "image/png"},
                  {"src": "/assets/img/icon-512.png", "sizes": "512x512", "type": "image/png"}]}, ensure_ascii=False, indent=2))


def main():
    build_home()
    build_services()
    build_arr_pages()
    build_combo_pages()
    build_static()
    build_conseils()
    build_misc()
    build_seo()
    print(f"{len(SITEMAP)} pages indexables générées.")


if __name__ == "__main__":
    main()
