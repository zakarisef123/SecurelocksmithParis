# -*- coding: utf-8 -*-
"""Contenu du site Secure Locksmith Paris (en anglais) : services, arrondissements, tarifs, conseils.

Tout le texte du site se modifie ici. Relancez ensuite : python3 _src/build.py
"""

# ---------------------------------------------------------------------------
# Services
# ---------------------------------------------------------------------------
SERVICES = [
    {
        "slug": "door-opening",
        "cat": "urgence",
        "nom": "Lockout & door opening",
        "court": "Door opening",
        "icon": "i-door",
        "prix": "from €110",
        "prix_num": 110,
        "phrase": "a door opening",
        "resume": "Locked out, keys left inside: we open your door gently, with no damage and no lock change in most cases.",
        "intro": "A gust of wind, a moment of distraction, and you are standing on the landing with your keys on the other side of the door. Don't worry: a door that has simply slammed shut (not double-locked) can almost always be opened without any damage. Our locksmiths cover the whole of Paris, day and night, with non-destructive opening tools.",
        "sections": [
            ("Slammed shut or locked: why it matters",
             "When a door is <strong>slammed shut</strong>, only the latch (the angled bolt that retracts when you turn the handle) is holding it. A flexible shim slid between the door and the frame is usually enough to open it. When the door is <strong>locked with a key</strong>, the deadbolts are engaged: opening it without damage is still possible in many cases, but it takes longer and sometimes requires drilling the cylinder, which is always explained and priced first."),
            ("Techniques that protect your door",
             "Shims, picks and cylinder bypass tools: our locksmith chooses the least invasive method for your type of door. Armored doors in Parisian buildings often have specific protections, and we carry the right tools. Drilling is only a last resort, with your consent, and the cylinder is then replaced on the spot."),
            ("While you wait",
             "Think of the building caretaker (gardien), a trusted neighbor or your letting agency: someone may have a spare key. Avoid the credit-card trick and screwdrivers: they damage the seal, the strike plate or the edge of the door, and make the job longer. If a child is inside or something is cooking on the stove, tell us on the phone and we will treat your call as a priority."),
        ],
        "faq": [
            ("How much does it cost to open a slammed door in Paris?", "€110 incl. VAT during the day (8am–6pm), €150 in the evening (6pm–10pm) and €220 at night (10pm–8am). For a door locked with a key, prices start at €180 during the day. The price is given on the phone, then confirmed in a written quote before we start."),
            ("Will my lock be damaged?", "In the vast majority of cases, no: a slammed door opens without leaving a mark. If drilling became necessary, the locksmith would explain why and give you the price beforehand, and you would remain free to say no."),
            ("How long does it take?", "Often less than ten minutes for a slammed door. An armored door or a door locked with a key can take longer."),
        ],
    },
    {
        "slug": "jammed-lock",
        "cat": "urgence",
        "nom": "Jammed lock repair",
        "court": "Jammed lock",
        "icon": "i-lock",
        "prix": "from €180",
        "prix_num": 180,
        "phrase": "a jammed lock repair",
        "resume": "Key won't turn, stiff cylinder, stuck bolt: on-site diagnosis and repair rather than replacement.",
        "intro": "The key goes in but won't turn, the handle resists, the door won't lock anymore: a jammed lock can keep you out, keep you in, or stop you from securing your apartment when you leave. Our locksmith finds the cause and repairs the mechanism whenever possible, without selling you a new lock you don't need.",
        "sections": [
            ("What causes a lock to jam?",
             "Most often: a cylinder clogged with dust or the wrong lubricant, a worn or slightly bent key, a door that has dropped so the bolt rubs against the strike plate, a broken spring inside the lock case, or a loose rod on a multi-point lock. In older buildings, changes in humidity also make wooden doors swell and shift."),
            ("Our repair, step by step",
             "If you are locked out, we open the door first. The locksmith then takes the mechanism apart, shows you the faulty part and suggests the right repair: cleaning, adjusting the strike plate, replacing a spring or, if the cylinder is worn out, fitting a new one. Common parts are carried in the van so the job can be finished the same day."),
            ("Keeping your lock smooth",
             "Once a year, a little dry lubricant (graphite or PTFE) in the keyway is enough. Avoid cooking oil and greasy sprays, which trap dust. If your door rubs or needs lifting to close, have the hinges adjusted: it is often the hidden cause of a bolt that sticks."),
        ],
        "faq": [
            ("The key spins without catching: is it serious?", "It is usually a broken key bit or a broken cam in the cylinder. Don't force it: we open the door and replace only the faulty part."),
            ("Can a 3-point lock be repaired without replacing everything?", "Yes, in most cases. We replace only the lock case, rod or cylinder concerned, not the whole system."),
            ("Will my insurance cover the repair?", "It depends on your policy and on the cause (wear or attempted break-in). We give you a detailed invoice to send to your insurer."),
        ],
    },
    {
        "slug": "broken-key",
        "cat": "urgence",
        "nom": "Broken key extraction",
        "court": "Broken key",
        "icon": "i-key",
        "prix": "free quote",
        "prix_num": None,
        "phrase": "a broken key extraction",
        "resume": "Piece of key stuck in the cylinder: clean extraction without changing the lock, plus advice on what to do next.",
        "intro": "A tired key eventually gives way, usually at the worst moment: early in the morning or late at night. In most cases, the piece left in the cylinder can be removed without taking the lock apart or replacing it.",
        "sections": [
            ("Above all, don't force it",
             "Pushing the piece with another key, a paper clip or a screwdriver drives it deeper and can jam the pins. Glue will ruin the cylinder. If the end sticks out clearly, pull it straight out with fine pliers, without turning. Otherwise, leave it to a professional."),
            ("How we remove the fragment",
             "The locksmith slides very thin extractors along the pins to hook the broken piece and pull it out. He then checks that the cylinder works with your spare key and, if it is badly worn, offers a new cylinder with several keys."),
            ("What if it was your last key?",
             "For a high-security cylinder, copies are made from the ownership card at an authorized dealer. Without a card or a spare, the simplest option is to replace the cylinder: you get new keys and the certainty that nobody else has a copy."),
        ],
        "faq": [
            ("Do I need a new lock after a key breaks?", "Not necessarily. If the cylinder is undamaged and you have a spare, extraction is enough."),
            ("How much does a key extraction cost?", "It depends on the type of cylinder and the time of day: the price is given on the phone, then confirmed in a free quote before the work starts."),
            ("My key broke in my mailbox lock", "We also work on mailbox, cellar and storage-room locks."),
        ],
    },
    {
        "slug": "lock-replacement",
        "cat": "urgence",
        "nom": "Lock & cylinder replacement",
        "court": "Lock replacement",
        "icon": "i-cyl",
        "prix": "from €160",
        "prix_num": 160,
        "phrase": "a lock replacement",
        "resume": "Lost or stolen keys, moving in, worn lock: new cylinder or A2P multi-point lock fitted the same day.",
        "intro": "Keys lost on the metro, a stolen bag, a new apartment where you don't know who has copies, a lock that has been sticking for months: changing the cylinder or the lock is the safest way to be back in control of who can get in.",
        "sections": [
            ("Cylinder only, or the whole lock?",
             "In most situations, replacing the <strong>cylinder</strong> (the barrel the key goes into) is enough: it is quick and affordable. The <strong>whole lock</strong> is replaced when the case is damaged, after a break-in, or to upgrade to a stronger 3- or 5-point lock."),
            ("Understanding A2P stars",
             "The French A2P certification, issued by the CNPP, rates resistance to break-ins: one star for 5 minutes, two for 10 minutes, three for 15 minutes. Some insurance policies require a minimum level: check yours and we will recommend the right model. High-security cylinders come with an ownership card that protects key copying."),
            ("Clear options, fitted prices",
             "The locksmith shows you several ranges, from standard to certified high security, with an all-inclusive price (part and fitting). You choose, he installs it, then hands you the invoice, the new keys and the ownership card."),
        ],
        "faq": [
            ("How much does a cylinder replacement cost?", "From €160 incl. VAT during the day (8am–6pm), €200 in the evening (6pm–10pm) and €230 at night (10pm–8am). A complete lock starts at €250. The final price depends on the brand and security level you choose: a detailed quote is given beforehand."),
            ("Should I change my lock after my keys are stolen?", "Yes, especially if documents showing your address were taken at the same time. Depending on your policy, your insurer may cover the replacement."),
            ("Tenant or landlord: who pays?", "Lost keys are usually the tenant's responsibility; replacing a worn-out lock is usually the landlord's. Your lease is the reference."),
        ],
    },
    {
        "slug": "smart-lock",
        "cat": "travaux",
        "nom": "Smart lock installation & repair",
        "court": "Smart lock",
        "icon": "i-smart",
        "prix": "free quote",
        "prix_num": None,
        "phrase": "a smart lock",
        "resume": "Installation and repair of smart locks: open with your phone, a code, a badge or your fingerprint.",
        "intro": "Opening with your phone, giving temporary access to a nanny or a short-term guest, knowing who came in and when: smart locks are increasingly popular in Paris. We install them on your existing door and step in when they stop cooperating.",
        "sections": [
            ("Installation suited to your door",
             "Depending on the model, the smart lock fits on the inside over your current cylinder, or replaces the cylinder and handle. We first check compatibility (door thickness, cylinder type, armored or not), then install it, set up the app with you and test every way of opening."),
            ("When the lock stops responding",
             "Flat batteries, an interrupted update, lost pairing, a motor straining against a misaligned bolt: we get you in if you are outside, bring the system back to life and adjust the door so the fault doesn't come back."),
            ("Good habits",
             "Always keep a mechanical backup key outside your home, choose a model paired with a certified cylinder for a front door, and replace the batteries at the first low-battery warning."),
        ],
        "faq": [
            ("My smart lock is stuck and I'm outside", "Call us: we open the door as we would with a standard lock, then get your smart lock working again."),
            ("Can one be fitted on an armored door?", "Often yes, depending on the cylinder. Send us a photo of your door on WhatsApp for a quick answer."),
            ("How much does installation cost?", "Both installation and repair come with a free quote: the price depends on the model and is given before any work starts."),
        ],
    },
    {
        "slug": "break-in-repair",
        "cat": "urgence",
        "nom": "Break-in repair & securing",
        "court": "After a break-in",
        "icon": "i-tool",
        "prix": "free quote",
        "prix_num": None,
        "phrase": "securing your home after a break-in",
        "resume": "Forced door or burglary: emergency temporary locking, lock replacement, reinforcement and paperwork for your insurer.",
        "intro": "After a burglary or an attempted break-in, there is only one priority: being able to lock your home again tonight. We secure your door as an emergency, then offer a lasting repair, with all the documents your insurer will ask for.",
        "sections": [
            ("The right steps, in order",
             "1. Don't touch anything and call the police (17) to report it. 2. File a complaint at the police station or online: your insurer will ask for the receipt. 3. Have your door secured: we work 24/7 across Paris. 4. Notify your insurer, usually within 2 working days."),
            ("Immediate securing",
             "Replacing a ripped-out cylinder, fitting a temporary lock, reinforcing the strike plate or frame, or boarding up if the door no longer closes. The goal: you can sleep safely at home tonight."),
            ("Repair and reinforcement",
             "Depending on the damage: A2P multi-point lock, anti-jemmy angle bars, cylinder guard, frame reinforcement, armoring of the existing door. We provide a detailed quote and before/after photos for your insurance assessor."),
        ],
        "faq": [
            ("Does insurance pay for the locksmith after a burglary?", "With most home insurance policies, yes, on presentation of the police report and the invoice. Ours is detailed and compliant."),
            ("Can you come before the police?", "It is better to wait for the police report. If the door doesn't close at all, we can secure it temporarily while preserving evidence."),
            ("Do you install armored doors?", "Yes: we armor existing doors and fit reinforcements, and we install complete armored door sets on quotation."),
        ],
    },
    {
        "slug": "door-armoring",
        "cat": "travaux",
        "nom": "Door armoring (reinforcement)",
        "court": "Door armoring",
        "icon": "i-shield",
        "prix": "from €2,300",
        "prix_num": 2300,
        "phrase": "armoring a door",
        "resume": "Reinforce your existing door: steel plate, multi-point lock and anti-jemmy bars, without changing its look from the landing.",
        "intro": "Armoring turns your current door into a security door, without replacing the frame or changing how it looks from outside. It is the most common solution in Parisian buildings, where the co-ownership rules often require landing doors to keep their original appearance.",
        "sections": [
            ("What door armoring includes",
             "A steel plate fixed to the inside of the door leaf, a multi-point lock with a high-security cylinder, anti-jemmy angle bars on the frame, reinforced hinges and anti-lift hinge bolts. Depending on the door, we add a threshold, a peephole or a door limiter."),
            ("Why armor rather than replace?",
             "Armoring usually costs less than a complete armored door set, is fitted in a day and keeps your original door, often solid wood in older buildings. It suits most doors in good condition. If the frame is too weak, we will tell you and suggest a complete door set instead."),
            ("A detailed quote after a visit",
             "We come to measure your door, check the frame and present several levels of protection. The quote is free and lists the equipment, the fitted price and the lead time."),
        ],
        "faq": [
            ("How much does door armoring cost in Paris?", "From €2,300 incl. VAT, fitted, depending on the size, the number of locking points and the lock chosen. The exact price is on a free quote drawn up after a visit."),
            ("Do I need the building's approval?", "The outer face of the door overlooks the common areas. Armoring that keeps the door's appearance from the landing rarely raises objections, but check your building's co-ownership rules."),
            ("How long does fitting take?", "Usually one day: your door is closed and secure the same evening."),
        ],
    },
    {
        "slug": "armored-door",
        "cat": "travaux",
        "nom": "Armored door installation",
        "court": "Armored door",
        "icon": "i-door",
        "prix": "from €3,350",
        "prix_num": 3350,
        "phrase": "an armored door installation",
        "resume": "A2P BP1, BP2 or BP3 certified armored door set: door, frame and multi-point lock designed together and made to measure.",
        "intro": "A complete armored door set is the highest level of protection: the door and its frame are designed together, in steel, with a built-in multi-point lock. It is the recommended solution when the existing frame is damaged, after a violent break-in, or for the most exposed homes.",
        "sections": [
            ("Certification levels",
             "The French A2P BP certification, issued by the CNPP, rates a door set's resistance to break-ins: BP1 (5 minutes), BP2 (10 minutes), BP3 (15 minutes). Some insurers require a minimum level: check your policy and we will recommend the right model."),
            ("A finish that suits your building",
             "Armored door sets come in many finishes (wood, mouldings, colors) to match Parisian landings and the building's rules. They also improve sound and heat insulation."),
            ("From measurements to fitting",
             "Visit and measurements, detailed quote, made-to-measure order, then fitting, usually in one day, including removal of the old door. The manufacturing lead time is shown on the quote; if needed, we secure your current door in the meantime."),
        ],
        "faq": [
            ("What budget for an armored door?", "From €3,350 incl. VAT, fitted. The price depends on the certification level, the size and the finish: a free quote is given after a visit."),
            ("Armoring or a new armored door: which one?", "If your door and frame are in good condition, armoring is often enough. If the frame is weak or damaged, a complete door set is safer. We advise you after seeing your door."),
            ("Is fitting messy?", "No: the old frame is removed cleanly, the new door set is adjusted and the finishes are restored. We protect the landing and your apartment during the work."),
        ],
    },
    {
        "slug": "cellar-door",
        "cat": "travaux",
        "nom": "Armored cellar door",
        "court": "Cellar door",
        "icon": "i-lock",
        "prix": "from €1,550",
        "prix_num": 1550,
        "phrase": "an armored cellar door",
        "resume": "Cellar broken into or poorly protected: steel cellar door set with a security lock, made to fit your opening.",
        "intro": "Cellars in Parisian buildings are frequent targets: flimsy wooden doors, weak padlocks, dimly lit corridors. A steel cellar door set with a proper security lock protects what you store there for good.",
        "sections": [
            ("A door built for basements",
             "Steel frame and leaf, security or multi-point lock, reinforced hinges and a damp-resistant finish. The door is made to the size of your opening, which is often irregular in older buildings."),
            ("After a cellar break-in",
             "We first secure access (temporary lock, reinforcement), then offer a permanent door. Remember to file a police report and inform your building manager (syndic): other cellars may have been hit too."),
            ("In agreement with the building",
             "As cellars are located in the common areas, it is advisable to inform the building manager before replacing the door. We can provide a technical description."),
        ],
        "faq": [
            ("How much does an armored cellar door cost?", "From €1,550 incl. VAT, fitted, depending on the size and the lock. Free quote after a visit."),
            ("Can you just change the cellar lock?", "Yes. If the door is sound, a new lock or an added security bolt may be enough: we will tell you on site."),
            ("My cellar was broken into last night", "Call us: we secure access quickly, on quotation, and give you an invoice for your insurer."),
        ],
    },
    {
        "slug": "mailbox-lock",
        "cat": "travaux",
        "nom": "Mailbox lock replacement",
        "court": "Mailbox lock",
        "icon": "i-mail",
        "prix": "from €110",
        "prix_num": 110,
        "phrase": "a mailbox lock replacement",
        "resume": "Lost key, broken lock or moving in: we replace the lock on your mailbox and supply new keys.",
        "intro": "A lost key, a forced lock, a new occupant: replacing a mailbox lock is a quick job that keeps your mail out of anyone else's hands.",
        "sections": [
            ("A lock that fits your mailbox",
             "Building mailboxes use standardized locks. We identify the model and fit a compatible lock, supplied with its keys."),
            ("Opening without damage",
             "If you no longer have a key, we open the mailbox without damaging the flap, then replace the lock."),
            ("What about your other locks?",
             "If you lost your whole key ring, think about your front-door cylinder and your cellar too: we can handle everything in a single visit."),
        ],
        "faq": [
            ("How much does a mailbox lock replacement cost?", "€110 incl. VAT for a standard model. Special models come with a free quote."),
            ("Tenant or landlord: who pays?", "A lost key is usually the tenant's responsibility, wear and tear the landlord's. Your lease is the reference."),
            ("Do you work on badge or code mailboxes?", "Depending on the model, yes. Send us a photo on WhatsApp so we can check."),
        ],
    },
]

