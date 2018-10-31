var player = 0;
var player_to_move = 0;
var moves_played = new Set();
var comp = false;
var started = false;

var scores = [0,0];

$(document).ready(function() {
    
    $('p#tomove').hide();
    $('p#score').hide();
    $('p#start').show();

    ('#start-form').on(submit, function() {
	$('p#tomove').show();
	$('p#score').show();
	$('.start-screen').hide();
	// check which player was selected
	player = parseInt($('input[name=player]:checked').val());
        
	started = true;
	
    // 	alert('started');

	return false;

    });
    
    setInterval("ajaxd()",1000); // call every 1 seconds                         
    $(document).on('click', 'rect.line', lineClick);
    //$('svg.board').find('> rect.line').click(lineClick);
    
    $('p#tomove').text("Player " + player_to_move + " to move")
    
});




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
        colour = "red";
    } else {
        colour = "blue";
    }
    x_ = 8 + parseInt(box[0]) * (65+8);
    y_ = 8 + (4 - parseInt(box[1])) * (65+8);
    var elem = '<rect x = "' + x_ + '", y = "' + y_ + '", height="65", width="65", style="fill:' + colour + '"></rect>';
    $('.board').append(elem);
    $("#cont").html($("#cont").html());
};

function lineClick(){
    
    //alert("Move: " + $(this).attr("id"));
    var move = $(this).attr("id");
    
    if (moves_played.has(move) || !(started)) { //|| player_to_move!=player) {
        //alert('Invalid move!');
        
        
    } else {
        moves_played.add(move);
        // change color of line
        
        $(this).attr('style', 'fill:black');
        
        var squares = capturedSquares(move);
        
        $.each(squares, function(i,sq) {
            colorBox(sq, player_to_move);
        });
        
        if (squares.length == 0) {
            switchPlayer();
        } else {
            scores[player_to_move] = scores[player_to_move] + squares.length
        };
        
        $('p#score').text(scores[0] + "-" + scores[1]);
        
        if (scores[0] + scores[1] == 25) {
            if (scores[player] > 12.5) {
                $('p#tomove').text("You won!")
            } else {
                $('p#tomove').text("You lost.")
            }
        }

        $.post("/", {move: move});
        
    }
        
}

function switchPlayer() {
    player_to_move = 1-player_to_move;
    if (player_to_move == player && comp == true) {
        $('svg.board').find('> rect.line').css("cursor", "auto")
        $('p#tomove').text("Player " + player_to_move + " to move")
    } else {
        $('p#tomove').text("Player " + player_to_move + " to move")
        $('svg.board').find('> rect.line').css("cursor", "pointer")
    }
    
}

function ajaxd() {                                                                                                                                                   
    //reload board  
    
    $.get( "/", function( data ) {
        var move = data;
        alert( "Load was performed: " + move);
    });                                               
} 



