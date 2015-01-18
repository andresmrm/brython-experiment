Phaser.Filter.DayLight = function (game) {

    Phaser.Filter.call(this, game);

    this.uniforms.r = { type: '1f', value: 1.0 };
    this.uniforms.g = { type: '1f', value: 1.0 };
    this.uniforms.b = { type: '1f', value: 1.0 };
    this.uniforms.rs = { type: '1f', value: 0.0 };
    this.uniforms.gs = { type: '1f', value: 0.0 };
    this.uniforms.bs = { type: '1f', value: 0.0 };

    this.fragmentSrc = [

        "precision mediump float;",

        "varying vec2       vTextureCoord;",
        "uniform sampler2D  uSampler;",
        "uniform float      r;",
        "uniform float      g;",
        "uniform float      b;",
        "uniform float      rs;",
        "uniform float      gs;",
        "uniform float      bs;",

        "void main(void) {",
            "gl_FragColor = texture2D(uSampler, vTextureCoord);",
            //"gl_FragColor.rgb = mix(gl_FragColor.rgb, vec3(0.2126 * gl_FragColor.r + 0.7152 * gl_FragColor.g + 0.0722 * gl_FragColor.b), gray);",
        "if(gl_FragColor.a != 0.0){ ",
        // "gl_FragColor.rgba = vec4(r * gl_FragColor.r +0.5, gl_FragColor.g, b * gl_FragColor.b, gl_FragColor.a);",
        "gl_FragColor.rgb = vec3(r * gl_FragColor.r + rs, g * gl_FragColor.g + gs, b * gl_FragColor.b + bs);",
        "}}"
    ];

};

Phaser.Filter.DayLight.prototype = Object.create(Phaser.Filter.prototype);
Phaser.Filter.DayLight.prototype.constructor = Phaser.Filter.DayLight;

Object.defineProperty(Phaser.Filter.DayLight.prototype, 'r', {

    get: function() {
        return this.uniforms.r.value;
    },

    set: function(value) {
        this.uniforms.r.value = value;
    }

});

Object.defineProperty(Phaser.Filter.DayLight.prototype, 'g', {

    get: function() {
        return this.uniforms.g.value;
    },

    set: function(value) {
        this.uniforms.g.value = value;
    }

});

Object.defineProperty(Phaser.Filter.DayLight.prototype, 'b', {

    get: function() {
        return this.uniforms.b.value;
    },

    set: function(value) {
        this.uniforms.b.value = value;
    }

});

Object.defineProperty(Phaser.Filter.DayLight.prototype, 'rs', {

    get: function() {
        return this.uniforms.rs.value;
    },

    set: function(value) {
        this.uniforms.rs.value = value;
    }

});

Object.defineProperty(Phaser.Filter.DayLight.prototype, 'gs', {

    get: function() {
        return this.uniforms.gs.value;
    },

    set: function(value) {
        this.uniforms.gs.value = value;
    }

});

Object.defineProperty(Phaser.Filter.DayLight.prototype, 'bs', {

    get: function() {
        return this.uniforms.bs.value;
    },

    set: function(value) {
        this.uniforms.bs.value = value;
    }

});