# ---------------------------------------------------------------------------
# 24/7 emergencies: (situation, linked service, displayed price, what to do meanwhile)
# ---------------------------------------------------------------------------
URGENCES = [
    ("Door slammed shut, keys inside", "door-opening", "€110", "Don't use a credit card or screwdriver: you would damage the strike plate."),
    ("Door locked, keys lost", "door-opening", "from €180", "Ask the caretaker or a neighbor whether they keep a spare."),
    ("Jammed lock, key won't turn", "jammed-lock", "€180", "Don't force it: you could snap the key inside the cylinder."),
    ("Key broken in the lock", "broken-key", "quote", "Don't push the piece in further and never use glue."),
    ("Burglary, door forced open", "break-in-repair", "quote", "Call the police (17) and don't touch anything before they come."),
    ("Keys stolen: change the cylinder", "lock-replacement", "from €160", "If your ID was stolen too, have the cylinder changed today."),
    ("Smart lock not responding", "smart-lock", "quote", "Look for your mechanical backup key before calling."),
    ("Cellar broken into", "cellar-door", "quote", "Tell the building manager: other cellars may have been hit too."),
]

# ---------------------------------------------------------------------------
# The 20 arrondissements
# n: (nickname, INSEE population, postcodes, administrative quarters, landmarks, metro stations, housing)
# ---------------------------------------------------------------------------
ARRONDISSEMENTS = {
    1: ("Louvre", 15114, ["75001"], ["Saint-Germain-l'Auxerrois", "Halles", "Palais-Royal", "Place-Vendôme"],
        ["Rue Saint-Honoré", "the Tuileries Garden", "the Forum des Halles"], ["Louvre-Rivoli", "Pyramides", "Tuileries"],
        "historic apartments above shops, private mansions and many offices"),
    2: ("Bourse", 19847, ["75002"], ["Gaillon", "Vivienne", "Mail", "Bonne-Nouvelle"],
        ["the covered passages", "Rue Réaumur", "the Sentier district"], ["Bourse", "Sentier", "Quatre-Septembre"],
        "19th-century apartment buildings, workshops turned into lofts and small businesses"),
    3: ("Temple", 32179, ["75003"], ["Arts-et-Métiers", "Enfants-Rouges", "Archives", "Sainte-Avoye"],
        ["the Picasso Museum", "Square du Temple", "Rue de Bretagne"], ["Temple", "Arts et Métiers", "Filles du Calvaire"],
        "Marais mansions, cobbled courtyards and buildings with large carriage doors"),
    4: ("Hôtel-de-Ville", 27332, ["75004"], ["Saint-Merri", "Saint-Gervais", "Arsenal", "Notre-Dame"],
        ["Place des Vosges", "the Centre Pompidou", "Île de la Cité"], ["Saint-Paul", "Hôtel de Ville", "Pont Marie"],
        "17th- and 18th-century buildings, attic rooms and Marais boutiques"),
    5: ("Panthéon", 55252, ["75005"], ["Saint-Victor", "Jardin-des-Plantes", "Val-de-Grâce", "Sorbonne"],
        ["the Arènes de Lutèce", "Place de la Contrescarpe", "the Jardin des Plantes"], ["Maubert-Mutualité", "Place Monge", "Cardinal Lemoine"],
        "student studios, old buildings and university residences"),
    6: ("Luxembourg", 40389, ["75006"], ["Monnaie", "Odéon", "Notre-Dame-des-Champs", "Saint-Germain-des-Prés"],
        ["Boulevard Saint-Germain", "Rue de Rennes", "the Odéon Theatre"], ["Odéon", "Mabillon", "Saint-Placide"],
        "elegant apartments, art galleries and high-end armored doors"),
    7: ("Palais-Bourbon", 48015, ["75007"], ["Saint-Thomas-d'Aquin", "Invalides", "École-Militaire", "Gros-Caillou"],
        ["the Champ de Mars", "the Musée d'Orsay", "Rue Cler"], ["École Militaire", "Solférino", "La Tour-Maubourg"],
        "upscale Haussmann buildings, ministries and large family apartments"),
    8: ("Élysée", 35317, ["75008"], ["Champs-Élysées", "Faubourg-du-Roule", "Madeleine", "Europe"],
        ["Place de la Concorde", "Rue du Faubourg-Saint-Honoré", "Boulevard Haussmann"], ["Miromesnil", "Saint-Augustin", "George V"],
        "head offices, luxury boutiques and vast Haussmann apartments"),
    9: ("Opéra", 57271, ["75009"], ["Saint-Georges", "Chaussée-d'Antin", "Faubourg-Montmartre", "Rochechouart"],
        ["the department stores", "Rue des Martyrs", "Nouvelle Athènes"], ["Notre-Dame-de-Lorette", "Cadet", "Le Peletier"],
        "Haussmann buildings, offices and family apartments"),
    10: ("Entrepôt", 83873, ["75010"], ["Saint-Vincent-de-Paul", "Porte-Saint-Denis", "Porte-Saint-Martin", "Hôpital-Saint-Louis"],
         ["the Canal Saint-Martin", "Gare du Nord", "Rue du Faubourg-Saint-Denis"], ["Jacques Bonsergent", "Château d'Eau", "Colonel Fabien"],
         "old buildings, courtyard workshops and a great many shops"),
    11: ("Popincourt", 138170, ["75011"], ["Folie-Méricourt", "Roquette", "Sainte-Marguerite", "Saint-Ambroise"],
         ["Rue de la Roquette", "Boulevard Voltaire", "Rue Oberkampf"], ["Voltaire", "Parmentier", "Charonne"],
         "small working-class buildings, passages and former workshops turned into homes"),
    12: ("Reuilly", 138024, ["75012"], ["Bel-Air", "Picpus", "Bercy", "Quinze-Vingts"],
         ["the Coulée Verte", "Cour Saint-Émilion", "the Bois de Vincennes"], ["Nation", "Daumesnil", "Dugommier"],
         "residences from the 1970s to the 2000s, Haussmann buildings and the new Bercy district"),
    13: ("Gobelins", 181271, ["75013"], ["Salpêtrière", "Gare", "Maison-Blanche", "Croulebarbe"],
         ["Avenue de Choisy", "Paris Rive Gauche", "the Gobelins Manufactory"], ["Tolbiac", "Olympiades", "Bibliothèque François-Mitterrand"],
         "the Olympiades towers, modern residences with door codes and the houses of the Butte-aux-Cailles"),
    14: ("Observatoire", 136455, ["75014"], ["Montparnasse", "Parc-de-Montsouris", "Petit-Montrouge", "Plaisance"],
         ["Rue Daguerre", "Parc Montsouris", "the Cité Universitaire"], ["Mouton-Duvernet", "Pernety", "Plaisance"],
         "brick buildings, houses, artists' studios and large housing estates"),
    15: ("Vaugirard", 229713, ["75015"], ["Saint-Lambert", "Necker", "Grenelle", "Javel"],
         ["the Front de Seine", "Parc André-Citroën", "Rue du Commerce"], ["Commerce", "Vaugirard", "Félix Faure"],
         "Front de Seine towers, 1930s buildings and many family residences"),
    16: ("Passy", 159386, ["75016", "75116"], ["Auteuil", "Muette", "Porte-Dauphine", "Chaillot"],
         ["Rue de Passy", "Avenue Victor-Hugo", "the Bois de Boulogne"], ["La Muette", "Ranelagh", "Michel-Ange-Auteuil"],
         "private mansions, gated villas and apartments fitted with armored doors"),
    17: ("Batignolles-Monceau", 159212, ["75017"], ["Ternes", "Plaine-de-Monceaux", "Batignolles", "Épinettes"],
         ["Parc Clichy-Batignolles", "Avenue de Wagram", "Rue de Lévis"], ["Brochant", "Wagram", "Guy Môquet"],
         "Haussmann buildings, the Clichy-Batignolles eco-district and the small houses of Épinettes"),
    18: ("Butte-Montmartre", 183127, ["75018"], ["Grandes-Carrières", "Clignancourt", "Goutte-d'Or", "La Chapelle"],
         ["Place du Tertre", "Rue Lepic", "the flea market"], ["Lamarck-Caulaincourt", "Jules Joffrin", "Marcadet-Poissonniers"],
         "old buildings with narrow staircases, artists' studios and recent residences"),
    19: ("Buttes-Chaumont", 178691, ["75019"], ["La Villette", "Pont-de-Flandre", "Amérique", "Combat"],
         ["the Bassin de la Villette", "Parc des Buttes-Chaumont", "La Mouzaïa"], ["Laumière", "Ourcq", "Botzaris"],
         "large housing estates, badge-access residences and the houses of La Mouzaïa"),
    20: ("Ménilmontant", 185140, ["75020"], ["Belleville", "Saint-Fargeau", "Père-Lachaise", "Charonne"],
         ["Parc de Belleville", "Rue des Pyrénées", "the village of Charonne"], ["Pyrénées", "Gambetta", "Porte de Bagnolet"],
         "working-class buildings, artisans' yards, social housing and townhouses"),
}

