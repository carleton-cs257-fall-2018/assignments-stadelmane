function getBaseURL() {
    var baseURL = 'http://perlman.mathcs.carleton.edu:5103';
        
        //window.location.protocol + '//' + window.location.hostname + ':' + api_port;
    return baseURL;
}

function getTeams(leagueName) {
    
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
    
function appendTeams(options) {
                       
    console.log('Appending...');
    
    var selectBox = document.getElementById('teams');
    
    selectBox.innerHTML = options;
    
    console.log('DONE');
    
}