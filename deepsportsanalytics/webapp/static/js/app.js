$(function () {
    var AppModel = Backbone.Model.extend({
        defaults: function () {
            return { };
        },
    });

    var AppView = Backbone.View.extend({
        el: $("#app"),

        initialize: function () {
          this.$('#predictions-container').append(
            new PredictionListView({ model: new PredictionListModel({
                        predictDateFrom: moment().add(1, 'days'),
                        predictDateTo: moment().add(2, 'days'),
                      })
            }).render().el);
        },
        render: function () {
          return this;
        },
    });
    var App = new AppView({ model: new AppModel() });
});
