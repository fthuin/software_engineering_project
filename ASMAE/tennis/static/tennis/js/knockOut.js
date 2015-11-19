//utilisé pour le drag and drop
function sendTree()
{
document.getElementById("treeData").value = JSON.stringify(TreeData);
document.getElementById("treeLabel").value = JSON.stringify(TreeLabel);
document.getElementById("gagnant").value = getGagnant();
document.getElementById("finaliste").value = getFinaliste();

}
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

  var ID1 = src.id;
  var ID2 = tgt.id;

  if(ID1 != ID2){
    swapPair(ID1,ID2);
  }

  //TODO update list leftList et rightList a chaque drop
}

function allowDrop(ev) {
    ev.preventDefault();
}

//Donnée de notre arbre
var TreeData;

//label
var TreeLabel;

//Function utilisé avec le modal pour set un score
function setScore(){
  //recuperation des scores
  var score1 = document.getElementById("inputTeam1").value;
  var score2 = document.getElementById("inputTeam2").value;

  if(parseInt(score1)>=0 && parseInt(score2)>=0 && parseInt(score1)!=parseInt(score2)){

    //recuperation de l'emplacement des teams
    var empl = document.getElementById("emplacement").value;
    var round = empl.split("-")[0];
    var place = empl.split("-")[1];

    //team1
    TreeData[round][place][0].score = parseInt(score1);
    var name1 = TreeData[round][place][0].name;
    var ID1 = TreeData[round][place][0].id;

    //team2
    TreeData[round][place][1].score = parseInt(score2);
    var name2 = TreeData[round][place][1].name;
    var ID2 = TreeData[round][place][1].id;

    //Team qui passe 
    //emplacement
    var offset = place%2;
    var newPlace = Math.floor(place/2);
    var newRound = parseInt(round)+1;

    //nom et ID du gagant
    var name = "";
    var ID = 0;
    if(parseInt(score2)>parseInt(score1)){
      name = name2;
      ID = ID2.split(" ")[1];
    }else{
      name = name1;
      ID = ID1.split(" ")[1];
    }

    //set team
    TreeData[newRound][newPlace][offset].name = name;
    TreeData[newRound][newPlace][offset].id = TreeData[newRound][newPlace][offset].id.split(" ")[0] + " "+ID;

    $('#scoreModal').modal('hide');

    setArbre(TreeData,TreeLabel)

  }else{
    document.getElementById("hintScore").innerHTML = "Attention, les deux scores doivent être différents et positifs"
  }
}

//Function utilisé pour show un modal pour set un score
function showScore(id){

  var round = id.split("-")[0];
  var place = id.split("-")[1];

  var Team1 = TreeData[round][place][0].name;
  var Team2 = TreeData[round][place][1].name;

  //n'affiche rien si il n'y a pas deux equipe
  if(Team1=="<br />" || Team2=="<br />"){
    return;
  }

  //emplacement des teams
  document.getElementById("emplacement").value = round+"-"+place;

  //reset des input 
  document.getElementById("inputTeam1").value = "";
  document.getElementById("inputTeam2").value = "";
  document.getElementById("hintScore").innerHTML = "";

  //Affichage des deux équipe
  document.getElementById("formteam1").innerHTML = Team1.replace("<br />"," &#38; ");
  document.getElementById("formteam2").innerHTML = Team2.replace("<br />"," &#38; ");

  $('#scoreModal').modal('show'); 
  
}

//Permet de dessiner l'arbre avec les infos reprises dans data et les labels dans label
function setArbre(data,label){
  //Set element height in order not to need to scroll down after set score
  document.getElementById("my_gracket").style.minHeight = document.getElementById("my_gracket").offsetHeight+"px";
  document.getElementById("my_gracket").innerHTML = "";
  
  //set arbre reading the json data
  (function(win, doc, $){

    $("#my_gracket").gracket({ 
      src : data,
      canvasLineWidth : 2,      // adjusts the thickness of a line
      canvasLineGap : 10,        // adjusts the gap between element and line
      canvasLineCap : "round",  // or "square"
      canvasLineColor : "#D4542D", // or #HEX
      roundLabels : label,
      funct: showScore
    });

  })(window, document, jQuery);
}

