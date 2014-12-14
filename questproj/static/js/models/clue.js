var app = app || {};

app.Clue = Backbone.Model.extend({
    defaults: {
        question: 'Some question.',
        answer: 'Some answer.',
        category: 'Some category.'
    },

	parse: function( response ) {
	    response.id = response._id;
	    return response;
	}
    
});