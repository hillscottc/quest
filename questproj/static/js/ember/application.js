
window.Todos = Ember.Application.create();

Todos.Store = DS.Store.extend();

// Indicate we are using fixtures
Todos.ApplicationAdapter = DS.FixtureAdapter.extend();

