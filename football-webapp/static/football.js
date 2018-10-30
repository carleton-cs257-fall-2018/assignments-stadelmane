initialize();

function initialize() {
    var element = document.getElementById('find_data_button');
    if (element) {
        element.onclick = onFindDataButtonClicked;
    }
}

function getBaseURL() {
    var baseURL = 'http://perlman.mathcs.carleton.edu:5103';
        
        //window.location.protocol + '//' + window.location.hostname + ':' + api_port;
    return baseURL;
}

//function getTeamId(teamName) {
//    
//    var url = getBaseURL() + '/team/' + teamName;
//    
//    console.log(url);
//    
//    var teamId = 0;
//    
//    fetch(url, {method: 'get'})
//    
//    .then((response) => response.json())
//    
//    .then(function(teamName) {
//        
//        teamId = teamName[0]['id'];
//        return teamId;
//        })
//    
//    .catch(function(error) {
//        console.log(error);
//    })
//    
//    
//}


function onFindDataButtonClicked() {
    
    var element = document.getElementById('teams');
    
    var teamId = parseInt(element.options[element.selectedIndex].value) + 1;
        
    var url = getBaseURL() + '/match_stats?home_team_id=' + teamId + '&away_team_id=' + teamId;

    console.log(url);
    // Send the request to the Books API /authors/ endpoint
    fetch(url, {method: 'get'})
    

    // When the results come back, transform them from JSON string into
    // a Javascript object (in this case, a list of author dictionaries).
    .then((response) => response.json())

    // Once you have your list of author dictionaries, use it to build
    // an HTML table displaying the author names and lifespan.
    .then(function(statsList) {
        
        var allStats = [];
        
        var allStatsUrl = getBaseURL() + '/all_stats/';
        
        fetch(allStatsUrl, {method: 'get'})
        
        .then((response) => response.json())
        
        .then(function(allStatsList) {
            
            allStats = allStatsList;
            buildTable(allStats, statsList);
        })
        .catch(function(error) {
            console.log(error);
        })
    })
       
    // Log the error if anything went wrong during the fetch.
    .catch(function(error) {
        console.log(error);
    })
        
    function buildTable(allStats, statsList) {   
        // Build the table body.
        var tableBody = '';
        for (var k = 0; k < statsList.length; k++) {
            
            
            
            tableBody += '<tr>';
            tableBody += '<td>';
            
    
            for (var j = 0; j < allStats.length; j++) {
               
                
                var currentStat = allStats[j][j];
                
                console.log(currentStat);
                
                tableBody += currentStat + ' : '+ statsList[k][currentStat] + ' ';
            
            }
            tableBody += '</td>';
            
            
            tableBody += '</tr>';
        }


        // Put the table body we just built inside the table that's already on the page.
        var resultsTableElement = document.getElementById('results_table');
        if (resultsTableElement) {
            resultsTableElement.innerHTML = tableBody;
        }
    
    }
    

}