# ---------------------------------------------------------------------------
# Price list (incl. VAT): service, day 8am–6pm, evening 6pm–10pm, night 10pm–8am
# None = quote only for that time slot. "From …" = starting price.
# ---------------------------------------------------------------------------
TARIFS = [
    ("Slammed door opening", "€110", "€150", "€220"),
    ("Locked door opening", "From €180", "From €240", "From €280"),
    ("Jammed lock, key won't turn", "€180", "€240", "€280"),
    ("Cylinder replacement", "From €160", "From €200", "From €230"),
    ("Lock replacement", "From €250", None, None),
    ("Door armoring", "From €2,300", None, None),
    ("Complete armored door set", "From €3,350", None, None),
    ("Cellar door set", "From €1,550", None, None),
    ("Mailbox lock (standard model)", "€110", None, None),
]

# Insurers (name, logo file in assets/img/assureurs/ or None) – mentioned for information only, no partnership
ASSUREURS = [
    # Assureurs habitation et bancassureurs (liste vérifiée en novembre 2026)
    ("AXA", "axa"), ("Allianz", "allianz"), ("MAIF", "maif"), ("MACIF", "macif"), ("MAAF", "maaf"),
    ("Groupama", "groupama"), ("Generali", "generali"), ("Matmut", "matmut"), ("Caisse d'Épargne", "caisse-epargne"),
    ("Abeille Assurances", "abeille"), ("Swiss Life", "swiss-life"), ("AG2R La Mondiale", "ag2r"),
    ("Thélem", "thelem"), ("GAN", "gan"), ("MAE", "mae"), ("MACSF", "macsf"), ("Direct Assurance", "direct-assurance"),
    ("L'olivier Assurance", "lolivier"), ("Hiscox", "hiscox"), ("April", "april"), ("Assu 2000", "assu2000"),
    ("Sogessur", "sogessur"), ("Euro-Assurance", "euro-assurance"),
    ("GMF", None), ("MMA", None), ("Crédit Agricole Assurances", None), ("BNP Paribas Cardif", None),
    ("Société Générale Assurances", None), ("LCL", None), ("Crédit Mutuel", None), ("CIC", None),
    ("La Banque Postale", None), ("Banque Populaire", None), ("Allianz Direct", None), ("Leocare", None),
    ("Mutuelle de Poitiers Assurances", None),
]

