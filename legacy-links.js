/* Only known former Daniel fragments move. No query data is copied or stored. */
(() => {
  const legacy = new Set(['#landing','#daniel-1','#daniel-3','#daniel-6','#reflection','#lions-den','#finished']);
  if (legacy.has(window.location.hash)) window.location.replace('daniel.html' + window.location.hash);
})();
