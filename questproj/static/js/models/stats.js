var app = app || {};

app.Stats = Backbone.Model.extend({

    defaults: {
        rights: 0,
        wromgs: 0
    }

	//initialize: function() {
     //   // broadcast rights changes
     //   this.on('change:rights', function() {
     //       Backbone.trigger('change:rights', this);
     //       console.log("broadcast rights change");
     //   })
	//}

});

