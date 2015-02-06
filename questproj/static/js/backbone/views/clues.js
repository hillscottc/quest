var app = app || {};

app.CluesView = Backbone.View.extend({

    el: '#clues-view',

    initialize: function(initialClues) {

        // An event aggregator for the view.
        this.vent = _.extend({}, Backbone.Events);

        this.collection = new app.Clues(initialClues);
        this.collection.fetch({reset: true});
        this.render();
        this.listenTo(this.collection, 'add', this.renderItem );
        this.listenTo(this.collection, 'reset', this.render );
        this.listenTo(this.vent, 'guessRight', this.guessRight);
        this.listenTo(this.vent, 'guessWrong', this.guessWrong);
        console.log("CluesView initialized.");
    },

    events: {
        'input #searchText' : 'search',
        'propertychange #searchText' : 'search' // for IE
    },

    guessRight: function() {

        // Increment the rights count
        var rights_el = $('#right-count');
        var num = rights_el.html() ? parseInt(rights_el.html()) : 0;
        num++;
        rights_el.html(num);

        // Show a modal sometimes.
        var modal_el = $('#basicModal');
        var msg = "";
        if (num == 1)
            msg = "You have answered the first question in this group.";
        else if (num % 5 == 0) {
            msg = "You have answered " + num + " questions.";
        }
        if (msg != "") {
            modal_el.find('.modal-body').html(msg);
            modal_el.modal({"show": true});
        }

    },

    guessWrong: function() {
        var wrongs_el = this.$('#wrong-count');
        var num = wrongs_el.html() ? parseInt(wrongs_el.html()) : 0;
        wrongs_el.html(num + 1);
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
        var clueView = new app.ClueView({model: item, vent: this.vent});
        $("#clues-list").append( clueView.render().el );
    }
});