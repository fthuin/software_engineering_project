function preselectSelectOption(matiere,type,etat){
	function setSelectedIndex(s, valsearch)
	{
	// Loop through all the items in drop down list
		for (i = 0; i< s.options.length; i++)
		{
			if (s.options[i].value == valsearch)
			{
			// Item is found. Set its property and exit
			s.options[i].selected = true;
			break;
			}
		}
		return;
	}

	setSelectedIndex(document.getElementById("matiere"),matiere);
	setSelectedIndex(document.getElementById("type"),type);
	setSelectedIndex(document.getElementById("etat"),etat);
}

var UserList;

function setUser(User,page){
	UserList = User;
	var panneau = document.getElementById("UserList");
	panneau.innerHTML = "";

	var pageLength = 10;
	for (var i = 0; i < User.length && i<pageLength; i++) {
		var year = User[i][4].split(',')[1];
		var now = new Date().getFullYear();
		var age = now-year;
		var p = '<a onClick="selectUser('+"'"+User[i][0]+"',"+"'"+User[i][2]+"',"+"'"+User[i][1]+"'"+');" href="javascript:void(0)" class="list-group-item">'+User[i][0]+' - '+User[i][3]+' '+User[i][1]+' '+User[i][2]+' - '+age+' ans</a>';
		panneau.innerHTML += p;
	};

	var info = document.getElementById("UserInfo");
	info.innerHTML = '1-'+i+' sur '+pageLength+' résultats ('+User.length+' au total)';

}

function selectUser(username,nom,prenom){
	document.getElementById("username2Value").value = username;
	document.getElementById("username2").innerHTML = username;
	document.getElementById("nom2").innerHTML = nom;
	document.getElementById("prenom2").innerHTML = prenom;
}

function setDescription(sexe,birth){
	//Reset valeur du joueur 2
	document.getElementById("username2Value").value = "";
	document.getElementById("username2").innerHTML = " - ";
	document.getElementById("nom2").innerHTML = " - ";
	document.getElementById("prenom2").innerHTML = " - ";

	var panneau = document.getElementById("UserList");

	//CLean tableau
	setUser(UserList);

	var selector = document.getElementById("selector");
	var value = selector.options[selector.selectedIndex].id;
	var tournoi = selector.options[selector.selectedIndex].innerHTML;

	var valid = true;
	var error = "";

	if(tournoi=="Tournoi des familles"){
		//Check s'il peut participer à ce tournoi
		var year = birth.split(',')[1];
		var now = new Date().getFullYear();
		var age = now-year;
		if(age>15 && age<25){
			error = "Vous ne pouvez pas participer au tournoi des familles car vous n'avez pas moins de 15 ans ou plus de 25 ans !";
			valid = false;
			for (var i = 0; i < panneau.children.length; i++) {
				panneau.children[i].style.color ="red";
				panneau.children[i].style.fontWeight ="bold";
				panneau.children[i].onclick = function() {return false;};
			}

		}

		//Set les participant s'il peut les prendre ou non
		for (var i = 0; i < panneau.children.length; i++) {
			//Age du joueur du panneau
			var otherAge = panneau.children[i].innerHTML.split(" - ")[2].split(" ")[0];
			//SI on a moins de 15ans, il faut que le joueur ai plus de 25 ans
			if(age<=15 && otherAge<25){
				panneau.children[i].style.color ="red";
				panneau.children[i].style.fontWeight ="bold";
				panneau.children[i].onclick = function() {return false;};
			}
			//SI on a plus de 25ans, il faut que le joueur ai 15 ans ou moins
			if(age>=25 && otherAge>15){
				panneau.children[i].style.color ="red";
				panneau.children[i].style.fontWeight ="bold";
				panneau.children[i].onclick = function() {return false;};
			}
			
		}

	}
	if(tournoi=="Double mixte"){
		//Set les participant s'il peut les prendre ou non
		for (var i = 0; i < panneau.children.length; i++) {
			//Sexe du joueur du panneau
			var otherSexe = panneau.children[i].innerHTML.split(" - ")[1].split(" ")[0];
			if(sexe==otherSexe){
				panneau.children[i].style.color ="red";
				panneau.children[i].style.fontWeight ="bold";
				panneau.children[i].onclick = function() {return false;};
			}
		}
	}
	if(tournoi=="Double hommes"){
		//Check s'il peut participer à ce tournoi
		if(sexe=="Mme"){
			error = "Vous ne pouvez pas participer au double hommes car vous n'êtes pas un homme !";
			valid = false;
			for (var i = 0; i < panneau.children.length; i++) {
				panneau.children[i].style.color ="red";
				panneau.children[i].style.fontWeight ="bold";
				panneau.children[i].onclick = function() {return false;};
			}
		}

		//Set les participant s'il peut les prendre ou non
		for (var i = 0; i < panneau.children.length; i++) {
			//Sexe du joueur du panneau
			var otherSexe = panneau.children[i].innerHTML.split(" - ")[1].split(" ")[0];
			if(otherSexe=="Mme"){
				panneau.children[i].style.color ="red";
				panneau.children[i].style.fontWeight ="bold";
				panneau.children[i].onclick = function() {return false;};
			}
		}
	}
	if(tournoi=="Double femmes"){
		//Check s'il peut participer à ce tournoi
		if(sexe=="Mr"){
			error = "Vous ne pouvez pas participer au double femmes car vous n'êtes pas un femme !";
			valid = false;
			for (var i = 0; i < panneau.children.length; i++) {
				panneau.children[i].style.color ="red";
				panneau.children[i].style.fontWeight ="bold";
				panneau.children[i].onclick = function() {return false;};
			}
		}

		//Set les participant s'il peut les prendre ou non
		for (var i = 0; i < panneau.children.length; i++) {
			//Sexe du joueur du panneau
			var otherSexe = panneau.children[i].innerHTML.split(" - ")[1].split(" ")[0];
			if(otherSexe=="Mr"){
				panneau.children[i].style.color ="red";
				panneau.children[i].style.fontWeight ="bold";
				panneau.children[i].onclick = function() {return false;};
			}
		}
	}

	document.getElementById("Description").innerHTML=value;
	document.getElementById("hint-tournoi").innerHTML = error;
	if(!valid){
		document.getElementById("InscriptionButton").disabled = true;
	}else{
		document.getElementById("InscriptionButton").disabled = false;
	}

	
	
}

