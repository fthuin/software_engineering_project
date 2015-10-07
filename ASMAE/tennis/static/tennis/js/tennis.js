document.getElementById("foot01").innerHTML =
"<p>&copy;  " + new Date().getFullYear() + " ASMAE. All rights reserved.</p>";

/*
* Validation du formulaire d'inscription
* Vérification des champs et de la validité du numero de tel email et addresse
* TODO : email adress et tel validity
*/
function validateRegister() {
	var valid = true;

	//Verification username présent et > 2
	var username = document.forms["registerForm"]["username"].value;
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
	var password = document.forms["registerForm"]["password"].value;
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
	var lastname = document.forms["registerForm"]["lastname"].value;
	if(lastname==null || lastname == ""){
		document.getElementById("hint-lastname").innerHTML = " ! Entrer votre nom";
		valid = false;
	}else{
		document.getElementById("hint-lastname").innerHTML = "";
	}

	//Verification prénom présent
	var firstname = document.forms["registerForm"]["firstname"].value;
	if(firstname==null || firstname == ""){
		document.getElementById("hint-firstname").innerHTML = " ! Entrer votre prénom";
		valid = false;
	}else{
		document.getElementById("hint-firstname").innerHTML = "";
	}

	//Verification email présent
	var email = document.forms["registerForm"]["email"].value;
	if(email==null || email == ""){
		document.getElementById("hint-email").innerHTML = " ! Entrer un email valide";
		valid = false;
	}else{
		//Verify email validity TODO
		document.getElementById("hint-email").innerHTML = "";
	}

	//Verification telephone présent
	var tel = document.forms["registerForm"]["tel"].value;
	var gsm = document.forms["registerForm"]["gsm"].value;
	if((tel==null || tel == "") && (gsm==null || gsm == "")){
		document.getElementById("hint-tel").innerHTML = " ! Entrer votre numéro de téléphone ou GSM";
		valid = false;
	}else{
		//Verify number validity TODO
		document.getElementById("hint-tel").innerHTML = "";
	}

	//Verification rue présent
	var street = document.forms["registerForm"]["street"].value;
	if(street==null || street == ""){
		document.getElementById("hint-street").innerHTML = " ! Entrer votre rue";
		valid = false;
	}else{
		document.getElementById("hint-street").innerHTML = "";
	}

	//Verification numero présent
	var number = document.forms["registerForm"]["number"].value;
	if(number==null || number == ""){
		document.getElementById("hint-number").innerHTML = " ! Entrer votre numéro/boite";
		valid = false;
	}else{
		document.getElementById("hint-number").innerHTML = "";
	}

	//Verification code postal présent
	var postalcode = document.forms["registerForm"]["postalcode"].value;
	if(postalcode==null || postalcode == ""){
		document.getElementById("hint-postalcode").innerHTML = " ! Entrer votre code postal";
		valid = false;
	}else{
		document.getElementById("hint-postalcode").innerHTML = "";
	}

	//Verification localité présent
	var locality = document.forms["registerForm"]["locality"].value;
	if(locality==null || locality == ""){
		document.getElementById("hint-locality").innerHTML = " ! Entrer votre localité";
		valid = false;
	}else{
		document.getElementById("hint-locality").innerHTML = "";
	}

	//TODO vérification addresse correcte

	//Verification date de naissance présent
	var birthdate = document.forms["registerForm"]["birthdate"].value;
	if(birthdate==null || birthdate == ""){
		document.getElementById("hint-birthdate").innerHTML = " ! Entrer votre date de naissance";
		valid = false;
	}else{
		document.getElementById("hint-birthdate").innerHTML = "";
	}


	return valid;
}