var app = app || {};

app.Stats = Backbone.Model.extend({

    defaults: {
        rights: '0',
        wrongs: '0'
    },

	initialize: function() {
        this.on('change', function(){
            console.log('- Values for this model have changed.');
        });
        console.log('A Stats model has been initialized.');
    }

    //, urlRoot : function(){
    	//return '/api/v1/clue/';
	//}

//    , parse: function( response ) {
//	    response.id = response._id;
//	    return response;
//	}

});