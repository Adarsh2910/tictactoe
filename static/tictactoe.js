// -Author- : Adarsh

var button = [];
var disabledButtonsCount = [];
var ctx = [];
var currentPlayer;
var moveId = '0';
var xDrawer;
var content = [];
var reload;

$(function() {

	for (var i = 1; i < 10; i++) {
		button[i]= document.getElementById('box'+i);
	}

	for (var i = 1; i < 10; i++) {
		ctx[i]=button[i].getContext('2d');
	}

	for (var i = 1; i < 10; i++) {
		document.getElementById("box"+i).style.pointerEvents = "none";
	}

	$('#reload').click(function() {
		setTimeout(reset,500);
	})

	$("#firstP").click(function() {
		firstMove('Human');
		$("#choose").hide();
	});

	$("#secondP").click(function() {
		firstMove('Computer');
		$("#choose").hide();
	});
});


function reset() {
	for (var i = 1; i < 10; i++) {
		document.getElementById("box"+i).style.pointerEvents = "none";
		disabledButtonsCount[i]= false;
		ctx[i].clearRect(0,0,96,96);
		button[i].style.opacity = 1.0;
		button[i].style.Transform = "rotateY(0deg)";
		button[i].style.webkitTransform = "rotateY(0deg)";
		button[i].style.msTransform = "rotateY(0deg)";
		button[i].style.mozTransform = "rotateY(0deg)";
		button[i].style.oTransform = "rotateY(0deg)";
		document.getElementById("box"+i).style.animation = "";
	}

	document.getElementById('firstP').innerHTML = "Player";
	document.getElementById('secondP').innerHTML = "Computer";
	$("#firstP").attr("style","background-color: #337ab7 !important;");
	$("#secondP").attr("style","background-color: #337ab7 !important;");

	$("#firstP").hover(function() { 
		$(this).css("background-color", "#3cb0fd");
	}, function() {
		$(this).css("background-color", "#337ab7");
    });

	$("#secondP").hover(function() {
		$(this).css("background-color", "#3cb0fd");
	}, function() {
    	$(this).css("background-color", "#337ab7");
    });

	$("#choose").show();

	$("#firstP").attr('disabled', false);
	$("#secondP").attr('disabled', false);
	content = [];
	moveId='0';
}


function togglePlayer() {
	
	currentPlayer = (currentPlayer=='Human')?'Computer':'Human';


	setTimeout(function() {
		if(currentPlayer=='Human') {
		$("#firstP").attr("style","background-color: #d9534f");
		$("#secondP").attr("style","background-color: #337ab7");
	}
	else {
		$("#secondP").attr("style","background-color: #d9534f");
		$("#firstP").attr("style","background-color: #337ab7");
	}
	},300);

	if(moveId.length==10) {
		$("#secondP").attr("style","background-color: #337ab7");
		$("#firstP").attr("style","background-color: #337ab7");	
	}

	for (var i = 1; i < 10; i++){ //enables button after move
		var usedBox = moveId.search(i);
		if(usedBox=='-1')
			document.getElementById("box"+i).style.pointerEvents = "auto";
	}

}

function moveX(move) {
	moveId += move.toString();

	animateButton(move);
	setTimeout(function() {
			ctx[move].lineWidth = 3;
	 		ctx[move].beginPath();
	 		ctx[move].moveTo(19,19);
	 		ctx[move].lineTo(80,80);
	 		ctx[move].moveTo(80,19);
	 		ctx[move].lineTo(19,80);
	 		ctx[move].stroke();
	 		ctx[move].closePath();
	},300);
}


function moveO(move) {
	moveId += move.toString();

	animateButton(move);
	setTimeout(function() {
			ctx[move].lineWidth = 3;
			ctx[move].beginPath();
			ctx[move].arc(48,48,32,0,2*Math.PI);
			ctx[move].stroke();
			ctx[move].closePath();
		},300);
}


