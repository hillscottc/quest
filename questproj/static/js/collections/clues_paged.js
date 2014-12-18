var app = app || {};

app.CluesPaged = Backbone.Paginator.requestPager.extend({

    model: app.Clue,

    url: '/api/v1/random_clues/',

    paginator_ui: {
        firstPage: 0,
        currentPage: 0,
        perPage: 3,
        // 10 as a default in case service doesn't return the total
        totalPages: 10
    },

    server_api: {
        // the query field in the request
        '$filter': '',

        // number of items to return per request/page
        '$top': function() { return this.perPage },

        // customize as needed. For the Netflix API, skipping ahead based on
        // page * number of results per page was necessary.
        '$skip': function() { return this.currentPage * this.perPage },

        '$orderby': 'ReleaseYear',
        '$format': 'json',

         // custom parameters
        '$inlinecount': 'allpages',
        '$callback': 'callback'
    },

    parse: function (response) {
        // Be sure to change this based on how your results
        // are structured (e.g., d.results is Netflix-specific)
        var tags = response.d.results;

        //Normally this.totalPages would equal response.d.__count
        //but as this particular NetFlix request only returns a
        //total count of items for the search, we divide.
        this.totalPages = Math.ceil(response.d.__count / this.perPage);
        return tags;
    }

});