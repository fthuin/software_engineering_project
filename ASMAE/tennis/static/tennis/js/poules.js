function drag (ev) {
  ev.dataTransfer.setData("src", ev.target.id);
}

function drop (ev) {
  ev.preventDefault();
  var src = document.getElementById(ev.dataTransfer.getData("src"));
  var srcParent = src.parentNode;
  var tgt = ev.currentTarget.firstElementChild;

  ev.currentTarget.replaceChild(src, tgt);
  srcParent.appendChild(tgt);
}

function allowDrop(ev) {
    ev.preventDefault();
}

$(document).ready(function(){
    $('[data-toggle="popover"]').popover();   
});



var pairList;

function setPairList(pairL){
	pairList = pairL;
}

function setPoules(nbrPoules){
	document.getElementById("poulesDiv").innerHTML = "";
	var v = pairList.length;
	var poules = nbrPoules;
	var max = Math.ceil(v/poules);
	var count = 0;
	for (var i = 0; i < nbrPoules; i++) {
		var nbr = Math.ceil(v/poules);
		v = v - nbr;
		poules = poules - 1;
		var panel = createPanel(i+1);
		document.getElementById("poulesDiv").appendChild(panel);


		for (var j = 0; j < nbr; j++) {
			var p = createPair(pairList[count]);
			count = count + 1;
			document.getElementById("list"+(i+1)).appendChild(p);


		};
		for (var j = 0; j < max - nbr; j++) {
			var p = createEmptyPair(i);
			document.getElementById("list"+(i+1)).appendChild(p);
		};
		
	};
}


function createPanel(number){
	var panel = document.createElement("div");
	panel.className = 'col-lg-4';
	panel.innerHTML = '<div class="panel panel-default"><div class="panel-heading"><div class="row"><label class="control-label col-xs-4">Poule '+number+'</label><div class="col-xs-8"><select class="form-control" name="Leader" id="Leader'+number+'"><option disabled selected>Choisir un leader</option></select></div></div></div><div class="list-group" id="list'+number+'"></div></div>';
    return panel;
}

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

	
	var comm ;
	if(pair.comment != ""){
		comm = document.createElement("div");
		comm.innerHTML = '<a href="javascript:void(0);" data-toggle="popover" data-html="true" data-placement="left" data-content="'+pair.comment+'"><b style="color:#222;"><i class="fa fa-file-text-o fa-2x"></i></b></a>';
	}
	
	p.innerHTML = '<div class="dropBox" ondragover="allowDrop(event)" ondrop="drop(event)" style="padding-left:10px;padding-right:10px;padding-top:3px; padding-bottom:3px;"><div id="'+pair.id+'" draggable="true" ondragstart="drag(event)"><div class="zone"><div class="row"><div class="col-xs-10"><b style="color:#222"><i class="'+gender1+'"></i></b> '+pair.user1+'('+pair.age1+')'+'<br><b style="color:#222"><i class="'+gender2+'"></i></b> '+pair.user2+'('+pair.age2+')'+'</div><div class="col-xs-2"></div></div></div></div></div>';

	return p;
}

function createEmptyPair(i){
	var p = document.createElement("div");
	p.innerHTML='<div class="dropBox" ondragover="allowDrop(event)" ondrop="drop(event)" style="padding-left:10px;padding-right:10px;padding-top:3px; padding-bottom:3px;"><div id="bidon'+i+'" draggable="true" ondragstart="drag(event)"><div class="zone"><div class="row"><div class="col-xs-10"><br><br></div><div class="col-xs-2"></div></div></div></div></div>';
	return p;
}






