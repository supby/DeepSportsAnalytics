var PredictionModel = Backbone.Model.extend({
    defaults: function () {
        return {
          gameDate: '',
          team1Name: '',
          team2Name: '',
          winProba: 0
        };
    },
});

var PredictionList = Backbone.Collection.extend({
    model: PredictionModel,

    parse: function (response) {
        return response.data;
    }
});

var Predictions = new PredictionList;

var PredictionView = Backbone.View.extend({
    tagName: 'tr',

    render: function () {
      this.$el.html(_.template($('#prediction-template').text())(this.model.toJSON()));
      return this;
    }
});
