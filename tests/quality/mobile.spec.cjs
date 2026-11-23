const { test, expect } = require('@playwright/test');

test('small-screen collection, ready studies and print routes', async ({ page }) => {
  await page.goto('/');
  await expect(page.getByRole('heading', { level: 1 })).toBeVisible();
  const width = await page.evaluate(() => document.documentElement.clientWidth);
  expect(width, 'mobile viewport (CSS pixels)').toBeLessThanOrEqual(430);
  const cards = page.locator('.lesson-list li').filter({ hasText: 'Ready to study' });
  const paths = await cards.locator('h2 a').evaluateAll(links => links.map(a => a.href));
  expect(paths.length).toBeGreaterThan(0);
  const checkReflow = () => expect.poll(() => page.evaluate(() => (
    document.documentElement.scrollWidth <= document.documentElement.clientWidth
  ))).toBe(true);
  await checkReflow();

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
  await page.getByRole('link', { name: /Begin the quick path/ }).tap();
  await expect(page).toHaveURL(/#quick$/);
  const disclosure = page.locator('#quick details').first();
  await disclosure.locator('summary').tap();
  await expect(disclosure).toHaveJSProperty('open', true);
  await page.getByRole('link', { name: 'Print & keep', exact: true }).tap();
  await expect(page).toHaveURL(/#downloads$/);
});
