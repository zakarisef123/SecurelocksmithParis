# -*- coding: utf-8 -*-
"""Version française du contenu du site (même structure que data.py).

Les « slug » restent ceux de la version anglaise : ils servent aux photos et aux ancres.
Les adresses françaises (/fr/services/ouverture-de-porte/…) sont calculées dans build.py.
Relancez ensuite : python3 _src/build.py
"""

# ---------------------------------------------------------------------------
# Services
# ---------------------------------------------------------------------------
SERVICES = [
    {
        "slug": "door-opening",
        "cat": "urgence",
        "nom": "Ouverture de porte",
        "court": "Ouverture de porte",
        "icon": "i-door",
        "prix": "dès 110 € TTC",
        "prix_num": 110,
        "phrase": "une ouverture de porte",
        "resume": "Porte claquée, clés oubliées à l'intérieur : ouverture en douceur, sans casse ni changement de serrure dans la plupart des cas.",
        "intro": "Un courant d'air, un geste machinal, et vous voilà sur le palier avec les clés de l'autre côté de la porte. Rassurez-vous : une porte simplement claquée, c'est-à-dire non fermée à double tour, s'ouvre presque toujours sans aucun dégât. Nos serruriers interviennent partout dans Paris, de jour comme de nuit, avec des outils d'ouverture fine.",
        "sections": [
            ("Claquée ou verrouillée : ce qui change pour l'ouverture",
             "Quand la porte est <strong>claquée</strong>, seul le demi-tour (la languette qui se rétracte quand on tourne la poignée) la retient. Une lame souple glissée entre l'ouvrant et le dormant suffit en général à l'ouvrir. Quand elle est <strong>fermée à clé</strong>, ce sont les pênes dormants qui travaillent : l'ouverture sans casse reste possible dans de nombreux cas, mais demande plus de temps, parfois un perçage du cylindre, toujours expliqué et chiffré avant."),
            ("Des techniques qui préservent votre porte",
             "Lames, crochets, outils de contournement du cylindre : notre serrurier choisit la méthode la moins invasive pour votre modèle de porte. Les portes blindées des immeubles parisiens disposent souvent de protections spécifiques ; nous avons l'outillage adapté. Le perçage n'intervient qu'en dernier recours, avec votre accord, et le cylindre est alors remplacé sur place."),
            ("Pendant que vous patientez",
             "Pensez au gardien de l'immeuble, à un voisin de confiance ou à votre agence : quelqu'un possède peut-être un double. Évitez la carte bancaire et le tournevis : ils abîment le joint, la gâche ou le chant de la porte, et l'ouverture devient plus longue. Si un enfant est à l'intérieur ou si une casserole est sur le feu, dites-le-nous au téléphone : l'intervention est traitée en priorité."),
        ],
        "faq": [
            ("Quel est le prix d'une ouverture de porte claquée à Paris ?", "110 € TTC en semaine en journée (8h–18h), 160 € en soirée (18h–22h, et de 8h à 22h le week-end et les jours fériés) et 220 € la nuit (22h–8h). Pour une porte fermée à clé, comptez à partir de 180 € en journée. Le prix est annoncé au téléphone, puis confirmé par un devis écrit avant l'intervention."),
            ("Ma serrure sera-t-elle abîmée ?", "Dans l'immense majorité des cas, non : une porte claquée s'ouvre sans laisser de trace. Si un perçage devenait nécessaire, le serrurier vous expliquerait pourquoi et vous en donnerait le prix avant, et vous resteriez libre de refuser."),
            ("Combien de temps faut-il pour ouvrir ?", "Souvent moins de dix minutes pour une porte claquée. Une porte blindée ou fermée à clé peut demander davantage."),
        ],
    },
    {
        "slug": "jammed-lock",
        "cat": "urgence",
        "nom": "Déblocage de serrure",
        "court": "Serrure bloquée",
        "icon": "i-lock",
        "prix": "dès 180 € TTC",
        "prix_num": 180,
        "phrase": "un déblocage de serrure",
        "resume": "Clé qui ne tourne plus, cylindre grippé, pêne coincé : diagnostic sur place et réparation plutôt que remplacement.",
        "intro": "La clé entre mais refuse de tourner, la poignée force, la porte ne se verrouille plus : une serrure bloquée peut vous empêcher de rentrer comme de sortir, ou de fermer votre appartement en partant. Notre serrurier identifie l'origine du blocage et répare le mécanisme chaque fois que c'est possible, sans vous vendre une serrure neuve inutile.",
        "sections": [
            ("D'où vient le blocage ?",
             "Le plus souvent : un cylindre encrassé par la poussière ou un mauvais lubrifiant, une clé usée ou légèrement tordue, une porte qui s'est affaissée et dont le pêne frotte sur la gâche, un ressort cassé dans le boîtier, ou une tringle désolidarisée sur une serrure multipoints. Dans les immeubles anciens, les variations d'humidité font aussi gonfler et travailler le bois des portes."),
            ("Notre intervention, étape par étape",
             "Si vous êtes dehors, nous ouvrons d'abord la porte. Le serrurier démonte ensuite le mécanisme, vous montre la pièce en cause et vous propose la réparation adaptée : nettoyage, réglage de la gâche, remplacement d'un ressort ou, si le cylindre est hors d'usage, pose d'un cylindre neuf. Les pièces courantes sont dans le véhicule pour terminer le jour même."),
            ("Garder une serrure fluide",
             "Une fois par an, un peu de lubrifiant sec (graphite ou PTFE) dans le canon suffit. Bannissez l'huile alimentaire et les sprays gras qui collent la poussière. Si votre porte frotte ou qu'il faut la soulever pour fermer, faites régler les paumelles : c'est souvent la cause cachée d'un pêne qui force."),
        ],
        "faq": [
            ("La clé tourne dans le vide : est-ce grave ?", "C'est souvent le panneton de la clé ou la came du cylindre qui est cassé. N'insistez pas : nous ouvrons la porte et remplaçons uniquement la pièce défaillante."),
            ("Peut-on réparer une serrure 3 points sans tout changer ?", "Oui, dans la plupart des cas. On remplace uniquement le boîtier, la tringle ou le cylindre concerné, sans changer l'ensemble."),
            ("Mon assurance prend-elle en charge la réparation ?", "Cela dépend de votre contrat et de la cause (usure ou tentative d'effraction). Nous vous remettons une facture détaillée à transmettre à votre assureur."),
        ],
    },
    {
        "slug": "broken-key",
        "cat": "urgence",
        "nom": "Extraction de clé cassée",
        "court": "Clé cassée",
        "icon": "i-key",
        "prix": "sur devis gratuit",
        "prix_num": None,
        "phrase": "l'extraction d'une clé cassée",
        "resume": "Morceau de clé coincé dans le cylindre : extraction propre sans changer la serrure, puis conseils pour la suite.",
        "intro": "Une clé fatiguée finit un jour par céder, et c'est souvent au pire moment : tôt le matin ou tard le soir. Dans la plupart des cas, le morceau resté dans le cylindre peut être retiré sans démonter ni remplacer la serrure.",
        "sections": [
            ("Surtout, ne forcez pas",
             "Pousser le morceau avec une autre clé, un trombone ou un tournevis l'enfonce plus loin et peut coincer les goupilles. Quant à la colle, elle condamne le cylindre. Si le bout dépasse nettement, tirez-le bien droit avec une pince fine, sans tourner. Sinon, laissez faire un professionnel."),
            ("Comment nous retirons le morceau",
             "Le serrurier glisse des extracteurs très fins le long des goupilles pour accrocher le morceau et le ramener vers l'extérieur. Il vérifie ensuite que le cylindre fonctionne avec votre double et, si l'usure est avancée, vous propose un cylindre neuf avec plusieurs clés."),
            ("Et si c'était votre dernière clé ?",
             "Pour un cylindre de sécurité, la reproduction se fait à partir de la carte de propriété auprès d'un revendeur agréé. Sans carte ni double, le plus simple est de remplacer le cylindre : vous repartez avec des clés neuves et la certitude que personne d'autre n'en possède."),
        ],
        "faq": [
            ("Faut-il changer la serrure après une clé cassée ?", "Pas forcément. Si le cylindre n'est pas abîmé et que vous avez un double, l'extraction suffit."),
            ("Combien coûte l'extraction d'une clé cassée ?", "Le prix dépend du type de cylindre et de l'heure : il vous est annoncé au téléphone, puis confirmé par un devis gratuit avant l'intervention."),
            ("Ma clé s'est cassée dans ma boîte aux lettres", "Nous intervenons aussi sur les serrures de boîte aux lettres, de cave et de local."),
        ],
    },
    {
        "slug": "lock-replacement",
        "cat": "urgence",
        "nom": "Changement de serrure et de cylindre",
        "court": "Changement de serrure",
        "icon": "i-cyl",
        "prix": "dès 160 € TTC",
        "prix_num": 160,
        "phrase": "un changement de serrure",
        "resume": "Clés perdues ou volées, emménagement, serrure usée : cylindre neuf ou serrure multipoints A2P posés le jour même.",
        "intro": "Trousseau perdu dans le métro, sac volé, nouvel appartement dont vous ignorez qui a les doubles, serrure qui accroche depuis des mois : changer le cylindre ou la serrure est le moyen le plus sûr de redevenir seul maître de vos accès.",
        "sections": [
            ("Cylindre seul ou serrure complète ?",
             "Dans la majorité des situations, remplacer le <strong>cylindre</strong> (le barillet dans lequel entre la clé) suffit : c'est rapide et économique. La <strong>serrure complète</strong> se change quand le boîtier est endommagé, après une effraction, ou pour passer à une fermeture 3 ou 5 points plus résistante."),
            ("A2P : lire les étoiles",
             "La certification A2P, délivrée par le CNPP, indique la résistance à l'effraction : une étoile pour 5 minutes, deux pour 10 minutes, trois pour 15 minutes. Certains contrats d'assurance exigent un niveau minimum : vérifiez le vôtre, nous vous conseillerons le modèle adapté. Les cylindres de sécurité sont livrés avec une carte de propriété qui protège la reproduction des clés."),
            ("Un choix clair, un prix posé",
             "Le serrurier vous présente plusieurs gammes, du standard à la haute sécurité certifiée, avec un prix tout compris (pièce et pose). Vous choisissez, il installe, puis vous remet la facture, les clés neuves et la carte de propriété."),
        ],
        "faq": [
            ("Combien coûte un changement de cylindre ?", "À partir de 160 € TTC en semaine en journée (8h–18h), 210 € en soirée (18h–22h, et de 8h à 22h le week-end et les jours fériés) et 230 € la nuit (22h–8h). Une serrure complète démarre à 250 €. Le prix final dépend de la marque et du niveau de sécurité choisis : un devis détaillé vous est remis avant."),
            ("Dois-je changer la serrure après un vol de clés ?", "Oui, surtout si des papiers portant votre adresse ont disparu en même temps. Selon votre contrat, votre assurance peut prendre en charge le remplacement."),
            ("Locataire ou propriétaire : qui paie ?", "La perte des clés est en général à la charge du locataire, le remplacement d'une serrure vétuste plutôt à celle du propriétaire. Votre bail fait foi."),
        ],
    },
    {
        "slug": "smart-lock",
        "cat": "travaux",
        "nom": "Serrure connectée : pose et dépannage",
        "court": "Serrure connectée",
        "icon": "i-smart",
        "prix": "sur devis gratuit",
        "prix_num": None,
        "phrase": "une serrure connectée",
        "resume": "Pose et dépannage de serrures connectées : ouverture par smartphone, code, badge ou empreinte digitale.",
        "intro": "Ouvrir avec son téléphone, donner un accès temporaire à une nounou ou à un locataire de courte durée, savoir qui est entré et quand : la serrure connectée séduit de plus en plus de Parisiens. Nous l'installons sur votre porte existante et intervenons quand elle refuse de coopérer.",
        "sections": [
            ("Une installation adaptée à votre porte",
             "Selon le modèle, la serrure connectée se fixe côté intérieur sur votre cylindre actuel, ou remplace cylindre et poignée. Nous vérifions d'abord la compatibilité (épaisseur de porte, type de cylindre, porte blindée ou non), installons, paramétrons l'application avec vous et testons chaque mode d'ouverture."),
            ("Quand la serrure ne répond plus",
             "Piles à plat, mise à jour interrompue, appairage perdu, moteur qui force sur un pêne mal aligné : nous vous ouvrons si vous êtes à l'extérieur, remettons le système en route et réglons la porte pour que la panne ne revienne pas."),
            ("Les bons réflexes",
             "Gardez toujours une clé mécanique de secours hors de chez vous, préférez un modèle associé à un cylindre certifié pour une porte d'entrée, et changez les piles dès la première alerte de batterie faible."),
        ],
        "faq": [
            ("Ma serrure connectée est bloquée et je suis dehors", "Appelez-nous : nous ouvrons comme pour une serrure classique, puis remettons votre serrure connectée en service."),
            ("Peut-on en poser une sur une porte blindée ?", "Souvent oui, selon le cylindre en place. Envoyez-nous une photo de votre porte sur WhatsApp pour une réponse rapide."),
            ("Combien coûte une installation ?", "Installation comme dépannage font l'objet d'un devis gratuit : le prix dépend du modèle et vous est communiqué avant toute intervention."),
        ],
    },
    {
        "slug": "break-in-repair",
        "cat": "urgence",
        "nom": "Sécurisation après effraction",
        "court": "Après effraction",
        "icon": "i-tool",
        "prix": "sur devis gratuit",
        "prix_num": None,
        "phrase": "la sécurisation de votre logement après une effraction",
        "resume": "Porte forcée ou cambriolage : fermeture provisoire en urgence, remplacement de serrure, renforts et documents pour votre assureur.",
        "intro": "Après un cambriolage ou une tentative d'effraction, une seule priorité : pouvoir refermer chez vous le soir même. Nous sécurisons votre porte en urgence, puis vous proposons une remise en état durable, avec tous les justificatifs dont votre assureur aura besoin.",
        "sections": [
            ("Les bons gestes, dans l'ordre",
             "1. Ne touchez à rien et appelez la police (17) pour le constat. 2. Déposez plainte au commissariat ou en ligne : votre assureur demandera le récépissé. 3. Faites sécuriser votre porte : nous intervenons 24h/24 dans tout Paris. 4. Déclarez le sinistre à votre assurance, en général sous 2 jours ouvrés."),
            ("Mise en sécurité immédiate",
             "Remplacement du cylindre arraché, pose d'une serrure provisoire, renfort de la gâche ou du bâti, condamnation temporaire si la porte ne ferme plus. Objectif : que vous dormiez en sécurité chez vous dès ce soir."),
            ("Remise en état et renforcement",
             "Selon les dégâts : serrure multipoints A2P, cornières anti-pinces, protège-cylindre, renfort de bâti, blindage de la porte existante. Nous vous remettons un devis détaillé et des photos avant/après pour l'expert de votre assurance."),
        ],
        "faq": [
            ("L'assurance rembourse-t-elle le serrurier après un cambriolage ?", "Avec la plupart des contrats multirisques habitation, oui, sur présentation du dépôt de plainte et de la facture. La nôtre est détaillée et conforme."),
            ("Pouvez-vous venir avant la police ?", "Mieux vaut attendre le constat. Si la porte ne ferme plus du tout, nous la sécurisons provisoirement en préservant les traces utiles à l'enquête."),
            ("Posez-vous des portes blindées ?", "Oui : nous blindons les portes existantes, posons des renforts et installons des blocs-portes blindés complets sur devis."),
        ],
    },
    {
        "slug": "door-armoring",
        "cat": "travaux",
        "nom": "Blindage de porte",
        "court": "Blindage de porte",
        "icon": "i-shield",
        "prix": "dès 2 300 € TTC",
        "prix_num": 2300,
        "phrase": "le blindage d'une porte",
        "resume": "Renforcez votre porte existante : tôle d'acier, serrure multipoints et cornières anti-pinces, sans changer son aspect côté palier.",
        "intro": "Le blindage transforme votre porte actuelle en porte de sécurité, sans remplacer le bâti ni modifier son aspect extérieur. C'est la solution la plus courante dans les immeubles parisiens, où le règlement de copropriété demande souvent de conserver l'apparence des portes palières.",
        "sections": [
            ("Ce que comprend un blindage",
             "Une tôle d'acier fixée sur la face intérieure du vantail, une serrure multipoints avec cylindre de sécurité, des cornières anti-pinces sur le bâti, des paumelles renforcées et des pions anti-dégondage. Selon la porte, nous ajoutons un seuil, un judas ou un entrebâilleur."),
            ("Blinder plutôt que remplacer ?",
             "Le blindage coûte en général moins cher qu'un bloc-porte complet, se pose en une journée et conserve votre porte d'origine, souvent en bois massif dans l'ancien. Il convient à la plupart des portes en bon état. Si le bâti est trop fragile, nous vous le disons et vous proposons un bloc-porte."),
            ("Un devis détaillé après visite",
             "Nous venons mesurer votre porte, contrôler le bâti et vous présenter plusieurs niveaux de protection. Le devis est gratuit et précise le matériel, le prix posé et le délai."),
        ],
        "faq": [
            ("Combien coûte un blindage de porte à Paris ?", "À partir de 2 300 € TTC posé, selon les dimensions, le nombre de points de fermeture et la serrure choisie. Le prix exact figure sur un devis gratuit établi après visite."),
            ("Faut-il l'accord de la copropriété ?", "La face extérieure de la porte donne sur les parties communes. Un blindage qui conserve l'aspect côté palier pose rarement problème, mais vérifiez votre règlement de copropriété."),
            ("Combien de temps dure la pose ?", "En général une journée : votre porte est fermée et sécurisée le soir même."),
        ],
    },
    {
        "slug": "armored-door",
        "cat": "travaux",
        "nom": "Pose de porte blindée",
        "court": "Porte blindée",
        "icon": "i-door",
        "prix": "dès 3 350 € TTC",
        "prix_num": 3350,
        "phrase": "la pose d'une porte blindée",
        "resume": "Bloc-porte blindé certifié A2P BP1, BP2 ou BP3 : porte, huisserie et serrure multipoints conçues ensemble, posées sur mesure.",
        "intro": "Le bloc-porte blindé est la protection la plus complète : la porte et son huisserie sont conçues ensemble, en acier, avec une serrure multipoints intégrée. C'est la solution recommandée quand le bâti existant est abîmé, après une effraction violente, ou pour les logements les plus exposés.",
        "sections": [
            ("Les niveaux de certification",
             "La certification A2P BP, délivrée par le CNPP, mesure la résistance d'un bloc-porte à l'effraction : BP1 (5 minutes), BP2 (10 minutes), BP3 (15 minutes). Certaines assurances exigent un niveau minimum : vérifiez votre contrat, nous vous conseillerons le modèle adapté."),
            ("Une finition adaptée à votre immeuble",
             "Les blocs-portes blindés existent dans de nombreuses finitions (bois, moulures, teintes) pour respecter l'harmonie des paliers parisiens et le règlement de l'immeuble. Ils améliorent aussi l'isolation phonique et thermique."),
            ("De la prise de mesures à la pose",
             "Visite et prise de cotes, devis détaillé, commande sur mesure, puis pose, en général en une journée, avec évacuation de l'ancienne porte. Le délai de fabrication figure sur le devis ; si besoin, nous sécurisons votre porte actuelle en attendant."),
        ],
        "faq": [
            ("Quel budget pour une porte blindée ?", "À partir de 3 350 € TTC posée. Le prix dépend du niveau de certification, des dimensions et de la finition : un devis gratuit vous est remis après visite."),
            ("Blindage ou bloc-porte : que choisir ?", "Si votre porte et son bâti sont en bon état, le blindage suffit souvent. Si le bâti est fragile ou abîmé, le bloc-porte est plus sûr. Nous vous conseillons après avoir vu votre porte."),
            ("La pose fait-elle beaucoup de dégâts ?", "Non : l'ancienne huisserie est déposée proprement, le bloc-porte est ajusté, puis les finitions sont reprises. Nous protégeons le palier et l'appartement pendant les travaux."),
        ],
    },
    {
        "slug": "cellar-door",
        "cat": "travaux",
        "nom": "Porte de cave blindée",
        "court": "Porte de cave",
        "icon": "i-lock",
        "prix": "dès 1 550 € TTC",
        "prix_num": 1550,
        "phrase": "une porte de cave blindée",
        "resume": "Cave forcée ou mal protégée : bloc-porte de cave en acier avec serrure de sûreté, fabriqué aux dimensions de votre ouverture.",
        "intro": "Les caves des immeubles parisiens sont des cibles fréquentes : portes en bois léger, cadenas fragiles, couloirs peu éclairés. Un bloc-porte de cave en acier, équipé d'une vraie serrure de sûreté, protège durablement ce que vous y rangez.",
        "sections": [
            ("Une porte pensée pour les sous-sols",
             "Bâti et vantail en acier, serrure de sûreté ou multipoints, paumelles renforcées, finition résistante à l'humidité. La porte est fabriquée aux dimensions de votre ouverture, souvent irrégulière dans l'ancien."),
            ("Après une effraction de cave",
             "Nous sécurisons d'abord l'accès (serrure provisoire, renfort), puis nous vous proposons une porte définitive. Pensez à déposer plainte et à prévenir votre syndic : d'autres caves ont peut-être été visitées."),
            ("En accord avec la copropriété",
             "Les caves se trouvant dans les parties communes, il est conseillé d'informer le syndic avant de remplacer la porte. Nous pouvons vous fournir un descriptif technique."),
        ],
        "faq": [
            ("Combien coûte une porte de cave blindée ?", "À partir de 1 550 € TTC posée, selon les dimensions et la serrure. Devis gratuit après visite."),
            ("Peut-on simplement changer la serrure de la cave ?", "Oui. Si la porte est saine, une serrure neuve ou l'ajout d'un verrou de sûreté peut suffire : nous vous le dirons sur place."),
            ("Ma cave a été forcée cette nuit", "Appelez-nous : nous sécurisons l'accès rapidement, sur devis, et vous remettons une facture pour votre assurance."),
        ],
    },
    {
        "slug": "mailbox-lock",
        "cat": "travaux",
        "nom": "Serrure de boîte aux lettres",
        "court": "Boîte aux lettres",
        "icon": "i-mail",
        "prix": "dès 110 € TTC",
        "prix_num": 110,
        "phrase": "le changement d'une serrure de boîte aux lettres",
        "resume": "Clé perdue, serrure cassée ou emménagement : nous remplaçons la serrure de votre boîte aux lettres, clés neuves fournies.",
        "intro": "Clé égarée, serrure forcée, nouvel occupant : changer la serrure d'une boîte aux lettres est une intervention rapide, qui évite que votre courrier reste accessible à quelqu'un d'autre.",
        "sections": [
            ("Une serrure compatible avec votre boîte",
             "Les boîtes aux lettres d'immeuble utilisent des serrures standardisées. Nous identifions le modèle et posons une serrure compatible, livrée avec ses clés."),
            ("Ouverture sans dégât",
             "Si vous n'avez plus de clé, nous ouvrons la boîte sans abîmer le portillon, puis nous remplaçons la serrure."),
            ("Et le reste de vos accès ?",
             "Si vous avez perdu tout votre trousseau, pensez aussi au cylindre de votre porte d'entrée et à votre cave : nous pouvons tout traiter lors du même passage."),
        ],
        "faq": [
            ("Combien coûte le changement d'une serrure de boîte aux lettres ?", "110 € TTC pour un modèle standard. Les modèles spécifiques font l'objet d'un devis gratuit."),
            ("Locataire ou propriétaire : qui paie ?", "La perte de clé est généralement à la charge du locataire, l'usure plutôt à celle du propriétaire. Votre bail fait foi."),
            ("Intervenez-vous sur les boîtes à badge ou à code ?", "Selon le modèle, oui. Envoyez-nous une photo sur WhatsApp pour vérifier."),
        ],
    },
]

