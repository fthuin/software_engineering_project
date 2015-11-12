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