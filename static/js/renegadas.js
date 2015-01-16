function teste() {
    alert("TESTE");
}

var br_preload = null;
var br_create = null;
var br_update = null;
var br_render = null;

function preload() {
	br_preload();
}

function create() {
	br_create();
}

function update() {
	br_update();
}

function render() {
	br_render();
}

function collisionHandler (player, veg) {

    //  If the player collides with the chillis then they get eaten :)
    //  The chilli frame ID is 17
    if (veg.frame == 17)
    {
        veg.kill();
    }

}

var stater = {preload: preload, create: create, update: update, render: render};
//game = new phaser.game(800, 600, window.phaser.auto, 'canvas-anchor', stater);