# ---------------------------------------------------------------------------
# Urgences 24h/24 : (situation, service lié, prix affiché par tranche, conseil en attendant)
# ---------------------------------------------------------------------------
URGENCES = [
    ("Porte claquée, clés à l'intérieur", "door-opening", ("110 €", "160 €", "220 €"), "N'utilisez ni carte bancaire ni tournevis : vous abîmeriez la gâche."),
    ("Porte fermée à clé, clés perdues", "door-opening", ("dès 180 €", "dès 250 €", "dès 280 €"), "Demandez au gardien ou à un voisin s'il garde un double."),
    ("Serrure bloquée, la clé ne tourne plus", "jammed-lock", ("180 €", "250 €", "280 €"), "Ne forcez pas : vous risquez de casser la clé dans le cylindre."),
    ("Clé cassée dans la serrure", "broken-key", "quote", "Ne poussez pas le morceau plus loin et n'utilisez jamais de colle."),
    ("Cambriolage, porte forcée", "break-in-repair", "quote", "Appelez la police (17) et ne touchez à rien avant son arrivée."),
    ("Clés volées : changer le cylindre", "lock-replacement", ("dès 160 €", "dès 210 €", "dès 230 €"), "Si vos papiers ont été volés avec, faites changer le cylindre aujourd'hui."),
    ("Serrure connectée en panne", "smart-lock", "quote", "Cherchez votre clé mécanique de secours avant d'appeler."),
    ("Cave forcée", "cellar-door", "quote", "Prévenez le syndic : d'autres caves ont peut-être été visitées."),
]