//set un arbre de knock out
//La liste 1 sont les joueur 1 (taille == 1 2 4 ou 8)
//la liste 2 sont les joueurs 2
//MAx length 16
function setTree(listPair1, listPair2){
  //Length
  var length = listPair1.length + listPair2.length;
  var size = 0;

  //Length limit is 16 => if more error and tree is set to 0
  if(length>16){
    size = 0;
  }else if(length > 8){
    size = 4
  }else if(length > 4){
    size = 3
  }else if(length > 2){
    size = 2
  }else if(length > 0){
    size = 1
  }


  //Calcul pour voir ou placer la liste deux
  var round1Length = Math.pow(2,size);

  var offset = Math.floor(listPair2.length/2);

  var initial = Math.floor((round1Length/4) - offset);

  //liste des labels
  var l = [];
  //Data contenant notre arbre
  var jsonArbre = [];
  //utilise pour donner des id uniques
  var count = 0;

  //Parcours de la taille de l'arbre
  for (var i = 0; i < size ; i++) {
    //Json du round
    var jsonRound = [];
    //Nombre d'entrée par rounds
    var nbr = Math.pow(2,(size-i));

    //Mise à jours des labels
    if(nbr==2){
      l.push("Finale");
    }else{
      l.push("1/"+nbr/2+" finale");
    };
    
    //Ajouts des paires vide
    for (var j = 0; j < nbr/2; j++) {

      var name1 = "<br />";
      var pairID1 = count;
      //Si premier round et il faut ajouter un nom
      if(i == 0){
        name1 = listPair1[j].user1 + "<br />&nbsp;" + listPair1[j].user2 ;
        pairID1 = listPair1[j].id;
      }

      var jsonDuel = [];
      jsonDuel.push({
        name: name1,
        id: i+"-"+j+"-"+count+" "+pairID1
      })

      count = count + 1;

      var name2 = "<br />";
      var pairID2 = count;
      if(i == 0 && j>= initial && (j-initial)<listPair2.length){
        name2 = listPair2[j-initial].user1 + "<br />&nbsp;" + listPair2[j-initial].user2;
        pairID2 = listPair2[j-initial].id;
      }

      jsonDuel.push({
        name: name2,
        id: i+"-"+j+"-"+count+" "+pairID2
      })
      jsonRound.push(jsonDuel);
      count = count + 1;
    };

    jsonArbre.push(jsonRound);
  };

  //Dernier round (gagnant)
  var jsonLastRound = [];
  var jsonWinner = [];
  jsonWinner.push({
        name: "<br />",
        id: "gagnant"
  })
  jsonLastRound.push(jsonWinner);
  jsonArbre.push(jsonLastRound);

  //Update label
  l.push("Gagnant");

  //TODO resolve single pair
  jsonArbre = resolveSingle(jsonArbre);

  //Enregistremetn des labels
  TreeLabel = l;

  //Enregistrement de l'arbre
  TreeData = jsonArbre;

  //On afficher l'arbre 
  setArbre(jsonArbre,l)
}

function resolveSingle(jsonArbre){

  for (var i = 0; i < jsonArbre[0].length; i++) {
    var name1 = jsonArbre[0][i][0].name;
    var ID1 = jsonArbre[0][i][0].id;
    var name2 = jsonArbre[0][i][1].name;
    var ID2 = jsonArbre[0][i][0].id;

    if(name1 != name2 && (name1=="<br />" || name2=="<br />")){
      //conflict
      var offset = i%2;
      var place = Math.floor(i/2);
      var name = "";
      var ID = 0;
      if(name1=="<br />"){
        name = name2;
        ID = ID2.split(" ")[1];
      }else{
        name = name1;
        ID = ID1.split(" ")[1];
      }
      jsonArbre[1][place][offset].name = name;
      jsonArbre[1][place][offset].id = jsonArbre[1][place][offset].id.split(" ")[0] + " "+ID;
    }
  };

  return jsonArbre;
}

