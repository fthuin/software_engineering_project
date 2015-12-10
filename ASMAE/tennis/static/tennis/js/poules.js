function setKm()
{

	/* DEBUT COPIER COLLER */
    document.getElementById("assignTerrains").value = ""
    document.getElementById("assignPairPoules").value = ""
    document.getElementById("assignLeaders").value = ""
    var nbr = document.getElementById("poulesNumber").value;
    var poulesDict = {};
    for (var i = 0; i < nbr ; i++) {
        var poule = {}
        poule['leader'] = document.getElementById("Leader"+(i+1)).value;
        poule['terrainID'] = document.getElementById("ID"+(i+1)).textContent;
        poule['pairList'] = [];
        poulesDict[''+i] = poule;
        // TODO : Check si le leader et le terrainID sont valides
    }
    for (var i = 0; i < PairList.length ; i++) {
        // On link les paires aux ID des poules
        var id = "" + document.getElementById(""+PairList[i].id).parentNode.parentNode.parentNode.id;
        id = id.replace("list", "");
        poulesDict[''+(id-1)]['pairList'].push(PairList[i]);
    }
    for (var i = 0; i < nbr ; i++) {
         document.getElementById("assignTerrains").value += poulesDict[''+i]['terrainID'] + '-';
         document.getElementById("assignPairPoules").value += '[' + i + ']-'
         for (var j = 0 ; j < poulesDict[''+i]['pairList'].length ; j++) {
            document.getElementById("assignPairPoules").value += poulesDict[''+i]['pairList'][j].id + '-';
         }
         document.getElementById("assignLeaders").value += poulesDict[''+i]['leader'] + '/';
    }
	/* FIN COPIER COLLER */
	/* Accéder à la première paire de la première poule */
	// poulesDict['1']['pairList'][0]
	/* Fin accéder à la premiere ... */
	//alert(poulesDict['1']['pairList'][0].u2addr);


	dico = {};
/*	for(var j=0;j<TerrainList.length;j++){
				dico[TerrainList[j].id] = {};
				totalDistanceTerrain = 0;*/

					for(var key in poulesDict){
						var terId = poulesDict[key]['terrainID']
						var terIndex = -1;
						for(var j=0;j<TerrainList.length;j++){
							if(TerrainList[j].id == terId){
								terIndex = j
							}
						}

						if(terIndex != -1)
						{

						var terrainLat = TerrainList[terIndex].lat;
						var terrainLng = TerrainList[terIndex].lng;
						var terrainlatLng = new google.maps.LatLng(parseFloat(terrainLat.replace(",", ".")), parseFloat(terrainLng.replace(",", ".")))

						var totalDistanceTerrain = 0;
						for(var i = 0;i<poulesDict[key]['pairList'].length;i++){

							var user1Lat = poulesDict[key]['pairList'][i].lat1;
							var user1Lng = poulesDict[key]['pairList'][i].lng1;
							var user2Lat = poulesDict[key]['pairList'][i].lat2;
							var user2Lng = poulesDict[key]['pairList'][i].lng2;
							var latLng1 = new google.maps.LatLng(parseFloat(user1Lat.replace(",", ".")), parseFloat(user1Lng.replace(",", ".")));
							var latLng2 = new google.maps.LatLng(parseFloat(user2Lat.replace(",", ".")), parseFloat(user2Lng.replace(",", ".")));
							var distance1 = google.maps.geometry.spherical.computeDistanceBetween(latLng1, terrainlatLng);
							var distance2 = google.maps.geometry.spherical.computeDistanceBetween(latLng2, terrainlatLng);
							totalDistanceTerrain = totalDistanceTerrain + distance1 + distance2;
							//alert(distance1);
							//alert(distance2);
						}
					//alert("total");
					//alert(totalDistanceTerrain);

					dico[key] = totalDistanceTerrain;
					document.getElementById("empreinte"+(parseInt(key)+1)).innerHTML = Math.round(totalDistanceTerrain)/1000;
					}
				}


	}

//}

//utilisé pour le drag and drop
function drag (ev) {
  ev.dataTransfer.setData("src", ev.target.id);
}

