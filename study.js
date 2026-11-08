'use strict';
// Reflection stays only in this page; exports require explicit action.
const $ = selector => document.querySelector(selector);
$('#finished').hidden = true;
function revealDestination(hash) {
  if (hash === '#finished') $('#finished').hidden = false;
}
// Reveal before native anchor navigation so focus, history and scrolling stay native.
document.querySelectorAll('a[href="#finished"]').forEach(link => {
  link.addEventListener('click',() => revealDestination(link.hash));
});
function orient() {
  const hash = location.hash || '#landing';
  revealDestination(hash);
  document.querySelectorAll('.chapters a').forEach(link => {
    if (link.hash === hash) link.setAttribute('aria-current','location');
    else link.removeAttribute('aria-current');
  });
  if (hash === '#finished') $('#finished-title').focus({preventScroll:true});
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
