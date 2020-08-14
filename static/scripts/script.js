var tableAlly = document.getElementById("ally"), rIndex, cIndex;
var tableEnemy = document.getElementById("enemy");
var allBattleshipsPlaced = false;
var gameOver = false;
var messageShown = false;
var steps = 0;

function placeBattleship() {
	req = $.ajax({
		url: '/#', 
		type: 'POST', 
		data: { row: "DONE", column: "DONE" } 
	});

	req.done(function(data){

		var cellsToTransform = $("td").filter(function(){
			return $(this).css("background-color") === "rgb(255, 255, 255)";
		});
		if (data.result == "success"){
			cellsToTransform.css("background-color", "rgb(1, 50, 44)");
			cellsToTransform.css("border", "2px solid white");
			if (cellsToTransform.length == 2){
				cellsToTransform.html("D");
			}
			else if (cellsToTransform.length == 3){
				cellsToTransform.html("C");
			}
			else{
				cellsToTransform.html("B");
			}

			if (data.message == "all battleship placed"){
				$(".placeBattleship").hide();
				$(".cellAlly").css("cursor", "context-menu");
				$(".cellEnemy").css("cursor", "pointer");

				allBattleshipsPlaced = true;

				var cellsAlly = $(".cellAlly").filter(function(){
					return $(this).css("background-color") != "rgb(1, 50, 44)";
				});
			}
		}
		else{
			cellsToTransform.css("background-color", "transparent");
			cellsToTransform.css("border", "2px solid white");
		}
	});
}

function allyTableHandler(){
	for (var i = 0; i < tableAlly.rows.length; i++){
		for (var j = 0; j < tableAlly.rows[i].cells.length; j++){
			tableAlly.rows[i].cells[j].onclick = function(){
				if (allBattleshipsPlaced == false){
					var cell = this;
					rIndex = cell.parentElement.rowIndex;
					cIndex = cell.cellIndex;
					//console.log(rIndex, cIndex);

					req = $.ajax({
						url: '/#', 
						type: 'POST', 
						data: { row: rIndex, column: cIndex } 
					});

					req.done(function(data){
						//console.log(data.result, ":", data.message);
						if (data.result == "success"){
							if (data.message == "appended to current battleship"){
								$(cell).css("background-color", "white");
								$(cell).css("border", "3px solid black");
							}
							else{
								$(cell).css("background-color", "transparent");
								$(cell).css("border", "2px solid white");
							}
						}
					});
				}
			};
		}
	}
}

function enemyTableHandler(){
	for (var i = 0; i < tableEnemy.rows.length; i++){
		for (var j = 0; j < tableEnemy.rows[i].cells.length; j++){
			tableEnemy.rows[i].cells[j].onclick = function(){
				if (allBattleshipsPlaced == true && gameOver == false){
					var cell = this;
					rIndex = cell.parentElement.rowIndex;
					cIndex = cell.cellIndex;
					//console.log(rIndex, cIndex);

					req = $.ajax({
						url: '/#', 
						type: 'POST', 
						data: { row: rIndex, column: cIndex } 
					});

					req.done(function(data){
						//console.log(data.result, ":", data.message, "->", data.computer_hit, "==>", data.game_ended);
						if (data.result == "failure")
							return;
						steps++;
						if (data.result == "hit"){
							$(cell).css("background-color", "rgb(45, 0, 0)");
						}
						else if (data.result == "not hit"){
							$(cell).css("background-color", "white");
						}
						if (data.message == "human wins"){
							$(".cellEnemy").css("cursor", "context-menu");
							gameOver = true;
							setTimeout(function(){
								toggleWonGame();
							}, 100);
							return;
						}


						if (data.computer_hit == "yes"){
							$("#ally"+data.message).html("");
							$("#ally"+data.message).css("background-color", "rgb(45, 0, 0)");
						}
						else {
							$("#ally"+data.message).css("background-color", "white");
						}
						if (data.game_ended == "computer wins"){
							$(".cellEnemy").css("cursor", "context-menu");
							gameOver = true;
							setTimeout(function(){
								toggleLostGame();
							}, 100);
							return;
						}
					});
				}
			};
		}
	}	
}

function resetGame(){
	$(".cellAlly").css("background-color", "transparent");
	$(".cellAlly").css("border", "2px solid white");
	$(".cellAlly").css("cursor", "pointer");
	$(".cellAlly").html("");

	$(".cellEnemy").css("background-color", "transparent");
	$(".cellEnemy").css("border", "2px solid white");

	$(".placeBattleship").show();
	allBattleshipsPlaced = false;
	gameOver = false;
	steps = 0;
}

allyTableHandler();
enemyTableHandler();

function toggleGameRules(){
	document.getElementById("popup-1").classList.toggle("active");
}

function toggleHighScores(){
	document.getElementById("popup-2").classList.toggle("active");
}

function toggleWonGame(){
	document.getElementById("popup-3").classList.toggle("active");
	toggleMessage();
}

function toggleLostGame(){
	document.getElementById("popup-4").classList.toggle("active");
	
	req = $.ajax({
		url: '/#', 
		type: 'POST', 
		data: { over : "YES" } 
		});

	req.done(function(data){
		while(data.remaining.length){
			let element = data.remaining.shift()
			$("#enemy"+element).css("background-color", "rgb(205, 92, 92)");
			#console.log(element);
		}
	});
}

function toggleMessage(){
	if (messageShown == false){
		//console.log(steps);
		document.getElementById("steps").innerHTML = "Game Over! You won! You defeated the entire enemy fleet in " + steps + " moves!";
		messageShown = true;
	}
	else{
		document.getElementById("steps").innerHTML = "";
		messageShown = false;
	}
}

window.onload = resizer;

window.addEventListener("resize", resizer);

function resizer(){
	if ($(window).width() >= 1125) {
        $("body").css("background-size", "100vw 100vh");
        $(".ally").css("margin-right", "2%");
    } 
    else {
        $("body").css("background-size", "cover");
        $(".ally").css("margin-right", "0");
    }
}