function drop (ev) {
  ev.preventDefault();
  var src = document.getElementById(ev.dataTransfer.getData("src"));
  var srcParent = src.parentNode;
  var tgt = ev.currentTarget.firstElementChild;

  var targetID = ('' + tgt.parentNode.parentNode.parentNode.parentNode.id).replace('panel', '');
  var sourceID = ('' + src.parentNode.parentNode.parentNode.parentNode.id).replace('panel', '');

  ev.currentTarget.replaceChild(src, tgt);
  srcParent.appendChild(tgt);

  //update leader liste
  updatePanel(targetID, "Choisir un leader");
  updatePanel(sourceID, "Choisir un leader");

	setKm();
	leaderAssignement();

}

function allowDrop(ev) {
    ev.preventDefault();
}

//Listener pour le popover
$(document).ready(function(){
    $('[data-toggle="popover"]').popover();
});


var pairDict;
var pairList;
var terrainList;

function setPairDict(pairD) {
    pairDict = pairD;
}

function setPairList(pairL,terrainL){
	pairList = pairL;
	terrainList = terrainL;
}

function setTerrains(nbrPoules) {
    var v = pairList.length;
    var lenTer = terrainList.length;
    for (var i = 0 ; i < nbrPoules ; i++) {
        for (var j = 0 ; j < lenTer ; j++) {
            document.getElementById("terrain"+(i+1)).appendChild(getDropDownOption(terrainList[j],(i+1)));
        }
    }
}

function mySetPoules(nbrPoules, sizePoules) {
	document.getElementById("poulesSize").value = sizePoules;
	document.getElementById("poulesNumber").value = nbrPoules;
	//On flush le contenant de nous poules
	document.getElementById("poulesDiv").innerHTML = "";
	//On recupere le nombre de paires
	for (var i = 0; i < nbrPoules; i++) {
	    var row;

		if(i%3 == 0){
			row = document.createElement("div")
			row.className = "row"
			document.getElementById("poulesDiv").appendChild(row);
		}
		//Creation du panel de la poule
		var panel = createPanel(i+1);
		row.appendChild(panel)
		//document.getElementById("poulesDiv").appendChild(panel);
	    var listPair = pairDict[(i+1)]
	    var j;
	    for (j=0 ; j < listPair.length ; j++) {
	        var p = createPair(listPair[j])
	        document.getElementById("list"+(i+1)).appendChild(p);

			var nom1 = listPair[j].user1;
			var nom2 = listPair[j].user2;
			document.getElementById("Leader"+(i+1)).appendChild(getOption(nom1));
			document.getElementById("Leader"+(i+1)).appendChild(getOption(nom2));
			document.getElementById("Leader"+(i+1)).appendChild(getSpaceOption());
	    }
	    while (j < sizePoules) {
			var p = createEmptyPair(i+"-"+j);
			document.getElementById("list"+(i+1)).appendChild(p);
			j++;
	    }
	    document.getElementById("Leader"+(i+1)).removeChild(document.getElementById("Leader"+(i+1)).childNodes[document.getElementById("Leader"+(i+1)).childNodes.length-1]);
	}

	setTerrains(nbrPoules);
	for (var i = 0 ; i < terrainSaved.length ; i++) {
	    if (terrainSaved[i].id != '') {
	        setInfoTerrain(terrainSaved[i].user,terrainSaved[i].matiere,terrainSaved[i].type,terrainSaved[i].addr,terrainSaved[i].id,terrainSaved[i].poules,i+1)
	    }
	}
	for (var i = 0 ; i < leaderSaved.length ; i++) {
	    if (leaderSaved[i].fullname != ' ') {
	        document.getElementById("Leader"+(i+1)).value = leaderSaved[i].fullname;
	    }
	}
}

//Fonction utilisée pour set les poules en fonction du nombre de poules
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

		var row;

		if(i%3 == 0){
			row = document.createElement("div")
			row.className = "row"
			document.getElementById("poulesDiv").appendChild(row);
		}
		//Creation du panel de la poule
		var panel = createPanel(i+1);
		row.appendChild(panel)
		//document.getElementById("poulesDiv").appendChild(panel);

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

		}
		document.getElementById("Leader"+(i+1)).removeChild(document.getElementById("Leader"+(i+1)).childNodes[document.getElementById("Leader"+(i+1)).childNodes.length-1]);
		//Si c'est plutot que le nombre max on rajotue des espaces vides
		for (var j = 0; j < max - nbr; j++) {
			var p = createEmptyPair(i+"-"+j);
			document.getElementById("list"+(i+1)).appendChild(p);
		}
	}

	setTerrains(nbrPoules);
}

