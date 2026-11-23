const { defineConfig, devices } = require('@playwright/test');
const path = require('node:path');

const origin = 'http://127.0.0.1:4173';
module.exports = defineConfig({
  testDir: '.',
  fullyParallel: false,
  workers: 1,
  reporter: 'list',
  timeout: 45_000,
  use: { baseURL: origin, reducedMotion: 'reduce' },
  projects: [
    { name: 'iPhone-like WebKit', testMatch: 'mobile.spec.cjs', use: { ...devices['iPhone 13'], browserName: 'webkit' } },
    { name: 'axe Chromium', testMatch: 'accessibility.spec.cjs', use: { browserName: 'chromium' } },
  ],
  webServer: {
    command: 'python3 -m http.server 4173 --bind 127.0.0.1',
    cwd: path.resolve(__dirname, '../..'),
    url: origin,
    reuseExistingServer: false,
  },
});
