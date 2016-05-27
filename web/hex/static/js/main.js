var frame_width = 1000;
var frame_height = 600;
var board_width = 1000 - 10;
var board_height = frame_height - 60;

var game = new Phaser.Game(frame_width, frame_height, Phaser.Auto, "body",
                           {preload: preload, create: create,});

var size = 50;
var diameter = 60;
var height = 2 * size;
var width = Math.sqrt(3)/2 * height;
var board_colors = [0x000000, 0xffffff];
var row_dimension;
var column_dimension;

var BLACK = 0;
var WHITE = 1;
var EMPTY = 2;

var board;
var hexagons;

// Generate a hexagon centered at the given center point.
function hexagon(center) {
    var point = center.clone();
    var corners = [];

    point.add(0, size);
    corners.push(point.clone());

    for (var i = 0; i < 5; ++i) {
        point.rotate(center.x, center.y, 60, true);
        corners.push(point.clone());
    }

    return new Phaser.Polygon(corners);
}

// Generate one column of the board.
function generate_column(start, row_dimension) {
    var center = start.clone();
    var hexagons = [];

    for (var i = 0; i < row_dimension; ++i) {
        hexagons.push(hexagon(center));
        center.add(width / 2, 3/4 * height);
    }

    return hexagons;
}

// Generate the hexagons that make up the board.
function generate_board(row_dimension, column_dimension) {
    var hexagons = [];

    set_size(row_dimension, column_dimension);

    var column_start = new Phaser.Point(width / 2, height / 2);

    for (var i = 0; i < column_dimension; ++i) {
        Array.prototype.push.apply(hexagons,
                                   generate_column(column_start, row_dimension));
        column_start.add(width, 0);
    }

    return hexagons;
}

// Calculate the maximum unit size based on board frame height.
function max_size_height(column_dimension, board_height) {
    var height_multiple = 1 + (3 / 4) * (column_dimension - 1);
    return board_height / height_multiple / 2;
}

// Calculate the maximum unit size based on board frame width.
function max_size_width(row_dimension, column_dimension, board_width) {
    var width_multiple = column_dimension + (row_dimension - 1) / 2;
    return board_width / width_multiple / Math.sqrt(3);
}

function set_dimensions(size) {
    diameter = 1.2 * size;
    height = 2 * size;
    width = Math.sqrt(3)/2 * height;
}

// Set the size of the board units.
function set_size(row_dimension, column_dimension) {
    var from_height = max_size_height(column_dimension, board_height);
    var from_width = max_size_width(row_dimension, column_dimension,
                                    board_width);

    if (from_height < from_width) {
        size = from_height;
    } else {
        size = from_width;
    }

    set_dimensions(size);
}

// Calculate the center of mass of the given polygon.
function poly_center(poly) {
    var coords = poly.toNumberArray();

    var x = 0.0;
    var y = 0.0;

    for (var i = 0; i < coords.length / 2; ++i) {
        x += coords[2 * i];
        y += coords[2 * i + 1];
    }

    x /= coords.length / 2;
    y /= coords.length / 2;

    return [x, y];
}

// Draw a piece within the given hexagon, if needed.
function draw_piece(hexagon, piece, graphics) {
    if (piece == EMPTY) {
        return;
    }

    center = poly_center(hexagon);

    graphics.beginFill(board_colors[piece]);
    graphics.drawCircle(center[0], center[1], diameter);
    graphics.endFill();
}

function draw_board(hexagons, graphics) {
    graphics.lineStyle(3, 0x000000, 1);

    for (var i = 0; i < hexagons.length; ++i) {
        graphics.beginFill(0xffffff);
        graphics.drawPolygon(hexagons[i]);
        draw_piece(hexagons[i], board[i], graphics);
        graphics.endFill();
    }
}

function declare_winner(winner) {
    if (winner === BLACK) {
        var win_string = "Black wins!";
    } else if (winner === WHITE) {
        var win_string = "White wins!";
    }

    $("#who_wins").html(win_string);
    $("#winner_modal").modal('show');
}

