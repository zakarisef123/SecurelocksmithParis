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

  // Tranche horaire actuelle (heure de Paris) : mise en avant du bon tarif
  var h;
  try { h = parseInt(new Intl.DateTimeFormat("fr-FR", {hour:"numeric", hour12:false, timeZone:"Europe/Paris"}).format(new Date()), 10); }
  catch(e) { h = new Date().getHours(); }
  if (isNaN(h)) h = new Date().getHours();
  var slot = h >= 8 && h < 18 ? "jour" : (h >= 18 && h < 22 ? "soir" : "nuit");
  var labels = {jour:"journée", soir:"soirée", nuit:"nuit"};
  document.querySelectorAll('[data-slots] [data-slot="' + slot + '"], [data-tarifs] [data-slot="' + slot + '"]').forEach(function(el){ el.classList.add("now"); });
  document.querySelectorAll(".tarif-now").forEach(function(p){
    p.textContent = "Il est " + h + "h à Paris : la colonne « " + labels[slot] + " » est mise en avant.";
    p.hidden = false;
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
      btn.disabled = true; btn.textContent = "Envoi…";
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
