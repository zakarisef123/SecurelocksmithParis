# -*- coding: utf-8 -*-
"""Générateur du site Secure Locksmith Paris (serrurier Paris 75, 20 arrondissements).

Usage : python3 _src/build.py
Écrit toutes les pages HTML, le sitemap, robots.txt et llms.txt à la racine du dépôt.
Aucune dépendance : Python 3.8+ suffit.
"""
import datetime
import html
import json
import os
import random
import re

from data import ARRONDISSEMENTS, ARTICLES, ASSUREURS, MARQUES, SERVICES, TARIFS

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
    "maps_url": "https://www.google.com/maps/search/?api=1&query=Secure+Lock+Serrurerie+Paris",
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
    # Mentions légales
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


def ico(name, cls="ic"):
    return f'<svg class="{cls}" aria-hidden="true"><use href="#{name}"/></svg>'


# ---------------------------------------------------------------------------
# Silhouette de Paris (fichier SVG partagé par toutes les pages)
# ---------------------------------------------------------------------------
def build_skyline():
    rnd = random.Random(75)
    W, H = 1600, 260
    tower_x = 1150
    parts = ['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1600 260" preserveAspectRatio="xMidYMax slice">',
             '<defs><linearGradient id="t" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#ffe1a0"/>'
             '<stop offset=".55" stop-color="#f7b24f"/><stop offset="1" stop-color="#d9733a"/></linearGradient>'
             '<radialGradient id="g" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="#ffcf7a" stop-opacity=".45"/>'
             '<stop offset="1" stop-color="#ffcf7a" stop-opacity="0"/></radialGradient></defs>']
    # halo et tour Eiffel illuminée
    parts.append(f'<ellipse cx="{tower_x}" cy="120" rx="150" ry="150" fill="url(#g)"/>')
    tx = tower_x
    tower = (f"M{tx-1.5} 8h3v26h-3z"
             f"M{tx-6} 34h12l4 56h-20z"
             f"M{tx-17} 88h34v6h-34z"
             f"M{tx-13} 94h26l9 58h-44z"
             f"M{tx-30} 150h60v7h-60z"
             f"M{tx-27} 157h54l34 103h-24q-30-66-74 0h-24z")
    parts.append(f'<path fill="url(#t)" d="{tower}"/>')
    # treillis suggéré
    parts.append(f'<path stroke="#8a4a2a" stroke-opacity=".35" stroke-width="1" fill="none" d="M{tx-8} 40l16 22M{tx+8} 40l-16 22M{tx-11} 100l22 24M{tx+11} 100l-22 24M{tx-22} 165l44 30M{tx+22} 165l-44 30"/>')
    # dôme (Sacré-Cœur stylisé) sur la gauche
    dx = 330
    parts.append(f'<path fill="#1c1436" d="M{dx-40} 150h80v110h-80zM{dx-30} 150a30 34 0 0 1 60 0zM{dx-2} 108h4v8h-4zM{dx-6} 116a6 8 0 0 1 12 0zM{dx-60} 170a14 16 0 0 1 28 0v90h-28zM{dx+32} 170a14 16 0 0 1 28 0v90h-28z"/>')
    # toits parisiens (deux plans)
    for layer, (col, hmin, hmax, win) in enumerate((("#211741", 70, 120, .16), ("#0e0b22", 45, 95, .28))):
        x = -20
        while x < W:
            w = rnd.randint(58, 120)
            if layer == 1 and tower_x - 70 < x + w and x < tower_x + 70:
                h = rnd.randint(30, 48)  # laisser voir le pied de la tour
            else:
                h = rnd.randint(hmin, hmax)
            y = H - h
            roof = rnd.randint(12, 20)
            parts.append(f'<path fill="{col}" d="M{x} {H}V{y}h{w}V{H}zM{x+6} {y}l{6} -{roof}h{w-24}l{6} {roof}z"/>')
            for _ in range(rnd.randint(1, 3)):
                cx = x + rnd.randint(10, max(11, w - 16))
                parts.append(f'<rect fill="{col}" x="{cx}" y="{y-roof-rnd.randint(4, 12)}" width="6" height="{roof+12}"/>')
            # fenêtres éclairées
            for wy in range(y + 12, H - 10, 18):
                for wx in range(x + 9, x + w - 10, 15):
                    if rnd.random() < win:
                        parts.append(f'<rect fill="#ffc46b" fill-opacity="{rnd.choice([".55", ".75", ".9"])}" x="{wx}" y="{wy}" width="5" height="8" rx="1"/>')
            x += w + rnd.randint(-4, 4)
    parts.append("</svg>")
    os.makedirs(os.path.join(ROOT, "assets", "img"), exist_ok=True)
    with open(os.path.join(ROOT, "assets", "img", "skyline.svg"), "w", encoding="utf-8") as f:
        f.write("".join(parts))


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


