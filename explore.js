'use strict';
// Theme selection exists only in memory. No reading or engagement history.
const themeButtons = [...document.querySelectorAll('[data-theme]')];
const resources = [...document.querySelectorAll('.library-resource')];
const filterStatus = document.querySelector('#filter-status');
function filterResources(theme, label) {
  let count = 0;
  resources.forEach(resource => {
    resource.hidden = theme !== 'all' && !resource.dataset.themes.split(' ').includes(theme);
    if (!resource.hidden) count++;
  });
  themeButtons.forEach(button => button.setAttribute('aria-pressed', String(button.dataset.theme === theme)));
  document.querySelectorAll('.resource-section').forEach(section => {
    section.querySelector('.category-empty').hidden = [...section.querySelectorAll('.library-resource')].some(resource => !resource.hidden);
  });
  filterStatus.textContent = `${count} ${count === 1 ? 'resource' : 'resources'} · ${label}`;
  document.querySelector('#no-results').hidden = count !== 0;
}
themeButtons.forEach(button => button.addEventListener('click', () => filterResources(button.dataset.theme, button.textContent)));
document.querySelector('#theme-controls').hidden = false;
filterResources('all', 'All resources');