# Brands we work on (name, logo file in assets/img/marques/, category)
MARQUES = [
    ("Point Fort Fichet", "point-fort-fichet", "Locks"), ("Picard", "picard", "Locks"), ("Vachette", "vachette", "Locks"),
    ("Bricard", "bricard", "Locks"), ("Héraclès", "heracles", "Locks"), ("Pollux", "pollux", "Locks"),
    ("JPM", "jpm", "Locks"), ("Thirard", "thirard", "Locks"), ("Metalux", "metalux", "Locks"),
    ("Laperche", "laperche", "Locks"), ("Stremler", "stremler", "Locks"), ("Mul-T-Lock", "mul-t-lock", "Locks"),
    ("Abus", "abus", "Locks"), ("DOM", "dom", "Locks"), ("EVVA", "evva", "Locks"), ("dormakaba", "kaba", "Locks"),
    ("Keso", "keso", "Locks"), ("Iseo", "iseo", "Locks"), ("Cisa", "cisa", "Locks"), ("Mottura", "mottura", "Locks"),
    ("Tesa", "tesa", "Locks"), ("Yale", "yale", "Locks"),
    ("Tordjman Métal", "tordjman", "Armored doors"), ("Bel'M", "belm", "Armored doors"), ("K•Line", "kline", "Armored doors"),
    ("Zilten", "zilten", "Armored doors"), ("Lapeyre", "lapeyre", "Armored doors"), ("Tryba", "tryba", "Armored doors"),
    ("Dierre", "dierre", "Armored doors"), ("Gardesa", "gardesa", "Armored doors"), ("Hörmann", "hormann", "Armored doors"),
    ("Somfy", "somfy", "Smart locks"), ("Netatmo", "netatmo", "Smart locks"), ("Nuki", "nuki", "Smart locks"),
    ("Ultion", "ultion", "Smart locks"), ("Danalock", "danalock", "Smart locks"), ("Bold", "bold", "Smart locks"),
    ("Igloohome", "igloohome", "Smart locks"),
]

