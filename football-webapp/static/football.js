initialize();

function initialize() {
    addTeamsOptions('');
    addStatsOptions();
    var element = document.getElementById('find_data_button');
    if (element) {
        element.onclick = onFindDataButtonClicked;
    }
}

function getBaseURL() {
    var baseURL = 'http://perlman.mathcs.carleton.edu:5122';
        
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
    
    //var element = document.getElementById('teams');
    
    var teamIdArray = $('#teams').val();
    
    var statsArray = $('#stats').val();
    
    var startDateList = $('#datepickerBEG').val().split('/');
    
    var startDate = startDateList[2] + '-' + startDateList[0] + '-' + startDateList[1];
    
    var endDateList = $('#datepickerEND').val().split('/');
    
    var endDate = endDateList[2] + '-' + endDateList[0] + '-' + endDateList[1];
    
    console.log(startDate);
    
    console.log(endDate);
    
    
    var getAllStats = false;
    
    //var teamId = parseInt(element.options[element.selectedIndex].value) + 1;
    
    var IdString = '';
    
    for (var i = 0; i < teamIdArray.length; i++) {
        
        var apiId = parseInt(teamIdArray[i]) + 1;
        
        if (i == teamIdArray.length - 1) {
            
            
            IdString += apiId;
        }
        else {
            
            IdString += apiId + ',';
            
        }

    }
        
    var url = getBaseURL() + '/match_stats?home_team_id=' + IdString + '&away_team_id=' + IdString;
    
    if (statsArray.length != 0) {
        
        getAllStats = true;
        
        var statsString = '';
        
        
        for (var i = 0; i < statsArray.length; i++) {
        
            if (i == statsArray.length - 1) {
            
                statsString += statsArray[i];
        }
        
        else {
            
                statsString += statsArray[i] + ',';
            
        }
        
        }
        
        url += '&stats=' + statsString;
        
        statsArray.push('home_team_id');
        statsArray.push('away_team_id');
        statsArray.push('date');
        statsArray.push('final_result');
    }
        
    else {
        
        var allStatsUrl = getBaseURL() + '/all_stats/';
        
        fetch(allStatsUrl, {method: 'get'})
        
        .then((response) => response.json())
        
        .then(function(allStatsList) {
            
            statsArray = allStatsList;
            
        })
        
        .catch(function(error) {
            console.log(error);
        })
        
    }
    
    url += '&date=' + startDate + "*" + endDate;

    console.log(url);
    // Send the request to the Books API /authors/ endpoint
    fetch(url, {method: 'get'})
    
    // When the results come back, transform them from JSON string into
    // a Javascript object (in this case, a list of author dictionaries).
    .then((response) => response.json())

    // Once you have your list of author dictionaries, use it to build
    // an HTML table displaying the author names and lifespan.
    .then(function(matchStatsList) {
        
        buildTable(statsArray, matchStatsList);
    
    })
       
    // Log the error if anything went wrong during the fetch.
    .catch(function(error) {
        console.log(error);
    })
        
    function buildTable(statsArray, matchStatsList) {   
        // Build the table body.
        var tableBody = '';

        var optionValues = [];

        $('#teams option').each(function() {
            optionValues.push($(this).text());
        });
        
        for (var k = 0; k < matchStatsList.length; k++) {
            
            
            
            tableBody += '<tr>';
            tableBody += '<td>';
            
    
            for (var j = 0; j < statsArray.length; j++) {
               
                if (getAllStats) {
                    
                    var currentStat = statsArray[j];
                    
                }
                
                else {
                    
                    var currentStat = statsArray[j][j];
                }
                
    
                if (currentStat == "home_team_id" || currentStat == "away_team_id"){
                    teamId = matchStatsList[k][currentStat];
                    teamName = optionValues[teamId-1];
                    if (currentStat == "home_team_id"){
                        currentStat = "home_team";
                    }
                    else{
                        currentStat = "away_team";


                    }
                    tableBody += currentStat + ': '+ teamName + ' ';

                }
                else{
                    tableBody += currentStat + ': '+ matchStatsList[k][currentStat] + ' ';

                }
            }




            tableBody += '</td>';
            
            
            tableBody += '</tr>';
            tableBody += '<tr></tr><tr></tr><tr></tr><td><hr></td>';
        }
        var tableColumns = [];
        for (var i = 0; i < statsArray.length(); i++){
            tableColumns.append({
                name : statsArray[i],
                type : 'String',
                visible : true,
                filterType : 'list',
                width : 200
            });
        console.log(tableColumns);

        }


        // Put the table body we just built inside the table that's already on the page.
        var resultsTableElement = document.getElementById('results_table');
        if (resultsTableElement) {
            resultsTableElement.innerHTML = tableBody;
        }
    
    }
    

}







