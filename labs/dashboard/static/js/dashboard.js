function selectData() {

    var birthYears = [];
    var amountOfPeople = [];

    dicAggregation.forEach(createLists);
        function createLists(dict) {
            birthYears.push (dict.key);
            amountOfPeople.push (dict.doc_count);
        }

    return {
        birthYears: birthYears,
        amountOfPeople: amountOfPeople,
    };
}

var ctx = document.getElementById('chartBirthPerYear').getContext('2d');
var chart = new Chart(ctx, {
    type: 'bar',
    data: {
        labels: selectData().birthYears,
        datasets: [{
            label: 'Amount of People born per Year',
            backgroundColor: 'rgb(255, 99, 132)',
            borderColor: 'rgb(255, 99, 132)',
            data: selectData().amountOfPeople
        }]
    },
    options: {}
});

function updateChart() {
    var lowerYear = document.getElementById("lowerYear").value.trim();
    var upperYear = document.getElementById("upperYear").value.trim();

    if (lowerYear == "") {
        var lowerYear = dicAggregation[0].key;
    }
    if (upperYear == "") {
        var upperYear = dicAggregation[dicAggregation.length - 1].key;
    }

    var selection = [];

    dicAggregation.forEach(createSelection);
        function createSelection(dict) {
            if (dict.key > lowerYear && dict.key < upperYear)
                selection.push (dict);
        }

    var birthYears = [];
    var amountOfPeople = [];

    selection.forEach(createLists);
        function createLists(dict) {
            birthYears.push (dict.key);
            amountOfPeople.push (dict.doc_count);
        }

    chart.data.datasets[0].data = amountOfPeople;
    chart.data.labels = birthYears;
    chart.update();
}