function checkBox(id){
  var input = "ID"+id;
  var check = "check"+id;
  //pour decheck => c'est bon
  if(document.getElementById(input).checked){
    document.getElementById(input).checked = !document.getElementById(input).checked;
    document.getElementById(check).className = "glyphicon glyphicon-unchecked";
  }else{
    //Check if we don't exceed 16
    var allBoxes = document.getElementsByClassName("allBox");
    var count = 0;
    for (var i = 0; i < allBoxes.length; i++) {
      if(allBoxes[i].checked){
        count += 1;
      }
    };
    if (count > 15){
      //Error
      //TODO afficher qu'on ne peut avoir que maximum 16 paires selectionner sur autre chose que alert
      alert("Vous ne pouvez selectionner que 16 paires maximum.")
    }else{
      document.getElementById(input).checked = !document.getElementById(input).checked;
      document.getElementById(check).className = "glyphicon glyphicon-check";
    }
  }
}

function firstModal(){
  //On compte le nombre de paires selectionnées
  var allBoxes = document.getElementsByClassName("allBox");
    var count = 0;""
    for (var i = 0; i < allBoxes.length; i++) {
      if(allBoxes[i].checked){
        count += 1;
      }
    };

  //Si il y a moins que deux paires on affiche
  if(count < 2){
    document.getElementById("msgFirstModal").innerHTML = "Veuillez selectionner au moins 2 paires."
    document.getElementById("buttonFirstModal").disabled = true;
  }else{
    //On affiche le nombre de paires selectionnées
    document.getElementById("msgFirstModal").innerHTML = "Continuer avec ces "+count+" paires selectionnées?"
    document.getElementById("buttonFirstModal").disabled = false;
  }

  

  //On montre le modal
  $('#firstModal').modal('show');
}

//TODO removes ces listes?
var leftList = [];
var righList = [];

function swapPair(id1,id2){
  var Pair1;
  var Pair2;

  var list1 = 0;
  var emplacement1 = -1;

  var list2 = 0;
  var emplacement2 = -1;



  for (var i = 0; i < leftList.length; i++) {
    if(leftList[i].id == id1){
      Pair1 = leftList[i];
      list1 = 1;
      emplacement1 = i;
    }
    if(leftList[i].id == id2){
      Pair2 = leftList[i];
      list2 = 1;
      emplacement2 = i;
    }
  };
  for (var i = 0; i < righList.length; i++) {
    if(righList[i].id == id1){
      Pair1 = righList[i];
      list1 = 2;
      emplacement1 = i;
    }
    if(righList[i].id == id2){
      Pair2 = righList[i];
      list2 = 2;
      emplacement2 = i;
    }
  };

  if(list1 == 1){
    leftList[emplacement1] = Pair2;
  }else{
    righList[emplacement1] = Pair2;
  }

  if(list2 == 1){
    leftList[emplacement2] = Pair1;
  }else{
    righList[emplacement2] = Pair1;
  }



}

