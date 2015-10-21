var PredictionListModel = Backbone.Model.extend({
    defaults: function () {
        return {
          filter: null,
          predictDateFrom: null,
          predictDateTo: null,
          predictionsUrl: 'api/v1.0/predict/model'
        };
    },
    loadPredictions: function(){
      Predictions.url = this.attributes['predictionsUrl']
                + '/' + this.attributes['predictDateFrom'].format("YYYY-MM-DD")
                + '/' + this.attributes['predictDateTo'].format("YYYY-MM-DD");
      Predictions.fetch();
    },

});

var PredictionListView = Backbone.View.extend({
    initialize: function () {
      this.listenTo(Predictions, 'sync', this.addAll);
    },
    loadPredictions: function() {
      this.resetList();
      this.setNoData(false);
      this.setLoading(true);
      this.model.loadPredictions();
    },
    addOne: function (prediction) {
      if (!prediction.isNull())
        $('.predictions-table-tbody')
          .append(new PredictionView({ model: prediction }).render().el);
      else
        this.setNoData(true);
    },
    addAll: function () {
      if(Predictions.length == 0)
        this.setNoData(true);
      else {
        this.setNoData(false);
        Predictions.each(this.addOne, this);
      }
      this.setLoading(false);
    },
    setNoData: function(set) {
      if(set)
        this.$('.pred-tbl-no-data-row').show();
      else
        this.$('.pred-tbl-no-data-row').hide();
    },
    setLoading: function(set) {
      if(set)
        this.$('.pred-tbl-loading-row').show();
      else
        this.$('.pred-tbl-loading-row').hide();
    },
    render: function () {
      this.$el.html(_.template($('#predictions-template').text())(this.model.toJSON()));
      this.$el.append(
        new StatModelStateView({
          model: new StatModelStateModel({ id: 'model' })
        }).render().el)
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
