# Secure Locksmith Paris – site web (anglais, français et espagnol)

Site statique du serrurier **Secure Locksmith Paris** (Paris 75, 20 arrondissements), en **anglais** (à la racine : `/`, `/emergency/`…), en **français** (dans `/fr/` : `/fr/`, `/fr/urgence/`…) et en **espagnol** (dans `/es/` : `/es/`, `/es/urgencias/`…), généré par un script Python sans dépendance. Un sélecteur EN / FR / ES en haut et en bas de chaque page mène à la même page dans les autres langues.

## Modifier le site
- **Textes, services, tarifs, arrondissements, articles** : `_src/data.py` (anglais), `_src/data_fr.py` (français) et `_src/data_es.py` (espagnol) : pensez à modifier les trois
- **Textes des pages** (titres, boutons, paragraphes) : dans `_src/build.py`, chaque texte est écrit `t("anglais", "français", "espagnol")`
- **Téléphone, e-mail, domaine, Google (GTM / Analytics / Ads), informations légales** : bloc `CONFIG` en haut de `_src/build.py`
- **Couleurs et mise en page** : `assets/css/main.css`

Puis régénérer :

```bash
python3 _src/build.py
```

Sur Netlify, la génération est faite automatiquement à chaque déploiement (`netlify.toml`).

## Référencement des trois langues
- Chaque page indique ses équivalents dans les autres langues (`hreflang` en, fr, es et x-default = anglais), dans la page et dans `sitemap.xml`.
- `<html lang>`, `og:locale`, titres, descriptions et données structurées sont dans la langue de la page.
- Les anciennes adresses françaises (`/urgence/`, `/serrurier-paris-15e/`…) redirigent (301) vers la version française (`/fr/urgence/`, `/fr/serrurier-paris-15e/`), et l'ancienne page `/cerrajero-paris` vers la version espagnole (`/es/`).

## Pages générées
- Accueil, `/emergency/`, `/services/` (10 services), `/prices/`, `/our-commitments/`, `/insurance/`, `/reviews/`, `/faq/`, `/contact/`, `/advice/`, `/legal-notice/`, `/privacy/`, `/site-map/`
- 20 pages arrondissement enrichies (`/locksmith-paris-15th/`), chaque service y a sa section (`/locksmith-paris-15th/#door-opening`)
- `sitemap.xml`, `robots.txt`, `llms.txt`
- Les mêmes pages en français dans `/fr/` (`/fr/urgence/`, `/fr/services/ouverture-de-porte/`, `/fr/serrurier-paris-15e/`, `/fr/tarifs/`…)
- Les mêmes pages en espagnol dans `/es/` (`/es/urgencias/`, `/es/servicios/apertura-de-puertas/`, `/es/cerrajero-paris-15/`, `/es/precios/`…)
- `_redirects` : redirections 301 des anciennes adresses françaises vers `/fr/` et des anciennes pages service × arrondissement ; pages 404 française pour `/fr/` et espagnole pour `/es/`

## Photos
Déposez les vraies photos dans `assets/img/photos/` (JPG ou WebP, ~1600 px) avec ces noms : `home.jpg` (accueil), `team.jpg`, et une par service : `door-opening`, `jammed-lock`, `broken-key`, `lock-replacement`, `smart-lock`, `break-in-repair`, `door-armoring`, `armored-door`, `cellar-door`, `mailbox-lock`.
Après avoir changé une photo de service, lancez `python3 _src/make_thumbs.py` (Pillow requis) : il recrée les vignettes légères de `assets/img/thumbs/`, utilisées sur l'accueil, la page Services, les liens « autres services » et le guide d'urgence.

## Avant / après et interventions récentes
- **Avant / après** (pages services) : déposez les photos dans `assets/img/realisations/` et déclarez-les dans `REALISATIONS` de `_src/data.py`. Le bloc n'apparaît que s'il y a de vraies photos.
- **Interventions récentes** (pages arrondissement) : liste `INTERVENTIONS` de `_src/data.py`, sans nom de client.

## Avis
Copiez de vrais avis Google dans la liste `AVIS` de `_src/data.py` (jamais d'avis inventés).

## À compléter avant la mise en ligne
Dans `CONFIG` : `siren`, `siret`, `mediateur`.