# ---------------------------------------------------------------------------
# Les 20 arrondissements
# n: (surnom, population INSEE, codes postaux, quartiers administratifs, repères, métros, habitat)
# ---------------------------------------------------------------------------
ARRONDISSEMENTS = {
    1: ("Louvre", 15114, ["75001"], ["Saint-Germain-l'Auxerrois", "Halles", "Palais-Royal", "Place-Vendôme"],
        ["la rue Saint-Honoré", "le jardin des Tuileries", "le Forum des Halles"], ["Louvre-Rivoli", "Pyramides", "Tuileries"],
        "appartements anciens au-dessus des boutiques, hôtels particuliers et nombreux bureaux"),
    2: ("Bourse", 19847, ["75002"], ["Gaillon", "Vivienne", "Mail", "Bonne-Nouvelle"],
        ["les passages couverts", "la rue Réaumur", "le quartier du Sentier"], ["Bourse", "Sentier", "Quatre-Septembre"],
        "immeubles de rapport du XIXe siècle, ateliers reconvertis en lofts et petites entreprises"),
    3: ("Temple", 32179, ["75003"], ["Arts-et-Métiers", "Enfants-Rouges", "Archives", "Sainte-Avoye"],
        ["le musée Picasso", "le square du Temple", "la rue de Bretagne"], ["Temple", "Arts et Métiers", "Filles du Calvaire"],
        "hôtels particuliers du Marais, cours pavées et immeubles à portes cochères"),
    4: ("Hôtel-de-Ville", 27332, ["75004"], ["Saint-Merri", "Saint-Gervais", "Arsenal", "Notre-Dame"],
        ["la place des Vosges", "le Centre Pompidou", "l'île de la Cité"], ["Saint-Paul", "Hôtel de Ville", "Pont Marie"],
        "immeubles des XVIIe et XVIIIe siècles, chambres sous les toits et commerces du Marais"),
    5: ("Panthéon", 55252, ["75005"], ["Saint-Victor", "Jardin-des-Plantes", "Val-de-Grâce", "Sorbonne"],
        ["les arènes de Lutèce", "la place de la Contrescarpe", "le Jardin des Plantes"], ["Maubert-Mutualité", "Place Monge", "Cardinal Lemoine"],
        "studios étudiants, immeubles anciens et résidences universitaires"),
    6: ("Luxembourg", 40389, ["75006"], ["Monnaie", "Odéon", "Notre-Dame-des-Champs", "Saint-Germain-des-Prés"],
        ["le boulevard Saint-Germain", "la rue de Rennes", "le théâtre de l'Odéon"], ["Odéon", "Mabillon", "Saint-Placide"],
        "appartements bourgeois, galeries d'art et portes blindées haut de gamme"),
    7: ("Palais-Bourbon", 48015, ["75007"], ["Saint-Thomas-d'Aquin", "Invalides", "École-Militaire", "Gros-Caillou"],
        ["le Champ-de-Mars", "le musée d'Orsay", "la rue Cler"], ["École Militaire", "Solférino", "La Tour-Maubourg"],
        "immeubles haussmanniens cossus, ministères et grands appartements familiaux"),
    8: ("Élysée", 35317, ["75008"], ["Champs-Élysées", "Faubourg-du-Roule", "Madeleine", "Europe"],
        ["la place de la Concorde", "la rue du Faubourg-Saint-Honoré", "le boulevard Haussmann"], ["Miromesnil", "Saint-Augustin", "George V"],
        "sièges sociaux, boutiques de luxe et vastes appartements haussmanniens"),
    9: ("Opéra", 57271, ["75009"], ["Saint-Georges", "Chaussée-d'Antin", "Faubourg-Montmartre", "Rochechouart"],
        ["les grands magasins", "la rue des Martyrs", "la Nouvelle Athènes"], ["Notre-Dame-de-Lorette", "Cadet", "Le Peletier"],
        "immeubles haussmanniens, bureaux et appartements familiaux"),
    10: ("Entrepôt", 83873, ["75010"], ["Saint-Vincent-de-Paul", "Porte-Saint-Denis", "Porte-Saint-Martin", "Hôpital-Saint-Louis"],
         ["le canal Saint-Martin", "la gare du Nord", "la rue du Faubourg-Saint-Denis"], ["Jacques Bonsergent", "Château d'Eau", "Colonel Fabien"],
         "immeubles anciens, ateliers sur cour et commerces très nombreux"),
    11: ("Popincourt", 138170, ["75011"], ["Folie-Méricourt", "Roquette", "Sainte-Marguerite", "Saint-Ambroise"],
         ["la rue de la Roquette", "le boulevard Voltaire", "la rue Oberkampf"], ["Voltaire", "Parmentier", "Charonne"],
         "petits immeubles faubouriens, passages et anciens ateliers devenus logements"),
    12: ("Reuilly", 138024, ["75012"], ["Bel-Air", "Picpus", "Bercy", "Quinze-Vingts"],
         ["la Coulée verte", "la cour Saint-Émilion", "le bois de Vincennes"], ["Nation", "Daumesnil", "Dugommier"],
         "résidences des années 1970 à 2000, immeubles haussmanniens et nouveau quartier de Bercy"),
    13: ("Gobelins", 181271, ["75013"], ["Salpêtrière", "Gare", "Maison-Blanche", "Croulebarbe"],
         ["l'avenue de Choisy", "Paris Rive Gauche", "la manufacture des Gobelins"], ["Tolbiac", "Olympiades", "Bibliothèque François-Mitterrand"],
         "tours des Olympiades, résidences modernes à digicode et maisons de la Butte-aux-Cailles"),
    14: ("Observatoire", 136455, ["75014"], ["Montparnasse", "Parc-de-Montsouris", "Petit-Montrouge", "Plaisance"],
         ["la rue Daguerre", "le parc Montsouris", "la Cité universitaire"], ["Mouton-Duvernet", "Pernety", "Plaisance"],
         "immeubles en brique, maisons, ateliers d'artistes et grands ensembles"),
    15: ("Vaugirard", 229713, ["75015"], ["Saint-Lambert", "Necker", "Grenelle", "Javel"],
         ["le Front de Seine", "le parc André-Citroën", "la rue du Commerce"], ["Commerce", "Vaugirard", "Félix Faure"],
         "tours du Front de Seine, immeubles des années 1930 et nombreuses résidences familiales"),
    16: ("Passy", 159386, ["75016", "75116"], ["Auteuil", "Muette", "Porte-Dauphine", "Chaillot"],
         ["la rue de Passy", "l'avenue Victor-Hugo", "le bois de Boulogne"], ["La Muette", "Ranelagh", "Michel-Ange-Auteuil"],
         "hôtels particuliers, villas privées et appartements équipés de portes blindées"),
    17: ("Batignolles-Monceau", 159212, ["75017"], ["Ternes", "Plaine-de-Monceaux", "Batignolles", "Épinettes"],
         ["le parc Clichy-Batignolles", "l'avenue de Wagram", "la rue de Lévis"], ["Brochant", "Wagram", "Guy Môquet"],
         "immeubles haussmanniens, éco-quartier Clichy-Batignolles et petites maisons des Épinettes"),
    18: ("Butte-Montmartre", 183127, ["75018"], ["Grandes-Carrières", "Clignancourt", "Goutte-d'Or", "La Chapelle"],
         ["la place du Tertre", "la rue Lepic", "le marché aux Puces"], ["Lamarck-Caulaincourt", "Jules Joffrin", "Marcadet-Poissonniers"],
         "immeubles anciens aux escaliers étroits, ateliers d'artistes et résidences récentes"),
    19: ("Buttes-Chaumont", 178691, ["75019"], ["La Villette", "Pont-de-Flandre", "Amérique", "Combat"],
         ["le bassin de la Villette", "le parc des Buttes-Chaumont", "la Mouzaïa"], ["Laumière", "Ourcq", "Botzaris"],
         "grands ensembles, résidences à badge et maisons de la Mouzaïa"),
    20: ("Ménilmontant", 185140, ["75020"], ["Belleville", "Saint-Fargeau", "Père-Lachaise", "Charonne"],
         ["le parc de Belleville", "la rue des Pyrénées", "le village de Charonne"], ["Pyrénées", "Gambetta", "Porte de Bagnolet"],
         "immeubles faubouriens, cités d'artisans, logements sociaux et maisons de ville"),
}

