function readDataFromFile(evt) {
    //TODO: check data format correct
    file_name = evt.target.files[0];
	//I added these two lines to display file name, sorry.
	displayFileName = document.getElementById('file_source').value.split("\\")
	document.getElementById('file_display').value = displayFileName[displayFileName.length -1];
    Papa.parse(file_name, {
        header: true,
        complete: function(results) {
            data_raw = results.data;
            for(i in data_raw){
            	if(data_raw[i].SMS == undefined){
            		data_raw.splice(i, 1)
            	}
            }
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
}



function parseAnswers(input){
	// remove all the space first
	options = input.replace(/\s+/g, '').split(';')
	parsed_answer = {}
	for(i = 0; i < options.length; i++){
		option = options[i]
		label = option.split(':')[0]
		answers = option.split(':')[1].split(',')
		for(j = 0; j < answers.length; j++){
			ans = answers[j]
			parsed_answer[ans] = label

		}		
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

function getOptions(answers){
	optionCounter = []
	for(i in answers){
		optionCounter.push(answers[i])
	}
	counter = Counter(optionCounter);
	var options = [];
	for(var key in counter){
		options.push(key)
	}
	options.push('unknown')
	return options;
}