//fonction utilisé pour set les poules en fonction de la taille des poules
function setPoules2(taillePoule){
	//On flush le contenant de nous poules
	document.getElementById("poulesDiv").innerHTML = "";
	//On recupere le nombre de pair
	var v = pairList.length;
	//on recupere le nombre de poules
	var poules = Math.ceil(PairList.length/taillePoule);
	var nbrPoules = poules
	//il y aura au max 'max' pair par poules
	var max = taillePoule;

	//alert(max);

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

		}
		document.getElementById("Leader"+(i+1)).removeChild(document.getElementById("Leader"+(i+1)).childNodes[document.getElementById("Leader"+(i+1)).childNodes.length-1]);
		//Si c'est plutot que le nombre max on rajotue des espaces vides
		for (var j = 0; j < max - nbr; j++) {
			var p = createEmptyPair(i+"-"+j);
			document.getElementById("list"+(i+1)).appendChild(p);
		}

	}

	setTerrains(nbrPoules);
}



//Update the list of user in the leader list of a panel
function updatePanel(numero, contenu){
	//Panel et liste
	var panel = document.getElementById("list"+numero);
	var list = document.getElementById("Leader"+numero);
	list.innerHTML = "<option disabled selected>"+contenu+"</option>";
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
	}
	list.removeChild(list.childNodes[list.childNodes.length-1]);
}

function getPairbyId(ID){
	for (var i = 0; i < pairList.length; i++) {
		if(pairList[i].id == ID){
			return pairList[i];
		};
	};
}

function getDropDownOption(terrain,id){
	poules = ""
	for (var i = 0; i < terrain.poules.length; i++) {
		poules += terrain.poules[i].id +"/"+terrain.poules[i].tournoi+"/"+terrain.poules[i].jour + "|"
	};
	var li = document.createElement("LI");
	li.innerHTML = 	'<a href="javascript:void(0);" onclick="setInfoTerrain('+"'"+terrain.user+"','"+terrain.matiere+"','"+terrain.type+"','"+terrain.addr+"','"+terrain.id+"','"+poules+"','"+id+"'"+');">['+terrain.id+'] <b>'+terrain.user+'</b> ('+terrain.matiere+')'+'<br>'+
						terrain.addr
					'</a>';

	return li;

}

function setInfoTerrain(user,matiere,type,addr,id,poules,ID){
	document.getElementById("proprio"+ID).innerHTML = user;
	document.getElementById("matiere"+ID).innerHTML = matiere;
	document.getElementById("type"+ID).innerHTML = type;
	document.getElementById("addr"+ID).innerHTML = addr;
	document.getElementById("ID"+ID).innerHTML = id;
	setKm()

	//Si c'est pas un objet on le reconstruit
	var p = [];
	if(typeof(poules)!="object" && poules.length > 0){
		var table = poules.split("|");
		table = table.splice(0,table.length-1);
		for (var i = 0; i < table.length; i++) {
			var t = table[i].split("/")
			p.push({id:t[0],tournoi:t[1],jour:t[2]})
		};
		poules = p
	}


	var p = [];
	for (var i = 0; i < poules.length; i++) {
		//alert(JSON.stringify(poules[i]))
		if(poules[i].jour == jour_tournoi && (nom_tournoi != poules[i].tournoi)) {
			p.push(poules[i])
		}
	};
	poules = p;

	if(poules.length > 0 ){
		var content = "";
		for (var i = 0; i < poules.length; i++) {
			content += poules[i].tournoi + ": " + poules[i].id + "<br>";
		};
		document.getElementById("errorTerrain"+ID).style.display = "inherit";
		document.getElementById("errorTerrain"+ID).setAttribute("data-content",content);
	}else{
		document.getElementById("errorTerrain"+ID).style.display = "none";
	}
}
function setInfoTerrainNoUpdateKm(user,matiere,type,addr,id,poules,ID){
	document.getElementById("proprio"+ID).innerHTML = user;
	document.getElementById("matiere"+ID).innerHTML = matiere;
	document.getElementById("type"+ID).innerHTML = type;
	document.getElementById("addr"+ID).innerHTML = addr;
	document.getElementById("ID"+ID).innerHTML = id;


	//Si c'est pas un objet on le reconstruit
	var p = [];
	if(typeof(poules)!="object" && poules.length > 0){
		var table = poules.split("|");
		table = table.splice(0,table.length-1);
		for (var i = 0; i < table.length; i++) {
			var t = table[i].split("/")
			p.push({id:t[0],tournoi:t[1],jour:t[2]})
		};
		poules = p
	}


	var p = [];
	for (var i = 0; i < poules.length; i++) {
		//alert(JSON.stringify(poules[i]))
		if(poules[i].jour == jour_tournoi && (nom_tournoi != poules[i].tournoi)) {
			p.push(poules[i])
		}
	};
	poules = p;

	if(poules.length > 0 ){
		var content = "";
		for (var i = 0; i < poules.length; i++) {
			content += poules[i].tournoi + ": " + poules[i].id + "<br>";
		};
		document.getElementById("errorTerrain"+ID).style.display = "inherit";
		document.getElementById("errorTerrain"+ID).setAttribute("data-content",content);
	}else{
		document.getElementById("errorTerrain"+ID).style.display = "none";
	}

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
	o.innerHTML = '-';

	return o;
}

