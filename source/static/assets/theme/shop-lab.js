(function (global) {
  "use strict";

  var me = document.currentScript && document.currentScript.src;
  var ROOT = me ? me.replace(/assets\/theme\/shop-lab\.js.*$/, "") : "";
  var $ = function (id) { return document.getElementById(id); };
  var K, esc, SQL = null;
  var SECRET = "nimbu-" + Math.random().toString(36).slice(2);

  var MISSIONS = [
    { id: "shop-error", points: 50, title: "Leaky errors", text: "Make the shop show you a raw database error.",
      hint: "Search for a single quote and look at the API response in the Network tab." },
    { id: "shop-backup", points: 100, title: "Forgotten backup", text: "Find a backup file the developers forgot to delete.",
      hint: "Visit /robots.txt in the address bar. It lists places the owners would rather nobody looked." },
    { id: "shop-sqli", points: 150, title: "Log in as the admin", text: "Log in as admin@nimbu.shop without the password.",
      hint: "The email goes straight into SQL inside quotes. End the quote and comment out the password check." },
    { id: "shop-admin", points: 100, title: "The page nobody links to", text: "Open the shop's administration page.",
      hint: "Read the shop's code in Sources to find the route name. You'll need an admin session." },
    { id: "shop-idor", points: 150, title: "Other people's orders", text: "Read an order that belongs to someone else.",
      hint: "Log in as demo@nimbu.shop / demo123, open one of your orders and watch the API call. Then change the number." },
    { id: "shop-xss", points: 200, title: "Stored XSS", text: "Post a review that pops up an alert box for everyone who views the product.",
      hint: "Reviews are shown as HTML. Try <img src=x onerror=alert(1)>." },
    { id: "shop-negative", points: 150, title: "They pay you", text: "Check out with a basket total below zero.",
      hint: "Add something to the basket, then use Edit and resend on POST /api/basket with a negative qty." },
    { id: "shop-feedback", points: 100, title: "Zero stars", text: "Send feedback with a rating of 0. The form only offers 1 to 5.",
      hint: "Send the form once, then edit the request's JSON and resend it." },
    { id: "shop-reset", points: 150, title: "Reset Jim's password", text: "Reset the password for jim@nimbu.shop through his security question.",
      hint: "The question asks for his pet's name. Read the product reviews." },
    { id: "shop-coupon", points: 150, title: "Coupon twice", text: "WELCOME10 takes 10% off, once per customer. Get more than 10% off one basket.",
      hint: "Apply the coupon, then try it again written a little differently. Does the shop compare codes the same way every time?" },
    { id: "shop-redirect", points: 100, title: "Open redirect", text: "Make a nimbu.shop link that sends visitors to a website of your choice.",
      hint: "Sources shows a footer link that goes through /go?to=. Type /go?to=https://example.com in the address bar." },
    { id: "shop-upload", points: 200, title: "Not a picture", text: "Upload a profile picture that runs JavaScript when someone opens it.",
      hint: "Profile page. The upload only checks that the name contains .png. Try a name like me.png.html with <img src=x onerror=alert(1)> inside, then open its link." },
    { id: "shop-jwt", points: 250, title: "Forge a token", text: "Become admin by editing your login token, without the admin password.",
      hint: "Storage tab: decode the token, set alg to none, role to admin, delete the signature, keep the last dot, re-encode." }
  ];

  var PRODUCTS = [
    [1, "Cat-ear gaming headset", "Glowing ears, decent sound, terrible microphone.", 59, "🎧"],
    [2, "Mechanical keyboard", "Loud enough to annoy the whole house.", 89, "⌨️"],
    [3, "Privacy webcam cover", "Slide it shut. Three-pack.", 4, "📷"],
    [4, "USB data blocker", "Charge at the airport without sharing your data.", 9, "🔌"],
    [5, "Hardware security key", "Phishing-resistant two-factor login.", 45, "🔑"],
    [6, "Lock-pick practice set", "Clear practice lock and picks. For your own locks only.", 29, "🔒"],
    [7, "Faraday phone pouch", "Blocks signals in and out.", 19, "📵"],
    [8, "Sticker pack: I read the logs", "Five vinyl stickers.", 3, "🏷️"]
  ];

  var S;

  function h(s) {
    var a = 0x811c9dc5, b = 0x01000193 ^ 0x5bd1e995;
    for (var i = 0; i < s.length; i++) {
      a = Math.imul(a ^ s.charCodeAt(i), 0x01000193) >>> 0;
      b = Math.imul(b ^ s.charCodeAt(i), 0x5bd1e995) >>> 0;
      b ^= b >>> 13;
    }
    return ("0000000" + a.toString(16)).slice(-8) + ("0000000" + (b >>> 0).toString(16)).slice(-8);
  }

  function b64u(s) {
    return btoa(unescape(encodeURIComponent(s))).replace(/\+/g, "-").replace(/\//g, "_").replace(/=+$/, "");
  }
  function unb64u(s) {
    s = String(s).replace(/-/g, "+").replace(/_/g, "/");
    while (s.length % 4) s += "=";
    return decodeURIComponent(escape(atob(s)));
  }

  function sign(data) { return h(SECRET + "." + data) + h(data + "." + SECRET); }

  function token(u) {
    var data = b64u(JSON.stringify({ alg: "HS256", typ: "JWT" })) + "." +
      b64u(JSON.stringify({ sub: u.id, email: u.email, role: u.role, iat: Math.floor(Date.now() / 1000) }));
    return data + "." + sign(data);
  }

  function verify(t) {
    var p = String(t || "").split(".");
    if (p.length !== 3) return null;
    var head, body;
    try { head = JSON.parse(unb64u(p[0])); body = JSON.parse(unb64u(p[1])); } catch (e) { return null; }
    if (String(head.alg || "").toLowerCase() === "none") return { claims: body, none: true };
    if (head.alg === "HS256" && p[2] === sign(p[0] + "." + p[1])) return { claims: body, none: false };
    return null;
  }

  function fresh() {
    var db = new SQL.Database();
    db.run("CREATE TABLE users (id INTEGER PRIMARY KEY, email TEXT, password TEXT, role TEXT, question TEXT, answer TEXT);" +
      "CREATE TABLE products (id INTEGER PRIMARY KEY, name TEXT, description TEXT, price REAL, icon TEXT, deleted INTEGER DEFAULT 0);" +
      "CREATE TABLE orders (id INTEGER PRIMARY KEY, user_id INTEGER, items TEXT, total REAL, address TEXT, note TEXT);");
    var add = function (sql, rows) { var s = db.prepare(sql); rows.forEach(function (r) { s.run(r); }); s.free(); };
    add("INSERT INTO users VALUES (?, ?, ?, ?, ?, ?)", [
      [1, "admin@nimbu.shop", h("Zx!" + Math.random()), "admin", "What city were you born in?", "x" + Math.random()],
      [2, "jim@nimbu.shop", h("ncc-1701-d"), "customer", "What is your pet's name?", "bruno"],
      [3, "demo@nimbu.shop", h("demo123"), "customer", "What is your favourite colour?", "green"],
      [4, "priya@nimbu.shop", h("p@ssw0rd!"), "customer", "What was your first school?", "st marys"]]);
    add("INSERT INTO products (id, name, description, price, icon) VALUES (?, ?, ?, ?, ?)", PRODUCTS);
    add("INSERT INTO products (id, name, description, price, icon, deleted) VALUES (?, ?, ?, ?, ?, ?)",
      [[9, "Christmas special (withdrawn)", "Old stock.", 0.01, "🎁", 1]]);
    add("INSERT INTO orders VALUES (?, ?, ?, ?, ?, ?)", [
      [1, 1, "1 x Hardware security key", 45, "Admin office, NimbuMart HQ", "Internal: " + K.reveal("shop-idor")],
      [2, 2, "2 x Sticker pack: I read the logs", 6, "14 Lake Road", "Leave with the neighbour"],
      [3, 3, "1 x Privacy webcam cover", 4, "Demo Street 1", ""],
      [4, 3, "1 x USB data blocker", 9, "Demo Street 1", "Gift wrap please"],
      [5, 4, "1 x Faraday phone pouch", 19, "22 Hill View", ""]]);
    S = {
      db: db, reviews: {
        1: [{ by: "jim@nimbu.shop", text: "Great for long gaming nights. My dog Bruno howls every time the ears light up though!" },
          { by: "priya@nimbu.shop", text: "The microphone is useless but the ears are cute." }],
        5: [{ by: "priya@nimbu.shop", text: "Set it up on every account. Phishing pages can't use it. Worth it." }],
        6: [{ by: "jim@nimbu.shop", text: "Opened my practice lock in 20 minutes. Bruno was not impressed." }]
      },
      baskets: {}, coupons: {}, discount: {}, uploads: {}, nextOrder: 6, feedback: [], token: "", log: [], history: [], path: "/#/", pick: null, rep: null, tab: "net"
    };
  }

  function rows(r) {
    if (!r.length) return [];
    return r[0].values.map(function (v) { var o = {}; r[0].columns.forEach(function (c, i) { o[c] = v[i]; }); return o; });
  }

  function q(sql, args) {
    var st = S.db.prepare(sql);
    if (args) st.bind(args);
    var out = [];
    while (st.step()) out.push(st.getAsObject());
    st.free();
    return out;
  }

  function json(status, body) { return { status: status, type: "application/json", body: JSON.stringify(body, null, 2) }; }
  function text(status, body, type) { return { status: status, type: type || "text/plain", body: body }; }

  function auth(req) {
    var a = (req.headers.authorization || "").replace(/^Bearer\s+/i, "");
    if (!a) return null;
    return verify(a);
  }

  function sqlError(e, sql) {
    K.award("shop-error", "Leaky errors");
    return json(500, { error: "SQLITE_ERROR: " + (e.message || e), query: sql,
      stack: "at Database.exec (/srv/nimbu/node_modules/sqlite/db.js:211)\nat ProductController.search (/srv/nimbu/routes/products.js:48)" });
  }

  var ROUTES = [
    ["GET", /^\/robots\.txt$/, function () { return text(200, "User-agent: *\nDisallow: /ftp\nDisallow: /api/admin\n"); }],
    ["GET", /^\/ftp\/?$/, function () {
      return text(200, "Index of /ftp\n\n  legal.md              2026-02-11   1.2 KB\n  backup-2026.bak       2026-09-30  18.4 KB\n  quarantine/           2026-10-02      -\n");
    }],
    ["GET", /^\/ftp\/legal\.md$/, function () { return text(200, "# Terms\n\nWe may change prices at any time. Hacking this shop is allowed only in this lab.\n"); }],
    ["GET", /^\/ftp\/backup-2026\.bak$/, function () {
      K.award("shop-backup", "Forgotten backup");
      return text(200, "-- NimbuMart nightly dump 2026-09-30\nCREATE TABLE users (id, email, password, role, question, answer);\n" +
        "INSERT INTO users VALUES (1, 'admin@nimbu.shop', '<redacted>', 'admin', ...);\n-- deploy key: " + K.reveal("shop-backup") + "\n");
    }],
    ["GET", /^\/ftp\/quarantine\/?$/, function () { return text(403, "403 Forbidden"); }],
    ["POST", /^\/api\/login$/, function (req) {
      var b = req.json || {};
      var sql = "SELECT id, email, role FROM users WHERE email = '" + (b.email || "") + "' AND password = '" + h(String(b.password || "")) + "'";
      var r;
      try { r = rows(S.db.exec(sql)); } catch (e) { return sqlError(e, sql); }
      if (!r.length) return json(401, { error: "Invalid email or password." });
      var u = r[0];
      if (u.role === "admin") K.award("shop-sqli", "Log in as the admin");
      return json(200, { token: token(u), user: { id: u.id, email: u.email, role: u.role } });
    }],
    ["GET", /^\/api\/products$/, function (req) {
      var term = req.query.q || "";
      var sql = "SELECT id, name, price FROM products WHERE name LIKE '%" + term + "%' AND deleted = 0";
      try { return json(200, { data: rows(S.db.exec(sql)) }); } catch (e) { return sqlError(e, sql); }
    }],
    ["GET", /^\/api\/products\/(\d+)$/, function (req, m) {
      var p = q("SELECT id, name, description, price, icon FROM products WHERE id = ? AND deleted = 0", [+m[1]])[0];
      if (!p) return json(404, { error: "No such product." });
      p.reviews = S.reviews[p.id] || [];
      return json(200, { data: p });
    }],
    ["POST", /^\/api\/products\/(\d+)\/reviews$/, function (req, m) {
      var a = auth(req);
      if (!a) return json(401, { error: "Log in to write a review." });
      var t = String((req.json || {}).text || "").slice(0, 2000);
      if (!t.trim()) return json(400, { error: "Write something first." });
      (S.reviews[+m[1]] = S.reviews[+m[1]] || []).push({ by: a.claims.email, text: t });
      return json(201, { ok: true });
    }],
    ["GET", /^\/api\/me$/, function (req) {
      var a = auth(req);
      return a ? json(200, { data: a.claims }) : json(401, { error: "Not logged in." });
    }],
    ["GET", /^\/api\/orders$/, function (req) {
      var a = auth(req);
      if (!a) return json(401, { error: "Not logged in." });
      return json(200, { data: q("SELECT id, items, total FROM orders WHERE user_id = ? ORDER BY id", [a.claims.sub]) });
    }],
    ["GET", /^\/api\/orders\/(\d+)$/, function (req, m) {
      var a = auth(req);
      if (!a) return json(401, { error: "Not logged in." });
      var o = q("SELECT * FROM orders WHERE id = ?", [+m[1]])[0];
      if (!o) return json(404, { error: "No such order." });
      if (o.user_id !== a.claims.sub) K.award("shop-idor", "Other people's orders");
      return json(200, { data: o });
    }],
    ["GET", /^\/api\/basket$/, function (req) {
      var a = auth(req);
      if (!a) return json(401, { error: "Not logged in." });
      return json(200, { data: basket(a.claims.sub) });
    }],
    ["POST", /^\/api\/basket$/, function (req) {
      var a = auth(req);
      if (!a) return json(401, { error: "Not logged in." });
      var b = req.json || {}, qty = parseInt(b.qty, 10), pid = parseInt(b.productId, 10);
      if (!q("SELECT id FROM products WHERE id = ? AND deleted = 0", [pid]).length) return json(404, { error: "No such product." });
      if (!qty) return json(400, { error: "qty must be a number." });
      var bk = S.baskets[a.claims.sub] = S.baskets[a.claims.sub] || {};
      bk[pid] = (bk[pid] || 0) + qty;
      if (!bk[pid]) delete bk[pid];
      return json(200, { data: basket(a.claims.sub) });
    }],
    ["POST", /^\/api\/checkout$/, function (req) {
      var a = auth(req);
      if (!a) return json(401, { error: "Not logged in." });
      var bk = basket(a.claims.sub);
      if (!bk.items.length) return json(400, { error: "Your basket is empty." });
      var id = S.nextOrder++;
      q("INSERT INTO orders VALUES (?, ?, ?, ?, ?, ?)", [id, a.claims.sub, bk.items.map(function (i) { return i.qty + " x " + i.name; }).join(", "),
        bk.total, "On file", ""]);
      S.baskets[a.claims.sub] = {};
      S.discount[a.claims.sub] = 0;
      var out = { ok: true, order: id, total: bk.total };
      if (bk.total < 0) {
        K.award("shop-negative", "They pay you");
        out.message = "Refund of " + (-bk.total).toFixed(2) + " credited to your wallet.";
      }
      return json(200, out);
    }],
    ["POST", /^\/api\/coupon$/, function (req) {
      var a = auth(req);
      if (!a) return json(401, { error: "Not logged in." });
      var code = String((req.json || {}).code || "").trim(), uid = a.claims.sub;
      if (code.toUpperCase() !== "WELCOME10") return json(404, { error: "No such coupon." });
      var used = S.coupons[uid] = S.coupons[uid] || {};
      if (used[code]) return json(409, { error: "You have already used " + code + "." });
      used[code] = true;
      S.discount[uid] = (S.discount[uid] || 0) + 10;
      if (S.discount[uid] > 10) K.award("shop-coupon", "Coupon twice");
      return json(200, { ok: true, discount: S.discount[uid], data: basket(uid) });
    }],
    ["GET", /^\/go$/, function (req) {
      var to = String(req.query.to || "");
      if (!to) return json(400, { error: "to is required." });
      if (/^(https?:)?\/\//i.test(to) && !/^(https?:)?\/\/([a-z0-9-]+\.)*nimbu\.shop(\/|$)/i.test(to)) K.award("shop-redirect", "Open redirect");
      return text(302, "302 Found\nLocation: " + to + "\n\nRedirecting you to " + to + " ...");
    }],
    ["POST", /^\/api\/avatar$/, function (req) {
      var a = auth(req);
      if (!a) return json(401, { error: "Not logged in." });
      var b = req.json || {}, name = String(b.filename || "").replace(/[^A-Za-z0-9._-]/g, "").slice(0, 60);
      if (!/\.(png|jpe?g|gif)/i.test(name)) return json(400, { error: "Only pictures (.png, .jpg, .gif) please." });
      S.uploads[name] = { by: a.claims.email, body: String(b.content || "").slice(0, 4000) };
      return json(201, { ok: true, url: "/uploads/" + name });
    }],
    ["GET", /^\/uploads\/([A-Za-z0-9._-]+)$/, function (req, m) {
      var f = S.uploads[m[1]];
      if (!f) return text(404, "404 Not Found");
      return text(200, f.body, /\.(html?|svg)$/i.test(m[1]) ? "text/html" : "image/png");
    }],
    ["POST", /^\/api\/feedback$/, function (req) {
      var b = req.json || {}, rating = Number(b.rating);
      if (isNaN(rating)) return json(400, { error: "rating must be a number." });
      S.feedback.push({ rating: rating, comment: String(b.comment || "").slice(0, 500) });
      if (rating < 1 || rating > 5) K.award("shop-feedback", "Zero stars");
      return json(201, { ok: true, thanks: "Thanks for your " + rating + "-star feedback!" });
    }],
    ["GET", /^\/api\/reset-question$/, function (req) {
      var u = q("SELECT question FROM users WHERE email = ?", [String(req.query.email || "").toLowerCase()])[0];
      return u ? json(200, { question: u.question }) : json(404, { error: "No account with that email." });
    }],
    ["POST", /^\/api\/reset$/, function (req) {
      var b = req.json || {}, email = String(b.email || "").toLowerCase();
      var u = q("SELECT id, answer FROM users WHERE email = ?", [email])[0];
      if (!u) return json(404, { error: "No account with that email." });
      if (String(b.answer || "").trim().toLowerCase() !== u.answer) return json(403, { error: "Wrong answer." });
      if (String(b.newPassword || "").length < 4) return json(400, { error: "Choose a longer password." });
      q("UPDATE users SET password = ? WHERE id = ?", [h(String(b.newPassword)), u.id]);
      if (email === "jim@nimbu.shop") K.award("shop-reset", "Reset Jim's password");
      return json(200, { ok: true, message: "Password changed. You can log in now." });
    }],
    ["GET", /^\/api\/admin\/users$/, function (req) {
      var a = auth(req);
      if (!a) return json(401, { error: "Not logged in." });
      if (a.claims.role !== "admin") return json(403, { error: "Admins only." });
      if (a.none) K.award("shop-jwt", "Forge a token");
      return json(200, { data: q("SELECT id, email, role FROM users ORDER BY id"), feedback: S.feedback });
    }]
  ];

  function basket(uid) {
    var bk = S.baskets[uid] || {}, items = [], total = 0;
    Object.keys(bk).forEach(function (pid) {
      var p = q("SELECT name, price FROM products WHERE id = ?", [+pid])[0];
      if (!p) return;
      items.push({ productId: +pid, name: p.name, price: p.price, qty: bk[pid] });
      total += p.price * bk[pid];
    });
    var off = Math.min(S.discount[uid] || 0, 100);
    if (off) total = total * (100 - off) / 100;
    return { items: items, discount: off, total: Math.round(total * 100) / 100 };
  }

  function parse(path) {
    var u = new URL(path, "https://nimbu.shop"), query = {};
    u.searchParams.forEach(function (v, k) { query[k] = v; });
    return { path: u.pathname, query: query };
  }

  function server(req) {
    var p = parse(req.path);
    req.query = p.query;
    req.headers = req.headers || {};
    try { req.json = req.body ? JSON.parse(req.body) : null; } catch (e) { return json(400, { error: "Body is not valid JSON." }); }
    var known = false;
    for (var i = 0; i < ROUTES.length; i++) {
      var m = p.path.match(ROUTES[i][1]);
      if (m && ROUTES[i][0] === req.method) return ROUTES[i][2](req, m);
      if (m) known = true;
    }
    if (known) return json(405, { error: "Method not allowed." });
    return p.path.indexOf("/api/") === 0 ? json(404, { error: "Not found." }) : text(404, "404 Not Found");
  }

  function send(method, path, body, extra) {
    var headers = {};
    if (S.token) headers.authorization = "Bearer " + S.token;
    if (body != null) headers["content-type"] = "application/json";
    Object.keys(extra || {}).forEach(function (k) { headers[k.toLowerCase()] = extra[k]; });
    var req = { method: method, path: path, headers: headers, body: body == null ? "" : typeof body === "string" ? body : JSON.stringify(body) };
    var res = server({ method: req.method, path: req.path, headers: Object.assign({}, headers), body: req.body });
    S.log.unshift({ req: req, res: res, at: new Date() });
    if (S.log.length > 80) S.log.pop();
    if (S.tab === "net") dev();
    var data = null;
    try { data = res.type === "application/json" ? JSON.parse(res.body) : res.body; } catch (e) {}
    return { status: res.status, data: data, raw: res };
  }

  function el(html) { $("sh-page").innerHTML = html; }

  function header() {
    var who = S.token && verify(S.token);
    return '<div class="sh-top"><a href="#" data-go="/#/" class="sh-logo">🍋 NimbuMart</a>' +
      '<form class="sh-search" data-search><input name="q" placeholder="Search products" value=""><button class="btn">Search</button></form>' +
      '<nav><a href="#" data-go="/#/basket">Basket</a><a href="#" data-go="/#/orders">Orders</a><a href="#" data-go="/#/profile">Profile</a><a href="#" data-go="/#/feedback">Feedback</a>' +
      (who ? '<span class="sh-who">' + esc(who.claims.email) + '</span><a href="#" data-logout>Log out</a>' : '<a href="#" data-go="/#/login">Log in</a>') +
      "</nav></div>";
  }

  function grid(list) {
    if (!list.length) return '<p class="sx-empty">No products found.</p>';
    return '<div class="sh-grid">' + list.map(function (p) {
      var icon = (PRODUCTS.filter(function (x) { return x[0] === p.id; })[0] || [])[4] || "📦";
      return '<a href="#" class="sh-card" data-go="/#/product/' + esc(p.id) + '"><span class="sh-icon">' + icon + "</span><b>" + esc(p.name) +
        "</b><span>₹" + esc(p.price) + "</span></a>";
    }).join("") + "</div>";
  }

  function raw(r) {
    return '<pre class="sh-raw">' + esc(r.raw.status + " " + (r.raw.type || "") + "\n\n" + r.raw.body) + "</pre>";
  }

  function needLogin() { return '<p>Please <a href="#" data-go="/#/login">log in</a> first.</p>'; }

  function reviewsFrame(list) {
    var html = list.map(function (r) { return '<div class="r"><b>' + r.by.replace(/</g, "&lt;") + "</b><div>" + r.text + "</div></div>"; }).join("") ||
      "<p><i>No reviews yet.</i></p>";
    var doc = "<!doctype html><meta charset=utf-8><style>body{font:15px/1.5 Georgia,serif;margin:8px;color:#111}.r{border-bottom:1px solid #ddd;padding:6px 0}" +
      "b{font-size:13px;color:#555}</style><script>(function(){function s(k){return function(m){parent.postMessage({nimbuXss:k,msg:String(m)},'*')}}" +
      "window.alert=s('alert');window.confirm=s('confirm');window.prompt=s('prompt');})()<\/script>" + html;
    return '<iframe class="sh-reviews" sandbox="allow-scripts" title="Reviews" srcdoc="' + esc(doc) + '"></iframe>';
  }

  var VIEWS = [
    [/^\/#\/?$/, function () {
      var r = send("GET", "/api/products?q=");
      el(header() + '<h2 class="sh-h">Gear for careful people</h2>' + (r.status === 200 ? grid(r.data.data) : raw(r)));
    }],
    [/^\/#\/search\?q=(.*)$/, function (m) {
      var term = decodeURIComponent(m[1].replace(/\+/g, " "));
      var r = send("GET", "/api/products?q=" + encodeURIComponent(term));
      el(header() + '<h2 class="sh-h">Results for “' + esc(term) + "”</h2>" +
        (r.status === 200 ? grid(r.data.data) : '<p class="sq-bad">Something went wrong.</p>' + raw(r)));
    }],
    [/^\/#\/product\/(\d+)$/, function (m) {
      var r = send("GET", "/api/products/" + m[1]);
      if (r.status !== 200) return el(header() + raw(r));
      var p = r.data.data;
      el(header() + '<div class="sh-product"><span class="sh-icon big">' + p.icon + "</span><div><h2>" + esc(p.name) + "</h2><p>" + esc(p.description) +
        '</p><p class="sh-price">₹' + esc(p.price) + '</p><form data-basket="' + p.id + '"><label>Quantity <input name="qty" type="number" min="1" max="20" value="1"></label> ' +
        '<button class="btn dark">Add to basket</button> <span class="sh-msg"></span></form></div></div><h3>Reviews</h3>' + reviewsFrame(p.reviews) +
        (S.token ? '<form data-review="' + p.id + '" class="sh-form"><label>Your review <textarea name="text" rows="2"></textarea></label><button class="btn">Post review</button></form>' :
          '<p class="sx-note">Log in to write a review.</p>'));
    }],
    [/^\/#\/login$/, function () {
      el(header() + '<form class="sh-form" data-login><h2>Log in</h2><label>Email <input name="email" autocomplete="off"></label>' +
        '<label>Password <input name="password" type="password"></label><button class="btn dark">Log in</button> <span class="sh-msg"></span>' +
        '<p class="sx-note">Demo account: demo@nimbu.shop / demo123 · <a href="#" data-go="/#/forgot">Forgot your password?</a></p></form>');
    }],
    [/^\/#\/forgot$/, function () {
      el(header() + '<form class="sh-form" data-forgot><h2>Reset your password</h2><label>Email <input name="email" autocomplete="off"></label>' +
        '<button class="btn">Get my security question</button><div class="sh-q"></div><span class="sh-msg"></span></form>');
    }],
    [/^\/#\/basket$/, function () {
      if (!S.token) return el(header() + needLogin());
      var r = send("GET", "/api/basket");
      if (r.status !== 200) return el(header() + raw(r));
      var b = r.data.data;
      el(header() + "<h2>Your basket</h2>" + (b.items.length ? '<table class="sq-table"><tr><th>Item</th><th>Qty</th><th>Price</th></tr>' +
        b.items.map(function (i) { return "<tr><td>" + esc(i.name) + "</td><td>" + esc(i.qty) + "</td><td>₹" + esc(i.price) + "</td></tr>"; }).join("") +
        "</table>" + (b.discount ? "<p>Discount: " + esc(b.discount) + "%</p>" : "") +
        '<form class="sh-form sh-inline" data-coupon><label>Coupon <input name="code" placeholder="WELCOME10"></label><button class="btn">Apply</button> <span class="sh-msg"></span></form>' +
        '<p class="sh-price">Total: ₹' + esc(b.total) + '</p><button class="btn dark" data-checkout>Check out</button> <span class="sh-msg"></span>' :
        '<p class="sx-empty">Your basket is empty.</p>'));
    }],
    [/^\/#\/orders$/, function () {
      if (!S.token) return el(header() + needLogin());
      var r = send("GET", "/api/orders");
      if (r.status !== 200) return el(header() + raw(r));
      el(header() + "<h2>Your orders</h2>" + (r.data.data.length ? "<ul>" + r.data.data.map(function (o) {
        return '<li><a href="#" data-go="/#/order/' + o.id + '">Order #' + o.id + "</a>: " + esc(o.items) + " (₹" + esc(o.total) + ")</li>";
      }).join("") + "</ul>" : '<p class="sx-empty">No orders yet.</p>'));
    }],
    [/^\/#\/order\/(\d+)$/, function (m) {
      if (!S.token) return el(header() + needLogin());
      var r = send("GET", "/api/orders/" + m[1]);
      if (r.status !== 200) return el(header() + raw(r));
      var o = r.data.data;
      el(header() + "<h2>Order #" + esc(o.id) + "</h2><p>" + esc(o.items) + "</p><p>Total: ₹" + esc(o.total) + "</p><p>Ship to: " + esc(o.address) + "</p>" +
        (o.note ? "<p>Note: " + esc(o.note) + "</p>" : ""));
    }],
    [/^\/#\/profile$/, function () {
      if (!S.token) return el(header() + needLogin());
      var mine = Object.keys(S.uploads);
      el(header() + '<h2>Your profile</h2><form class="sh-form" data-avatar><h3>Profile picture</h3>' +
        '<label>File name <input name="filename" placeholder="me.png"></label>' +
        '<label>File contents <textarea name="content" rows="3" placeholder="(this lab pretends the file is text)"></textarea></label>' +
        '<button class="btn dark">Upload</button> <span class="sh-msg"></span></form>' +
        (mine.length ? "<h3>Uploaded</h3><ul>" + mine.map(function (n) { return '<li><a href="#" data-go="/uploads/' + esc(n) + '">/uploads/' + esc(n) + "</a></li>"; }).join("") + "</ul>" : ""));
    }],
    [/^\/#\/feedback$/, function () {
      el(header() + '<form class="sh-form" data-feedback><h2>Tell us how we did</h2><label>Rating <select name="rating">' +
        [5, 4, 3, 2, 1].map(function (n) { return "<option>" + n + "</option>"; }).join("") + '</select></label>' +
        '<label>Comment <textarea name="comment" rows="3" maxlength="200"></textarea></label><button class="btn dark">Send</button> <span class="sh-msg"></span></form>');
    }],
    [/^\/#\/administration$/, function () {
      var r = send("GET", "/api/admin/users");
      if (r.status !== 200) return el(header() + '<h2>403 Forbidden</h2><p>' + esc((r.data && r.data.error) || "") + "</p>");
      K.award("shop-admin", "The page nobody links to");
      el(header() + '<h2>Administration</h2><p class="sq-good">' + esc(K.reveal("shop-admin")) + '</p><h3>Users</h3><table class="sq-table"><tr><th>id</th><th>email</th><th>role</th></tr>' +
        r.data.data.map(function (u) { return "<tr><td>" + u.id + "</td><td>" + esc(u.email) + "</td><td>" + esc(u.role) + "</td></tr>"; }).join("") +
        "</table><h3>Customer feedback</h3>" + (r.data.feedback.length ? "<ul>" + r.data.feedback.map(function (f) {
          return "<li>" + esc(f.rating) + " stars: " + esc(f.comment) + "</li>";
        }).join("") + "</ul>" : '<p class="sx-empty">None yet.</p>'));
    }]
  ];

  function go(path, noHistory) {
    path = String(path || "/#/").trim();
    if (/^https?:\/\/nimbu\.shop/i.test(path)) path = path.replace(/^https?:\/\/nimbu\.shop/i, "");
    if (path.charAt(0) !== "/") path = "/" + path;
    if (path === "/" || path === "/index.html") path = "/#/";
    if (!noHistory && S.path !== path) S.history.push(S.path);
    S.path = path;
    $("sh-url").value = path;
    for (var i = 0; i < VIEWS.length; i++) {
      var m = path.match(VIEWS[i][0]);
      if (m) { VIEWS[i][1](m); return; }
    }
    if (path.indexOf("/#/") === 0) return el(header() + "<h2>Page not found</h2>");
    var r = send("GET", path);
    if (/^\/uploads\//.test(path) && r.raw.type === "text/html") {
      var doc = "<!doctype html><meta charset=utf-8><script>(function(){function s(k){return function(m){parent.postMessage({nimbuUpload:k,msg:String(m)},'*')}}" +
        "window.alert=s('alert');window.confirm=s('confirm');window.prompt=s('prompt');})()<\/script>" + r.raw.body;
      return el('<iframe class="sh-upframe" sandbox="allow-scripts" title="Uploaded file" srcdoc="' + esc(doc) + '"></iframe>');
    }
    el('<pre class="sh-raw sh-plain">' + esc(r.raw.body) + "</pre>");
  }

  function form(f) {
    var o = {};
    Array.prototype.forEach.call(f.elements, function (e) { if (e.name) o[e.name] = e.value; });
    return o;
  }

  function onSubmit(e) {
    var f = e.target, msg = f.querySelector(".sh-msg");
    var say = function (t, good) { if (msg) { msg.textContent = t; msg.className = "sh-msg " + (good ? "sq-good" : "sq-bad"); } };
    e.preventDefault();
    var v = form(f), r;
    if (f.hasAttribute("data-search")) return go("/#/search?q=" + encodeURIComponent(v.q));
    if (f.hasAttribute("data-login")) {
      r = send("POST", "/api/login", { email: v.email, password: v.password });
      if (r.status === 200) { S.token = r.data.token; return go("/#/"); }
      return say(r.status === 500 ? "Server error (see the Network tab)." : (r.data && r.data.error) || "Login failed.");
    }
    if (f.hasAttribute("data-basket")) {
      var qty = parseInt(v.qty, 10);
      if (!(qty >= 1 && qty <= 20)) return say("Quantity must be between 1 and 20.");
      if (!S.token) return say("Log in first.");
      r = send("POST", "/api/basket", { productId: +f.getAttribute("data-basket"), qty: qty });
      return say(r.status === 200 ? "Added." : (r.data && r.data.error) || "Failed.", r.status === 200);
    }
    if (f.hasAttribute("data-review")) {
      r = send("POST", "/api/products/" + f.getAttribute("data-review") + "/reviews", { text: v.text });
      return go(S.path, true);
    }
    if (f.hasAttribute("data-coupon")) {
      r = send("POST", "/api/coupon", { code: v.code });
      if (r.status === 200) return go(S.path, true);
      return say((r.data && r.data.error) || "Failed.");
    }
    if (f.hasAttribute("data-avatar")) {
      r = send("POST", "/api/avatar", { filename: v.filename, content: v.content });
      if (r.status === 201) return go(S.path, true);
      return say((r.data && r.data.error) || "Failed.");
    }
    if (f.hasAttribute("data-feedback")) {
      if (!(+v.rating >= 1 && +v.rating <= 5)) return say("Pick a rating from 1 to 5.");
      r = send("POST", "/api/feedback", { rating: +v.rating, comment: v.comment });
      return say(r.status === 201 ? r.data.thanks : "Failed.", r.status === 201);
    }
    if (f.hasAttribute("data-forgot")) {
      var box = f.querySelector(".sh-q");
      if (!f.elements.answer) {
        r = send("GET", "/api/reset-question?email=" + encodeURIComponent(v.email));
        if (r.status !== 200) return say((r.data && r.data.error) || "Not found.");
        box.innerHTML = "<p><b>" + esc(r.data.question) + '</b></p><label>Answer <input name="answer" autocomplete="off"></label>' +
          '<label>New password <input name="newPassword" type="password"></label><button class="btn dark">Reset password</button>';
        return;
      }
      r = send("POST", "/api/reset", { email: v.email, answer: v.answer, newPassword: v.newPassword });
      return say(r.status === 200 ? r.data.message : (r.data && r.data.error) || "Failed.", r.status === 200);
    }
  }

  function onClick(e) {
    var a = e.target.closest("[data-go],[data-logout],[data-checkout]");
    if (!a) return;
    e.preventDefault();
    if (a.hasAttribute("data-go")) return go(a.getAttribute("data-go"));
    if (a.hasAttribute("data-logout")) { S.token = ""; return go("/#/"); }
    if (a.hasAttribute("data-checkout")) {
      var r = send("POST", "/api/checkout", {});
      var m = a.parentNode.querySelector(".sh-msg");
      if (r.status === 200) {
        el(header() + '<h2>Thank you!</h2><p>Order #' + r.data.order + " placed. Total ₹" + esc(r.data.total) + ".</p>" +
          (r.data.message ? '<p class="sq-good">' + esc(r.data.message) + "</p>" : ""));
      } else if (m) m.textContent = (r.data && r.data.error) || "Failed.";
    }
  }

  function headersText(hs) { return Object.keys(hs).map(function (k) { return k + ": " + hs[k]; }).join("\n"); }

  var SOURCE = [
    "const API = '/api';",
    "const routes = {",
    "  '/': Home, '/search': Search, '/product/:id': Product,",
    "  '/login': Login, '/forgot': ForgotPassword,",
    "  '/basket': Basket, '/orders': Orders, '/order/:id': Order,",
    "  '/profile': Profile, '/feedback': Feedback,",
    "  '/administration': AdminPanel,",
    "};",
    "",
    "function authHeader() { return { Authorization: 'Bearer ' + localStorage.token }; }",
    "const FOOTER = '<a href=\"/go?to=https://track.nimbu.shop/parcel\">Track my parcel</a>';",
    "",
    "export const api = {",
    "  login: (email, password) => post(API + '/login', { email, password }),",
    "  products: (q) => get(API + '/products?q=' + q),",
    "  product: (id) => get(API + '/products/' + id),",
    "  review: (id, text) => post(API + '/products/' + id + '/reviews', { text }),",
    "  basket: () => get(API + '/basket'),",
    "  addToBasket: (productId, qty) => post(API + '/basket', { productId, qty }),",
    "  checkout: () => post(API + '/checkout', {}),",
    "  orders: () => get(API + '/orders'),",
    "  order: (id) => get(API + '/orders/' + id),",
    "  feedback: (rating, comment) => post(API + '/feedback', { rating, comment }),",
    "  resetQuestion: (email) => get(API + '/reset-question?email=' + email),",
    "  reset: (email, answer, newPassword) => post(API + '/reset', { email, answer, newPassword }),",
    "  adminUsers: () => get(API + '/admin/users'),",
    "  coupon: (code) => post(API + '/coupon', { code }),",
    "  avatar: (filename, content) => post(API + '/avatar', { filename, content }),",
    "};",
    "",
    "function Basket() {",
    "  const qty = Number(form.qty.value);",
    "  if (qty < 1 || qty > 20) return showError('Quantity must be between 1 and 20.');",
    "  return api.addToBasket(product.id, qty);",
    "}",
    "",
    "function Feedback() {",
    "  if (rating < 1 || rating > 5) return showError('Pick a rating from 1 to 5.');",
    "  return api.feedback(rating, comment);",
    "}"
  ].join("\n");

  function dev() {
    var body = $("sh-devbody");
    document.querySelectorAll(".sh-tabs button").forEach(function (b) { b.className = b.getAttribute("data-tab") === S.tab ? "on" : ""; });
    if (S.tab === "net") {
      var pick = S.pick != null ? S.log[S.pick] : null;
      body.innerHTML = '<div class="sh-net"><div class="sh-reqs">' + (S.log.length ? S.log.map(function (x, i) {
        return '<button data-pick="' + i + '" class="' + (i === S.pick ? "on" : "") + (x.res.status >= 400 ? " err" : "") + '"><b>' + x.req.method + "</b> " +
          esc(x.req.path) + " <span>" + x.res.status + "</span></button>";
      }).join("") : '<p class="sx-empty">No requests yet.</p>') + '</div><div class="sh-detail">' + (pick ?
        '<div class="sh-btns"><button class="btn dark" data-resend>Edit and resend</button></div><h4>Request</h4><pre>' +
        esc(pick.req.method + " " + pick.req.path + "\n" + headersText(pick.req.headers) + (pick.req.body ? "\n\n" + pick.req.body : "")) +
        "</pre><h4>Response</h4><pre>" + esc(pick.res.status + "  " + pick.res.type + "\n\n" + pick.res.body) + "</pre>" :
        '<p class="sx-empty">Pick a request to see what was sent and what came back.</p>') + "</div></div>";
    } else if (S.tab === "repeat") {
      var r = S.rep || { method: "GET", path: "/api/products?q=", headers: S.token ? "Authorization: Bearer " + S.token : "", body: "" };
      body.innerHTML = '<div class="sh-rep"><div class="sh-line"><select id="rp-m">' + ["GET", "POST", "PUT", "DELETE"].map(function (m) {
        return "<option" + (m === r.method ? " selected" : "") + ">" + m + "</option>";
      }).join("") + '</select><input id="rp-p" value="' + esc(r.path) + '" spellcheck="false"><button class="btn dark" id="rp-send">Send</button></div>' +
        '<label>Headers (one per line)<textarea id="rp-h" rows="2" spellcheck="false">' + esc(r.headers) + "</textarea></label>" +
        '<label>Body (JSON)<textarea id="rp-b" rows="4" spellcheck="false">' + esc(r.body) + '</textarea></label><pre id="rp-out" class="sh-raw">' +
        esc(r.out || "Send a request to see the response.") + "</pre></div>";
      $("rp-send").addEventListener("click", function () {
        var hs = {};
        $("rp-h").value.split(/\n/).forEach(function (l) { var i = l.indexOf(":"); if (i > 0) hs[l.slice(0, i).trim()] = l.slice(i + 1).trim(); });
        var saved = S.token;
        S.token = "";
        var res = send($("rp-m").value, $("rp-p").value.trim(), $("rp-b").value.trim() ? $("rp-b").value : null, hs);
        S.token = saved;
        S.rep = { method: $("rp-m").value, path: $("rp-p").value, headers: $("rp-h").value, body: $("rp-b").value,
          out: res.raw.status + "  " + res.raw.type + "\n\n" + res.raw.body };
        $("rp-out").textContent = S.rep.out;
        if (res.status === 200 && res.data && res.data.token && /\/api\/login/.test($("rp-p").value)) S.token = res.data.token;
      });
    } else if (S.tab === "store") {
      var parts = String(S.token || "").split("."), hd = "", pl = "";
      try { hd = JSON.stringify(JSON.parse(unb64u(parts[0])), null, 1); pl = JSON.stringify(JSON.parse(unb64u(parts[1])), null, 1); } catch (e) {}
      body.innerHTML = '<div class="sh-rep"><p class="sx-note">localStorage for https://nimbu.shop</p><label>token<textarea id="st-t" rows="3" spellcheck="false">' +
        esc(S.token) + '</textarea></label><div class="sh-btns"><button class="btn" id="st-save">Save token</button></div>' +
        '<div class="sh-jwt"><label>Header (decoded)<textarea id="st-h" rows="4" spellcheck="false">' + esc(hd) + "</textarea></label>" +
        '<label>Payload (decoded)<textarea id="st-p" rows="4" spellcheck="false">' + esc(pl) + "</textarea></label>" +
        '<label>Signature<input id="st-s" value="' + esc(parts[2] || "") + '" spellcheck="false"></label></div>' +
        '<div class="sh-btns"><button class="btn dark" id="st-enc">Re-encode into the token</button><span class="sh-msg" id="st-msg"></span></div></div>';
      $("st-save").addEventListener("click", function () { S.token = $("st-t").value.trim(); $("st-msg").textContent = "Saved."; go(S.path, true); });
      $("st-enc").addEventListener("click", function () {
        try {
          var t = b64u(JSON.stringify(JSON.parse($("st-h").value))) + "." + b64u(JSON.stringify(JSON.parse($("st-p").value))) + "." + $("st-s").value.trim();
          $("st-t").value = t;
          $("st-msg").textContent = "Encoded. Press Save token to use it.";
        } catch (e) { $("st-msg").textContent = "That isn't valid JSON."; }
      });
    } else {
      body.innerHTML = '<p class="sx-note">main.3f9a1c.js, the storefront code your browser downloaded</p><pre class="sh-src">' + esc(SOURCE) + "</pre>";
    }
  }

  function onDev(e) {
    var t = e.target.closest("[data-tab],[data-pick],[data-resend]");
    if (!t) return;
    if (t.hasAttribute("data-tab")) S.tab = t.getAttribute("data-tab");
    if (t.hasAttribute("data-pick")) S.pick = +t.getAttribute("data-pick");
    if (t.hasAttribute("data-resend")) {
      var x = S.log[S.pick];
      S.rep = { method: x.req.method, path: x.req.path, body: x.req.body,
        headers: Object.keys(x.req.headers).filter(function (k) { return k !== "content-type"; }).map(function (k) {
          return (k === "authorization" ? "Authorization" : k) + ": " + x.req.headers[k];
        }).join("\n") };
      S.tab = "repeat";
    }
    dev();
  }

  function onMessage(e) {
    var up = document.querySelector(".sh-upframe");
    if (up && e.source === up.contentWindow && e.data && e.data.nimbuUpload) {
      K.award("shop-upload", "Not a picture");
      e = { data: { nimbuXss: 1, msg: e.data.msg } };
    } else {
      var frame = document.querySelector(".sh-reviews");
      if (!frame || e.source !== frame.contentWindow || !e.data || !e.data.nimbuXss) return;
      K.award("shop-xss", "Stored XSS");
    }
    var d = document.createElement("div");
    d.className = "sh-alert";
    d.innerHTML = "<div><p>nimbu.shop says</p><b></b><button class=\"btn dark\">OK</button></div>";
    d.querySelector("b").textContent = e.data.msg;
    d.querySelector("button").addEventListener("click", function () { d.remove(); });
    $("sh-page").appendChild(d);
  }

  function paint() { K.missions($("sh-missions"), MISSIONS); }

  function reset() {
    fresh();
    $("sh-devbody").innerHTML = "";
    go("/#/", true);
    dev();
  }

  function start() {
    if (!$("sh-app")) return;
    K = global.LabKit;
    esc = K.esc;
    paint();
    global.addEventListener("labkit-award", paint);
    if (!global.initSqlJs) { $("sh-page").textContent = "Couldn't load the shop's database engine. Check your connection and reload."; return; }
    global.initSqlJs({ locateFile: function (f) { return ROOT + "assets/vendor/sqljs-1.13.0/" + f; } }).then(function (lib) {
      SQL = lib;
      reset();
      $("sh-page").addEventListener("click", onClick);
      $("sh-page").addEventListener("submit", onSubmit);
      document.querySelector(".sh-dev").addEventListener("click", onDev);
      global.addEventListener("message", onMessage);
      $("sh-goto").addEventListener("click", function () { go($("sh-url").value); });
      $("sh-url").addEventListener("keydown", function (e) { if (e.key === "Enter") go($("sh-url").value); });
      $("sh-reload").addEventListener("click", function () { go(S.path, true); });
      $("sh-back").addEventListener("click", function () { if (S.history.length) go(S.history.pop(), true); });
      $("sh-wipe").addEventListener("click", reset);
    }, function (e) { $("sh-page").textContent = "Couldn't start the shop: " + e.message; });
  }
  if (document.readyState === "complete") start();
  else global.addEventListener("load", start);
})(window);
