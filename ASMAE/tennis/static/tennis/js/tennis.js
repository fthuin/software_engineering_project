function ongletTournoi(){
	document.getElementById("tournoi").className = "active";
	document.getElementById("terrain").className = " ";
	document.getElementById("paire").className = " ";
	document.getElementById("extra").className = " ";

	document.getElementById("gestionTournoi").style.display = "inherit";
	document.getElementById("gestionTerrain").style.display = "none";
	document.getElementById("gestionPaire").style.display = "none";
	document.getElementById("gestionExtra").style.display = "none";
}

function ongletTerrain(){
	document.getElementById("tournoi").className = " ";
	document.getElementById("terrain").className = "active";
	document.getElementById("paire").className = " ";
	document.getElementById("extra").className = " ";

	document.getElementById("gestionTournoi").style.display = "none";
	document.getElementById("gestionTerrain").style.display = "inherit";
	document.getElementById("gestionPaire").style.display = "none";
	document.getElementById("gestionExtra").style.display = "none";
}

function ongletPaire(){
	document.getElementById("tournoi").className = " ";
	document.getElementById("terrain").className = " ";
	document.getElementById("paire").className = "active";
	document.getElementById("extra").className = " ";

	document.getElementById("gestionTournoi").style.display = "none";
	document.getElementById("gestionTerrain").style.display = "none";
	document.getElementById("gestionPaire").style.display = "inherit";
	document.getElementById("gestionExtra").style.display = "none";
}

function ongletExtra(){
	document.getElementById("tournoi").className = " ";
	document.getElementById("terrain").className = " ";
	document.getElementById("paire").className = " ";
	document.getElementById("extra").className = "active";

	document.getElementById("gestionTournoi").style.display = "none";
	document.getElementById("gestionTerrain").style.display = "none";
	document.getElementById("gestionPaire").style.display = "none";
	document.getElementById("gestionExtra").style.display = "inherit";
}

function extra(extra){
	document.getElementById("editExtra").style.display = "inherit";
	document.getElementById("newExtra").style.display = "none";

	document.getElementById("extraName").value = "Extra"+extra;
	document.getElementById("extraPrice").value = "TODO"
	document.getElementById("extracommentaire").innerHTML = "TODO"
}

function addExtra(){
	document.getElementById("editExtra").style.display = "none";
	document.getElementById("newExtra").style.display = "inherit";
}

function initialize() {
    var mapCanvas = document.getElementById('map');
    var mapOptions = {
      scrollwheel: false,
      navigationControl: false,
      center: new google.maps.LatLng(50.8539717, 4.4002427),
      zoom: 16,
      mapTypeId: google.maps.MapTypeId.ROADMAP
    }

    var map = new google.maps.Map(mapCanvas, mapOptions);
    var marker = new google.maps.Marker({
    position: {lat: 50.8539717, lng: 4.4002427},
    animation: google.maps.Animation.DROP,
    map: map,
    title: 'Cogefis'
  });
  }


function changeProfilPannel(){
	document.getElementById("Info").style.display="none";
	document.getElementById("editInfo").style.display="inherit"
}
/*
* Validation du formulaire d'inscription
* Vérification des champs et de la validité du numero de tel email et addresse
* TODO : email adress et tel validity
*/
function validateRegister() {
	var valid = true;
	//Verification username présent et > 2
	var username = document.getElementById("username").value;
	if(username==null || username == ""){
		document.getElementById("hint-username").innerHTML = " ! Entrer un nom d'utilisateur";
		valid = false;
	}else{
		if(username.length<3){
			document.getElementById("hint-username").innerHTML = " ! Votre nom d'utilisateur doit contenir au moins 3 caractères";
			valid = false;
		}else{
			document.getElementById("hint-username").innerHTML = "";
		}
	}

	//Verification mot de passe présent et > 2
	var password = document.getElementById("password").value;
	if(password==null || password == ""){
		document.getElementById("hint-password").innerHTML = " ! Entrer un mot de passe";
		valid = false;
	}else{
		if(password.length<3){
			document.getElementById("hint-password").innerHTML = " ! Votre mot de passe doit contenir au moins 3 caractères";
			valid = false;
		}else{
			document.getElementById("hint-password").innerHTML = "";
		}
	}

	//Verification nom présent
	var lastname = document.getElementById("lastname").value;
	if(lastname==null || lastname == ""){
		document.getElementById("hint-lastname").innerHTML = " ! Entrer votre nom";
		valid = false;
	}else{
		document.getElementById("hint-lastname").innerHTML = "";
	}

	//Verification prénom présent
	var firstname = document.getElementById("firstname").value;
	if(firstname==null || firstname == ""){
		document.getElementById("hint-firstname").innerHTML = " ! Entrer votre prénom";
		valid = false;
	}else{
		document.getElementById("hint-firstname").innerHTML = "";
	}

	//Verification email présent
	var email = document.getElementById("email").value;
	if(email==null || email == ""){
		document.getElementById("hint-email").innerHTML = " ! Entrer un email valide";
		valid = false;
	}else{
		//Verify email validity TODO
		document.getElementById("hint-email").innerHTML = "";
	}

	//Verification telephone présent
	var tel = document.getElementById("tel").value;
	var gsm = document.getElementById("gsm").value;
	if((tel==null || tel == "") && (gsm==null || gsm == "")){
		document.getElementById("hint-tel").innerHTML = " ! Entrer votre numéro de téléphone ou de GSM";
		valid = false;
	}else{
		//Verify number validity TODO
		document.getElementById("hint-tel").innerHTML = "";
	}
	//Verification rue présent
	var street = document.getElementById("street").value;
	if(street==null || street == ""){
		document.getElementById("hint-street").innerHTML = " ! Entrer votre rue";
		valid = false;
	}else{
		document.getElementById("hint-street").innerHTML = "";
	}

	//Verification numero présent
	var number = document.getElementById("number").value;
	if(number==null || number == ""){
		document.getElementById("hint-number").innerHTML = " ! Entrer votre numéro/boite";
		valid = false;
	}else{
		document.getElementById("hint-number").innerHTML = "";
	}

	//Verification code postal présent
	var postalcode = document.getElementById("postalcode").value;
	if(postalcode==null || postalcode == ""){
		document.getElementById("hint-postalcode").innerHTML = " ! Entrer votre code postal";
		valid = false;
	}else{
		document.getElementById("hint-postalcode").innerHTML = "";
	}

	//Verification localité présent
	var locality = document.getElementById("locality").value;
	if(locality==null || locality == ""){
		document.getElementById("hint-locality").innerHTML = " ! Entrer votre localité";
		valid = false;
	}else{
		document.getElementById("hint-locality").innerHTML = "";
	}

	//TODO vérification addresse correcte

	//Verification date de naissance présent
	var birthdate = document.getElementById("birthdate").value;
	if(birthdate==null || birthdate == ""){
		document.getElementById("hint-birthdate").innerHTML = " ! Entrer votre date de naissance";
		valid = false;
	}else{
		document.getElementById("hint-birthdate").innerHTML = "";
	}
	

	return false;
}

document.getElementById("foot01").innerHTML =
"<p>&copy;  " + new Date().getFullYear() + " ASMAE. All rights reserved.</p>";

google.maps.event.addDomListener(window, 'load', initialize);