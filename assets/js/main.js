(function(){
  // Menu mobile
  var burger = document.querySelector(".burger"), drawer = document.getElementById("drawer");
  if (burger && drawer) {
    burger.addEventListener("click", function(){
      var open = drawer.classList.toggle("open");
      burger.setAttribute("aria-expanded", open ? "true" : "false");
    });
    drawer.querySelectorAll("a").forEach(function(a){
      a.addEventListener("click", function(){ drawer.classList.remove("open"); burger.setAttribute("aria-expanded", "false"); });
    });
  }

  // Grille tarifaire : tranche de l'heure actuelle à Paris.
  // Semaine : jour 8h-18h, soir 18h-22h, nuit 22h-8h. Samedi, dimanche et jours fériés : soir 8h-22h, nuit 22h-8h.
  var h, dow, y, mo, d;
  try {
    var parts = {};
    new Intl.DateTimeFormat("en-GB", {timeZone: "Europe/Paris", weekday: "short", year: "numeric", month: "numeric", day: "numeric", hour: "numeric", hour12: false})
      .formatToParts(new Date()).forEach(function(p){ parts[p.type] = p.value; });
    h = parseInt(parts.hour, 10); y = +parts.year; mo = +parts.month; d = +parts.day;
    dow = ["Sun","Mon","Tue","Wed","Thu","Fri","Sat"].indexOf(parts.weekday);
  } catch(e) {}
  if (isNaN(h) || dow < 0 || !y) { var n = new Date(); h = n.getHours(); dow = n.getDay(); y = n.getFullYear(); mo = n.getMonth() + 1; d = n.getDate(); }
  h = h % 24;
  function holiday(y, mo, d){
    var fixed = ["1-1","5-1","5-8","7-14","8-15","11-1","11-11","12-25"];
    if (fixed.indexOf(mo + "-" + d) > -1) return true;
    // Pâques (calcul grégorien), puis lundi de Pâques, Ascension, lundi de Pentecôte
    var a = y % 19, b = Math.floor(y / 100), c = y % 100, k4 = b % 4, f = Math.floor((b + 8) / 25), g = Math.floor((b - f + 1) / 3);
    var hh = (19 * a + b - Math.floor(b / 4) - g + 15) % 30, l = (32 + 2 * k4 + 2 * Math.floor(c / 4) - hh - c % 4) % 7, m = Math.floor((a + 11 * hh + 22 * l) / 451);
    var em = Math.floor((hh + l - 7 * m + 114) / 31), ed = (hh + l - 7 * m + 114) % 31 + 1;
    var easter = Date.UTC(y, em - 1, ed), today = Date.UTC(y, mo - 1, d), diff = Math.round((today - easter) / 864e5);
    return diff === 1 || diff === 39 || diff === 50;
  }
  var isHoliday = holiday(y, mo, d), offDay = dow === 0 || dow === 6 || isHoliday;
  var current = offDay ? (h >= 8 && h < 22 ? "soir" : "nuit") : (h >= 8 && h < 18 ? "jour" : (h >= 18 && h < 22 ? "soir" : "nuit"));
  var dayName = isHoliday ? "a public holiday" : ["Sunday","Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"][dow];
  function fmtH(x){ return (x % 12 || 12) + (x < 12 ? "am" : "pm"); }
  var labels = offDay
    ? {jour:"day (weekdays only)", soir:"evening (8am – 10pm on weekends and public holidays)", nuit:"night (10pm – 8am)"}
    : {jour:"day (8am – 6pm)", soir:"evening (6pm – 10pm)", nuit:"night (10pm – 8am)"};
  var nowTxt = "It is " + fmtH(h) + " on " + dayName + " in Paris";
  if (offDay) document.querySelectorAll("small[data-h-we]").forEach(function(sm){
    sm.textContent = sm.getAttribute("data-h-we");
    var btn = sm.closest("button"); if (btn && btn.getAttribute("data-slot") === "jour") btn.classList.add("is-off");
  });
  // Cartes d'urgence de l'accueil : prix de la tranche actuelle
  document.querySelectorAll(".urg-p .up[data-slot]").forEach(function(v){ v.hidden = v.getAttribute("data-slot") !== current; });
  document.querySelectorAll("[data-tarifs]").forEach(function(card){
    var tabs = card.querySelectorAll(".slot-tabs button"), now = card.querySelector(".slot-now");
    function show(slot){
      tabs.forEach(function(t){
        var on = t.getAttribute("data-slot") === slot;
        t.setAttribute("aria-selected", on ? "true" : "false");
        t.classList.toggle("is-now", t.getAttribute("data-slot") === current);
      });
      card.querySelectorAll(".pv[data-slot]").forEach(function(v){ v.hidden = v.getAttribute("data-slot") !== slot; });
      if (now) {
        now.innerHTML = slot === current
          ? "<i></i>" + nowTxt + ": these are our " + labels[slot] + " prices."
          : "Prices for " + labels[slot] + ". " + nowTxt + ".";
        now.hidden = false;
      }
    }
    tabs.forEach(function(t){ t.addEventListener("click", function(){ show(t.getAttribute("data-slot")); }); });
    show(current);
  });

  // Mesure : Google Ads + événements GTM
  function conv(kind){
    var to = (window.SLP_CONV || {})[kind];
    if (to && window.gtag) gtag("event", "conversion", {send_to: to, value: 1.0, currency: "EUR"});
  }
  function push(name, data){
    window.dataLayer = window.dataLayer || [];
    var e = {event: name, page_path: location.pathname};
    for (var k in data) e[k] = data[k];
    window.dataLayer.push(e);
  }
  document.querySelectorAll('a[href^="tel:"], a[href^="https://wa.me"]').forEach(function(a){
    a.addEventListener("click", function(){
      var wa = a.href.indexOf("wa.me") > -1, where = a.getAttribute("data-track") || "contenu";
      if (window.gtag) gtag("event", wa ? "whatsapp_click" : "phone_click", {location: where});
      conv(wa ? "wa" : "call");
      push(wa ? "clic_whatsapp" : "clic_appel", {emplacement: where});
    });
  });

  // Formulaires Netlify : envoi sans changer de page
  document.querySelectorAll("form.lead-form").forEach(function(form){
    form.addEventListener("submit", function(e){
      e.preventDefault();
      if (!form.reportValidity()) return;
      var btn = form.querySelector("button[type=submit]"), label = btn.innerHTML;
      btn.disabled = true; btn.textContent = "Sending…";
      fetch("/", {method: "POST", headers: {"Content-Type": "application/x-www-form-urlencoded"},
                  body: new URLSearchParams(new FormData(form)).toString()})
        .then(function(r){
          if (!r.ok) throw new Error(r.status);
          if (window.gtag) gtag("event", "generate_lead", {service: form.service.value});
          conv("form");
          push("envoi_formulaire", {service: form.service.value, emplacement: form.page.value});
          form.reset();
          form.querySelector(".form-ok").hidden = false;
          btn.innerHTML = label; btn.disabled = false;
        })
        .catch(function(){ form.submit(); });
    });
  });

  // Guide d'urgence (page /emergency/) : situation + tranche horaire -> prix et conseil
  document.querySelectorAll("[data-guide]").forEach(function(g){
    var data = {};
    try { data = JSON.parse(document.getElementById("guide-data").textContent); } catch(e) {}
    var sit = null, slot = current, idx = {jour:0, soir:1, nuit:2};
    var slotNames = offDay
      ? {jour:"Daytime rate (weekdays only)", soir:"Weekend & holiday rate (8am–10pm)", nuit:"Night rate (10pm–8am)"}
      : {jour:"Daytime rate (8am–6pm)", soir:"Evening rate (6pm–10pm)", nuit:"Night rate (10pm–8am)"};
    var auto = g.querySelector(".gd-auto");
    if (auto) { auto.textContent = "· it is " + fmtH(h) + " on " + dayName + " in Paris, we selected it for you"; auto.hidden = false; }
    function q(n){ return g.querySelector('[data-g="' + n + '"]'); }
    function render(){
      g.querySelectorAll(".gd-opt").forEach(function(b){ b.setAttribute("aria-pressed", b.getAttribute("data-sit") === sit ? "true" : "false"); });
      g.querySelectorAll(".gd-slot").forEach(function(b){ b.setAttribute("aria-pressed", b.getAttribute("data-slot") === slot ? "true" : "false"); });
      if (!sit || !data[sit]) return;
      var d = data[sit];
      g.querySelector(".gd-empty").hidden = true;
      g.querySelector(".gd-out").hidden = false;
      q("slotlabel").textContent = d.label;
      if (d.prices) {
        q("price").textContent = (d.from ? "from " : "") + "€" + d.prices[idx[slot]];
        q("note").textContent = "incl. VAT · " + slotNames[slot] + " · confirmed on the phone";
      } else {
        q("price").textContent = "Free quote";
        q("note").textContent = "The price depends on your lock: we give it on the phone before we travel.";
      }
      q("tip").textContent = d.tip;
      q("quote").setAttribute("data-quote", d.service);
      q("more").setAttribute("href", d.url);
      push("guide_urgence", {situation: sit, creneau: slot});
    }
    g.addEventListener("click", function(e){
      var o = e.target.closest(".gd-opt"), sl = e.target.closest(".gd-slot");
      if (o) {
        sit = o.getAttribute("data-sit"); render();
        // sur téléphone, le résultat est sous la liste : on l'amène à l'écran
        if (window.innerWidth < 760) g.querySelector(".gd-result").scrollIntoView({behavior: "smooth", block: "start"});
      }
      if (sl) { slot = sl.getAttribute("data-slot"); render(); }
    });
    render();
  });

  // Fenêtre de devis : chaque bouton [data-quote] l'ouvre avec le service déjà choisi
  var qm = document.getElementById("quote-modal");
  if (qm && qm.showModal) {
    var qmForm = qm.querySelector("form.lead-form"), qmSvc = qm.querySelector("[data-qm-service]");
    document.addEventListener("click", function(e){
      var b = e.target.closest("[data-quote]");
      if (!b) return;
      e.preventDefault();
      var svc = b.getAttribute("data-quote");
      var sel = qmForm.querySelector("select[name=service]");
      var found = false;
      for (var i = 0; i < sel.options.length; i++) { if (sel.options[i].text === svc) { sel.selectedIndex = i; found = true; } }
      if (!found) sel.selectedIndex = sel.options.length - 1;
      qmSvc.innerHTML = "<small>Free quote</small>" + svc.replace(/[<>&]/g, "");
      qmForm.querySelector("input[name=page]").value = location.pathname + " (popup)";
      qmForm.querySelector(".form-ok").hidden = true;
      qm.showModal();
      document.body.classList.add("qm-lock");
      var first = qmForm.querySelector("input[name=name]"); if (first) setTimeout(function(){ first.focus(); }, 60);
      if (window.gtag) gtag("event", "quote_open", {service: svc});
      push("ouverture_devis", {service: svc});
    });
    qm.addEventListener("close", function(){ document.body.classList.remove("qm-lock"); });
    qm.querySelector("[data-qm-close]").addEventListener("click", function(){ qm.close(); });
    qm.addEventListener("click", function(e){ if (e.target === qm) qm.close(); });
  }

  // Avant / après : le curseur déplace la séparation
  document.querySelectorAll(".ba-frame").forEach(function(f){
    var r = f.querySelector(".ba-range");
    r.addEventListener("input", function(){ f.style.setProperty("--pos", r.value + "%"); });
  });

  // Ciel au fil du défilement : nuit (haut) -> couchant (milieu) -> horizon doré (bas)
  var root = document.documentElement, ticking = false;
  function sky(){
    ticking = false;
    var max = Math.max(1, document.documentElement.scrollHeight - window.innerHeight);
    var p = Math.min(1, Math.max(0, window.scrollY / max));
    root.style.setProperty("--p", p.toFixed(3));
    root.style.setProperty("--o1", Math.max(0, 1 - p * 2).toFixed(3));
    root.style.setProperty("--o2", Math.max(0, 1 - Math.abs(p - 0.5) * 2).toFixed(3));
    root.style.setProperty("--o3", Math.max(0, p * 2 - 1).toFixed(3));
  }
  window.addEventListener("scroll", function(){ if (!ticking) { ticking = true; requestAnimationFrame(sky); } }, {passive: true});
  window.addEventListener("resize", sky);
  sky();

  // Bandeau cookies (choix conservé 6 mois)
  var box = document.getElementById("cookies");
  if (box) {
    if (!window.SLP_CHOICE) box.hidden = false;
    box.querySelectorAll("[data-cookies]").forEach(function(b){
      b.addEventListener("click", function(){
        var v = b.getAttribute("data-cookies");
        try { localStorage.setItem("slp_cookies", JSON.stringify({v: v, t: Date.now()})); } catch(e) {}
        window.SLP_CHOICE = v;
        if (v === "granted" && window.slpTags) window.slpTags();
        if (v === "denied" && window.slpTagsOn) location.reload();
        box.hidden = true;
      });
    });
    document.querySelectorAll("[data-open-consent]").forEach(function(b){
      b.addEventListener("click", function(){ box.hidden = false; });
    });
  }
})();
