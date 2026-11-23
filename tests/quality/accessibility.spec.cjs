const { test, expect } = require('@playwright/test');
const AxeBuilder = require('@axe-core/playwright').default;
const { appendFileSync } = require('node:fs');

const routes = [
  ['Collection', '/'],
  ['Daniel study', '/daniel.html'],
  ['Daniel word challenge (open)', '/daniel.html'],
  ['Explore Further', '/explore.html'],
  ['Joel study', '/lessons/hosea-joel.html'],
  ['Amos study', '/lessons/amos-obadiah-jonah.html'],
];

test('report verified axe findings separately from items needing review', async ({ page }, info) => {
  const rows = [
    '### Accessibility smoke (automated, report-only)',
    '',
    'Violations are axe-detected findings. Needs review means an automated result was inconclusive. Neither a zero count nor this route sample proves accessibility. PDFs and manual checks are out of scope.',
    '',
    '| Page/state | Violations (rules) | Needs review (rules) |',
    '| --- | --- | --- |',
  ];

  for (const [name, route] of routes) {
    await test.step(name, async () => {
      const response = await page.goto(route);
      expect(response.ok(), route).toBeTruthy();
      if (name.includes('challenge')) {
        await page.locator('#daniel-word-challenge > summary').click();
        await expect(page.locator('#game-controls')).toBeVisible();
      }
      const result = await new AxeBuilder({ page })
        .withTags(['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa', 'wcag22aa'])
        .analyze();
      const ids = items => items.map(item => item.id).join(', ') || 'none';
      rows.push(`| ${name} | ${result.violations.length}: ${ids(result.violations)} | ${result.incomplete.length}: ${ids(result.incomplete)} |`);
      await info.attach(name, {
        contentType: 'application/json',
        body: JSON.stringify({
          url: result.url,
          violations: result.violations,
          incomplete: result.incomplete,
        }, null, 2),
      });
      console.log(rows.at(-1));
    });
  }

  if (process.env.GITHUB_STEP_SUMMARY) {
    appendFileSync(process.env.GITHUB_STEP_SUMMARY, rows.join('\n') + '\n');
  }
});
