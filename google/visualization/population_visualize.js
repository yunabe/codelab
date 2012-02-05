
var visualizePyramid = function(div, width, height) {
    google.load('visualization', '1', {'packages':['motionchart']});
    google.setOnLoadCallback(function() {
        var data = new google.visualization.DataTable();
        data.addColumn('string', 'Age');
        data.addColumn('number', 'Year');
        data.addColumn('number', 'Age');
        data.addColumn('number', 'Population');
        data.addColumn('string', 'Sex');
        data.addRows(pyramidData);
        var chart = new google.visualization.MotionChart(div);
        chart.draw(data, {'width': width, 'height':height});
    });
};

var visualizePopulation = function(div, width, height) {
    google.load("visualization", "1", {packages:["corechart"]});
    google.setOnLoadCallback(function() {
        var data = new google.visualization.DataTable();
        data.addColumn('string', 'Year');
        for (var i = 0; i < populationColumns.length; ++i) {
            data.addColumn('number', populationColumns[i]);
        }
        data.addRows(populationData);
        var chart = new google.visualization.AreaChart(div);
        chart.draw(data, {'width': width, 'height': height, 'title': 'Population',
                          'vAxis': {'minValue': 0},
                          'hAxis': {'title': 'Year', 'titleTextStyle': {'color': '#FF0000'}}
                         });
    });
};

var visualizeRatio = function(div, width, height) {
    google.load("visualization", "1", {packages:["corechart"]});
    google.setOnLoadCallback(function() {
        var data = new google.visualization.DataTable();
        data.addColumn('string', 'Year');
        for (var i = 0; i < ratioColumns.length; ++i) {
            data.addColumn('number', ratioColumns[i]);
        }
        data.addRows(ratioData);
        var chart = new google.visualization.AreaChart(div);
        chart.draw(data, {'width': width, 'height': height, 'title': 'Ratio',
                          'vAxis': {'minValue': 0},
                          'hAxis': {'title': 'Year', 'titleTextStyle': {'color': '#FF0000'}}
                         });
    });
};

var visualizeEligibility = function(div, width, height) {
    google.load("visualization", "1", {packages:["corechart"]});
    google.setOnLoadCallback(function() {
        var data = new google.visualization.DataTable();
        data.addColumn('string', 'Year');
        for (var i = 0; i < eligibilityColumns.length; ++i) {
            data.addColumn('number', eligibilityColumns[i]);
        }
        data.addRows(elibitilibyNumRows);
        for (var i = 0; i < eligibilityData.length; ++i) {
            data.setValue(eligibilityData[i][0],
                          eligibilityData[i][1],
                          eligibilityData[i][2]);
        }
        var chart = new google.visualization.AreaChart(div);
        chart.draw(data, {'width': width, 'height': height, 'title': 'Eligibility Age',
                          'vAxis': {'minValue': 55},
                          'hAxis': {'title': 'Year', 'titleTextStyle': {'color': '#FF0000'}}
                         });
    });
};
