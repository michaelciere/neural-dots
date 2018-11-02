var player = 0;
var player_to_move = 0;
var moves_played = new Set();
var comp = true;
var comp_seconds = 0
var started = false;

var scores = [0,0];
var last_move;

$(document).ready(function() {
    
    $('p#tomove').hide();
    $('p#score').hide();
    $('p#start').show();

    $('#start-form').submit( function(e) {
	e.preventDefault();
	$('p#tomove').show();
	$('p#score').show();
	$('.start-screen').hide();
	// check which player was selected
	player = parseInt($('input[name=player]:checked').val());

	started = true;

	startGame();
	
    	return false;

    });
    
    $(document).on('click', 'rect.line', lineClick);
        
    $('p#tomove').text("Player " + player_to_move + " to move")
    
    
});


function compTimePlus(){
    comp_seconds++;
    document.getElementById("count").value = comp_seconds;
}

function compTimeMinus(){
    if (comp_seconds > 0) {
	comp_seconds--;
	document.getElementById("count").value = comp_seconds;
    }
}

function startGame() {

    comp_seconds = document.getElementById("count").value;
    if (player == 1 && comp == true) {
	playCompMove();
    }
    
};

function squareLines(x,y) {
    lines = [[x, y, x+1, y],
     [x, y, x, y+1],
     [x, y+1, x+1, y+1],
     [x+1, y, x+1, y+1]];
    lines2 = ['','','','']
    $.each(lines, function(i, arr) {
        lines2[i] = arr.join('') });
    return(lines2)
}

function capturedSquares(move) {
    coords = move.split("")
    coords = $.each(coords, function(i,val) {
        coords[i] = parseInt(val)});
    x1 = coords[0]
    y1 = coords[1]
    x2 = coords[2]
    y2 = coords[3]

    if (y1 == y2) {
        // horizontal move
        box1 = squareLines(x1,y1);
        box2 = squareLines(x1, y1-1);
        box1_captured = true
        box2_captured = true
        $.each(box1, function(i, line) {
            if (!(moves_played.has(line))) {
                box1_captured = false
            }
        });
        $.each(box2, function(i, line) {
            if (!(moves_played.has(line))) {
                box2_captured = false
            }
        });
        boxes = [];
        if (box1_captured) {
            str = "" + x1 + "" + y1;
            boxes.push(str);
        }
        if (box2_captured) {
            str = "" + x1 + "" + (y2-1);
            boxes.push(str)
        }
        return(boxes)
    } else {
        // vertical move
        box1 = squareLines(x1,y1);
        box2 = squareLines(x1-1, y1);
        box1_captured = true
        box2_captured = true
        $.each(box1, function(i, line) {
            if (!(moves_played.has(line))) {
                box1_captured = false
            }
        });
        $.each(box2, function(i, line) {
            if (!(moves_played.has(line))) {
                box2_captured = false
            }
        });
        boxes = [];
        if (box1_captured) {
            str = "" + x1 + "" + y1;
            boxes.push(str);
        }
        if (box2_captured) {
            str = "" + (x1-1) + "" + y1;
            boxes.push(str)
        }
        return(boxes)
    }
};

function colorBox(box, plyr) {
    if (plyr == 0) {
        colour = "red; opacity:0.5";
    } else {
        colour = "blue; opacity:0.5";
    }
    x_ = 8 + parseInt(box[0]) * (65+8);
    y_ = 8 + (4 - parseInt(box[1])) * (65+8);
    var elem = '<rect x = "' + x_ + '", y = "' + y_ + '", height="65", width="65", style="fill:' + colour + '"></rect>';
    $('.board').append(elem);
    $("#cont").html($("#cont").html());
};

function playMove(move) {
    moves_played.add(move);
    $.post("/", {'move': move});
    
    $(('#'+last_move)).attr('style', 'fill:black');
    $(('#'+move)).attr('style', 'fill:red');
    last_move = move;

    var squares = capturedSquares(move);
    $.each(squares, function(i,sq) {
        colorBox(sq, player_to_move);
    });
    
    if (squares.length > 0) {
        scores[player_to_move] = scores[player_to_move] + squares.length
	$('p#score').text(scores[0] + "-" + scores[1]);
    };
    
    if (scores[0] + scores[1] == 25) {
        if (scores[player] > 12.5) {
            $('p#tomove').text("You won!")
        } else {
            $('p#tomove').text("You lost.")
        }
    } else {
	if (squares.length == 0) {
	    switchPlayer();
	    if (player_to_move != player) {
		playCompMove();
	    } // else: player to move, wait
	} else {
	    if (player_to_move != player) {
		// still comp's turn, get another move
		playCompMove();
	    } // else: still player's turn, wait for next move
	}
    }


};


function playCompMove(){
    var sec = 0;
    if (moves_played.size > 25) {
	sec = 4;
    }
    comp_move = $.post("/", {'move': ("c" + sec)}, function( data ) {
	comp_move = data;
	playMove(comp_move);
    });
};


function lineClick(){
    
    //alert("Move: " + $(this).attr("id"));
    var move = $(this).attr("id");

    if (moves_played.has(move) || (!(started)) || (player_to_move!=player)) {
        //alert('Invalid move!');        
    } else {
	playMove(move);
    }

length}

function switchPlayer() {
    player_to_move = 1-player_to_move;
    $('p#tomove').text("Player " + player_to_move + " to move")
    if (player_to_move != player && comp == true) {
        $('svg.board').find('> rect.line').css("cursor", "auto")
    } else {
        $('svg.board').find('> rect.line').css("cursor", "pointer")
    }
    
}




