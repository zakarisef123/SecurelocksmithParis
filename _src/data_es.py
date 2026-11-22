# -*- coding: utf-8 -*-
"""Versión española del contenido del sitio (misma estructura que data.py y data_fr.py).

Los « slug » siguen siendo los de la versión inglesa: sirven para las fotos y los anclajes.
Las direcciones españolas (/es/servicios/apertura-de-puertas/…) se calculan en build.py.
Después, vuelva a ejecutar: python3 _src/build.py
"""

# ---------------------------------------------------------------------------
# Servicios
# ---------------------------------------------------------------------------
SERVICES = [
    {
        "slug": "door-opening",
        "cat": "urgence",
        "nom": "Apertura de puertas",
        "court": "Apertura de puerta",
        "icon": "i-door",
        "prix": "desde 110 € IVA incl.",
        "prix_num": 110,
        "phrase": "una apertura de puerta",
        "resume": "Puerta cerrada de golpe, llaves olvidadas dentro: apertura cuidadosa, sin daños ni cambio de cerradura en la mayoría de los casos.",
        "intro": "Una corriente de aire, un gesto automático, y ya está en el rellano con las llaves al otro lado de la puerta. Tranquilo: una puerta simplemente cerrada de golpe, es decir, sin echar la llave, se abre casi siempre sin ningún daño. Nuestros cerrajeros intervienen en todo París, de día y de noche, con herramientas de apertura fina.",
        "sections": [
            ("Cerrada de golpe o cerrada con llave: qué cambia para la apertura",
             "Cuando la puerta está <strong>cerrada de golpe</strong>, solo la sujeta el resbalón (la lengüeta que se retrae al girar la manilla). Una lámina flexible deslizada entre la hoja y el marco suele bastar para abrirla. Cuando está <strong>cerrada con llave</strong>, trabajan los pestillos: la apertura sin daños sigue siendo posible en muchos casos, pero lleva más tiempo y a veces requiere taladrar el bombín, siempre explicado y presupuestado antes."),
            ("Técnicas que respetan su puerta",
             "Láminas, ganzúas, herramientas para sortear el bombín: nuestro cerrajero elige el método menos invasivo para su modelo de puerta. Las puertas blindadas de los edificios parisinos suelen tener protecciones específicas; contamos con las herramientas adecuadas. Solo se taladra como último recurso, con su acuerdo, y el bombín se sustituye en el momento."),
            ("Mientras espera",
             "Piense en el conserje del edificio, en un vecino de confianza o en su agencia: quizá alguien tenga una copia. Evite la tarjeta bancaria y el destornillador: dañan la junta, el cerradero o el canto de la puerta, y la apertura se alarga. Si hay un niño dentro o algo en el fuego, díganoslo por teléfono: la intervención se atiende con prioridad."),
        ],
        "faq": [
            ("¿Cuánto cuesta abrir una puerta cerrada de golpe en París?", "110 € IVA incl. entre semana de día (8:00–18:00), 160 € por la tarde (18:00–22:00, y de 8:00 a 22:00 los fines de semana y festivos) y 220 € por la noche (22:00–8:00). Para una puerta cerrada con llave, cuente desde 180 € de día. El precio se anuncia por teléfono y después se confirma con un presupuesto escrito antes de la intervención."),
            ("¿Se dañará mi cerradura?", "En la inmensa mayoría de los casos, no: una puerta cerrada de golpe se abre sin dejar marcas. Si hiciera falta taladrar, el cerrajero le explicaría por qué y le daría el precio antes, y usted sería libre de negarse."),
            ("¿Cuánto se tarda en abrir?", "A menudo menos de diez minutos para una puerta cerrada de golpe. Una puerta blindada o cerrada con llave puede llevar más tiempo."),
        ],
    },
    {
        "slug": "jammed-lock",
        "cat": "urgence",
        "nom": "Desbloqueo de cerraduras",
        "court": "Cerradura bloqueada",
        "icon": "i-lock",
        "prix": "desde 180 € IVA incl.",
        "prix_num": 180,
        "phrase": "un desbloqueo de cerradura",
        "resume": "Llave que no gira, bombín agarrotado, pestillo atascado: diagnóstico en el sitio y reparación en lugar de sustitución.",
        "intro": "La llave entra pero no gira, la manilla se resiste, la puerta ya no cierra: una cerradura bloqueada puede impedirle entrar o salir, o cerrar su piso al marcharse. Nuestro cerrajero identifica el origen del bloqueo y repara el mecanismo siempre que es posible, sin venderle una cerradura nueva innecesaria.",
        "sections": [
            ("¿De dónde viene el bloqueo?",
             "Lo más habitual: un bombín sucio por el polvo o por un mal lubricante, una llave gastada o ligeramente torcida, una puerta que ha cedido y cuyo pestillo roza con el cerradero, un muelle roto dentro de la caja, o una varilla suelta en una cerradura multipunto. En los edificios antiguos, los cambios de humedad también hacen que la madera de las puertas se hinche y se mueva."),
            ("Nuestra intervención, paso a paso",
             "Si está fuera, primero abrimos la puerta. Después, el cerrajero desmonta el mecanismo, le enseña la pieza causante y le propone la reparación adecuada: limpieza, ajuste del cerradero, sustitución de un muelle o, si el bombín ya no sirve, colocación de un bombín nuevo. Las piezas habituales van en la furgoneta para terminar el mismo día."),
            ("Mantener una cerradura suave",
             "Una vez al año, basta con un poco de lubricante seco (grafito o PTFE) en el bombín. Olvídese del aceite de cocina y de los espráis grasos que atrapan el polvo. Si su puerta roza o hay que levantarla para cerrar, haga ajustar las bisagras: suele ser la causa oculta de un pestillo que se resiste."),
        ],
        "faq": [
            ("La llave gira en vacío: ¿es grave?", "A menudo se ha roto el paletón de la llave o la leva del bombín. No insista: abrimos la puerta y sustituimos solo la pieza defectuosa."),
            ("¿Se puede reparar una cerradura de 3 puntos sin cambiarla entera?", "Sí, en la mayoría de los casos. Se sustituye solo la caja, la varilla o el bombín afectado, sin cambiar todo el conjunto."),
            ("¿Cubre mi seguro la reparación?", "Depende de su póliza y de la causa (desgaste o intento de robo). Le entregamos una factura detallada para enviar a su aseguradora."),
        ],
    },
    {
        "slug": "broken-key",
        "cat": "urgence",
        "nom": "Extracción de llaves rotas",
        "court": "Llave rota",
        "icon": "i-key",
        "prix": "presupuesto gratuito",
        "prix_num": None,
        "phrase": "la extracción de una llave rota",
        "resume": "Trozo de llave atascado en el bombín: extracción limpia sin cambiar la cerradura, y consejos para después.",
        "intro": "Una llave cansada acaba cediendo un día, y suele ser en el peor momento: temprano por la mañana o tarde por la noche. En la mayoría de los casos, el trozo que queda en el bombín puede retirarse sin desmontar ni sustituir la cerradura.",
        "sections": [
            ("Sobre todo, no fuerce",
             "Empujar el trozo con otra llave, un clip o un destornillador lo hunde más y puede bloquear los pitones. Y el pegamento inutiliza el bombín. Si el extremo sobresale claramente, tire de él en línea recta con unos alicates finos, sin girar. Si no, deje que lo haga un profesional."),
            ("Cómo retiramos el trozo",
             "El cerrajero desliza extractores muy finos a lo largo de los pitones para enganchar el trozo y sacarlo hacia fuera. Después comprueba que el bombín funciona con su copia y, si el desgaste es importante, le propone un bombín nuevo con varias llaves."),
            ("¿Y si era su última llave?",
             "En un bombín de seguridad, la copia se hace a partir de la tarjeta de propiedad en un distribuidor autorizado. Sin tarjeta ni copia, lo más sencillo es sustituir el bombín: se queda con llaves nuevas y con la certeza de que nadie más las tiene."),
        ],
        "faq": [
            ("¿Hay que cambiar la cerradura tras romperse una llave?", "No necesariamente. Si el bombín no está dañado y tiene una copia, basta con la extracción."),
            ("¿Cuánto cuesta extraer una llave rota?", "El precio depende del tipo de bombín y de la hora: se le anuncia por teléfono y después se confirma con un presupuesto gratuito antes de la intervención."),
            ("Se me ha roto la llave en el buzón", "También trabajamos en cerraduras de buzón, de trastero y de locales."),
        ],
    },
    {
        "slug": "lock-replacement",
        "cat": "urgence",
        "nom": "Cambio de cerraduras y bombines",
        "court": "Cambio de cerradura",
        "icon": "i-cyl",
        "prix": "desde 160 € IVA incl.",
        "prix_num": 160,
        "phrase": "un cambio de cerradura",
        "resume": "Llaves perdidas o robadas, mudanza, cerradura gastada: bombín nuevo o cerradura multipunto A2P instalados el mismo día.",
        "intro": "Llavero perdido en el metro, bolso robado, piso nuevo del que no sabe quién tiene copias, cerradura que se engancha desde hace meses: cambiar el bombín o la cerradura es la forma más segura de volver a ser el único que controla sus accesos.",
        "sections": [
            ("¿Solo el bombín o la cerradura completa?",
             "En la mayoría de las situaciones basta con sustituir el <strong>bombín</strong> (el cilindro en el que entra la llave): es rápido y económico. La <strong>cerradura completa</strong> se cambia cuando la caja está dañada, tras un robo, o para pasar a un cierre de 3 o 5 puntos más resistente."),
            ("A2P: cómo leer las estrellas",
             "La certificación A2P, expedida por el CNPP francés, indica la resistencia al robo: una estrella para 5 minutos, dos para 10 minutos y tres para 15 minutos. Algunas pólizas de seguro exigen un nivel mínimo: revise la suya y le aconsejaremos el modelo adecuado. Los bombines de seguridad se entregan con una tarjeta de propiedad que protege la copia de las llaves."),
            ("Una elección clara, un precio instalado",
             "El cerrajero le presenta varias gamas, de la estándar a la alta seguridad certificada, con un precio todo incluido (pieza e instalación). Usted elige, él instala y después le entrega la factura, las llaves nuevas y la tarjeta de propiedad."),
        ],
        "faq": [
            ("¿Cuánto cuesta cambiar un bombín?", "Desde 160 € IVA incl. entre semana de día (8:00–18:00), 210 € por la tarde (18:00–22:00, y de 8:00 a 22:00 los fines de semana y festivos) y 230 € por la noche (22:00–8:00). Una cerradura completa empieza en 250 €. El precio final depende de la marca y del nivel de seguridad elegidos: se le entrega un presupuesto detallado antes."),
            ("¿Debo cambiar la cerradura si me roban las llaves?", "Sí, sobre todo si a la vez han desaparecido documentos con su dirección. Según su póliza, el seguro puede cubrir la sustitución."),
            ("Inquilino o propietario: ¿quién paga?", "La pérdida de las llaves suele correr a cargo del inquilino, y la sustitución de una cerradura vieja más bien a cargo del propietario. Lo que cuenta es su contrato de alquiler."),
        ],
    },
    {
        "slug": "smart-lock",
        "cat": "travaux",
        "nom": "Cerradura inteligente: instalación y reparación",
        "court": "Cerradura inteligente",
        "icon": "i-smart",
        "prix": "presupuesto gratuito",
        "prix_num": None,
        "phrase": "una cerradura inteligente",
        "resume": "Instalación y reparación de cerraduras inteligentes: apertura con el móvil, código, tarjeta o huella dactilar.",
        "intro": "Abrir con el móvil, dar un acceso temporal a una niñera o a un inquilino de corta estancia, saber quién ha entrado y cuándo: la cerradura inteligente convence a cada vez más parisinos. La instalamos en su puerta actual e intervenimos cuando se niega a colaborar.",
        "sections": [
            ("Una instalación adaptada a su puerta",
             "Según el modelo, la cerradura inteligente se fija por el lado interior sobre su bombín actual, o sustituye el bombín y la manilla. Primero comprobamos la compatibilidad (grosor de la puerta, tipo de bombín, puerta blindada o no), instalamos, configuramos la aplicación con usted y probamos cada modo de apertura."),
            ("Cuando la cerradura deja de responder",
             "Pilas agotadas, actualización interrumpida, emparejamiento perdido, motor que fuerza contra un pestillo mal alineado: le abrimos si está fuera, volvemos a poner el sistema en marcha y ajustamos la puerta para que la avería no se repita."),
            ("Buenos hábitos",
             "Guarde siempre una llave mecánica de emergencia fuera de casa, elija un modelo combinado con un bombín certificado para una puerta de entrada y cambie las pilas en cuanto aparezca el primer aviso de batería baja."),
        ],
        "faq": [
            ("Mi cerradura inteligente se ha bloqueado y estoy fuera", "Llámenos: abrimos como con una cerradura clásica y después volvemos a poner en servicio su cerradura inteligente."),
            ("¿Se puede instalar en una puerta blindada?", "A menudo sí, según el bombín instalado. Envíenos una foto de su puerta por WhatsApp para una respuesta rápida."),
            ("¿Cuánto cuesta la instalación?", "Tanto la instalación como la reparación se hacen con presupuesto gratuito: el precio depende del modelo y se le comunica antes de cualquier intervención."),
        ],
    },
    {
        "slug": "break-in-repair",
        "cat": "urgence",
        "nom": "Seguridad tras un robo",
        "court": "Tras un robo",
        "icon": "i-tool",
        "prix": "presupuesto gratuito",
        "prix_num": None,
        "phrase": "la protección de su vivienda tras un robo",
        "resume": "Puerta forzada o robo en casa: cierre provisional urgente, cambio de cerradura, refuerzos y documentos para su aseguradora.",
        "intro": "Tras un robo o un intento de robo, solo hay una prioridad: poder cerrar su casa esa misma noche. Aseguramos su puerta con urgencia y después le proponemos una reparación duradera, con todos los justificantes que su aseguradora necesitará.",
        "sections": [
            ("Qué hacer, en orden",
             "1. No toque nada y llame a la policía (17) para que levante acta. 2. Presente una denuncia en la comisaría o por internet: su aseguradora le pedirá el resguardo. 3. Haga asegurar su puerta: intervenimos 24/7 en todo París. 4. Declare el siniestro a su seguro, normalmente en un plazo de 2 días hábiles."),
            ("Protección inmediata",
             "Sustitución del bombín arrancado, colocación de una cerradura provisional, refuerzo del cerradero o del marco, cierre temporal si la puerta ya no cierra. Objetivo: que duerma seguro en su casa esta misma noche."),
            ("Reparación y refuerzo",
             "Según los daños: cerradura multipunto A2P, angulares antipalanca, escudo protector del bombín, refuerzo del marco, blindaje de la puerta existente. Le entregamos un presupuesto detallado y fotos del antes y el después para el perito de su seguro."),
        ],
        "faq": [
            ("¿Reembolsa el seguro al cerrajero tras un robo?", "Con la mayoría de los seguros multirriesgo de hogar, sí, presentando la denuncia y la factura. La nuestra es detallada y conforme."),
            ("¿Pueden venir antes que la policía?", "Es mejor esperar a que la policía levante acta. Si la puerta ya no cierra en absoluto, la aseguramos provisionalmente conservando las huellas útiles para la investigación."),
            ("¿Instalan puertas blindadas?", "Sí: blindamos puertas existentes, colocamos refuerzos e instalamos bloques de puerta blindada completos con presupuesto."),
        ],
    },
    {
        "slug": "door-armoring",
        "cat": "travaux",
        "nom": "Blindaje de puertas",
        "court": "Blindaje de puerta",
        "icon": "i-shield",
        "prix": "desde 2300 € IVA incl.",
        "prix_num": 2300,
        "phrase": "el blindaje de una puerta",
        "resume": "Refuerce su puerta actual: chapa de acero, cerradura multipunto y angulares antipalanca, sin cambiar su aspecto desde el rellano.",
        "intro": "El blindaje convierte su puerta actual en una puerta de seguridad, sin sustituir el marco ni modificar su aspecto exterior. Es la solución más habitual en los edificios parisinos, donde los estatutos de la comunidad suelen exigir que se conserve el aspecto de las puertas de rellano.",
        "sections": [
            ("Qué incluye un blindaje",
             "Una chapa de acero fijada en la cara interior de la hoja, una cerradura multipunto con bombín de seguridad, angulares antipalanca en el marco, bisagras reforzadas y pivotes antiextracción. Según la puerta, añadimos un umbral, una mirilla o un limitador de apertura."),
            ("¿Blindar mejor que sustituir?",
             "El blindaje suele costar menos que un bloque de puerta completo, se instala en un día y conserva su puerta original, a menudo de madera maciza en los edificios antiguos. Sirve para la mayoría de las puertas en buen estado. Si el marco es demasiado frágil, se lo decimos y le proponemos un bloque de puerta."),
            ("Un presupuesto detallado tras la visita",
             "Vamos a medir su puerta, revisar el marco y presentarle varios niveles de protección. El presupuesto es gratuito y especifica el material, el precio instalado y el plazo."),
        ],
        "faq": [
            ("¿Cuánto cuesta blindar una puerta en París?", "Desde 2300 € IVA incl. instalado, según las dimensiones, el número de puntos de cierre y la cerradura elegida. El precio exacto figura en un presupuesto gratuito elaborado tras la visita."),
            ("¿Hace falta el permiso de la comunidad de propietarios?", "La cara exterior de la puerta da a las zonas comunes. Un blindaje que conserva el aspecto desde el rellano rara vez plantea problemas, pero revise los estatutos de su comunidad."),
            ("¿Cuánto dura la instalación?", "Normalmente un día: su puerta queda cerrada y segura esa misma noche."),
        ],
    },
    {
        "slug": "armored-door",
        "cat": "travaux",
        "nom": "Instalación de puertas blindadas",
        "court": "Puerta blindada",
        "icon": "i-door",
        "prix": "desde 3350 € IVA incl.",
        "prix_num": 3350,
        "phrase": "la instalación de una puerta blindada",
        "resume": "Bloque de puerta blindada certificado A2P BP1, BP2 o BP3: puerta, marco y cerradura multipunto diseñados juntos e instalados a medida.",
        "intro": "El bloque de puerta blindada es la protección más completa: la puerta y su marco se diseñan juntos, en acero, con una cerradura multipunto integrada. Es la solución recomendada cuando el marco actual está dañado, tras un robo violento o para las viviendas más expuestas.",
        "sections": [
            ("Los niveles de certificación",
             "La certificación A2P BP, expedida por el CNPP francés, mide la resistencia al robo de un bloque de puerta: BP1 (5 minutos), BP2 (10 minutos), BP3 (15 minutos). Algunos seguros exigen un nivel mínimo: revise su póliza y le aconsejaremos el modelo adecuado."),
            ("Un acabado adaptado a su edificio",
             "Los bloques de puerta blindada existen en muchos acabados (madera, molduras, colores) para respetar la armonía de los rellanos parisinos y las normas del edificio. También mejoran el aislamiento acústico y térmico."),
            ("De la toma de medidas a la instalación",
             "Visita y toma de medidas, presupuesto detallado, pedido a medida y después instalación, normalmente en un día, con retirada de la puerta antigua. El plazo de fabricación figura en el presupuesto; si hace falta, aseguramos su puerta actual mientras tanto."),
        ],
        "faq": [
            ("¿Qué presupuesto hace falta para una puerta blindada?", "Desde 3350 € IVA incl. instalada. El precio depende del nivel de certificación, de las dimensiones y del acabado: se le entrega un presupuesto gratuito tras la visita."),
            ("Blindaje o bloque de puerta: ¿qué elegir?", "Si su puerta y su marco están en buen estado, el blindaje suele bastar. Si el marco es frágil o está dañado, el bloque de puerta es más seguro. Le aconsejamos después de ver su puerta."),
            ("¿La instalación provoca muchos daños?", "No: el marco antiguo se retira con cuidado, el bloque de puerta se ajusta y después se rematan los acabados. Protegemos el rellano y el piso durante la obra."),
        ],
    },
    {
        "slug": "cellar-door",
        "cat": "travaux",
        "nom": "Puerta de trastero blindada",
        "court": "Puerta de trastero",
        "icon": "i-lock",
        "prix": "desde 1550 € IVA incl.",
        "prix_num": 1550,
        "phrase": "una puerta de trastero blindada",
        "resume": "Trastero forzado o mal protegido: bloque de puerta de trastero de acero con cerradura de seguridad, fabricado a la medida de su hueco.",
        "intro": "Los trasteros del sótano de los edificios parisinos (las «caves») son objetivos frecuentes: puertas de madera ligera, candados frágiles, pasillos poco iluminados. Un bloque de puerta de trastero de acero, con una verdadera cerradura de seguridad, protege de forma duradera lo que guarda en él.",
        "sections": [
            ("Una puerta pensada para los sótanos",
             "Marco y hoja de acero, cerradura de seguridad o multipunto, bisagras reforzadas y acabado resistente a la humedad. La puerta se fabrica a la medida de su hueco, a menudo irregular en los edificios antiguos."),
            ("Tras un robo en el trastero",
             "Primero aseguramos el acceso (cerradura provisional, refuerzo) y después le proponemos una puerta definitiva. Recuerde presentar una denuncia y avisar al administrador de la finca: quizá hayan entrado en otros trasteros."),
            ("De acuerdo con la comunidad de propietarios",
             "Como los trasteros están en las zonas comunes, conviene informar al administrador de la finca antes de sustituir la puerta. Podemos facilitarle una descripción técnica."),
        ],
        "faq": [
            ("¿Cuánto cuesta una puerta de trastero blindada?", "Desde 1550 € IVA incl. instalada, según las dimensiones y la cerradura. Presupuesto gratuito tras la visita."),
            ("¿Se puede cambiar solo la cerradura del trastero?", "Sí. Si la puerta está en buen estado, puede bastar con una cerradura nueva o con añadir un cerrojo de seguridad: se lo diremos en el sitio."),
            ("Esta noche han forzado mi trastero", "Llámenos: aseguramos el acceso rápidamente, con presupuesto, y le entregamos una factura para su seguro."),
        ],
    },
    {
        "slug": "mailbox-lock",
        "cat": "travaux",
        "nom": "Cerradura de buzón",
        "court": "Buzón",
        "icon": "i-mail",
        "prix": "desde 110 € IVA incl.",
        "prix_num": 110,
        "phrase": "el cambio de una cerradura de buzón",
        "resume": "Llave perdida, cerradura rota o mudanza: sustituimos la cerradura de su buzón, con llaves nuevas incluidas.",
        "intro": "Llave extraviada, cerradura forzada, nuevo ocupante: cambiar la cerradura de un buzón es una intervención rápida que evita que su correo siga al alcance de otra persona.",
        "sections": [
            ("Una cerradura compatible con su buzón",
             "Los buzones de los edificios utilizan cerraduras estandarizadas. Identificamos el modelo e instalamos una cerradura compatible, entregada con sus llaves."),
            ("Apertura sin daños",
             "Si ya no tiene llave, abrimos el buzón sin dañar la portezuela y después sustituimos la cerradura."),
            ("¿Y el resto de sus accesos?",
             "Si ha perdido todo el llavero, piense también en el bombín de su puerta de entrada y en su trastero: podemos encargarnos de todo en la misma visita."),
        ],
        "faq": [
            ("¿Cuánto cuesta cambiar la cerradura de un buzón?", "110 € IVA incl. para un modelo estándar. Los modelos específicos se hacen con presupuesto gratuito."),
            ("Inquilino o propietario: ¿quién paga?", "La pérdida de la llave suele correr a cargo del inquilino, y el desgaste más bien a cargo del propietario. Lo que cuenta es su contrato de alquiler."),
            ("¿Trabajan con buzones de tarjeta o de código?", "Según el modelo, sí. Envíenos una foto por WhatsApp para comprobarlo."),
        ],
    },
]