def btn_wa(text="Bonjour, j'ai besoin d'un serrurier à Paris.", label="WhatsApp", cls="btn btn-glass", track="wa"):
    return f'<a class="{cls}" href="{E(wa_link(text))}" target="_blank" rel="noopener" data-track="{track}">{ico("i-wa")}<span>{E(label)}</span></a>'


def ticks(items, cls="ticks"):
    return f'<ul class="{cls}">' + "".join(f"<li>{ico('i-check')}{E(i)}</li>" for i in items) + "</ul>"


def crumbs(items):
    parts = ['<a href="/">Accueil</a>']
    for label, url in items:
        parts.append(f'<a href="{url}">{E(label)}</a>' if url else f'<span aria-current="page">{E(label)}</span>')
    return '<nav class="crumbs" aria-label="Fil d\'Ariane">' + '<i aria-hidden="true">/</i>'.join(parts) + "</nav>"


def rating_badge(cls="rating"):
    if not CONFIG["avis_note"]:
        return ""
    stars = "".join(ico("i-star", "st") for _ in range(5))
    return (f'<a class="{cls}" href="{E(MAPS)}" target="_blank" rel="noopener"><span class="stars">{stars}</span>'
            f'<b>{CONFIG["avis_note"]}/5</b><span>· {CONFIG["avis_nombre"]} avis Google</span></a>')


def faq_html(faq):
    return '<div class="faq">' + "".join(
        f'<details{" open" if i == 0 else ""}><summary>{E(q)}<span aria-hidden="true"></span></summary><div><p>{a}</p></div></details>'
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
        "geo": {"@type": "GeoCoordinates", "latitude": 48.8566, "longitude": 2.3522},
        "hasMap": MAPS, "sameAs": [CONFIG["instagram"]],
        "openingHoursSpecification": {"@type": "OpeningHoursSpecification",
                                      "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
                                      "opens": "00:00", "closes": "23:59"},
        "areaServed": [{"@type": "City", "name": "Paris"}],
    }
    if full:
        d["areaServed"] += [{"@type": "AdministrativeArea", "name": z["nom"]} for z in ARR]
        d["hasOfferCatalog"] = {"@type": "OfferCatalog", "name": "Serrurerie à Paris", "itemListElement": [
            {"@type": "Offer", "itemOffered": {"@type": "Service", "name": s["nom"], "url": URL + svc_url(s)},
             **({"priceSpecification": {"@type": "PriceSpecification", "minPrice": s["prix_num"], "priceCurrency": "EUR"}} if s["prix_num"] else {})}
            for s in SERVICES]}
    return d


FORM_N = [0]