//Return le panel d'une poule
function createPanel(number){
	var panel = document.createElement("div");
	panel.className = 'col-lg-4';
	panel.innerHTML = '<div class="panel panel-default" id="panel'+number+'">'+
						'<div class="panel-heading">'+
							'<div class="row">'+
								'<label class="control-label col-xs-4">Poule '+number+'</label>'+
								'<div class="col-xs-8">'+
									'<select class="form-control" name="Leader" id="Leader'+number+'">'+
										'<option disabled selected>Choisir un leader</option>'+
									'</select>'+
								'</div>'+
							'</div>'+
						'</div>'+
						'<div class="list-group" id="list'+number+'">'+
						'</div>'+
						'<div class="panel-footer">'+
							'<hr class="line2">'+
							'<div class="row">'+
								'<div class="col-xs-6">'+
									'<div class="dropdown">'+
			    						'<button class="btn btn-default dropdown-toggle" type="button"  data-toggle="dropdown">Choisir un terrain '+
			    						'<span class="caret"></span></button>'+
										'<ul class="dropdown-menu scrollable-menu" role="menu" id="terrain'+number+'">'+
										'</ul>'+
									'</div>'+
								'</div>'+
								'<div class="col-xs-6">'+
									'<i id="errorTerrain'+number+'" data-toggle="popover" data-html="true" data-placement="top" data-content="lol" class="fa fa-info-circle fa-2x center" style="display:none;cursor:pointer;color:red;width:100%;padding-top:5px;vertical-align:middle" data-original-title="" title=""></i>'+
								'</div>'+
							'</div>'+
							'<div class="row">'+
								'<label class="control-label col-xs-4">ID</label>'+
								'<div class="col-xs-8"><p class="info" style="margin:0;" id="ID'+number+'">-</p></div>'+
							'</div>'+
							'<div class="row">'+
								'<label class="control-label col-xs-4">Propriétaire</label>'+
								'<div class="col-xs-8"><p class="info" style="margin:0;" id="proprio'+number+'">-</p></div>'+
							'</div>'+
							'<div class="row">'+
								'<label class="control-label col-xs-4">Matiere</label>'+
								'<div class="col-xs-8"><p class="info" style="margin:0;" id="matiere'+number+'">-</p></div>'+
							'</div>'+
							'<div class="row">'+
								'<label class="control-label col-xs-4">Type</label>'+
								'<div class="col-xs-8"><p class="info" style="margin:0;" id="type'+number+'">-</p></div>'+
							'</div>'+
							'<div class="row">'+
								'<label class="control-label col-xs-4">Adresse</label>'+
								'<div class="col-xs-8"><p class="info" style="margin:0;" id="addr'+number+'">-<br><br></p></div>'+
							'</div>'+

							'<div class="row">'+
								'<label class="control-label col-xs-4">Kilomètres</label>'+
								'<div class="col-xs-8"><p class="info" id="empreinte'+number+'"> - </p></div>'+
							'</div>'+
						'</div>'+
					'</div>';
    return panel;
}

