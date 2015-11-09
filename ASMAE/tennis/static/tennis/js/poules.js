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