def lead_form(source, service=None, titre="Demande de devis gratuit", sous="Réponse rapide, 7j/7.", arr=""):
    FORM_N[0] += 1
    n = FORM_N[0]
    opts = "".join(f'<option{" selected" if service == s["court"] else ""}>{E(s["court"])}</option>' for s in SERVICES)
    arr_opts = "".join(f'<option{" selected" if arr == z["court"] else ""}>{E(z["court"])}</option>' for z in ARR)
    return f'''<form class="lead-form" name="devis" method="POST" action="/merci/" data-netlify="true" netlify-honeypot="champ-robot">
  <input type="hidden" name="form-name" value="devis"><input type="hidden" name="page" value="{E(source)}">
  <p hidden><label>Laisser vide <input name="champ-robot"></label></p>
  <h3>{E(titre)}</h3><p class="form-sub">{E(sous)}</p>
  <div class="grid2">
    <label>Nom<input id="n{n}" name="nom" autocomplete="name" required placeholder="Votre nom"></label>
    <label>Téléphone<input id="t{n}" name="telephone" type="tel" inputmode="tel" autocomplete="tel" required pattern="[0-9+ .()-]{{10,}}" placeholder="06 00 00 00 00"></label>
  </div>
  <div class="grid2">
    <label>Besoin<select name="service">{opts}<option{" selected" if not service else ""}>Autre demande</option></select></label>
    <label>Arrondissement<select name="arrondissement"><option value="">Choisir…</option>{arr_opts}</select></label>
  </div>
  <label>Message<textarea name="message" rows="3" placeholder="Type de porte, situation, horaire souhaité…"></textarea></label>
  <button class="btn btn-sunset btn-block" type="submit">{ico("i-mail")}<span>Envoyer ma demande</span></button>
  <p class="form-legal">Urgence ? Appelez le <a href="{TEL_HREF}">{TEL}</a>. Vos données servent uniquement à vous répondre (<a href="/confidentialite/">confidentialité</a>).</p>
  <div class="form-ok" role="status" hidden>{ico("i-check")}<div><strong>Message bien reçu.</strong> Nous vous rappelons très vite.</div></div>
</form>'''


def contact_band(titre="Un problème de serrure ? Parlons-en.", texte="Un serrurier vous répond tout de suite, le prix est annoncé avant le déplacement.",
                 source="/", service=None, arr=""):
    return f'''<section class="band-contact" id="devis">
  <div class="wrap band-grid">
    <div class="band-text">
      <span class="kicker">Disponible maintenant</span>
      <h2>{E(titre)}</h2>
      <p>{E(texte)}</p>
      <div class="cta-row">{btn_call(cls="btn btn-gold btn-lg", track="call_band")}{btn_wa(cls="btn btn-glass btn-lg", track="wa_band")}</div>
      {ticks(["Prix annoncé au téléphone", "Devis écrit signé avant travaux", "Facture acceptée par les assurances"], "ticks light")}
    </div>
    {lead_form(source, service, arr=arr)}
  </div>
</section>'''


def side_box(titre="Un serrurier vous rappelle", texte="Décrivez votre situation : le tarif vous est donné avant tout déplacement."):
    return f'''<aside class="side-box">
  <div class="side-in">
    <span class="live"><i></i>Serruriers disponibles</span>
    <h3>{E(titre)}</h3>
    <p>{E(texte)}</p>
    {btn_call(cls="btn btn-gold btn-block", track="call_side")}
    {btn_wa(label="Envoyer une photo", cls="btn btn-line btn-block", track="wa_side")}
    {ticks(["Devis gratuit et sans engagement", "Ouverture sans casse dans la plupart des cas", "Paiement CB, espèces, virement"], "ticks small")}
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
  <div class="tarif-card urgent">
    <div class="tc-head"><span class="kicker">Urgences 24h/24</span><h3>Dépannage selon l'heure</h3></div>
    <table class="tarif-table" data-tarifs><thead><tr><th scope="col">Prestation</th>{head}</tr></thead><tbody>{rows}</tbody></table>
    <p class="tarif-now" hidden></p>
  </div>
  <div class="tarif-card">
    <div class="tc-head"><span class="kicker">Sur rendez-vous</span><h3>Travaux et pose</h3></div>
    <ul class="tarif-list">{trv}</ul>
    <p class="tarif-foot">Prix de départ en journée. Devis détaillé offert après visite.</p>
  </div>
</div>
<p class="tarif-note">{ico("i-file")}Tarifs TTC, main d'œuvre comprise. Le prix exact dépend de votre porte et de votre serrure : il vous est annoncé au téléphone puis confirmé par un devis écrit et signé avant l'intervention.</p>'''


def assureurs_block():
    chips = "".join(f"<li>{E(a)}</li>" for a in ASSUREURS)
    return f'''<section class="assur">
  <div class="wrap">
    <div class="assur-head">
      <div><span class="kicker">Assurance habitation</span><h2>Une facture que votre assureur reconnaît</h2></div>
      <p>Nos factures détaillées sont acceptées par les compagnies d'assurance habitation. La prise en charge dépend des garanties de votre contrat (effraction, vol ou perte de clés…). <a href="/assurance/">Comment être remboursé →</a></p>
    </div>
    <ul class="assur-list">{chips}</ul>
    <p class="fine">{E(NOM)} est une entreprise indépendante, sans partenariat avec ces compagnies. Les noms cités appartiennent à leurs propriétaires respectifs.</p>
  </div>
</section>'''