function set_board(data) {
    if (data.error === true) {
        return;
    }
    board = data.board;
    draw_board(hexagons, graphics);

}

function reset_board(data) {
    if (data.error === true) {
        return;
    }
    row_dimension = data.row_dimension;
    column_dimension = data.column_dimension;
    set_size(row_dimension, column_dimension);
    hexagons = generate_board(row_dimension, column_dimension);
    graphics.clear();
    get_state();
}

function get_state() {
    $.ajax({ url: $SCRIPT_ROOT + '/_board',
             dataType: 'json',
             async: false,
             data: {},
             success: set_board
           });
}

function make_move(row, column) {
    $.ajax({ url: $SCRIPT_ROOT + '/_play_move',
             dataType: 'json',
             async: false,
             data: {'row': row,
                    'column': column},
             success: set_board
           });
}

function board_index(row, column) {
    return (column * row_dimension + row);
}

// Check if we've clicked on a hex and request a move if appropriate.
function on_click(key) {
    for (var i = 0; i < column_dimension; ++i) {
        for (var j = 0; j < row_dimension; ++j) {
            var hex = hexagons[board_index(j, i)];
            if (hex.contains(this.input.x, this.input.y)) {
                make_move(j, i);
                break;
            }
        }
    }
}

function undo_move() {
    $.ajax({ url: $SCRIPT_ROOT + '/_undo_move',
             dataType: 'json',
             async: false,
             data: {},
             success: set_board
           });
}

function reset_game() {
    $.ajax({ url: $SCRIPT_ROOT + '/_reset_game',
             dataType: 'json',
             async: false,
             data: {},
             success: reset_board
           });
}

function ai_move() {
    $.ajax({ url: $SCRIPT_ROOT + '/_ai_move',
             dataType: 'json',
             async: false,
             data: {},
             success: set_board
           });
}

function resize_board() {
    var $form = $('.ui.form');
    var row_dimension = $form.form('get value', 'row_dimension');
    var column_dimension = $form.form('get value', 'column_dimension');

    $('#resize_modal').modal('hide')

    $.ajax({ url: $SCRIPT_ROOT + '/_resize_board',
             dataType: 'json',
             async: false,
             data: {'row_dimension': row_dimension,
                    'column_dimension': column_dimension},
             success: reset_board
           });

    return false;
}

function resize_board_modal() {
    var prompt_string = "Please enter a number in the range [2:13].";
    $('.ui.form')
        .form({
            fields: {
                row_dimension: {
                    identifier : 'row_dimension',
                    rules: [
                        {
                            type : 'integer[1..13]',
                            prompt: prompt_string
                        }
                    ]
                },
                column_dimension: {
                    identifier : 'column_dimension',
                    rules: [
                        {
                            type : 'integer[1..13]',
                            prompt: prompt_string
                        }
                    ]
                }
            },
            onSuccess: resize_board
        });
    var modal_element = $('#resize_modal').modal('setting', {
        onApprove: resize_board
    });
    modal_element.modal('show');
}

function preload() {
    // Set the game to scale automatically.
    game.scale.scaleMode = Phaser.ScaleManager.SHOW_ALL;
    game.scale.pageAlignHorizontally = true;
    game.scale.pageAlignVertically = true;

    // Load the image assets.
    game.load.image('undo', '../static/assets/undo.png');
    game.load.image('reset', '../static/assets/reset.png');
    game.load.image('aimove', '../static/assets/aimove.png');
    game.load.image('resize', '../static/assets/resize.png');
}

function create() {
    game.stage.backgroundColor = 0xffffff;
    graphics = game.add.graphics(0, 0);

    hexagons = generate_board(row_dimension, column_dimension);

    var button = game.add.button(10, 550, 'undo', undo_move);
    var button = game.add.button(180, 550, 'reset', reset_game);
    var button = game.add.button(350, 550, 'aimove', ai_move);
    var button = game.add.button(520, 550, 'resize', resize_board_modal);

    reset_game();
    draw_board(hexagons, graphics);

    game.input.onDown.add(on_click, game);
}
