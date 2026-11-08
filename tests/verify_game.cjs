'use strict';
// Development-only: npm install --prefix /tmp/daniel-game-test jsdom@26.1.0
// NODE_PATH=/tmp/daniel-game-test/node_modules node --test tests/verify_game.cjs
const { test } = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const { JSDOM } = require('jsdom');
const root = path.resolve(__dirname, '..');
function setup(loadScript = true) {
  const dom = new JSDOM(fs.readFileSync(path.join(root, 'index.html'), 'utf8'), {runScripts: 'outside-only', url: 'https://example.test/'});
  const {document} = dom.window;
  if (loadScript && fs.existsSync(path.join(root, 'game.js'))) dom.window.eval(fs.readFileSync(path.join(root, 'game.js'), 'utf8'));
  const game = document.querySelector('#daniel-word-challenge');
  assert.ok(game, 'The optional word challenge must exist independently of study completion');
  game.open = true;
  return {dom, document, game, get: id => document.getElementById(id), key(key, options = {}) {
    game.dispatchEvent(new dom.window.KeyboardEvent('keydown', {key, bubbles: true, ...options}));
  }};
}

test('optional game starts with a clue and hidden answer, without requiring study completion', () => {
  const {get} = setup();
  assert.equal(get('game-controls').hidden, false);
  assert.equal(get('game-progress').textContent, 'Word 1 of 8');
  assert.equal(get('game-word').getAttribute('aria-label'), '6 letters: blank blank blank blank blank blank');
  assert.equal(get('game-explanation').hidden, true);
});

test('correct guesses reveal letters, repeated guesses do nothing, misses allow unlimited play', () => {
  const {get, key, document} = setup();
  document.querySelector('[data-letter="D"]').click();
  assert.equal(get('game-word').getAttribute('aria-label'), '6 letters: D blank blank blank blank blank');
  const status = get('game-status').textContent;
  key('d');
  assert.equal(get('game-status').textContent, status);
  for (const letter of 'zxywqopbctu') key(letter);
  assert.match(get('game-status').textContent, /not in this word/);
  for (const letter of 'aniel') key(letter);
  assert.match(get('game-status').textContent, /You found DANIEL/);
  assert.equal(get('game-explanation').hidden, false);
  assert.equal(get('game-hint').disabled, true);
  key('v');
  assert.match(get('game-status').textContent, /You found DANIEL/);
});

test('a hint reveals a missing letter; reveal identifies an answer without claiming it was solved', () => {
  const {get} = setup();
  get('game-hint').click();
  assert.equal(get('game-word').getAttribute('aria-label'), '6 letters: D blank blank blank blank blank');
  get('game-reveal').click();
  assert.match(get('game-status').textContent, /^Answer: DANIEL/);
  assert.equal(get('game-explanation').hidden, false);
  get('game-next').click();
  assert.equal(get('game-progress').textContent, 'Word 2 of 8');
  assert.equal(get('game-word').getAttribute('aria-label'), '5 letters: blank blank blank blank blank');
  assert.equal(get('game-explanation').hidden, true);
  assert.equal(get('game-hint').disabled, false);
});

test('all puzzles are solvable by hints and the final puzzle restarts cleanly', () => {
  const {get, document} = setup();
  const answers = ['DANIEL', 'WATER', 'TEN DAYS', 'BUT IF NOT', 'GOLDEN IMAGE', 'THREE TIMES', 'JERUSALEM', 'ANGEL'];
  for (let i = 0; i < answers.length; i++) {
    let attempts = 0;
    while (!get('game-hint').disabled && attempts++ < 26) get('game-hint').click();
    assert.match(get('game-status').textContent, new RegExp('You found ' + answers[i]));
    assert.equal(get('game-explanation').hidden, false);
    assert.match(get('game-source').href, /^https:\/\/www\.churchofjesuschrist\.org\/study\/scriptures\/ot\/dan\/[136]\?/);
    get('game-next').click();
    assert.equal(document.activeElement.id, 'game-clue');
  }
  assert.equal(get('game-progress').textContent, 'Word 1 of 8');
});

test('multiword answers preserve word boundaries for accessible labels', () => {
  const {get} = setup();
  get('game-next').click(); get('game-next').click();
  assert.equal(get('game-word').getAttribute('aria-label'), '3 letters: blank blank blank; 4 letters: blank blank blank blank');
  get('game-reveal').click();
  assert.equal(get('game-word').getAttribute('aria-label'), '3 letters: T E N; 4 letters: D A Y S');
});

test('closed game, reflection typing, shortcuts, and IME input do not make guesses', () => {
  const {get, key, game, dom} = setup();
  const blank = get('game-word').getAttribute('aria-label');
  game.open = false; key('d'); game.open = true;
  get('thought').dispatchEvent(new dom.window.KeyboardEvent('keydown', {key: 'a', bubbles: true}));
  key('a', {ctrlKey: true}); key('n', {metaKey: true}); key('i', {altKey: true}); key('e', {isComposing: true}); key('Enter');
  assert.equal(get('game-word').getAttribute('aria-label'), blank);
});

test('page exit and a new page reset progress without storage', () => {
  const {get, dom} = setup();
  get('game-next').click();
  dom.window.dispatchEvent(new dom.window.PageTransitionEvent('pagehide'));
  assert.equal(get('game-progress').textContent, 'Word 1 of 8');
  assert.equal(dom.window.localStorage.length, 0);
  assert.equal(dom.window.sessionStorage.length, 0);
  assert.equal(dom.window.document.cookie, '');
  assert.equal(setup().get('game-progress').textContent, 'Word 1 of 8');
});

test('missing script leaves helpful fallback and no dead game controls', () => {
  const {get} = setup(false);
  assert.equal(get('game-controls').hidden, true);
  assert.equal(get('game-fallback').hidden, false);
  assert.match(get('game-fallback').textContent, /JavaScript/);
  assert.ok(get('finish'));
});

test('completion moves focus from an action that becomes disabled to the next word', () => {
  const {get, document} = setup();
  get('game-reveal').focus();
  get('game-reveal').click();
  assert.equal(document.activeElement.id, 'game-next');
  get('game-next').click();
  get('game-hint').focus();
  let count = 0;
  while (!get('game-hint').disabled && count++ < 26) get('game-hint').click();
  assert.equal(document.activeElement.id, 'game-next');
});
