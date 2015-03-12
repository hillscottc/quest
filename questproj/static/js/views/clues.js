var Backbone = require("backbone");
var $ = require('jquery');
var _ = require('underscore');
var Clues = require('../collections/clues');
var ClueView = require('./clue');


CluesView = Backbone.View.extend({

    el: '#clues-view',

    initialize: function(initialClues) {
        this.collection = new Clues(initialClues);
        this.collection.fetch({reset: true});
        this.vent = _.extend({}, Backbone.Events);   // Event aggregator
        this.rights_count = 0;
        this.render();
        this.listenTo(this.collection, 'add', this.renderItem);
        this.listenTo(this.collection, 'reset', this.render);
        this.listenTo(this.vent, 'guessRight', this.guessRight);
        console.log("CluesView initialized.");
    },

    events: {
        'input #searchText' : 'search',
        'propertychange #searchText' : 'search' // for IE
    },

    guessRight: function(targ) {
        var questionid = targ.model['attributes']['id'];
        console.log(questionid);
        this.rights_count++;
        $("#answer-count").text(this.rights_count);
    },

    search: function() {
        var letters = $("#searchText").val();
        var items = this.collection.search(letters);

        // Clear
        $("#clues-list").html("");

        // Render the result items
        items.each(function(item){
            this.renderItem( item );
        }, this );

    },

    // Render each item in collection.
    render: function() {
        this.collection.each(function(item) {
            this.renderItem( item );
        }, this );
    },

    // Render an individual item
    renderItem: function( item ) {
        var clueView = new ClueView({model: item, vent: this.vent});
        $("#clues-list").append( clueView.render().el );
    }
});

module.exports = CluesView;
