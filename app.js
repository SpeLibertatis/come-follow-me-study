"use strict";
(() => {
  const panels = [...document.querySelectorAll('[data-panel]')];
  const note = document.getElementById('private-thought');
  const status = document.querySelector('.save-status');
  const say = message => { if (status) status.textContent = message; };
  const validPanel = value => /^(start|finish|deep|story[0-2])$/.test(value);
  function showPanel(value, focus = false) {
    if (!panels.length) return;
    const target = validPanel(value) ? value : 'start';
    panels.forEach(panel => { panel.hidden = panel.dataset.panel !== target; });
    if (focus) document.getElementById(target)?.focus();
  }
  function syncLocation(focus = false) {
    showPanel(location.hash.slice(1), focus && (validPanel(location.hash.slice(1)) || !location.hash));
    document.querySelectorAll('nav a').forEach(link => {
      if (link.hash === location.hash) link.setAttribute('aria-current', 'location');
      else link.removeAttribute('aria-current');
    });
  }
  document.querySelectorAll('[data-go]').forEach(button => {
    button.addEventListener('click', () => {
      const target = button.dataset.go;
      if (!validPanel(target)) return;
      if (location.hash === '#' + target) showPanel(target, true);
      else location.hash = target;
    });
  });
  window.addEventListener('hashchange', () => syncLocation(true));
  syncLocation();
  // Keep evidence ahead of interpretation while retaining previously opened prompts.
  document.querySelectorAll('.story').forEach(story => {
    const steps = [...story.querySelectorAll('details')];
    steps.forEach((step, index) => {
      if (index) step.hidden = true;
      step.addEventListener('toggle', () => {
        if (step.open && steps[index + 1]) steps[index + 1].hidden = false;
      });
    });
  });
  document.querySelectorAll('[data-save]').forEach(button => {
    button.addEventListener('click', async () => {
      if (!note) return;
      const value = note.value;
      if (!value.trim()) {
        say('Write a thought first, or simply reflect quietly.');
        note.focus();
        return;
      }
      try {
        if (button.dataset.save === 'copy') {
          if (!navigator.clipboard?.writeText) throw Error('Clipboard unavailable');
          await navigator.clipboard.writeText(value);
          say('Copied. Your clipboard may be visible to other apps.');
        } else if (button.dataset.save === 'share') {
          if (!navigator.share) {
            say('Sharing is unavailable here. Use Copy or Download instead.');
            return;
          }
          await navigator.share({title: 'My private scripture reflection', text: value});
          say('Share sheet closed. Check your chosen app to confirm it saved.');
        } else if (button.dataset.save === 'download') {
          const url = URL.createObjectURL(new Blob([value + '\n'], {type: 'text/plain;charset=utf-8'}));
          const link = document.createElement('a');
          link.href = url;
          link.download = 'my-scripture-reflection.txt';
          link.click();
          setTimeout(() => URL.revokeObjectURL(url), 30000);
          say("Download requested. Check your device's Files or Downloads folder.");
        }
      } catch (error) {
        if (error?.name === 'AbortError') say('Sharing canceled. Your note is still on this page.');
        else {
          note.focus();
          note.select();
          say('That action did not complete. Your text is selected for manual copying, or try another option.');
        }
      }
    });
  });
  const clearNote = () => { if (note) note.value = ''; say(''); };
  window.addEventListener('pagehide', clearNote);
  window.addEventListener('pageshow', event => { if (event.persisted) clearNote(); });
})();
