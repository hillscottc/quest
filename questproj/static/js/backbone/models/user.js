var app = app || {};

app.User = Backbone.Model.extend({

    defaults: {
        question: 'Some question.',
        answer: 'Some answer.',
        category: 'Some category.'
    },

	initialize: function() {
	},

	urlRoot : function(){
    	return '/api/v1/user/';
	}

});