# ---------------------------------------------------------------------------
# Grille tarifaire (TTC) : prestation, journée (semaine 8h–18h), soirée (semaine 18h–22h ; week-end et fériés 8h–22h), nuit 22h–8h
# None = sur devis pour cette tranche horaire. « À partir de … » = prix de départ.
# ---------------------------------------------------------------------------
TARIFS = [
    ("Ouverture de porte claquée", "110 €", "160 €", "220 €"),
    ("Ouverture de porte fermée à clé", "À partir de 180 €", "À partir de 250 €", "À partir de 280 €"),
    ("Serrure bloquée, clé qui ne tourne plus", "180 €", "250 €", "280 €"),
    ("Changement de cylindre", "À partir de 160 €", "À partir de 210 €", "À partir de 230 €"),
    ("Remplacement de serrure", "À partir de 250 €", None, None),
    ("Blindage de porte", "À partir de 2 300 €", None, None),
    ("Bloc-porte blindé complet", "À partir de 3 350 €", None, None),
    ("Bloc-porte de cave", "À partir de 1 550 €", None, None),
    ("Serrure de boîte aux lettres (modèle standard)", "110 €", None, None),
]

# Marques (nom, fichier logo dans assets/img/marques/, catégorie)
_CAT = {"Locks": "Serrures", "Armored doors": "Portes blindées", "Smart locks": "Serrures connectées"}


