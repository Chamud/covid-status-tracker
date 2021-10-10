function navbarselect(item) {
	if (item == "home"){
		document.getElementById("navhome").classList = "nav-link active shadow"
	}
	else if (item == "tracker"){
		document.getElementById("navtracker").classList = "nav-link active shadow"
	}
	else if (item == "map"){
		document.getElementById("navmap").classList = "nav-link active shadow"
	}else if (item == "stf"){
		document.getElementById("navstf").classList = "nav-link active shadow"
	}
	else if (item == "adm"){
		document.getElementById("navadm").classList = "nav-link active shadow"
	}
}