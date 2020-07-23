const iframe =  document.querySelector('iframe');

const refreshFrame = () => iframe.src = 'copout/static/map/map.html';

window.addEventListener('load', refreshFrame);
window.removeEventListener('load', refreshFrame);