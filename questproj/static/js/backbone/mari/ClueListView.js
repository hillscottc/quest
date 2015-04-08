'use strict';
var Backbone = require("backbone");
Backbone.$ = require("jquery");
var Marionette = require("backbone.marionette");


var ClueListView = Marionette.CompositeView.extend({
    template: '#template-todoListCompositeView',
    childView: Views.ItemView,
    childViewContainer: '#todo-list',

    ui: {
        toggle: '#toggle-all'
    },

    events: {
        'click @ui.toggle': 'onToggleAllClick'
    },

    collectionEvents: {
        'all': 'update'
    },

    initialize: function () {
        this.listenTo(App.request('filterState'), 'change:filter', this.render, this);
    },

    addChild: function (child) {
        var filteredOn = App.request('filterState').get('filter');

        if (child.matchesFilter(filteredOn)) {
            Backbone.Marionette.CompositeView.prototype.addChild.apply(this, arguments);
        }
    },

    onRender: function () {
        this.update();
    },

    update: function () {
        function reduceCompleted(left, right) {
            return left && right.get('completed');
        }

        var allCompleted = this.collection.reduce(reduceCompleted, true);

        this.ui.toggle.prop('checked', allCompleted);
        this.$el.parent().toggle(!!this.collection.length);
    },

    onToggleAllClick: function (e) {
        var isChecked = e.currentTarget.checked;

        this.collection.each(function (todo) {
            todo.save({ 'completed': isChecked });
        });
    }
});



module.exports = ClueListView;