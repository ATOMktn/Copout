const iframe =  document.querySelector('iframe');

window.addEventListener('click', () => {
    iframe.src = iframe.src;
});