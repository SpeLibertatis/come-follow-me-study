const { test, expect } = require('@playwright/test');

test('small-screen collection, ready studies and print routes', async ({ page }) => {
  await page.goto('/');
  await expect(page.getByRole('heading', { level: 1 })).toBeVisible();
  const width = await page.evaluate(() => document.documentElement.clientWidth);
  expect(width, 'mobile viewport (CSS pixels)').toBeLessThanOrEqual(430);
  const checkReflow = () => expect.poll(() => page.evaluate(() => (
    document.documentElement.scrollWidth <= document.documentElement.clientWidth
  ))).toBe(true);
  await checkReflow();
  await page.getByRole('link', {name: /2026 Old Testament/}).tap();
  await expect(page).toHaveURL(/2026\.html$/);
  await checkReflow();
  const cards = page.locator('.lesson-list li').filter({ hasText: 'Ready to study' });
  const paths = await cards.locator('h2 a').evaluateAll(links => links.map(a => a.href));
  expect(paths.length).toBeGreaterThan(0);
  for (const url of paths) {
    await test.step(new URL(url).pathname, async () => {
      await page.goto(url);
      await expect(page.getByRole('heading', { level: 1 })).toBeVisible();
      await checkReflow();

      const downloads = await page.locator('main a[href$=".pdf"]').evaluateAll(links => links.map(a => a.href));
      expect(downloads.length).toBeGreaterThan(0);
      for (const file of new Set(downloads)) {
        const response = await page.request.get(file);
        expect(response.ok(), file).toBeTruthy();
        expect((await response.body()).subarray(0, 4).toString(), file).toBe('%PDF');
      }
    });
  }
});

test('current narrative quick path and native disclosure work by touch', async ({ page }) => {
  await page.goto('/lessons/amos-obadiah-jonah.html');
  const quick = page.getByRole('link').and(page.locator('.hero-actions a[href="#quick"]'));
  await expect(quick).toHaveAccessibleName(/quick/i);
  await quick.tap();
  await expect(page).toHaveURL(/#quick$/);
  const disclosure = page.locator('#quick details').first();
  await disclosure.locator('summary').tap();
  await expect(disclosure).toHaveJSProperty('open', true);
  const print = page.getByRole('link').and(page.locator('main nav a[href="#downloads"]'));
  await expect(print).toHaveAccessibleName(/print/i);
  await print.tap();
  await expect(page).toHaveURL(/#downloads$/);
});


test('cold mobile collection loads one hero within budget and stays on native routes', async ({ page }, info) => {
  // Interception disables browser cache; the new test context has not loaded the site.
  await page.context().route('**/*', route => route.continue());
  const responses = [];
  const collect = response => responses.push(response);
  page.on('response', collect);
  await page.goto('/', {waitUntil: 'networkidle'});
  const hero = page.locator('.feature-art img');
  expect(await hero.count()).toBeLessThanOrEqual(1);
  if (await hero.count()) {
    await hero.evaluate(img => img.decode());
    const selected = await hero.evaluate(img => img.currentSrc);
    const heroCandidates = await page.locator('.feature-art source').evaluateAll(
      sources => sources.map(source => new URL(source.srcset, document.baseURI).href));
    heroCandidates.push(selected);
    const heroResponses = responses.filter(response => heroCandidates.includes(response.url()));
    expect(heroResponses.map(response => response.url())).toEqual([selected]);
    const mobileSource = new URL(await hero.getAttribute('src'), page.url()).href;
    expect(selected).toBe(mobileSource);
  }
  expect(responses.every(response => new URL(response.url()).origin === new URL(page.url()).origin)).toBeTruthy();
  expect(responses.some(response => /assets\/lessons\/|\/20(26|27)\.html/.test(new URL(response.url()).pathname))).toBeFalsy();
  const resources = await Promise.all(responses.map(async response => ({
    url: new URL(response.url()).pathname,
    bytes: (await response.body()).length,
  })));
  const bytes = resources.reduce((total, item) => total + item.bytes, 0);
  await info.attach('cold-mobile-body-bytes', {body: JSON.stringify({bytes, resources}), contentType: 'application/json'});
  console.log(`Cold mobile landing decoded response bodies: ${bytes} bytes`);
  expect(bytes).toBeLessThan(120 * 1024);
  page.off('response', collect);
  await page.getByRole('link', {name: 'Browse all lessons'}).tap();
  await expect(page).toHaveURL(/#studies$/);
  await page.getByRole('link', {name: /2027 New Testament/}).tap();
  await expect(page).toHaveURL(/2027\.html$/);
  await expect(page.getByRole('heading', {name: 'Matthew 1; Luke 1'})).toBeVisible();
  await expect(page.getByText('Dec 28, 2026–Jan 3, 2027', {exact: true})).toBeVisible();
  expect(await page.evaluate(() => document.documentElement.scrollWidth <= document.documentElement.clientWidth)).toBeTruthy();
  const header = page.getByRole('banner');
  await expect(header.getByRole('link', {name: 'COME, FOLLOW ME'})).toBeVisible();
  await header.getByRole('link', {name: 'All lessons', exact: true}).tap();
  await expect(page).toHaveURL(/index\.html#studies$/);
  const start = page.getByRole('link', {name: /Start the study/});
  const target = new URL(await start.getAttribute('href'), page.url()).href;
  await start.tap();
  await expect(page).toHaveURL(target);
});
