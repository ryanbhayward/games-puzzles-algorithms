(function () {
  'use strict';

  // Prevent arrow keys from scrolling screen
  window.addEventListener("keydown", function (e) {
    // space and arrow keys
    if ([32, 37, 38, 39, 40].indexOf(e.keyCode) > -1) {
      e.preventDefault();
    }
  }, false);

  var game = new Phaser.Game(600, 600, Phaser.CANVAS, 'sliding-tile', {
    preload: preload,
    create: create,
    render: render
  });

  var PIECE_WIDTH = 600 / 3;
  var PIECE_HEIGHT = 600 / 3;
  var BOARD_COLS = 3;
  var BOARD_ROWS = 3;

  var piecesGroup;
  var piecesAmount = BOARD_COLS * BOARD_ROWS;
  var searchDelay = 0;

  var slidingTile;
  var solver;
  var steps;
  var searchSteps;
  var size1;
  var size2;

  /**
   * Preload the 600 x 600 image
   */
  function preload() {
    game.load.spritesheet("background", "/static/img/bl.jpg", PIECE_WIDTH, PIECE_HEIGHT);
  }

  function create() {
    game.input.keyboard.addCallbacks(this, onCurDown, function () {
    }, function () {
    });
    $.get('/sliding_tile/state', {})
      .then(getState.bind(this));
    game.time.advancedTiming = true;
  }

  function render() {
    game.debug.text(game.time.fps, 2, 14, '#00ff00');
  }

  function prepareBoard(arrayValue) {
    var piecesIndex = 0;
    var i;
    var j;
    var piece;

    arrayValue = arrayValue || slidingTile;

    if (piecesGroup) {
      piecesGroup.destroy();
    }
    piecesGroup = game.add.group();

    var counter = 0;
    for (i = 0; i < BOARD_ROWS; i++) {
      for (j = 0; j < BOARD_COLS; j++) {
        if (!arrayValue[piecesIndex]) {
          piece = piecesGroup.create(j * PIECE_WIDTH, i * PIECE_HEIGHT);
          piece.black = true;
        } else {
          piece = piecesGroup.create(j * PIECE_WIDTH, i * PIECE_HEIGHT, "background", arrayValue[piecesIndex]);
        }
        piece.name = 'piece' + i.toString() + 'x' + j.toString();
        piece.currentIndex = piecesIndex;
        piece.inputEnabled = true;
        piece.posX = j;
        piece.posY = i;
        piecesIndex++;
        counter++;
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
    if (['left', 'up', 'right', 'down'].indexOf(move) > -1) {
      $.ajax({url: '/sliding_tile/move', type: 'PUT', data: {'move': move}, success: getState.bind(this)});
      return;
    }

    // handle searching
    if (x.code === 'KeyX') {
      this.searchSteps = 0;
      $.get('/sliding_tile/search_step', {}, searchStep.bind(this));
      return;
    }
    // handle reset
    if (x.code === 'KeyR') {
      $('#searchOutput').text('');
      $('#searchSteps').text('');
      $.get('/sliding_tile/refresh', {}, getState.bind(this));
      location.reload();
    }
  }

  function searchStep(rawData) {
    var data = JSON.parse(rawData);
    var solved = data.solved;
    if (solved === null) {
      $('#searchOutput').text('Impossible, no solution');
      $.get('/sliding_tile/state', {}, getState.bind(this));
      this.searchSteps = null;
    } else if (solved === true) {
      console.log('solved', data);
      $('#searchOutput').text(data.solution);
      $.get('/sliding_tile/state', {}, getState.bind(this));
      applyMoves(data.solution);
    } else {
      this.sliding_tile = data.sliding_tile;
      prepareBoard(this.sliding_tile);
      if (!this.searchSteps)
        this.searchSteps = 0;
      this.searchSteps += 1;
      $('#searchSteps').text(this.searchSteps);
      setTimeout(function () {
        $.get('/sliding_tile/search_step', {}, searchStep.bind(this))
      }.bind(this), searchDelay);
    }
  }

  function getState(rawData) {
    var data = JSON.parse(rawData);
    slidingTile = data.sliding_tile;
    solver = data.solver;
    steps = data.steps;
    size1 = data.size1;
    size2 = data.size2;
    $('#search').val(solver);
    $('#steps').text(steps);
    $('#size1').val(Math.floor(size1));
    $('#size2').val(Math.floor(size2));
    $('#delay').val(searchDelay);
    prepareBoard();
  }

  function applyMoves(moves) {
    for(var i = 0; i < moves.length; i++) {
      var move = moves[i];
      if (['left', 'up', 'right', 'down'].indexOf(move) > -1) {
        $.ajax({url: '/sliding_tile/move', type: 'PUT', data: {'move': move}, success: getState.bind(this)});
      }
    }
  }


  $('#sliding-tile-form').submit(function () {
    size1 = $('#size1').val();
    size2 = $('#size2').val();
    var search = $('#search').val();
    $.post('/sliding_tile/set_search', {'search': search}, getState);
    $.post('/sliding_tile/set_size', {'size1': size1, 'size2': size2}, getState);
    return true;
  });

  $('#delay').change(function () {
    searchDelay = Number($('#delay').val());
  });
})();
