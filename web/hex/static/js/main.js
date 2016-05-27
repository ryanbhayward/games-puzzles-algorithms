(function() {

'use strict';

var frame_width = 1000;
var frame_height = 600;
var board_width = 1000 - 10;
var board_height = frame_height - 60;

var game = new Phaser.Game(frame_width, frame_height, Phaser.Auto, "body",
                           {preload: preload, create: create,});

var size = 50;
var height = 2 * size;
var width = Math.sqrt(3)/2 * height;
var row_dimension = 12;
var column_dimension = 12;

var board;
var graphics;
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


    var column_start = new Phaser.Point(width / 2, height / 2);

    for (var i = 0; i < column_dimension; ++i) {
        Array.prototype.push.apply(hexagons,
                                   generate_column(column_start, row_dimension));
        column_start.add(width, 0);
    }

    return hexagons;
}

// Calculate the maximum unit size based on board frame height.
function max_size_height(row_dimension, board_height) {
    var height_multiple = 1 + (3 / 4) * (row_dimension - 1);
    return board_height / height_multiple / 2;
}

// Calculate the maximum unit size based on board frame width.
function max_size_width(row_dimension, column_dimension, board_width) {
    var width_multiple = column_dimension + (row_dimension - 1) / 2;
    return board_width / width_multiple / Math.sqrt(3);
}

function set_dimensions(size) {
    height = 2 * size;
    width = Math.sqrt(3)/2 * height;
}

// Set the size of the board units.
function set_size(row_dimension, column_dimension) {
    var from_height = max_size_height(row_dimension, board_height);
    var from_width = max_size_width(row_dimension, column_dimension,
                                    board_width);

    if (from_height < from_width) {
        size = from_height;
    } else {
        size = from_width;
    }

    set_dimensions(size);
}

function draw_board(hexagons, graphics) {
    graphics.lineStyle(3, 0x000000, 1);

    for (var i = 0; i < hexagons.length; ++i) {
        graphics.beginFill(0xffffff);
        graphics.drawPolygon(hexagons[i]);
        graphics.endFill();
    }
}

function preload() {
    // Set the game to scale automatically.
    game.scale.scaleMode = Phaser.ScaleManager.SHOW_ALL;
    game.scale.pageAlignHorizontally = true;
    game.scale.pageAlignVertically = true;
}

function create() {
    game.stage.backgroundColor = 0xffffff;
    graphics = game.add.graphics(0, 0);

    hexagons = generate_board(row_dimension, column_dimension);

    draw_board(hexagons, graphics);
}

})();
