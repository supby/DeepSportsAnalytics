var PredictionListModel = Backbone.Model.extend({
    defaults: function () {
        return {
          filter: null,
          predictDateFrom: null,
          predictDateTo: null,
          predictionsUrl: 'api/v1.0/predict/model'
        };
    }
});

var PredictionListView = Backbone.View.extend({

    initialize: function () {
      this.listenTo(Predictions, 'sync', this.addAll);
      this.loadPredictions();
    },
    loadPredictions: function() {
      Predictions.url = this.model.get('predictionsUrl')
                + '/' + this.model.get('predictDateFrom').format("YYYY-MM-DD")
                + '/' + this.model.get('predictDateTo').format("YYYY-MM-DD");
      Predictions.fetch();
    },
    addOne: function (prediction) {
      $('#predictions-table')
        .append(new PredictionView({ model: prediction }).render().el);
    },
    addAll: function () {
      if(Predictions.length == 0)
        this.$('.pred-tbl-no-data-row').show();
      else {
        this.$('.pred-tbl-no-data-row').hide();
        Predictions.each(this.addOne, this);
      }
    },
    render: function () {
      this.$el.html(_.template($('#predictions-template').text())(this.model.toJSON()));
      this.$('.predict-game-datepicker')
          .text(this.model.get('predictDateFrom').format("YYYY-MM-DD"))
          .fdatepicker()
          .fdatepicker('update', this.model.get('predictDateFrom').format("YYYY-MM-DD"))
          .on('changeDate', $.proxy(this.gameDateChanged, this));
      return this;
    },
    gameDateChanged: function (ev) {
      var dp = $(ev.target);
      var dateString = dp.data('date');

      this.model.set('predictDateFrom', moment(dateString));
      this.model.set('predictDateTo', moment(dateString).add(1, 'days'));

      dp.text(dateString).fdatepicker('hide');
      this.loadPredictions();
    }
});
