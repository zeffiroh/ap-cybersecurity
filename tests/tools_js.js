const fs = require("fs");
const path = require("path");
const vm = require("vm");

const ROOT = path.resolve(__dirname, "..");
const THEME = path.join(ROOT, "source", "static", "assets", "theme");

function load(names) {
  const tools = {};
  const sandbox = { window: {}, console, URL, TextEncoder, unescape, encodeURIComponent, escape, decodeURIComponent };
  sandbox.window = sandbox;
  vm.createContext(sandbox);
  vm.runInContext(fs.readFileSync(path.join(THEME, "tools.js"), "utf8"), sandbox);
  names.forEach((n) => vm.runInContext(fs.readFileSync(path.join(THEME, n), "utf8"), sandbox));
  sandbox.AayatTools.list().forEach((d) => { tools[d.id] = d; });
  return { tools, sandbox };
}

const cmd = process.argv[2];
const { tools } = load(["tool-packets.js", "tool-events.js"]);

if (cmd === "packets") {
  const jobs = JSON.parse(fs.readFileSync(0, "utf8"));
  const out = jobs.map(([file, filter]) => {
    const cap = tools.packets.parse(fs.readFileSync(file, "utf8"));
    try { return cap.rows.filter(tools.packets.compile(filter)).length; } catch (e) { return "ERR " + e.message; }
  });
  process.stdout.write(JSON.stringify(out));
} else if (cmd === "events") {
  const jobs = JSON.parse(fs.readFileSync(0, "utf8"));
  const out = jobs.map(([file, q]) => {
    const log = tools.events.parse(fs.readFileSync(file, "utf8"));
    try { return log.events.filter(tools.events.compile(q)).length; } catch (e) { return "ERR " + e.message; }
  });
  process.stdout.write(JSON.stringify(out));
} else {
  process.stdout.write(JSON.stringify(Object.keys(tools).sort()));
}
