var frame_width = 1000;
var frame_height = 600;

var game = new Phaser.Game(frame_width, frame_height, Phaser.Auto, "body",
                           {preload: preload, create: create,});

var size = 50;
var height = 2 * size;
var width = Math.sqrt(3)/2 * height;

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

function preload() {
    // Set the game to scale automatically.
    game.scale.scaleMode = Phaser.ScaleManager.SHOW_ALL;
    game.scale.pageAlignHorizontally = true;
    game.scale.pageAlignVertically = true;
}

function create() {
    game.stage.backgroundColor = 0xffffff;
}
