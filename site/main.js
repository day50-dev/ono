// Simple animation for performance bars
document.addEventListener('DOMContentLoaded', () => {
  const bars = document.querySelectorAll('.bar');
  bars.forEach(bar => {
    const height = bar.style.height;
    bar.style.height = '0';
    setTimeout(() => {
      bar.style.transition = 'height 1.5s ease-in-out';
      bar.style.height = height;
    }, 500);
  });
});
