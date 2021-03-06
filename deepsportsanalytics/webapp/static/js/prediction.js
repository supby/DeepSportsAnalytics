var PredictionModel = Backbone.Model.extend({
    defaults: function () {
        return {
          gameDate: null,
          team1Name: null,
          team2Name: null,
          winProba: null
        };
    },
    isNull: function() {
      return this.attributes['gameDate'] == null
            && this.attributes['team1Name'] == null
            && this.attributes['team2Name'] == null
            && this.attributes['winProba'] == null;
    }
});

var PredictionList = Backbone.Collection.extend({
    model: PredictionModel,

    parse: function (response) {
        return response.data;
    }
});

var PredictionView = Backbone.View.extend({
    tagName: 'tr',
    render: function () {
      var winProba = this.model.get('winProba');

      this.$el.attr('prediction', winProba);
      this.$el.html(_.template($('#prediction-template').text())(this.model.toJSON()));

      if(winProba < 30 || winProba > 70)
        this.$el.addClass('dsa-color-success');

      return this;
    }
});
