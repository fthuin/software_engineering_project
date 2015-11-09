/*
 * Fonction pour mettre des Strings en majuscules (ignorant les
 * accents)
 * src : http://www.finalclap.com/faq/257-javascript-supprimer-remplacer-accent
 */

String.prototype.sansAccent = function(){
    var accent = [
        /[\300-\306]/g, /[\340-\346]/g, // A, a
        /[\310-\313]/g, /[\350-\353]/g, // E, e
        /[\314-\317]/g, /[\354-\357]/g, // I, i
        /[\322-\330]/g, /[\362-\370]/g, // O, o
        /[\331-\334]/g, /[\371-\374]/g, // U, u
        /[\321]/g, /[\361]/g, // N, n
        /[\307]/g, /[\347]/g, // C, c
    ];
    var noaccent = ['A','a','E','e','I','i','O','o','U','u','N','n','C','c'];
     
    var str = this;
    for(var i = 0; i < accent.length; i++){
        str = str.replace(accent[i], noaccent[i]);
    }
     
    return str;
}

/*
 * Fonction used to select option in the terrain edit section
 */
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
//-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
//-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
//-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
/*
 * Section for the users pagination in the tournement registration
 */
//Lite des users
var UserList;
//longueur de la page
var pageLength;

//On met à jours les infos
function setUserListInfo(userList,longueur){
	UserList = userList;
	pageLength = longueur;
}

//Permet de changer le contenu de la page en fonction de la page ou on se trouve
function setUser(page){
	//Conteneur de notre liste
	var panneau = document.getElementById("UserList");
	panneau.innerHTML = "";

	var debut = (page-1)*pageLength;
	var fin = page*pageLength;

	//Ajout des users
	for (var i = debut; i < UserList.length && i<fin; i++) {
		var year = UserList[i][4].split('/')[2];
		var now = new Date().getFullYear();
		var age = now-year;
		var p = '<a onClick="selectUser('+"'"+UserList[i][0]+"',"+"'"+UserList[i][2]+"',"+"'"+UserList[i][1]+"'"+');" href="javascript:void(0)" class="list-group-item">'+UserList[i][0]+' - '+UserList[i][3]+' '+UserList[i][1]+' '+UserList[i][2]+' - '+age+' ans</a>';
		panneau.innerHTML += p;
	};

	//Info maj
	var info = document.getElementById("UserInfo");
	info.innerHTML = (debut+1)+'-'+i+' sur '+pageLength+' résultats ('+UserList.length+' au total)';

}

//Lorsqu'on selectionne un utilistaeur on met ses valeurs dans le tableaux du dessous
function selectUser(username,nom,prenom){
	document.getElementById("username2Value").value = username;
	document.getElementById("user2").innerHTML = prenom +' '+nom+' ('+username+')';
	if(document.getElementById("hint-tournoi").innerHTML==""){
		document.getElementById("InscriptionButton").disabled = false;
	}
}

//Lorsqu'on click sur un tournoi, on met à jours la description ainsi que les différentes restriction par rapport au tournoi
function setDescription(sexe,birth){
	//Reset valeur du joueur 2
	document.getElementById("username2Value").value = "";
	document.getElementById("user2").innerHTML = 'Coéquipier';
	document.getElementById("InscriptionButton").disabled = true;

	//Paneau d'utilisateur
	var panneau = document.getElementById("UserList");

	//Tournoi selectionner
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
		}
	}
	if(tournoi=="Double hommes"){
		//Check s'il peut participer à ce tournoi
		if(sexe=="Mme"){
			error = "Vous ne pouvez pas participer au double hommes car vous n'êtes pas un homme !";
			valid = false;
		}
	}
	if(tournoi=="Double femmes"){
		//Check s'il peut participer à ce tournoi
		if(sexe=="Mr"){
			error = "Vous ne pouvez pas participer au double femmes car vous n'êtes pas un femme !";
			valid = false;
		}
	}

	document.getElementById("Description").innerHTML=value;
	document.getElementById("hint-tournoi").innerHTML = error;

	var pagination = document.getElementById("UserPagination");
	var pageNow = 1;
	for (var i = 0; i < pagination.children.length; i++) {

		if(pagination.children[i].className=="page active"){
			pageNow = pagination.children[i].children[0].innerHTML
		}
	};
	//On set les uers restrictions
	setUserRestriction(sexe,birth,pageNow);
}

