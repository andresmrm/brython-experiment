//var game = new Phaser.Game(500, 400, Phaser.AUTO, 'canvas-anchor');

var BasicGame = function(game) {};

BasicGame.Boot = function (game) {
    // nothing here
};

BasicGame.Boot.prototype = 
{
	create: function() 
	{
        window.game.stage.backgroundColor = '#f0f';
    },
};

//game.state.add('Boot', BasicGame.Boot);
//game.state.start('Boot');