function selectMasterCard(){
	document.getElementById("mastercard").style.display = "inherit";
	document.getElementById("visa").style.display = "none";
	document.getElementById("paypal").style.display = "none";
	document.getElementById("virement").style.display = "none";
}

function selectVisa(){
	document.getElementById("mastercard").style.display = "none";
	document.getElementById("visa").style.display = "inherit";
	document.getElementById("paypal").style.display = "none";
	document.getElementById("virement").style.display = "none";
}

function selectPaypal(){
	document.getElementById("mastercard").style.display = "none";
	document.getElementById("visa").style.display = "none";
	document.getElementById("paypal").style.display = "inherit";
	document.getElementById("virement").style.display = "none";
}

function selectVirement(){
	document.getElementById("mastercard").style.display = "none";
	document.getElementById("visa").style.display = "none";
	document.getElementById("paypal").style.display = "none";
	document.getElementById("virement").style.display = "inherit";
}

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

function extra(id, nom,prix,comment){
	document.getElementById("editExtra").style.display = "inherit";
	document.getElementById("newExtra").style.display = "none";

	var c = document.getElementById("listExtra").children;
	for (i = 0; i < c.length; i++) {
		if(c[i].id==id){
			c[i].className="list-group-item active";
		}else{
			c[i].className="list-group-item";
		}
    }
	document.getElementById("extraID").value = id;
	document.getElementById("deleteID").value = id;
	document.getElementById("extraName").value = nom;
	document.getElementById("formTitle").innerHTML = "Editer " + nom;
	document.getElementById("extraPrice").value = prix;
	document.getElementById("extracommentaire").innerHTML = comment;
}

function activeExtra(){
	var c = document.getElementById("listExtra").children;
	c[0].className="list-group-item active";
}

function addExtra(){
	document.getElementById("editExtra").style.display = "none";
	document.getElementById("newExtra").style.display = "inherit";

	var c = document.getElementById("listExtra").children;
	for (i = 0; i < c.length; i++) {
		c[i].className="list-group-item";
    }

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
	document.getElementById("editInfo").style.display="inherit";
}

function changeMDP(){
	document.getElementById("compteInfo").style.display="none";
	document.getElementById("editMDP").style.display="inherit";
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
	

	return valid;
}

function validateEditInfo() {
	var valid = true;

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
	

	return valid;
}

document.getElementById("foot01").innerHTML =
"<p>&copy;  " + new Date().getFullYear() + " ASMAE. All rights reserved.</p>";

google.maps.event.addDomListener(window, 'load', initialize);
activeExtra();
alert("lol");