//permet de mette  des restrictions sur les utilistaurs. S'ils peuvent pas etre avec sois en tournoi il sont mis en rouge et non clickable
function setUserRestriction(sexe,birth,page){
	//CLean tableau
	setUser(page);

	var panneau = document.getElementById("UserList");

	var selector = document.getElementById("selector");
	var value = selector.options[selector.selectedIndex].id;
	var tournoi = selector.options[selector.selectedIndex].innerHTML;

	if(tournoi=="Tournoi des familles"){
		var year = birth.split(',')[1];
		var now = new Date().getFullYear();
		var age = now-year;
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
			//Les joueurs entre 15 et 25 ans ne peuvent pas participer
			if(otherAge<25 && otherAge>15){
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

}
//Fin de la section des users dans l'inscription à un tournoi
//-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
//-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
//-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
/*
 * Sections utilisé lors du paiement pour choisir une méthode de paiement
 */
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
//Fin de la section sur les paiements
//-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
//-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
//-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
/*
 * Section staff
 */
//TOURNOI
function setTournoi(TournoiList){
	var panneau = document.getElementById("ListTournoi");
	panneau.innerHTML = "";
	for (var i = 0; i < TournoiList.length; i++) {
		var nom = TournoiList[i][0];
		var description = TournoiList[i][1];
		var jour = TournoiList[i][2];
		var p = '<a class="list-group-item"><b>Nom : </b>'+nom+'<br><b>Description : </b>'+description+'<br><b>Jour : </b>'+jour+'</a>';
		panneau.innerHTML += p;
	};
}

function setPlusMoins(){
	if(document.getElementById("plusmoins").className.indexOf("chevron-up")>-1){
		document.getElementById("plusmoins").className  = "glyphicon glyphicon-chevron-down pull-right"
	}else{
		document.getElementById("plusmoins").className  = "glyphicon glyphicon-chevron-up pull-right"
	}
	
}


//TERRAIN
//Lite des terrains
var CourtList;
//longueur de la page
var pageLength;

//On met à jours les infos
function setCourtListInfo(courtList,longueur){
	CourtList = courtList;
	pageLength = longueur;
}

//Permet de changer le contenu de la page en fonction de la page ou on se trouve
function setCourt(page){
	//Conteneur de notre liste
	var panneau = document.getElementById("CourtList");
	panneau.innerHTML = "";

	var debut = (page-1)*pageLength;
	var fin = page*pageLength;

	//Ajout des courts
	for (var i = debut; i < CourtList.length && i<fin; i++) {
		//Set info court
		var adress;
		if(CourtList[i][9]!=""){
			adress = CourtList[i][5]+' '+CourtList[i][6]+' bte '+CourtList[i][9]+',<br> '+CourtList[i][7]+' '+CourtList[i][8];
		}else{
			adress = CourtList[i][5]+' '+CourtList[i][6]+',<br> '+CourtList[i][7]+' '+CourtList[i][8];
		}
		var valid = CourtList[i][10];
		var dispo = CourtList[i][11];
		
		//var p = '<tr class="clickable-row" data-href="utilisateurs/'+UserList[i][0]+'"><td>'+UserList[i][0]+'</td><td>'+UserList[i][1]+'</td><td>'+UserList[i][2]+'</td><td>'+age+' ans</td></tr>';
		var p = '<tr onclick="window.document.location='+"'terrains/"+CourtList[i][3]+"'"+';" class="clickable-row"><td>'+CourtList[i][3]+'</td><td>'+CourtList[i][4]+'</td><td>'+valid+'</td><td>'+dispo+'</td><td>'+CourtList[i][1]+' '+CourtList[i][2]+' ('+CourtList[i][0]+')</td><td>'+adress+'</td></tr>';
		panneau.innerHTML += p;
	};

	//Info maj
	var info = document.getElementById("CourtInfo");
	info.innerHTML = (debut+1)+'-'+i+' sur '+pageLength+' résultats ('+CourtList.length+' au total)';

}


//PAIR
//Lite des terrains
var PairList;

//On met à jours les infos
function setPairListInfo(pairList,longueur){
	PairList = pairList;
	pageLength = longueur;
}

//Permet de changer le contenu de la page en fonction de la page ou on se trouve
function setPair(page){
	//Conteneur de notre liste
	var panneau = document.getElementById("PairList");
	panneau.innerHTML = "";

	var debut = (page-1)*pageLength;
	var fin = page*pageLength;

	//Ajout des pair
	for (var i = debut; i < PairList.length && i<fin; i++) {
		//Set info pair
		var user1 = PairList[i][7] +' '+ PairList[i][5] + ' ('+PairList[i][3]+')';
		var user2 = PairList[i][8] +' '+ PairList[i][6] + ' ('+PairList[i][4]+')';
		var valid = PairList[i][1];
		var pay = PairList[i][2];
		var info = '<b>ID : </b>'+PairList[i][0]+' / <b> Tournoi : </b>'+PairList[i][9]+' / <b>Valide : </b>'+valid+' / <b>Payé : </b>'+pay;
		
		var p = '<tr onclick="window.document.location='+"'paires/"+PairList[i][0]+"'"+';" class="clickable-row"><td>'+PairList[i][0]+'</td><td>'+PairList[i][9]+'</td><td>'+valid+'</td><td>'+pay+'</td><td>'+user1+'</td><td>'+user2+'</td></tr>';
		
		//var p = '<a href="paires/'+PairList[i][0]+'" class="list-group-item">'+info+'<br>'+user1+' - '+user2+'</a>';
		panneau.innerHTML += p;
	};

	//Info maj
	var info = document.getElementById("PairInfo");
	info.innerHTML = (debut+1)+'-'+i+' sur '+pageLength+' résultats ('+PairList.length+' au total)';

}

//USER
//Permet de changer le contenu de la page en fonction de la page ou on se trouve
function setUserStaff(page){
	//Conteneur de notre liste
	var panneau = document.getElementById("UserList");
	panneau.innerHTML = "";

	var debut = (page-1)*pageLength;
	var fin = page*pageLength;

	//Ajout des users
	for (var i = debut; i < UserList.length && i<fin; i++) {
		var year = UserList[i][4].split('/')[2];
		var now = new Date().getFullYear();
		var age = now-year;
		var p = '<tr onclick="window.document.location='+"'utilisateurs/"+UserList[i][0]+"'"+';" class="clickable-row"><td>'+UserList[i][0]+'</td><td>'+UserList[i][1]+'</td><td>'+UserList[i][2]+'</td><td>'+age+' ans</td></tr>';
		panneau.innerHTML += p;
	};

	//Info maj
	var info = document.getElementById("UserInfo");
	info.innerHTML = (debut+1)+'-'+i+' sur '+pageLength+' résultats ('+UserList.length+' au total)';

}

function setUserPermStaff(page){
	//Conteneur de notre liste
	var panneau = document.getElementById("UserList");
	panneau.innerHTML = "";

	var debut = (page-1)*pageLength;
	var fin = page*pageLength;

	//Ajout des users
	for (var i = debut; i < UserList.length && i<fin; i++) {
		var year = UserList[i][4].split('/')[2];
		var now = new Date().getFullYear();
		var age = now-year;
		var p = '<a onClick="selectUserStaff('+"'"+UserList[i][0]+"',"+"'"+UserList[i][2]+"',"+"'"+UserList[i][1]+"',"+"'"+UserList[i][5]+"','"+UserList[i][6]+"'"+');" href="javascript:void(0)" class="list-group-item">'+UserList[i][0]+' - '+UserList[i][3]+' '+UserList[i][1]+' '+UserList[i][2]+' - '+age+' ans</a>';
		panneau.innerHTML += p;
	};

	//Info maj
	var info = document.getElementById("UserInfo");
	info.innerHTML = (debut+1)+'-'+i+' sur '+pageLength+' résultats ('+UserList.length+' au total)';

}

var logList;
var logListPageLength;
function setLogListInfo(list, pageLength) {
    logList = list;
    logListPageLength = pageLength;
}

function setLogStaff(page) {
	//Conteneur de notre liste
	var panneau = document.getElementById("LogList");
	panneau.innerHTML = "";

	var debut = (page-1)*logListPageLength;
	var fin = page*logListPageLength;

	//Ajout des logs
	for (var i = debut; i < logList.length && i<fin; i++) {
	    var p = '<tr><td>'+logList[i][0]+'</td><td>'+logList[i][1]+' '+logList[i][2]+' ('+logList[i][3]+')</td><td>'+logList[i][4]+'</td><td>'+logList[i][5]+'</td></tr>';
		panneau.innerHTML += p;
	};

	//Info maj
	var info = document.getElementById("LogInfo");
	info.innerHTML = (debut+1)+'-'+i+' sur '+logListPageLength+' résultats ('+logList.length+' au total)';
}

function admin()
{
    if(document.getElementById("permID").checked == true)
    {
        document.getElementById("extraID").disabled = true;
        document.getElementById("userID").disabled = true;
        document.getElementById("pairID").disabled = true;
        document.getElementById("courtID").disabled = true;      
        document.getElementById("Tournoi des famillesID").disabled = true;
        document.getElementById("Double hommesID").disabled = true;
        document.getElementById("Double femmesID").disabled = true;
        document.getElementById("Double mixteID").disabled = true;
    }
    if(document.getElementById("permID").checked == false)
    {
        document.getElementById("extraID").disabled = false;
        document.getElementById("userID").disabled = false;
        document.getElementById("pairID").disabled = false;
        document.getElementById("courtID").disabled = false;      
        document.getElementById("Tournoi des famillesID").disabled = false;
        document.getElementById("Double hommesID").disabled = false;
        document.getElementById("Double femmesID").disabled = false;
        document.getElementById("Double mixteID").disabled = false;
    }
}
function selectUserStaff(username,nom,prenom,perm,group){
	document.getElementById("usernameID").value = username;
	document.getElementById("userInfo").innerHTML = prenom +' '+nom+' ('+username+')';
	document.getElementById("valider").disabled = false;
	document.getElementById("userInfo").href = "/tennis/staff/utilisateurs/"+username;
	
	//TODO set permissions on checkpoint
    if(perm.indexOf("extra") > -1)
    {
        document.getElementById("extraID").checked = true;
    }
    else
    {
        document.getElementById("extraID").checked = false;
    }
    if(perm.indexOf("pair") > -1)
    {
        document.getElementById("pairID").checked = true;
    }
    else
    {
        document.getElementById("pairID").checked = false;
    }
    if(perm.indexOf("court") > -1)
    {
        document.getElementById("courtID").checked = true;
    }
    else
    {
        document.getElementById("courtID").checked = false;
    }
    if(perm.indexOf("User") > -1)
    {
        document.getElementById("userID").checked = true;
    }
    else
    {
        document.getElementById("userID").checked = false;
    }
     if(perm.indexOf("tournoi des familles") > -1)
    {
        document.getElementById("Tournoi des famillesID").checked = true;
    }
    else
    {
        document.getElementById("Tournoi des famillesID").checked = false;
    }
     if(perm.indexOf("double hommes") > -1)
    {
        document.getElementById("Double hommesID").checked = true;
    }
    else
    {
        document.getElementById("Double hommesID").checked = false;
    }
     if(perm.indexOf("double femmes") > -1)
    {
        document.getElementById("Double femmesID").checked = true;
    }
    else
    {
        document.getElementById("Double femmesID").checked = false;
    }
     if(perm.indexOf("double mixte") > -1)
    {
        document.getElementById("Double mixteID").checked = true;
    }
    else
    {
        document.getElementById("Double mixteID").checked = false;
    }
     if(group.indexOf("Admin") > -1)
    {
        document.getElementById("permID").checked = true;
    }
    else
    {
        document.getElementById("permID").checked = false;
    }
    admin();
}


//EXTRA
//permet de selectionner un extra
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
	var prixWithPoint = prix.replace(",",".");
	document.getElementById("extraPrice").value = prixWithPoint;
	document.getElementById("extracommentaire").innerHTML = comment;
}

//Active le premier extra
function activeExtra(){
	var c = document.getElementById("listExtra").children;
	c[0].className="list-group-item active";
}

//Permet d'ajouter un nouvel extra
function addExtra(){
	document.getElementById("editExtra").style.display = "none";
	document.getElementById("newExtra").style.display = "inherit";

	var c = document.getElementById("listExtra").children;
	for (i = 0; i < c.length; i++) {
		c[i].className="list-group-item";
    }

}

//Fin de la section staff
//-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
//-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
//-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
/*
 * Section profil
 */

 //permet d'avoir le formulaire d'edition du profil
function changeProfilPannel(){
	document.getElementById("Info").style.display="none";
	document.getElementById("editInfo").style.display="inherit";
}

//permet d'avoir le formulaire d'edition du mot de passe
function changeMDP(){
	document.getElementById("compteInfo").style.display="none";
	document.getElementById("editMDP").style.display="inherit";
}

//Fonction utilisé pour validé le formulaire d'édition du profil
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
//fin de la section profil
//-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
//-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
//-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
/*
 * Section inscription
 */

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
	var birthdate = document.getElementById("birthdateID").value;
	if(birthdate.indexOf("x") > -1){
		document.getElementById("hint-birthdate").innerHTML = " ! Entrer votre date de naissance";
		valid = false;
	}else{
		document.getElementById("hint-birthdate").innerHTML = "";
	}
	

	return valid;
}
//Fin de la section inscription
//-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
//-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
//-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
/*
 * Section contact
 */

//Initialisation de la google map
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
//fin de la section contact
//-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
//-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
//-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
/*
 * Footer
 */
 //permet de mettre les droit et l'année dans le footer
document.getElementById("foot01").innerHTML =
"<p>&copy;  " + new Date().getFullYear() + " ASMAE. All rights reserved.</p>";
//Fin de la section footer
//-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
//-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
//-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
