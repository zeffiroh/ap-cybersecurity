window.APCYBER_CONFIG = {
  neon: {
    authUrl: "https://ep-mute-sound-b6w4s5va.neonauth.c-2.sa-east-1.aws.neon.tech/neondb/auth",
    dataApiUrl: "https://ep-mute-sound-b6w4s5va.apirest.c-2.sa-east-1.aws.neon.tech/neondb/rest/v1"
  }
};

window.APCYBER_PAYWALL = {
  enabled: true,

  payUrl: "pay/",

  pay: {
    methods: [
      { label: "Razorpay", note: "UPI, cards, netbanking, wallets · India", url: "https://rzp.io/rzp/unlock-aap-cybersecurity" },
      { label: "Gumroad", note: "Cards, PayPal · international", url: "https://mitaliaayatmahnoor.gumroad.com/l/cybersecurity-kickstarter" },
      { label: "PayPal", note: "International", url: "" }
    ]
  },

  donateEveryDays: 30,

  free: [
    "index.html", "unit-*/index.html", "unit-*/*/index.html",
    "unit-1/1.1/**",
    "glossary.html", "calendar.html", "support.html", "classes.html", "videos.html", "notebook.html", "community.html",
    "store.html", "labs.html", "seminars.html", "certificate.html",
    "buy/**", "unlock/**", "pay/**", "ledger/**", "teacher/database-check.html"
  ],

  products: {
    labs: {
      name: "Labs",
      title: "Part of Labs",
      text: "Labs is the hands-on side of the course: incident runbooks with an analyst console, a real Linux computer, JupyterLab " +
        "with every code book, the SQL injection lab, the hackable shop, the capture-the-flag board, every skill lab, premium notebooks and the lesson videos. " +
        "It is sold separately from the course.",
      button: "Get Labs",
      buy: "store.html#labs",
      preview: "labs.html",
      previewLabel: "What's inside",
      paths: ["linux.html", "lab/**", "sqli.html", "shop.html", "ctf.html", "cyberchef/**", "unit-*/*/*/lab.html"]
    }
  }
};

window.APCYBER_STORES = {
  bundle: {
    name: "Course + Labs",
    blurb: "Everything in the Course and everything in Labs together, for less than buying them one by one.",
    india: "Pay what you want, with a minimum",
    badge: "Best value",
    methods: [
      { label: "Razorpay", note: "India", url: "" },
      { label: "Gumroad", note: "International", url: "" }
    ]
  },
  course: {
    name: "Course",
    blurb: "Every lesson, quiz, slide deck, unit test, the capstone, progress tracking and your report card.",
    india: "Pay what you want",
    methods: [
      { label: "Razorpay", note: "India · UPI, cards, netbanking", url: "https://rzp.io/rzp/unlock-aap-cybersecurity" },
      { label: "Gumroad", note: "International · cards, PayPal", url: "https://mitaliaayatmahnoor.gumroad.com/l/cybersecurity-kickstarter" }
    ]
  },
  labs: {
    name: "Labs",
    blurb: "Incident runbooks with an analyst console (terminal, script toolkit, log viewer, notes), real Linux in the browser, JupyterLab with every code book, the SQL injection lab, Hack the shop, the CTF board, " +
      "every skill lab, premium notebooks and every lesson video. Pay once, keep it.",
    india: "Pay what you want, with a minimum",
    methods: [
      { label: "Razorpay", note: "India · pay what you want", url: "" },
      { label: "Gumroad", note: "International · $149", url: "" }
    ]
  },
  seminars: {
    name: "Seminars subscription",
    blurb: "Every recorded seminar and its hands-on lab, including new ones, for a year. Or unlock single seminars with tickets.",
    india: "Pay what you want, with a minimum",
    methods: [
      { label: "Razorpay", note: "India", url: "" },
      { label: "Gumroad", note: "International", url: "" }
    ]
  },
  tickets: {
    name: "Tickets",
    blurb: "Buy any number. A batch class costs 1 ticket; a 1:1 class or a seminar costs what its page says.",
    india: "Priced per ticket, cheaper in packs",
    packs: [
      { tickets: 5, inr: "", usd: "" },
      { tickets: 10, inr: "", usd: "" },
      { tickets: 25, inr: "", usd: "" }
    ],
    methods: [
      { label: "Razorpay", note: "India · type how many you want", url: "" },
      { label: "Gumroad", note: "International · choose a quantity", url: "" }
    ]
  },
  book: {
    name: "Textbook",
    blurb: "The full textbook as PDF (and EPUB on Gumroad).",
    page: "buy/"
  }
};

window.APCYBER_SUPPORT = {
  buttonId: "",
  pageUrl: "https://zeffiroh.github.io/ap-cybersecurity/pay/?donate=1",
  contactEmail: "mukumahnoor@gmail.com",

  rates: {
    course: "",
    "unit-1": "",
    "unit-2": "",
    "unit-3": "",
    "unit-4": "",
    "unit-5": ""
  },

  courseSponsor: { name: "", blurb: "", url: "" },

  unitSponsors: {
    "unit-1": null,
    "unit-2": null,
    "unit-3": null,
    "unit-4": null,
    "unit-5": null
  }
};
