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
                        modelName: 'model',
                        predictDateFrom: moment().add(1, 'days'),
                        predictDateTo: moment().add(2, 'days'),
                        dataSource: 'nhlref_2015_2016_local'
                      })
            }).render().el);

            this.$('#predictions-container2').append(
              new PredictionListView({ model: new PredictionListModel({
                          modelName: 'model-ns',
                          predictDateFrom: moment().add(1, 'days'),
                          predictDateTo: moment().add(2, 'days'),
                          dataSource: 'nhlref_2015_2016_local'
                        })
              }).render().el);
          return this;
        },
    });
    var App = new AppView({ model: new AppModel() }).render();
});
