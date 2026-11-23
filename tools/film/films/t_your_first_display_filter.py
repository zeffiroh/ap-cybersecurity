from kit import after, build, chapter, clear, close, cmd, files_window, say, term, wait

scenes = [
 chapter("Opening"),
 files_window(),
 say("Hello, and welcome. Logs tell you what a computer says happened. Packets show what actually crossed the wire. Today you'll open a packet capture and use display filters to find a script being downloaded onto a server."),
 {"point": [0.45, 0.3], "in": "files", "secs": 1.0},
 say("The setting. Tamarind Health, the night of the fifth to the sixth of November 2026, all times in UTC. The capture, capture.pcap, comes from the core switch's mirror port, starting at 01:15. A mirror port copies every packet that passes through the switch, so this is the clinic network's own recording of that night."),
 close("files"),
 term,

 chapter("1. Packets: the download"),
 say("In the packet viewer, a display filter keeps only the packets you ask for and hides the rest. Wireshark is the free, open-source packet viewer. The first filter is http.request, which shows only web requests. That's the quickest way to see what was downloaded over plain HTTP."),
 {"open": ["env", "QT_SCALE_FACTOR=1.35", "wireshark", "-r", "capture.pcap", "-Y", "http.request"], "window": "capture.pcap|Wireshark", "as": "ws", "geometry": [40, 40, 1840, 1000], "timeout": 60, "settle": 3},
 wait(3),
 {"point": [0.3, 0.12], "in": "ws", "secs": 1.0, "wait": 2},
 after("Two requests. Read each row: the source address, the host name and the path. Both went to cdn.patch-relay.example, a name made to look like a software update service. The first fetched m.sh, a shell script. The second fetched a.bin, a program. Click a request and read its User-Agent header, the name the downloading program gives itself."),
 {"point": [0.3, 0.16], "in": "ws", "secs": 0.8, "click": True, "wait": 4},
 after("The first says Wget. That matches the sudo line in the server's log, where the attacker ran wget. The second says curl slash 7.81.0, which matches a line inside the script. So the attacker downloaded the script by hand, and the script then downloaded the program. The second filter widens the view: ip dot addr equals 203.0.113.77, every packet to or from the download server."),
 {"use": "ws", "at": [0.5, 0.5], "keys": ["ctrl+slash", "ctrl+a"]},
 {"use": "ws", "at": [0.5, 0.5], "type": "ip.addr == 203.0.113.77", "cps": 14, "wait": 4},
 close("ws"),
 say("Finally, the command line. tshark is the command-line version of the packet viewer, and it prints one line per request."),
 cmd("tshark -r capture.pcap -Y 'http.request' -T fields -e ip.src -e http.host -e http.request.uri -e http.user_agent", 3.5),
 after("Same answer from a different tool: cdn.patch-relay.example, and a second request from curl."),
 clear,

 chapter("Where next"),
 say("That was one step from Seminar 1, Reading evidence: packets, Linux, Windows and network sensors. The full seminar has a longer video, every step at three levels, a graded hand-in that I mark myself, and a certificate at the end. The links are on your screen."),
 chapter("Wrap-up"),
 say("To recap. A capture is the network's own recording. Filter with http.request to see downloads, read the User-Agent to see which program asked, and widen with ip.addr to see the whole conversation. Thank you for watching."),
 wait(2),
]

build("t-your-first-display-filter", scenes, host="tamarind-soc", pcap=["capture.pcap"])
