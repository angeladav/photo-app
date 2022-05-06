const makeBigger = () => {
   //alert('make bigger!');
   fontSizeP+=5;
   fontSizeH *= 1.25;
   document.querySelector(".content p").style.fontSize = fontSizeP + "px";
   document.querySelector("h1").style.fontSize = fontSizeH + "px";

};

const makeSmaller = () => {
   //alert('make smaller!');
   fontSizeP-=5;
   fontSizeH *= 0.75;
   document.querySelector(".content p").style.fontSize = fontSizeP + "px";
   document.querySelector("h1").style.fontSize = fontSizeH + "px";
};

// let fontSizeP = 20;
// let fontSizeH = 25;

var el = document.querySelector(".content p");
var style = window.getComputedStyle(el, null).getPropertyValue('font-size');
var fontSizeP = parseFloat(style); 

var el = document.querySelector("h1");
var style = window.getComputedStyle(el, null).getPropertyValue('font-size');
var fontSizeH = parseFloat(style); 

document.querySelector("#a1").addEventListener('click', makeBigger);
document.querySelector("#a2").addEventListener('click', makeSmaller);

