# Secure Locksmith Paris – site web

Site statique du serrurier **Secure Locksmith Paris** (Paris 75, 20 arrondissements), généré par un script Python sans dépendance.

## Modifier le site
- **Textes, services, tarifs, arrondissements, articles** : `_src/data.py`
- **Téléphone, e-mail, domaine, Google (GTM / Analytics / Ads), mentions légales** : bloc `CONFIG` en haut de `_src/build.py`
- **Couleurs et mise en page** : `assets/css/main.css` (variables en haut du fichier)

Puis régénérer :

```bash
python3 _src/build.py
```

Sur Netlify, la génération est faite automatiquement à chaque déploiement (`netlify.toml`).

## Pages générées
- Accueil, services (6), 20 pages arrondissement (`/serrurier-paris-15e/`…)
- 120 pages service × arrondissement (`/serrurier-paris-15e/ouverture-de-porte/`…)
- Tarifs, assurance, avis, FAQ, contact, conseils, mentions légales, confidentialité, plan du site
- `sitemap.xml`, `robots.txt`, `llms.txt`

## À compléter avant la mise en ligne
Dans `CONFIG` : `siren`, `siret`, `mediateur` (mentions légales obligatoires), et le lien exact de la fiche Google (`maps_url`, `avis_url`).
