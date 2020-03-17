const debug = require('debug')('puppeteer');
const debugChildP = debug.extend('cpPython');
const path = require('path');
const spawn = require('child_process').spawn;
const CronJob = require('cron').CronJob;
const puppeteer = require('puppeteer-core');
const Jimp = require('jimp');

// config variables
const config = require('./config.js');
// as a best practice
// all global variables should be referenced via global. syntax
// and their names should always begin with g
global.gConfig = config;

const fileName = 'screenshot.png';
let d = new Date();

const job = new CronJob({

  cronTime: global.gConfig.refresh_interval,
  timezone: global.gConfig.timezone,
  onTick: function() {
    let d = new Date();

    debug('Display refresh START at', d);

    (async () => {

      // open puppeteer
      const browser = await puppeteer.launch({
        args: ['--no-sandbox', '--disable-setuid-sandbox', '--headless', '--disable-gpu'],
        executablePath: '/usr/bin/chromium-browser'
      })

      // create a new virtual window/page in puppeteer
      const page = await browser.newPage();

      // set the virtual browser width and size
      // should be the same as the eink display
      await page.setViewport({
        width: global.gConfig.display_width,
        height: global.gConfig.display_height
      });

      // open the MagicMirror site with puppeteer
      await page.goto(`http://localhost:${global.gConfig.magicmirror_port}`);

      // wait x seconds to load the complete content of the MagicMirror site
      // change it in config.js "wait_to_load"
      await page.waitFor(global.gConfig.wait_to_load*1000);

      await page.screenshot({path: fileName});

      await browser.close();
      
      // invert colors for the screenshot
      if (global.gConfig.invert_color) {
        // read the screenshot
        const img = await Jimp.read(fileName);
        
        // invert the image
        await img.invert();
          
        //save image
        await img.quality(80).writeAsync(fileName);
      }

      // run the python script to display the screenshots on the eink display
      const childPython = spawn('python', ['./ePaperPython/main.py']);

      childPython.stdout.on('data', (data) => {
        debugChildP(data.toString());
      });

      childPython.stderr.on('data', (err) => {
        debugChildP(err.toString());
      });

      // if python script was finished
      childPython.on('close', (code) => {
        debugChildP(`child process (Python ePaperPython) exited with code ${code} (0=success).`);
        const date = new Date();
        if(code===0) debug('Display refresh END at', date);
      });

    })();

  },
  onComplete: function () {
    const date = new Date();
    debug('puppeteer STOPPED at ', d);
  },
  start: true,
  runOnInit: true,
});

debug('Script START at', d);


