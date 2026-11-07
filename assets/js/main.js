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

  // Grille tarifaire : onglet de l'heure actuelle à Paris, changement manuel possible
  var h;
  try { h = parseInt(new Intl.DateTimeFormat("fr-FR", {hour:"numeric", hour12:false, timeZone:"Europe/Paris"}).format(new Date()), 10); }
  catch(e) { h = new Date().getHours(); }
  if (isNaN(h)) h = new Date().getHours();
  h = h % 24;
  var current = h >= 8 && h < 18 ? "jour" : (h >= 18 && h < 22 ? "soir" : "nuit");
  function fmtH(x){ return (x % 12 || 12) + (x < 12 ? "am" : "pm"); }
  var labels = {jour:"day (8am – 6pm)", soir:"evening (6pm – 10pm)", nuit:"night (10pm – 8am)"};
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
          ? "<i></i>It is " + fmtH(h) + " in Paris: these are our " + labels[slot] + " prices."
          : "Prices for " + labels[slot] + ". It is currently " + fmtH(h) + " in Paris.";
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
