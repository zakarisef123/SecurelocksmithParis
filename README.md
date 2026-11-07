# Secure Locksmith Paris – site web (en anglais)

Site statique du serrurier **Secure Locksmith Paris** (Paris 75, 20 arrondissements), entièrement en anglais, généré par un script Python sans dépendance.

## Modifier le site
- **Textes, services, tarifs, arrondissements, articles** : `_src/data.py`
- **Téléphone, e-mail, domaine, Google (GTM / Analytics / Ads), informations légales** : bloc `CONFIG` en haut de `_src/build.py`
- **Couleurs et mise en page** : `assets/css/main.css`

Puis régénérer :

```bash
python3 _src/build.py
```

Sur Netlify, la génération est faite automatiquement à chaque déploiement (`netlify.toml`).

## Pages générées
- Accueil, `/emergency/`, `/services/` (10 services), `/prices/`, `/our-commitments/`, `/insurance/`, `/reviews/`, `/faq/`, `/contact/`, `/advice/`, `/legal-notice/`, `/privacy/`, `/site-map/`
- 20 pages arrondissement (`/locksmith-paris-15th/`…) et 200 pages service × arrondissement (`/locksmith-paris-15th/door-opening/`…)
- `sitemap.xml`, `robots.txt`, `llms.txt`
- `_redirects` : redirections 301 de toutes les anciennes adresses françaises vers les nouvelles

## Photos
Déposez les vraies photos dans `assets/img/photos/` (JPG ou WebP, ~1600 px) avec ces noms : `home.jpg` (accueil), `team.jpg`, et une par service : `door-opening`, `jammed-lock`, `broken-key`, `lock-replacement`, `smart-lock`, `break-in-repair`, `door-armoring`, `armored-door`, `cellar-door`, `mailbox-lock`.

## Avis
Copiez de vrais avis Google dans la liste `AVIS` de `_src/data.py` (jamais d'avis inventés).

## À compléter avant la mise en ligne
Dans `CONFIG` : `siren`, `siret`, `mediateur`.
