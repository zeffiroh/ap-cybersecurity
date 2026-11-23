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
RUN echo "deb http://deb.debian.org/debian bookworm-backports main" > /etc/apt/sources.list.d/backports.list \
 && apt-get update && apt-get install -y --no-install-recommends libglib2.0-bin graphviz bsdextrautils \
 && apt-get install -y --no-install-recommends -t bookworm-backports suricata && rm -rf /var/lib/apt/lists/* \
 && curl -fsSL -o /tmp/gl.tgz https://github.com/gitleaks/gitleaks/releases/download/v8.21.2/gitleaks_8.21.2_linux_x64.tar.gz \
 && tar -xzf /tmp/gl.tgz -C /usr/local/bin gitleaks && rm /tmp/gl.tgz \
 && curl -fsSL -o /tmp/trivy.tgz https://github.com/aquasecurity/trivy/releases/download/v0.76.2/trivy_0.76.2_Linux-64bit.tar.gz \
 && tar -xzf /tmp/trivy.tgz -C /usr/local/bin trivy && rm /tmp/trivy.tgz \
 && /opt/tools/bin/pip install --no-cache-dir pytm cvss cryptography
USER analyst
WORKDIR /home/analyst
RUN printf 'title: Warm the cache\nlogsource:\n  product: windows\n  service: security\ndetection:\n  selection:\n    EventID: 4688\n  condition: selection\ntags:\n  - attack.t1204.002\n  - d3fend.d3-pa\n' > /tmp/warm.yml \
 && (sigma check /tmp/warm.yml >/dev/null 2>&1 || true) && rm /tmp/warm.yml && ls ~/.cache/pysigma \
 && mkdir -p /tmp/w && printf 'FROM debian\n' > /tmp/w/Dockerfile && (trivy config --quiet /tmp/w >/dev/null 2>&1 || true) && rm -rf /tmp/w && ls ~/.cache/trivy
USER root
COPY desktop.sh /usr/local/bin/desktop.sh
COPY director.py /usr/local/bin/director.py
RUN chmod +x /usr/local/bin/desktop.sh
USER analyst
