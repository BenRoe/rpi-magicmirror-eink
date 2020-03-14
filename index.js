const debug = require('debug')('puppeteer');
const debugChildP = debug.extend('cpPython');
const path = require('path');
const spawn = require('child_process').spawn;
const CronJob = require('cron').CronJob;
const puppeteer = require('puppeteer-core');

// config variables
const config = require('./config.js');
// as a best practice
// all global variables should be referenced via global. syntax
// and their names should always begin with g
global.gConfig = config;

let d = new Date();
const job = new CronJob({
  cronTime: global.gConfig.refresh_interval,
  timezone: global.gConfig.timezone,
  onTick: function() {
    let d = new Date();
    debug('Display refresh START at', d);
    (async () => {

      const browser = await puppeteer.launch({
        args: ['--no-sandbox', '--disable-setuid-sandbox', '--headless', '--disable-gpu'],
        executablePath: '/usr/bin/chromium-browser'
      })
      const page = await browser.newPage();
      await page.setViewport({
        width: global.gConfig.display_width,
        height: global.gConfig.display_height
      });
      await page.goto(`http://localhost:${global.gConfig.magicmirror_port}/showfloorplan/`);
      await page.waitFor(global.gConfig.wait_to_load*1000);
      await page.screenshot({path: 'black.png'});

      await browser.close();

      const childPython = spawn('python', ['./ePaperPython/main.py']);

      childPython.stdout.on('data', (data) => {
        debugChildP(data.toString());
      });

      childPython.stderr.on('data', (err) => {
        debugChildP(err.toString());
      });

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
});

debug('Script START at', d);
job.start();


