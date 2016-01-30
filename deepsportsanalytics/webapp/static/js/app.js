$(function () {
    var AppModel = Backbone.Model.extend({
        defaults: function () {
            return { };
        },
    });

    var AppView = Backbone.View.extend({
        el: $("#app"),

        initialize: function () {
        },
        render: function () {
          this.$('#predictions-container').append(
            new PredictionListView({ model: new PredictionListModel({
                        title: 'NHL 2015 - 2016 Predictions',
                        modelName: 'model-lr-nhlref-all',
                        predictDateFrom: moment().add(1, 'days'),
                        predictDateTo: moment().add(2, 'days'),
                        dataSource: 'nhlref_all'
                      })
            }).render().el,
            new PredictionListView({ model: new PredictionListModel({
                        title: 'NBA 2015 - 2016 Predictions',
                        modelName: 'model-lr-nbaref-all',
                        predictDateFrom: moment().add(1, 'days'),
                        predictDateTo: moment().add(2, 'days'),
                        dataSource: 'nbaref_all'
                      })
            }).render().el);
          return this;
        },
    });
    var App = new AppView({ model: new AppModel() }).render();
});
