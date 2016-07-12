(function () {
  'use strict';

  // Prevent arrow keys from scrolling screen
  window.addEventListener("keydown", function(e) {
    // space and arrow keys
    if([32, 37, 38, 39, 40].indexOf(e.keyCode) > -1) {
      e.preventDefault();
    }
  }, false);
  
  var grey = 'data:image/jpeg;base64,' +
    'iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNM+Q8AAc0BZX6f84gAAAAASUVORK5CYII=';
  var black = 'data:image/jpeg;base64,' +
    'iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNk+A8AAQUBAScY42YAAAAASUVORK5CYII=';
  var green = 'data:image/jpeg;base64,' +
    'iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkOMHwHwADYQHJEKmC9QAAAABJRU5ErkJggg==';
  var yellow = 'data:image/jpeg;base64,' +
    'iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8/1/yPwAINAMYyt59LwAAAABJRU5ErkJggg==';
  var darkYellow = 'data:image/jpeg;base64,' +
    'iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNMYWT4DwACnAFmA4+qdwAAAABJRU5ErkJggg==';
  var cellSize = 8;

  var game = new Phaser.Game(600, 400, Phaser.AUTO, 'maze', {preload: preload, create: create, render: render});

  var maze;
  var solver;
  var steps;
  var searchSteps;
  var initializeState = true;
  var userSprite;
  var historySprites = [];
  var searchDelay = 500;

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
    wBg.src = yellow;
    game.cache.addImage('yellow', yellow, wBg);
    var dBg = new Image();
    dBg.src = darkYellow;
    game.cache.addImage('darkYellow', darkYellow, dBg);
  }

  function create() {
    game.input.keyboard.addCallbacks(this, onCurDown, function () {
    }, function () {
    });
    $.get('/maze/state', {}, getState.bind(this));
    game.time.advancedTiming = true;
  }

  function render() {
    game.debug.text(game.time.fps, 2, 14, '#00ff00');
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
    if (['left', 'up', 'right', 'down'].indexOf(move) > -1) {
      $.ajax({url: '/maze/move', type: 'PUT', data: {'move': move}, success: getState.bind(this)});
      return;
    }

    // handle searching
    if (x.code === 'KeyX') {
      var historyLength = historySprites.length;
      for (var i = 0; i < historyLength; i++) {
        historySprites.pop().destroy();
      }
      this.searchSteps = 0;
      $.get('/maze/search_step', {}, searchStep.bind(this));
      return;
    }
    // handle reset
    if (x.code === 'KeyR') {
      $('#searchOutput').text('');
      $('#searchSteps').text('');
      $.get('/maze/refresh', {}, getState.bind(this));
      location.reload();
    }
  }

  function updateMazeState(maze) {
    var i = 0;
    var j = 0;
    var row;
    var cell;
    if (initializeState) {
      for (i = 0; i < maze.length; i++) {
        row = maze[i];
        for (j = 0; j < row.length; j++) {
          cell = row[j];
          if (cell === 1) {
            // initialize wall sprites
            game.add.tileSprite(j * cellSize, i * cellSize, cellSize, cellSize, 'grey');
          }
          else if (cell === 2) {
            // initialize user sprite
            userSprite = game.add.tileSprite(j * cellSize, i * cellSize, cellSize, cellSize, 'yellow');
          }
          else if (cell === 3) {
            // initialize goal sprite
            game.add.tileSprite(j * cellSize, i * cellSize, cellSize, cellSize, 'green').alpha = 0.5;
          }
        }
      }
      initializeState = false;
    } else {
      for (i = 0; i < maze.length; i++) {
        row = maze[i];
        for (j = 0; j < row.length; j++) {
          cell = row[j];
          if (cell === 2) {
            var historySprite = game.add.tileSprite(userSprite.x, userSprite.y, cellSize, cellSize, 'darkYellow');
            historySprites.push(historySprite);
            userSprite.x = j * cellSize;
            userSprite.y = i * cellSize;
            for (var k = 0; k < historySprites.length; k++) {
              var tempHistorySprite = historySprites[k];
              if (tempHistorySprite.x === userSprite.x && tempHistorySprite.y === userSprite.y) {
                tempHistorySprite.destroy();
                historySprites.splice(k, 1);
              }
            }
          }
        }
      }
    }
  }

  function searchStep(rawData) {
    var data = JSON.parse(rawData);
    var solved = data.solved;
    if (solved === null) {
      $('#searchOutput').text('Impossible, no solution');
      $.get('/maze/state', {}, getState.bind(this));
      this.searchSteps = null;
    } else if (solved === true) {
      $('#searchOutput').text(data.solution);
      $.get('/maze/state', {}, getState.bind(this));
      var historyLength = historySprites.length;
      for (var i = 0; i < historyLength; i++) {
        historySprites.pop().destroy();
      }
      applyMoves(data.solution);
    } else {
      this.maze = data.maze;
      updateMazeState(this.maze);
      if (!this.searchSteps)
        this.searchSteps = 0;
      this.searchSteps += 1;
      $('#searchSteps').text(this.searchSteps);
      setTimeout(function () {
        $.get('/maze/search_step', {}, searchStep.bind(this))
      }.bind(this), searchDelay);
    }
  }

  function getState(rawData) {
    var data = JSON.parse(rawData);
    maze = data.maze;
    solver = data.solver;
    steps = data.steps;
    updateMazeState(maze);
    $('#search').val(solver);
    $('#steps').text(steps);
    $('#width').val(Math.floor(maze[0].length / 2));
    $('#height').val(Math.floor(maze.length / 2));
    $('#delay').val(searchDelay);
  }

  function applyMoves(moves) {
    for(var i = 0; i < moves.length; i++) {
      var move = moves[i];
      if (['left', 'up', 'right', 'down'].indexOf(move) > -1) {
        $.ajax({url: '/maze/move', type: 'PUT', data: {'move': move}, success: getState.bind(this)});
      }
    }
  }

  $('#maze-form').submit(function () {
    var width = $('#width').val();
    var height = $('#height').val();
    var search = $('#search').val();
    $.post('/maze/set_search', {'search': search}, getState);
    $.post('/maze/set_size', {'width': width, 'height': height}, getState);
    return true;
  });

  $('#delay').change(function () {
    searchDelay = Number($('#delay').val());
  });

})();