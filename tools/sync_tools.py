import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from builder import toolsteps as T

STUDIO = ROOT / "tools" / "studio" / "ui" / "index.html"


def main():
    html = STUDIO.read_text(encoding="utf-8")
    tags = "".join(f'<script src="/site/assets/theme/{f}"></script>\n' for f in T.TOOL_FILES)
    new, n = re.subn(r'(<script src="/site/assets/theme/tools\.js"></script>\n)(?:<script src="/site/assets/theme/tool-[a-z0-9-]+\.js"></script>\n)*', lambda m: m.group(1) + tags, html)
    if n != 1:
        sys.exit("The studio page doesn't load tools.js where I expected.")
    if new != html:
        STUDIO.write_text(new, encoding="utf-8", newline="\n")
        print(f"The studio now loads {len(T.TOOL_FILES)} tools.")
    else:
        print("The studio already loads every tool.")


if __name__ == "__main__":
    main()
