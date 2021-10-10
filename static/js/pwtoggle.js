function pwtoggle(inp, tog){
	var pwvisibility = document.getElementById(inp);
	var pwtog = document.getElementById(tog);
  	if (pwvisibility.type === "password") 
  	{
    	pwvisibility.type = "text";
    	pwtog.classList = "fa fa-eye-slash";
  	}else 
  	{
    	pwvisibility.type = "password";
    	pwtog.classList = "fa fa-eye";
  	}

}