def _marques():
    from data import MARQUES as M
    return [(n, s, _CAT.get(c, c)) for n, s, c in M]


MARQUES = _marques()

# Avis Google en français : mêmes règles que dans data.py (uniquement de vrais avis)
AVIS = []

# ---------------------------------------------------------------------------
# Conseils (blog) – « slug » = adresse anglaise ; l'adresse française est dans build.py
# ---------------------------------------------------------------------------
ARTICLES = [
    {
        "slug": "lost-keys-paris",
        "titre": "Clés perdues à Paris : les 5 réflexes à avoir tout de suite",
        "court": "Clés perdues : les 5 réflexes",
        "cat": "Urgence", "date": "2026-10-20", "icon": "i-key",
        "desc": "Trousseau égaré dans le métro, sac volé en terrasse : ce qu'il faut faire dans l'heure pour rentrer chez vous et rester en sécurité.",
        "corps": [
            ("p", "Les clés perdues font partie des urgences les plus courantes à Paris : un trousseau qui glisse d'une poche dans le métro, un sac oublié en terrasse, une veste prêtée. Voici l'ordre dans lequel agir."),
            ("h2", "1. Refaites calmement votre trajet"),
            ("p", "Appelez les derniers endroits où vous êtes passé (café, bureau, salle de sport). Le service des objets trouvés de la Préfecture de police centralise aussi les objets rapportés dans les transports et sur la voie publique : il peut se consulter en ligne."),
            ("h2", "2. Cherchez un double"),
            ("ul", ["Un proche ou un voisin de confiance ?", "Le gardien de l'immeuble ?", "Votre agence ou votre propriétaire ?"]),
            ("h2", "3. Évaluez le risque"),
            ("p", "Si vos clés étaient avec un document portant votre adresse (carte d'identité, courrier, carte grise), considérez qu'un inconnu peut entrer chez vous : <strong>changer le cylindre</strong> devient prioritaire. Sans adresse associée, le risque est plus faible, mais un remplacement reste conseillé si vous avez le moindre doute."),
            ("h2", "4. Faites ouvrir sans casse"),
            ("p", "Si la porte est seulement claquée, un serrurier l'ouvre en quelques minutes sans abîmer la serrure. Si elle est fermée à double tour, l'ouverture sans casse reste souvent possible, et le cylindre peut être remplacé dans la foulée. Chez Secure Locksmith Paris, le prix est annoncé au téléphone avant le déplacement."),
            ("h2", "5. Prévenez votre assureur"),
            ("p", "Certains contrats couvrent la perte ou le vol des clés. Gardez la facture détaillée et, en cas de vol, le récépissé de plainte."),
        ],
    },
    {
        "slug": "armored-door-paris-apartment",
        "titre": "Porte blindée dans un immeuble parisien : ce qu'il faut savoir avant de se lancer",
        "court": "Porte blindée à Paris : le guide",
        "cat": "Sécurité", "date": "2026-09-30", "icon": "i-shield",
        "desc": "Blindage de la porte existante ou bloc-porte, accord de la copropriété, certification A2P : les questions à se poser en appartement.",
        "corps": [
            ("p", "Dans un appartement parisien, la porte palière est le principal point d'entrée des cambrioleurs. La blinder est l'un des investissements les plus efficaces pour la sécurité de votre logement, à condition de bien choisir."),
            ("h2", "Blindage ou bloc-porte ?"),
            ("p", "Le <strong>blindage</strong> renforce votre porte actuelle avec une tôle d'acier, une serrure multipoints et des cornières. Il conserve l'aspect extérieur de la porte, ce qui est souvent apprécié en copropriété. Le <strong>bloc-porte</strong> remplace tout l'ensemble (porte et huisserie) : c'est la solution la plus résistante, avec une certification A2P BP1, BP2 ou BP3."),
            ("h2", "Et la copropriété ?"),
            ("p", "La face extérieure de la porte palière donne sur les parties communes. Si son aspect change (couleur, moulures, matériau), le règlement de copropriété peut imposer une autorisation ou un modèle. Un blindage qui conserve le parement extérieur pose rarement problème : vérifiez tout de même votre règlement."),
            ("h2", "Les points à vérifier"),
            ("ul", ["La serrure : multipoints, avec un cylindre certifié A2P et une carte de propriété.", "Les paumelles : anti-dégondage.", "Le bâti : renforcé, sinon la porte la plus solide cède par le côté.", "L'isolation phonique et thermique, appréciable dans les immeubles anciens."]),
            ("p", "Nos serruriers se déplacent pour évaluer votre porte gratuitement et vous remettre un devis détaillé."),
        ],
    },
    {
        "slug": "spot-an-honest-locksmith",
        "titre": "Comment reconnaître un serrurier honnête (et éviter les arnaques)",
        "court": "Reconnaître un serrurier honnête",
        "cat": "Conseils", "date": "2026-09-08", "icon": "i-award",
        "desc": "Prospectus trompeurs, prix flous, serrure percée sans raison : les signaux d'alerte et les droits qui vous protègent.",
        "corps": [
            ("p", "Le dépannage en serrurerie est l'un des secteurs qui suscitent le plus de réclamations de consommateurs en France. Quelques réflexes simples suffisent pourtant à éviter les mauvaises surprises."),
            ("h2", "Les signaux qui doivent alerter"),
            ("ol", ["Un autocollant ou un prospectus « numéro d'urgence » qui imite la mairie ou le syndic.", "Un prix vague au téléphone, ou un « à partir de 19 € » sans plus de précision.", "Aucun devis écrit avant de commencer.", "Une proposition de percer ou de changer la serrure alors que la porte était simplement claquée.", "Un paiement uniquement en espèces, sans facture.", "Une entreprise sans nom, sans numéro SIRET ni avis vérifiables."]),
            ("h2", "Ce que la loi impose"),
            ("p", "Pour un dépannage à domicile, le professionnel doit vous informer de ses tarifs et vous remettre un <strong>devis détaillé</strong> avant l'intervention lorsque le prix peut être déterminé à l'avance. Vous pouvez le refuser. Une <strong>facture détaillée</strong> doit vous être remise à la fin."),
            ("h2", "En cas de litige"),
            ("p", "Conservez tous les documents, contestez la facture par écrit, signalez la pratique sur le site SignalConso et sollicitez le médiateur de la consommation indiqué par l'entreprise."),
            ("h2", "Notre façon de faire"),
            ("p", "Chez Secure Locksmith Paris, le prix est annoncé au téléphone, confirmé par un devis signé, et la facture est détaillée pour votre assurance. Nos avis sont publics sur notre fiche Google."),
        ],
    },
    {
        "slug": "after-a-burglary",
        "titre": "Après un cambriolage : sécuriser son appartement en 24 heures",
        "court": "Après un cambriolage : que faire ?",
        "cat": "Urgence", "date": "2026-08-18", "icon": "i-tool",
        "desc": "Constat, plainte, assurance, fermeture provisoire puis renforcement : le plan d'action heure par heure.",
        "corps": [
            ("p", "Découvrir sa porte forcée est un choc. Pour ne rien oublier et retrouver rapidement un logement qui ferme, suivez ce plan."),
            ("h2", "Dans l'heure"),
            ("ul", ["Ne rentrez pas si vous pensez que quelqu'un est encore à l'intérieur : appelez la police (17).", "Ne touchez à rien avant le constat.", "Photographiez les dégâts (porte, serrure, pièces)."]),
            ("h2", "Dans la journée"),
            ("ul", ["Déposez plainte (au commissariat ou par pré-plainte en ligne).", "Faites opposition sur vos cartes bancaires volées.", "Faites sécuriser votre porte : un serrurier pose un cylindre neuf ou une fermeture provisoire."]),
            ("h2", "Sous 2 jours ouvrés"),
            ("p", "Déclarez le sinistre à votre assureur avec le récépissé de plainte, la liste des objets volés et la facture du serrurier."),
            ("h2", "Ensuite : renforcer"),
            ("p", "Serrure multipoints A2P, protège-cylindre, cornières anti-pinces, blindage de porte : nous vous proposons les renforts adaptés à votre porte et à votre budget, avec un devis détaillé pour l'expert de l'assurance."),
        ],
    },
]