# ---------------------------------------------------------------------------
# Urgencias 24/7: (situación, servicio asociado, precio mostrado por franja, consejo mientras espera)
# ---------------------------------------------------------------------------
URGENCES = [
    ("Puerta cerrada de golpe, llaves dentro", "door-opening", ("110 €", "160 €", "220 €"), "No use ni tarjeta bancaria ni destornillador: dañaría el cerradero."),
    ("Puerta cerrada con llave, llaves perdidas", "door-opening", ("desde 180 €", "desde 250 €", "desde 280 €"), "Pregunte al conserje o a un vecino si guardan una copia."),
    ("Cerradura bloqueada, la llave no gira", "jammed-lock", ("180 €", "250 €", "280 €"), "No fuerce: podría romper la llave dentro del bombín."),
    ("Llave rota en la cerradura", "broken-key", "quote", "No empuje el trozo más adentro y no use nunca pegamento."),
    ("Robo, puerta forzada", "break-in-repair", "quote", "Llame a la policía (17) y no toque nada antes de que llegue."),
    ("Llaves robadas: cambiar el bombín", "lock-replacement", ("desde 160 €", "desde 210 €", "desde 230 €"), "Si le robaron también los documentos, cambie el bombín hoy mismo."),
    ("Cerradura inteligente averiada", "smart-lock", "quote", "Busque su llave mecánica de emergencia antes de llamar."),
    ("Trastero forzado", "cellar-door", "quote", "Avise al administrador de la finca: quizá hayan entrado en otros trasteros."),
]

