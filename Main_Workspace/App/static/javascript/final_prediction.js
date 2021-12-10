async function get_data(type) {
    try {
        response = await fetch(`http://127.0.0.1:5000/get_target_data/${type}`, {
            headers: {
                "Content-Type": "Application/json"
            }
        })
        console.log(response)
        result = await response.json()
        console.log(result)
        data = [
            ['Date', 'ARIMA Prediction', 'SARIMA Prediction', 'Final Excepted Prediction']
        ]
        for (let i = 0; i < 15; i++) {
            tempdata = []
            tempdata.push(result['Future Dates'][i])
            tempdata.push(result['ARIMA Prediction'][i])
            tempdata.push(result['SARIMA Prediction'][i])
            tempdata.push(result['Final Excepted Prediction'][i])
            data.push(tempdata)
        }
        return data
    } catch (error) {
        console.log(error);
    }
}

get_data()

google.charts.load('current', {
    'packages': ['corechart']
});
google.charts.setOnLoadCallback(drawChart);
async function drawChart() {
    data = get_data('confirmed')
    console.log(data);
    var data = google.visualization.arrayToDataTable(data);
    var options = {
        title: 'Covid-19 Active cases prediction',
        curveType: 'function',
        legend: {
            position: 'bottom'
        }
    };
    var chart = new google.visualization.LineChart(document.getElementById('curve_chart'));
    chart.draw(data, options);
}

// async function getOverallGraph(object) {
//     try {
//         let response= await fetch(`http://127.0.0.1:5000/get_graph/${object}`)
//     } catch (error) {
//         console.log(error);
//     }
// }


