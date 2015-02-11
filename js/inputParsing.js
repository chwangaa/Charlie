function readDataFromFile(evt) {
    //TODO: check data format correct
    file_name = evt.target.files[0];
    
    Papa.parse(file_name, {
        header: true,
        complete: function(results) {
            data_raw = results.data;
            data_filtered = data_raw;
            CTR_formatValid = validateInput(data_raw[0]);
            if(CTR_formatValid){
     			// if valid, should start interpreting data
     			data_countries = getAttributeList(data_raw, 'Country')
     			data_rstations = getAttributeList(data_raw, 'RStation')
     			sidebar_data = {countries: data_countries, stations: data_rstations}
     			renderSideBars(sidebar_data, '#li_filters')
				}
        }
    });
    //TODO: getNations()
    //TODO: getStations()
    //TODO: renderSideBars(filters)
}



function parseAnswers(input){
	options = input.split(';')
	parsed_answer = {}
	for(i = 0; i < options.length; i++){
		option = options[i]
		label = option.split(':')[0]
		answers = option.split(':')[1].split(',')
		a = []
		for(j = 0; j < answers.length; j++){
			ans = answers[j]
			a.push(ans)
		}
		
		parsed_answer[label] = a
	}
	return parsed_answer
}

function validateInput(data){
	if(data.SMS == undefined){
		CTR_ERROR_MSG = "dataset does not have SMS attribute defined"
		return false;
	}
	else if(data.Country == undefined){
		CTR_ERROR_MSG = "dataset does not have Country attribute defined"
		return false;
	}
	else if(data.RStation == undefined){
		CTR_ERROR_MSG = "dataset does not have RStation attribute defined"
		return false;
	}
	else{
		return true;
	}
}