# ---------------------------------------------------------------------------
# Los 20 distritos (arrondissements)
# n: (apodo, población INSEE, códigos postales, barrios administrativos, referencias, metros, tipo de vivienda)
# ---------------------------------------------------------------------------
ARRONDISSEMENTS = {
    1: ("Louvre", 15114, ["75001"], ["Saint-Germain-l'Auxerrois", "Halles", "Palais-Royal", "Place-Vendôme"],
        ["la rue Saint-Honoré", "el jardín de las Tullerías", "el Forum des Halles"], ["Louvre-Rivoli", "Pyramides", "Tuileries"],
        "pisos antiguos encima de las tiendas, palacetes y muchas oficinas"),
    2: ("Bourse", 19847, ["75002"], ["Gaillon", "Vivienne", "Mail", "Bonne-Nouvelle"],
        ["los pasajes cubiertos", "la rue Réaumur", "el barrio del Sentier"], ["Bourse", "Sentier", "Quatre-Septembre"],
        "edificios de viviendas del siglo XIX, talleres convertidos en lofts y pequeñas empresas"),
    3: ("Temple", 32179, ["75003"], ["Arts-et-Métiers", "Enfants-Rouges", "Archives", "Sainte-Avoye"],
        ["el museo Picasso", "el square du Temple", "la rue de Bretagne"], ["Temple", "Arts et Métiers", "Filles du Calvaire"],
        "palacetes del Marais, patios empedrados y edificios con grandes portones"),
    4: ("Hôtel-de-Ville", 27332, ["75004"], ["Saint-Merri", "Saint-Gervais", "Arsenal", "Notre-Dame"],
        ["la place des Vosges", "el Centro Pompidou", "la isla de la Cité"], ["Saint-Paul", "Hôtel de Ville", "Pont Marie"],
        "edificios de los siglos XVII y XVIII, buhardillas y comercios del Marais"),
    5: ("Panthéon", 55252, ["75005"], ["Saint-Victor", "Jardin-des-Plantes", "Val-de-Grâce", "Sorbonne"],
        ["las arenas de Lutecia", "la place de la Contrescarpe", "el Jardin des Plantes"], ["Maubert-Mutualité", "Place Monge", "Cardinal Lemoine"],
        "estudios para estudiantes, edificios antiguos y residencias universitarias"),
    6: ("Luxembourg", 40389, ["75006"], ["Monnaie", "Odéon", "Notre-Dame-des-Champs", "Saint-Germain-des-Prés"],
        ["el boulevard Saint-Germain", "la rue de Rennes", "el teatro del Odéon"], ["Odéon", "Mabillon", "Saint-Placide"],
        "pisos señoriales, galerías de arte y puertas blindadas de alta gama"),
    7: ("Palais-Bourbon", 48015, ["75007"], ["Saint-Thomas-d'Aquin", "Invalides", "École-Militaire", "Gros-Caillou"],
        ["el Campo de Marte", "el museo de Orsay", "la rue Cler"], ["École Militaire", "Solférino", "La Tour-Maubourg"],
        "elegantes edificios haussmannianos, ministerios y grandes pisos familiares"),
    8: ("Élysée", 35317, ["75008"], ["Champs-Élysées", "Faubourg-du-Roule", "Madeleine", "Europe"],
        ["la plaza de la Concordia", "la rue du Faubourg-Saint-Honoré", "el boulevard Haussmann"], ["Miromesnil", "Saint-Augustin", "George V"],
        "sedes sociales, tiendas de lujo y amplios pisos haussmannianos"),
    9: ("Opéra", 57271, ["75009"], ["Saint-Georges", "Chaussée-d'Antin", "Faubourg-Montmartre", "Rochechouart"],
        ["los grandes almacenes", "la rue des Martyrs", "la Nouvelle Athènes"], ["Notre-Dame-de-Lorette", "Cadet", "Le Peletier"],
        "edificios haussmannianos, oficinas y pisos familiares"),
    10: ("Entrepôt", 83873, ["75010"], ["Saint-Vincent-de-Paul", "Porte-Saint-Denis", "Porte-Saint-Martin", "Hôpital-Saint-Louis"],
         ["el canal Saint-Martin", "la estación del Norte", "la rue du Faubourg-Saint-Denis"], ["Jacques Bonsergent", "Château d'Eau", "Colonel Fabien"],
         "edificios antiguos, talleres en patios interiores y muchísimos comercios"),
    11: ("Popincourt", 138170, ["75011"], ["Folie-Méricourt", "Roquette", "Sainte-Marguerite", "Saint-Ambroise"],
         ["la rue de la Roquette", "el boulevard Voltaire", "la rue Oberkampf"], ["Voltaire", "Parmentier", "Charonne"],
         "pequeños edificios de arrabal, pasajes y antiguos talleres convertidos en viviendas"),
    12: ("Reuilly", 138024, ["75012"], ["Bel-Air", "Picpus", "Bercy", "Quinze-Vingts"],
         ["la Coulée verte", "la cour Saint-Émilion", "el bosque de Vincennes"], ["Nation", "Daumesnil", "Dugommier"],
         "residencias de los años 1970 a 2000, edificios haussmannianos y el nuevo barrio de Bercy"),
    13: ("Gobelins", 181271, ["75013"], ["Salpêtrière", "Gare", "Maison-Blanche", "Croulebarbe"],
         ["la avenue de Choisy", "Paris Rive Gauche", "la manufactura de los Gobelinos"], ["Tolbiac", "Olympiades", "Bibliothèque François-Mitterrand"],
         "torres de las Olympiades, residencias modernas con portero automático y casas de la Butte-aux-Cailles"),
    14: ("Observatoire", 136455, ["75014"], ["Montparnasse", "Parc-de-Montsouris", "Petit-Montrouge", "Plaisance"],
         ["la rue Daguerre", "el parque Montsouris", "la Ciudad Universitaria"], ["Mouton-Duvernet", "Pernety", "Plaisance"],
         "edificios de ladrillo, casas, talleres de artistas y grandes conjuntos de viviendas"),
    15: ("Vaugirard", 229713, ["75015"], ["Saint-Lambert", "Necker", "Grenelle", "Javel"],
         ["el Front de Seine", "el parque André-Citroën", "la rue du Commerce"], ["Commerce", "Vaugirard", "Félix Faure"],
         "torres del Front de Seine, edificios de los años 1930 y numerosas residencias familiares"),
    16: ("Passy", 159386, ["75016", "75116"], ["Auteuil", "Muette", "Porte-Dauphine", "Chaillot"],
         ["la rue de Passy", "la avenue Victor-Hugo", "el bosque de Boulogne"], ["La Muette", "Ranelagh", "Michel-Ange-Auteuil"],
         "palacetes, urbanizaciones privadas y pisos con puertas blindadas"),
    17: ("Batignolles-Monceau", 159212, ["75017"], ["Ternes", "Plaine-de-Monceaux", "Batignolles", "Épinettes"],
         ["el parque Clichy-Batignolles", "la avenue de Wagram", "la rue de Lévis"], ["Brochant", "Wagram", "Guy Môquet"],
         "edificios haussmannianos, el ecobarrio Clichy-Batignolles y las casitas de Épinettes"),
    18: ("Butte-Montmartre", 183127, ["75018"], ["Grandes-Carrières", "Clignancourt", "Goutte-d'Or", "La Chapelle"],
         ["la place du Tertre", "la rue Lepic", "el mercado de las Pulgas"], ["Lamarck-Caulaincourt", "Jules Joffrin", "Marcadet-Poissonniers"],
         "edificios antiguos con escaleras estrechas, talleres de artistas y residencias recientes"),
    19: ("Buttes-Chaumont", 178691, ["75019"], ["La Villette", "Pont-de-Flandre", "Amérique", "Combat"],
         ["la dársena de la Villette", "el parque de las Buttes-Chaumont", "la Mouzaïa"], ["Laumière", "Ourcq", "Botzaris"],
         "grandes conjuntos de viviendas, residencias con tarjeta de acceso y casas de la Mouzaïa"),
    20: ("Ménilmontant", 185140, ["75020"], ["Belleville", "Saint-Fargeau", "Père-Lachaise", "Charonne"],
         ["el parque de Belleville", "la rue des Pyrénées", "el pueblo de Charonne"], ["Pyrénées", "Gambetta", "Porte de Bagnolet"],
         "edificios de arrabal, ciudades de artesanos, viviendas sociales y casas adosadas"),
}