# ---------------------------------------------------------------------------
# Google reviews: paste REAL reviews from your Google Business Profile here (never invented ones).
# Format: {"auteur": "Marie L.", "note": 5, "date": "October 2026", "texte": "…", "arr": "Paris 15th"}
# While the list is empty, the site shows the Google rating and a link to the profile.
# ---------------------------------------------------------------------------
AVIS = []

# ---------------------------------------------------------------------------
# Advice (blog)
# ---------------------------------------------------------------------------
ARTICLES = [
    {
        "slug": "lost-keys-paris",
        "titre": "Lost your keys in Paris? 5 things to do right away",
        "court": "Lost keys: 5 things to do",
        "cat": "Emergency", "date": "2026-10-20", "icon": "i-key",
        "desc": "Keys dropped on the metro, bag stolen on a café terrace: what to do within the hour to get back home and stay safe.",
        "corps": [
            ("p", "Lost keys are one of the most common emergencies in Paris: a key ring slipping out of a pocket on the metro, a bag left on a terrace, a borrowed jacket. Here is what to do, in order."),
            ("h2", "1. Calmly retrace your steps"),
            ("p", "Call the last places you visited (café, office, gym). The Paris Police Lost Property Office (Préfecture de police) also centralizes items handed in on public transport and in the street, and can be searched online."),
            ("h2", "2. Look for a spare key"),
            ("ul", ["A relative or a trusted neighbor?", "The building caretaker (gardien)?", "Your letting agency or landlord?"]),
            ("h2", "3. Assess the risk"),
            ("p", "If your keys were with a document showing your address (ID card, mail, car registration), assume a stranger could get in: <strong>changing the cylinder</strong> becomes the priority. With no address attached, the risk is lower, but a replacement is still advisable if you have any doubt."),
            ("h2", "4. Get your door opened without damage"),
            ("p", "If the door is only slammed shut, a locksmith opens it in a few minutes without damaging the lock. If it is double-locked, opening without damage is often still possible, and the cylinder can be replaced straight away. At Secure Locksmith Paris, the price is given on the phone before we travel."),
            ("h2", "5. Tell your insurer"),
            ("p", "Some policies cover lost or stolen keys. Keep the detailed invoice and, in case of theft, the police report."),
        ],
    },
    {
        "slug": "armored-door-paris-apartment",
        "titre": "Armored doors in Parisian buildings: what to know before you start",
        "court": "Armored doors in Paris: the guide",
        "cat": "Security", "date": "2026-09-30", "icon": "i-shield",
        "desc": "Armoring your existing door or a new door set, building approval, A2P certification: the questions to ask for an apartment.",
        "corps": [
            ("p", "In a Parisian apartment, the front door is the main entry point for burglars. Armoring it is one of the most effective investments in your home's security, provided you choose well."),
            ("h2", "Armoring or a new door set?"),
            ("p", "<strong>Armoring</strong> reinforces your current door with a steel plate, a multi-point lock and angle bars. It keeps the door's outside appearance, which building co-ownerships usually appreciate. A <strong>door set</strong> replaces everything (door and frame): it is the strongest solution, with A2P BP1, BP2 or BP3 certification."),
            ("h2", "What about the building rules?"),
            ("p", "The outside of your front door faces the common areas. If its appearance changes (color, mouldings, material), the co-ownership rules may require approval or a specific model. Armoring that keeps the outer panel rarely causes problems, but check your rules anyway."),
            ("h2", "What to check"),
            ("ul", ["The lock: multi-point, with an A2P-certified cylinder and an ownership card.", "The hinges: anti-lift.", "The frame: reinforced, otherwise even the strongest door gives way at the side.", "Sound and heat insulation, welcome in older buildings."]),
            ("p", "Our locksmiths will come and assess your door for free and give you a detailed quote."),
        ],
    },
    {
        "slug": "spot-an-honest-locksmith",
        "titre": "How to spot an honest locksmith (and avoid scams)",
        "court": "Spotting an honest locksmith",
        "cat": "Advice", "date": "2026-09-08", "icon": "i-award",
        "desc": "Misleading flyers, vague prices, locks drilled for no reason: the warning signs and the rights that protect you.",
        "corps": [
            ("p", "Emergency locksmith services generate a large share of consumer complaints in France. A few simple habits are enough to avoid nasty surprises."),
            ("h2", "Warning signs"),
            ("ol", ["A sticker or flyer with an \"emergency number\" imitating the town hall or the building manager.", "A vague price on the phone, or \"from €19\" with no further detail.", "No written quote before the work starts.", "An offer to drill or replace the lock when the door was simply slammed shut.", "Cash-only payment, without an invoice.", "A company with no name, no registration number and no verifiable reviews."]),
            ("h2", "What French law requires"),
            ("p", "For a home call-out, the professional must inform you of their prices and give you a <strong>detailed quote</strong> before the work when the price can be determined in advance. You can refuse it. A <strong>detailed invoice</strong> must be given to you at the end."),
            ("h2", "If there is a dispute"),
            ("p", "Keep every document, dispute the bill in writing, report the practice on the government's SignalConso website and contact the consumer mediator named by the company."),
            ("h2", "How we work"),
            ("p", "At Secure Locksmith Paris, the price is given on the phone, confirmed by a signed quote, and the invoice is detailed for your insurer. Our reviews are public on our Google Business Profile."),
        ],
    },
    {
        "slug": "after-a-burglary",
        "titre": "After a burglary: securing your apartment within 24 hours",
        "court": "After a burglary: what to do",
        "cat": "Emergency", "date": "2026-08-18", "icon": "i-tool",
        "desc": "Police report, complaint, insurance, temporary locking then reinforcement: an hour-by-hour action plan.",
        "corps": [
            ("p", "Finding your door forced open is a shock. To forget nothing and quickly have a home that locks again, follow this plan."),
            ("h2", "Within the hour"),
            ("ul", ["Don't go in if you think someone may still be inside: call the police (17).", "Don't touch anything before the police report.", "Photograph the damage (door, lock, rooms)."]),
            ("h2", "During the day"),
            ("ul", ["File a complaint (at a police station or pre-complaint online).", "Cancel any stolen bank cards.", "Have your door secured: a locksmith fits a new cylinder or a temporary lock."]),
            ("h2", "Within 2 working days"),
            ("p", "Notify your insurer with the police report receipt, the list of stolen items and the locksmith's invoice."),
            ("h2", "Then: reinforce"),
            ("p", "A2P multi-point lock, cylinder guard, anti-jemmy angle bars, door armoring: we suggest reinforcements suited to your door and budget, with a detailed quote for the insurance assessor."),
        ],
    },
]

