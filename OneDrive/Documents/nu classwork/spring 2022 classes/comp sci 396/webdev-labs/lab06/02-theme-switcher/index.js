/*
    Hints: 
    1. Attach click event handlers to all four of the 
       buttons (#default, #ocean, #desert, and #high-contrast).
    2. Modify the className property of the body tag 
       based on the button that was clicked.
*/

const defaulttheme = () => {

   document.getElementsByTagName("body")[0].className = "";

}

const oceantheme = () => {

   document.getElementsByTagName("body")[0].className = "ocean";

}

const deserttheme = () => {

   document.getElementsByTagName("body")[0].className = "desert";

}

const highcontrasttheme = () => {

   document.getElementsByTagName("body")[0].className = "high-contrast";

}

document.querySelector("#default").addEventListener('click', defaulttheme);
document.querySelector("#ocean").addEventListener('click', oceantheme);
document.querySelector("#desert").addEventListener('click', deserttheme);
document.querySelector("#high-contrast").addEventListener('click', highcontrasttheme);