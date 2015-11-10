//utilisé pour le drag and drop
function drag (ev) {
  ev.dataTransfer.setData("src", ev.target.id);
}

function drop (ev) {
  ev.preventDefault();
  var src = document.getElementById(ev.dataTransfer.getData("src"));
  var srcParent = src.parentNode;
  var tgt = ev.currentTarget.firstElementChild;

  var targetID = tgt.parentNode.parentNode.parentNode.parentNode.id;
  var sourceID = src.parentNode.parentNode.parentNode.parentNode.id;

  ev.currentTarget.replaceChild(src, tgt);
  srcParent.appendChild(tgt);

  //update leader liste
  updatePanel(targetID);
  updatePanel(sourceID);
  
}

function allowDrop(ev) {
    ev.preventDefault();
}

//Listener pour le popover
$(document).ready(function(){
    $('[data-toggle="popover"]').popover();   
});



var pairList;

function setPairList(pairL){
	pairList = pairL;
}

function setPoules(nbrPoules){
	//On flush le contenant de nous poules
	document.getElementById("poulesDiv").innerHTML = "";
	//On recupere le nombre de pair
	var v = pairList.length;
	//on recupere le nombre de poules
	var poules = nbrPoules;
	//il y aura au max 'max' pair par poules
	var max = Math.ceil(v/poules);

	document.getElementById("poulesSize").value = max;

	document.getElementById("poulesNumber").value = nbrPoules;

	var count = 0;
	//on crée nbrPoules de poules
	for (var i = 0; i < nbrPoules; i++) {
		//On compte le nombre d'element dans cette poule
		var nbr = Math.ceil(v/poules);
		v = v - nbr;
		poules = poules - 1;
		//Creation du panel de la poule
		var panel = createPanel(i+1);
		document.getElementById("poulesDiv").appendChild(panel);

		//Ajout des pair dans le panel et dans la liste du leader
		for (var j = 0; j < nbr; j++) {
			//Panel
			var p = createPair(pairList[count]);
			document.getElementById("list"+(i+1)).appendChild(p);

			//List
			var nom1 = pairList[count].user1;
			var nom2 = pairList[count].user2;
			document.getElementById("Leader"+(i+1)).appendChild(getOption(nom1));
			document.getElementById("Leader"+(i+1)).appendChild(getOption(nom2));
			document.getElementById("Leader"+(i+1)).appendChild(getSpaceOption());

			count = count + 1;

		};
		document.getElementById("Leader"+(i+1)).removeChild(document.getElementById("Leader"+(i+1)).childNodes[document.getElementById("Leader"+(i+1)).childNodes.length-1]);
		//Si c'est plutot que le nombre max on rajotue des espaces vides
		for (var j = 0; j < max - nbr; j++) {
			var p = createEmptyPair(i);
			document.getElementById("list"+(i+1)).appendChild(p);
		};
		
	};
}

//Update the list of user in the leader list of a panel
function updatePanel(numero){
	//Panel et liste
	var panel = document.getElementById("list"+numero);
	var list = document.getElementById("Leader"+numero);
	list.innerHTML = "<option disabled selected>Choisir un leader</option>";
	var c = panel.childNodes
	//Update des noms
	for (var i = 0; i < c.length; i++) {
		var id = c[i].childNodes[0].childNodes[0].id;
		if(id.indexOf("bidon")<0){
			var pair = getPairbyId(id);
			list.appendChild(getOption(pair.user1));
			list.appendChild(getOption(pair.user2));
			list.appendChild(getSpaceOption());
		}
	};
	list.removeChild(list.childNodes[list.childNodes.length-1]);
}

function getPairbyId(ID){
	for (var i = 0; i < pairList.length; i++) {
		if(pairList[i].id == ID){
			return pairList[i];
		};
	};
}

//Return une option avec comme nom et valeur le name
function getOption(name){
	var o = document.createElement("option");
	o.value = name;
	o.innerHTML = name;

	return o;
}

function getSpaceOption() {
	var o = document.createElement("option");
	o.disabled = true;
	o.value = "";
	o.innerHTML = "";

	return o;
}

//Return le panel d'une poule
function createPanel(number){
	var panel = document.createElement("div");
	panel.className = 'col-lg-4';
	panel.innerHTML = '<div class="panel panel-default" id="'+number+'"><div class="panel-heading"><div class="row"><label class="control-label col-xs-4">Poule '+number+'</label><div class="col-xs-8"><select class="form-control" name="Leader" id="Leader'+number+'"><option disabled selected>Choisir un leader</option></select></div></div></div><div class="list-group" id="list'+number+'"></div><div class="panel-footer"><div class="row"><label class="control-label col-xs-4">Terrain (TODO)</label><div class="col-xs-8"><select class="form-control" name="terrain" id="terrain'+number+'"><option disabled selected>Choisir un terrain</option></select></div></div><div class="row"><label class="control-label col-xs-7">Empreinte Carbone</label><div class="col-xs-5"><p class="info">TODO</p></div></div></div></div>';
    return panel;
}

//Return une pair
function createPair(pair){
	var p = document.createElement("div");
	
	var gender1 = "";
	var gender2 = "";
	if(pair.titre1=="Mr"){
		gender1 = "fa fa-male";
	}else{
		gender1 = "fa fa-female";
	}
	if(pair.titre2=="Mr"){
		gender2 = "fa fa-male";
	}else{
		gender2 = "fa fa-female";
	}

	
	var comm = "" ;
	if(pair.comment != ""){
		comm = '<a href="javascript:void(0);" data-toggle="popover" data-html="true" data-placement="left" data-content="'+pair.comment+'"><b style="color:#222;"><i class="fa fa-file-text-o fa-2x"></i></b></a>';
	}
	
	p.innerHTML = '<div class="dropBox" ondragover="allowDrop(event)" ondrop="drop(event)" style="padding-left:10px;padding-right:10px;padding-top:3px; padding-bottom:3px;"><div id="'+pair.id+'" draggable="true" ondragstart="drag(event)"><div class="zone"><div class="row"><div class="col-xs-10"><b style="color:#222"><i class="'+gender1+'"></i></b> '+pair.user1+' ('+pair.age1+' ans)'+'<br><b style="color:#222"><i class="'+gender2+'"></i></b> '+pair.user2+' ('+pair.age2+' ans)'+'</div><div class="col-xs-2">'+comm+'</div></div></div></div></div>';

	return p;
}

//return une pair vide
function createEmptyPair(i){
	var p = document.createElement("div");
	p.innerHTML='<div class="dropBox" ondragover="allowDrop(event)" ondrop="drop(event)" style="padding-left:10px;padding-right:10px;padding-top:3px; padding-bottom:3px;"><div id="bidon'+i+'" draggable="true" ondragstart="drag(event)"><div class="zone"><div class="row"><div class="col-xs-10"><br><br></div><div class="col-xs-2"></div></div></div></div></div>';
	return p;
}






