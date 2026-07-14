/**
 * Hurbs LLC - Minimal JavaScript
 * Logo load-failure fallback only. Copyright year is intentionally static
 * ("© 2026 Hurbs LLC" per the design reference).
 */

document.addEventListener('DOMContentLoaded', () => {
  const logo = document.querySelector('.nav-logo img');
  if (logo) {
    logo.onerror = () => {
      logo.style.display = 'none';
      const fallback = document.createElement('span');
      fallback.textContent = 'HURBS LLC';
      fallback.style.font = "400 22px 'Alfa Slab One', serif";
      logo.parentNode.appendChild(fallback);
    };
  }
});