# ---------------------------------------------------------------------------
# Textes de confiance
# ---------------------------------------------------------------------------
COMPARATIF = [
    ("Un prix « à partir de 19 € » au téléphone, puis une facture de plusieurs centaines d'euros.",
     "Un prix réel annoncé au téléphone d'après votre description, et nos tarifs publiés sur ce site."),
    ("Le travail commence avant que vous ayez signé quoi que ce soit.",
     "Un devis écrit et signé avant toute intervention. Sans votre signature, rien ne commence."),
    ("La serrure est percée ou changée alors que la porte était simplement claquée.",
     "Ouverture sans casse en priorité. Un perçage n'est proposé qu'en dernier recours, expliqué et chiffré."),
    ("Un paiement exigé en espèces, sans facture ou avec une facture illisible.",
     "Carte bancaire, espèces ou virement, au choix, avec une facture détaillée à chaque fois."),
    ("Un numéro trouvé sur un autocollant qui imite la mairie ou le syndic.",
     "Une entreprise identifiée : nom, adresse, fiche Google et avis publics vérifiables."),
    ("Une plateforme d'appels qui revend votre demande au serrurier le plus offrant.",
     "Un serrurier qui décroche lui-même et se déplace en personne, de jour comme de nuit."),
]

CHARTE = [
    ("i-euro", "1. Le prix vous est annoncé avant le déplacement",
     "Au téléphone, nous vous posons quelques questions simples : la porte est-elle claquée ou fermée à clé ? Blindée ou non ? Quel type de serrure ? À partir de vos réponses, nous vous annonçons un prix TTC, selon l'heure d'intervention. Ce prix correspond à notre grille tarifaire, publiée sur ce site. Si vous préférez, envoyez une photo de votre porte sur WhatsApp : l'estimation sera encore plus précise."),
    ("i-file", "2. Un devis écrit et signé avant toute intervention",
     "Sur place, le serrurier constate la situation et vous remet un devis détaillé : nature de l'intervention, matériel éventuel, prix TTC. Vous le lisez, vous posez vos questions, vous signez. Pas avant. C'est une obligation réglementaire (arrêté du 24 janvier 2017) que nous appliquons à chaque intervention, sans exception, y compris la nuit."),
    ("i-door", "3. Pas de casse inutile, pas de remplacement inutile",
     "Une porte claquée s'ouvre presque toujours sans dégât. Nous utilisons d'abord les techniques d'ouverture fine (lames, crochetage, contournement du cylindre). Si un perçage ou un remplacement devient nécessaire, le serrurier vous explique pourquoi, vous montre la pièce en cause et vous indique le prix avant de le faire. Vous restez libre de refuser."),
    ("i-shield", "4. Du matériel de qualité, adapté à votre porte",
     "Quand une pièce doit être remplacée, nous vous proposons plusieurs gammes, du cylindre standard au cylindre de haute sécurité certifié A2P, avec leur prix posé. Nous travaillons avec des marques reconnues (Fichet, Picard, Vachette, Bricard, Mul-T-Lock…) et nous vous remettons les clés neuves et, le cas échéant, la carte de propriété."),
    ("i-card", "5. Un paiement clair et une facture détaillée",
     "Vous payez ce qui figure sur le devis signé, ni plus ni moins. Carte bancaire, espèces ou virement : le choix vous appartient. La facture détaille l'intervention et le matériel ; elle est conforme pour votre assurance habitation."),
    ("i-building", "6. Une entreprise identifiable",
     "Notre nom, notre adresse, notre téléphone et notre fiche Google figurent sur chaque page de ce site. Nos avis sont publiés par nos clients sur Google : ils sont publics et nous ne pouvons ni les modifier ni les supprimer. Vous pouvez les consulter avant même de nous appeler."),
    ("i-phone", "7. Un interlocuteur direct, 24h/24",
     "Quand vous appelez, c'est un serrurier qui vous répond, pas un centre d'appels qui transmet votre demande. Le même interlocuteur vous suit de l'appel à la facture, et reste joignable après l'intervention si vous avez une question."),
    ("i-home", "8. Le respect de votre logement",
     "Nous protégeons le sol si nécessaire, nous laissons les lieux propres et nous vous expliquons ce qui a été fait. Après une effraction, nous vous conseillons sur les démarches (plainte, assurance) et sur les renforts utiles, sans vous pousser à des travaux dont vous n'avez pas besoin."),
]

INCLUS = [
    "Le déplacement dans Paris, offert si des travaux sont réalisés",
    "La main-d'œuvre du serrurier",
    "Le diagnostic et les explications sur place",
    "Le devis écrit, gratuit et sans engagement",
    "La facture détaillée pour votre assurance",
    "La TVA : nos prix sont toujours affichés TTC",
]

