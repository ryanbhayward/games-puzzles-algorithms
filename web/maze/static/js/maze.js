(function() {
"use strict";

var grey = "data:image/jpeg;base64," +
"iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNM+Q8AAc0BZX6f84gAAAAASUVORK5CYII=";
var black = "data:image/jpeg;base64," +
"iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNk+A8AAQUBAScY42YAAAAASUVORK5CYII=";
var green = "data:image/jpeg;base64," +
"iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkOMHwHwADYQHJEKmC9QAAAABJRU5ErkJggg==";
var white = "data:image/jpeg;base64," +
"iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8/1/yPwAINAMYyt59LwAAAABJRU5ErkJggg==";
var cellSize = 8;

var game = new Phaser.Game(500,500,Phaser.AUTO,'maze', {preload:preload, create:create, render:render});

var maze;
var solver;
var steps;
var searchSteps;
var timeout;

function preload() {
  var iBg = new Image();
  iBg.src = grey;
  game.cache.addImage('grey', grey, iBg);
  var bBg = new Image();
  bBg.src = black;
  game.cache.addImage('black', black, bBg);
  var gBg = new Image();
  gBg.src = green;
  game.cache.addImage('green', green, gBg);
  var wBg = new Image();
  wBg.src = white;
  game.cache.addImage('white', white, wBg);
};

function create(){
  game.input.keyboard.addCallbacks(this, onCurDown, function(){}, function(){})
  $.get("/state", {}, getState.bind(this));
  timeout = game.time.time;
	game.time.advancedTiming = true;
};

function render() {
	game.debug.text(game.time.fps, 2, 14, "#00ff00");
  if (!this.maze || !this.maze.length)
    return;
  game.world.forEach(function(item) {
    item.destroy();
  });
  for (var i = 0; i < this.maze.length; i++) {
    var row = this.maze[i];
    for (var j = 0; j < row.length; j++) {
      var cell = row[j];
      if (cell === 0)
        game.add.tileSprite(j * cellSize, i * cellSize, cellSize, cellSize, 'black');
      else if (cell === 1)
        game.add.tileSprite(j * cellSize, i * cellSize, cellSize, cellSize, 'grey');
      else if (cell === 2)
        game.add.tileSprite(j * cellSize, i * cellSize, cellSize, cellSize, 'white');
      else if (cell === 3)
        game.add.tileSprite(j * cellSize, i * cellSize, cellSize, cellSize, 'green');
    }
  }
}

function onCurDown(x) {
  // handle movement
  var move = '';
  if (['ArrowLeft', 'KeyA'].indexOf(x.code) > -1)
    move = 'left';
  else if (['ArrowRight', 'KeyD'].indexOf(x.code) > -1)
    move = 'right';
  else if (['ArrowDown', 'KeyS'].indexOf(x.code) > -1)
    move = 'down';
  else if (['ArrowUp', 'KeyW'].indexOf(x.code) > -1)
    move = 'up';
  if (['left', 'up', 'right', 'down'].indexOf(move) > -1){
    $.ajax({url: '/move', type: 'PUT', data: {'move': move}, success: getState.bind(this)});
    return
  }

  // handle searching
  if (x.code === 'KeyX') {
    console.log('search');
    $.get("/search_step", {}, searchStep.bind(this))
    return
  }
  // handle reset
  if (x.code === 'KeyR') {
    $('#searchOutput').text('');
    $('#searchSteps').text('');
    $.get("/refresh", {}, getState.bind(this));
    return
  }
}

function searchStep(rawData) {
  var data = JSON.parse(rawData);
  var solved = data.solved;
  if (solved === null) {
    $('#searchOutput').text('Impossible, no solution');
    $.get("/state", {}, getState.bind(this));
    this.searchSteps = null;
    return;
  } else if (solved === true) {
    $('#searchOutput').text(data.solution);
    $.get("/state", {}, getState.bind(this));
    return;
  } else {
    this.maze = data.maze;
    if (!this.searchSteps)
      this.searchSteps = 0;
    this.searchSteps += 1;
    $('#searchSteps').text(this.searchSteps);
    $.get("/search_step", {}, searchStep.bind(this));
  }
}

function getState(rawData) {
  var data = JSON.parse(rawData);
  this.maze = data.maze;
  this.solver = data.solver;
  this.steps = data.steps;
  $("#search").val(this.solver);
  $('#steps').text(this.steps);
  $('#width').val(Math.floor(this.maze[0].length/2));
  $('#height').val(Math.floor(this.maze.length/2));
}

$("#maze-form").submit(function(){
  var width = $('#width').val();
  var height = $('#height').val();
  var search = $('#search').val();
  $.post("/set_search", {'search': search}, getState)
  $.post("/set_size", {'width': width, 'height': height}, getState)
  return true;
});

})()