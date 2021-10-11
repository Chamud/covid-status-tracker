function searchname() {
	// Declare variables
  var input, filter, table, tr, td, i, txtValue;
  input = document.getElementById("searchbar");
  filter = input.value.toUpperCase();
  table = document.getElementById("admintable");
  tr = table.getElementsByTagName("tr");

  // Loop through all table rows, and hide those who don't match the search query
  for (i = 0; i < tr.length; i++) {
    td = tr[i].getElementsByTagName("td")[0];
    if (td) {
      txtValue = td.textContent || td.innerText;
      if (txtValue.toUpperCase().indexOf(filter) > -1) {
        tr[i].style.display = "";
      } else {
		td = tr[i].getElementsByTagName("td")[1];
	    if (td) {
	      txtValue = td.textContent || td.innerText;
	      if (txtValue.toUpperCase().indexOf(filter) > -1) {
	        tr[i].style.display = "";
	      } else {
	        tr[i].style.display = "none";
	      }
	    }
      }
    }
  }
}

function filterusers(filter){
	table = document.getElementById("admintable");
  	tr = table.getElementsByTagName("tr");
  	if(filter == "all")
  	{
  		 for (i = 0; i < tr.length; i++) {
  		 	tr[i].style.display = "";
  		 }
  	}
  	if(filter == "pub")
  	{
  		for (i = 0; i < tr.length; i++) {
  		 	td = tr[i].getElementsByTagName("td")[3];
		    if (td) {
		      txtValue = td.innerText.toUpperCase();
		      if (txtValue.includes("TRUE")) {
		        tr[i].style.display = "none";
		      } else {
				td = tr[i].getElementsByTagName("td")[4];
			    if (td) {
			      txtValue = td.innerText.toUpperCase();
			      if (txtValue.includes("TRUE")) {
			        tr[i].style.display = "none";
			      } else {

			        tr[i].style.display = "";
			      }
			    }
		      }
		    }
  		}
  	}
  	if(filter == "stf")
  	{
  		for (i = 0; i < tr.length; i++) {
  		 	td = tr[i].getElementsByTagName("td")[3];
		    if (td) {
		    	txtValue = td.innerText.toUpperCase();
		      	if (txtValue.includes("TRUE")) {
					td = tr[i].getElementsByTagName("td")[4];
			    	if (td) {
				      	txtValue = td.innerText.toUpperCase();
				      	if (txtValue.includes("TRUE")) {
				        	tr[i].style.display = "none";
				      	} 
				      	else {
				        	tr[i].style.display = "";
				      	}
			    	}
			    }
			    else{
			    	tr[i].style.display = "none";
			    }
		    }
  		}
  	}
  	if(filter == "adm")
  	{
  		for (i = 0; i < tr.length; i++) {
  		 	td = tr[i].getElementsByTagName("td")[4];
		    if (td) {
		    	txtValue = td.innerText.toUpperCase();
		      	if (txtValue.includes("TRUE")) {
				
				    tr[i].style.display = "";
			    }
			    else{
			    	tr[i].style.display = "none";
			    }
		    }
  		}
  	}
}