function checkWinner() {
	if(content[1]==content[2]&&content[2]==content[3]) {
		if(content[1]!=undefined) {
			return '123';
		}
	}
	if(content[4]==content[5]&&content[5]==content[6]) {
		if(content[4]!=undefined) {
			return '456';
		}
	}
	if(content[7]==content[8]&&content[8]==content[9]) {
		if(content[7]!=undefined) {
			return '789';
		}
	}
	if(content[1]==content[4]&&content[4]==content[7]) {
		if(content[1]!=undefined) {	
			return '147';
		}
	}
	if(content[2]==content[5]&&content[5]==content[8]) {
		if(content[2]!=undefined) {	
			return '258';
		}
	}
	if(content[3]==content[6]&&content[6]==content[9]) {
		if(content[3]!=undefined) {	
			return '369';
		}
	}
	if(content[1]==content[5]&&content[5]==content[9]) {
		if(content[1]!=undefined) {	
			return '159';
		}
	}
	if(content[3]==content[5]&&content[5]==content[7]) {
		if(content[3]!=undefined){
			return '357';
		}
	}

	return 0;
}

function flashWinner(winString) {
	document.getElementById("box"+winString.charAt(0)).style.animation = "flash 1.5s infinite";
	document.getElementById("box"+winString.charAt(1)).style.animation = "flash 1.5s infinite";
	document.getElementById("box"+winString.charAt(2)).style.animation = "flash 1.5s infinite";
}

function playerMove(move) {
	content[move] = currentPlayer;
	if(xDrawer==currentPlayer) {
		moveX(move);
	}
	else {
		moveO(move);
	}
	
	var winString = checkWinner();

	if(winString!=0){
		flashWinner(winString);
		for(var i = 1; i < 10; i++){
			document.getElementById("box"+i).style.pointerEvents = "none";
		}
	}
	else
		togglePlayer();
}


function computerMove() {

	$.ajax({
		url: "get_optimal_move?move_id="+moveId,
		success: function(data) {
			json = JSON.parse(data);
			var move = json.move;
			console.log(move);
			document.getElementById("box"+move).style.pointerEvents = "auto";	

			content[move] = currentPlayer;


			if(xDrawer==currentPlayer) {
				moveX(move);
			}
			else{
				moveO(move);
			}

			var winString = checkWinner();

			if(winString!=0) {
				flashWinner(winString);
				for(var i = 1; i<10; i++){
					document.getElementById("box"+i).style.pointerEvents = "none";
				}
			}
			else
				togglePlayer();
		}
	});
}


function animateButton(move) {
	if(!disabledButtonsCount[move]){
		disabledButtonsCount[move]=true;
		document.getElementById("box"+move).style.pointerEvents = "none";//disable buttons
		button[move].style.opacity = 0.7;
		button[move].style.Transform = "rotateY(180deg)";
		button[move].style.webkitTransform = "rotateY(180deg)";
		button[move].style.msTransform = "rotateY(180deg)";
		button[move].style.mozTransform = "rotateY(180deg)";
		button[move].style.oTransform = "rotateY(180deg)";
	}
}


function onButtonClick(move){
	playerMove(move);
	console.log(moveId);

	for (var i = 1; i < 10; i++) { //disable button after player move
		if(i!=move)
			document.getElementById("box"+i).style.pointerEvents = "none";
	}

	setTimeout(computerMove, 300);
}


function firstMove(player){
	reset();
	currentPlayer = player;
	xDrawer = player;

	if(currentPlayer == 'Human'){
		for (var i = 1; i < 10; i++){
			document.getElementById("box"+i).style.pointerEvents = "auto";
		}
		document.getElementById("firstP").innerHTML = "Player : X";
		document.getElementById("secondP").innerHTML = "Computer : O";
		$("#firstP").attr('disabled', true);
		$("#secondP").attr('disabled', true);
		$("#firstP").attr("style","background-color: #d9534f !important;");
		$("#secondP").attr("style","background-color: #337ab7 !important;");
	}

	if(currentPlayer == 'Computer') {
		document.getElementById("firstP").innerHTML = "Player : O"
		document.getElementById("secondP").innerHTML = "Computer : X"
		$("#firstP").attr('disabled', true);
		$("#secondP").attr('disabled', true);
		$("#secondP").attr("style","background-color: #d9534f !important;");
		$("#firstP").attr("style","background-color: #337ab7 !important;");

		setTimeout(computerMove, 300);
	}
}
