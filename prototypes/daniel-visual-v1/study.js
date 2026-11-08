'use strict';
// State is deliberately volatile. No persistence or network APIs.
const scenes = [
  {title:'At the king’s table',ref:'DANIEL 1:3–20',chapter:1,context:'Narrative context · In the Babylonian court, young captives receive new training, names, and provisions. The account places Daniel’s decision within this pressure to assimilate (Daniel 1:3–8).',question:'What do you notice about the way Daniel makes his request?',steps:['Command · The king assigns daily food and wine to the young men in training (1:5).','Response · Daniel resolves not to defile himself, asks permission, and proposes a ten-day test of vegetables and water (1:8–14).','Outcome · The account describes their healthy appearance and later their learning and skill (1:15–20). Interpretation: notice Daniel’s resolve alongside his respectful approach.']},
  {title:'Before the furnace',ref:'DANIEL 3:13–30',chapter:3,context:'Narrative context · The king’s image and public decree make worship a test of loyalty in the story (Daniel 3:1–7). This imagined setting is not an archaeological reconstruction.',question:'What remains unchanged in their answer if deliverance does not come?',steps:['Command · The king orders worship of the image under threat of the furnace (3:14–15).','Response · The friends affirm God’s power to deliver, yet refuse to worship the image even if He does not (3:16–18).','Outcome · The narrative describes their preservation in the fire and the king’s acknowledgment of their God (3:24–30). Interpretation: their commitment came before they knew the outcome.']},
  {title:'The open window',ref:'DANIEL 6:6–23',chapter:6,context:'Narrative context · Daniel 6 places Daniel under Darius. Officials use a royal prohibition to target his established religious practice (Daniel 6:1–9). Read this as the account’s setting, without treating every historical identification as settled.',question:'Which detail shows that prayer was already part of Daniel’s life?',steps:['Command · A decree forbids petitions to any god or man other than the king for thirty days, with the lions’ den as penalty (6:6–9).','Response · Daniel continues his established practice of prayer and thanksgiving (6:10–11).','Outcome · Daniel is cast into the den and later found unharmed; he attributes his preservation to God (6:16–23). Interpretation: the story invites reflection on steady devotion, not a formula for safety.']}
];
const $ = selector => document.querySelector(selector);
const buttons = [...document.querySelectorAll('[data-scene]')];
const progress = scenes.map(() => 0);
function renderScene(index) {
  const scene = scenes[index];
  buttons.forEach((button,i) => button.setAttribute('aria-pressed',String(i === index)));
  $('#scene-title').textContent = scene.title;
  $('#scene-ref').textContent = scene.ref;
  $('#scene-context').textContent = scene.context;
  $('#scene-question').textContent = scene.question;
  $('#scene-source').href = `https://www.churchofjesuschrist.org/study/scriptures/ot/dan/${scene.chapter}?lang=eng`;
  const container = $('#reveals');
  container.replaceChildren();
  scene.steps.forEach((step,i) => {
    if (i > progress[index]) return;
    const details = document.createElement('details');
    const summary = document.createElement('summary');
    const paragraph = document.createElement('p');
    summary.textContent = ['01 / Reveal the command','02 / Reveal the response','03 / Reveal the outcome'][i];
    paragraph.textContent = step;
    details.append(summary,paragraph);
    details.addEventListener('toggle',() => {
      if (details.open && progress[index] === i && i < 2) {
        progress[index]++;
        const next = makeNext(index,i + 1);
        container.append(next);
      }
    });
    container.append(details);
  });
}
function makeNext(index,i) {
  const details = document.createElement('details');
  const summary = document.createElement('summary');
  const paragraph = document.createElement('p');
  summary.textContent = ['01 / Reveal the command','02 / Reveal the response','03 / Reveal the outcome'][i];
  paragraph.textContent = scenes[index].steps[i];
  details.append(summary,paragraph);
  details.addEventListener('toggle',() => {
    if (details.open && progress[index] === i && i < 2) {
      progress[index]++;
      $('#reveals').append(makeNext(index,i + 1));
    }
  });
  return details;
}
buttons.forEach((button,i) => button.addEventListener('click',() => renderScene(i)));
renderScene(0);
document.querySelectorAll('[name="mode"]').forEach(input => input.addEventListener('change',() => {
  const deep = input.value === 'deep';
  document.querySelectorAll('.deep-content').forEach(element => element.hidden = !deep);
  $('#mode-summary').textContent = deep ? 'YOUR PATH · ABOUT 45–60 MINUTES' : 'YOUR PATH · ABOUT 15 MINUTES';
}));
function orient() {
  const hash = location.hash || '#landing';
  document.querySelectorAll('.chapters a').forEach(link => {
    if (link.hash === hash) link.setAttribute('aria-current','location');
    else link.removeAttribute('aria-current');
  });
}
window.addEventListener('hashchange',orient);
orient();
const thought = $('#thought');
const status = $('#save-status');
function textToSave() {
  if (!thought.value.trim()) { status.textContent = 'Write a thought first, or leave this reflection private and unwritten.'; return null; }
  return thought.value;
}
$('#copy').addEventListener('click',async () => {
  const text = textToSave(); if (text === null) return;
  try { await navigator.clipboard.writeText(text); status.textContent = 'Copied to your clipboard. Choose where to paste it.'; }
  catch { thought.focus(); thought.select(); status.textContent = 'Automatic copy is unavailable. Your text is selected; use your device’s Copy command.'; }
});
$('#share').addEventListener('click',async () => {
  const text = textToSave(); if (text === null) return;
  if (!navigator.share) { status.textContent = 'Sharing is unavailable here. Use Copy text or Download .txt.'; return; }
  try { await navigator.share({title:'My Daniel study reflection',text}); status.textContent = 'Share request completed. The chosen app controls its copy.'; }
  catch(error) { status.textContent = error.name === 'AbortError' ? 'Share canceled. Your reflection remains here.' : 'Sharing failed. Use Copy text or Download .txt.'; }
});
$('#download').addEventListener('click',() => {
  const text = textToSave(); if (text === null) return;
  try {
    const url = URL.createObjectURL(new Blob([text],{type:'text/plain;charset=utf-8'}));
    const link = document.createElement('a'); link.href = url; link.download = 'daniel-reflection.txt';
    document.body.append(link); link.click(); link.remove();
    setTimeout(() => URL.revokeObjectURL(url),1000);
    status.textContent = 'Download requested. Check your browser’s downloads; the file will remain on your device.';
  } catch { status.textContent = 'Download unavailable. Use Copy text to keep your reflection.'; }
});
$('#clear').addEventListener('click',() => { thought.value = ''; status.textContent = 'Reflection cleared from this page.'; thought.focus(); });
window.addEventListener('pagehide',() => { thought.value = ''; status.textContent = ''; });
