/* Magic Mirror Config Sample
 *
 * By Michael Teeuw http://michaelteeuw.nl
 * MIT Licensed.
 *
 * For more information how you can configurate this file
 * See https://github.com/MichMich/MagicMirror#configuration
 *
 */

var config = {
	address: "0.0.0.0", // Address to listen on, can be:
	                      // - "localhost", "127.0.0.1", "::1" to listen on loopback interface
	                      // - another specific IPv4/6 to listen on a specific interface
	                      // - "", "0.0.0.0", "::" to listen on any interface
	                      // Default, when address config is left out, is "localhost"
	port: 8080,
	//ipWhitelist: ["127.0.0.1", "::ffff:127.0.0.1", "::1", "::ffff:172.17.0.1","192.168.178.21", "::ffff:192.168.178.21", "::21", "::ffff:192.168.178.21"],
	ipWhitelist: [],
	// Set [] to allow all IP addresses
	                                                       // or add a specific IPv4 of 192.168.1.5 :
	                                                       // ["127.0.0.1", "::ffff:127.0.0.1", "::1", "::ffff:192.168.1.5"],
	                                                       // or IPv4 range of 192.168.3.0 --> 192.168.3.15 use CIDR format :
	                                                       // ["127.0.0.1", "::ffff:127.0.0.1", "::1", "::ffff:192.168.3.0/28"],

	language: "en",
	timeFormat: 24,
	units: "metric",
	modules: [
//		{
//			module: "alert",
//		},
//		{
//			module: "updatenotification",
//			position: "top_bar"
//		},
		{
			module: "clock",
			position: "top_left"
		},
		{
			module: "calendar",
			header: "Kalender",
			position: "top_left",
			config: {
				maximumEntries: 10,
				// displaySymbol: false,
				maxTitleLength: 25,
				fetchInterval: 900000, // 15min
				animationSpeed: 0,
				fade: false,
				dateFormat: "DD.MM",
				fullDayEventDateFormat: "DD.MM",
				timeFormat: "absolute",
				urgency: 26,
				wrapEvents: true,
				displayRepeatingCountTitle: true,
				calendars: [
					{
						symbol: "calendar-check-o ",
						url: "webcal://www.calendarlabs.com/ical-calendar/ics/46/Germany_Holidays.ics"
					}
				]
			}
		},
		// {
		// 	module: "currentweather",
		// 	position: "top_right",
		// 	config: {
		// 		location: "New York",
		// 		locationID: "",  //ID from http://bulk.openweathermap.org/sample/; unzip the gz file and find your city
		// 		appid: "YOUR_OPENWEATHER_API_KEY"
		// 	}
		// },
		{
			module: "weatherforecast",
			position: "top_left",
			header: "Weather Forecast",
			config: {
				location: "Leipzig",
				locationID: "",  //ID from http://www.openweathermap.org/help/city_list.txt
				appid: "",
        roundTemp: true,
        animationSpeed: 0,
        fade: false,
        showRainAmount: true,
			}
		},
    {
      module: "MMM-CoinMarketCap",
      position: "top_right",
      config: {
        currencies: ["ethereum", "enjin-coin", "garlicoin"],
        columns: [ "logo", "price", "changes", "graph" ],
        // columns: [ "logo", "priceWithChanges", "graph" ],
        showColumnHeaders: false,
        conversion: "EUR",
        showRowSeparator: false,
        fontSize: "medium",
        logoSize: "medium",
        graphRange: 30,
        graphSize: "small",
      },
    },
    {
      module: "MMM-Reddit",
      position: "top_right",
      config: {
        subreddit: ["raspberry_pi", "MechanicalKeyboards", "CryptoCurrency"],
        showHeader: false,
        headerType: "sentence",
        displayType: "headlines",
        count: 4,
        show: 4,
        width: 360,
        showRank: false,
        showScore: false,
        showSubreddit: true,
        showNumComments: false,
        colorText: false,
        showThumbnail: false,
      },
    },
	]

};

/*************** DO NOT EDIT THE LINE BELOW ***************/
if (typeof module !== "undefined") {module.exports = config;}
