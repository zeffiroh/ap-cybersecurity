(function (global) {
  "use strict";

  var me = document.currentScript && document.currentScript.src;
  var ROOT = me ? me.replace(/assets\/theme\/student-extras\.js.*$/, "") : "";
  var $ = function (id) { return document.getElementById(id); };

  function esc(s) {
    return String(s == null ? "" : s).replace(/[&<>"]/g, function (c) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c];
    });
  }
  function rpc(fn, args) {
    var P = global.AayatProgress;
    return (P ? P.neon() : Promise.resolve(null)).then(function (db) {
      if (!db) throw new Error("The course database is not connected yet.");
      return db.rpc(fn, args || {}, { attempts: 1 });
    });
  }
  function email() { return global.Identity ? global.Identity.getEmail() : ""; }
  function signIn() { if (global.Identity) global.Identity.open({}, function () { location.reload(); }); }
  function map() { return global.AAYAT_MAP || { units: [], topics: {}, atoms: {} }; }
  function stores(k) { return ((global.APCYBER_STORES || {})[k] || {}); }
  function when(iso) {
    return iso ? new Date(iso).toLocaleString(undefined, { weekday: "short", day: "numeric", month: "short", hour: "numeric", minute: "2-digit" }) : "Time to be set";
  }
  function track(id) {
    var e = email();
    if (e) rpc("api_track", { p: { email: e, kind: "video", ref: "v" + id } }).catch(function () {  });
  }
  function player(yt, id) {
    return '<button class="sx-thumb" data-yt="' + esc(yt) + '" data-id="' + esc(id) + '" aria-label="Play video">' +
      '<img src="https://i.ytimg.com/vi/' + esc(yt) + '/hqdefault.jpg" alt="" loading="lazy"><span class="sx-play">&#9654;</span></button>';
  }
  function bindPlayers(root) {
    root.querySelectorAll(".sx-thumb").forEach(function (b) {
      b.addEventListener("click", function () {
        var f = document.createElement("iframe");
        f.className = "sx-frame";
        f.src = "https://www.youtube-nocookie.com/embed/" + b.getAttribute("data-yt") + "?autoplay=1&rel=0";
        f.allow = "accelerometer; autoplay; encrypted-media; picture-in-picture; fullscreen";
        f.allowFullscreen = true;
        b.replaceWith(f);
        if (b.getAttribute("data-id")) track(b.getAttribute("data-id"));
      });
    });
  }
  function buyBox(kind, title, extra) {
    var s = stores(kind), live = (s.methods || []).filter(function (m) { return m.url; });
    return '<div class="sx-buy"><b>' + esc(title) + "</b>" + (s.price ? "<div>" + esc(s.price) + "</div>" : "") +
      (extra ? "<p>" + extra + "</p>" : "") +
      (live.length ? '<div class="sx-btns">' + live.map(function (m) {
        return '<a class="btn" href="' + esc(m.url) + '" target="_blank" rel="noopener">' + esc(m.label) + "</a> <small>" + esc(m.note) + "</small>";
      }).join("<br>") + "</div><p><small>Use the email you sign in with. Access opens within about 5 minutes of paying.</small></p>"
        : "<p><small>Payments open soon. Ask your teacher in the meantime.</small></p>") + "</div>";
  }

  function lesson(box) {
    var atom = box.getAttribute("data-atom"), M = map(), a = M.atoms[atom];
    var dir = a ? a.href.replace(/index\.html$/, "") : "";
    var links = '<div class="sx-links"><a class="btn" href="' + ROOT + "notebook.html?ref=" + encodeURIComponent(atom) + '">My notebook for ' + esc(atom) + "</a>" +
      '<a class="btn" href="' + ROOT + "notebook.html?ref=" + encodeURIComponent(atom) + '&book=1">Open the code book</a>' +
      '<a class="btn" href="' + ROOT + 'classes.html">Get a live class</a></div>';
    box.innerHTML = links;
    rpc("api_lesson_video", { p_atom: atom }).then(function (d) {
      if (!d || !d.videos.length) return;
      var h = d.videos.map(function (v) {
        return '<div class="sx-video"><div class="sx-vh">Video lesson &middot; ' + esc(v.title) + (v.free ? " &middot; free" : "") + "</div>" +
          (v.youtube ? player(v.youtube, v.id) : '<div class="sx-locked"><span class="sx-lock">&#128274;</span>' +
            buyBox("videoPass", "Unlock every lesson video", "One payment, once, unlocks the video for every lesson.") +
            (email() ? "" : '<p><button class="btn" data-sx-signin>Already paid? Sign in</button></p>') + "</div>") +
          (v.note ? '<p class="sx-note">' + esc(v.note) + "</p>" : "") + "</div>";
      }).join("");
      box.insertAdjacentHTML("afterbegin", h);
      bindPlayers(box);
      var s = box.querySelector("[data-sx-signin]");
      if (s) s.addEventListener("click", signIn);
    }).catch(function () {  });
  }

  function classesPage(root) {
    var M = map();
    function topicName(t) { return t && M.topics[t] ? t + " " + M.topics[t].title : ""; }
    function price(c) {
      if (c.mode !== "paid" || (!c.inr && !c.usd)) return c.mode === "request" ? "Your requested class" : "Free";
      return [c.inr ? "₹" + c.inr : "", c.usd ? "$" + c.usd : ""].filter(Boolean).join(" · ");
    }
    function card(c) {
      var day = c.starts ? c.starts.slice(0, 10) : "";
      var full = c.capacity && c.taken >= c.capacity && c.seat === "none";
      var act = "";
      if (c.seat === "confirmed") {
        act = '<span class="sx-ok">You\'re in</span>' + (c.meet ? ' <a class="btn dark" href="' + esc(c.meet) + '" target="_blank" rel="noopener">Join the meeting</a>' : "");
      } else if (c.seat === "pending") {
        act = '<span class="sx-wait">Booked, waiting for payment</span>' +
          buyBox("classes", "Pay for class " + c.code + " (" + price(c) + ")", "At checkout, enter the class code <b>" + esc(c.code) + "</b>.") +
          ' <button class="btn" data-leave="' + c.id + '">Cancel booking</button>';
      } else if (full) {
        act = '<span class="sx-wait">Full</span>';
      } else {
        act = '<button class="btn dark" data-join="' + c.id + '">' + (c.mode === "paid" && (c.inr || c.usd) ? "Book a seat" : "Join") + "</button>";
      }
      return '<article class="sx-class"><div class="sx-when">' + esc(when(c.starts)) + " &middot; " + c.minutes + " min</div>" +
        "<h3>" + esc(c.title) + '</h3><div class="sx-meta">' + esc(price(c)) + (topicName(c.topic) ? " &middot; " + esc(topicName(c.topic)) : "") +
        (c.capacity ? " &middot; " + Math.max(0, c.capacity - c.taken) + " seats left" : "") + " &middot; code " + esc(c.code) + "</div>" +
        (c.note ? "<p>" + esc(c.note) + "</p>" : "") + '<div class="sx-act">' + act +
        (day ? ' <a class="btn" href="' + ROOT + "calendar.html?at=" + day + '">See it on the calendar</a>' : "") + "</div></article>";
    }
    function load() {
      $("sx-status").textContent = "Loading…";
      rpc("api_classes").then(function (d) {
        var now = Date.now(), list = d.classes || [];
        var up = list.filter(function (c) { return !c.starts || new Date(c.starts).getTime() + c.minutes * 60000 > now; });
        var past = list.filter(function (c) { return c.starts && new Date(c.starts).getTime() + c.minutes * 60000 <= now; });
        $("sx-status").textContent = d.me ? "Signed in as " + d.me : "Sign in to join, book or request a class.";
        $("sx-upcoming").innerHTML = up.length ? up.map(card).join("") : '<p class="sx-empty">No classes scheduled yet. Request one below.</p>';
        var recs = past.filter(function (c) { return c.hasRecording; });
        $("sx-recordings").innerHTML = recs.length ? '<div class="sx-gallery">' + recs.map(function (c) {
          return '<div class="sx-video"><div class="sx-vh">' + esc(c.title) + " &middot; " + esc(when(c.starts)) + "</div>" +
            (c.recording ? player(c.recording, "") : '<div class="sx-locked"><span class="sx-lock">&#128274;</span><p>For students who joined this class.</p></div>') + "</div>";
        }).join("") + "</div>" : '<p class="sx-empty">Recordings appear here after each class.</p>';
        $("sx-requests").innerHTML = (d.requests || []).length ? '<ul class="sx-list">' + d.requests.map(function (r) {
          return "<li>" + esc(topicName(r.topic) || "Any topic") + " &middot; <b>" + esc(r.status) + "</b>" + (r.times ? " &middot; " + esc(r.times) : "") + "</li>";
        }).join("") + "</ul>" : "";
        bindPlayers(root);
        root.querySelectorAll("[data-join]").forEach(function (b) {
          b.addEventListener("click", function () {
            if (!email()) return signIn();
            rpc("api_join_class", { p_id: +b.getAttribute("data-join") }).then(function (r) {
              if (!r.ok) throw new Error(r.error);
              load();
            }).catch(function (e) { $("sx-status").textContent = e.message; });
          });
        });
        root.querySelectorAll("[data-leave]").forEach(function (b) {
          b.addEventListener("click", function () { rpc("api_leave_class", { p_id: +b.getAttribute("data-leave") }).then(load); });
        });
      }).catch(function (e) { $("sx-status").textContent = "Could not load: " + e.message; });
    }
    $("sx-topic").innerHTML = '<option value="">Any topic</option>' + M.units.map(function (u) {
      return '<optgroup label="Unit ' + u.n + " " + esc(u.title) + '">' + u.topics.map(function (t) {
        return '<option value="' + t + '">' + esc(t + " " + M.topics[t].title) + "</option>";
      }).join("") + "</optgroup>";
    }).join("");
    $("sx-request").addEventListener("click", function () {
      if (!email()) return signIn();
      rpc("api_request_class", { p: { topic: $("sx-topic").value, times: $("sx-times").value, note: $("sx-note").value } }).then(function (r) {
        if (!r.ok) throw new Error(r.error);
        $("sx-req-msg").textContent = "Sent. You'll see it on your calendar once it's scheduled.";
        $("sx-times").value = ""; $("sx-note").value = "";
        load();
      }).catch(function (e) { $("sx-req-msg").textContent = e.message; });
    });
    load();
  }

  function videosPage(root) {
    var M = map();
    rpc("api_my_feed").then(function (f) {
      var vids = f.videos || [];
      $("sx-pass").innerHTML = f.videoAccess ? '<p class="sx-ok">You have the video pass. Every lesson video is unlocked.</p>'
        : buyBox("videoPass", "Video pass: every lesson video, one payment", "Pay once and keep every lesson video, including new ones.") +
          (f.me ? "" : '<p><button class="btn" data-sx-signin>Already paid? Sign in</button></p>');
      var s = root.querySelector("[data-sx-signin]");
      if (s) s.addEventListener("click", signIn);
      if (!vids.length) { $("sx-videos").innerHTML = '<p class="sx-empty">No videos yet.</p>'; return; }
      var byTopic = {}, other = [];
      vids.forEach(function (v) {
        var t = v.atom ? v.atom.split(".").slice(0, 2).join(".") : v.topic;
        if (t && M.topics[t]) (byTopic[t] = byTopic[t] || []).push(v); else other.push(v);
      });
      var h = [];
      M.units.forEach(function (u) {
        var ts = u.topics.filter(function (t) { return byTopic[t]; });
        if (!ts.length) return;
        h.push("<h2>Unit " + u.n + " &middot; " + esc(u.title) + "</h2>");
        ts.forEach(function (t) {
          h.push('<h3><span class="aa-id">' + t + "</span>" + esc(M.topics[t].title) + '</h3><div class="sx-gallery">' + byTopic[t].map(vcard).join("") + "</div>");
        });
      });
      if (other.length) h.push('<h2>More videos</h2><div class="sx-gallery">' + other.map(vcard).join("") + "</div>");
      $("sx-videos").innerHTML = h.join("");
      bindPlayers(root);
      if (location.hash) { var el = document.querySelector(location.hash); if (el) el.scrollIntoView(); }
    }).catch(function (e) { $("sx-videos").textContent = "Could not load: " + e.message; });
    function vcard(v) {
      var a = v.atom && M.atoms[v.atom];
      return '<div class="sx-video" id="v' + v.id + '"><div class="sx-vh">' + esc(v.title) + (v.free ? " &middot; free" : "") + "</div>" +
        (v.youtube ? player(v.youtube, v.id) : '<div class="sx-locked"><span class="sx-lock">&#128274;</span><p>Part of the video pass.</p></div>') +
        (a ? '<p class="sx-note"><a href="' + ROOT + a.href + '">' + esc(v.atom + " " + a.title) + "</a></p>" : "") +
        (v.note ? '<p class="sx-note">' + esc(v.note) + "</p>" : "") + "</div>";
    }
  }

  function start() {
    var l = document.querySelector("[data-extras=lesson]");
    if (l) lesson(l);
    if ($("sx-classes")) classesPage($("sx-classes"));
    if ($("sx-videos-page")) videosPage($("sx-videos-page"));
  }
  if (document.readyState === "complete") start();
  else global.addEventListener("load", start);
})(window);
