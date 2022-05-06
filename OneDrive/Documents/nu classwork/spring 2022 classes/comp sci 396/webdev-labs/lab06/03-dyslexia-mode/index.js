/* 
  See Smashing Magazine Tutorial:
  https://www.smashingmagazine.com/2021/11/dyslexia-friendly-mode-website/
*/


const dyslexiaToggle = () => { 
  document.getElementsByTagName("body")[0].classList.toggle("dyslexia-mode");
}

document.querySelector("#dyslexia-toggle").addEventListener('click', dyslexiaToggle);