# ---------------------------------------------------------------------------
# Trust content
# ---------------------------------------------------------------------------
# Comparison: abusive practices in the industry / how we work
COMPARATIF = [
    ("A \"from €19\" price on the phone, then an invoice for several hundred euros.",
     "A real price given on the phone from your description, and our rates published on this website."),
    ("The work starts before you have signed anything.",
     "A written, signed quote before any work. Without your signature, nothing starts."),
    ("The lock is drilled or replaced even though the door was simply slammed shut.",
     "Non-destructive opening first. Drilling is only offered as a last resort, explained and priced."),
    ("Cash-only payment, with no invoice or an unreadable one.",
     "Card, cash or bank transfer, your choice, with a detailed invoice every time."),
    ("A number found on a sticker imitating the town hall or the building manager.",
     "An identified company: name, address, Google Business Profile and verifiable public reviews."),
    ("A call center that sells your call to the highest-bidding locksmith.",
     "A locksmith who answers the phone himself and comes in person, day or night."),
]

# Trust charter (/our-commitments/ page)
CHARTE = [
    ("i-euro", "1. The price is given before we travel",
     "On the phone, we ask you a few simple questions: is the door slammed shut or locked? Armored or not? What type of lock? From your answers, we give you a price including VAT, depending on the time of day. That price matches our published price list. If you prefer, send a photo of your door on WhatsApp for an even more accurate estimate."),
    ("i-file", "2. A written, signed quote before any work",
     "On site, the locksmith assesses the situation and gives you a detailed quote: what will be done, any parts, the price including VAT. You read it, ask your questions, and sign. Not before. It is a legal requirement in France (decree of 24 January 2017) that we apply to every job, without exception, including at night."),
    ("i-door", "3. No unnecessary damage, no unnecessary replacement",
     "A slammed door can almost always be opened without damage. We always start with non-destructive techniques (shims, picking, cylinder bypass). If drilling or replacement becomes necessary, the locksmith explains why, shows you the faulty part and tells you the price before doing it. You remain free to refuse."),
    ("i-shield", "4. Quality equipment suited to your door",
     "When a part has to be replaced, we offer several ranges, from a standard cylinder to an A2P-certified high-security one, with their fitted prices. We work with recognized brands (Fichet, Picard, Vachette, Bricard, Mul-T-Lock…) and hand you the new keys and, where applicable, the ownership card."),
    ("i-card", "5. Clear payment and a detailed invoice",
     "You pay what is on the signed quote, no more, no less. Card, cash or bank transfer: it's your choice. The invoice details the work and the parts and is suitable for your home insurance claim."),
    ("i-building", "6. An identifiable company",
     "Our name, address, phone number and Google Business Profile appear on every page of this website. Our reviews are posted by customers on Google: they are public and we can neither edit nor delete them. You can read them before you even call us."),
    ("i-phone", "7. A direct contact, 24/7",
     "When you call, a locksmith answers, not a call center passing on your request. The same person follows your job from the call to the invoice, and remains reachable afterwards if you have a question."),
    ("i-home", "8. Respect for your home",
     "We protect the floor when needed, leave the place clean and explain what was done. After a break-in, we advise you on the next steps (police report, insurance) and on useful reinforcements, without pushing you into work you don't need."),
]

# What the price includes (service pages)
INCLUS = [
    "Travel within Paris, free if work is carried out",
    "The locksmith's labor",
    "On-site diagnosis and explanations",
    "A written quote, free and with no obligation",
    "A detailed invoice for your insurer",
    "VAT: our prices are always shown including VAT",
]

# ---------------------------------------------------------------------------
# Réalisations avant / après (pages services) : déposez les photos dans assets/img/realisations/
# Format : "slug-du-service": [{"before": "fichier-avant.jpg", "after": "fichier-apres.jpg",
#                              "caption": "Paris 11th · 3-point to 7-point armored door, fitted in one day"}]
# Uniquement de vraies photos de chantiers du client.
# ---------------------------------------------------------------------------
REALISATIONS = {}

# ---------------------------------------------------------------------------
# Interventions récentes par arrondissement (pages arrondissement), sans nom de client.
# Format : 11: [("Nov 2026", "Rue de la Roquette", "Slammed door opened without damage in 8 min")]
# ---------------------------------------------------------------------------
INTERVENTIONS = {}