# ---------------------------------------------------------------------------
# Tarifas (IVA incl.): servicio, día (entre semana 8:00–18:00), tarde (entre semana 18:00–22:00; fines de semana y festivos 8:00–22:00), noche 22:00–8:00
# None = con presupuesto para esa franja horaria. «Desde …» = precio de partida.
# ---------------------------------------------------------------------------
TARIFS = [
    ("Apertura de puerta cerrada de golpe", "110 €", "160 €", "220 €"),
    ("Apertura de puerta cerrada con llave", "Desde 180 €", "Desde 250 €", "Desde 280 €"),
    ("Cerradura bloqueada, llave que no gira", "180 €", "250 €", "280 €"),
    ("Cambio de bombín", "Desde 160 €", "Desde 210 €", "Desde 230 €"),
    ("Sustitución de cerradura", "Desde 250 €", None, None),
    ("Blindaje de puerta", "Desde 2300 €", None, None),
    ("Bloque de puerta blindada completo", "Desde 3350 €", None, None),
    ("Bloque de puerta de trastero", "Desde 1550 €", None, None),
    ("Cerradura de buzón (modelo estándar)", "110 €", None, None),
]

# Marcas (nombre, archivo del logotipo en assets/img/marques/, categoría)
_CAT = {"Locks": "Cerraduras", "Armored doors": "Puertas blindadas", "Smart locks": "Cerraduras inteligentes"}


