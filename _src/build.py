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

import data as DATA_EN
import data_fr as DATA_FR
import data_es as DATA_ES
from data import (ARRONDISSEMENTS, ARTICLES, ASSUREURS, AVIS, CHARTE, COMPARATIF, INCLUS, INTERVENTIONS, MARQUES, REALISATIONS,
                  SERVICES, TARIFS, URGENCES, VIDEOS)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ---------------------------------------------------------------------------
# Langues : le site est généré trois fois, en anglais (racine), en français (/fr/) et en espagnol (/es/).
# Dans le code, les liens internes s'écrivent toujours avec l'adresse anglaise ;
# en français et en espagnol, page() les remplace par l'adresse traduite (voir FR_PATHS et ES_PATHS plus bas).
# ---------------------------------------------------------------------------
LANG = "en"


def t(en, fr, es):
    """Texte selon la langue en cours de génération (anglais, français, espagnol)."""
    return fr if LANG == "fr" else es if LANG == "es" else en


def sort_services(lst):
    # Emergency services first, then works & installation
    return [s for s in lst if s["cat"] == "urgence"] + [s for s in lst if s["cat"] != "urgence"]


SERVICES = sort_services(SERVICES)
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
    "gtm_id": "GTM-TXSNDJQV",  # compte GTM « Secure Lock » : balises Google Ads appel + formulaire
    "ga_id": "G-GL99Q7CQKN",
    "ads_id": "AW-17925645444",
    # Conversions Google Ads envoyées directement par le site. Laisser vide : les conversions
    # « Clic appel site (GTM) » et « Formulaire de contact site (GTM) » sont envoyées par GTM
    # (événements clic_appel et envoi_formulaire). Remplir ici les compterait deux fois.
    "ads_conv": {"call": "", "wa": "", "form": ""},
    "google_verification": "26oalrhYl1sf4O17TalfT0E-_m-pbH7o4PDT2PE984Q",
    # Widget d'avis Google qui se met à jour tout seul (Trustindex, Elfsight, EmbedSocial…) :
    # collez ici le code d'intégration fourni par le service ; il remplace le carrousel ci-dessous.
    "reviews_widget": "",
    # Entreprise (affichée sur le site et dans les mentions légales)
    "raison_sociale": "Secure Lock Serrurerie",
    "adresse": {"rue": "47 rue Vivienne", "cp": "75002", "ville": "Paris"},
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


NBSP = " "


def fmt_int(n):
    if LANG == "es" and n < 10000:
        return str(n)  # en espagnol, pas d'espace dans les nombres à 4 chiffres (2300 €)
    return f"{n:,}".replace(",", NBSP) if LANG != "en" else f"{n:,}"


def eur(n):
    return f"{fmt_int(n)}{NBSP}€" if LANG != "en" else f"€{n:,}"


def slogan():
    return t(CONFIG["slogan"], "Votre serrurier de confiance", "Su cerrajero de confianza")


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
    "i-sound-off": f'<symbol id="i-sound-off" viewBox="0 0 24 24" {_S}><path d="M11 5 6 9H3v6h3l5 4z"/><path d="m22 9-6 6M16 9l6 6"/></symbol>',
    "i-sound-on": f'<symbol id="i-sound-on" viewBox="0 0 24 24" {_S}><path d="M11 5 6 9H3v6h3l5 4z"/><path d="M15.5 8.5a5 5 0 0 1 0 7M18.5 5.5a9 9 0 0 1 0 13"/></symbol>',
})
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
def thumb(slug, cls="", alt=""):
    """Vignette légère (assets/img/thumbs/, créée par _src/make_thumbs.py), sinon la photo, sinon rien."""
    for folder in ("thumbs", "photos"):
        if os.path.exists(os.path.join(ROOT, "assets", "img", folder, f"{slug}.webp")):
            return f'<img class="{cls}" src="/assets/img/{folder}/{slug}.webp" alt="{E(alt)}" width="480" height="300" loading="lazy" decoding="async">'
    return ""


def video_card(slug, where):
    """Vidéo de chantier d'un service ; where = "side" (colonne, ordinateur) ou "inline" (après l'intro, téléphone)."""
    if slug not in VIDEOS:
        return ""
    f, titre, legende, *_ = VIDEOS[slug]
    return f'''<figure class="vcard vcard-{where}">
  <div class="vbox"><video src="/assets/video/{f}.mp4" poster="/assets/video/{f}.jpg" muted loop playsinline preload="none" data-auto aria-label="{E(titre)}"></video>
  <button type="button" class="v-snd" aria-label="{t("Turn sound on", "Activer le son", "Activar el sonido")}">{ico("i-sound-off")}{ico("i-sound-on")}</button></div>
  <figcaption><b>{E(titre)}</b><small>{E(legende)}</small></figcaption>
</figure>'''


def ld_video(slug, path):
    f, titre, legende, desc, date = VIDEOS[slug]
    return {"@context": "https://schema.org", "@type": "VideoObject", "name": titre, "description": desc,
            "thumbnailUrl": f"{URL}/assets/video/{f}.jpg", "contentUrl": f"{URL}/assets/video/{f}.mp4",
            "uploadDate": date, "embedUrl": URL + path, "publisher": {"@id": BID}}


def ordinal(n):
    return "st" if n % 10 == 1 and n != 11 else "nd" if n % 10 == 2 and n != 12 else "rd" if n % 10 == 3 and n != 13 else "th"


def build_arr(arrs=None, lang="en"):
    out = []
    for n, (surnom, pop, cps, quartiers, reperes, metros, habitat) in (arrs or ARRONDISSEMENTS).items():
        suf_en = ordinal(n)
        suf = {"fr": "er" if n == 1 else "e", "es": ""}.get(lang, suf_en)
        z = {
            "n": n, "suf": suf, "num": f"{n}{suf}", "slug": f"locksmith-paris-{n}{suf_en}",
            "fr_slug": f"serrurier-paris-{n}{'er' if n == 1 else 'e'}", "es_slug": f"cerrajero-paris-{n}",
            "court": f"Paris {n}{suf}", "nom": f"Paris {n}{suf} arrondissement", "surnom": surnom,
            "a": f"in the {n}{suf} arrondissement", "a_court": f"in Paris {n}{suf}",
            "pop": pop, "cp": cps, "quartiers": quartiers, "reperes": reperes, "metros": metros, "habitat": habitat,
        }
        if lang == "fr":
            z.update({"nom": f"Paris {n}{suf} arrondissement", "a": f"dans le {n}{suf} arrondissement", "a_court": f"à Paris {n}{suf}"})
        elif lang == "es":
            z.update({"court": f"París {n}", "nom": f"distrito {n} de París", "a": f"en el distrito {n}", "a_court": f"en París {n}"})
        out.append(z)
    for i, z in enumerate(out):
        z["url"] = f"/{z['slug']}/"
        z["prev"] = out[i - 1] if i > 0 else None
        z["next"] = out[i + 1] if i < len(out) - 1 else None
    return out


ARR = build_arr()


def et(lst):
    return lst[0] if len(lst) == 1 else ", ".join(lst[:-1]) + t(" and ", " et ", " y ") + lst[-1]


def svc_url(s):
    return f"/services/{s['slug']}/"


def combo_url(s, z):
    return f"/{z['slug']}/{s['slug']}/"


def prix_txt(s, strong=False):
    if not s["prix_num"]:
        q = t("free quote", "sur devis gratuit", "presupuesto gratuito")
        return f"<strong>{q}</strong>" if strong else q
    p = eur(s["prix_num"]) + t(" incl. VAT", f"{NBSP}TTC", f"{NBSP}IVA incl.")
    frm = t("from", "dès", "desde")
    return f"{frm} <strong>{p}</strong>" if strong else f"{frm} {p}"


# ---------------------------------------------------------------------------
# Components
# ---------------------------------------------------------------------------
def btn_call(label=None, cls="btn btn-gold", track="call"):
    return f'<a class="{cls}" href="{TEL_HREF}" data-track="{track}">{ico("i-phone")}<span>{E(label or TEL)}</span></a>'


def btn_wa(text=None, label="WhatsApp", cls="btn btn-outline-light", track="wa"):
    return f'<a class="{cls}" href="{E(wa_link(text or WA_MSG))}" target="_blank" rel="noopener" data-track="{track}">{ico("i-wa")}<span>{E(label)}</span></a>'


def ticks(items, cls="ticks"):
    return f'<ul class="{cls}">' + "".join(f"<li>{ico('i-check')}<span>{E(i)}</span></li>" for i in items) + "</ul>"


def crumbs(items):
    parts = [f'<a href="/">{t("Home", "Accueil", "Inicio")}</a>']
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
            f'<span><b>{avis_note()}</b>{stars()}<small>{CONFIG["avis_nombre"]} {t("Google reviews", "avis Google", "opiniones en Google")}</small></span></a>')


def avis_note():
    return CONFIG["avis_note"].replace(".", ",") if LANG != "en" else CONFIG["avis_note"]


def faq_html(faq):
    return '<div class="faq">' + "".join(
        f'<details{" open" if i == 0 else ""}><summary>{E(q)}<i aria-hidden="true"></i></summary><div><p>{a}</p></div></details>'
        for i, (q, a) in enumerate(faq)) + "</div>"