def marques_block():
    cols = "".join(f'<div><h4>{E(cat)}</h4><p>{E(" · ".join(lst))}</p></div>' for cat, lst in MARQUES.items())
    return f'<div class="marques"><h3>Toutes les grandes marques</h3><div class="marques-grid">{cols}</div></div>'


def arr_grid(link=lambda z: z["url"], label=lambda z: f"Serrurier {z['court']}", cls="arr-grid"):
    return f'<div class="{cls}">' + "".join(
        f'<a href="{link(z)}"><b>{z["n"]}<sup>{z["suf"]}</sup></b><span>{E(label(z))}</span></a>' for z in ARR) + "</div>"


def reviews_block(titre="Nos clients en parlent sur Google"):
    note = ""
    if CONFIG["avis_note"]:
        stars = "".join(ico("i-star", "st") for _ in range(5))
        note = f'<div class="big-note"><b>{CONFIG["avis_note"]}</b><div><span class="stars">{stars}</span><span>{CONFIG["avis_nombre"]} avis vérifiés</span></div></div>'
    return f'''<section class="reviews" id="avis">
  <div class="wrap reviews-grid">
    <div>
      <span class="kicker">Avis clients</span>
      <h2>{E(titre)}</h2>
      <p class="lead-dark">Nos avis sont déposés par nos clients sur notre fiche Google : publics, vérifiables, et nous ne pouvons pas les modifier.</p>
      {note}
      <div class="cta-row"><a class="btn btn-sunset" href="{E(MAPS)}" target="_blank" rel="noopener">{ico("i-star")}<span>Lire les avis</span></a>
      <a class="btn btn-line" href="{E(AVIS_URL)}" target="_blank" rel="noopener">{ico("i-award")}<span>Laisser un avis</span></a></div>
    </div>
    <div class="map-card"><iframe title="Zone d'intervention : Paris" loading="lazy" referrerpolicy="no-referrer-when-downgrade" src="https://maps.google.com/maps?q=Paris%2C%20France&amp;z=12&amp;hl=fr&amp;output=embed"></iframe>
      <div class="map-tag">{ico("i-pin")}<span>Paris 1er → 20e</span></div></div>
  </div>
</section>'''


# ---------------------------------------------------------------------------
# Gabarit de page
# ---------------------------------------------------------------------------
NAV = [("Services", "/services/"), ("Arrondissements", "/serrurier-paris/"), ("Tarifs", "/tarifs/"),
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
            f'<img src="/assets/img/logo-112.png" width="56" height="56" alt=""></picture>'
            f'<span class="wordmark"><b>Secure</b> Locksmith<small>Paris</small></span></a>')