def _marques():
    from data import MARQUES as M
    return [(n, s, _CAT.get(c, c)) for n, s, c in M]


MARQUES = _marques()

# Opiniones de Google: mismas reglas que en data.py (solo opiniones reales)
AVIS = []

# ---------------------------------------------------------------------------
# Consejos (blog) – « slug » = dirección inglesa; la dirección española está en build.py
# ---------------------------------------------------------------------------
ARTICLES = [
    {
        "slug": "lost-keys-paris",
        "titre": "Llaves perdidas en París: los 5 reflejos que hay que tener enseguida",
        "court": "Llaves perdidas: los 5 reflejos",
        "cat": "Urgencia", "date": "2026-10-20", "icon": "i-key",
        "desc": "Llavero extraviado en el metro, bolso robado en una terraza: lo que hay que hacer en la primera hora para volver a casa y seguir seguro.",
        "corps": [
            ("p", "Las llaves perdidas son una de las urgencias más habituales en París: un llavero que se escapa de un bolsillo en el metro, un bolso olvidado en una terraza, una chaqueta prestada. Este es el orden en el que conviene actuar."),
            ("h2", "1. Rehaga su recorrido con calma"),
            ("p", "Llame a los últimos lugares por los que ha pasado (café, oficina, gimnasio). El servicio de objetos perdidos de la Prefectura de Policía (Préfecture de police) también centraliza los objetos entregados en los transportes y en la vía pública: se puede consultar por internet."),
            ("h2", "2. Busque una copia"),
            ("ul", ["¿Un familiar o un vecino de confianza?", "¿El conserje del edificio?", "¿Su agencia o su casero?"]),
            ("h2", "3. Evalúe el riesgo"),
            ("p", "Si sus llaves estaban junto a un documento con su dirección (documento de identidad, correo, permiso de circulación), considere que un desconocido podría entrar en su casa: <strong>cambiar el bombín</strong> pasa a ser prioritario. Sin dirección asociada, el riesgo es menor, pero se recomienda cambiarlo si tiene la menor duda."),
            ("h2", "4. Haga abrir sin daños"),
            ("p", "Si la puerta solo está cerrada de golpe, un cerrajero la abre en pocos minutos sin dañar la cerradura. Si está cerrada con llave, la apertura sin daños suele seguir siendo posible, y el bombín puede sustituirse a continuación. En Secure Locksmith Paris, el precio se anuncia por teléfono antes del desplazamiento."),
            ("h2", "5. Avise a su aseguradora"),
            ("p", "Algunas pólizas cubren la pérdida o el robo de las llaves. Guarde la factura detallada y, en caso de robo, el resguardo de la denuncia."),
        ],
    },
    {
        "slug": "armored-door-paris-apartment",
        "titre": "Puerta blindada en un edificio parisino: lo que hay que saber antes de lanzarse",
        "court": "Puerta blindada en París: la guía",
        "cat": "Seguridad", "date": "2026-09-30", "icon": "i-shield",
        "desc": "Blindaje de la puerta existente o bloque de puerta, permiso de la comunidad, certificación A2P: las preguntas que hay que hacerse en un piso.",
        "corps": [
            ("p", "En un piso parisino, la puerta del rellano es el principal punto de entrada de los ladrones. Blindarla es una de las inversiones más eficaces para la seguridad de su vivienda, siempre que se elija bien."),
            ("h2", "¿Blindaje o bloque de puerta?"),
            ("p", "El <strong>blindaje</strong> refuerza su puerta actual con una chapa de acero, una cerradura multipunto y angulares. Conserva el aspecto exterior de la puerta, algo que suele valorarse en una comunidad de propietarios. El <strong>bloque de puerta</strong> sustituye todo el conjunto (puerta y marco): es la solución más resistente, con una certificación A2P BP1, BP2 o BP3."),
            ("h2", "¿Y la comunidad de propietarios?"),
            ("p", "La cara exterior de la puerta del rellano da a las zonas comunes. Si su aspecto cambia (color, molduras, material), los estatutos de la comunidad pueden exigir un permiso o un modelo concreto. Un blindaje que conserva el revestimiento exterior rara vez plantea problemas: aun así, revise los estatutos."),
            ("h2", "Los puntos que hay que comprobar"),
            ("ul", ["La cerradura: multipunto, con un bombín certificado A2P y una tarjeta de propiedad.", "Las bisagras: antiextracción.", "El marco: reforzado; si no, hasta la puerta más sólida cede por el lateral.", "El aislamiento acústico y térmico, muy apreciable en los edificios antiguos."]),
            ("p", "Nuestros cerrajeros se desplazan para evaluar su puerta gratuitamente y entregarle un presupuesto detallado."),
        ],
    },
    {
        "slug": "spot-an-honest-locksmith",
        "titre": "Cómo reconocer a un cerrajero honrado (y evitar las estafas)",
        "court": "Reconocer a un cerrajero honrado",
        "cat": "Consejos", "date": "2026-09-08", "icon": "i-award",
        "desc": "Folletos engañosos, precios poco claros, cerraduras taladradas sin motivo: las señales de alerta y los derechos que le protegen.",
        "corps": [
            ("p", "La cerrajería de urgencia es uno de los sectores que más reclamaciones de consumidores generan en Francia. Sin embargo, bastan unos pocos reflejos sencillos para evitar sorpresas desagradables."),
            ("h2", "Las señales que deben alertarle"),
            ("ol", ["Una pegatina o un folleto de «número de urgencia» que imita al ayuntamiento o al administrador de la finca.", "Un precio vago por teléfono, o un «desde 19 €» sin más precisión.", "Ningún presupuesto escrito antes de empezar.", "Una propuesta de taladrar o cambiar la cerradura cuando la puerta solo estaba cerrada de golpe.", "Un pago solo en efectivo, sin factura.", "Una empresa sin nombre, sin número SIRET ni opiniones verificables."]),
            ("h2", "Lo que exige la ley francesa"),
            ("p", "Para una intervención a domicilio, el profesional debe informarle de sus precios y entregarle un <strong>presupuesto detallado</strong> antes de la intervención cuando el precio pueda determinarse de antemano. Usted puede rechazarlo. Al final se le debe entregar una <strong>factura detallada</strong>."),
            ("h2", "En caso de litigio"),
            ("p", "Conserve todos los documentos, impugne la factura por escrito, denuncie la práctica en la web oficial SignalConso y acuda al mediador de consumo indicado por la empresa."),
            ("h2", "Nuestra forma de trabajar"),
            ("p", "En Secure Locksmith Paris, el precio se anuncia por teléfono, se confirma con un presupuesto firmado y la factura es detallada para su seguro. Nuestras opiniones son públicas en nuestro perfil de Google."),
        ],
    },
    {
        "slug": "after-a-burglary",
        "titre": "Tras un robo: proteger su piso en 24 horas",
        "court": "Tras un robo: ¿qué hacer?",
        "cat": "Urgencia", "date": "2026-08-18", "icon": "i-tool",
        "desc": "Atestado, denuncia, seguro, cierre provisional y después refuerzo: el plan de acción hora a hora.",
        "corps": [
            ("p", "Descubrir la puerta forzada es un golpe duro. Para no olvidar nada y recuperar rápidamente una vivienda que cierre, siga este plan."),
            ("h2", "En la primera hora"),
            ("ul", ["No entre si cree que alguien puede seguir dentro: llame a la policía (17).", "No toque nada antes de que la policía levante acta.", "Fotografíe los daños (puerta, cerradura, habitaciones)."]),
            ("h2", "En el mismo día"),
            ("ul", ["Presente una denuncia (en la comisaría o mediante la predenuncia por internet).", "Bloquee sus tarjetas bancarias robadas.", "Haga asegurar su puerta: un cerrajero instala un bombín nuevo o un cierre provisional."]),
            ("h2", "En un plazo de 2 días hábiles"),
            ("p", "Declare el siniestro a su aseguradora con el resguardo de la denuncia, la lista de objetos robados y la factura del cerrajero."),
            ("h2", "Después: reforzar"),
            ("p", "Cerradura multipunto A2P, escudo protector del bombín, angulares antipalanca, blindaje de puerta: le proponemos los refuerzos adecuados para su puerta y su presupuesto, con un presupuesto detallado para el perito del seguro."),
        ],
    },
]

