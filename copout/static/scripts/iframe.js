const iframe =  document.querySelector('iframe');

iframe.addEventListener('load', () => {
    iframe.src = iframe.src;
});