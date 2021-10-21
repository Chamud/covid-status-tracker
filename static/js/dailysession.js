function imposeMinMax(el){
  	if(el.value != ""){
  /*	if(parseInt(el.value) < parseInt(el.min)){
      	el.value = el.min;
    }*/
    	if(parseInt(el.value) > parseInt(el.max)){
      	el.value = el.max;
    }
  }
}

function twoSlider(slider, slidevalue, mild, severe){
	if(slidevalue<1){
		document.getElementById(mild).style.backgroundColor = "#eee";
		document.getElementById(mild).style.color = "green";
		document.getElementById(severe).style.backgroundColor = "#eee";
		document.getElementById(severe).style.color = "red";
	}
	else if(slidevalue<6){
		document.getElementById(mild).style.backgroundColor = "#48A14D";
		document.getElementById(mild).style.color = "white";
		document.getElementById(severe).style.backgroundColor = "#eee";
		document.getElementById(severe).style.color = "red";
	}
	else if(slidevalue<10){
		document.getElementById(severe).style.backgroundColor = "#D92121";
		document.getElementById(severe).style.color = "white";
		document.getElementById(mild).style.backgroundColor = "#eee";
		document.getElementById(mild).style.color = "green";
	}
	const root = document.querySelector(":root");
	root.style.setProperty(slider, slidevalue*7.92+'%');
}

function threeSlider(slider, slidevalue, mild, painful, severe){

	if(slidevalue<1){
		document.getElementById(mild).style.backgroundColor = "#eee";
		document.getElementById(mild).style.color = "green";
		document.getElementById(painful).style.backgroundColor = "#eee";
		document.getElementById(painful).style.color = "#ffc107";
		document.getElementById(severe).style.backgroundColor = "#eee";
		document.getElementById(severe).style.color = "red";
	}
	else if(slidevalue<4){
		document.getElementById(mild).style.backgroundColor = "#48A14D";
		document.getElementById(mild).style.color = "white";
		document.getElementById(severe).style.backgroundColor = "#eee";
		document.getElementById(severe).style.color = "red";
		document.getElementById(painful).style.backgroundColor = "#eee";
		document.getElementById(painful).style.color = "#ffc107";
	}
	else if(slidevalue<7){
		document.getElementById(painful).style.backgroundColor = "#ffc107";
		document.getElementById(painful).style.color = "white";
		document.getElementById(mild).style.backgroundColor = "#eee";
		document.getElementById(mild).style.color = "green";
		document.getElementById(severe).style.backgroundColor = "#eee";
		document.getElementById(severe).style.color = "red";
	}
	else if(slidevalue<10){
		document.getElementById(severe).style.backgroundColor = "#D92121";
		document.getElementById(severe).style.color = "white";
		document.getElementById(mild).style.backgroundColor = "#eee";
		document.getElementById(mild).style.color = "green";
		document.getElementById(painful).style.backgroundColor = "#eee";
		document.getElementById(painful).style.color = "#ffc107";
	}

	const root = document.querySelector(":root");
	root.style.setProperty(slider, slidevalue*7.95+'%');
}

var clockElement = document.getElementById('clock');

function clock() {
   clockElement.textContent = new Date().toLocaleString();
}
function clock() {
   clockElement.textContent = new Date().toLocaleString();
}