# ---------------------------------------------------------------------------
# Textos de confianza
# ---------------------------------------------------------------------------
COMPARATIF = [
    ("Un precio «desde 19 €» por teléfono y después una factura de varios cientos de euros.",
     "Un precio real anunciado por teléfono según su descripción, y nuestras tarifas publicadas en esta web."),
    ("El trabajo empieza antes de que haya firmado nada.",
     "Un presupuesto escrito y firmado antes de cualquier intervención. Sin su firma, no empieza nada."),
    ("Se taladra o se cambia la cerradura cuando la puerta solo estaba cerrada de golpe.",
     "Primero, apertura sin daños. Solo se propone taladrar como último recurso, explicado y presupuestado."),
    ("Se exige el pago en efectivo, sin factura o con una factura ilegible.",
     "Tarjeta bancaria, efectivo o transferencia, a su elección, con una factura detallada cada vez."),
    ("Un número encontrado en una pegatina que imita al ayuntamiento o al administrador de la finca.",
     "Una empresa identificada: nombre, dirección, perfil de Google y opiniones públicas verificables."),
    ("Una plataforma de llamadas que revende su solicitud al cerrajero que más paga.",
     "Un cerrajero que contesta él mismo y se desplaza en persona, de día y de noche."),
]

CHARTE = [
    ("i-euro", "1. Se le anuncia el precio antes del desplazamiento",
     "Por teléfono le hacemos unas preguntas sencillas: ¿la puerta está cerrada de golpe o con llave? ¿Es blindada o no? ¿Qué tipo de cerradura tiene? Según sus respuestas, le anunciamos un precio con IVA, en función de la hora de la intervención. Ese precio corresponde a nuestra lista de tarifas, publicada en esta web. Si lo prefiere, envíe una foto de su puerta por WhatsApp: la estimación será aún más precisa."),
    ("i-file", "2. Un presupuesto escrito y firmado antes de cualquier trabajo",
     "En el sitio, el cerrajero comprueba la situación y le entrega un presupuesto detallado: tipo de intervención, material si lo hay, precio con IVA. Usted lo lee, hace sus preguntas y firma. No antes. Es una obligación legal en Francia (orden del 24 de enero de 2017) que aplicamos en cada intervención, sin excepción, también de noche."),
    ("i-door", "3. Ningún daño innecesario, ninguna sustitución innecesaria",
     "Una puerta cerrada de golpe se abre casi siempre sin daños. Primero usamos técnicas de apertura fina (láminas, ganzúas, apertura del bombín sin romperlo). Si hace falta taladrar o sustituir una pieza, el cerrajero le explica por qué, le enseña la pieza causante y le indica el precio antes de hacerlo. Usted es libre de negarse."),
    ("i-shield", "4. Material de calidad, adaptado a su puerta",
     "Cuando hay que sustituir una pieza, le proponemos varias gamas, del bombín estándar al bombín de alta seguridad certificado A2P, con su precio instalado. Trabajamos con marcas reconocidas (Fichet, Picard, Vachette, Bricard, Mul-T-Lock…) y le entregamos las llaves nuevas y, en su caso, la tarjeta de propiedad."),
    ("i-card", "5. Un pago claro y una factura detallada",
     "Paga lo que figura en el presupuesto firmado, ni más ni menos. Tarjeta bancaria, efectivo o transferencia: usted elige. La factura detalla la intervención y el material; es válida para su seguro de hogar."),
    ("i-building", "6. Una empresa identificable",
     "Nuestro nombre, nuestra dirección, nuestro teléfono y nuestro perfil de Google figuran en cada página de esta web. Nuestras opiniones las publican nuestros clientes en Google: son públicas y no podemos modificarlas ni borrarlas. Puede consultarlas incluso antes de llamarnos."),
    ("i-phone", "7. Un interlocutor directo, 24/7",
     "Cuando llama, le contesta un cerrajero, no una centralita que transmite su solicitud. El mismo interlocutor le acompaña de la llamada a la factura, y sigue localizable después de la intervención si tiene alguna pregunta."),
    ("i-home", "8. El respeto de su vivienda",
     "Protegemos el suelo si es necesario, dejamos el lugar limpio y le explicamos lo que se ha hecho. Tras un robo, le aconsejamos sobre los trámites (denuncia, seguro) y sobre los refuerzos útiles, sin empujarle a hacer obras que no necesita."),
]

