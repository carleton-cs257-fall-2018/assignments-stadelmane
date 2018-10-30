function getBaseURL() {
    var baseURL = 'http://perlman.mathcs.carleton.edu:5122';
        
        //window.location.protocol + '//' + window.location.hostname + ':' + api_port;
    return baseURL;
}

function addTeamsOptions(leagueName) {
    
    var url = getBaseURL() + '/leagues';
    
    var options = '';
    
    fetch(url, {method: 'get'})
    
    .then((response) => response.json())
    
    .then(function(teamList) {
        
        
        for (var k = 0; k < teamList.length; k++) {
            
            var teamName = teamList[k]['team'];
            
            options += '<option value=' + "'" + k + "'" 
                        + '>' + teamName + '</option>';
                

        }
        appendTeams(options);
        
    })
    
    .catch(function(error) {
        console.log(error);
    })

    
}

function addStatsOptions(leagueName) {
    
        
    var allStatsUrl = getBaseURL() + '/all_stats/';
        
    fetch(allStatsUrl, {method: 'get'})
        
    .then((response) => response.json())
        
    .then(function(allStatsList) {
            
        var options = '';
                
        for (var k = 0; k < allStatsList.length; k++) {
            
            var stat = allStatsList[k][k];
            
            if (stat == 'home_team_id' || stat == 'away_team_id'            || stat == 'date' || stat == 'final_result')                                                       {
    
            }
            
            else {
                    options += '<option value=' + "'" + stat + "'" 
                        + '>' + stat + '</option>';
            }

        }
        appendStats(options);
    })
    
    .catch(function(error) {
        console.log(error);
    })

    
}

function appendStats(options) {
                       
    console.log('Appending...');
    
    var selectBox = document.getElementById('stats');
    
    selectBox.innerHTML = options;
    
    $('#stats').multiSelect();
    
    console.log('DONE');
}
    
    
function appendTeams(options) {
                       
    console.log('Appending...');
    
    var selectBox = document.getElementById('teams');
    
    selectBox.innerHTML = options;
    
    $('#teams').multiSelect();
    
    console.log('DONE');
    
}