def footer():
    svc = "".join(f'<li><a href="{svc_url(s)}">{E(s["court"])}</a></li>' for s in SERVICES)
    arr = "".join(f'<a href="{z["url"]}">{z["n"]}<sup>{z["suf"]}</sup></a>' for z in ARR)
    return f'''<footer class="foot">
  <div class="wrap">
    <div class="foot-grid">
      <div class="foot-brand">
        {logo_html("brand brand-foot")}
        <p>{E(CONFIG["slogan"])} à Paris. Dépannage 24h/24 et 7j/7 dans les 20 arrondissements, prix annoncé avant le déplacement, facture remboursable par votre assurance.</p>
        <a class="foot-tel" href="{TEL_HREF}" data-track="call_footer">{ico("i-phone")}{TEL}</a>
        <p class="foot-links"><a href="mailto:{CONFIG["email"]}">{CONFIG["email"]}</a><br><a href="{CONFIG["instagram"]}" target="_blank" rel="noopener me">{ico("i-insta", "ic sm")} Instagram</a></p>
      </div>
      <div><h4>Services</h4><ul>{svc}</ul></div>
      <div><h4>Le site</h4><ul><li><a href="/tarifs/">Tarifs</a></li><li><a href="/assurance/">Assurance</a></li><li><a href="/avis/">Avis clients</a></li><li><a href="/questions-frequentes/">Questions fréquentes</a></li><li><a href="/conseils/">Conseils</a></li><li><a href="/contact/">Contact</a></li></ul></div>
      <div class="foot-arr"><h4>Serrurier par arrondissement</h4><div class="arr-mini">{arr}</div><a class="more" href="/serrurier-paris/">Tout Paris →</a></div>
    </div>
    <div class="foot-bottom">
      <span>© {TODAY[:4]} {E(NOM)}</span>
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
<meta name="theme-color" content="#151335">
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
<link href="https://fonts.googleapis.com/css2?family=Outfit:wght@500;600;700;800&family=Manrope:wght@400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/assets/css/main.css?v={asset_v("assets/css/main.css")}">
{ld_html}</head>
<body>
{SPRITE}
<header class="top" id="top">
  <div class="wrap top-in">
    {logo_html()}
    <nav class="menu" aria-label="Navigation principale">{nav}</nav>
    <div class="top-cta">
      <a class="top-tel" href="{TEL_HREF}" data-track="call_header"><small>24h/24 · 7j/7</small><b>{TEL}</b></a>
      <a class="btn btn-gold btn-sm call-ic" href="{TEL_HREF}" data-track="call_header_btn" aria-label="Appeler">{ico("i-phone")}<span>Appeler</span></a>
      <button class="burger" type="button" aria-label="Menu" aria-expanded="false" aria-controls="drawer"><i></i><i></i><i></i></button>
    </div>
  </div>
  <nav class="drawer" id="drawer" aria-label="Navigation mobile"><a href="/">Accueil</a>{nav}<a class="btn btn-gold" href="{TEL_HREF}" data-track="call_drawer">{ico("i-phone")}<span>{TEL}</span></a></nav>
</header>
<main>
{body}
</main>
{footer()}
<div class="cookies" id="cookies" role="dialog" aria-label="Cookies" hidden>
  <p><strong>Mesure d'audience</strong> Avec votre accord, nous utilisons Google Analytics et Google Tag Manager pour comprendre comment le site est utilisé (pages vues, clics sur les boutons d'appel). <a href="/confidentialite/#cookies">En savoir plus</a></p>
  <div><button type="button" class="btn btn-line btn-sm" data-cookies="denied">Refuser</button><button type="button" class="btn btn-sunset btn-sm" data-cookies="granted">Accepter</button></div>
</div>
<div class="dock">
  <a class="btn btn-gold" href="{TEL_HREF}" data-track="call_dock">{ico("i-phone")}<span>Appeler un serrurier</span></a>
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


def hero(crumb_items, h1, lead, extra="", kicker=None):
    k = f'<span class="kicker light">{E(kicker)}</span>' if kicker else ""
    return f'''<section class="sky sky-page">
  <div class="starfield" aria-hidden="true"></div>
  <div class="wrap sky-in">
    {crumbs(crumb_items)}
    {k}
    <h1>{h1}</h1>
    <p class="lead">{lead}</p>
    <div class="cta-row">{btn_call(cls="btn btn-gold btn-lg", track="call_hero")}{btn_wa(cls="btn btn-glass btn-lg", track="wa_hero")}</div>
    {extra}
  </div>
  <img class="skyline" src="/assets/img/skyline.svg" alt="" aria-hidden="true">
</section>'''


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


def svc_cards():
    out = []
    for i, s in enumerate(SERVICES):
        prix = f'dès <b>{s["prix_num"]} €</b>' if s["prix_num"] else "<b>devis gratuit</b>"
        out.append(f'''<a class="svc" href="{svc_url(s)}">
  <span class="svc-ic">{ico(s["icon"])}</span>
  <h3>{E(s["court"])}</h3>
  <p>{E(s["resume"])}</p>
  <span class="svc-foot"><span class="svc-prix">{prix}</span><span class="svc-go">{ico("i-arrow")}</span></span>
</a>''')
    return '<div class="svc-grid">' + "".join(out) + "</div>"


def articles_cards(lst):
    return '<div class="posts">' + "".join(f'''<article class="post">
  <div class="post-ic">{ico(a["icon"])}</div>
  <div class="post-meta"><b>{E(a["cat"])}</b><time datetime="{a["date"]}">{fr_date(a["date"])}</time></div>
  <h3><a href="/conseils/{a["slug"]}/">{E(a["court"])}</a></h3>
  <p>{E(a["desc"])}</p>