def ld_faq(faq):
    return {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": re.sub("<[^>]+>", "", a)}} for q, a in faq]}


def ld_crumbs(items):
    lst = [{"@type": "ListItem", "position": 1, "name": t("Home", "Accueil", "Inicio"), "item": URL + "/"}]
    for i, (label, url) in enumerate(items, start=2):
        lst.append({"@type": "ListItem", "position": i, "name": label, "item": URL + url})
    return {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": lst}


def ld_business(full=False):
    a = CONFIG["adresse"]
    d = {
        "@context": "https://schema.org", "@type": "Locksmith", "@id": BID, "name": NOM,
        "alternateName": CONFIG["raison_sociale"], "slogan": slogan(),
        "url": URL + "/", "telephone": CONFIG["tel_intl"], "email": CONFIG["email"],
        "image": URL + "/assets/img/og.jpg", "logo": URL + "/assets/img/icon-512.png",
        "priceRange": "€€", "currenciesAccepted": "EUR",
        "paymentAccepted": t("Credit card, Cash, Bank transfer", "Carte bancaire, Espèces, Virement", "Tarjeta bancaria, Efectivo, Transferencia"),
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
        d["hasOfferCatalog"] = {"@type": "OfferCatalog", "name": t("Locksmith services in Paris", "Services de serrurerie à Paris", "Servicios de cerrajería en París"), "itemListElement": [
            {"@type": "Offer", "itemOffered": {"@type": "Service", "name": s["nom"], "url": URL + svc_url(s)},
             **({"priceSpecification": {"@type": "PriceSpecification", "minPrice": s["prix_num"], "priceCurrency": "EUR"}} if s["prix_num"] else {})}
            for s in SERVICES]}
    return d


FORM_N = [0]


def lead_form(source, service=None, titre=None, sous=None, arr="", hid=""):
    FORM_N[0] += 1
    n = FORM_N[0]
    titre = titre or t("Request a free quote", "Demandez un devis gratuit", "Pida un presupuesto gratuito")
    sous = sous or t("We call you back quickly, 7 days a week.", "Nous vous rappelons rapidement, 7 jours sur 7.", "Le devolvemos la llamada rápidamente, los 7 días de la semana.")
    opts = "".join(f'<option{" selected" if service == s["court"] else ""}>{E(s["court"])}</option>' for s in SERVICES)
    arr_opts = "".join(f'<option{" selected" if arr == z["court"] else ""}>{E(z["court"])}</option>' for z in ARR)
    return f'''<form class="lead-form" name="quote" method="POST" action="/thank-you/" data-netlify="true" netlify-honeypot="bot-field">
  <input type="hidden" name="form-name" value="quote"><input type="hidden" name="page" value="{E(source)}">
  <p hidden><label>{t("Leave empty", "Laisser vide", "Dejar vacío")} <input name="bot-field"></label></p>
  <div class="form-head"><h3{f' id="{hid}"' if hid else ""}>{E(titre)}</h3><p>{E(sous)}</p></div>
  <div class="grid2">
    <label for="n{n}">{t("Name", "Nom", "Nombre")}<input id="n{n}" name="name" autocomplete="name" required placeholder="{t("Your name", "Votre nom", "Su nombre")}"></label>
    <label for="t{n}">{t("Phone", "Téléphone", "Teléfono")}<input id="t{n}" name="phone" type="tel" inputmode="tel" autocomplete="tel" required pattern="[0-9+ .()-]{{8,}}" placeholder="{t("+33 6 00 00 00 00", "06 00 00 00 00", "+33 6 00 00 00 00")}"></label>
  </div>
  <div class="grid2">
    <label for="s{n}">{t("What do you need?", "Votre besoin", "¿Qué necesita?")}<select id="s{n}" name="service">{opts}<option{" selected" if not service else ""}>{t("Other request", "Autre demande", "Otra solicitud")}</option></select></label>
    <label for="a{n}">{t("Arrondissement", "Arrondissement", "Distrito")}<select id="a{n}" name="arrondissement"><option value="">{t("Choose…", "Choisir…", "Elegir…")}</option>{arr_opts}</select></label>
  </div>
  <label for="m{n}">{t("Message", "Message", "Mensaje")}<textarea id="m{n}" name="message" rows="3" placeholder="{t("Type of door, situation, preferred time…", "Type de porte, situation, horaire souhaité…", "Tipo de puerta, situación, horario preferido…")}"></textarea></label>
  <button class="btn btn-navy btn-block btn-lg" type="submit">{ico("i-mail")}<span>{t("Send my request", "Envoyer ma demande", "Enviar mi solicitud")}</span></button>
  <p class="form-legal">{ico("i-lock", "ic xs")}{t("Your details are only used to reply to you.", "Vos coordonnées servent uniquement à vous répondre.", "Sus datos solo se usan para responderle.")} <a href="/privacy/">{t("Privacy", "Confidentialité", "Privacidad")}</a></p>
  <div class="form-ok" role="status" hidden>{ico("i-check")}<div>{t("<strong>Request received.</strong> We will call you back very soon. Emergency:", "<strong>Demande bien reçue.</strong> Nous vous rappelons très vite. Urgence :", "<strong>Solicitud recibida.</strong> Le llamamos muy pronto. Urgencias:")} <a href="{TEL_HREF}">{TEL}</a></div></div>
</form>'''


def btn_wa_svc(s, label="WhatsApp"):
    """Petit bouton WhatsApp d'un service, avec un message déjà rempli (remplace les anciens boutons « Quote »)."""
    return btn_wa(t(f"Hello, I need a locksmith in Paris for: {s['nom']}.", f"Bonjour, j'ai besoin d'un serrurier à Paris pour : {s['nom']}.", f"Hola, necesito un cerrajero en París para: {s['nom']}."),
                  label, "btn-q btn-q-wa", "wa_svc")


def btn_quote(service, label=None, cls="btn btn-quote"):
    label = label or t("Get a free quote", "Devis gratuit", "Presupuesto gratuito")
    return f'<button type="button" class="{cls}" data-quote="{E(service)}">{ico("i-mail")}<span>{E(label)}</span></button>'


def quote_modal():
    """Fenêtre de devis, présente une fois par page ; ouverte par n'importe quel bouton [data-quote]."""
    return f'''<dialog class="qm" id="quote-modal" aria-labelledby="qm-title">
  <button type="button" class="qm-close" data-qm-close aria-label="{t("Close", "Fermer", "Cerrar")}">×</button>
  <div class="qm-side"><span class="live"><i></i>{t("Available 24/7", "Disponible 24h/24", "Disponible 24/7")}</span><p class="qm-svc" data-qm-service></p>
    <ul class="ticks small light"><li>{ico("i-check")}<span>{t("Free quote, no obligation", "Devis gratuit, sans engagement", "Presupuesto gratuito y sin compromiso")}</span></li><li>{ico("i-check")}<span>{t("Price confirmed before any work", "Prix confirmé avant toute intervention", "Precio confirmado antes de cualquier trabajo")}</span></li><li>{ico("i-check")}<span>{t("English spoken", "On parle anglais", "Hablamos francés e inglés")}</span></li></ul>
    <a class="qm-call" href="{TEL_HREF}" data-track="call_modal">{ico("i-phone")}<span><small>{t("In a hurry? Call", "Pressé ? Appelez", "¿Tiene prisa? Llame al")}</small><b>{TEL}</b></span></a></div>
  {lead_form("popup", titre=t("Get your free quote", "Votre devis gratuit", "Su presupuesto gratuito"), sous=t("Leave your number: we call you back within minutes, 24/7.", "Laissez votre numéro : nous vous rappelons en quelques minutes, 24h/24.", "Deje su número: le llamamos en pocos minutos, 24/7."), hid="qm-title")}
</dialog>'''


def contact_band(titre=None, texte=None, source="/", service=None, arr=""):
    titre = titre or t("Need a locksmith in Paris?", "Besoin d'un serrurier à Paris ?", "¿Necesita un cerrajero en París?")
    texte = texte or t("Call us: a locksmith answers directly and gives you the price before travelling.",
                       "Appelez-nous : un serrurier vous répond directement et vous annonce le prix avant de se déplacer.", "Llámenos: un cerrajero le atiende directamente y le da el precio antes de desplazarse.")
    return f'''<section class="band" id="quote">
  <div class="wrap band-grid">
    <div class="band-text">
      <span class="eyebrow light">{t("Immediate answer · 24/7", "Réponse immédiate · 24h/24", "Respuesta inmediata · 24/7")}</span>
      <h2>{E(titre)}</h2>
      <p>{E(texte)}</p>
      <a class="band-phone" href="{TEL_HREF}" data-track="call_band"><span class="ring">{ico("i-phone")}</span><span><small>{t("Direct line, no call center", "Ligne directe, sans centre d'appels", "Línea directa, sin centralita")}</small><b>{TEL}</b></span></a>
      {ticks(t(["Price given before we travel", "Written quote signed before any work", "Detailed invoice for your insurer", "Card, cash or bank transfer"],
               ["Prix annoncé avant le déplacement", "Devis écrit signé avant toute intervention", "Facture détaillée pour votre assureur", "Carte, espèces ou virement"], ["Precio anunciado antes del desplazamiento", "Presupuesto escrito y firmado antes de cualquier trabajo", "Factura detallada para su aseguradora", "Tarjeta, efectivo o transferencia"]), "ticks light")}
    </div>
    {lead_form(source, service, arr=arr)}
  </div>
</section>'''


def side_box(titre=None, texte=None, quote=None):
    titre = titre or t("A locksmith available now", "Un serrurier disponible maintenant", "Un cerrajero disponible ahora")
    texte = texte or t("Describe your situation on the phone: you get the price before anyone travels.",
                       "Décrivez votre situation au téléphone : vous connaissez le prix avant tout déplacement.", "Describa su situación por teléfono: conocerá el precio antes de cualquier desplazamiento.")
    return f'''<aside class="side-box">
  <div class="side-head"><span class="live"><i></i>{t("Available 24/7", "Disponible 24h/24", "Disponible 24/7")}</span><h3>{E(titre)}</h3></div>
  <div class="side-body">
    <p>{E(texte)}</p>
    {btn_call(cls="btn btn-gold btn-block btn-lg", track="call_side")}
    {btn_wa(label=t("Send a photo", "Envoyer une photo", "Enviar una foto"), cls="btn btn-outline btn-block", track="wa_side")}
    {ticks(t(["Free quote, no obligation", "Damage-free opening in most cases", "Invoice accepted by insurers"],
             ["Devis gratuit, sans engagement", "Ouverture sans casse dans la plupart des cas", "Facture acceptée par les assureurs"], ["Presupuesto gratuito y sin compromiso", "Apertura sin daños en la mayoría de los casos", "Factura aceptada por las aseguradoras"]), "ticks small")}
    {google_badge("g-badge compact")}
  </div>
</aside>'''


SLOTS = [("jour", "i-sun", "Day", "8am – 6pm"), ("soir", "i-sunset", "Evening", "6pm – 10pm"), ("nuit", "i-moon", "Night", "10pm – 8am")]
# Le week-end et les jours fériés, pas de tarif de jour : tarif du soir de 8h à 22h (le script adapte les horaires affichés)
SLOTS_WE = {"jour": "weekdays only", "soir": "8am – 10pm", "nuit": "10pm – 8am"}
WEEKEND_NOTE = "<b>Weekends and public holidays:</b> on Saturdays, Sundays and public holidays, the minimum rate applied is the Evening (6pm–10pm) rate; if the call-out takes place during the Night slot (10pm–8am), the Night rate applies."


def tarif_table():
    urg = [t for t in TARIFS if all(t[1:])]
    trav = [t for t in TARIFS if not all(t[1:])]

    def prix_html(v):
        pre = next((p for p in ("From ", "À partir de ", "Desde ") if v.startswith(p)), "")
        m = v[len(pre):]
        return f'<span class="pv-from">{t("from", "dès", "desde") if pre else ""}</span><b class="pv-num">{E(m)}</b>'
    tabs = "".join(f'<button type="button" role="tab" data-slot="{k}" aria-selected="{"true" if k == "jour" else "false"}">{ico(i)}<span><b>{l}</b><small data-h="{h}" data-h-we="{SLOTS_WE[k]}">{h}</small></span></button>'
                   for k, i, l, h in SLOTS)
    rows = "".join(f'<li><span class="pl-name">{E(p)}</span><span class="pl-price">'
                   + "".join(f'<span class="pv" data-slot="{k}"{"" if k == "jour" else " hidden"}>{prix_html(v)}</span>' for (k, _, _, _), v in zip(SLOTS, prix))
                   + "</span></li>" for p, *prix in urg)
    trv = "".join(f'<li><span class="pl-name">{E(p)}</span><span class="pl-price"><span class="pv">{prix_html(j)}</span></span></li>' for p, j, *_ in trav)
    return f'''<div class="tarifs">
  <div class="tarif-card main" data-tarifs>
    <div class="tc-head"><div><span class="eyebrow light">{t("24/7 emergency call-outs", "Dépannage d'urgence 24h/24", "Asistencia urgente 24/7")}</span><h3>{t("Prices depend on the time of day", "Les prix dépendent de l'heure", "Los precios dependen de la hora")}</h3></div><span class="tc-ttc">{t("Incl. VAT", "TTC", "IVA incl.")}</span></div>
    <div class="slot-tabs" role="tablist" aria-label="{t("Time of call-out", "Heure d'intervention", "Hora de la intervención")}">{tabs}</div>
    <p class="slot-now" hidden></p>
    <ul class="price-list">{rows}</ul>
    <p class="tarif-we">{ico("i-clock")}<span>{WEEKEND_NOTE}</span></p>
  </div>
  <div class="tarif-card">
    <div class="tc-head light"><div><span class="eyebrow">{t("By appointment", "Sur rendez-vous", "Con cita previa")}</span><h3>{t("Works &amp; installation", "Travaux et installation", "Obras e instalación")}</h3></div></div>
    <ul class="price-list">{trv}</ul>
    <p class="tarif-foot">{t("Daytime starting prices. Free detailed quote after a visit.", "Prix de départ en journée. Devis détaillé gratuit après visite.", "Precios de partida en horario de día. Presupuesto detallado gratuito tras la visita.")}</p>
  </div>
</div>
<p class="tarif-note">{ico("i-file")}<span>{t("Prices include VAT and labor. The exact price depends on your door and lock: it is given on the phone, then confirmed by a written, signed quote before any work, as required by French regulations (decree of 24 January 2017).", "Prix TTC, main-d'œuvre comprise. Le prix exact dépend de votre porte et de votre serrure : il vous est annoncé au téléphone, puis confirmé par un devis écrit et signé avant toute intervention, comme l'exige la réglementation (arrêté du 24 janvier 2017).", "Precios con IVA y mano de obra incluidos. El precio exacto depende de su puerta y de su cerradura: se le anuncia por teléfono y después se confirma con un presupuesto escrito y firmado antes de cualquier trabajo, como exige la normativa francesa (orden del 24 de enero de 2017).")}</span></p>'''


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
    head = (f'''<div class="strip-head"><p><b>{t("Invoices recognized by French home insurers", "Factures reconnues par les assureurs habitation", "Facturas reconocidas por las aseguradoras de hogar francesas")}</b>'''
            f'''<span>{t("Reimbursement depends on your policy", "Le remboursement dépend de votre contrat", "El reembolso depende de su póliza")} · <a href="/insurance/">{t("learn more", "en savoir plus", "saber más")}</a></span></p></div>''') if titre else ""
    return f'''<section class="strip">
  <div class="wrap">{head}</div>
  <div class="ins-marquee" aria-label="{t("Home insurers", "Assureurs habitation", "Aseguradoras de hogar")}">{rows}</div>
  <div class="wrap"><p class="fine">{E(NOM)} {t("is an independent company with no partnership with these insurers; names and logos belong to their respective owners.", "est une entreprise indépendante, sans partenariat avec ces assureurs ; les noms et logos appartiennent à leurs propriétaires respectifs.", "es una empresa independiente, sin acuerdos con estas aseguradoras; los nombres y logotipos pertenecen a sus respectivos propietarios.")}</p></div>
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
    txt = " · ".join(f"<b>{E(c)}</b>{t(':', ' :', ':')} {E(', '.join(l))}" for c, l in cats.items())
    return f'''<div class="brands">
  <div class="ins-marquee brands-marquee" aria-label="{t("Lock and door brands", "Marques de serrures et de portes", "Marcas de cerraduras y de puertas")}">{rows}</div>
  <p class="fine">{txt}.</p>
</div>'''


def arr_grid(link=lambda z: z["url"], label=lambda z: z["surnom"], cls="arr-grid"):
    return f'<div class="{cls}">' + "".join(
        f'<a href="{link(z)}"><span class="thumb"><img src="/assets/img/arr/{z["n"]}.webp" alt="" width="64" height="64" loading="lazy" decoding="async">'
        f'<b>{z["n"]}<span>{z["suf"]}</span></b></span><span class="t"><strong>{z["court"]}</strong><small>{E(label(z))}</small></span>{ico("i-chev", "ic go")}</a>'
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
    auteur = r.get("auteur") or r.get("author") or t("Google user", "Utilisateur Google", "Usuario de Google")
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
    return f'<div class="rv-marquee" aria-label="{t("Google reviews", "Avis Google", "Opiniones en Google")}">{out}</div>'


def reviews_block(titre=None):
    titre = titre or t("What our customers say", "Ce que disent nos clients", "Lo que dicen nuestros clientes")
    eyebrow = t("Customer reviews", "Avis clients", "Opiniones de clientes")
    note = ""
    if CONFIG["avis_note"]:
        note = f'''<div class="score-card">
  <div class="score-top">{G_LOGO}<span>{t("Google reviews", "Avis Google", "Opiniones en Google")}</span></div>
  <div class="score"><b>{avis_note()}</b><span>/5</span></div>
  {stars(5, "st lg")}
  <p>{t(f"Average rating from <b>{CONFIG['avis_nombre']} reviews</b> posted by our customers", f"Note moyenne sur <b>{CONFIG['avis_nombre']} avis</b> publiés par nos clients", f"Valoración media de <b>{CONFIG['avis_nombre']} opiniones</b> publicadas por nuestros clientes")}</p>
  <a class="btn btn-navy btn-block" href="{E(MAPS)}" target="_blank" rel="noopener">{t("Read our Google reviews", "Lire nos avis Google", "Leer nuestras opiniones en Google")}</a>
  <a class="btn btn-outline btn-block" href="{E(AVIS_URL)}" target="_blank" rel="noopener">{t("Leave a review", "Laisser un avis", "Dejar una opinión")}</a>
</div>'''
    if CONFIG["reviews_widget"]:
        return f'''<section class="sec soft" id="reviews">
  <div class="wrap">
    <div class="sec-head"><span class="eyebrow">{eyebrow}</span><h2>{E(titre)}</h2></div>
    <div class="reviews-widget">{CONFIG["reviews_widget"]}</div>
  </div>
</section>'''
    cards = review_cards()
    if cards:
        return f'''<section class="sec soft" id="reviews">
  <div class="wrap">
    <div class="sec-head split"><div><span class="eyebrow">{eyebrow}</span><h2>{E(titre)}</h2></div>
    <div class="rv-summary">{note}</div></div>
  </div>
  {cards}
</section>'''
    side = f'''<div class="review-promise">
  <h3>{t("Public, verifiable reviews", "Des avis publics et vérifiables", "Opiniones públicas y verificables")}</h3>
  <p>{t("We don't publish anonymous testimonials on our website: our reviews are posted by customers directly on our Google Business Profile. They are public and dated, and we can neither edit nor delete them.", "Nous ne publions pas de témoignages anonymes sur notre site : nos avis sont déposés par nos clients directement sur notre fiche Google. Ils sont publics et datés, et nous ne pouvons ni les modifier ni les supprimer.", "No publicamos testimonios anónimos en nuestra web: nuestras opiniones las dejan los clientes directamente en nuestro perfil de Google. Son públicas y tienen fecha, y no podemos modificarlas ni borrarlas.")}</p>
  <ul class="ticks">
    <li>{ico("i-check")}<span>{t("Posted directly by our customers on Google", "Publiés directement par nos clients sur Google", "Publicadas directamente por nuestros clientes en Google")}</span></li>
    <li>{ico("i-check")}<span>{t("Available to read before you even call us", "Consultables avant même de nous appeler", "Puede leerlas incluso antes de llamarnos")}</span></li>
    <li>{ico("i-check")}<span>{t("Price, speed, tidiness: judge for yourself before calling", "Prix, rapidité, propreté : jugez par vous-même avant d'appeler", "Precio, rapidez, limpieza: juzgue usted mismo antes de llamar")}</span></li>
  </ul>
</div>'''
    return f'''<section class="sec soft" id="reviews">
  <div class="wrap">
    <div class="sec-head"><span class="eyebrow">{eyebrow}</span><h2>{E(titre)}</h2></div>
    <div class="reviews">{note}{side}</div>
  </div>
</section>'''


def map_embed():
    from urllib.parse import quote
    q = quote(f"Secure Lock Serrurerie @{CONFIG['lat']},{CONFIG['lng']}")
    return (f'<div class="map"><iframe title="{E(NOM)} {t("on Google Maps", "sur Google Maps", "en Google Maps")}" loading="lazy" referrerpolicy="no-referrer-when-downgrade" '
            f'src="https://maps.google.com/maps?q={q}&amp;z=14&amp;hl={LANG}&amp;output=embed"></iframe>'
            f'<a class="map-link" href="{E(MAPS)}" target="_blank" rel="noopener">{G_LOGO}{t("See our Google profile", "Voir notre fiche Google", "Ver nuestro perfil de Google")}</a></div>')


def comparatif_block():
    rows = "".join(f'<li><div class="cmp-bad"><span class="cmp-ic">×</span><p>{E(b)}</p></div><div class="cmp-good">{ico("i-check")}<p>{E(g)}</p></div></li>'
                   for b, g in COMPARATIF)
    return f'''<div class="cmp">
  <div class="cmp-head"><span>{t("Abusive practices to avoid", "Les pratiques abusives à éviter", "Prácticas abusivas que hay que evitar")}</span><span>{t("At", "Chez", "En")} {E(NOM)}</span></div>
  <ul>{rows}</ul>
</div>'''


def inclus_block(titre=None):
    titre = titre or t("What the price includes", "Ce que comprend le prix", "Lo que incluye el precio")
    lis = "".join(f"<li>{ico('i-check')}<span>{E(i)}</span></li>" for i in INCLUS)
    return f'<div class="inclus"><h3>{E(titre)}</h3><ul>{lis}</ul></div>'


def engagements_short():
    lis = "".join(f'<li>{ico(i)}<span><b>{E(tt.split(". ", 1)[1])}</b></span></li>' for i, tt, _ in CHARTE[:6])
    return f'''<div class="eng-short"><h3>{t("Our commitments, in writing", "Nos engagements, par écrit", "Nuestros compromisos, por escrito")}</h3><ul>{lis}</ul>
  <a class="text-link" href="/our-commitments/">{t("Read our trust charter", "Lire notre charte de confiance", "Leer nuestra carta de confianza")} {ico("i-arrow", "ic sm")}</a></div>'''


def company_card():
    rows = [("i-building", t("Company", "Entreprise", "Empresa"), f"{E(CONFIG['raison_sociale'])}")]
    if CONFIG["siret"]:
        rows.append(("i-file", t("SIRET (company no.)", "SIRET", "SIRET (n.º de empresa)"), siret_fmt()))
    rows += [("i-pin", t("Registered office", "Siège social", "Domicilio social"), E(adresse_txt())), ("i-phone", t("Phone", "Téléphone", "Teléfono"), f'<a href="{TEL_HREF}">{TEL}</a>'),
             ("i-mail", "Email", f'<a href="mailto:{CONFIG["email"]}">{CONFIG["email"]}</a>'),
             ("i-card", t("Payment", "Paiement", "Pago"), t("Card, cash, bank transfer", "Carte, espèces, virement", "Tarjeta, efectivo, transferencia"))]
    if CONFIG["experience"]:
        rows.insert(1, ("i-award", t("Experience", "Expérience", "Experiencia"), E(CONFIG["experience"])))
    if CONFIG["assurance_rc"]:
        rows.append(("i-shield", t("Insurance", "Assurance", "Seguro"), E(CONFIG["assurance_rc"])))
    lis = "".join(f'<li>{ico(i)}<span><small>{l}</small>{v}</span></li>' for i, l, v in rows)
    return f'''<div class="company">
  <div class="company-head"><img src="/assets/img/logo-112.webp" width="56" height="56" alt=""><div><b>{E(NOM)}</b><small>{t("Company details", "Informations sur l'entreprise", "Datos de la empresa")}</small></div></div>
  <ul>{lis}</ul>
  <a class="company-link" href="/legal-notice/">{t("Full legal notice", "Mentions légales complètes", "Aviso legal completo")} {ico("i-arrow", "ic sm")}</a>
</div>'''


# ---------------------------------------------------------------------------
# Page template
# ---------------------------------------------------------------------------
NAV = [("Emergency", "/emergency/"), ("Services", "/services/"), ("Prices", "/prices/"), ("Our commitments", "/our-commitments/"),
       ("Arrondissements", "/locksmith-paris/"), ("Contact", "/contact/")]
SITEMAP = []


IMG_RE = re.compile(r"""(/assets/(?:img|video)/[^"'?\s)]+\.(?:webp|jpe?g|png|svg|gif|mp4))(?![?\w])""")


def bust_images(html_doc):
    # Les images sont gardées 7 jours par les navigateurs : on ajoute ?v=<empreinte du fichier>
    # pour qu'une photo remplacée (même nom de fichier) s'affiche tout de suite.
    def sub(m):
        rel = m.group(1).lstrip("/")
        return f"{m.group(1)}?v={asset_v(rel)}" if os.path.exists(os.path.join(ROOT, rel)) else m.group(1)
    return IMG_RE.sub(sub, html_doc)


def asset_v(rel):
    import hashlib
    try:
        with open(os.path.join(ROOT, rel), "rb") as f:
            return hashlib.md5(f.read()).hexdigest()[:10]
    except FileNotFoundError:
        return TODAY


def logo_html(cls="brand"):
    return (f'<a href="/" class="{cls}" aria-label="{E(NOM)} – {t("home", "accueil", "inicio")}"><picture><source type="image/webp" srcset="/assets/img/logo-112.webp">'
            f'<img src="/assets/img/logo-112.png" width="52" height="52" alt=""></picture>'
            f'<span class="wordmark"><b>Secure Locksmith</b><small>{t("Locksmith · Paris", "Serrurier · Paris", "Cerrajero · París")}</small></span></a>')


def footer():
    svc = "".join(f'<li><a href="{svc_url(s)}">{E(s["nom"])}</a></li>' for s in SERVICES)
    arr = "".join(f'<a href="{z["url"]}" title="{t("Locksmith", "Serrurier", "Cerrajero")} {E(z["court"])}"><img src="/assets/img/arr/{z["n"]}.webp" alt="" width="176" height="176" loading="lazy" decoding="async"><span>{z["n"]}<sup>{z["suf"]}</sup></span></a>' for z in ARR)
    siret = f"<br>SIRET {siret_fmt()}" if CONFIG["siret"] else ""
    info = t([("Our commitments", "/our-commitments/"), ("Prices", "/prices/"), ("Insurance &amp; reimbursement", "/insurance/"), ("Customer reviews", "/reviews/"),
              ("FAQ", "/faq/"), ("Advice", "/advice/"), ("Contact", "/contact/")],
             [("Nos engagements", "/our-commitments/"), ("Tarifs", "/prices/"), ("Assurance et remboursement", "/insurance/"), ("Avis clients", "/reviews/"),
              ("Questions fréquentes", "/faq/"), ("Conseils", "/advice/"), ("Contact", "/contact/")], [("Nuestros compromisos", "/our-commitments/"), ("Precios", "/prices/"), ("Seguro y reembolso", "/insurance/"), ("Opiniones de clientes", "/reviews/"),
              ("Preguntas frecuentes", "/faq/"), ("Consejos", "/advice/"), ("Contacto", "/contact/")])
    info = "".join(f'<li><a href="{u}">{l}</a></li>' for l, u in info)
    return f'''<footer class="foot">
  <div class="wrap">
    <div class="foot-cta">
      <div><b>{t("An emergency? A locksmith answers right away.", "Une urgence ? Un serrurier vous répond tout de suite.", "¿Una urgencia? Un cerrajero le atiende al momento.")}</b><span>{t("24/7 · Sundays and public holidays included", "24h/24, 7j/7 · dimanches et jours fériés compris", "24/7 · domingos y festivos incluidos")}</span></div>
      {btn_call(cls="btn btn-gold btn-lg", track="call_footer_cta")}
    </div>
    <div class="foot-grid">
      <div class="foot-brand">
        {logo_html("brand brand-foot")}
        <p>{t("Locksmith in Paris, across all 20 arrondissements. 24/7 call-outs, price given before we travel, signed quote before any work, invoice for your insurer. English-speaking service.", "Serrurier à Paris, dans les 20 arrondissements. Dépannage 24h/24, prix annoncé avant le déplacement, devis signé avant toute intervention, facture pour votre assurance. Service en français et en anglais.", "Cerrajero en París, en los 20 distritos. Asistencia 24/7, precio anunciado antes del desplazamiento, presupuesto firmado antes de cualquier trabajo y factura para su seguro. Atención en francés y en inglés.")}</p>
        <p class="foot-id">{E(CONFIG["raison_sociale"])}<br>{E(adresse_txt())}{siret}</p>
      </div>
      <div><h4>{t("Services", "Services", "Servicios")}</h4><ul>{svc}</ul></div>
      <div><h4>{t("Information", "Informations", "Información")}</h4><ul>{info}</ul></div>
      <div><h4>{t("Contact", "Contact", "Contacto")}</h4><ul class="foot-contact"><li><a href="{TEL_HREF}" data-track="call_footer">{ico("i-phone", "ic sm")}{TEL}</a></li><li><a href="mailto:{CONFIG["email"]}">{ico("i-mail", "ic sm")}{CONFIG["email"]}</a></li><li><a href="{CONFIG["instagram"]}" target="_blank" rel="noopener me">{ico("i-insta", "ic sm")}Instagram</a></li></ul>
        <h4 class="mt">{t("Arrondissements", "Arrondissements", "Distritos")}</h4><div class="arr-mini">{arr}</div></div>
    </div>
    <div class="foot-bottom">
      <span>© {TODAY[:4]} {E(NOM)} – {E(CONFIG["raison_sociale"])}</span>
      <nav><a href="/legal-notice/">{t("Legal notice", "Mentions légales", "Aviso legal")}</a><a href="/privacy/">{t("Privacy", "Confidentialité", "Privacidad")}</a><a href="/site-map/">{t("Site map", "Plan du site", "Mapa del sitio")}</a><button type="button" class="linklike" data-open-consent>Cookies</button><!--LANGFOOT--></nav>
    </div>
  </div>
</footer>'''


# Adresse affichée pour chaque langue : les pages anglaises sont à la racine, les françaises dans /fr/, les espagnoles dans /es/
def fr_path(path):
    """Adresse française d'une adresse anglaise (None si la page n'existe pas en français)."""
    return FR_PATHS.get(path)


def es_path(path):
    """Adresse espagnole d'une adresse anglaise (None si la page n'existe pas en espagnol)."""
    return ES_PATHS.get(path)


def loc(path):
    return path if LANG == "en" else LANG_PATHS[LANG].get(path) or path


_LINK_RE = re.compile(r'''(["'(])(https://securelockserrurerie\.com)?(/[^"'#?\s<>)]*)''')


def localize(doc):
    """Versions française et espagnole : remplace les liens internes anglais par les adresses traduites."""
    doc = doc.replace(BID, "%%BID%%")
    paths = LANG_PATHS[LANG]

    def sub(m):
        p = paths.get(m.group(3))
        return f"{m.group(1)}{m.group(2) or ''}{p}" if p else m.group(0)
    doc = _LINK_RE.sub(sub, doc)
    return doc.replace("%%BID%%", BID).replace(" €", NBSP + "€")


def lang_switch(path, cls="lang"):
    cur = ' aria-current="true"'
    links = [("en", path, "English"), ("fr", fr_path(path) or "/fr/", "Français"), ("es", es_path(path) or "/es/", "Español")]
    return (f'<nav class="{cls}" aria-label="Language / Langue / Idioma">'
            + "".join(f'<a href="{u}" hreflang="{l}" lang="{l}"{cur if LANG == l else ""} title="{n}">{l.upper()}</a>' for l, u, n in links)
            + "</nav>")


def alt_links(path):
    """Équivalents d'une page anglaise dans chaque langue : [(langue, adresse)], vide si la page n'est pas traduite."""
    fr, es = fr_path(path), es_path(path)
    if not fr:
        return []
    return [("en", path), ("fr", fr)] + ([("es", es)] if es else []) + [("x-default", path)]


def alternates(path):
    return "".join(f'<link rel="alternate" hreflang="{l}" href="{URL}{u}">\n' for l, u in alt_links(path))


def page(path, title, desc, body, ld=(), active=None, robots="index, follow", og_type="website"):
    canonical = URL + path
    nav = "".join(f'<a href="{u}"{" class=\"nav-urg\"" if u == "/emergency/" else ""}{" aria-current=\"page\"" if u == active else ""}>{"<i></i>" if u == "/emergency/" else ""}{E(l)}</a>' for l, u in NAV)
    ld_html = "".join(f'<script type="application/ld+json">{json.dumps(d, ensure_ascii=False)}</script>\n' for d in ld)
    ads = CONFIG["ads_id"]
    conv = json.dumps({k: f"{ads}/{v}" for k, v in CONFIG["ads_conv"].items() if v}) if ads else "{}"
    ads_js = f"gtag('config','{ads}');" if ads else ""
    note = (f'<a class="tb-rating" href="{E(MAPS)}" target="_blank" rel="noopener">{stars(5, "st xs")}<b>{avis_note()}/5</b> {t("on Google", "sur Google", "en Google")} ({CONFIG["avis_nombre"]} {t("reviews", "avis", "opiniones")})</a>'
            if CONFIG["avis_note"] else "")
    doc = f'''<!DOCTYPE html>
<html lang="{LANG}">
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
<!--ALT--><meta name="google-site-verification" content="{CONFIG["google_verification"]}">
<meta name="theme-color" content="#0d1233">
<meta name="geo.region" content="FR-75">
<meta name="geo.placename" content="Paris">
<meta name="geo.position" content="48.8566;2.3522">
<meta property="og:type" content="{og_type}">
<meta property="og:locale" content="{t("en_GB", "fr_FR", "es_ES")}">
{"".join(f'<meta property="og:locale:alternate" content="{c}">' for l, c in OG_LOCALES.items() if l != LANG)}
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
<div class="sky-scroll" aria-hidden="true"><i class="ss-night"></i><i class="ss-dusk"></i><i class="ss-horizon"></i></div>
{SPRITE}
<div class="topbar">
  <div class="wrap tb-in">
    <span class="tb-live"><i></i>{t("Locksmiths available now in Paris", "Serruriers disponibles maintenant à Paris", "Cerrajeros disponibles en París")}</span>
    <span class="tb-items"><span>{ico("i-file", "ic xs")}{t("Signed quote before any work", "Devis signé avant toute intervention", "Presupuesto firmado antes del trabajo")}</span><span>{ico("i-shield", "ic xs")}{t("Invoices accepted by insurers", "Factures acceptées par les assureurs", "Facturas válidas para su seguro")}</span></span>
    {note}
  </div>
</div>
<header class="top" id="top">
  <div class="wrap top-in">
    {logo_html()}
    <nav class="menu" aria-label="{t("Main navigation", "Navigation principale", "Navegación principal")}">{nav}</nav>
    <div class="top-cta">
      <!--LANGSW-->
      <a class="top-tel" href="{TEL_HREF}" data-track="call_header"><span class="ring">{ico("i-phone")}</span><span><small>{t("24/7 emergency", "Urgence 24h/24", "Urgencias 24/7")}</small><b>{TEL}</b></span></a>
      <button class="burger" type="button" aria-label="{t("Menu", "Menu", "Menú")}" aria-expanded="false" aria-controls="drawer"><i></i><i></i><i></i></button>
    </div>
  </div>
  <nav class="drawer" id="drawer" aria-label="{t("Mobile navigation", "Navigation mobile", "Navegación móvil")}"><a href="/">{t("Home", "Accueil", "Inicio")}</a>{nav}<a class="btn btn-gold" href="{TEL_HREF}" data-track="call_drawer">{ico("i-phone")}<span>{t("Call", "Appeler le", "Llamar al")} {TEL}</span></a></nav>
</header>
<main>
{body}
</main>
{footer()}
<div class="cookies" id="cookies" role="dialog" aria-label="Cookies" hidden>
  <p>{t('<strong>Your privacy</strong> With your consent, we measure website traffic (Google Analytics, Google Tag Manager) to improve it. Nothing is loaded without your consent. <a href="/privacy/#cookies">Learn more</a>', '<strong>Votre vie privée</strong> Avec votre accord, nous mesurons la fréquentation du site (Google Analytics, Google Tag Manager) pour l\'améliorer. Rien n\'est chargé sans votre accord. <a href="/privacy/#cookies">En savoir plus</a>', '<strong>Su privacidad</strong> Con su consentimiento, medimos las visitas a la web (Google Analytics, Google Tag Manager) para mejorarla. No se carga nada sin su consentimiento. <a href="/privacy/#cookies">Más información</a>')}</p>
  <div><button type="button" class="btn btn-outline btn-sm" data-cookies="denied">{t("Decline", "Refuser", "Rechazar")}</button><button type="button" class="btn btn-navy btn-sm" data-cookies="granted">{t("Accept", "Accepter", "Aceptar")}</button></div>
</div>
<div class="dock">
  <a class="btn btn-gold" href="{TEL_HREF}" data-track="call_dock">{ico("i-phone")}<span>{t("Call now · 24/7", "Appeler · 24h/24", "Llamar · 24/7")}</span></a>
  <a class="btn btn-wa" href="{WA}" target="_blank" rel="noopener" data-track="wa_dock" aria-label="WhatsApp">{ico("i-wa")}</a>
</div>
<a class="wa-float" href="{WA}" target="_blank" rel="noopener" data-track="wa_float" aria-label="WhatsApp">{ico("i-wa")}<span>WhatsApp</span></a>
<script src="/assets/js/main.js?v={asset_v("assets/js/main.js")}" defer></script>
</body>
</html>
'''
    if LANG != "en":
        doc = localize(doc)
    indexable = robots.startswith("index")
    doc = (doc.replace("<!--ALT-->", alternates(path) if indexable else "")
              .replace("<!--LANGSW-->", lang_switch(path))
              .replace("<!--LANGFOOT-->", lang_switch(path, "lang lang-foot"))
              .replace("%%EN_SITEMAP%%", "/site-map/"))
    real = loc(path)
    out = os.path.join(ROOT, real.lstrip("/"), "index.html") if real.endswith("/") else os.path.join(ROOT, real.lstrip("/"))
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "w", encoding="utf-8") as f:
        f.write(bust_images(doc))
    if indexable and LANG == "en":
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
      <div class="cta-row">{btn_call(cls="btn btn-gold btn-lg", track="call_hero")}{btn_wa(cls="btn btn-wa btn-lg", track="wa_hero")}</div>
      {extra}
    </div>
    {card}
  </div>
</section>'''


def hero_card(prix=None, label=None):
    prix = prix or prix_txt(SERVICES[0])
    label = label or SERVICES[0]["court"]
    return f'''<aside class="hcard">
  <ul>
    <li>{ico("i-euro")}<span><small>{E(label)}</small><b>{E(prix)}</b></span></li>
    <li>{ico("i-clock")}<span><small>{t("Average arrival time in Paris", "Délai moyen d'arrivée dans Paris", "Tiempo medio de llegada en París")}</small><b>{t("≈ 30 minutes", "≈ 30 minutes", "≈ 30 minutos")}</b></span></li>
    <li>{ico("i-file")}<span><small>{t("Quote", "Devis", "Presupuesto")}</small><b>{t("Free, signed before any work", "Gratuit, signé avant toute intervention", "Gratuito, firmado antes de cualquier trabajo")}</b></span></li>
  </ul>
  {google_badge("g-badge compact")}
</aside>'''


# ---------------------------------------------------------------------------
# Home
# ---------------------------------------------------------------------------
HOME_FAQ = [
    ("How much does it cost to open a door in Paris?", "A slammed door is opened for €110 incl. VAT on weekdays (8am–6pm), €160 in the evening and on weekends and €220 at night. The price is given on the phone, then confirmed in a written quote before any work."),
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
    if LANG == "es":
        return f"{int(d)} de {MOIS[int(m) - 1]} de {y}"
    return f"{int(d)} {MOIS[int(m) - 1]} {y}"


def svc_rows(lst, tag="h3", link=svc_url):
    def lead(s):
        t = thumb(s["slug"])
        return f'<span class="svc-thumb">{t}<span class="svc-ic">{ico(s["icon"])}</span></span>' if t else f'<span class="svc-ic">{ico(s["icon"])}</span>'
    return '<div class="svc-rows">' + "".join(f'''<div class="svc-row">{lead(s)}
  <div><{tag}><a class="svc-link" href="{link(s)}">{E(s["nom"])}</a></{tag}><p>{E(s["resume"])}</p></div><span class="svc-prix">{E(s["prix"])}{ico("i-chev", "ic go")}</span>{btn_wa_svc(s)}</div>''' for s in lst) + "</div>"


def urg_prix(prix):
    # Prix des cartes d'urgence : un prix par tranche horaire, le script affiche celui de l'heure actuelle à Paris
    if prix == "quote":
        return t('<small>price</small>free quote', '<small>prix</small>sur devis gratuit', '<small>precio</small>presupuesto gratuito')
    noms = t({"jour": "daytime", "soir": "evening", "nuit": "night"}, {"jour": "journée", "soir": "soirée", "nuit": "nuit"}, {"jour": "día", "soir": "tarde", "nuit": "noche"})
    return "".join(f'<span class="up" data-slot="{k}"{"" if k == "jour" else " hidden"}><small>{noms[k]}</small>{E(v)}</span>'
                   for (k, *_), v in zip(SLOTS, prix))


def urgences_block(light=False):
    keys = ["slammed", "locked", "jammed", "broken", "burglary", "stolen", "smart", "cellar"]
    cards = "".join(f'''<a class="urg" href="{svc_url(SVC_BY_SLUG[slug])}">
  {f'<img class="urg-img" src="/assets/img/urgences/{key}.webp" alt="" width="640" height="360" loading="lazy" decoding="async">' if os.path.exists(os.path.join(ROOT, "assets", "img", "urgences", f"{key}.webp")) else ""}
  <span class="urg-body"><span class="urg-ic">{ico(SVC_BY_SLUG[slug]["icon"])}</span>
  <span class="urg-t"><b>{E(t)}</b><small>{E(conseil)}</small></span>
  <span class="urg-p">{urg_prix(prix)}</span></span>
</a>''' for key, (t, slug, prix, conseil) in zip(keys, URGENCES))
    return f'''<div class="urg-grid{" light" if light else ""}">{cards}</div>'''


def urgence_section():
    return f'''<section class="urgence" id="emergency">
  <div class="wrap">
    <div class="urg-head">
      <div>
        <span class="urg-badge"><i></i>{t("Emergency 24/7", "Urgence 24h/24", "Urgencias 24/7")}</span>
        <h2>{t("An emergency? A locksmith at your door in about 30 minutes", "Une urgence ? Un serrurier devant votre porte en 30 minutes environ", "¿Una urgencia? Un cerrajero en su puerta en unos 30 minutos")}</h2>
        <p>{t("Night, weekend, public holiday: a locksmith answers and sets off right away. The price is given on the phone, before anyone travels.", "Nuit, week-end, jour férié : un serrurier vous répond et part tout de suite. Le prix est annoncé au téléphone, avant tout déplacement.", "Noche, fin de semana, festivo: un cerrajero le atiende y sale de inmediato. El precio se anuncia por teléfono, antes de cualquier desplazamiento.")}</p>
      </div>
      <a class="urg-call" href="{TEL_HREF}" data-track="call_urgence"><span class="ring">{ico("i-phone")}</span><span><small>{t("Direct line", "Ligne directe", "Línea directa")}</small><b>{TEL}</b></span></a>
    </div>
    {urgences_block()}
    <p class="urg-foot">{t('Prices shown for the current time in Paris. Weekends and public holidays: evening rate from 8am to 10pm, night rate from 10pm to 8am. <a href="/prices/">Full price list</a> · <a href="/emergency/">What to do in an emergency</a>', 'Prix affichés pour l\'heure actuelle à Paris. Week-ends et jours fériés : tarif de soirée de 8h à 22h, tarif de nuit de 22h à 8h. <a href="/prices/">Tous nos tarifs</a> · <a href="/emergency/">Que faire en cas d\'urgence</a>', 'Precios mostrados para la hora actual en París. Fines de semana y festivos: tarifa de tarde de 8:00 a 22:00 y tarifa de noche de 22:00 a 8:00. <a href="/prices/">Todos nuestros precios</a> · <a href="/emergency/">Qué hacer en caso de urgencia</a>')}</p>
  </div>
</section>'''


def svc_cards(lst=None):
    out = []
    for s in (lst if lst is not None else SVC_URG):
        prix = (f'<small>{t("from (incl. VAT)", "dès (TTC)", "desde (IVA incl.)")}</small><b>{eur(s["prix_num"])}</b>' if s["prix_num"]
                else t("<small>price</small><b>Free quote</b>", "<small>prix</small><b>Devis gratuit</b>", "<small>precio</small><b>Presupuesto gratuito</b>"))
        ph = photo(s["slug"], s["nom"], "svc-photo", "(max-width: 760px) 100vw, 380px")
        out.append(f'''<article class="svc{" has-photo" if ph else ""}">
  {ph}
  <div class="svc-body">
    <span class="svc-ic">{ico(s["icon"])}</span>
    <h3><a class="svc-link" href="{svc_url(s)}">{E(s["nom"])}</a></h3>
    <p>{E(s["resume"])}</p>
    <div class="svc-foot"><span class="svc-prix">{prix}</span><span class="svc-acts">{btn_wa_svc(s)}<a class="svc-go" href="{svc_url(s)}">{t("Details", "Détails", "Detalles")} {ico("i-arrow", "ic sm")}</a></span></div>
  </div>
</article>''')
    if len(out) % 3:
        out.append(f'''<a class="svc svc-cta" href="{TEL_HREF}" data-track="call_svc_grid">
  <div class="svc-body"><span class="svc-ic">{ico("i-phone")}</span><h3>{t("Another emergency?", "Une autre urgence ?", "¿Otra urgencia?")}</h3>
  <p>{t("Garage door, shop, old lock… Describe the situation and we'll tell you straight away whether we can help, and at what price.", "Porte de garage, commerce, serrure ancienne… Décrivez la situation : nous vous disons tout de suite si nous pouvons intervenir, et à quel prix.", "Puerta de garaje, local comercial, cerradura antigua… Describa la situación y le diremos al momento si podemos intervenir y a qué precio.")}</p>
  <div class="svc-foot"><span class="svc-prix"><small>{t("direct line 24/7", "ligne directe 24h/24", "línea directa 24/7")}</small><b>{TEL}</b></span><span class="svc-go">{t("Call", "Appeler", "Llamar")} {ico("i-arrow", "ic sm")}</span></div></div>
</a>''')
    return '<div class="svc-grid">' + "".join(out) + "</div>"


def svc_tiles():
    """Accueil : grille compacte des 10 services (photo, icône, nom, prix), un clic mène à la page du service."""
    def ph(s):
        img = thumb(s["slug"])
        # sans photo : bande aux couleurs du site avec l'icône en grand (en attendant la vraie photo)
        return f'<span class="stile-ph">{img}</span>' if img else f'<span class="stile-ph empty">{ico(s["icon"])}</span>'
    tiles = "".join(f'''<a class="stile" href="{svc_url(s)}">
  {ph(s)}
  <span class="stile-body"><span class="svc-ic">{ico(s["icon"])}</span>
  <b>{E(s["court"])}</b>
  <span class="stile-p">{(t("from ", "dès ", "desde ") + eur(s["prix_num"])) if s["prix_num"] else t("Free quote", "Devis gratuit", "Presupuesto gratuito")}</span></span>
  {'<span class="stile-tag">24/7</span>' if s["cat"] == "urgence" else ""}
</a>''' for s in SERVICES)
    return f'<div class="stiles">{tiles}</div><p class="stiles-more"><a class="text-link" href="/services/">{t("All services, prices and details", "Tous les services, prix et détails", "Todos los servicios, precios y detalles")} {ico("i-arrow", "ic sm")}</a></p>'


def articles_cards(lst):
    return '<div class="posts">' + "".join(f'''<article class="post">
  <div class="post-top"><span class="post-ic">{ico(a["icon"])}</span><span class="post-cat">{E(a["cat"])}</span></div>
  <h3><a href="/advice/{a["slug"]}/">{E(a["court"])}</a></h3>
  <p>{E(a["desc"])}</p>
  <span class="post-more"><time datetime="{a["date"]}">{fr_date(a["date"])}</time><span>{t("Read", "Lire", "Leer")} {ico("i-arrow", "ic sm")}</span></span>
</article>''' for a in lst) + "</div>"


def engagements():
    items = t([
        ("i-euro", "Price given before we travel", "You describe the situation and we give you the price including VAT. It doesn't change on the way."),
        ("i-file", "Signed quote before any work", "As required by French regulations: nothing starts without your written agreement."),
        ("i-door", "Damage-free opening first", "Shims, picking, cylinder bypass: we preserve your lock whenever possible."),
        ("i-shield", "Leading brands", "Cylinders and locks from recognized manufacturers, A2P-certified models on request."),
        ("i-card", "Transparent payment", "Card, cash or bank transfer, with a detailed invoice every time."),
        ("i-phone", "A locksmith on the line", "No call center: a professional answers, day and night, in English or French."),
    ], [
        ("i-euro", "Prix annoncé avant le déplacement", "Vous décrivez la situation, nous vous annonçons le prix TTC. Il ne change pas en route."),
        ("i-file", "Devis signé avant toute intervention", "Comme l'exige la réglementation : rien ne commence sans votre accord écrit."),
        ("i-door", "Ouverture sans casse en priorité", "Lames, crochetage, contournement du cylindre : nous préservons votre serrure chaque fois que c'est possible."),
        ("i-shield", "Grandes marques", "Cylindres et serrures de fabricants reconnus, modèles certifiés A2P sur demande."),
        ("i-card", "Paiement transparent", "Carte, espèces ou virement, avec une facture détaillée à chaque fois."),
        ("i-phone", "Un serrurier au bout du fil", "Pas de centre d'appels : un professionnel vous répond, de jour comme de nuit, en français ou en anglais."),
    ], [
        ("i-euro", "Precio anunciado antes del desplazamiento", "Usted describe la situación y le damos el precio con IVA. No cambia por el camino."),
        ("i-file", "Presupuesto firmado antes de cualquier trabajo", "Como exige la normativa francesa: nada empieza sin su acuerdo por escrito."),
        ("i-door", "Primero, apertura sin daños", "Láminas, ganzúas, apertura del bombín sin romperlo: conservamos su cerradura siempre que es posible."),
        ("i-shield", "Grandes marcas", "Bombines y cerraduras de fabricantes reconocidos, modelos con certificación A2P a petición."),
        ("i-card", "Pago transparente", "Tarjeta, efectivo o transferencia, con una factura detallada cada vez."),
        ("i-phone", "Un cerrajero al teléfono", "Sin centralita: le atiende un profesional, de día y de noche, en francés o en inglés."),
    ])
    return '<div class="engage">' + "".join(f'<div>{ico(i)}<h3>{E(tt)}</h3><p>{E(d)}</p></div>' for i, tt, d in items) + "</div>"


def build_home():
    visual = photo("home", t(f"{NOM}, locksmith in Paris", f"{NOM}, serrurier à Paris", f"{NOM}, cerrajero en París"), "hero-photo", "(max-width: 1100px) 100vw, 560px", eager=True)
    if not visual and os.path.exists(os.path.join(ROOT, "assets", "img", "photos", "hero-round.webp")):
        visual = f'<picture class="emblem photo-round"><img src="/assets/img/photos/hero-round.webp" width="440" height="440" alt="{t("Secure Lock locksmith in his work vest, seen from behind", "Serrurier Secure Lock dans son gilet de travail, vu de dos", "Cerrajero de Secure Lock con su chaleco de trabajo, visto de espaldas")}" fetchpriority="high"></picture>'
    if not visual:
        visual = f'<picture class="emblem"><source type="image/webp" srcset="/assets/img/logo-512.webp"><img src="/assets/img/icon-512.png" width="440" height="440" alt="{t("Secure Locksmith Paris logo", "Logo Secure Locksmith Paris", "Logotipo de Secure Locksmith Paris")}" fetchpriority="high"></picture>'
    equipe = photo("team", t("Locksmith advising customers at their front door", "Serrurier conseillant des clients devant leur porte d'entrée", "Cerrajero asesorando a unos clientes ante la puerta de su casa"), "about-photo")
    about_visual = equipe or company_card()
    body = f'''<section class="hero has-bg">
  {bg_img("tour-eiffel")}
  <div class="wrap hero-grid">
    <div class="hero-text">
      <span class="eyebrow light">{t("Locksmith in Paris · all 20 arrondissements", "Serrurier à Paris · les 20 arrondissements", "Cerrajero en París · los 20 distritos")}</span>
      <h1>{t("English Speaking Locksmith in Paris,", "Serrurier à Paris,", "Cerrajero en París,")}<br><span class="gold">{t("24/7", "24h/24", "24/7")}</span></h1>
      <p class="lead">{t("Locked out, jammed lock, broken key, break-in: a qualified, English-speaking locksmith comes to you in about 30 minutes on average. The price is given on the phone and the quote is signed before any work.", "Porte claquée, serrure bloquée, clé cassée, effraction : un serrurier qualifié arrive chez vous en 30 minutes environ en moyenne. Le prix est annoncé au téléphone et le devis est signé avant toute intervention.", "Puerta cerrada de golpe, cerradura bloqueada, llave rota, robo: un cerrajero cualificado llega a su casa en unos 30 minutos de media. El precio se anuncia por teléfono y el presupuesto se firma antes de cualquier trabajo.")}</p>
      <div class="cta-row">{btn_call(cls="btn btn-gold btn-xl", track="call_hero")}{btn_wa(cls="btn btn-wa btn-xl", track="wa_hero")}</div>
      <div class="hero-proof">
        {google_badge("g-badge dark")}
        <ul class="proof-list"><li>{ico("i-check")}{t("Door opening from €110", "Ouverture de porte dès 110 €", "Apertura de puerta desde 110 €")}</li><li>{ico("i-check")}{t("No hidden fees", "Aucun frais caché", "Sin gastos ocultos")}</li><li>{ico("i-check")}{t("Invoice for your insurer", "Facture pour votre assurance", "Factura para su seguro")}</li></ul>
      </div>
    </div>
    <div class="hero-visual">
      {visual}
      <div class="float f1"><span class="live"><i></i>{t("Available now", "Disponible maintenant", "Disponible ahora")}</span><b>{t("Arrival ≈ 30 min", "Arrivée ≈ 30 min", "Llegada ≈ 30 min")}</b></div>
      <div class="float f2">{ico("i-shield")}<span><b>{t("Signed quote", "Devis signé", "Presupuesto firmado")}</b><small>{t("before every job", "avant chaque intervention", "antes de cada intervención")}</small></span></div>
    </div>
  </div>
</section>
{urgence_section()}
{assureurs_strip()}
<section class="sec" id="services">
  <div class="wrap">
    <div class="sec-head split">
      <div><span class="eyebrow">{t("Our services", "Nos services", "Nuestros servicios")}</span><h2>{t("Every locksmith service, everywhere in Paris", "Tous les services de serrurerie, partout dans Paris", "Todos los servicios de cerrajería, en todo París")}</h2></div>
      <p>{t("Apartment, townhouse, shop, cellar or storage room: we work on every type of door and lock, from old Parisian landing doors to multi-point armored doors.", "Appartement, maison, commerce, cave ou local : nous intervenons sur tous les types de portes et de serrures, des vieilles portes palières parisiennes aux portes blindées multipoints.", "Piso, casa, local comercial, trastero o almacén: trabajamos en todo tipo de puertas y cerraduras, desde las antiguas puertas de rellano parisinas hasta las puertas blindadas multipunto.")}</p>
    </div>
    {svc_tiles()}
  </div>
</section>
<section class="sec soft">
  <div class="wrap about">
    <div class="about-text">
      <span class="eyebrow">{t("Why trust us", "Pourquoi nous faire confiance", "Por qué confiar en nosotros")}</span>
      <h2>{t("An identified Paris locksmith who commits in writing", "Un serrurier parisien identifié, qui s'engage par écrit", "Un cerrajero parisino identificado, que se compromete por escrito")}</h2>
      <p class="lead-dark">{t(f"Emergency locksmiths have a bad reputation, often for good reason. At {E(NOM)}, we have chosen the opposite approach: an identified company, published prices and commitments you can check.", f"Le dépannage en serrurerie a mauvaise réputation, souvent à juste titre. Chez {E(NOM)}, nous avons choisi l'inverse : une entreprise identifiée, des tarifs publiés et des engagements que vous pouvez vérifier.", f"Los cerrajeros de urgencia tienen mala fama, a menudo con razón. En {E(NOM)} hemos elegido lo contrario: una empresa identificada, precios publicados y compromisos que usted puede comprobar.")}</p>
      <p class="about-p">{t('When you are stuck outside your door, often late at night, you have neither the time nor the energy to compare offers. That is exactly when nasty surprises happen, especially if you don\'t speak French. Our answer is simple: you know the price before the locksmith sets off, you sign a quote before he starts, and you receive a detailed invoice at the end. No "extra charges" discovered on site, no lock replaced for no reason.', "Quand vous êtes bloqué devant votre porte, souvent tard le soir, vous n'avez ni le temps ni l'énergie de comparer les offres. C'est précisément là que surviennent les mauvaises surprises. Notre réponse est simple : vous connaissez le prix avant le départ du serrurier, vous signez un devis avant qu'il commence, et vous recevez une facture détaillée à la fin. Pas de « frais supplémentaires » découverts sur place, pas de serrure changée sans raison.", "Cuando se queda en la calle delante de su puerta, a menudo tarde por la noche, no tiene ni tiempo ni ganas de comparar ofertas. Es justo entonces cuando llegan las sorpresas desagradables, sobre todo si no habla francés. Nuestra respuesta es sencilla: conoce el precio antes de que salga el cerrajero, firma un presupuesto antes de que empiece y recibe una factura detallada al final. Nada de «gastos adicionales» descubiertos en el sitio, ni cerraduras cambiadas sin motivo.")}</p>
      <p class="about-p">{t("We work only in Paris. That focus lets us arrive quickly and know Parisian doors well: landing doors in Haussmann buildings, multi-point armored doors, old locks and modern badge-access residences.", "Nous travaillons uniquement à Paris. Cela nous permet d'arriver vite et de bien connaître les portes parisiennes : portes palières des immeubles haussmanniens, portes blindées multipoints, serrures anciennes et résidences modernes à badge.", "Solo trabajamos en París. Eso nos permite llegar rápido y conocer bien las puertas parisinas: puertas de rellano de los edificios haussmannianos, puertas blindadas multipunto, cerraduras antiguas y residencias modernas con acceso por tarjeta.")}</p>
      {engagements()}
      <a class="btn btn-navy" style="margin-top:34px" href="/our-commitments/">{ico("i-file")}<span>{t("Read our trust charter", "Lire notre charte de confiance", "Leer nuestra carta de confianza")}</span></a>
    </div>
    <div class="about-side">{about_visual}{company_card() if equipe else ""}</div>
  </div>
</section>
<section class="sec">
  <div class="wrap">
    <div class="sec-head split">
      <div><span class="eyebrow">{t("Locksmith scams", "Arnaques au serrurier", "Estafas de cerrajeros")}</span><h2>{t("What you will never see from us", "Ce que vous ne verrez jamais chez nous", "Lo que nunca verá con nosotros")}</h2></div>
      <p>{t("Emergency locksmith services are among the sectors generating the most complaints to the French consumer protection authority (DGCCRF). Here, point by point, are the most common abusive practices and how we work instead.", "Le dépannage en serrurerie fait partie des secteurs qui génèrent le plus de plaintes auprès de la DGCCRF. Voici, point par point, les pratiques abusives les plus courantes et notre façon de travailler à la place.", "La cerrajería de urgencia es uno de los sectores que más reclamaciones genera ante la autoridad francesa de protección del consumidor (DGCCRF). Estas son, punto por punto, las prácticas abusivas más habituales y cómo trabajamos nosotros en su lugar.")}</p>
    </div>
    {comparatif_block()}
    <p class="cmp-foot">{t('Unsure about a locksmith? Read our guide <a href="/advice/spot-an-honest-locksmith/">How to spot an honest locksmith</a>.', 'Un doute sur un serrurier ? Lisez notre guide <a href="/advice/spot-an-honest-locksmith/">Comment reconnaître un serrurier honnête</a>.', '¿Dudas sobre un cerrajero? Lea nuestra guía <a href="/advice/spot-an-honest-locksmith/">Cómo reconocer a un cerrajero honrado</a>.')}</p>
  </div>
</section>
<section class="sec" id="prices">
  <div class="wrap">
    <div class="sec-head split">
      <div><span class="eyebrow">{t("Prices", "Tarifs", "Precios")}</span><h2>{t("Clear prices, published before any work", "Des prix clairs, publiés avant toute intervention", "Precios claros, publicados antes de cualquier trabajo")}</h2></div>
      <p>{t("Our prices depend on the time of the call-out. They are shown here, given on the phone and confirmed in writing: you know what you will pay before the locksmith sets off.", "Nos prix dépendent de l'heure d'intervention. Ils sont affichés ici, annoncés au téléphone et confirmés par écrit : vous savez ce que vous allez payer avant le départ du serrurier.", "Nuestros precios dependen de la hora de la intervención. Se muestran aquí, se anuncian por teléfono y se confirman por escrito: sabe lo que va a pagar antes de que salga el cerrajero.")}</p>
    </div>
    {tarif_table()}
  </div>
</section>
<section class="sec navy">
  <div class="wrap">
    <div class="sec-head center"><span class="eyebrow light">{t("How it works", "Comment ça se passe", "Cómo funciona")}</span><h2>{t("What happens when you call us", "Ce qui se passe quand vous nous appelez", "Qué pasa cuando nos llama")}</h2></div>
    <ol class="steps">
      {t('''<li><b>1</b><h3>You call</h3><p>You describe the door and the situation, or send a photo on WhatsApp.</p></li>
      <li><b>2</b><h3>Price given</h3><p>You get the price including VAT straight away, before the locksmith sets off.</p></li>
      <li><b>3</b><h3>Signed quote</h3><p>On site, the price is confirmed in writing. Nothing starts without your signature.</p></li>
      <li><b>4</b><h3>Work &amp; invoice</h3><p>Careful work and a detailed invoice to send to your insurer.</p></li>''',
      '''<li><b>1</b><h3>Vous appelez</h3><p>Vous décrivez la porte et la situation, ou vous envoyez une photo sur WhatsApp.</p></li>
      <li><b>2</b><h3>Prix annoncé</h3><p>Vous connaissez tout de suite le prix TTC, avant le départ du serrurier.</p></li>
      <li><b>3</b><h3>Devis signé</h3><p>Sur place, le prix est confirmé par écrit. Rien ne commence sans votre signature.</p></li>
      <li><b>4</b><h3>Intervention et facture</h3><p>Un travail soigné et une facture détaillée à transmettre à votre assureur.</p></li>''', '''<li><b>1</b><h3>Usted llama</h3><p>Describe la puerta y la situación, o nos envía una foto por WhatsApp.</p></li>
      <li><b>2</b><h3>Precio anunciado</h3><p>Conoce al momento el precio con IVA, antes de que salga el cerrajero.</p></li>
      <li><b>3</b><h3>Presupuesto firmado</h3><p>En el sitio, el precio se confirma por escrito. Nada empieza sin su firma.</p></li>
      <li><b>4</b><h3>Trabajo y factura</h3><p>Un trabajo cuidadoso y una factura detallada para enviar a su aseguradora.</p></li>''')}
    </ol>
    <div class="steps-cta">{btn_call(t("Call a locksmith", "Appeler un serrurier", "Llamar a un cerrajero"), cls="btn btn-gold btn-lg", track="call_steps")}<span>{t("or send a photo on", "ou envoyez une photo sur", "o envíe una foto por")} <a href="{E(wa_link(WA_MSG))}" target="_blank" rel="noopener" data-track="wa_steps">WhatsApp</a></span></div>
  </div>
</section>
{reviews_block()}
<section class="sec">
  <div class="wrap">
    <div class="sec-head split">
      <div><span class="eyebrow">{t("Brands", "Marques", "Marcas")}</span><h2>{t("We work on all the major brands", "Nous intervenons sur toutes les grandes marques", "Trabajamos con todas las grandes marcas")}</h2></div>
      <p>{t("Locks, cylinders, armored doors and smart locks: our locksmiths know the main manufacturers and carry common parts in their van.", "Serrures, cylindres, portes blindées et serrures connectées : nos serruriers connaissent les principaux fabricants et ont les pièces courantes dans leur véhicule.", "Cerraduras, bombines, puertas blindadas y cerraduras inteligentes: nuestros cerrajeros conocen a los principales fabricantes y llevan las piezas más habituales en la furgoneta.")}</p>
    </div>
    {marques_block()}
  </div>
</section>
<section class="sec soft" id="arrondissements">
  <div class="wrap">
    <div class="sec-head split">
      <div><span class="eyebrow">{t("Service area", "Zone d'intervention", "Zona de servicio")}</span><h2>{t("A locksmith in every Paris arrondissement", "Un serrurier dans chaque arrondissement de Paris", "Un cerrajero en cada distrito de París")}</h2></div>
      <p>{t("We work exclusively within Paris. Choose your arrondissement to see the neighborhoods we cover and our services near you.", "Nous intervenons exclusivement dans Paris. Choisissez votre arrondissement pour voir les quartiers couverts et nos services près de chez vous.", "Trabajamos exclusivamente dentro de París. Elija su distrito para ver los barrios que cubrimos y nuestros servicios cerca de usted.")}</p>
    </div>
    {arr_grid()}
  </div>
</section>
<section class="sec" id="faq">
  <div class="wrap faq-wrap">
    <div class="sec-head">
      <span class="eyebrow">{t("FAQ", "FAQ", "Preguntas frecuentes")}</span>
      <h2>{t("Your questions, our answers", "Vos questions, nos réponses", "Sus preguntas, nuestras respuestas")}</h2>
      <p>{t("Another question? Call us, we answer 24/7.", "Une autre question ? Appelez-nous, nous répondons 24h/24.", "¿Otra pregunta? Llámenos, respondemos 24/7.")}</p>
      <a class="btn btn-outline" href="/faq/">{t("All questions", "Toutes les questions", "Todas las preguntas")}</a>
    </div>
    {faq_html(HOME_FAQ)}
  </div>
</section>
<section class="sec soft">
  <div class="wrap">
    <div class="sec-head split">
      <div><span class="eyebrow">{t("Advice", "Conseils", "Consejos")}</span><h2>{t("Practical guides from our locksmiths", "Les guides pratiques de nos serruriers", "Guías prácticas de nuestros cerrajeros")}</h2></div>
      <p><a class="text-link" href="/advice/">{t("See all our advice", "Voir tous nos conseils", "Ver todos nuestros consejos")} {ico("i-arrow", "ic sm")}</a></p>
    </div>
    {articles_cards(ARTICLES[:4])}
  </div>
</section>
{contact_band()}'''
    ld = [ld_business(full=True), ld_faq(HOME_FAQ),
          {"@context": "https://schema.org", "@type": "WebSite", "name": NOM, "url": URL + "/", "inLanguage": LANG, "publisher": {"@id": BID}}]
    page("/", t("Locksmith Paris 24/7 | Emergency & Lockout Service – Secure Locksmith", "Serrurier Paris 24h/24 | Dépannage & Urgence – Secure Locksmith",
                "Cerrajero París 24/7 | Urgencias y Aperturas – Secure Locksmith"),
         t(f"English-speaking locksmith in Paris, 24/7 across all 20 arrondissements. Door opening from €110 incl. VAT, price given before we travel, signed quote, invoice for your insurer. ☎ {TEL}",
           f"Serrurier à Paris 24h/24 dans les 20 arrondissements. Ouverture de porte dès 110 € TTC, prix annoncé avant le déplacement, devis signé, facture pour votre assurance. ☎ {TEL}", f"Cerrajero en París 24/7 en los 20 distritos. Apertura de puerta desde 110 € IVA incl., precio anunciado antes del desplazamiento, presupuesto firmado, factura para su seguro. ☎ {TEL}"),
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
    <img src="{a}" alt="{t("After", "Après", "Después")} : {E(r.get("caption", s["nom"]))}" loading="lazy" decoding="async">
    <div class="ba-before"><img src="{b}" alt="{t("Before", "Avant", "Antes")}" loading="lazy" decoding="async"></div>
    <span class="ba-tag l">{t("Before", "Avant", "Antes")}</span><span class="ba-tag r">{t("After", "Après", "Después")}</span>
    <span class="ba-handle" aria-hidden="true"></span>
    <input class="ba-range" type="range" min="0" max="100" value="50" aria-label="{t("Compare before and after", "Comparer avant et après", "Comparar antes y después")}">
  </div>
  <figcaption>{E(r.get("caption", ""))}</figcaption>
</figure>''')
    if not items:
        return ""
    return (t("<h2>Before &amp; after: our recent work</h2><p>Slide to compare. These are real jobs carried out by our team in Paris.</p>",
              "<h2>Avant / après : nos dernières réalisations</h2><p>Faites glisser pour comparer. Ce sont de vrais chantiers réalisés par notre équipe à Paris.</p>", "<h2>Antes y después: nuestros últimos trabajos</h2><p>Deslice para comparar. Son trabajos reales realizados por nuestro equipo en París.</p>")
            + f'<div class="ba-grid">{"".join(items)}</div>')


def build_services():
    items = (f'<h2 class="group-title">{ico("i-clock")}{t("Emergency call-outs <small>24/7</small>", "Dépannage d\'urgence <small>24h/24</small>", "Asistencia urgente <small>24/7</small>")}</h2>' + svc_rows(SVC_URG, "h3")
             + f'<h2 class="group-title">{ico("i-shield")}{t("Works, armored doors &amp; installation <small>by appointment</small>", "Travaux, portes blindées et installation <small>sur rendez-vous</small>", "Obras, puertas blindadas e instalación <small>con cita previa</small>")}</h2>' + svc_rows(SVC_TRAV, "h3"))
    body = hero([(t("Services", "Services", "Servicios"), None)], t("Our locksmith services in Paris", "Nos services de serrurerie à Paris", "Nuestros servicios de cerrajería en París"),
                t("24/7 emergency call-outs (lockouts, jammed locks, broken keys, break-ins) and works by appointment (door armoring, armored doors, cellar doors, smart locks, mailbox locks), with their starting prices.",
                  "Dépannage d'urgence 24h/24 (portes claquées, serrures bloquées, clés cassées, effractions) et travaux sur rendez-vous (blindage, portes blindées, portes de cave, serrures connectées, boîtes aux lettres), avec leurs prix de départ.", "Asistencia urgente 24/7 (puertas cerradas de golpe, cerraduras bloqueadas, llaves rotas, robos) y trabajos con cita previa (blindaje, puertas blindadas, puertas de trastero, cerraduras inteligentes, buzones), con sus precios de partida."),
                kicker=t("24/7", "24h/24", "24/7"))
    body += f'<section class="sec"><div class="wrap layout"><div>{items}</div>{side_box()}</div></section>'
    body += (assureurs_strip() + f'<section class="sec"><div class="wrap"><div class="sec-head"><span class="eyebrow">{t("Brands", "Marques", "Marcas")}</span><h2>{t("All the major brands", "Toutes les grandes marques", "Todas las grandes marcas")}</h2></div>{marques_block()}</div></section>'
             + contact_band(source="/services/"))
    page("/services/", t(f"Locksmith services in Paris 24/7 | {NOM}", f"Services de serrurerie à Paris 24h/24 | {NOM}", f"Servicios de cerrajería en París 24/7 | {NOM}"),
         t("All our locksmith services in Paris: door opening from €110, jammed locks, broken keys, lock replacement, smart locks, break-in repair, armored doors.",
           "Tous nos services de serrurier à Paris : ouverture de porte dès 110 €, serrure bloquée, clé cassée, changement de serrure, serrure connectée, sécurisation après effraction, portes blindées.", "Todos nuestros servicios de cerrajero en París: apertura de puerta desde 110 €, cerradura bloqueada, llave rota, cambio de cerradura, cerradura inteligente, seguridad tras un robo, puertas blindadas."),
         body, [ld_business(), ld_crumbs([(t("Services", "Services", "Servicios"), "/services/")])], active="/services/")

    for s in SERVICES:
        path = svc_url(s)
        secs = "".join(f"<h2>{E(h)}</h2><p>{c}</p>" for h, c in s["sections"])
        others = "".join(f'<a class="chip chip-ph" href="{svc_url(o)}">{thumb(o["slug"], "chip-img") or ico(o["icon"])}{E(o["court"])}</a>' for o in SERVICES if o is not s)
        ph = photo(s["slug"], s["nom"], "prose-photo", "(max-width: 1100px) 100vw, 760px")
        content = f'''<article class="prose">
  <p class="intro">{s["intro"]}</p>
  {video_card(s["slug"], "inline")}
  {ph}
  {before_after(s)}
  <div class="note-box">{ico("i-euro")}<p>{t("Price:", "Prix :", "Precio:")} {prix_txt(s, True)}. {t('The exact price is given on the phone and confirmed in a written quote before any work. <a href="/prices/">Day, evening and night prices</a>', 'Le prix exact est annoncé au téléphone et confirmé par un devis écrit avant toute intervention. <a href="/prices/">Tarifs de jour, de soirée et de nuit</a>', 'El precio exacto se anuncia por teléfono y se confirma con un presupuesto escrito antes de cualquier trabajo. <a href="/prices/">Precios de día, de tarde y de noche</a>')}</p></div>
  {secs}
  <h2>{E(s["court"])}{t(": choose your arrondissement", " : choisissez votre arrondissement", ": elija su distrito")}</h2>
  {arr_grid(link=lambda z: f"{z['url']}#{s['slug']}", cls="arr-grid compact")}
  <h2>{t("A clear, all-inclusive price", "Un prix clair, tout compris", "Un precio claro, todo incluido")}</h2>
  <p>{t("The price you are given on the phone includes VAT and labor. It is confirmed in a written quote before any work: if the situation on site turns out to be different from what you described, the locksmith explains why and offers a new quote, which you are free to refuse.", "Le prix annoncé au téléphone comprend la TVA et la main-d'œuvre. Il est confirmé par un devis écrit avant toute intervention : si la situation sur place est différente de ce que vous avez décrit, le serrurier vous explique pourquoi et vous propose un nouveau devis, que vous êtes libre de refuser.", "El precio que se le anuncia por teléfono incluye el IVA y la mano de obra. Se confirma con un presupuesto escrito antes de cualquier trabajo: si la situación en el sitio es distinta de la que describió, el cerrajero le explica por qué y le propone un nuevo presupuesto, que usted es libre de rechazar.")}</p>
  <div class="trust-duo">{inclus_block()}{engagements_short()}</div>
  <h2>{t("Frequently asked questions", "Questions fréquentes", "Preguntas frecuentes")}</h2>
  {faq_html(s["faq"])}
  <h2>{t("Our other services", "Nos autres services", "Nuestros otros servicios")}</h2><div class="chips">{others}</div>
</article>'''
        card = hero_card(prix_txt(s), s["court"])
        body = hero([(t("Services", "Services", "Servicios"), "/services/"), (s["court"], None)], f'{E(s["nom"])} {t("in Paris", "à Paris", "en París")}',
                    f'{E(s["resume"])} {t("Anywhere in Paris, 24/7.", "Partout dans Paris, 24h/24.", "En todo París, 24/7.")}',
                    ticks(t(["Price given before we travel", "Signed quote before any work", "Invoice for your insurer"],
                            ["Prix annoncé avant le déplacement", "Devis signé avant toute intervention", "Facture pour votre assurance"], ["Precio anunciado antes del desplazamiento", "Presupuesto firmado antes de cualquier trabajo", "Factura para su seguro"]), "ticks light inline"),
                    kicker=t("Service", "Service", "Servicio"), card=card, quote=s["court"])
        body += f'<section class="sec"><div class="wrap layout">{content}<div class="side-col">{video_card(s["slug"], "side")}{side_box(quote=s["court"])}</div></div></section>'
        body += assureurs_strip() + reviews_block() + contact_band(t(f"{s['court']}? We'll be there fast.", f"{s['court']} ? Nous arrivons vite.", f"¿{s['court']}? Llegamos rápido."),
                                                                   t("Call us or leave your details: we call you back with a clear price.", "Appelez-nous ou laissez vos coordonnées : nous vous rappelons avec un prix clair.", "Llámenos o déjenos sus datos: le devolvemos la llamada con un precio claro."),
                                                                   source=path, service=s["court"])
        ld = [ld_business(), ld_crumbs([(t("Services", "Services", "Servicios"), "/services/"), (s["court"], path)]), ld_faq(s["faq"]),
              {"@context": "https://schema.org", "@type": "Service", "name": s["nom"], "serviceType": s["nom"], "url": URL + path,
               "provider": {"@id": BID}, "areaServed": {"@type": "City", "name": "Paris"},
               **({"offers": {"@type": "Offer", "priceSpecification": {"@type": "PriceSpecification", "minPrice": s["prix_num"], "priceCurrency": "EUR"}}} if s["prix_num"] else {})}]
        if s["slug"] in VIDEOS:
            ld.append(ld_video(s["slug"], path))
        page(path, t(f'{s["nom"]} Paris 24/7 – {s["prix"]} | {NOM}', f'{s["nom"]} à Paris 24h/24 – {s["prix"]} | {NOM}', f'{s["nom"]} en París 24/7 – {s["prix"]} | {NOM}'),
             t(f'{s["nom"]} in Paris, 24/7. {s["resume"]} Price given before we travel. ☎ {TEL}',
               f'{s["nom"]} à Paris, 24h/24. {s["resume"]} Prix annoncé avant le déplacement. ☎ {TEL}', f'{s["nom"]} en París, 24/7. {s["resume"]} Precio anunciado antes del desplazamiento. ☎ {TEL}'), body, ld, active="/services/")


# ---------------------------------------------------------------------------
# Arrondissements
# ---------------------------------------------------------------------------
ARR_INTROS = [
    "Locked out {a}? {nom} sends a qualified locksmith to your door, day or night, usually within about thirty minutes. The price is given on the phone before he sets off.",
    "From {r0} to the quieter streets of the {num}, our locksmiths work 24/7 on lockouts, jammed locks and broken keys, with a signed quote before any work.",
    "With {pop} residents, the {num} arrondissement ({surnom}) sees its share of lockouts and lost keys every day. Our locksmiths know its buildings and the locks fitted in them.",
    "A locksmith emergency {a}? From the {q} neighborhoods to the area around {r1}, we come quickly, at a price agreed in advance, with an invoice your insurer will accept.",
]


def de(x):
    """« de » + nom en français : du jardin, des passages, de l'île, de la rue (en espagnol : del jardín, de la calle)."""
    if LANG == "es":
        return "del " + x[3:] if x.startswith("el ") else "de " + x
    for a, b in (("le ", "du "), ("les ", "des ")):
        if x.startswith(a):
            return b + x[len(a):]
    return "de " + x


def arr_faq(z):
    if LANG == "es":
        return [
            (f"¿Cuánto cuesta un cerrajero {z['a_court']}?", f"Abrir una puerta cerrada de golpe {z['a']} cuesta 110 € IVA incl. entre semana de día, 160 € por la tarde y los fines de semana, y 220 € por la noche. El cambio de bombín empieza en 160 €. El precio siempre se anuncia antes del desplazamiento y se confirma por escrito."),
            (f"¿Cuánto tardan en llegar {z['a']}?", "Unos 30 minutos de media. El tiempo exacto depende del tráfico de París y se le anuncia por teléfono antes de que salga el cerrajero."),
            (f"¿Trabajan de noche {z['a_court']}?", "Sí, 24/7, domingos y festivos incluidos, con una tarifa de noche anunciada de antemano."),
            ("¿Me reembolsarán la factura?", "Nuestra factura detallada es aceptada por las aseguradoras de hogar francesas. El reembolso depende de su póliza (robo, hurto o pérdida de llaves)."),
        ]
    if LANG == "fr":
        return [
            (f"Combien coûte un serrurier {z['a_court']} ?", f"L'ouverture d'une porte claquée {z['a']} coûte 110 € TTC en semaine en journée, 160 € en soirée et le week-end, et 220 € la nuit. Un changement de cylindre démarre à 160 €. Le prix est toujours annoncé avant le déplacement et confirmé par écrit."),
            (f"En combien de temps pouvez-vous arriver {z['a']} ?", "Environ 30 minutes en moyenne. Le délai exact dépend de la circulation parisienne et vous est annoncé au téléphone avant le départ du serrurier."),
            (f"Intervenez-vous la nuit {z['a_court']} ?", "Oui, 24h/24 et 7j/7, dimanches et jours fériés compris, avec un tarif de nuit annoncé à l'avance."),
            ("Ma facture sera-t-elle remboursée ?", "Notre facture détaillée est acceptée par les assureurs habitation. Le remboursement dépend de votre contrat (effraction, vol ou perte de clés)."),
        ]
    return [
        (f"How much does a locksmith cost {z['a_court']}?", f"Opening a slammed door {z['a']} costs €110 incl. VAT on weekdays, €160 in the evening and on weekends and €220 at night. A cylinder replacement starts at €160. The price is always given before we travel and confirmed in writing."),
        (f"How quickly can you get here {z['a']}?", "About 30 minutes on average. The exact time depends on Paris traffic and is given on the phone before the locksmith sets off."),
        (f"Do you work at night {z['a_court']}?", "Yes, 24/7, including Sundays and public holidays, with a night rate given in advance."),
        ("Will my invoice be reimbursed?", "Our detailed invoice is accepted by French home insurers. Reimbursement depends on your policy (break-in, theft or loss of keys)."),
    ]


def local_services(z, i, lst):
    cards = []
    for s in lst:
        k = i + SERVICES.index(s)
        loc_ = SVC_LOCAL[s["slug"]]
        intro = loc_["intros"][k % 3].format(a=z["a"], nom=E(NOM))
        prix = f'{t("from", "dès", "desde")} <b>{eur(s["prix_num"])}</b>' if s["prix_num"] else f'<b>{t("free quote", "sur devis gratuit", "presupuesto gratuito")}</b>'
        ph = photo(s["slug"], "", "sl-photo", "(max-width: 760px) 100vw, 540px")
        if ph and os.path.exists(os.path.join(ROOT, "assets", "img", "thumbs", f'{s["slug"]}.webp')):
            # sur téléphone, la miniature légère (11 Ko) au lieu de la grande photo
            ph = f'<picture class="ph"><source media="(max-width: 760px)" srcset="/assets/img/thumbs/{s["slug"]}.webp">{ph}</picture>'
        cards.append(f'''<article class="svc-local{" has-photo" if ph else ""}" id="{s["slug"]}">
  {ph}
  <div class="sl-head"><span class="svc-ic">{ico(s["icon"])}</span><div><h3>{E(s["nom"])}</h3><span class="sl-price">{prix}</span></div></div>
  <p>{intro}</p>
  <p class="sl-tip"><strong>{t("Tip:", "Conseil :", "Consejo:")}</strong> {E(loc_["conseil"])}</p>
  <div class="sl-acts">{btn_wa_svc(s)}<a class="text-link" href="{svc_url(s)}">{t("How we work", "Notre méthode", "Cómo trabajamos")} {ico("i-arrow", "ic sm")}</a></div>
</article>''')
    return '<div class="sl-grid">' + "".join(cards) + "</div>"


def recent_jobs(z):
    jobs = INTERVENTIONS.get(z["n"], [])
    if not jobs:
        return ""
    lis = "".join(f'<li><small>{E(d)} · {E(rue)}</small><b>{E(txt)}</b></li>' for d, rue, txt in jobs)
    return f'<h2>{t("Recent jobs", "Interventions récentes", "Intervenciones recientes")} {E(z["a"])}</h2><ul class="jobs">{lis}</ul>'


def build_arr_pages():
    fr = LANG == "fr"
    body = hero([(t("Arrondissements", "Arrondissements", "Distritos"), None)], t("Locksmith in all <em>20 Paris arrondissements</em>", "Serrurier dans les <em>20 arrondissements de Paris</em>", "Cerrajero en los <em>20 distritos de París</em>"),
                t("Choose your arrondissement: prices, neighborhoods covered and services available near you.",
                  "Choisissez votre arrondissement : prix, quartiers couverts et services disponibles près de chez vous.", "Elija su distrito: precios, barrios cubiertos y servicios disponibles cerca de usted."), kicker="Paris 75")
    body += f'''<section class="sec"><div class="wrap">
  {arr_grid(label=lambda z: z["surnom"])}
  <div class="prose narrow">
    <h2>{t("A Paris locksmith, not a call center", "Un serrurier parisien, pas un centre d'appels", "Un cerrajero parisino, no una centralita")}</h2>
    <p>{E(NOM)} {t("works exclusively within Paris. That focus lets us arrive quickly and know Parisian buildings well: landing doors in Haussmann buildings, multi-point armored doors, old mortise locks and modern badge-access residences.", "intervient exclusivement dans Paris. Cela nous permet d'arriver vite et de bien connaître les immeubles parisiens : portes palières haussmanniennes, portes blindées multipoints, vieilles serrures à larder et résidences modernes à badge.", "trabaja exclusivamente dentro de París. Eso nos permite llegar rápido y conocer bien los edificios parisinos: puertas de rellano haussmannianas, puertas blindadas multipunto, viejas cerraduras embutidas y residencias modernas con acceso por tarjeta.")}</p>
    <p class="note-box">{ico("i-pin")}{t("Just outside Paris? Call us on", "Juste à l'extérieur de Paris ? Appelez-nous au", "¿Justo fuera de París? Llámenos al")} <a href="{TEL_HREF}">{TEL}</a>{t(": depending on availability, we can sometimes come, with travel costs given in advance.", " : selon nos disponibilités, nous pouvons parfois venir, avec des frais de déplacement annoncés à l'avance.", ": según nuestra disponibilidad, a veces podemos ir, con unos gastos de desplazamiento anunciados de antemano.")}</p>
  </div>
</div></section>''' + reviews_block() + contact_band(source="/locksmith-paris/")
    page("/locksmith-paris/", t(f"Locksmith Paris: all 20 arrondissements 24/7 | {NOM}", f"Serrurier Paris : les 20 arrondissements 24h/24 | {NOM}", f"Cerrajero París: los 20 distritos 24/7 | {NOM}"),
         t(f"Locksmith everywhere in Paris, from the 1st to the 20th arrondissement, 24/7. Door opening from €110 incl. VAT, price given before we travel. ☎ {TEL}",
           f"Serrurier partout dans Paris, du 1er au 20e arrondissement, 24h/24. Ouverture de porte dès 110 € TTC, prix annoncé avant le déplacement. ☎ {TEL}", f"Cerrajero en todo París, del distrito 1 al 20, 24/7. Apertura de puerta desde 110 € IVA incl., precio anunciado antes del desplazamiento. ☎ {TEL}"),
         body, [ld_business(full=True), ld_crumbs([(t("Arrondissements", "Arrondissements", "Distritos"), "/locksmith-paris/")])], active="/locksmith-paris/")

    serrurier = t("Locksmith", "Serrurier", "Cerrajero")
    for i, z in enumerate(ARR):
        path = z["url"]
        intro = ARR_INTROS[i % 4].format(a=z["a"], nom=E(NOM), num=z["num"], r0=z["reperes"][0], r1=z["reperes"][1],
                                         pop=fmt_int(z["pop"]), surnom=z["surnom"], q=et(z["quartiers"][:2]),
                                         de_r0=de(z["reperes"][0]), de_r1=de(z["reperes"][1]))
        intro = intro[0].upper() + intro[1:]
        facts = f'''<div class="facts">
  <div><small>{t("Postcode", "Code postal", "Código postal")}</small><b>{E(" / ".join(z["cp"]))}</b></div>
  <div><small>{t("Door opening", "Ouverture de porte", "Apertura de puerta")}</small><b>{t("from", "dès", "desde")} {eur(110)}</b></div>
  <div><small>{t("Availability", "Disponibilité", "Disponibilidad")}</small><b>{t("24/7", "24h/24", "24/7")}</b></div>
  <div><small>{t("Average arrival", "Arrivée moyenne", "Llegada media")}</small><b>≈ 30 min</b></div>
</div>'''
        nav_arr = ""

        def pn(o, sens):
            return (f'<a class="pn pn-{sens}" href="{o["url"]}"><img src="/assets/img/arr/{o["n"]}.webp" alt="" width="176" height="176" loading="lazy" decoding="async">'
                    f'<span><small>{t("← Previous", "← Précédent", "← Anterior") if sens == "prev" else t("Next →", "Suivant →", "Siguiente →")}</small><b>{serrurier} {E(o["court"])}</b></span></a>')
        if z["prev"]:
            nav_arr += pn(z["prev"], "prev")
        if z["next"]:
            nav_arr += pn(z["next"], "next")
        faq = arr_faq(z)
        habitat = z["habitat"][0].upper() + z["habitat"][1:]
        content = f'''<article class="prose">
  <p class="intro">{intro}</p>
  {facts}
  <h2>{t("Our services", "Nos services", "Nuestros servicios")} {E(z["a"])}</h2>
  <h3 class="group-title">{ico("i-clock")}{t("Emergency call-outs <small>24/7</small>", "Dépannage d'urgence <small>24h/24</small>", "Asistencia urgente <small>24/7</small>")}</h3>
  {local_services(z, i, SVC_URG)}
  <h3 class="group-title">{ico("i-shield")}{t("Works, armored doors &amp; installation <small>by appointment</small>", "Travaux, portes blindées et installation <small>sur rendez-vous</small>", "Obras, puertas blindadas e instalación <small>con cita previa</small>")}</h3>
  {local_services(z, i, SVC_TRAV)}
  {recent_jobs(z)}
  <h2>{t("Neighborhoods covered in the", "Quartiers couverts dans le", "Barrios cubiertos en el distrito")} {z["num"]}</h2>
  <p>{t("We cover the arrondissement's four administrative quarters:", "Nous couvrons les quatre quartiers administratifs de l'arrondissement :", "Cubrimos los cuatro barrios administrativos del distrito:")} <strong>{E(et(z["quartiers"]))}</strong>. {t("Whether you live near " + E(et(z["reperes"])), "Que vous habitiez près " + E(", ".join(de(r) for r in z["reperes"][:-1]) + " ou " + de(z["reperes"][-1])), "Tanto si vive cerca " + E(", ".join(de(r) for r in z["reperes"][:-1]) + " o " + de(z["reperes"][-1])))}, {t("a locksmith can be with you quickly.", "un serrurier peut être chez vous rapidement.", "un cerrajero puede estar en su casa rápidamente.")}</p>
  <div class="local">
    <div>{ico("i-metro")}<h3>{t("Landmarks", "Repères", "Referencias")}</h3><p>{t("Metro:", "Métro :", "Metro:")} {E(et(z["metros"]))}</p></div>
    <div>{ico("i-home")}<h3>{t("Buildings", "Habitat", "Viviendas")}</h3><p>{E(habitat)}.</p></div>
    <div>{ico("i-pin")}<h3>{t("Population", "Population", "Población")}</h3><p>{fmt_int(z["pop"])} {t("residents (INSEE)", "habitants (Insee)", "habitantes (INSEE)")}</p></div>
  </div>
  <h2>{t("Why call us", "Pourquoi nous appeler", "¿Por qué llamarnos")} {E(z["a"])}{t("?", " ?", "?")}</h2>
  <p>{t(f"When you need an emergency locksmith {E(z['a_court'])}, you often come across anonymous numbers and unrealistic teaser prices. With {E(NOM)}, you know who you are dealing with: an identified company, published prices, a signed quote before every job and public customer reviews on Google.", f"Quand vous cherchez un serrurier en urgence {E(z['a_court'])}, vous tombez souvent sur des numéros anonymes et des prix d'appel irréalistes. Avec {E(NOM)}, vous savez à qui vous avez affaire : une entreprise identifiée, des tarifs publiés, un devis signé avant chaque intervention et des avis clients publics sur Google.", f"Cuando busca un cerrajero urgente {E(z['a_court'])}, a menudo se encuentra con números anónimos y precios de reclamo poco realistas. Con {E(NOM)}, sabe con quién trata: una empresa identificada, precios publicados, un presupuesto firmado antes de cada intervención y opiniones públicas de clientes en Google.")}</p>
  <ul class="check-list">
    {t(f'''<li>{ico("i-check")}<span><strong>Price given on the phone</strong>, then a written quote signed before any work.</span></li>
    <li>{ico("i-check")}<span><strong>Damage-free opening</strong> in the vast majority of cases.</span></li>
    <li>{ico("i-check")}<span><strong>Detailed invoice</strong> accepted by French home insurers.</span></li>
    <li>{ico("i-check")}<span><strong>Public reviews</strong> you can check on <a href="{E(MAPS)}" target="_blank" rel="noopener">our Google profile</a>.</span></li>''',
    f'''<li>{ico("i-check")}<span><strong>Prix annoncé au téléphone</strong>, puis devis écrit signé avant toute intervention.</span></li>
    <li>{ico("i-check")}<span><strong>Ouverture sans casse</strong> dans l'immense majorité des cas.</span></li>
    <li>{ico("i-check")}<span><strong>Facture détaillée</strong> acceptée par les assureurs habitation.</span></li>
    <li>{ico("i-check")}<span><strong>Avis publics</strong> à consulter sur <a href="{E(MAPS)}" target="_blank" rel="noopener">notre fiche Google</a>.</span></li>''', f'''<li>{ico("i-check")}<span><strong>Precio anunciado por teléfono</strong> y después presupuesto escrito firmado antes de cualquier trabajo.</span></li>
    <li>{ico("i-check")}<span><strong>Apertura sin daños</strong> en la inmensa mayoría de los casos.</span></li>
    <li>{ico("i-check")}<span><strong>Factura detallada</strong> aceptada por las aseguradoras de hogar francesas.</span></li>
    <li>{ico("i-check")}<span><strong>Opiniones públicas</strong> que puede consultar en <a href="{E(MAPS)}" target="_blank" rel="noopener">nuestro perfil de Google</a>.</span></li>''')}
  </ul>
  <h2>{t("Frequently asked questions", "Questions fréquentes", "Preguntas frecuentes")} {E(z["a_court"])}</h2>
  {faq_html(faq)}
  <nav class="prev-next" aria-label="{t("Neighboring arrondissements", "Arrondissements voisins", "Distritos vecinos")}">{nav_arr}</nav>
</article>'''
        h1 = f'{serrurier} {E(z["court"])} <em>{t("24/7", "24h/24", "24/7")}</em>'
        lead = t(f'Door opening from €110 incl. VAT, jammed locks, broken keys, lock replacement {E(z["a"])} ({E(z["surnom"])}). Price given before we travel, free quote.',
                 f'Ouverture de porte dès 110 € TTC, serrure bloquée, clé cassée, changement de serrure {E(z["a"])} ({E(z["surnom"])}). Prix annoncé avant le déplacement, devis gratuit.', f'Apertura de puerta desde 110 € IVA incl., cerradura bloqueada, llave rota, cambio de cerradura {E(z["a"])} ({E(z["surnom"])}). Precio anunciado antes del desplazamiento, presupuesto gratuito.')
        crumb_items = [(t("Arrondissements", "Arrondissements", "Distritos"), "/locksmith-paris/"), (z["court"], None)]
        body = hero(crumb_items, h1, lead, ticks(t(["Free quote", "No hidden fees", "Nights, weekends, holidays"], ["Devis gratuit", "Aucun frais caché", "Nuits, week-ends, jours fériés"], ["Presupuesto gratuito", "Sin gastos ocultos", "Noches, fines de semana, festivos"]), "ticks light inline"),
                    kicker=f"{z['cp'][0]} · {z['surnom']}", bg=zone_bg(z))
        body += f'<section class="sec"><div class="wrap layout">{content}{side_box(f"{serrurier} {z["court"]}")}</div></section>'
        body += assureurs_strip() + contact_band(t(f"Locked out {z['a_court']}?", f"Porte claquée {z['a_court']} ?", f"¿Se ha quedado fuera {z['a_court']}?"),
                                                 t("Call us: price given on the phone, locksmith on the way straight away.", "Appelez-nous : prix annoncé au téléphone, serrurier en route aussitôt.", "Llámenos: precio anunciado por teléfono y cerrajero en camino al momento."),
                                                 source=path, arr=z["court"])
        ld = [ld_business(), ld_crumbs([(t("Arrondissements", "Arrondissements", "Distritos"), "/locksmith-paris/"), (z["court"], path)]), ld_faq(faq),
              {"@context": "https://schema.org", "@type": "Service", "name": f"{serrurier} {z['nom']}", "serviceType": t("24/7 locksmith services", "Serrurerie 24h/24", "Cerrajería 24/7"),
               "url": URL + path, "provider": {"@id": BID},
               "areaServed": {"@type": "AdministrativeArea", "name": z["nom"], "postalCode": z["cp"][0]},
               "offers": {"@type": "Offer", "priceSpecification": {"@type": "PriceSpecification", "minPrice": 110, "priceCurrency": "EUR"}}}]
        page(path, t(f"Locksmith {z['court']} ({z['cp'][0]}) 24/7 – {TEL}", f"Serrurier {z['court']} ({z['cp'][0]}) 24h/24 – {TEL}", f"Cerrajero {z['court']} ({z['cp'][0]}) 24/7 – {TEL}"),
             t(f"Locksmith {z['court']} ({z['cp'][0]}), 24/7: door opening from €110 incl. VAT, jammed locks, broken keys, lock replacement. Price given before we travel. ☎ {TEL}",
               f"Serrurier {z['court']} ({z['cp'][0]}), 24h/24 : ouverture de porte dès 110 € TTC, serrure bloquée, clé cassée, changement de serrure. Prix annoncé avant le déplacement. ☎ {TEL}", f"Cerrajero {z['court']} ({z['cp'][0]}), 24/7: apertura de puerta desde 110 € IVA incl., cerradura bloqueada, llave rota, cambio de cerradura. Precio anunciado antes del desplazamiento. ☎ {TEL}"),
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
        m = re.search(r"\d[\d,\s ]*", jour)
        if not m:
            continue
        val = int(re.sub(r"\D", "", m.group(0)))
        spec = {"@type": "PriceSpecification", "priceCurrency": "EUR", "valueAddedTaxIncluded": True}
        spec.update({"minPrice": val} if jour.startswith(("From", "À partir", "Desde")) else {"price": val})
        offers.append({"@type": "Offer", "name": p, "priceSpecification": spec, "itemOffered": {"@type": "Service", "name": p}, "seller": {"@id": BID}})
    return {"@context": "https://schema.org", "@type": "OfferCatalog", "name": t(f"{NOM} prices", f"Tarifs {NOM}", f"Precios {NOM}"), "url": URL + "/prices/", "itemListElement": offers}


def build_static():
    # Prices
    body = hero([(t("Prices", "Tarifs", "Precios"), None)], t("Fully <em>transparent</em> prices", "Des tarifs <em>totalement transparents</em>", "Precios <em>totalmente transparentes</em>"),
                t("Prices per service and per time of day. Everything is given before we travel and nothing is added on the way.",
                  "Les prix par prestation et par heure d'intervention. Tout est annoncé avant le déplacement et rien ne s'ajoute en route.", "Los precios por servicio y por hora de intervención. Todo se anuncia antes del desplazamiento y nada se añade por el camino."),
                kicker=t("No hidden fees", "Aucun frais caché", "Sin gastos ocultos"))
    prose = t('''<h2>What the price includes</h2>
      <ul><li>The locksmith's labor.</li><li>Travel within Paris, free if work is carried out.</li><li>VAT: all our prices include VAT.</li><li>A detailed invoice suitable for your insurer.</li></ul>
      <h2>Our commitments</h2>
      <ul><li><strong>Price given</strong> before the locksmith sets off.</li><li><strong>Written, signed quote</strong> before any work.</li><li><strong>No surprise surcharge</strong>: the evening or night rate is given on the phone.</li><li><strong>Certified equipment</strong> from recognized brands.</li></ul>
      <h2>Broken keys, smart locks, break-ins</h2>
      <p>These jobs depend heavily on the situation: they come with a <strong>free quote</strong>, given on the phone and then confirmed in writing.</p>
      <h2>Payment</h2><p>Card, cash or bank transfer.</p>''',
              '''<h2>Ce que comprend le prix</h2>
      <ul><li>La main-d'œuvre du serrurier.</li><li>Le déplacement dans Paris, offert si des travaux sont réalisés.</li><li>La TVA : tous nos prix sont TTC.</li><li>Une facture détaillée, conforme pour votre assurance.</li></ul>
      <h2>Nos engagements</h2>
      <ul><li><strong>Prix annoncé</strong> avant le départ du serrurier.</li><li><strong>Devis écrit et signé</strong> avant toute intervention.</li><li><strong>Aucune majoration surprise</strong> : le tarif de soirée ou de nuit est annoncé au téléphone.</li><li><strong>Matériel certifié</strong> de marques reconnues.</li></ul>
      <h2>Clés cassées, serrures connectées, effractions</h2>
      <p>Ces interventions dépendent beaucoup de la situation : elles font l'objet d'un <strong>devis gratuit</strong>, annoncé au téléphone puis confirmé par écrit.</p>
      <h2>Paiement</h2><p>Carte bancaire, espèces ou virement.</p>''', '''<h2>Lo que incluye el precio</h2>
      <ul><li>La mano de obra del cerrajero.</li><li>El desplazamiento dentro de París, gratuito si se realiza el trabajo.</li><li>El IVA: todos nuestros precios incluyen IVA.</li><li>Una factura detallada, válida para su aseguradora.</li></ul>
      <h2>Nuestros compromisos</h2>
      <ul><li><strong>Precio anunciado</strong> antes de que salga el cerrajero.</li><li><strong>Presupuesto escrito y firmado</strong> antes de cualquier trabajo.</li><li><strong>Ningún recargo sorpresa</strong>: la tarifa de tarde o de noche se anuncia por teléfono.</li><li><strong>Material certificado</strong> de marcas reconocidas.</li></ul>
      <h2>Llaves rotas, cerraduras inteligentes, robos</h2>
      <p>Estas intervenciones dependen mucho de la situación: se hacen con <strong>presupuesto gratuito</strong>, anunciado por teléfono y confirmado después por escrito.</p>
      <h2>Pago</h2><p>Tarjeta bancaria, efectivo o transferencia.</p>''')
    body += f'''<section class="sec"><div class="wrap">
  {tarif_table()}
  <div class="layout" style="margin-top:56px">
    <article class="prose">
      {prose}
    </article>
    {side_box(t("Your price on the phone", "Votre prix au téléphone", "Su precio por teléfono"), t("Describe the situation: you know the exact price before we set off.", "Décrivez la situation : vous connaissez le prix exact avant notre départ.", "Describa la situación: conocerá el precio exacto antes de que salgamos."))}
  </div>
</div></section>''' + assureurs_strip() + contact_band(source="/prices/")
    page("/prices/", t(f"Locksmith prices Paris – day, evening, night | {NOM}", f"Tarifs serrurier Paris – jour, soir, nuit | {NOM}", f"Precios de cerrajero en París – día, tarde, noche | {NOM}"),
         t("Locksmith prices in Paris: slammed door opening €110 incl. VAT during the day, locked door from €180, cylinder replacement from €160. Evening and night rates shown.",
           "Tarifs serrurier à Paris : ouverture de porte claquée 110 € TTC en journée, porte fermée à clé dès 180 €, changement de cylindre dès 160 €. Tarifs de soirée et de nuit affichés.", "Precios de cerrajero en París: apertura de puerta cerrada de golpe 110 € IVA incl. de día, puerta cerrada con llave desde 180 €, cambio de bombín desde 160 €. Tarifas de tarde y de noche publicadas."),
         body, [ld_business(), ld_crumbs([(t("Prices", "Tarifs", "Precios"), "/prices/")]), ld_tarifs()], active="/prices/")

    # Insurance
    note_ins = f'<p class="note-box">{ico("i-shield")}{E(NOM)} {t("is an independent company with no partnership with insurance companies. Reimbursement depends on your policy.", "est une entreprise indépendante, sans partenariat avec les compagnies d’assurance. Le remboursement dépend de votre contrat.", "es una empresa independiente, sin acuerdos con las compañías de seguros. El reembolso depende de su póliza.")}</p>'
    simple("/insurance/", t("Insurance", "Assurance", "Seguro"), t("Locksmith &amp; insurance: <em>getting reimbursed</em>", "Serrurier et assurance : <em>se faire rembourser</em>", "Cerrajero y seguro: <em>cómo obtener el reembolso</em>"),
           t("Our invoices are accepted by French home insurers. Here is how to get a locksmith call-out reimbursed.",
             "Nos factures sont acceptées par les assureurs habitation. Voici comment vous faire rembourser une intervention de serrurier.", "Nuestras facturas son aceptadas por las aseguradoras de hogar francesas. Así puede conseguir que le reembolsen la intervención de un cerrajero."),
           t('''<h2>When does insurance pay?</h2>
<p>Most French home insurance policies (multirisque habitation) cover locksmith costs after a <strong>burglary or attempted break-in</strong>. Some also cover <strong>theft</strong> or <strong>loss of keys</strong>, sometimes as an option. A door that has simply slammed shut is rarely covered, unless you have an assistance guarantee: check your policy. If you are a visitor, your travel insurance may also include assistance.</p>
<h2>Documents to provide</h2>
<ul><li>The <strong>police report receipt</strong> in case of break-in or theft.</li><li>Our <strong>detailed invoice</strong> (work done, parts fitted, price including VAT).</li><li>The <strong>signed quote</strong> and, on request, <strong>before/after photos</strong>.</li></ul>
<h2>Deadlines</h2>
<p>After a theft or burglary, you usually have <strong>2 working days</strong> to notify your insurer. For other claims, the deadline is often 5 working days. Your policy is the reference.</p>
<h2>How we help</h2>
<p>We give you all the supporting documents and can temporarily secure your door until the insurance assessor visits.</p>''',
             '''<h2>Quand l'assurance prend-elle en charge ?</h2>
<p>La plupart des contrats multirisques habitation couvrent les frais de serrurier après un <strong>cambriolage ou une tentative d'effraction</strong>. Certains couvrent aussi le <strong>vol</strong> ou la <strong>perte des clés</strong>, parfois en option. Une porte simplement claquée est rarement couverte, sauf garantie assistance : vérifiez votre contrat. Si vous êtes de passage, votre assurance voyage peut aussi inclure une assistance.</p>
<h2>Les documents à fournir</h2>
<ul><li>Le <strong>récépissé de dépôt de plainte</strong> en cas d'effraction ou de vol.</li><li>Notre <strong>facture détaillée</strong> (travaux réalisés, pièces posées, prix TTC).</li><li>Le <strong>devis signé</strong> et, sur demande, des <strong>photos avant/après</strong>.</li></ul>
<h2>Les délais</h2>
<p>Après un vol ou un cambriolage, vous disposez en général de <strong>2 jours ouvrés</strong> pour prévenir votre assureur. Pour les autres sinistres, le délai est souvent de 5 jours ouvrés. Votre contrat fait foi.</p>
<h2>Notre accompagnement</h2>
<p>Nous vous remettons tous les justificatifs et pouvons sécuriser provisoirement votre porte jusqu'au passage de l'expert de l'assurance.</p>''', '''<h2>¿Cuándo paga el seguro?</h2>
<p>La mayoría de los seguros de hogar franceses (multirriesgo hogar, «multirisque habitation») cubren los gastos de cerrajero tras un <strong>robo o un intento de robo con fuerza</strong>. Algunos cubren también el <strong>hurto</strong> o la <strong>pérdida de llaves</strong>, a veces como opción. Una puerta que simplemente se ha cerrado de golpe rara vez está cubierta, salvo si tiene una garantía de asistencia: revise su póliza. Si está de viaje, su seguro de viaje también puede incluir asistencia.</p>
<h2>Documentos que hay que aportar</h2>
<ul><li>El <strong>resguardo de la denuncia</strong> en caso de robo o hurto.</li><li>Nuestra <strong>factura detallada</strong> (trabajos realizados, piezas instaladas, precio con IVA).</li><li>El <strong>presupuesto firmado</strong> y, si se solicitan, <strong>fotos del antes y el después</strong>.</li></ul>
<h2>Plazos</h2>
<p>Tras un robo, normalmente dispone de <strong>2 días hábiles</strong> para avisar a su aseguradora. Para otros siniestros, el plazo suele ser de 5 días hábiles. Lo que cuenta es su póliza.</p>
<h2>Cómo le ayudamos</h2>
<p>Le entregamos todos los justificantes y podemos asegurar provisionalmente su puerta hasta la visita del perito del seguro.</p>''') + note_ins,
           t(f"Locksmith & home insurance: reimbursable invoice | {NOM}", f"Serrurier et assurance habitation : facture remboursable | {NOM}", f"Cerrajero y seguro de hogar: factura reembolsable | {NOM}"),
           t("How to get a locksmith reimbursed by your home insurance in France: guarantees, documents, deadlines. Our invoices are accepted by insurers.",
             "Comment se faire rembourser un serrurier par son assurance habitation : garanties, documents, délais. Nos factures sont acceptées par les assureurs.", "Cómo conseguir que su seguro de hogar en Francia le reembolse un cerrajero: garantías, documentos, plazos. Nuestras facturas son aceptadas por las aseguradoras."),
           after=assureurs_strip() + contact_band(source="/insurance/"))

    # FAQ
    allfaq = HOME_FAQ + [q for s in SERVICES for q in s["faq"]]
    simple("/faq/", t("FAQ", "FAQ", "Preguntas frecuentes"), t("Frequently asked <em>questions</em>", "Questions <em>fréquentes</em>", "Preguntas <em>frecuentes</em>"),
           t("Prices, arrival times, insurance, opening techniques: everything we are asked most often.",
             "Prix, délais, assurance, techniques d'ouverture : tout ce qu'on nous demande le plus souvent.", "Precios, tiempos de llegada, seguro, técnicas de apertura: todo lo que más nos preguntan."),
           f"<h2>{t('General', 'Général', 'General')}</h2>" + faq_html(HOME_FAQ) + "".join(f'<h2>{E(s["court"])}</h2>' + faq_html(s["faq"]) for s in SERVICES),
           t(f"FAQ – locksmith Paris | {NOM}", f"Questions fréquentes – serrurier Paris | {NOM}", f"Preguntas frecuentes – cerrajero París | {NOM}"),
           t("Door opening prices, arrival times, insurance reimbursement, damage-free opening: our answers.",
             "Prix d'une ouverture de porte, délais d'intervention, remboursement par l'assurance, ouverture sans casse : nos réponses.", "Precio de una apertura de puerta, tiempos de intervención, reembolso del seguro, apertura sin daños: nuestras respuestas."),
           extra_ld=[ld_faq(allfaq)], after=contact_band(source="/faq/"))

    # Reviews
    crumb = t("Customer reviews", "Avis clients", "Opiniones de clientes")
    body = hero([(crumb, None)], t("Customer reviews <em>on Google</em>", "Avis clients <em>sur Google</em>", "Opiniones de clientes <em>en Google</em>"),
                t("Our customers post their reviews on our Google Business Profile: they are public and verifiable.",
                  "Nos clients publient leurs avis sur notre fiche Google : ils sont publics et vérifiables.", "Nuestros clientes publican sus opiniones en nuestro perfil de Google: son públicas y verificables."), google_badge("g-badge dark"))
    body += reviews_block(t("Our reputation, fully transparent", "Notre réputation, en toute transparence", "Nuestra reputación, con total transparencia")) + contact_band(source="/reviews/")
    page("/reviews/", t(f"Customer reviews – locksmith Paris | {NOM}", f"Avis clients – serrurier Paris | {NOM}", f"Opiniones de clientes – cerrajero París | {NOM}"),
         t("Read our customers' Google reviews and leave your own. Locksmith in Paris, 24/7.", "Lisez les avis Google de nos clients et laissez le vôtre. Serrurier à Paris, 24h/24.", "Lea las opiniones de nuestros clientes en Google y deje la suya. Cerrajero en París, 24/7."),
         body, [ld_business(), ld_crumbs([(crumb, "/reviews/")])], active="/reviews/")

    # Contact
    body = hero([(t("Contact", "Contact", "Contacto"), None)], t("Contact <em>your locksmith</em>", "Contactez <em>votre serrurier</em>", "Contacte con <em>su cerrajero</em>"),
                t("For an emergency, calling is fastest. For a quote or planned work, write to us.",
                  "En cas d'urgence, le plus rapide est d'appeler. Pour un devis ou des travaux, écrivez-nous.", "En caso de urgencia, lo más rápido es llamar. Para un presupuesto o un trabajo programado, escríbanos."))
    body += f'''<section class="sec cream"><div class="wrap contact-grid">
  <div class="contact-card">
    <h2>{E(NOM)}</h2>
    <p>{t(f"{E(slogan())} in all 20 Paris arrondissements, 24/7. We speak English and French.", f"{E(slogan())} dans les 20 arrondissements de Paris, 24h/24. Nous parlons français et anglais.", f"{E(slogan())} en los 20 distritos de París, 24/7. Hablamos francés e inglés.")}</p>
    <a class="c-line" href="{TEL_HREF}" data-track="call_contact">{ico("i-phone")}<span><small>{t("Phone 24/7", "Téléphone 24h/24", "Teléfono 24/7")}</small><b>{TEL}</b></span></a>
    <a class="c-line" href="{E(wa_link(WA_MSG))}" target="_blank" rel="noopener" data-track="wa_contact">{ico("i-wa")}<span><small>WhatsApp</small><b>{t("Send a photo", "Envoyer une photo", "Enviar una foto")}</b></span></a>
    <a class="c-line" href="mailto:{CONFIG["email"]}">{ico("i-mail")}<span><small>Email</small><b>{CONFIG["email"]}</b></span></a>
    <a class="c-line" href="{CONFIG["instagram"]}" target="_blank" rel="noopener me">{ico("i-insta")}<span><small>Instagram</small><b>@securelockserrurerie</b></span></a>
    <div class="c-line">{ico("i-pin")}<span><small>{t("Service area", "Zone d'intervention", "Zona de servicio")}</small><b>{t("Paris, 1st to 20th arrondissement", "Paris, du 1er au 20e arrondissement", "París, del distrito 1 al 20")}</b></span></div>
  </div>
  {lead_form("/contact/", titre=t("Write to us", "Écrivez-nous", "Escríbanos"), sous=t("Quote, call-back, question: quick reply, 7 days a week.", "Devis, rappel, question : réponse rapide, 7 jours sur 7.", "Presupuesto, llamada, pregunta: respuesta rápida, los 7 días de la semana."))}
</div></section>
<section class="sec"><div class="wrap"><div class="sec-head"><span class="eyebrow">{t("Google Business Profile", "Fiche Google", "Perfil de Google")}</span><h2>{t("Find us", "Nous trouver", "Dónde encontrarnos")}</h2></div>{map_embed()}</div></section>''' + reviews_block()
    page("/contact/", t(f"Contact – locksmith Paris 24/7 | {NOM}", f"Contact – serrurier Paris 24h/24 | {NOM}", f"Contacto – cerrajero París 24/7 | {NOM}"),
         t(f"Contact {NOM} on {TEL}, 24/7, by phone, WhatsApp or email. Free quote, fast call-out anywhere in Paris. English spoken.",
           f"Contactez {NOM} au {TEL}, 24h/24, par téléphone, WhatsApp ou email. Devis gratuit, intervention rapide partout dans Paris.", f"Contacte con {NOM} en el {TEL}, 24/7, por teléfono, WhatsApp o email. Presupuesto gratuito, intervención rápida en todo París."),
         body, [ld_business(full=True), ld_crumbs([(t("Contact", "Contact", "Contacto"), "/contact/")])], active="/contact/")

    # Legal notice
    lignes = [E(CONFIG["raison_sociale"]) + (f" ({t('trading as', 'nom commercial :', 'nombre comercial:')} {E(NOM)})" if NOM != CONFIG["raison_sociale"] else "")]
    if CONFIG["responsable"]:
        lignes.append(f"{t('Publication director', 'Directeur de la publication', 'Director de la publicación')} : {E(CONFIG['responsable'])}")
    if CONFIG["siren"]:
        lignes.append(f"SIREN : {CONFIG['siren']}")
    if CONFIG["siret"]:
        lignes.append(f"SIRET : {CONFIG['siret']}")
    lignes += [f"{t('Address:', 'Adresse :', 'Dirección:')} {E(adresse_txt())}", f"{t('Phone:', 'Téléphone :', 'Teléfono:')} {TEL}", f"Email{t(':', ' :', ':')} {CONFIG['email']}"]
    mediateur = E(CONFIG["mediateur"]) or t("their contact details are available on request at ", "ses coordonnées sont disponibles sur demande à ", "sus datos de contacto están disponibles a petición en ") + CONFIG["email"]
    simple("/legal-notice/", t("Legal notice", "Mentions légales", "Aviso legal"), t("Legal notice", "Mentions légales", "Aviso legal"),
           t("Legal information about this website and the company.", "Informations légales sur ce site et l'entreprise.", "Información legal sobre esta web y la empresa."),
           t(f'''<h2>Website publisher</h2><p>{"<br>".join(lignes)}</p>
<h2>Hosting</h2><p>Netlify, Inc. – 44 Montgomery Street, Suite 300, San Francisco, CA 94104, United States.</p>
<h2>Intellectual property</h2><p>The texts, logo and graphic elements of this website belong to {E(NOM)}, unless otherwise stated. Insurance company and brand names are mentioned for information only and do not imply any partnership.</p>
<h2>Consumer mediation</h2><p>In accordance with article L612-1 of the French Consumer Code, you may use a consumer mediator free of charge: {mediateur}.</p>
<h2>Prices and quotes</h2><p>Prices shown are starting prices including VAT. In accordance with the French decree of 24 January 2017 on repair and maintenance call-outs in the building sector, a free, detailed quote is given and signed before any work, and a detailed invoice is provided at the end.</p>
<h2>Liability</h2><p>The information on this website is provided for guidance and may change.</p>''',
             f'''<h2>Éditeur du site</h2><p>{"<br>".join(lignes)}</p>
<h2>Hébergement</h2><p>Netlify, Inc. – 44 Montgomery Street, Suite 300, San Francisco, CA 94104, États-Unis.</p>
<h2>Propriété intellectuelle</h2><p>Les textes, le logo et les éléments graphiques de ce site appartiennent à {E(NOM)}, sauf mention contraire. Les noms des compagnies d'assurance et des marques sont cités à titre informatif et n'impliquent aucun partenariat.</p>
<h2>Médiation de la consommation</h2><p>Conformément à l'article L612-1 du Code de la consommation, vous pouvez recourir gratuitement à un médiateur de la consommation : {mediateur}.</p>
<h2>Prix et devis</h2><p>Les prix affichés sont des prix de départ TTC. Conformément à l'arrêté du 24 janvier 2017 relatif aux prestations de dépannage, de réparation et d'entretien dans le secteur du bâtiment, un devis détaillé gratuit est remis et signé avant toute intervention, et une facture détaillée est remise à la fin.</p>
<h2>Responsabilité</h2><p>Les informations de ce site sont fournies à titre indicatif et peuvent évoluer.</p>''', f'''<h2>Editor de la web</h2><p>{"<br>".join(lignes)}</p>
<h2>Alojamiento</h2><p>Netlify, Inc. – 44 Montgomery Street, Suite 300, San Francisco, CA 94104, Estados Unidos.</p>
<h2>Propiedad intelectual</h2><p>Los textos, el logotipo y los elementos gráficos de esta web pertenecen a {E(NOM)}, salvo que se indique lo contrario. Los nombres de las compañías de seguros y de las marcas se citan solo a título informativo y no implican ningún acuerdo.</p>
<h2>Mediación de consumo</h2><p>De acuerdo con el artículo L612-1 del Código de Consumo francés, puede recurrir gratuitamente a un mediador de consumo: {mediateur}.</p>
<h2>Precios y presupuestos</h2><p>Los precios mostrados son precios de partida con IVA incluido. De acuerdo con la orden francesa del 24 de enero de 2017 sobre las intervenciones de asistencia, reparación y mantenimiento en el sector de la construcción, se entrega un presupuesto detallado y gratuito, firmado antes de cualquier trabajo, y una factura detallada al final.</p>
<h2>Responsabilidad</h2><p>La información de esta web se ofrece a título orientativo y puede cambiar.</p>'''),
           t(f"Legal notice | {NOM}", f"Mentions légales | {NOM}", f"Aviso legal | {NOM}"),
           t(f"Legal notice of the {NOM} website, locksmith in Paris.", f"Mentions légales du site {NOM}, serrurier à Paris.", f"Aviso legal de la web de {NOM}, cerrajero en París."), aside=False)

    simple("/privacy/", t("Privacy", "Confidentialité", "Privacidad"), t("Privacy policy", "Politique de confidentialité", "Política de privacidad"),
           t("How we handle your personal data.", "Comment nous traitons vos données personnelles.", "Cómo tratamos sus datos personales."),
           t(f'''<h2>Data collected</h2><p>When you contact us (phone, WhatsApp, email or form), we only collect what is needed to handle your request: name, phone number, call-out address and description of the problem.</p>
<h2>Purpose</h2><p>This data is used to organize the call-out and to issue the quote and invoice. It is never sold or passed on.</p>
<h2>Form and WhatsApp</h2><p>Requests sent through the form are processed by Netlify Forms (our website host). WhatsApp messages are subject to WhatsApp's (Meta's) terms.</p>
<h2 id="cookies">Cookies and analytics</h2><p>Only with your consent, this website uses <strong>Google Tag Manager</strong> and <strong>Google Analytics</strong> (Google Ireland Ltd) to measure traffic and the use of the call, WhatsApp and form buttons. Without consent, none of these tools is loaded.</p>
<p>Your choice is stored for 6 months in your browser and can be changed at any time with the "Cookies" link at the bottom of each page.</p>
<h2>Retention</h2><p>Billing data is kept for 10 years (legal requirement). Other data is deleted no later than 3 years after the last contact.</p>
<h2>Your rights</h2><p>Under the GDPR, you have the right to access, correct, delete and object to the processing of your data. Write to {CONFIG["email"]}. You may also contact the French data protection authority (CNIL).</p>''',
             f'''<h2>Données collectées</h2><p>Lorsque vous nous contactez (téléphone, WhatsApp, email ou formulaire), nous recueillons uniquement ce qui est nécessaire pour traiter votre demande : nom, numéro de téléphone, adresse d'intervention et description du problème.</p>
<h2>Finalité</h2><p>Ces données servent à organiser l'intervention et à établir le devis et la facture. Elles ne sont jamais vendues ni cédées.</p>
<h2>Formulaire et WhatsApp</h2><p>Les demandes envoyées par le formulaire sont traitées par Netlify Forms (hébergeur du site). Les messages WhatsApp sont soumis aux conditions de WhatsApp (Meta).</p>
<h2 id="cookies">Cookies et mesure d'audience</h2><p>Uniquement avec votre accord, ce site utilise <strong>Google Tag Manager</strong> et <strong>Google Analytics</strong> (Google Ireland Ltd) pour mesurer la fréquentation et l'utilisation des boutons d'appel, WhatsApp et formulaire. Sans accord, aucun de ces outils n'est chargé.</p>
<p>Votre choix est conservé 6 mois dans votre navigateur et peut être modifié à tout moment avec le lien « Cookies » en bas de chaque page.</p>
<h2>Durée de conservation</h2><p>Les données de facturation sont conservées 10 ans (obligation légale). Les autres données sont supprimées au plus tard 3 ans après le dernier contact.</p>
<h2>Vos droits</h2><p>Conformément au RGPD, vous disposez d'un droit d'accès, de rectification, d'effacement et d'opposition au traitement de vos données. Écrivez à {CONFIG["email"]}. Vous pouvez également saisir la CNIL.</p>''', f'''<h2>Datos recogidos</h2><p>Cuando nos contacta (teléfono, WhatsApp, email o formulario), solo recogemos lo necesario para atender su solicitud: nombre, número de teléfono, dirección de la intervención y descripción del problema.</p>
<h2>Finalidad</h2><p>Estos datos sirven para organizar la intervención y para emitir el presupuesto y la factura. Nunca se venden ni se ceden.</p>
<h2>Formulario y WhatsApp</h2><p>Las solicitudes enviadas por el formulario las gestiona Netlify Forms (el alojamiento de nuestra web). Los mensajes de WhatsApp están sujetos a las condiciones de WhatsApp (Meta).</p>
<h2 id="cookies">Cookies y medición de audiencia</h2><p>Solo con su consentimiento, esta web utiliza <strong>Google Tag Manager</strong> y <strong>Google Analytics</strong> (Google Ireland Ltd) para medir las visitas y el uso de los botones de llamada, WhatsApp y formulario. Sin su consentimiento, no se carga ninguna de estas herramientas.</p>
<p>Su elección se guarda durante 6 meses en su navegador y puede cambiarla en cualquier momento con el enlace «Cookies» al pie de cada página.</p>
<h2>Conservación</h2><p>Los datos de facturación se conservan 10 años (obligación legal). Los demás datos se eliminan como máximo 3 años después del último contacto.</p>
<h2>Sus derechos</h2><p>De acuerdo con el RGPD, tiene derecho de acceso, rectificación, supresión y oposición al tratamiento de sus datos. Escriba a {CONFIG["email"]}. También puede dirigirse a la autoridad francesa de protección de datos (CNIL).</p>'''),
           t(f"Privacy policy | {NOM}", f"Politique de confidentialité | {NOM}", f"Política de privacidad | {NOM}"),
           t(f"Privacy policy of the {NOM} website.", f"Politique de confidentialité du site {NOM}.", f"Política de privacidad de la web de {NOM}."), aside=False)


URG_FAQ = [
    ("Do you really come at night and on Sundays?", "Yes, 24/7, public holidays included. The night rate (10pm–8am) is given on the phone before the locksmith sets off."),
    ("How quickly can you get here?", "About 30 minutes on average within Paris. The exact time depends on traffic and is given on the phone."),
    ("How much does an emergency door opening cost?", "€110 incl. VAT on weekdays, €160 in the evening and on weekends, €220 at night for a slammed door. A locked door starts at €180 during the day."),
    ("What should I have ready when the locksmith arrives?", "If possible, an ID or proof of address: the locksmith must make sure you are the occupant. If your documents are inside, a neighbor, the caretaker or your host can vouch for you."),
    ("Can I refuse the quote on site?", "Yes. The quote is free and with no obligation: if you refuse it, nothing is done."),
]


# Guide d'urgence : situation -> prix par tranche horaire (None = sur devis), service lié, conseil
GUIDE = [
    ("slammed", "Door slammed shut, keys inside", "door-opening", (110, 160, 220), False,
     "Don't try a credit card or screwdriver on the latch: you would damage the strike plate. Most slammed doors open in minutes with no damage."),
    ("locked", "Door locked with a key, keys lost", "door-opening", (180, 250, 280), True,
     "Ask the caretaker (gardien) or a neighbor whether they keep a spare. Opening without damage is still possible in many cases."),
    ("jammed", "Lock jammed, key won't turn", "jammed-lock", (180, 250, 280), False,
     "Stop forcing the key: you could snap it inside the cylinder. Don't spray oil into the lock."),
    ("broken", "Key broken in the lock", "broken-key", None, False,
     "Don't push the piece further in and never use glue. If it sticks out, pull it straight out with fine pliers."),
    ("burglary", "Burglary, door forced open", "break-in-repair", None, False,
     "Don't go in if someone may still be inside: call the police (17). Don't touch anything before they come."),
    ("stolen", "Keys stolen, change the cylinder", "lock-replacement", (160, 210, 230), True,
     "If your ID or address was stolen with the keys, have the cylinder changed today."),
    ("smart", "Smart lock not responding", "smart-lock", None, False,
     "Look for your mechanical backup key and check whether the app shows a low battery."),
    ("cellar", "Cellar broken into", "cellar-door", None, False,
     "Tell the building manager (syndic): other cellars may have been hit too."),
]


def guide_block():
    data = {k: {"label": l, "url": svc_url(SVC_BY_SLUG[slug]), "service": SVC_BY_SLUG[slug]["court"], "prices": p, "from": f, "tip": tip}
            for k, l, slug, p, f, tip in GUIDE}

    def gd_img(k, slug):
        if os.path.exists(os.path.join(ROOT, "assets", "img", "urgences", f"{k}.webp")):
            return f'<img class="gd-img" src="/assets/img/urgences/{k}.webp" alt="" width="640" height="360" loading="lazy" decoding="async">'
        return ico(SVC_BY_SLUG[slug]["icon"])
    opts = "".join(f'<button type="button" class="gd-opt" data-sit="{k}" aria-pressed="false">{gd_img(k, slug)}<span>{E(l)}</span></button>'
                   for k, l, slug, *_ in GUIDE)
    slots = "".join(f'<button type="button" class="gd-slot" data-slot="{k}" aria-pressed="{"true" if k == "jour" else "false"}">{ico(i)}<span><b>{l}</b><small data-h="{h}" data-h-we="{SLOTS_WE[k]}">{h}</small></span></button>'
                    for k, i, l, h in SLOTS)
    return f'''<div class="guide" data-guide>
  <div class="gd-step">
    <p class="gd-q"><b>1</b>{t("What happened?", "Que s'est-il passé ?", "¿Qué ha pasado?")}</p>
    <div class="gd-opts">{opts}</div>
  </div>
  <div class="gd-step">
    <p class="gd-q"><b>2</b>{t("When do you need us?", "Quand avez-vous besoin de nous ?", "¿Cuándo nos necesita?")} <small class="gd-auto" hidden></small></p>
    <div class="gd-slots">{slots}</div>
  </div>
  <div class="gd-result" aria-live="polite">
    <div class="gd-empty">{ico("i-arrow")}<span>{t("Choose your situation above to see your price and what to do now.", "Choisissez votre situation ci-dessus pour voir votre prix et quoi faire maintenant.", "Elija su situación arriba para ver su precio y qué hacer ahora.")}</span></div>
    <div class="gd-out" hidden>
      <div class="gd-price"><small data-g="slotlabel"></small><b data-g="price"></b><span data-g="note"></span></div>
      <div class="gd-tip">{ico("i-award")}<p><strong>{t("What to do now:", "Que faire maintenant :", "Qué hacer ahora:")}</strong> <span data-g="tip"></span></p></div>
      <div class="gd-acts">{btn_call(t("Call now · ", "Appeler · ", "Llamar · ") + TEL, cls="btn btn-gold btn-lg", track="call_guide")}<a class="btn btn-wa btn-lg" data-g="wa" href="{E(WA)}" target="_blank" rel="noopener" data-track="wa_guide">{ico("i-wa")}<span>WhatsApp</span></a><a class="btn btn-outline btn-lg" data-g="more" href="/services/">{ico("i-file")}<span>{t("How we handle it", "Notre intervention", "Cómo intervenimos")}</span></a></div>
    </div>
  </div>
  <script type="application/json" id="guide-data">{json.dumps(data, ensure_ascii=False)}</script>
</div>'''


def build_urgence():
    etapes = t([
        ("Stay calm and safe", "If someone may still be inside after a break-in, don't go in and call the police (17)."),
        ("Call us", f"On {TEL}, 24/7. Describe the door and the situation, or send a photo on WhatsApp."),
        ("You get the price", "Before the locksmith sets off, depending on the time of day. It doesn't change on the way."),
        ("Signed quote, then the work", "On site, the price is confirmed in writing. The locksmith only starts once you have signed."),
    ], [
        ("Restez calme et en sécurité", "Si quelqu'un est peut-être encore à l'intérieur après une effraction, n'entrez pas et appelez la police (17)."),
        ("Appelez-nous", f"Au {TEL}, 24h/24. Décrivez la porte et la situation, ou envoyez une photo sur WhatsApp."),
        ("Vous connaissez le prix", "Avant le départ du serrurier, selon l'heure d'intervention. Il ne change pas en route."),
        ("Devis signé, puis intervention", "Sur place, le prix est confirmé par écrit. Le serrurier ne commence qu'une fois le devis signé."),
    ], [
        ("Mantenga la calma y la seguridad", "Si alguien puede seguir dentro tras un robo, no entre y llame a la policía (17)."),
        ("Llámenos", f"Al {TEL}, 24/7. Describa la puerta y la situación, o envíenos una foto por WhatsApp."),
        ("Conoce el precio", "Antes de que salga el cerrajero, según la hora de la intervención. No cambia por el camino."),
        ("Presupuesto firmado y después el trabajo", "En el sitio, el precio se confirma por escrito. El cerrajero solo empieza cuando usted ha firmado."),
    ])
    steps = "".join(f"<li><b>{i}</b><div><h3>{E(h)}</h3><p>{E(d)}</p></div></li>" for i, (h, d) in enumerate(etapes, start=1))
    crumb = t("Emergency 24/7", "Urgence 24h/24", "Urgencias 24/7")
    body = hero([(crumb, None)], t("Emergency locksmith in Paris, <em>24/7</em>", "Serrurier en urgence à Paris, <em>24h/24</em>", "Cerrajero urgente en París, <em>24/7</em>"),
                t("Lockout, broken key, jammed lock, burglary: a locksmith comes right away anywhere in the 20 arrondissements, at night, at weekends and on public holidays. Price given before we travel.",
                  "Porte claquée, clé cassée, serrure bloquée, cambriolage : un serrurier arrive tout de suite dans les 20 arrondissements, la nuit, le week-end et les jours fériés. Prix annoncé avant le déplacement.", "Puerta cerrada de golpe, llave rota, cerradura bloqueada, robo: un cerrajero llega al momento a cualquiera de los 20 distritos, de noche, en fin de semana y en festivos. Precio anunciado antes del desplazamiento."),
                ticks(t(["Arrival ≈ 30 min", "Price given on the phone", "Signed quote before work"], ["Arrivée ≈ 30 min", "Prix annoncé au téléphone", "Devis signé avant intervention"], ["Llegada ≈ 30 min", "Precio anunciado por teléfono", "Presupuesto firmado antes del trabajo"]), "ticks light inline"),
                kicker=t("Immediate call-out", "Intervention immédiate", "Intervención inmediata"), bg="tour-eiffel")
    body += f'''<section class="sec"><div class="wrap">
  <div class="sec-head split"><div><span class="eyebrow">{t("Your price in 2 clicks", "Votre prix en 2 clics", "Su precio en 2 clics")}</span><h2>{t("What is your emergency?", "Quelle est votre urgence ?", "¿Cuál es su urgencia?")}</h2></div>
  <p>{t("Answer two questions: you get the price that applies right now and what to do while you wait. Then call us, or leave your number and we call you back.", "Répondez à deux questions : vous obtenez le prix qui s'applique maintenant et quoi faire en attendant. Appelez-nous ensuite, ou laissez votre numéro et nous vous rappelons.", "Responda a dos preguntas: obtendrá el precio que se aplica ahora mismo y qué hacer mientras espera. Después llámenos, o deje su número y le devolvemos la llamada.")}</p></div>
  {guide_block()}
</div></section>
<section class="sec soft"><div class="wrap layout"><article class="prose">
  <h2>{t("What to do in an emergency", "Que faire en cas d'urgence", "Qué hacer en caso de urgencia")}</h2>
  <ol class="urg-steps">{steps}</ol>
  <h2>{t("Our emergency prices", "Nos tarifs d'urgence", "Nuestros precios de urgencia")}</h2>
  <p>{t("Our prices depend on the time of day: day (weekdays 8am–6pm), evening (weekdays 6pm–10pm) and night (10pm–8am). On Saturdays, Sundays and public holidays there is no daytime rate: the evening rate applies from 8am to 10pm. The current time slot is selected automatically.", "Nos prix dépendent de l'heure : journée (en semaine 8h–18h), soirée (en semaine 18h–22h) et nuit (22h–8h). Le samedi, le dimanche et les jours fériés, il n'y a pas de tarif de journée : le tarif de soirée s'applique de 8h à 22h. La tranche horaire actuelle est sélectionnée automatiquement.", "Nuestros precios dependen de la hora: día (entre semana 8:00–18:00), tarde (entre semana 18:00–22:00) y noche (22:00–8:00). Los sábados, domingos y festivos no hay tarifa de día: se aplica la tarifa de tarde de 8:00 a 22:00. La franja horaria actual se selecciona automáticamente.")}</p>
</article>{side_box(t("Emergency: call now", "Urgence : appelez maintenant", "Urgencia: llame ahora"), t("A locksmith answers directly and gives you the price before setting off.", "Un serrurier vous répond directement et vous annonce le prix avant de partir.", "Un cerrajero le atiende directamente y le da el precio antes de salir."))}</div>
<div class="wrap" style="margin-top:28px">{tarif_table()}</div></section>
<section class="sec"><div class="wrap faq-wrap"><div class="sec-head"><span class="eyebrow">{t("Questions", "Questions", "Preguntas")}</span><h2>{t("Emergencies: your questions", "Urgences : vos questions", "Urgencias: sus preguntas")}</h2></div>{faq_html(URG_FAQ)}</div></section>'''
    body += assureurs_strip() + contact_band(t("Locked out? Call us.", "Porte claquée ? Appelez-nous.", "¿Se ha quedado fuera? Llámenos."),
                                             t("A locksmith answers right away and gives you the price before travelling.", "Un serrurier vous répond tout de suite et vous annonce le prix avant de se déplacer.", "Un cerrajero le atiende al momento y le da el precio antes de desplazarse."),
                                             source="/emergency/")
    page("/emergency/", t(f"Emergency locksmith Paris 24/7 – {TEL} | {NOM}", f"Serrurier urgence Paris 24h/24 – {TEL} | {NOM}", f"Cerrajero urgente París 24/7 – {TEL} | {NOM}"),
         t(f"Emergency locksmith in Paris, 24/7: lockouts from €110 incl. VAT, broken keys, jammed locks, burglaries. Arrival in about 30 min, price given before we travel. English spoken. ☎ {TEL}",
           f"Serrurier en urgence à Paris, 24h/24 : porte claquée dès 110 € TTC, clé cassée, serrure bloquée, cambriolage. Arrivée en 30 min environ, prix annoncé avant le déplacement. ☎ {TEL}", f"Cerrajero urgente en París, 24/7: puerta cerrada de golpe desde 110 € IVA incl., llave rota, cerradura bloqueada, robo. Llegada en unos 30 min, precio anunciado antes del desplazamiento. ☎ {TEL}"),
         body, [ld_business(full=True), ld_crumbs([(crumb, "/emergency/")]), ld_faq(URG_FAQ)], active="/emergency/")


def build_charte():
    items = "".join(f'<div class="charte-item">{ico(i)}<div><h2>{E(h)}</h2><p>{E(d)}</p></div></div>' for i, h, d in CHARTE)
    crumb = t("Our commitments", "Nos engagements", "Nuestros compromisos")
    body = hero([(crumb, None)], t("Our trust charter", "Notre charte de confiance", "Nuestra carta de confianza"),
                t("Eight concrete commitments, applied to every job, day and night. Feel free to remind us of them at any time.",
                  "Huit engagements concrets, appliqués à chaque intervention, de jour comme de nuit. N'hésitez pas à nous les rappeler à tout moment.", "Ocho compromisos concretos, aplicados en cada intervención, de día y de noche. No dude en recordárnoslos en cualquier momento."),
                kicker=t("Transparency", "Transparence", "Transparencia"))
    body += f'''<section class="sec"><div class="wrap layout"><article class="prose">
  <p class="intro">{t(f"Emergency locksmiths suffer from a bad reputation: misleading teaser prices, inflated invoices, locks replaced for no reason. We built {E(NOM)} on the opposite principle. Here is exactly what we commit to, for every customer.", f"Le dépannage en serrurerie souffre d'une mauvaise réputation : prix d'appel trompeurs, factures gonflées, serrures changées sans raison. Nous avons construit {E(NOM)} sur le principe inverse. Voici précisément ce à quoi nous nous engageons, pour chaque client.", f"La cerrajería de urgencia arrastra mala fama: precios de reclamo engañosos, facturas infladas, cerraduras cambiadas sin motivo. Hemos construido {E(NOM)} sobre el principio contrario. Esto es exactamente a lo que nos comprometemos con cada cliente.")}</p>
  <div class="charte">{items}</div>
  <h2>{t("What you will never see from us", "Ce que vous ne verrez jamais chez nous", "Lo que nunca verá con nosotros")}</h2>
  {comparatif_block()}
  <h2>{t("Your rights with a locksmith in France", "Vos droits face à un serrurier", "Sus derechos ante un cerrajero en Francia")}</h2>
  <p>{t('For a home call-out, the professional must inform you of their prices and give you a detailed quote before the work (decree of 24 January 2017). You can refuse the quote. At the end, a detailed invoice must be given to you. In the event of a dispute, you can contact the consumer mediator named in our <a href="/legal-notice/">legal notice</a> free of charge, or report a practice on the government\'s SignalConso website.', 'Pour un dépannage à domicile, le professionnel doit vous informer de ses tarifs et vous remettre un devis détaillé avant l\'intervention (arrêté du 24 janvier 2017). Vous pouvez refuser le devis. À la fin, une facture détaillée doit vous être remise. En cas de litige, vous pouvez saisir gratuitement le médiateur de la consommation indiqué dans nos <a href="/legal-notice/">mentions légales</a>, ou signaler une pratique sur le site SignalConso.', 'Para una intervención a domicilio, el profesional debe informarle de sus precios y entregarle un presupuesto detallado antes del trabajo (orden del 24 de enero de 2017). Puede rechazar el presupuesto. Al final, se le debe entregar una factura detallada. En caso de litigio, puede recurrir gratuitamente al mediador de consumo indicado en nuestro <a href="/legal-notice/">aviso legal</a>, o denunciar una práctica en la web oficial SignalConso.')}</p>
  <h2>{t("Check for yourself", "Vérifiez par vous-même", "Compruébelo usted mismo")}</h2>
  <p>{t(f'Before calling us, read <a href="{E(MAPS)}" target="_blank" rel="noopener">our {CONFIG["avis_nombre"]} Google reviews</a>, our <a href="/prices/">price list</a> and our <a href="/legal-notice/">legal information</a>. And if any point of this charter were not respected, tell us: it\'s the only way to stay up to standard.', f'Avant de nous appeler, lisez <a href="{E(MAPS)}" target="_blank" rel="noopener">nos {CONFIG["avis_nombre"]} avis Google</a>, notre <a href="/prices/">grille tarifaire</a> et nos <a href="/legal-notice/">informations légales</a>. Et si un point de cette charte n\'était pas respecté, dites-le-nous : c\'est la seule façon de rester à la hauteur.', f'Antes de llamarnos, lea <a href="{E(MAPS)}" target="_blank" rel="noopener">nuestras {CONFIG["avis_nombre"]} opiniones en Google</a>, nuestra <a href="/prices/">lista de precios</a> y nuestra <a href="/legal-notice/">información legal</a>. Y si algún punto de esta carta no se respetara, díganoslo: es la única manera de estar a la altura.')}</p>
</article>{side_box(t("A clear price from the first call", "Un prix clair dès le premier appel", "Un precio claro desde la primera llamada"), t("Describe your situation: you get the price before anyone travels.", "Décrivez votre situation : vous connaissez le prix avant tout déplacement.", "Describa su situación: conocerá el precio antes de cualquier desplazamiento."))}</div></section>'''
    body += reviews_block() + contact_band(source="/our-commitments/")
    page("/our-commitments/", t(f"Our commitments: trust charter | {NOM}", f"Nos engagements : charte de confiance | {NOM}", f"Nuestros compromisos: carta de confianza | {NOM}"),
         t("Price given before we travel, signed quote before any work, no unnecessary damage, detailed invoice: the trust charter of our Paris locksmith company.",
           "Prix annoncé avant le déplacement, devis signé avant toute intervention, pas de casse inutile, facture détaillée : la charte de confiance de notre entreprise de serrurerie parisienne.", "Precio anunciado antes del desplazamiento, presupuesto firmado antes de cualquier trabajo, ningún daño innecesario, factura detallada: la carta de confianza de nuestra empresa de cerrajería parisina."),
         body, [ld_business(), ld_crumbs([(crumb, "/our-commitments/")])], active="/our-commitments/")


def build_conseils():
    crumb = t("Advice", "Conseils", "Consejos")
    body = hero([(crumb, None)], t("Locksmith advice <em>for Paris residents and visitors</em>", "Conseils de serrurier <em>pour les Parisiens et les visiteurs</em>", "Consejos de cerrajero <em>para residentes y visitantes de París</em>"),
                t("Practical guides to react in an emergency, secure your home and avoid nasty surprises.",
                  "Des guides pratiques pour réagir en cas d'urgence, sécuriser votre logement et éviter les mauvaises surprises.", "Guías prácticas para reaccionar ante una urgencia, proteger su vivienda y evitar sorpresas desagradables."))
    body += f'<section class="sec"><div class="wrap">{articles_cards(ARTICLES)}</div></section>' + contact_band(source="/advice/")
    page("/advice/", t(f"Locksmith & security advice in Paris | {NOM}", f"Conseils serrurerie et sécurité à Paris | {NOM}", f"Consejos de cerrajería y seguridad en París | {NOM}"),
         t("Lost keys, armored doors in Parisian buildings, locksmith scams, after a burglary: our practical guides.",
           "Clés perdues, porte blindée en immeuble parisien, arnaques au serrurier, après un cambriolage : nos guides pratiques.", "Llaves perdidas, puertas blindadas en edificios parisinos, estafas de cerrajeros, qué hacer tras un robo: nuestras guías prácticas."),
         body, [ld_business(), ld_crumbs([(crumb, "/advice/")])], active="/advice/")
    for a in ARTICLES:
        path = f"/advice/{a['slug']}/"
        parts = []
        for kind, val in a["corps"]:
            if kind in ("ul", "ol"):
                parts.append(f"<{kind}>" + "".join(f"<li>{v}</li>" for v in val) + f"</{kind}>")
            else:
                parts.append(f"<{kind}>{val}</{kind}>")
        prose = "".join(parts) + (f'<div class="note-box">{ico("i-phone")}<p>' + t(
            f'<strong>Need a locksmith now?</strong> {E(NOM)} works 24/7 across Paris. Call <a href="{TEL_HREF}">{TEL}</a>: the price is given on the phone. See also our <a href="/services/">services</a> and <a href="/prices/">prices</a>.',
            f'<strong>Besoin d\'un serrurier maintenant ?</strong> {E(NOM)} intervient 24h/24 dans tout Paris. Appelez le <a href="{TEL_HREF}">{TEL}</a> : le prix est annoncé au téléphone. Voir aussi nos <a href="/services/">services</a> et nos <a href="/prices/">tarifs</a>.', f'<strong>¿Necesita un cerrajero ahora?</strong> {E(NOM)} trabaja 24/7 en todo París. Llame al <a href="{TEL_HREF}">{TEL}</a>: el precio se anuncia por teléfono. Vea también nuestros <a href="/services/">servicios</a> y nuestros <a href="/prices/">precios</a>.')
            + '</p></div>')
        rel = articles_cards([o for o in ARTICLES if o is not a][:3])
        body = hero([(crumb, "/advice/"), (a["court"], None)], E(a["titre"]), E(a["desc"]),
                    f'<p class="post-by">{E(a["cat"])} · {fr_date(a["date"])} · {t("by the", "par l\'équipe", "por el equipo de")} {E(NOM)}{t(" team", "", "")}</p>')
        body += f'<section class="sec"><div class="wrap layout"><article class="prose">{prose}</article>{side_box()}</div></section>'
        body += f'<section class="sec cream"><div class="wrap"><div class="sec-head"><h2>{t("Read next", "À lire aussi", "Para seguir leyendo")}</h2></div>{rel}</div></section>' + contact_band(source=path)
        ld = [ld_business(), ld_crumbs([(crumb, "/advice/"), (a["court"], path)]),
              {"@context": "https://schema.org", "@type": "BlogPosting", "headline": a["titre"], "description": a["desc"],
               "datePublished": a["date"], "dateModified": a["date"], "inLanguage": LANG, "mainEntityOfPage": URL + path,
               "author": {"@type": "Organization", "name": NOM, "url": URL + "/"}, "publisher": {"@id": BID}, "image": URL + "/assets/img/og.jpg"}]
        page(path, f'{a["titre"]} | {NOM}', a["desc"], body, ld, active="/advice/", og_type="article")


def build_misc():
    conv = CONFIG["ads_conv"].get("form")
    home = t("Back to home", "Retour à l'accueil", "Volver al inicio")
    body = f'''<section class="phero center-page"><div class="wrap">
  <span class="big-ic">{ico("i-check")}</span>
  <h1>{t("Thank you, your request has been sent", "Merci, votre demande a bien été envoyée", "Gracias, su solicitud se ha enviado")}</h1>
  <p class="lead">{t("We will call you back very soon. For an emergency (lockout, break-in), call us directly: it's the fastest way.", "Nous vous rappelons très vite. En cas d'urgence (porte claquée, effraction), appelez-nous directement : c'est le plus rapide.", "Le llamamos muy pronto. En caso de urgencia (puerta cerrada de golpe, robo), llámenos directamente: es lo más rápido.")}</p>
  <div class="cta-row center">{btn_call(cls="btn btn-gold btn-lg", track="call_merci")}<a class="btn btn-outline-light btn-lg" href="/">{home}</a></div>
</div></section>'''
    if CONFIG["ads_id"] and conv:
        body += f"<script>gtag('event','conversion',{{'send_to':'{CONFIG['ads_id']}/{conv}','value':1.0,'currency':'EUR'}});</script>"
    # Envoi sans JavaScript (page rechargée) : même événement que main.js, capté par GTM
    body += "<script>window.dataLayer=window.dataLayer||[];dataLayer.push({event:'envoi_formulaire',emplacement:'merci'});</script>"
    page("/thank-you/", t(f"Request sent | {NOM}", f"Demande envoyée | {NOM}", f"Solicitud enviada | {NOM}"), t("Your request has been sent.", "Votre demande a bien été envoyée.", "Su solicitud se ha enviado."), body, robots="noindex, nofollow")

    body = f'''<section class="phero center-page"><div class="wrap">
  <p class="err">404</p>
  <h1>{t("Page not found", "Page introuvable", "Página no encontrada")}</h1>
  <p class="lead">{t("It may have moved. Need a locksmith? We are available 24/7.", "Elle a peut-être été déplacée. Besoin d'un serrurier ? Nous sommes disponibles 24h/24.", "Puede que se haya movido. ¿Necesita un cerrajero? Estamos disponibles 24/7.")}</p>
  <div class="cta-row center">{btn_call(cls="btn btn-gold btn-lg", track="call_404")}<a class="btn btn-outline-light btn-lg" href="/">{home}</a></div>
</div></section>'''
    page("/404.html", t(f"Page not found | {NOM}", f"Page introuvable | {NOM}", f"Página no encontrada | {NOM}"), t("This page doesn't exist.", "Cette page n'existe pas.", "Esta página no existe."), body, robots="noindex, follow")

    serrurier = t("Locksmith", "Serrurier", "Cerrajero")
    groups = [(t("Main pages", "Pages principales", "Páginas principales"), t(
                  [("Home", "/"), ("Emergency 24/7", "/emergency/"), ("Services", "/services/"), ("Arrondissements", "/locksmith-paris/"), ("Prices", "/prices/"),
                   ("Our commitments", "/our-commitments/"), ("Insurance", "/insurance/"), ("Customer reviews", "/reviews/"), ("FAQ", "/faq/"),
                   ("Advice", "/advice/"), ("Contact", "/contact/")],
                  [("Accueil", "/"), ("Urgence 24h/24", "/emergency/"), ("Services", "/services/"), ("Arrondissements", "/locksmith-paris/"), ("Tarifs", "/prices/"),
                   ("Nos engagements", "/our-commitments/"), ("Assurance", "/insurance/"), ("Avis clients", "/reviews/"), ("Questions fréquentes", "/faq/"),
                   ("Conseils", "/advice/"), ("Contact", "/contact/")], [("Inicio", "/"), ("Urgencias 24/7", "/emergency/"), ("Servicios", "/services/"), ("Distritos", "/locksmith-paris/"), ("Precios", "/prices/"),
                   ("Nuestros compromisos", "/our-commitments/"), ("Seguro", "/insurance/"), ("Opiniones de clientes", "/reviews/"), ("Preguntas frecuentes", "/faq/"),
                   ("Consejos", "/advice/"), ("Contacto", "/contact/")])),
              (t("Services", "Services", "Servicios"), [(s["nom"], svc_url(s)) for s in SERVICES]),
              (t("Arrondissements", "Arrondissements", "Distritos"), [(f"{serrurier} {z['court']}", z["url"]) for z in ARR]),
              (t("Advice", "Conseils", "Consejos"), [(a["court"], f"/advice/{a['slug']}/") for a in ARTICLES])]
    prose = "".join(f'<h2>{E(g)}</h2><div class="chips">' + "".join(f'<a class="chip" href="{u}">{E(l)}</a>' for l, u in lst) + "</div>" for g, lst in groups)
    chips = {"en": '<a class="chip" href="%%EN_SITEMAP%%" hreflang="en" lang="en">Site map in English</a>',
             "fr": '<a class="chip" href="/fr/plan-du-site/" hreflang="fr" lang="fr">Plan du site en français</a>',
             "es": '<a class="chip" href="/es/mapa-del-sitio/" hreflang="es" lang="es">Mapa del sitio en español</a>'}
    other = (f'<h2>{t("Other languages", "Autres langues", "Otros idiomas")}</h2><div class="chips">'
             + "".join(c for l, c in chips.items() if l != LANG) + "</div>")
    simple("/site-map/", t("Site map", "Plan du site", "Mapa del sitio"), t("Site map", "Plan du site", "Mapa del sitio"), t(f"Every page of the {NOM} website.", f"Toutes les pages du site {NOM}.", f"Todas las páginas de la web de {NOM}."), prose + other,
           t(f"Site map | {NOM}", f"Plan du site | {NOM}", f"Mapa del sitio | {NOM}"), t(f"Site map of {NOM}: services, arrondissements, advice.", f"Plan du site {NOM} : services, arrondissements, conseils.", f"Mapa del sitio de {NOM}: servicios, distritos, consejos."), aside=False)


# ---------------------------------------------------------------------------
# SEO files and redirects
# ---------------------------------------------------------------------------
def write(name, content):
    with open(os.path.join(ROOT, name), "w", encoding="utf-8") as f:
        f.write(content)


# Ancien site en français (adresses à la racine) : correspondance avec les pages anglaises
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


# Adresses de la version française : page anglaise -> page française
def build_fr_paths():
    m = {"/": "/fr/", "/services/": "/fr/services/", "/contact/": "/fr/contact/", "/404.html": "/fr/404.html"}
    m.update({en: "/fr" + fr for fr, en in FR_PAGES.items() if fr.endswith("/")})
    m.update({f"/services/{en}/": f"/fr/services/{fr}/" for fr, en in FR_SVC.items()})
    m.update({z["url"]: f"/fr/{z['fr_slug']}/" for z in build_arr()})
    return m


FR_PATHS = build_fr_paths()

# Version espagnole : page anglaise -> page espagnole
ES_SVC = {"door-opening": "apertura-de-puertas", "jammed-lock": "cerradura-bloqueada", "broken-key": "llave-rota",
          "lock-replacement": "cambio-de-cerradura", "smart-lock": "cerradura-inteligente", "break-in-repair": "reparacion-tras-robo",
          "door-armoring": "blindaje-de-puertas", "armored-door": "puerta-blindada", "cellar-door": "puerta-de-trastero", "mailbox-lock": "cerradura-de-buzon"}
ES_PAGES = {"/": "/es/", "/emergency/": "/es/urgencias/", "/services/": "/es/servicios/", "/prices/": "/es/precios/",
            "/insurance/": "/es/seguro/", "/reviews/": "/es/opiniones/", "/faq/": "/es/preguntas-frecuentes/",
            "/our-commitments/": "/es/nuestros-compromisos/", "/advice/": "/es/consejos/", "/contact/": "/es/contacto/",
            "/legal-notice/": "/es/aviso-legal/", "/privacy/": "/es/privacidad/", "/thank-you/": "/es/gracias/",
            "/site-map/": "/es/mapa-del-sitio/", "/locksmith-paris/": "/es/cerrajero-paris/", "/404.html": "/es/404.html",
            "/advice/lost-keys-paris/": "/es/consejos/llaves-perdidas-paris/",
            "/advice/armored-door-paris-apartment/": "/es/consejos/puerta-blindada-piso-paris/",
            "/advice/spot-an-honest-locksmith/": "/es/consejos/reconocer-cerrajero-honrado/",
            "/advice/after-a-burglary/": "/es/consejos/despues-de-un-robo/"}


def build_es_paths():
    m = dict(ES_PAGES)
    m.update({f"/services/{en}/": f"/es/servicios/{es}/" for en, es in ES_SVC.items()})
    m.update({z["url"]: f"/es/{z['es_slug']}/" for z in build_arr()})
    return m


ES_PATHS = build_es_paths()
LANG_PATHS = {"fr": FR_PATHS, "es": ES_PATHS}
OG_LOCALES = {"en": "en_GB", "fr": "fr_FR", "es": "es_ES"}

# Contenu qui change avec la langue (data.py / data_fr.py / data_es.py et constantes de ce fichier)
LANG_KEYS = ["SERVICES", "URGENCES", "ARRONDISSEMENTS", "TARIFS", "MARQUES", "ARTICLES", "COMPARATIF", "CHARTE", "INCLUS", "VIDEOS",
             "WA_MSG", "NAV", "SLOTS", "SLOTS_WE", "WEEKEND_NOTE", "PARIS_BG", "HOME_FAQ", "MOIS", "ARR_INTROS", "URG_FAQ", "GUIDE", "SVC_LOCAL"]
_EN_STATE = {}


def set_lang(lang):
    global LANG, SERVICES, SVC_URG, SVC_TRAV, SVC_BY_SLUG, ARR
    g = globals()
    if not _EN_STATE:
        _EN_STATE.update({k: g[k] for k in LANG_KEYS})
    g.update(_EN_STATE if lang == "en" else {k: getattr(DATA_FR if lang == "fr" else DATA_ES, k) for k in LANG_KEYS})
    LANG = lang
    SERVICES = sort_services(SERVICES)
    SVC_URG = [s for s in SERVICES if s["cat"] == "urgence"]
    SVC_TRAV = [s for s in SERVICES if s["cat"] != "urgence"]
    SVC_BY_SLUG = {s["slug"]: s for s in SERVICES}
    ARR = build_arr(ARRONDISSEMENTS, lang)
    _BG_N[0] = 0


def build_redirects():
    # Anciennes adresses françaises (à la racine) -> nouvelle version française dans /fr/
    rules = [(fr, FR_PATHS.get(en, en)) for fr, en in FR_PAGES.items()]
    # anciennes pages anglaise et espagnole de l'ancien site -> versions anglaise et espagnole
    rules = [(old, {"/cerrajero-paris": "/es/", "/english-locksmith-paris": "/"}.get(old, new)) for old, new in rules]
    rules += [(f"/services/{fr}/", f"/fr/services/{fr}/") for fr in FR_SVC]
    for z in ARR:
        fr_z = f"/fr/{z['fr_slug']}/"
        rules.append((f"/{z['fr_slug']}/", fr_z))
        rules += [(f"/{z['fr_slug']}/{fr}/", f"{fr_z}#{en}") for fr, en in FR_SVC.items()]
        # anciennes pages anglaises « service × arrondissement », fusionnées dans la page de l'arrondissement
        rules += [(combo_url(s, z), f"{z['url']}#{s['slug']}") for s in SERVICES]
    lines = []
    for old, new in rules:
        lines.append(f"{old}  {new}  301")
        if old.endswith("/"):
            lines.append(f"{old.rstrip('/')}  {new}  301")
    write("_redirects", "# Anciennes adresses françaises → version française (/fr/) ; anciennes pages service × arrondissement → page de l'arrondissement\n"
          + "\n".join(lines) + "\n# Pages 404 en français et en espagnol\n/fr/*  /fr/404.html  404\n/es/*  /es/404.html  404\n")
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

    # Chaque page existe en anglais, en français et en espagnol : les adresses sont listées avec leurs équivalents (hreflang)
    urls = ""
    for p in SITEMAP:
        links = alt_links(p)
        alt = "".join(f'    <xhtml:link rel="alternate" hreflang="{l}" href="{URL}{u}"/>\n' for l, u in links)
        for u in [u for l, u in links if l != "x-default"] or [p]:
            urls += f"  <url>\n    <loc>{URL}{u}</loc>\n{alt}    <lastmod>{TODAY}</lastmod>\n    <priority>{prio(p)}</priority>\n  </url>\n"
    write("sitemap.xml", '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" '
          'xmlns:xhtml="http://www.w3.org/1999/xhtml">\n' + urls + "</urlset>\n")
    write("robots.txt", f"User-agent: *\nAllow: /\nDisallow: /_src/\nDisallow: /thank-you/\nDisallow: /fr/merci/\nDisallow: /es/gracias/\n\nSitemap: {URL}/sitemap.xml\n")

    svc = "\n".join(f"- [{s['nom']}]({URL}{svc_url(s)}): {s['prix']}. {s['resume']}" for s in SERVICES)
    grille = "\n".join(f"- {r[0]}: " + " / ".join(v or "quote" for v in r[1:]) for r in TARIFS)
    arr = "\n".join(f"- [Locksmith {z['court']}]({URL}{z['url']}) – {z['cp'][0]}" for z in ARR)
    fr_pages = "\n".join(f"- [{l}]({URL}{FR_PATHS[p]})" for l, p in [
        ("Accueil", "/"), ("Urgence 24h/24", "/emergency/"), ("Services", "/services/"), ("Tarifs", "/prices/"),
        ("Arrondissements", "/locksmith-paris/"), ("Nos engagements", "/our-commitments/"), ("Contact", "/contact/")])
    es_pages = "\n".join(f"- [{l}]({URL}{ES_PATHS[p]})" for l, p in [
        ("Inicio", "/"), ("Urgencias 24/7", "/emergency/"), ("Servicios", "/services/"), ("Precios", "/prices/"),
        ("Distritos", "/locksmith-paris/"), ("Nuestros compromisos", "/our-commitments/"), ("Contacto", "/contact/")])
    note = f"- Google rating: {CONFIG['avis_note']}/5 ({CONFIG['avis_nombre']} reviews)\n" if CONFIG["avis_note"] else ""
    write("llms.txt", f"""# {NOM}

> English-speaking locksmith in Paris (75), across all 20 arrondissements, 24/7. Slammed door opening from €110 incl. VAT, price given on the phone before travelling, written quote signed before any work, invoice accepted by French home insurers.

## Information
- Name: {NOM} ({CONFIG['raison_sociale']})
- Phone: {TEL}, 24/7
- WhatsApp: {WA}
- Email: {CONFIG['email']}
- Website: {URL}/ (English), {URL}/fr/ (French) and {URL}/es/ (Spanish)
- Area: Paris only, 1st to 20th arrondissement
- Average arrival: about 30 minutes
- Languages: English, French
- Payment: card, cash, bank transfer
{note}
## Services
{svc}

## Prices incl. VAT (day: weekdays 8am–6pm / evening: weekdays 6pm–10pm, weekends and public holidays 8am–10pm / night 10pm–8am)
{grille}

## Arrondissements
{arr}

Each arrondissement page lists every service with its price and local details (e.g. {URL}{ARR[14]["url"]}#door-opening).

## Version française (French version)
Every page also exists in French, under /fr/ (e.g. {URL}{FR_PATHS[ARR[14]["url"]]}).
{fr_pages}

## Versión en español (Spanish version)
Every page also exists in Spanish, under /es/ (e.g. {URL}{ES_PATHS[ARR[14]["url"]]}).
{es_pages}
""")
    write("site.webmanifest", json.dumps({
        "name": f"{NOM} – 24/7 locksmith", "short_name": "Secure Locksmith", "lang": "en", "start_url": "/",
        "display": "standalone", "background_color": "#151335", "theme_color": "#151335",
        "icons": [{"src": "/assets/img/logo-240.png", "sizes": "240x240", "type": "image/png"},
                  {"src": "/assets/img/icon-512.png", "sizes": "512x512", "type": "image/png"}]}, ensure_ascii=False, indent=2))


def main():
    for lang in ("en", "fr", "es"):
        set_lang(lang)
        build_home()
        build_services()
        build_arr_pages()
        build_static()
        build_urgence()
        build_charte()
        build_conseils()
        build_misc()
    set_lang("en")
    build_seo()
    n = build_redirects()
    print(f"{len(SITEMAP)} pages indexables générées par langue (anglais, français, espagnol), {n} redirections.")


if __name__ == "__main__":
    main()
