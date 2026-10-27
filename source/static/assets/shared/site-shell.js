/* Site Shell Behavior */

function toggleSidebar() {
  const sb = document.querySelector(".site-sidebar");
  if (!sb) return;
  if (window.innerWidth <= 900) {
    sb.classList.toggle("open");
  } else {
    sb.classList.toggle("collapsed");
  }
}

(function () {
  var thisScript = document.currentScript;
  if (!thisScript) return;
  var src = thisScript.getAttribute("src") || "";
  var base = src.replace(/assets\/site-shared\/site-shell\.js.*$/, "");
  var nav = document.querySelector(".site-nav");
  if (!nav || nav.querySelector(".nav-grades-link")) return;
  var isInstructor = /\/instructor\//.test(location.pathname);
  var link = document.createElement("a");
  link.className = "nav-grades-link";
  link.href = base + "assets/reports/" + (isInstructor ? "class-report.html" : "student-report.html");
  link.textContent = isInstructor ? "Class Performance" : "My Grades";
  nav.appendChild(link);
})();