</article>''' for a in lst) + "</div>"


MOIS = ["janvier", "février", "mars", "avril", "mai", "juin", "juillet", "août", "septembre", "octobre", "novembre", "décembre"]


def fr_date(iso):
    y, m, d = iso.split("-")
    return f"{int(d)} {MOIS[int(m) - 1]} {y}"


def build_home():
    slots = "".join(f'<li data-slot="{k}">{ico(i)}<span>{l}<small>{h}</small></span><b>{p}</b></li>'
                    for (k, i, l, h), p in zip(SLOTS, TARIFS[0][1:]))
    body = f'''<section class="sky sky-home">
  <div class="starfield" aria-hidden="true"></div>
  <div class="wrap hero-grid">
    <div class="hero-text">
      <span class="kicker light">Serrurier Paris 75 · du 1er au 20e</span>
      <h1>Votre serrurier de confiance à Paris, <em>du lever au coucher du soleil… et toute la nuit</em></h1>
      <p class="lead">Porte claquée, serrure bloquée, clé cassée, cambriolage : un serrurier qualifié se déplace dans tout Paris, 24h/24. Le prix vous est annoncé au téléphone, le devis est signé avant de commencer.</p>
      <div class="cta-row">{btn_call(cls="btn btn-gold btn-lg", track="call_hero")}{btn_wa(cls="btn btn-glass btn-lg", track="wa_hero")}</div>
      {rating_badge("rating light")}
    </div>
    <aside class="quote-card" aria-label="Tarif ouverture de porte">
      <span class="live"><i></i>Serruriers en service dans Paris</span>
      <h2>Porte claquée</h2>
      <p>Ouverture sans casse, tarif selon l'heure :</p>
      <ul class="slots" data-slots>{slots}</ul>
      {btn_call("Appeler maintenant", cls="btn btn-gold btn-block", track="call_card")}
      <a class="btn btn-line btn-block" href="{E(wa_link("Bonjour, ma porte est claquée à Paris."))}" target="_blank" rel="noopener" data-track="wa_card">{ico("i-wa")}<span>Photo de la porte sur WhatsApp</span></a>
    </aside>
  </div>
  <img class="skyline" src="/assets/img/skyline.svg" alt="" aria-hidden="true">
</section>
<section class="promise">
  <div class="wrap promise-grid">
    <div>{ico("i-clock")}<b>≈ 30 min</b><span>pour arriver chez vous</span></div>
    <div>{ico("i-euro")}<b>Prix annoncé</b><span>avant le déplacement</span></div>
    <div>{ico("i-file")}<b>Devis signé</b><span>avant toute intervention</span></div>
    <div>{ico("i-shield")}<b>Facture</b><span>reconnue par les assureurs</span></div>
  </div>
</section>
<section class="sec" id="arrondissements">
  <div class="wrap">
    <div class="sec-head center">
      <span class="kicker">100 % Paris intra-muros</span>
      <h2>Un serrurier dans votre arrondissement</h2>
      <p>Nous travaillons uniquement à Paris : nos serruriers connaissent les immeubles, les portes blindées et les codes d'accès de chaque quartier.</p>
    </div>
    {arr_grid(label=lambda z: z["surnom"])}
  </div>
</section>
<section class="sec cream" id="services">
  <div class="wrap">
    <div class="sec-head">
      <span class="kicker">Nos interventions</span>
      <h2>Six services, une même exigence</h2>
      <p>Appartement, maison de ville, commerce ou cave : nous intervenons sur tous les types de portes et de serrures.</p>
    </div>
    {svc_cards()}
    {marques_block()}
  </div>
