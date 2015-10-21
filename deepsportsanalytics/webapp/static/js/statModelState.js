var StatModelStateModel = Backbone.Model.extend({
  urlRoot: '/api/v1.0/updatemodel/lastupdate',
  defaults: function () {
      return {
        lastUpdate: null,
        name: null
      };
  },
});

var StatModelStateView = Backbone.View.extend({
  initialize: function () {
    var self = this;
    this.model.fetch({
            success: function() {
                self.render();
              }
            });
  },
  render: function () {
    this.$el.html(_.template($('#stat-model-state-template').text())(this.model.toJSON()));
    return this;
  },
});