REALISATIONS = {}
INTERVENTIONS = {}

# Vidéos de chantier : service -> (fichier, titre, légende, description pour Google, date)
VIDEOS = {
    "smart-lock": ("smart-lock", "Une serrure connectée que nous avons posée", "Ouverte depuis le téléphone du propriétaire",
                   "Une serrure connectée posée par Secure Locksmith Paris, ouverte depuis le téléphone du propriétaire.", "2026-11-10"),
    "door-armoring": ("lock-3-points", "Une serrure 3 points que nous avons posée", "Un tour de clé, les trois pênes se verrouillent",
                      "Une serrure 3 points en applique posée sur une porte d'appartement à Paris : la clé tourne et les trois pênes se verrouillent.", "2026-11-10"),
    "lock-replacement": ("new-keys", "Une serrure multipoints que nous avons révisée", "Testée, puis clés neuves remises",
                         "Une serrure multipoints révisée à Paris, testée avec la clé, puis clés neuves remises au client.", "2026-11-10"),
}

# ---------------------------------------------------------------------------
# Textes des pages (équivalents français des constantes de build.py)
# ---------------------------------------------------------------------------
WA_MSG = "Bonjour, j'ai besoin d'un serrurier à Paris."

NAV = [("Urgence", "/emergency/"), ("Services", "/services/"), ("Tarifs", "/prices/"), ("Nos engagements", "/our-commitments/"),
       ("Arrondissements", "/locksmith-paris/"), ("Contact", "/contact/")]

SLOTS = [("jour", "i-sun", "Journée", "8h – 18h"), ("soir", "i-sunset", "Soirée", "18h – 22h"), ("nuit", "i-moon", "Nuit", "22h – 8h")]
SLOTS_WE = {"jour": "en semaine uniquement", "soir": "8h – 22h", "nuit": "22h – 8h"}
WEEKEND_NOTE = "<b>Week-ends et jours fériés :</b> le samedi, le dimanche et les jours fériés, le tarif minimum appliqué est celui de la Soirée (18h–22h) ; si l'intervention a lieu sur la tranche Nuit (22h–8h), c'est le tarif de Nuit qui s'applique."

PARIS_BG = {
    "tour-eiffel": "La tour Eiffel au coucher du soleil", "toits-de-paris": "Les toits de Paris",
    "notre-dame": "Notre-Dame de Paris et la Seine", "pantheon": "Le Panthéon", "conciergerie": "La Conciergerie au bord de la Seine",
    "place-des-victoires": "La place des Victoires", "sacre-coeur": "Le Sacré-Cœur à Montmartre",
    "vue-sacre-coeur": "Vue sur Montmartre", "avenue-etoile": "Avenue parisienne vue depuis l'Arc de Triomphe", "mairie": "Une mairie d'arrondissement à Paris",
}

HOME_FAQ = [
    ("Combien coûte l'ouverture d'une porte à Paris ?", "Une porte claquée est ouverte pour 110 € TTC en semaine en journée (8h–18h), 160 € en soirée et le week-end, et 220 € la nuit. Le prix est annoncé au téléphone, puis confirmé par un devis écrit avant toute intervention."),
    ("Intervenez-vous dans tout Paris ?", "Oui, dans les 20 arrondissements, du 1er au 20e, 24h/24 et 7j/7, jours fériés compris. Nos serruriers sont répartis dans la ville pour arriver rapidement chez vous."),
    ("En combien de temps pouvez-vous arriver ?", "Environ 30 minutes en moyenne dans Paris. Le délai exact dépend de la circulation et vous est annoncé au téléphone avant le départ du serrurier."),
    ("Le devis est-il gratuit ?", "Oui, gratuit et sans engagement. Rien n'est fait sans votre signature, et vous restez libre de refuser."),
    ("Parlez-vous anglais ?", "Oui. Vous pouvez nous appeler ou nous écrire sur WhatsApp en français ou en anglais : le devis et la facture vous sont expliqués clairement."),
    ("Mon assurance peut-elle me rembourser ?", "Souvent, oui : effraction, vol ou perte de clés, selon votre contrat. Notre facture détaillée est acceptée par les assureurs habitation."),
    ("Comment puis-je payer ?", "Par carte bancaire, en espèces ou par virement. Vous recevez toujours une facture."),
]

MOIS = ["janvier", "février", "mars", "avril", "mai", "juin", "juillet", "août", "septembre", "octobre", "novembre", "décembre"]

ARR_INTROS = [
    "Enfermé dehors {a} ? {nom} envoie un serrurier qualifié devant votre porte, de jour comme de nuit, en général en une trentaine de minutes. Le prix vous est annoncé au téléphone avant son départ.",
    "Des abords {de_r0} aux rues plus calmes du {num}, nos serruriers interviennent 24h/24 pour les portes claquées, les serrures bloquées et les clés cassées, avec un devis signé avant toute intervention.",
    "Avec ses {pop} habitants, le {num} arrondissement ({surnom}) connaît chaque jour son lot de portes claquées et de clés perdues. Nos serruriers connaissent ses immeubles et les serrures qui les équipent.",
    "Une urgence serrurerie {a} ? Des quartiers {q} jusqu'aux abords {de_r1}, nous arrivons rapidement, à un prix convenu à l'avance, avec une facture acceptée par votre assureur.",
]

URG_FAQ = [
    ("Venez-vous vraiment la nuit et le dimanche ?", "Oui, 24h/24 et 7j/7, jours fériés compris. Le tarif de nuit (22h–8h) vous est annoncé au téléphone avant le départ du serrurier."),
    ("En combien de temps pouvez-vous arriver ?", "Environ 30 minutes en moyenne dans Paris. Le délai exact dépend de la circulation et vous est annoncé au téléphone."),
    ("Combien coûte une ouverture de porte en urgence ?", "110 € TTC en semaine en journée, 160 € en soirée et le week-end, 220 € la nuit pour une porte claquée. Une porte fermée à clé démarre à 180 € en journée."),
    ("Que dois-je préparer pour l'arrivée du serrurier ?", "Si possible, une pièce d'identité ou un justificatif de domicile : le serrurier doit s'assurer que vous êtes bien l'occupant. Si vos papiers sont à l'intérieur, un voisin, le gardien ou votre hôte peut se porter garant."),
    ("Puis-je refuser le devis sur place ?", "Oui. Le devis est gratuit et sans engagement : si vous le refusez, rien n'est fait."),
]

# Guide d'urgence : situation -> prix par tranche horaire (None = sur devis), service lié, conseil
GUIDE = [
    ("slammed", "Porte claquée, clés à l'intérieur", "door-opening", (110, 160, 220), False,
     "N'essayez pas la carte bancaire ou le tournevis sur le demi-tour : vous abîmeriez la gâche. La plupart des portes claquées s'ouvrent en quelques minutes, sans dégât."),
    ("locked", "Porte fermée à clé, clés perdues", "door-opening", (180, 250, 280), True,
     "Demandez au gardien ou à un voisin s'il garde un double. L'ouverture sans casse reste possible dans de nombreux cas."),
    ("jammed", "Serrure bloquée, la clé ne tourne plus", "jammed-lock", (180, 250, 280), False,
     "Arrêtez de forcer sur la clé : vous risquez de la casser dans le cylindre. Ne mettez pas d'huile dans la serrure."),
    ("broken", "Clé cassée dans la serrure", "broken-key", None, False,
     "Ne poussez pas le morceau plus loin et n'utilisez jamais de colle. S'il dépasse, tirez-le bien droit avec une pince fine."),
    ("burglary", "Cambriolage, porte forcée", "break-in-repair", None, False,
     "N'entrez pas si quelqu'un est peut-être encore à l'intérieur : appelez la police (17). Ne touchez à rien avant son arrivée."),
    ("stolen", "Clés volées, changer le cylindre", "lock-replacement", (160, 210, 230), True,
     "Si votre pièce d'identité ou votre adresse a été volée avec les clés, faites changer le cylindre aujourd'hui."),
    ("smart", "Serrure connectée en panne", "smart-lock", None, False,
     "Cherchez votre clé mécanique de secours et vérifiez si l'application signale une batterie faible."),
    ("cellar", "Cave forcée", "cellar-door", None, False,
     "Prévenez le syndic : d'autres caves ont peut-être été visitées."),
]