</section>
<section class="sec night">
  <div class="wrap">
    <div class="sec-head center">
      <span class="kicker">Comment ça se passe</span>
      <h2>Quatre étapes, zéro surprise</h2>
    </div>
    <ol class="timeline">
      <li><b>1</b><h3>Un appel</h3><p>Vous décrivez la porte et la situation, ou envoyez une photo sur WhatsApp.</p></li>
      <li><b>2</b><h3>Un prix</h3><p>Le tarif TTC vous est annoncé tout de suite, avant que le serrurier ne parte.</p></li>
      <li><b>3</b><h3>Une signature</h3><p>Sur place, le prix est confirmé par un devis écrit. Rien ne commence sans votre accord.</p></li>
      <li><b>4</b><h3>Une facture</h3><p>Travail soigné, facture détaillée à transmettre à votre assureur.</p></li>
    </ol>
  </div>
</section>
<section class="sec" id="tarifs">
  <div class="wrap">
    <div class="sec-head">
      <span class="kicker">Tarifs publics</span>
      <h2>Le prix, avant tout le reste</h2>
      <p>Une urgence ne justifie jamais une facture surprise. Voici nos tarifs, par heure d'intervention.</p>
    </div>
    {tarif_table()}
  </div>
</section>
{assureurs_block()}
{reviews_block()}
<section class="sec cream">
  <div class="wrap why">
    <div class="sec-head">
      <span class="kicker">Pourquoi nous</span>
      <h2>Ce qui fait la différence</h2>
      <p>Un artisan parisien joignable en direct, sans plateforme ni centre d'appels.</p>
      <a class="btn btn-sunset" href="/contact/">{ico("i-mail")}<span>Nous écrire</span></a>
    </div>
    <div class="why-list">
      <div>{ico("i-door")}<h3>Ouverture en douceur</h3><p>Radio, crochetage, contournement : on préserve votre serrure chaque fois que c'est possible.</p></div>
      <div>{ico("i-shield")}<h3>Matériel certifié</h3><p>Cylindres et serrures A2P de grandes marques, pièces garanties.</p></div>
      <div>{ico("i-phone")}<h3>Un vrai interlocuteur</h3><p>De jour comme de nuit, c'est un serrurier qui décroche.</p></div>
      <div>{ico("i-home")}<h3>Respect de votre domicile</h3><p>Protection du sol, chantier propre, explications claires.</p></div>
    </div>
  </div>
</section>
<section class="sec" id="faq">
  <div class="wrap faq-wrap">
    <div class="sec-head">
      <span class="kicker">Questions fréquentes</span>
      <h2>Vos questions, nos réponses</h2>
      <p>Une question qui n'est pas ici ? Appelez-nous, on vous répond 24h/24.</p>
      <a class="btn btn-line" href="/questions-frequentes/">Toutes les questions</a>
    </div>
    {faq_html(HOME_FAQ)}
  </div>
</section>
<section class="sec cream">
  <div class="wrap">
    <div class="sec-head">
      <span class="kicker">Conseils de serrurier</span>
      <h2>Guides pratiques pour les Parisiens</h2>
      <p><a class="text-link" href="/conseils/">Tous les conseils →</a></p>
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
  <div><h2>{E(s["nom"])}</h2><p>{E(s["resume"])}</p></div><span class="svc-prix">{E(s["prix"])}</span></a>''' for s in SERVICES)
    body = hero([("Services", None)], "Nos services de serrurerie <em>à Paris</em>",
                "Ouverture de porte, serrure bloquée, clé cassée, changement de serrure, serrure connectée, sécurisation après effraction : tout ce que nous faisons, avec les prix de départ.",
                kicker="24h/24 · 7j/7")
    body += f'<section class="sec"><div class="wrap layout"><div class="svc-rows">{items}{marques_block()}</div>{side_box()}</div></section>'
    body += assureurs_block() + contact_band(source="/services/")
    page("/services/", f"Services de serrurerie à Paris 24h/24 | {NOM}",
         "Tous nos dépannages de serrurerie à Paris : ouverture de porte dès 110 €, serrure bloquée, clé cassée, changement de serrure, serrure connectée, après effraction.",
         body, [ld_business(), ld_crumbs([("Services", "/services/")])], active="/services/")

    for s in SERVICES:
        path = svc_url(s)
        secs = "".join(f"<h2>{E(t)}</h2><p>{c}</p>" for t, c in s["sections"])
        prix = f"dès <strong>{s['prix_num']} € TTC</strong>" if s["prix_num"] else "<strong>sur devis gratuit</strong>"
        others = "".join(f'<a class="chip" href="{svc_url(o)}">{ico(o["icon"])}{E(o["court"])}</a>' for o in SERVICES if o is not s)
        content = f'''<article class="prose">
  <p class="intro">{s["intro"]}</p>
  <div class="note-box">{ico("i-euro")}<p>Tarif : {prix}. Le prix exact vous est annoncé au téléphone et confirmé par un devis écrit avant l'intervention. <a href="/tarifs/">Grille jour, soirée, nuit →</a></p></div>
  {secs}
  <h2>{E(s["court"])} : choisissez votre arrondissement</h2>
  {arr_grid(link=lambda z: combo_url(s, z), label=lambda z: z["surnom"], cls="arr-grid compact")}
  <h2>Questions fréquentes</h2>
  {faq_html(s["faq"])}
  <h2>Nos autres services</h2><div class="chips">{others}</div>
