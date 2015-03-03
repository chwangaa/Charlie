function Counter(list){
	var counter = {}
	for(var i = 0, j = list.length; i < j; i++){
	   counter[list[i]] = (counter[list[i]] || 0) + 1;
	}
	return counter
}


function getWordFrequencyListAjax(data){
	var words = ""
	for(var i in data){
		var entry = data[i]
		if('modified_text' in entry) {
			words = words + " " + entry['modified_text']
		}
	}
    $.ajax({
        // This will go to /analysis/datasource_id/manip/update/
        url : "renderWordCloud/", // the endpoint
        type : "POST", // http method
        data : {'data': words}, // data sent with the post request
        // handle a successful response
        success : function(json) {
            freqs = json.data
  			drawCloudMap(freqs, '#cloud_tags')
        },
        // handle a non-successful response
        error : function(xhr,errmsg,err) {
        	console.log("severe error here")
        }
    });
}


function getAttributeList(data, attribute){
	var attribute_list = [];
	for(i in data){
		var sms = data[i];
		var value = sms[attribute];
		if(value != undefined){
			attribute_list.push(value);
		}
	}
	var counter = Counter(attribute_list);
	var unique_attributes = [];
	for(var key in counter){
		unique_attributes.push(key)
	}
	return unique_attributes;
}

function filterByCountry(data, country_names){
	function f(e){
		var country_name = e.Country.toLowerCase();
		return (country_names.indexOf(country_name)>=0);
	}
	return data.filter(f);
}

function filterByStation(data, station_names){
	function f(e){
		var station_name = e.RStation.toLowerCase();
		return (station_names.indexOf(station_name)>=0);
	}
	return data.filter(f);	
}

function filterByOpinion(data, opinion_names){
	function f(e){
		var opinion = e.opinion.toLowerCase();
		return (opinion_names.indexOf(opinion)>=0);
	}
	return data.filter(f);
}

function filterBy(data, attribute, value){
	function f(e){
		return (e[attribute] == value);
	}
	return data.filter(f);
}


var csrftoken = $.cookie('csrftoken');

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});