INCLUS = [
    "El desplazamiento dentro de París, gratuito si se realiza el trabajo",
    "La mano de obra del cerrajero",
    "El diagnóstico y las explicaciones en el sitio",
    "El presupuesto escrito, gratuito y sin compromiso",
    "La factura detallada para su seguro",
    "El IVA: nuestros precios siempre se muestran con IVA incluido",
]

REALISATIONS = {}
INTERVENTIONS = {}

# Vídeos de obra: servicio -> (archivo, título, pie de foto, descripción para Google, fecha)
VIDEOS = {
    "smart-lock": ("smart-lock", "Una cerradura inteligente que hemos instalado", "Abierta desde el móvil del propietario",
                   "Una cerradura inteligente instalada por Secure Locksmith Paris, abierta desde el móvil del propietario.", "2026-11-10"),
    "door-armoring": ("lock-3-points", "Una cerradura de 3 puntos que hemos instalado", "Una vuelta de llave y se cierran los tres pestillos",
                      "Una cerradura de 3 puntos de sobreponer instalada en la puerta de un piso en París: la llave gira y los tres pestillos se cierran.", "2026-11-10"),
    "lock-replacement": ("new-keys", "Una cerradura multipunto que hemos revisado", "Probada y entregada con llaves nuevas",
                         "Una cerradura multipunto revisada en París, probada con la llave y entregada al cliente con llaves nuevas.", "2026-11-10"),
}

# ---------------------------------------------------------------------------
# Textos de las páginas (equivalentes españoles de las constantes de build.py)
# ---------------------------------------------------------------------------
WA_MSG = "Hola, necesito un cerrajero en París."

NAV = [("Urgencias", "/emergency/"), ("Servicios", "/services/"), ("Precios", "/prices/"), ("Compromisos", "/our-commitments/"),
       ("Distritos", "/locksmith-paris/"), ("Contacto", "/contact/")]

SLOTS = [("jour", "i-sun", "Día", "8:00 – 18:00"), ("soir", "i-sunset", "Tarde", "18:00 – 22:00"), ("nuit", "i-moon", "Noche", "22:00 – 8:00")]
SLOTS_WE = {"jour": "solo entre semana", "soir": "8:00 – 22:00", "nuit": "22:00 – 8:00"}
WEEKEND_NOTE = "<b>Fines de semana y festivos:</b> los sábados, domingos y festivos, la tarifa mínima aplicada es la de Tarde (18:00–22:00); si la intervención tiene lugar en la franja de Noche (22:00–8:00), se aplica la tarifa de Noche."

PARIS_BG = {
    "tour-eiffel": "La torre Eiffel al atardecer", "toits-de-paris": "Los tejados de París",
    "notre-dame": "Notre-Dame de París y el Sena", "pantheon": "El Panteón", "conciergerie": "La Conciergerie a orillas del Sena",
    "place-des-victoires": "La place des Victoires", "sacre-coeur": "El Sacré-Cœur en Montmartre",
    "vue-sacre-coeur": "Vista de Montmartre", "avenue-etoile": "Avenida parisina vista desde el Arco del Triunfo", "mairie": "Un ayuntamiento de distrito en París",
}

HOME_FAQ = [
    ("¿Cuánto cuesta abrir una puerta en París?", "Una puerta cerrada de golpe se abre por 110 € IVA incl. entre semana de día (8:00–18:00), 160 € por la tarde y los fines de semana, y 220 € por la noche. El precio se anuncia por teléfono y después se confirma con un presupuesto escrito antes de cualquier trabajo."),
    ("¿Trabajan en todo París?", "Sí, en los 20 distritos, del 1 al 20, 24/7, festivos incluidos. Nuestros cerrajeros están repartidos por la ciudad para llegar rápido a su casa."),
    ("¿Cuánto tardan en llegar?", "Unos 30 minutos de media dentro de París. El tiempo exacto depende del tráfico y se le anuncia por teléfono antes de que salga el cerrajero."),
    ("¿El presupuesto es gratuito?", "Sí, gratuito y sin compromiso. No se hace nada sin su firma, y usted es libre de negarse."),
    ("¿En qué idiomas atienden?", "En francés y en inglés. También puede escribirnos por WhatsApp y enviarnos una foto de su puerta: el presupuesto y la factura se le explican con claridad."),
    ("¿Me puede reembolsar el seguro?", "A menudo, sí: robo, hurto o pérdida de llaves, según su póliza. Nuestra factura detallada es aceptada por las aseguradoras de hogar francesas."),
    ("¿Cómo puedo pagar?", "Con tarjeta bancaria, en efectivo o por transferencia. Siempre recibe una factura."),
]

MOIS = ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"]

ARR_INTROS = [
    "¿Se ha quedado fuera {a}? {nom} envía a un cerrajero cualificado a su puerta, de día o de noche, normalmente en unos treinta minutos. El precio se le anuncia por teléfono antes de que salga.",
    "Desde los alrededores {de_r0} hasta las calles más tranquilas del distrito {num}, nuestros cerrajeros trabajan 24/7 en puertas cerradas de golpe, cerraduras bloqueadas y llaves rotas, con un presupuesto firmado antes de cualquier trabajo.",
    "Con sus {pop} habitantes, el distrito {num} ({surnom}) vive cada día su ración de puertas cerradas de golpe y llaves perdidas. Nuestros cerrajeros conocen sus edificios y las cerraduras que los equipan.",
    "¿Una urgencia de cerrajería {a}? Desde los barrios de {q} hasta los alrededores {de_r1}, llegamos rápido, a un precio acordado de antemano y con una factura que su aseguradora aceptará.",
]

URG_FAQ = [
    ("¿De verdad vienen de noche y en domingo?", "Sí, 24/7, festivos incluidos. La tarifa de noche (22:00–8:00) se le anuncia por teléfono antes de que salga el cerrajero."),
    ("¿Cuánto tardan en llegar?", "Unos 30 minutos de media dentro de París. El tiempo exacto depende del tráfico y se le anuncia por teléfono."),
    ("¿Cuánto cuesta una apertura de puerta urgente?", "110 € IVA incl. entre semana de día, 160 € por la tarde y los fines de semana, 220 € por la noche para una puerta cerrada de golpe. Una puerta cerrada con llave empieza en 180 € de día."),
    ("¿Qué debo tener preparado cuando llegue el cerrajero?", "Si es posible, un documento de identidad o un justificante de domicilio: el cerrajero debe asegurarse de que usted es el ocupante. Si sus documentos están dentro, un vecino, el conserje o su anfitrión pueden responder por usted."),
    ("¿Puedo rechazar el presupuesto en el sitio?", "Sí. El presupuesto es gratuito y sin compromiso: si lo rechaza, no se hace nada."),
]

# Guía de urgencia: situación -> precio por franja horaria (None = con presupuesto), servicio asociado, consejo
GUIDE = [
    ("slammed", "Puerta cerrada de golpe, llaves dentro", "door-opening", (110, 160, 220), False,
     "No intente abrir el resbalón con una tarjeta o un destornillador: dañaría el cerradero. La mayoría de las puertas cerradas de golpe se abren en pocos minutos, sin daños."),
    ("locked", "Puerta cerrada con llave, llaves perdidas", "door-opening", (180, 250, 280), True,
     "Pregunte al conserje o a un vecino si guardan una copia. La apertura sin daños sigue siendo posible en muchos casos."),
    ("jammed", "Cerradura bloqueada, la llave no gira", "jammed-lock", (180, 250, 280), False,
     "Deje de forzar la llave: podría romperla dentro del bombín. No eche aceite en la cerradura."),
    ("broken", "Llave rota en la cerradura", "broken-key", None, False,
     "No empuje el trozo más adentro y no use nunca pegamento. Si sobresale, tire de él en línea recta con unos alicates finos."),
    ("burglary", "Robo, puerta forzada", "break-in-repair", None, False,
     "No entre si alguien puede seguir dentro: llame a la policía (17). No toque nada antes de que llegue."),
    ("stolen", "Llaves robadas, cambiar el bombín", "lock-replacement", (160, 210, 230), True,
     "Si le robaron el documento de identidad o algo con su dirección junto con las llaves, cambie el bombín hoy mismo."),
    ("smart", "Cerradura inteligente averiada", "smart-lock", None, False,
     "Busque su llave mecánica de emergencia y compruebe si la aplicación indica batería baja."),
    ("cellar", "Trastero forzado", "cellar-door", None, False,
     "Avise al administrador de la finca (syndic): quizá hayan entrado en otros trasteros."),
]

