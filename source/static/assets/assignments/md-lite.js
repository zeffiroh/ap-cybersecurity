/* minimal, dependency-free Markdown renderer for coding */
(function (global) {
  "use strict";

  function esc(s) {
    return s.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
  }

  function inline(s) {
    s = esc(s);
    s = s.replace(/`([^`]+)`/g, "<code>$1</code>");
    s = s.replace(/\*\*([^*]+)\*\*/g, "<strong>$1</strong>");
    return s;
  }

  function render(md) {
    var lines = (md || "").replace(/\r\n/g, "\n").split("\n");
    var out = [];
    var i = 0;
    var listBuf = null; // {tag, items: []}

    function flushList() {
      if (!listBuf) return;
      out.push("<" + listBuf.tag + ">" + listBuf.items.map(function (it) {
        return "<li>" + inline(it) + "</li>";
      }).join("") + "</" + listBuf.tag + ">");
      listBuf = null;
    }

    while (i < lines.length) {
      var line = lines[i];

      // fenced code block
      var fence = line.match(/^```(\w*)\s*$/);
      if (fence) {
        flushList();
        var codeLines = [];
        i++;
        while (i < lines.length && !/^```\s*$/.test(lines[i])) {
          codeLines.push(lines[i]);
          i++;
        }
        i++; // skip closing fence
        out.push('<pre class="pg-md-code"><code>' + esc(codeLines.join("\n")) + "</code></pre>");
        continue;
      }

      // headers
      var h = line.match(/^(#{1,4})\s+(.*)$/);
      if (h) {
        flushList();
        // shifted so prompt headers never land on h1/h2/h3 (those are page/panel
        // chrome): single # -> h4, ## -> h5, ###+ -> h6.
        var level = Math.min(h[1].length + 3, 6);
        out.push("<h" + level + ">" + inline(h[2]) + "</h" + level + ">");
        i++;
        continue;
      }

      // bullet list
      var bullet = line.match(/^\s*-\s+(.*)$/);
      if (bullet) {
        if (!listBuf || listBuf.tag !== "ul") { flushList(); listBuf = { tag: "ul", items: [] }; }
        listBuf.items.push(bullet[1]);
        i++;
        continue;
      }

      // numbered list
      var numbered = line.match(/^\s*\d+\.\s+(.*)$/);
      if (numbered) {
        if (!listBuf || listBuf.tag !== "ol") { flushList(); listBuf = { tag: "ol", items: [] }; }
        listBuf.items.push(numbered[1]);
        i++;
        continue;
      }

      flushList();

      // blank line
      if (/^\s*$/.test(line)) { i++; continue; }

      // paragraph: collect until blank line / next block marker
      var para = [line];
      i++;
      while (i < lines.length && !/^\s*$/.test(lines[i]) &&
             !/^```/.test(lines[i]) && !/^#{1,4}\s/.test(lines[i]) &&
             !/^\s*-\s+/.test(lines[i]) && !/^\s*\d+\.\s+/.test(lines[i])) {
        para.push(lines[i]);
        i++;
      }
      out.push("<p>" + inline(para.join(" ")) + "</p>");
    }
    flushList();
    return out.join("\n");
  }

  global.MDLite = { render: render };
})(window);
