/* Site settings. A blank value hides whatever it controls. */

window.APCYBER_CONFIG = {
  neon: {
    authUrl: "https://ep-mute-sound-b6w4s5va.neonauth.c-2.sa-east-1.aws.neon.tech/neondb/auth",
    dataApiUrl: "https://ep-mute-sound-b6w4s5va.apirest.c-2.sa-east-1.aws.neon.tech/neondb/rest/v1"
  }
};

/* The paywall. Access belongs to the signed-in account (the gradebook email) and, once unlocked, lasts
   for good. Ways in, all on unlock/: a Razorpay payment from the course's payment page (checked with
   Razorpay by db/sync_razorpay.py, which unlocks the email typed on that page), a code (made in the
   database, see db/README.md), or "Continue without paying" while there is no minimum. Every page
   outside `free` shows an unlock block until then. Paths are from the site root; * is one folder or
   file name, ** is anything below. */
window.APCYBER_PAYWALL = {
  enabled: true,

  // unlock/ opens  payUrl?return=<address>; the payment page sends the payer to that address
  // (…/unlock/?paid=1), which waits until the payment shows up as confirmed. "pay/" is the built-in page.
  payUrl: "pay/",

  pay: {
    // Each method is a store link. Only Razorpay payments are checked and unlock by themselves.
    // Blank ones are hidden; with none filled in, the payment page says "Free for now".
    methods: [
      { label: "Razorpay", note: "UPI, cards, netbanking, wallets · India", url: "https://rzp.io/rzp/unlock-aap-cybersecurity" },
      { label: "Gumroad", note: "Cards, PayPal · international", url: "" },
      { label: "PayPal", note: "International", url: "" }
    ]
  },

  donateEveryDays: 30,   // unlocked accounts see a donate banner at most this often; 0 turns it off

  free: [
    "index.html", "unit-*/index.html", "unit-*/*/index.html",   // home, unit and topic overviews
    "unit-1/1.1/**",                                            // the whole first topic
    "glossary.html", "calendar.html", "support.html",
    "buy/**", "unlock/**", "pay/**", "ledger/**", "teacher/database-check.html"
  ]
};

window.APCYBER_SUPPORT = {
  buttonId: "",          // Razorpay payment button id, e.g. "pl_ABC123XYZ456"
  pageUrl: "https://zeffiroh.github.io/ap-cybersecurity/pay/?donate=1",   // the Contribute button
  contactEmail: "mukumahnoor@gmail.com",                     // sponsorship enquiries

  rates: {               // rate card text, e.g. "Rs 6,000 / semester"
    course: "",
    "unit-1": "",
    "unit-2": "",
    "unit-3": "",
    "unit-4": "",
    "unit-5": ""
  },

  courseSponsor: { name: "", blurb: "", url: "" },

  unitSponsors: {        // null, or { name, title, blurb, url }
    "unit-1": null,
    "unit-2": null,
    "unit-3": null,
    "unit-4": null,
    "unit-5": null
  }
};