SVC_LOCAL = {
    "door-opening": {
        "intros": [
            "¿Se ha quedado fuera {a} con las llaves dentro? Un cerrajero de {nom} sale enseguida para abrir su puerta con cuidado, a menudo en pocos minutos y sin tocar la cerradura. Conoce el precio antes de que salga.",
            "Que no cunda el pánico si la puerta se ha cerrado de golpe a su espalda {a}: una puerta cerrada de golpe se abre casi siempre sin daños. Vamos de día y de noche, a un precio acordado de antemano.",
            "¿Atrapado en el rellano {a}? Llámenos: conoce el precio antes de que llegue el cerrajero, y su puerta se abre sin daños en la inmensa mayoría de los casos.",
        ],
        "conseil": "Evite la tarjeta bancaria y el destornillador: dañan el cerradero y la junta, y la intervención se alarga.",
    },
    "jammed-lock": {
        "intros": [
            "¿La llave no gira {a}? Nuestros cerrajeros encuentran la causa y reparan en el sitio: limpieza, ajuste del cerradero o sustitución del bombín si hace falta. Precio anunciado antes del desplazamiento.",
            "Cerradura dura, puerta que ya no se abre o ya no cierra {a}: un cerrajero llega con las piezas habituales para resolver el problema en una sola visita en la mayoría de los casos.",
            "Pestillo que roza, bombín sucio, puerta que se ha movido: las cerraduras bloqueadas son frecuentes {a}. Primero reparamos, y solo sustituimos cuando de verdad hace falta.",
        ],
        "conseil": "No fuerce la llave y olvídese del aceite de cocina: un lubricante seco (grafito o PTFE) funciona mucho mejor.",
    },
    "broken-key": {
        "intros": [
            "¿Llave rota en la cerradura {a}? Nuestros cerrajeros retiran el trozo con extractores específicos, normalmente sin desmontar la cerradura, 24/7, con presupuesto gratuito.",
            "Un trozo de llave atascado en el bombín {a}: un cerrajero va a extraerlo, revisa el bombín y solo lo sustituye en el momento si es útil.",
            "Que una llave vieja se rompa en la cerradura es habitual {a}. Retiramos el trozo limpiamente y después le aconsejamos: hacer una llave nueva o sustituir un bombín gastado.",
        ],
        "conseil": "Ni pegamento ni clip: podría hundir más el trozo e inutilizar el bombín.",
    },
    "lock-replacement": {
        "intros": [
            "Llaves perdidas, mudanza o cerradura gastada {a}: sustituimos bombines y cerraduras, del modelo estándar a la cerradura multipunto certificada A2P. Presupuesto gratuito, firmado antes de cualquier trabajo.",
            "Cambio de cerradura {a}: el cerrajero llega con una selección de bombines en stock, le presenta las opciones y sus precios, y después instala el que usted elija el mismo día.",
            "¿Acaba de mudarse {a} o ha perdido sus llaves? Cambiar el bombín es la forma más sencilla de volver a controlar quién puede entrar. Material certificado, factura detallada.",
        ],
        "conseil": "Fíjese en el número de estrellas A2P (de 1 a 3): indica la resistencia al robo y a veces lo exigen las aseguradoras.",
    },
    "smart-lock": {
        "intros": [
            "¿Quiere abrir su puerta con el móvil {a}? Instalamos y configuramos cerraduras inteligentes compatibles con su puerta, y reparamos las que dejan de responder.",
            "Cerradura inteligente {a}: instalación, configuración y reparación cuando las pilas se agotan o el motor se bloquea. Comprobamos la compatibilidad de su bombín antes de instalar nada.",
            "Avería de cerradura inteligente o proyecto de instalación {a}: abrimos 24/7 las puertas con una cerradura inteligente bloqueada, e instalamos con cita previa.",
        ],
        "conseil": "Guarde una llave mecánica de emergencia y vigile las pilas: son la primera causa de cerraduras inteligentes bloqueadas.",
    },
    "break-in-repair": {
        "intros": [
            "¿Robo o intento de robo {a}? Aseguramos su puerta con urgencia, 24/7, y después la reparamos o la reforzamos. Factura detallada para su aseguradora.",
            "Puerta forzada {a}: un cerrajero acude de día o de noche para instalar una cerradura provisional o definitiva y sustituir el bombín dañado.",
            "Tras un robo {a}, la prioridad es poder cerrar esta noche. Llegamos rápido, con presupuesto gratuito, y le aconsejamos sobre los refuerzos adecuados.",
        ],
        "conseil": "Fotografíe los daños y presente la denuncia antes de la reparación definitiva: su aseguradora le pedirá el resguardo.",
    },
    "door-armoring": {
        "intros": [
            "¿Quiere proteger su puerta de entrada {a} sin sustituirla? El blindaje refuerza su puerta actual con una chapa de acero, una cerradura multipunto y angulares antipalanca, conservando su aspecto desde el rellano.",
            "Blindaje de puerta {a}: vamos a medir su puerta, revisar el marco y presentarle varios niveles de protección, con un presupuesto gratuito y detallado. La instalación suele durar un día.",
            "Una vieja puerta de rellano, una cerradura básica, un marco cansado: es el caso de muchos pisos {a}. El blindaje suele ser la forma más eficaz de disuadir a los ladrones sin grandes obras.",
        ],
        "conseil": "Revise los estatutos de su comunidad: un blindaje que conserva el aspecto exterior de la puerta suele aceptarse sin trámites.",
    },
    "armored-door": {
        "intros": [
            "Instalación de puertas blindadas {a}: colocamos bloques de puerta certificados A2P BP1, BP2 o BP3, fabricados a medida y a juego con su rellano. Presupuesto gratuito tras la visita.",
            "Marco dañado, puerta demasiado ligera, vivienda expuesta {a}: un bloque de puerta blindada completo sustituye la puerta y el marco por un cierre diseñado para resistir los robos.",
            "¿Busca la protección más completa para su piso {a}? Un bloque de puerta blindada combina acero, cerradura multipunto y aislamiento, con un acabado adaptado a su edificio.",
        ],
        "conseil": "Pregunte a su aseguradora qué nivel de certificación exige (BP1, BP2 o BP3) antes de elegir su modelo.",
    },
    "cellar-door": {
        "intros": [
            "¿Trastero forzado o mal protegido {a}? Instalamos bloques de puerta de trastero de acero con cerradura de seguridad, fabricados a la medida de su hueco.",
            "Los trasteros de los edificios son un objetivo frecuente {a}. Una puerta de trastero de acero con una verdadera cerradura de seguridad acaba con los candados frágiles y las puertas de madera que ceden al primer empujón.",
            "Puerta de trastero {a}: protección urgente tras un robo y después puerta definitiva con presupuesto gratuito.",
        ],
        "conseil": "Avise al administrador de la finca antes de sustituir la puerta de su trastero y denuncie cualquier robo: quizá hayan entrado en otros trasteros.",
    },
    "mailbox-lock": {
        "intros": [
            "¿Ha perdido la llave del buzón {a}? Sustituimos la cerradura por un modelo compatible con llaves nuevas, por 110 € IVA incl. en un modelo estándar.",
            "¿Acaba de mudarse {a} y no sabe quién tiene la llave del buzón? Cambiar la cerradura lleva poco tiempo y protege su correo.",
            "Cerradura de buzón forzada o bloqueada {a}: la abrimos sin dañar la portezuela e instalamos una cerradura nueva.",
        ],
        "conseil": "Si ha desaparecido todo su llavero, haga revisar el bombín de su puerta de entrada y la cerradura de su trastero en la misma visita.",
    },
}
