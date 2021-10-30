function addnewrow(){
	var table = document.getElementById("staffContactTBody");
	var row = document.createElement('tr');

	var cls = "<input type='text' class='form-control form-control-sm minW' value=''>"
	td1 = document.createElement('td')
	td1.innerHTML = cls
	td2 = document.createElement('td')
	td2.innerHTML = cls
	td3 = document.createElement('td')
	td3.innerHTML = cls
	td4 = document.createElement('td')
	td4.innerHTML = cls
	td5 = document.createElement('td')
	td5.innerHTML = cls
	td6 = document.createElement('td')
	td6.innerHTML = cls
	td7 = document.createElement('td')
	td7.innerHTML = cls

	td8 = document.createElement('td')
	div = document.createElement('div')
	div.id = "staffbtnholder"
	form = document.createElement('form')
	form.method = "post"

	inp1 = document.createElement('input')
	inp1.type = "hidden"
	inp1.name = "csrfmiddlewaretoken"

	inp2 = document.createElement('input')
	inp2.type = "submit" 
	inp2.name = "update" 
	inp2.className = "btn btn-primary btn-sm stafftbltn"
	inp2.value = "Update"
	inp2.onclick = function(){addUpDelValues(this);}

	inp3 = document.createElement('input')
	inp3.type = "hidden"
	inp3.name = "updateData"

	inp4 = document.createElement('input')
	inp4.type = "submit" 
	inp4.name = "delete" 
	inp4.className = "btn btn-danger btn-sm stafftbltn"
	inp4.value = "Delete"
	inp4.onclick = function(){addUpDelValues(this);}

	inp5 = document.createElement('input')
	inp5.type = "hidden"
	inp5.name = "deleteData"



	form.appendChild(inp1)
	form.appendChild(inp2)
	form.appendChild(inp3)
	form.appendChild(inp4)
	form.appendChild(inp5)
	div.appendChild(form)
	td8.appendChild(div)

	row.appendChild(td1)
	row.appendChild(td2)
	row.appendChild(td3)
	row.appendChild(td4)
	row.appendChild(td5)
	row.appendChild(td6)
	row.appendChild(td7)
	row.appendChild(td8)

	table.appendChild(row)
}

function addnewlocrow() {
	var table = document.getElementById("stafflocateTBody");

	var row = document.createElement('tr');

	var cls = "<input type='text' class='form-control form-control-sm minW' value=''>"
	td1 = document.createElement('td')
	td1.innerHTML = cls
	td2 = document.createElement('td')
	td2.innerHTML = cls
	td3 = document.createElement('td')
	td3.innerHTML = cls
	td4 = document.createElement('td')
	td4.innerHTML = cls

	td5 = document.createElement('td')
	div = document.createElement('div')
	div.id = "staffbtnholder"
	form = document.createElement('form')
	form.method = "post"

	inp1 = document.createElement('input')
	inp1.type = "hidden"
	inp1.name = "csrfmiddlewaretoken"

	inp2 = document.createElement('input')
	inp2.type = "submit" 
	inp2.name = "updateLoc" 
	inp2.className = "btn btn-primary btn-sm stafftbltn"
	inp2.value = "Update"
	inp2.onclick = function(){addLocatValues(this);}

	inp3 = document.createElement('input')
	inp3.type = "hidden"
	inp3.name = "updateDataLoc"

	inp4 = document.createElement('input')
	inp4.type = "submit" 
	inp4.name = "deleteLoc" 
	inp4.className = "btn btn-danger btn-sm stafftbltn"
	inp4.value = "Delete"
	inp4.onclick = function(){addLocatValues(this);}

	inp5 = document.createElement('input')
	inp5.type = "hidden"
	inp5.name = "deleteDataLoc"



	form.appendChild(inp1)
	form.appendChild(inp2)
	form.appendChild(inp3)
	form.appendChild(inp4)
	form.appendChild(inp5)
	div.appendChild(form)
	td5.appendChild(div)

	row.appendChild(td1)
	row.appendChild(td2)
	row.appendChild(td3)
	row.appendChild(td4)
	row.appendChild(td5)
	

	table.appendChild(row)
}

function searchByCity() {
	// Declare variables
  var input, filter, table, tr, td, i, txtValue;
  input = document.getElementById("contactsearchbar");
  filter = input.value.toUpperCase();
  table = document.getElementById("staffContactTBody");
  tr = table.getElementsByTagName("tr");

  // Loop through all table rows, and hide those who don't match the search query
  for (i = 0; i < tr.length; i++) {
    td = tr[i].getElementsByTagName("td")[0];
    if (td) {
    	city = td.childNodes[0].value
    	if (city.toUpperCase().indexOf(filter) > -1)
    	{
    		tr[i].style.display = "";	
    	}
    	else
    	{
    		tr[i].style.display = "none";	
    	}
    	

    }
  }
}

function searchByLocate() {
	// Declare variables
  var input, filter, table, tr, td, i, txtValue;
  input = document.getElementById("locationsearchbar");
  filter = input.value.toUpperCase();
  table = document.getElementById("stafflocateTBody");
  tr = table.getElementsByTagName("tr");

  // Loop through all table rows, and hide those who don't match the search query
  for (i = 0; i < tr.length; i++) {
    td = tr[i].getElementsByTagName("td")[0];
    if (td) {
    	city = td.childNodes[0].value
    	if (city.toUpperCase().indexOf(filter) > -1)
    	{
    		tr[i].style.display = "";	
    	}
    	else
    	{
    		tr[i].style.display = "none";	
    	}
    	

    }
  }
}