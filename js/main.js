/**
 * Hurbs LLC - Minimal JavaScript
 * Simple script for basic functionality
 */

// Wait for DOM to be fully loaded
document.addEventListener('DOMContentLoaded', () => {
  console.log('Hurbs LLC website loaded');
  
  // Basic logo error handling
  const logo = document.querySelector('img[alt="Hurbs LLC Logo"]');
  if (logo) {
    // Set a fallback in case SVG fails to load
    logo.onerror = () => {
      console.warn('Logo failed to load');
      logo.style.display = 'none';
      
      // Create a text fallback
      const fallbackText = document.createElement('h2');
      fallbackText.textContent = 'HURBS LLC';
      fallbackText.style.fontSize = '2rem';
      fallbackText.style.fontWeight = 'bold';
      fallbackText.style.padding = '2rem 0';
      logo.parentNode.appendChild(fallbackText);
    };
  }
  
  // Update copyright year
  const yearElement = document.getElementById('current-year');
  if (yearElement) {
    yearElement.textContent = new Date().getFullYear();
  }
});
