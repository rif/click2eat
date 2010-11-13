// Display this message
var answer = confirm('Am detectat că foloseşti o versiune veche a navigatorului Internet Explorer. Pentru o experienţă cît mai plăcută pe web, recomandăm instalarea ultimei versiuni a acestui navigator. Administratorii nu îşi asumă nici o răspundere cu privire la modul în care această pagină web se va comporta pe un navigator vechi. \n\n Apăsînd "OK", te vom redirecta către o pagină de pe care îţi vei putea alege un navigator.');

// If the answet is Yes, then I will redirect to another page		
if(answer) window.top.location = 'http://www.browserchoice.eu/';