var Backbone = require("backbone");


var Clue = Backbone.Model.extend({

    defaults: {
        question: 'Some question.',
        answer: 'Some answer.',
        category: 'Some category.'
    },

	initialize: function() {
	},

	urlRoot : function(){
    	return '/api/v1/clue/';
	}

//    , parse: function( response ) {
//	    response.id = response._id;
//	    return response;
//	}

});

module.exports = Clue;