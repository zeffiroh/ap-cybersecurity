/* Site settings. A blank value hides whatever it controls. */

window.APCYBER_CONFIG = {
  neon: {
    authUrl: "https://ep-mute-sound-b6w4s5va.neonauth.c-2.sa-east-1.aws.neon.tech/neondb/auth",
    dataApiUrl: "https://ep-mute-sound-b6w4s5va.apirest.c-2.sa-east-1.aws.neon.tech/neondb/rest/v1"
  }
};

window.APCYBER_SUPPORT = {
  buttonId: "",          // Razorpay payment button id, e.g. "pl_ABC123XYZ456"
  pageUrl: "https://zeffiroh.github.io/get-me-a-coffee/",   // or a hosted payment page URL
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
