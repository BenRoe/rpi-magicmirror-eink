var config = {
  "magicmirror_port": 8080, // magic mirror port
  "display_width": 400, // eink display height in px
  "display_height": 300, // eink display width in px
  "display_type": "epd4in2b", // which eink display, currently supported: epd4in2b, epd7in5
  "display_invert": true,
  "wait_to_load": 18, // wait seconds to load the site and display all data
  "refresh_interval": "0 */1 * * * *", // update eink every 10 minutes
  // https://github.com/kelektiv/node-cron#cron-ranges
  "timezone": "Europe / Berlin" // https://www.inmotionhosting.com/support/website/general-server-setup/tz-ref-table
};

/*************** DO NOT EDIT THE LINE BELOW ***************/
if (typeof module !== "undefined") {module.exports = config;}