</article>'''
        body = hero([("Services", "/services/"), (s["court"], None)], f'{E(s["nom"])} <em>à Paris</em>',
                    f'{E(s["resume"])} Partout dans Paris, 24h/24, {"dès %d € TTC" % s["prix_num"] if s["prix_num"] else "sur devis gratuit"}.',
                    ticks(["Prix annoncé avant déplacement", "Devis signé avant travaux", "Facture pour l'assurance"], "ticks light inline"), kicker="Service")
        body += f'<section class="sec"><div class="wrap layout">{content}{side_box()}</div></section>'
        body += reviews_block() + contact_band(f"{s['court']} ? On arrive.", "Appelez ou laissez vos coordonnées : nous vous rappelons avec un prix clair.", source=path, service=s["court"])
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
                    kicker=f"{z['cp'][0]} · {z['surnom']}")
        body += f'<section class="sec"><div class="wrap layout">{content}{side_box(f"Serrurier {z["court"]}")}</div></section>'
        body += assureurs_block() + contact_band(f"Bloqué dehors {z['a_court']} ?", "Appelez-nous : prix annoncé au téléphone, serrurier en route aussitôt.", source=path, arr=z["court"])
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
                        kicker=f"{z['cp'][0]} · {z['surnom']}")
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
</div></section>''' + assureurs_block() + contact_band(source="/tarifs/")
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
           after=assureurs_block() + contact_band(source="/assurance/"))

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
                "Nos clients publient leurs avis sur notre fiche Google : ils sont publics et vérifiables.", rating_badge("rating light"))
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
</div></section>''' + reviews_block("Où nous trouver")
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
    body = f'''<section class="sky sky-page center-page"><div class="starfield" aria-hidden="true"></div><div class="wrap sky-in">
  <span class="big-ic">{ico("i-check")}</span>
  <h1>Merci, votre demande est partie</h1>
  <p class="lead">Nous vous rappelons très vite. Pour une urgence (porte claquée, effraction), appelez directement : c'est le plus rapide.</p>
  <div class="cta-row center">{btn_call(cls="btn btn-gold btn-lg", track="call_merci")}<a class="btn btn-glass btn-lg" href="/">Retour à l'accueil</a></div>
</div><img class="skyline" src="/assets/img/skyline.svg" alt="" aria-hidden="true"></section>'''
    if CONFIG["ads_id"] and conv:
        body += f"<script>gtag('event','conversion',{{'send_to':'{CONFIG['ads_id']}/{conv}','value':1.0,'currency':'EUR'}});</script>"
    page("/merci/", f"Demande envoyée | {NOM}", "Votre demande a bien été envoyée.", body, robots="noindex, nofollow")

    body = f'''<section class="sky sky-page center-page"><div class="starfield" aria-hidden="true"></div><div class="wrap sky-in">
  <p class="err">404</p>
  <h1>Cette page s'est perdue dans Paris</h1>
  <p class="lead">Elle a peut-être déménagé. Besoin d'un serrurier ? Nous sommes joignables 24h/24.</p>
  <div class="cta-row center">{btn_call(cls="btn btn-gold btn-lg", track="call_404")}<a class="btn btn-glass btn-lg" href="/">Retour à l'accueil</a></div>
</div><img class="skyline" src="/assets/img/skyline.svg" alt="" aria-hidden="true"></section>'''
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
    build_skyline()
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
