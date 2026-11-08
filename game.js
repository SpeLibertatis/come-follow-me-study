'use strict';
// Optional word play. Nothing is stored, submitted, or connected to study completion.
(() => {
  const game = document.querySelector('#daniel-word-challenge');
  if (!game) return;
  const puzzles = [
    {answer: 'DANIEL', chapter: 1, verses: '8', clue: 'Who decided in his heart not to accept the king’s food and wine?', note: 'Daniel makes a firm decision, then asks respectfully for a different arrangement.'},
    {answer: 'WATER', chapter: 1, verses: '12', clue: 'What did Daniel ask to drink during the test?', note: 'Daniel asks for pulse to eat and water to drink. This story is not a nutrition experiment for students to repeat.'},
    {answer: 'TEN DAYS', chapter: 1, verses: '12–15', clue: 'How long did Daniel ask the steward to try the different food?', note: 'The steward agrees to the ten-day test. Daniel pairs his conviction with a practical, respectful request.'},
    {answer: 'BUT IF NOT', chapter: 3, verses: '17–18', clue: 'Which three words introduce the friends’ decision to stay faithful even without rescue?', note: '“But if not” makes room for trust without a guaranteed rescue. Suffering does not mean someone lacks faith.'},
    {answer: 'GOLDEN IMAGE', chapter: 3, verses: '14–18', clue: 'What did the king command the three friends to worship?', note: 'Shadrach, Meshach, and Abed-nego refuse to worship the golden image, even when the king gives them another chance.'},
    {answer: 'THREE TIMES', chapter: 6, verses: '10', clue: 'How often each day did Daniel kneel and pray?', note: 'Daniel prays three times a day and gives thanks, “as he did aforetime.” He is continuing a practice he already had.'},
    {answer: 'JERUSALEM', chapter: 6, verses: '10', clue: 'Toward which city were Daniel’s windows open when he prayed?', note: 'The story places Daniel far from Jerusalem, but describes him still turning toward God in prayer.'},
    {answer: 'ANGEL', chapter: 6, verses: '22', clue: 'Who does Daniel say God sent to shut the lions’ mouths?', note: 'Daniel tells the king that God sent an angel. This is the rescue described in the account, not a promise that every faithful person escapes danger.'}
  ];
  const get = id => document.getElementById(id);
  const alphabet = get('game-alphabet');
  const word = get('game-word');
  const status = get('game-status');
  const hint = get('game-hint');
  const reveal = get('game-reveal');
  const next = get('game-next');
  let index = 0;
  let guessed = new Set();
  let complete = false;

  function renderWord() {
    const answer = puzzles[index].answer;
    const groups = answer.split(' ');
    const spoken = [];
    word.replaceChildren();
    groups.forEach(group => {
      const row = document.createElement('span');
      row.className = 'game-word-group';
      row.setAttribute('aria-hidden', 'true');
      const letters = [];
      for (const letter of group) {
        const cell = document.createElement('span');
        cell.className = 'game-letter';
        const visible = guessed.has(letter);
        cell.textContent = visible ? letter : '\u00a0';
        letters.push(visible ? letter : 'blank');
        row.append(cell);
      }
      spoken.push(`${group.length} letters: ${letters.join(' ')}`);
      word.append(row);
    });
    word.setAttribute('aria-label', spoken.join('; '));
    alphabet.querySelectorAll('button').forEach(button => {
      const letter = button.dataset.letter;
      const used = guessed.has(letter);
      const found = used && answer.includes(letter);
      button.setAttribute('aria-disabled', String(used || complete));
      button.tabIndex = used || complete ? -1 : 0;
      button.dataset.state = used ? (found ? 'found' : 'miss') : 'ready';
      button.setAttribute('aria-label', used ? `${letter}, ${found ? 'in' : 'not in'} the answer` : `Guess ${letter}`);
    });
    const active = document.activeElement;
    if (complete && (active === hint || active === reveal)) next.focus({preventScroll: true});
    hint.disabled = complete;
    reveal.disabled = complete;
    get('game-explanation').hidden = !complete;
  }

  function guess(letter, fromHint = false) {
    if (complete || guessed.has(letter)) return;
    guessed.add(letter);
    const answer = puzzles[index].answer;
    complete = [...answer].every(char => char === ' ' || guessed.has(char));
    if (complete) status.textContent = `You found ${answer}. ${puzzles[index].note}`;
    else if (fromHint) status.textContent = `Hint: ${letter} is in the answer. Keep exploring.`;
    else status.textContent = answer.includes(letter) ? `${letter} is in the answer.` : `${letter} is not in this word. Try another letter; there is no guess limit.`;
    renderWord();
  }

  function startPuzzle(moveFocus = false) {
    guessed = new Set();
    complete = false;
    const puzzle = puzzles[index];
    get('game-progress').textContent = `Word ${index + 1} of ${puzzles.length}`;
    get('game-clue').textContent = puzzle.clue;
    const source = get('game-source');
    source.textContent = `Look in Daniel ${puzzle.chapter}:${puzzle.verses} ↗`;
    source.href = `https://www.churchofjesuschrist.org/study/scriptures/ot/dan/${puzzle.chapter}?lang=eng`;
    get('game-explanation').textContent = puzzle.note;
    status.textContent = 'Choose a letter, use a hint, or look in the scripture.';
    next.textContent = index === puzzles.length - 1 ? 'Start again' : 'Next word';
    renderWord();
    if (moveFocus) get('game-clue').focus({preventScroll: false});
  }

  for (const letter of 'ABCDEFGHIJKLMNOPQRSTUVWXYZ') {
    const button = document.createElement('button');
    button.type = 'button';
    button.textContent = letter;
    button.dataset.letter = letter;
    button.addEventListener('click', () => guess(letter));
    alphabet.append(button);
  }
  hint.addEventListener('click', () => {
    const letter = [...puzzles[index].answer].find(char => char !== ' ' && !guessed.has(char));
    if (letter) guess(letter, true);
  });
  reveal.addEventListener('click', () => {
    if (complete) return;
    guessed = new Set([...puzzles[index].answer].filter(char => char !== ' '));
    complete = true;
    status.textContent = `Answer: ${puzzles[index].answer}. Read the note below, then try another word.`;
    renderWord();
  });
  next.addEventListener('click', () => {
    index = (index + 1) % puzzles.length;
    startPuzzle(true);
  });
  game.addEventListener('keydown', event => {
    if (!game.open || event.ctrlKey || event.metaKey || event.altKey || event.isComposing || event.repeat) return;
    if (event.target.closest('input, textarea, select, [contenteditable="true"]')) return;
    if (/^[a-z]$/i.test(event.key)) {
      event.preventDefault();
      guess(event.key.toUpperCase());
    }
  });
  window.addEventListener('pagehide', () => { index = 0; startPuzzle(); });
  startPuzzle();
  get('game-controls').hidden = false;
  get('game-fallback').hidden = true;
})();
