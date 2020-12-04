//'use strict';

        //var dicAggregation = {{aggregation|safe}};
        //console.log(dicAggregation);
        var lowerBound = document.getElementById("lowerBound").value;
        var upperBound = document.getElementById("upperBound").value;
        var selection = [];

        dicAggregation.forEach(createSelection);
            function createSelection(dict) {
                if (dict.key > lowerBound && dict.key < upperBound)
                    selection.push (dict);
            }

        var birthYears = [];
        var amountOfPeople = [];

        selection.forEach(createLists);
            function createLists(dict) {
                birthYears.push (dict.key);
                amountOfPeople.push (dict.doc_count);
            }

        console.log (birthYears);
        console.log (amountOfPeople);

        Vue.use(VueCharts);
            var dashboard = new Vue({
                el: '#dashboard',
                mounted() {
                    this.updateChart();
                },
                data: function data() {
                    return {
                        labels: birthYears,
                        dataset: amountOfPeople
                    };
                },
                methods: {
                    updateChart: function() {
                        var lowerBound = document.getElementById("lowerBound").value;
                        var upperBound = document.getElementById("upperBound").value;
                        var selection = [];

                        dicAggregation.forEach(createSelection);
                            function createSelection(dict) {
                                if (dict.key > lowerBound && dict.key < upperBound)
                                    selection.push (dict);
                            }

                        var birthYears = [];
                        var amountOfPeople = [];

                        selection.forEach(createLists);
                            function createLists(dict) {
                                birthYears.push (dict.key);
                                amountOfPeople.push (dict.doc_count);
                            }
                        this.labels = birthYears;
                        this.dataset = amountOfPeople;
                        //this.update();
                    }
                }
            });
