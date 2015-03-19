var Backbone = require("backbone");
var $ = require('jquery');
var _ = require('underscore');

UserView = Backbone.View.extend({

    el: '#userView',

    template: _.template( $('#userTemplate').html() ),

    initialize: function(options) {
        this.model = options.model;
        this.model.fetch();
        this.render();
        console.log("Userview init " + JSON.stringify(this.model));
    },

    render: function() {
        this.$el.html( this.template( this.model.attributes ) );
        return this;
    }
});

module.exports = UserView;