SVC_LOCAL = {
    "door-opening": {
        "intros": [
            "Enfermé dehors {a}, clés à l'intérieur ? Un serrurier {nom} part tout de suite pour ouvrir votre porte en douceur, souvent en quelques minutes et sans toucher à la serrure. Vous connaissez le prix avant son départ.",
            "Pas de panique si la porte a claqué derrière vous {a} : une porte claquée s'ouvre presque toujours sans dégât. Nous venons de jour comme de nuit, à un prix convenu à l'avance.",
            "Bloqué sur le palier {a} ? Appelez-nous : vous connaissez le prix avant l'arrivée du serrurier, et votre porte est ouverte sans casse dans l'immense majorité des cas.",
        ],
        "conseil": "Évitez la carte bancaire et le tournevis : ils abîment la gâche et le joint, et l'intervention devient plus longue.",
    },
    "jammed-lock": {
        "intros": [
            "La clé ne tourne plus {a} ? Nos serruriers trouvent la cause et réparent sur place : nettoyage, réglage de la gâche ou remplacement du cylindre si nécessaire. Prix annoncé avant le déplacement.",
            "Serrure dure, porte qui ne s'ouvre plus ou ne se verrouille plus {a} : un serrurier arrive avec les pièces courantes pour régler le problème en un seul passage dans la plupart des cas.",
            "Pêne qui frotte, cylindre encrassé, porte qui a bougé : les serrures bloquées sont fréquentes {a}. Nous réparons d'abord, et ne remplaçons que lorsque c'est vraiment nécessaire.",
        ],
        "conseil": "Ne forcez pas sur la clé et oubliez l'huile de cuisine : un lubrifiant sec (graphite ou PTFE) fonctionne bien mieux.",
    },
    "broken-key": {
        "intros": [
            "Clé cassée dans la serrure {a} ? Nos serruriers retirent le morceau avec des extracteurs dédiés, en général sans démonter la serrure, 24h/24, sur devis gratuit.",
            "Un morceau de clé coincé dans le cylindre {a} : un serrurier vient l'extraire, vérifie le cylindre et ne le remplace sur place que si c'est utile.",
            "Une vieille clé qui casse dans la serrure, c'est courant {a}. Nous retirons le morceau proprement, puis nous vous conseillons : refaire une clé ou remplacer un cylindre usé.",
        ],
        "conseil": "Ni colle, ni trombone : vous pourriez enfoncer le morceau plus loin et condamner le cylindre.",
    },
    "lock-replacement": {
        "intros": [
            "Clés perdues, emménagement ou serrure usée {a} : nous remplaçons cylindres et serrures, du modèle standard à la serrure multipoints certifiée A2P. Devis gratuit, signé avant toute intervention.",
            "Changement de serrure {a} : le serrurier arrive avec un choix de cylindres en stock, vous présente les options et leurs prix, puis pose celui que vous choisissez le jour même.",
            "Vous venez d'emménager {a} ou vous avez perdu vos clés ? Changer le cylindre est le moyen le plus simple de redevenir maître de vos accès. Matériel certifié, facture détaillée.",
        ],
        "conseil": "Regardez le nombre d'étoiles A2P (de 1 à 3) : il indique la résistance à l'effraction et est parfois exigé par les assureurs.",
    },
    "smart-lock": {
        "intros": [
            "Envie d'ouvrir votre porte avec votre téléphone {a} ? Nous installons et paramétrons des serrures connectées compatibles avec votre porte, et réparons celles qui ne répondent plus.",
            "Serrure connectée {a} : installation, paramétrage et dépannage quand les piles sont à plat ou que le moteur est bloqué. Nous vérifions la compatibilité de votre cylindre avant toute pose.",
            "Panne de serrure connectée ou projet d'installation {a} : nous ouvrons 24h/24 les portes équipées d'une serrure connectée bloquée, et installons sur rendez-vous.",
        ],
        "conseil": "Gardez une clé mécanique de secours et surveillez les piles : c'est la première cause de serrure connectée bloquée.",
    },
    "break-in-repair": {
        "intros": [
            "Cambriolage ou tentative d'effraction {a} ? Nous sécurisons votre porte en urgence, 24h/24, puis la réparons ou la renforçons. Facture détaillée pour votre assureur.",
            "Porte forcée {a} : un serrurier vient de jour comme de nuit poser une serrure provisoire ou définitive et remplacer le cylindre endommagé.",
            "Après une effraction {a}, la priorité est de pouvoir refermer ce soir. Nous arrivons vite, sur devis gratuit, et vous conseillons sur les bons renforts.",
        ],
        "conseil": "Photographiez les dégâts et déposez plainte avant la réparation définitive : votre assureur demandera le récépissé.",
    },
    "door-armoring": {
        "intros": [
            "Vous voulez sécuriser votre porte d'entrée {a} sans la remplacer ? Le blindage renforce votre porte existante avec une tôle d'acier, une serrure multipoints et des cornières anti-pinces, tout en conservant son aspect côté palier.",
            "Blindage de porte {a} : nous venons mesurer votre porte, contrôler le bâti et vous présenter plusieurs niveaux de protection, avec un devis gratuit et détaillé. La pose dure en général une journée.",
            "Vieille porte palière, serrure basique, bâti fatigué : c'est le cas de nombreux appartements {a}. Le blindage est souvent le moyen le plus efficace de dissuader les cambrioleurs sans gros travaux.",
        ],
        "conseil": "Vérifiez votre règlement de copropriété : un blindage qui conserve l'aspect extérieur de la porte est en général accepté sans formalités.",
    },
    "armored-door": {
        "intros": [
            "Pose de porte blindée {a} : nous installons des blocs-portes certifiés A2P BP1, BP2 ou BP3, fabriqués sur mesure et assortis à votre palier. Devis gratuit après visite.",
            "Bâti abîmé, porte trop légère, logement exposé {a} : un bloc-porte blindé complet remplace la porte et l'huisserie par une fermeture conçue pour résister à l'effraction.",
            "Vous cherchez la protection la plus complète pour votre appartement {a} ? Un bloc-porte blindé associe acier, serrure multipoints et isolation, dans une finition adaptée à votre immeuble.",
        ],
        "conseil": "Demandez à votre assureur quel niveau de certification il exige (BP1, BP2 ou BP3) avant de choisir votre modèle.",
    },
    "cellar-door": {
        "intros": [
            "Cave forcée ou mal protégée {a} ? Nous posons des blocs-portes de cave en acier avec serrure de sûreté, fabriqués aux dimensions de votre ouverture.",
            "Les caves d'immeuble sont souvent visées {a}. Une porte de cave en acier avec une vraie serrure de sûreté met fin aux cadenas fragiles et aux portes en bois qui cèdent à la première poussée.",
            "Porte de cave {a} : sécurisation en urgence après une effraction, puis porte définitive sur devis gratuit.",
        ],
        "conseil": "Prévenez votre syndic avant de remplacer la porte de votre cave, et signalez toute effraction : d'autres caves ont peut-être été visitées.",
    },
    "mailbox-lock": {
        "intros": [
            "Clé de boîte aux lettres perdue {a} ? Nous remplaçons la serrure par un modèle compatible avec des clés neuves, pour 110 € TTC sur un modèle standard.",
            "Vous venez d'emménager {a} et ne savez pas qui a la clé de la boîte aux lettres ? Changer la serrure prend peu de temps et protège votre courrier.",
            "Serrure de boîte aux lettres forcée ou bloquée {a} : nous l'ouvrons sans abîmer le portillon et posons une serrure neuve.",
        ],
        "conseil": "Si tout votre trousseau a disparu, faites vérifier le cylindre de votre porte d'entrée et la serrure de votre cave lors du même passage.",
    },
}
