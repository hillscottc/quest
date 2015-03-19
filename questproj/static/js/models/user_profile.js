var Backbone = require("backbone");


UserProfile = Backbone.Model.extend({

    defaults: {
        id: 0,
        user: {
            date_joined: "",
            last_login: "",
            username: "joeuser",
            email: "joe@anon.com",
            first_name: "Joe",
            last_name: "Schmo"
        }
    },

	initialize: function() {
	},

	urlRoot : function(){
    	return '/api/v1/user_prof/';
	}

});

module.exports = UserProfile;