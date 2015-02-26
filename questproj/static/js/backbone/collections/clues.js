var Backbone = require("backbone");
var Clue = require('../models/clue.js');


var Clues = Backbone.Collection.extend({

    model: Clue,

    url: '/api/v1/random_clues/',

    search: function(letters) {
        if(letters == "") return this;

        var pattern = new RegExp(letters,"gi");
        return _(this.filter(function(data) {
            return pattern.test(data.get("question"));
        }));
    }

});


module.exports = Clues;