//Return une pair
function createPair(pair){
	var p = document.createElement("div");

	var gender1 = "";
	var gender2 = "";
	if(pair.titre1=="Mr"){
		gender1 = '<i class="fa fa-male" style="color:blue"></i>';
	}else{
		gender1 = '<i class="fa fa-female" style="color:#ff0066"></i>';
	}
	if(pair.titre2=="Mr"){
		gender2 = '<i class="fa fa-male" style="color:blue"></i>';
	}else{
		gender2 = '<i class="fa fa-female" style="color:#ff0066"></i>';
	}


	var comm = "" ;
	if(pair.comment != ""){
		comm = '<a href="javascript:void(0);" data-toggle="tooltip" data-container="body" data-placement="left" data-html="true" title="'+pair.comment+'" onclick="clickEventPair('+pair.id+')"><b style="color:#222;"><i class="fa fa-file-text-o fa-2x"></i></b></a>';
	}

	p.innerHTML = '<div class="dropBox" ondragover="allowDrop(event)" ondrop="drop(event)" style="padding-left:10px;padding-right:10px;padding-top:3px; padding-bottom:3px;">' +
                        '<div id="'+pair.id+'" draggable="true" ondragstart="drag(event)">'+
                            '<div onclick="clickEventPair('+pair.id+')" id="zone'+pair.id+'" class="zone">'+
                                '<div class="row">'+
                                    '<div class="col-xs-10">'+
                                        '<b style="color:#222">'+gender1+'</b> '+ pair.smallName1 + ' - '+pair.age1+' ans' +
                                        '<br>'+
                                        '<b style="color:#222">'+gender2+'</b> '+ pair.smallName2 + ' - '+pair.age2+' ans' +
                                    '</div>'+
                                    '<div class="col-xs-2">'+comm+
                                    '</div>'+
                                '</div>'+
                            '</div>'+
                        '</div>'+
                    '</div>';

	return p;
}

//return une pair vide
function createEmptyPair(i){
	var p = document.createElement("div");
	var bidonID = "bidon"+i;
	p.innerHTML='<div class="dropBox" ondragover="allowDrop(event)" ondrop="drop(event)" style="padding-left:10px;padding-right:10px;padding-top:3px; padding-bottom:3px;"><div id="bidon'+i+'" draggable="true" ondragstart="drag(event)"><div onclick="clickEventPair('+"'bidon"+i+"'"+')" id="zonebidon'+i+'" class="zone"><div class="row"><div class="col-xs-10"><br><br></div><div class="col-xs-2"></div></div></div></div></div>';
	return p;
}

var selected = false;
var selected_id = -1;

function clickEventPair(ID){
	var elem = document.getElementById("zone"+ID)
	if(elem.className.indexOf("clicked")>-1){
		elem.className = "zone"
		selected = false;
		selected_id = -1
	}else{
		if(selected){
			// il faut swap ID et selected_id
			var node1 = document.getElementById("zone"+selected_id)
			var node2 = document.getElementById("zone"+ID)
			var Parent1 = node1.parentNode.parentNode;
			var Parent2 = node2.parentNode.parentNode;

			var targetID = ('' + node1.parentNode.parentNode.parentNode.parentNode.parentNode.id).replace('panel', '');
			var sourceID = ('' + node2.parentNode.parentNode.parentNode.parentNode.parentNode.id).replace('panel', '');

			temp = Parent1.innerHTML

			Parent1.innerHTML = node2.parentNode.parentNode.innerHTML;
			Parent2.innerHTML = temp;

			document.getElementById("zone"+selected_id).className = "zone"
			selected = false;

			//update leader liste
			updatePanel(targetID, "Choisir un leader");
			updatePanel(sourceID, "Choisir un leader");

			setKm();
			leaderAssignement();



		}else{
			selected = true;
			selected_id = ID;
			elem.className = "zone-clicked"
		}

	}
}

$(document).ready(function(){
    $('[data-toggle="tooltip"]').tooltip(); 
});
