FROM debian:bookworm-slim

ENV DEBIAN_FRONTEND=noninteractive LANG=C.UTF-8 TZ=UTC

RUN echo "wireshark-common wireshark-common/install-setuid boolean false" | debconf-set-selections \
 && apt-get update && apt-get install -y --no-install-recommends \
    xvfb xfwm4 xfce4-panel xfdesktop4 xfce4-terminal xfce4-settings xfconf thunar mousepad \
    dbus-x11 x11-xserver-utils xdotool wmctrl adwaita-icon-theme gnome-icon-theme fonts-dejavu fonts-noto-core \
    ffmpeg wireshark tshark yara sqlite3 jq lnav less file xxd curl ca-certificates git \
    python3 python3-venv python3-pip firefox-esr nmap \
 && rm -rf /var/lib/apt/lists/*

RUN python3 -m venv /opt/tools \
 && /opt/tools/bin/pip install --no-cache-dir sigma-cli pysigma-backend-sqlite duckdb scapy orjson xxhash jinja2 tqdm colorama evtx ujson \
 && git clone --depth 1 https://github.com/wagga40/Zircolite.git /opt/zircolite \
 && rm -rf /opt/zircolite/.git

RUN /opt/tools/bin/pip install --no-cache-dir /opt/zircolite \
 && curl -fsSL -o /tmp/duckdb.zip https://github.com/duckdb/duckdb/releases/download/v1.1.3/duckdb_cli-linux-amd64.zip \
 && python3 -c "import zipfile; zipfile.ZipFile('/tmp/duckdb.zip').extract('duckdb', '/usr/local/bin')" \
 && chmod +x /usr/local/bin/duckdb && rm /tmp/duckdb.zip

COPY policies.json /usr/lib/firefox-esr/distribution/policies.json

RUN useradd -m -s /bin/bash analyst \
 && mkdir -p /case /out \
 && chown analyst:analyst /case /out

ENV PATH=/opt/tools/bin:$PATH
COPY desktop.sh /usr/local/bin/desktop.sh
COPY director.py /usr/local/bin/director.py
RUN chmod +x /usr/local/bin/desktop.sh
USER analyst
WORKDIR /home/analyst