function secondStep(){
  //On retire l'affichage du premier step
  document.getElementById("firstStep").style.display = "none";
  //On affiche le deuxieme step
  document.getElementById("secondStep").style.display = "inherit";
  //on change le titre de la page
  document.getElementById("pageTitle").innerHTML = "Ordre des paires";

  //On stock les paires dans le panel du deuxieme step
  var allBoxes = document.getElementsByClassName("allBox");
  var challengers = [];
  for (var i = 0; i < allBoxes.length; i++) {
    if(allBoxes[i].checked){
      var ID = parseInt(allBoxes[i].name);
      var paire = allPaires[ID];
      challengers.push(paire);
    }
  };

  var length = challengers.length;

  if(length>16){
    size = 0;
  }else if(length > 8){
    size = 4;
  }else if(length > 4){
    size = 3;
  }else if(length > 2){
    size = 2;
  }else if(length > 0){
    size = 1;
  }

  challengers.sort(function(a, b) { 
  var r = a.pos - b.pos;
  return r;
});

  var RoundSize = Math.pow(2,size)/2;
  var leftSide = challengers.splice(0,RoundSize);

  var offset = Math.floor(challengers.length/2);

  var initial = Math.floor((RoundSize/2) - offset);

  leftList = leftSide;
  righList = challengers;


  for (var i = 0; i < leftSide.length; i++) {
    var nom = leftSide[i].user1 +'<p class="pull-right" style="margin:0">Position : '+leftSide[i].pos+'</p>'+ "<br>" + leftSide[i].user2 +'<p class="pull-right" style="margin:0">Poule : '+leftSide[i].poule+'</p>';

    if(i>= initial && i-initial<challengers.length){
      var nom2 = challengers[i-initial].user1 +'<p class="pull-right" style="margin:0">Position : '+challengers[i-initial].pos+'</p>'+ "<br>" + challengers[i-initial].user2 +'<p class="pull-right" style="margin:0">Poule : '+challengers[i-initial].poule+'</p>';
      document.getElementById("firstRoundBody").innerHTML += getVersus(nom,nom2,leftSide[i].id,challengers[i-initial].id);
    }else{
      document.getElementById("firstRoundBody").innerHTML += getSingle(nom,leftSide[i].id);
    }
  }


  //On retire le modal de l'ecran
  $('#firstModal').modal('hide');
}

//Return an html composant used in the first round panel
function getVersus(name1,name2,ID1,ID2){
  var versus = '<div class="row">'+
                  '<div class="col-sm-6">'+
                    '<div class="dropBox" ondragover="allowDrop(event)" ondrop="drop(event)" style="padding-left:10px;padding-right:10px;padding-top:3px; padding-bottom:3px;">'+
                      '<div id="'+ID1+'" draggable="true" ondragstart="drag(event)">'+
                        '<div class="zone">'+
                          name1+
                        '</div>'+
                      '</div>'+
                    '</div>'+
                  '</div>'+
                  '<div class="col-sm-6">'+
                    '<div class="dropBox" ondragover="allowDrop(event)" ondrop="drop(event)" style="padding-left:10px;padding-right:10px;padding-top:3px; padding-bottom:3px;">'+
                      '<div id="'+ID2+'" draggable="true" ondragstart="drag(event)">'+
                        '<div class="zone">'+
                          name2+
                        '</div>'+
                      '</div>'+
                    '</div>'+
                  '</div>'+
                '</div>';
  return versus;
}

function getSingle(name,ID){
  var single = '<div class="row">'+
                  '<div class="col-sm-3"></div>'+
                  '<div class="col-sm-6">'+
                    '<div class="dropBox" ondragover="allowDrop(event)" ondrop="drop(event)" style="padding-left:10px;padding-right:10px;padding-top:3px; padding-bottom:3px;">'+
                      '<div id="'+ID+'" draggable="true" ondragstart="drag(event)">'+
                        '<div class="zone">'+
                          name+
                        '</div>'+
                      '</div>'+
                    '</div>'+
                  '</div>'+
                  '<div class="col-sm-3"></div>'+
                '</div>';
  return single;
}


function startTree(){
  document.getElementById("secondStep").style.display = "none";
  document.getElementById("TableArbre").style.display = "inherit";
  document.getElementById("pageTitle").innerHTML = "Arbre du tournoi";
  setTree(leftList,righList);
}


//Return l'id de la pair Gagnante si il y en a une
function getGagnant(){
  var length = TreeData.length
  var Gagnant = "";
  if(TreeData[length-1][0][0].id.indexOf("pair")>-1){
    Gagnant = TreeData[length-1][0][0].id.split("pair")[1]
  }
  return Gagnant;
}

//Return l'id des finaliste de facon ID1-ID2
function getFinaliste(){
  var length = TreeData.length
  var Finaliste = "";
  if(TreeData[length-2][0][0].id.indexOf("pair")>-1 && TreeData[length-2][0][1].id.indexOf("pair")>-1){
    Finaliste = TreeData[length-2][0][0].id.split("pair")[1]+"-"+TreeData[length-2][0][1].id.split("pair")[1];
  }
  return Finaliste;
}

