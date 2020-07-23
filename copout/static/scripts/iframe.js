const iframe =  document.querySelector('iframe');

const refreshFrame = () => iframe.src = iframe.src;

window.addEventListener('DOMContentLoaded', refreshFrame);
window.removeEventListener('DOMContentLOaded', refreshFrame);