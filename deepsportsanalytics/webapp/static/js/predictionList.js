var PredictionListModel = Backbone.Model.extend({
    defaults: function () {
        return {
          modelName: null,
          dataSource: null,
          filter: null,
          predictDateFrom: null,
          predictDateTo: null,
          predictionsUrl: 'api/v1.0/predict',
          predictions: new PredictionList
        };
    }
});

var PredictionListView = Backbone.View.extend({
    initialize: function () {
      this.listenTo(this.model.get('predictions'), 'sync', this.addAll);
    },
    loadPredictions: function() {
      this.resetList();
      this.setNoData(false);
      this.setLoading(true);

      var preds = this.model.get('predictions');
      preds.url = this.model.get('predictionsUrl')
                + '/' + this.model.get('modelName')
                + '/' + this.model.get('dataSource')
                + '/' + this.model.get('predictDateFrom').format("YYYY-MM-DD")
                + '/' + this.model.get('predictDateTo').format("YYYY-MM-DD");
      preds.fetch();
    },
    addOne: function (prediction) {
      if (!prediction.isNull())
        this.$('.predictions-table-tbody')
          .append(new PredictionView({ model: prediction }).render().el);
      else
        this.setNoData(true);
    },
    addAll: function () {
      var preds = this.model.get('predictions');
      if(preds.length == 0)
        this.setNoData(true);
      else {
        this.setNoData(false);
        preds.each(this.addOne, this);
      }
      this.setLoading(false);
    },
    setNoData: function(set) {
      var noDataRow = this.$('.pred-tbl-no-data-row');
      if(set)
        noDataRow.show();
      else
        noDataRow.hide();
    },
    setLoading: function(set) {
      var loadingRow = this.$('.pred-tbl-loading-row');
      if(set)
        loadingRow.show();
      else
        loadingRow.hide();
    },
    render: function () {
      this.$el.html(_.template($('#predictions-template').text())(this.model.toJSON()));
      this.$('.predict-game-datepicker')
          .text(this.model.get('predictDateFrom').format("YYYY-MM-DD"))
          .fdatepicker()
          .fdatepicker('update', this.model.get('predictDateFrom').format("YYYY-MM-DD"))
          .on('changeDate', $.proxy(this.gameDateChanged, this));
      this.loadPredictions();
      return this;
    },
    gameDateChanged: function (ev) {
      var dp = $(ev.target);
      var dateString = dp.data('date');

      this.model.set('predictDateFrom', moment(dateString));
      this.model.set('predictDateTo', moment(dateString).add(1, 'days'));

      dp.text(dateString).fdatepicker('hide');
      this.loadPredictions();
    },
    resetList: function() {
      this.$('tr[prediction]').remove();
    }
});
