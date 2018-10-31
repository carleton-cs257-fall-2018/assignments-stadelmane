function getBaseURL() {
    var baseURL = window.location.protocol + '//' + window.location.hostname + ':' 
    + api_port;
    return baseURL;
}

//returns a dictionary with every team from the different leagues
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

//returns a list of dictionaries with every match stat within our data
function addStatsOptions(leagueName) {
    var allStatsUrl = getBaseURL() + '/all_stats/';

    fetch(allStatsUrl, {method: 'get'}) 
    .then((response) => response.json())
    .then(function(allStatsList) {
        
        var options = '';       
        for (var k = 0; k < allStatsList.length; k++) {  
            var stat = allStatsList[k][k];
            if (stat == 'home_team_id' || stat == 'away_team_id' || stat == 'date' 
                || stat == 'final_result'){
            }
            else {
                options += '<option value=' + "'" + stat + "'" + '>' + stat + 
                '</option>';
            }
        }
        appendStats(options);
    })
    .catch(function(error) {
        console.log(error);
    }) 
}

//Creates multi-select box with every stat
function appendStats(options) { 
    var selectBox = document.getElementById('stats');
    selectBox.innerHTML = options;
    $('#stats').multiSelect();
}
    
//Creates multi-select box with every team
function appendTeams(options) {          
    var selectBox = document.getElementById('teams');
    selectBox.innerHTML = options;
    $('#teams').multiSelect();  
}