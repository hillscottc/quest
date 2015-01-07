var app = app || {};

app.Stats = Backbone.Model.extend({

    defaults: {
        rights: '1',
        wrongs: '2'
    },

	initialize: function() {
        console.log('This model has been initialized.');
        this.on('change', function(){
            console.log('- Values for this model have changed.');
        });
    }

    //, urlRoot : function(){
    	//return '/api/v1/clue/';
	//}

//    , parse: function( response ) {
//	    response.id = response._id;
//	    return response;
//	}

});