const puppeteer = require('puppeteer');
const PuppeteerHar = require('puppeteer-har');

(async () => {
  // const browser = await puppeteer.launch(); //headless mode
  // const browser = await puppeteer.launch({ headless: false });
  const browser = await puppeteer.launch({
    headless: true,
    args: [ // Disable Chromium's unnecessary SUID sandbox.
        '--no-sandbox',
        '--disable-setuid-sandbox',
        // '--unhandled-rejections=strict'
    ]
  });


  const context = await browser.createIncognitoBrowserContext();
  const page = await context.newPage();
//   const page = await browser.newPage();
  await page.setUserAgent(
      'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.82 Safari/537.36'
  )
  const client = await page.target().createCDPSession();
  await client.send('Network.setCacheDisabled', {
  cacheDisabled: true,
  });
  const har = new PuppeteerHar(page);
  await har.start({ path: 'output/' + process.env.timestamp + '/' + process.env.website + '_' + process.env.iteration_loop +'.har' });
  // for (var loop = 0; loop < 10;loop++){

  await page.setDefaultNavigationTimeout(15000);
  await page.goto('https://' + process.env.website);
  await page.screenshot({path: 'output/' + process.env.timestamp + '/' + process.env.website + '_' + process.env.iteration_loop +'.png'});

  await new Promise(r => setTimeout(r, 5000));
  // }
  await page.goto('https://' + process.env.website);
  await new Promise(r => setTimeout(r, 5000));
  
//   await page.goto('https://http3check.net');

//   await new Promise(r => setTimeout(r, 5000));
//   await page.goto('https://http3check.net');

//   await new Promise(r => setTimeout(r, 5000));
//   await page.goto('https://http3check.net');

//   await new Promise(r => setTimeout(r, 5000));

  await har.stop();
  await browser.close();


})();