var app = app || {};

app.CluesView = Backbone.View.extend({

    el: '#clues-view',

    initialize: function(initialClues) {

        // An event aggregator for the view.
        this.vent = _.extend({}, Backbone.Events);
        this.rights_count = 0;
        this.collection = new app.Clues(initialClues);
        this.collection.fetch({reset: true});
        this.render();
        this.listenTo(this.collection, 'add', this.renderItem );
        this.listenTo(this.collection, 'reset', this.render );
        this.listenTo(this.vent, 'guessRight', this.guessRight);
        console.log("CluesView initialized.");
    },

    events: {
        'click #nostra-btn' : 'showHoro',
        'input #searchText' : 'search',
        'propertychange #searchText' : 'search' // for IE
    },

    showHoro: function() {
        $("#nostra-txt").load("/horoscope", function(responseTxt, statusTxt, xhr){
            if(statusTxt == "error") console.log("Err: " + xhr.status + ": " + xhr.statusText);
        });
    },

    guessRight: function() {
        this.rights_count++;
        console.log("Right:", this.rights_count)

        // Show a modal sometimes.
        if (this.rights_count == 1) {
            this.showModal("Congratulations!",
                "You have answered the first question. You'll get an updated horoscope " +
                "for every 3rd answer.");
        } else if (this.rights_count % 3 == 0) {
            var modal_el = $('#basicModal');
            modal_el.find('.modal-header h4').html("Your fortune is...");

            // Ajax-load the modal body
            $("#modal-body").load("/horoscope", function(responseTxt, statusTxt, xhr){
                if(statusTxt == "error") console.log("Err: " + xhr.status + ": " + xhr.statusText);
            });
            modal_el.modal({"show": true});
        }
    },

    showModal: function(header, body) {
        var modal_el = $('#basicModal');
        modal_el.find('.modal-header h4').html(header);
        modal_el.find('.modal-body h3').html(body);
        modal_el.modal({"show": true});
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