function Counter(list){
	var counter = {}
	for(var i = 0, j = list.length; i < j; i++){
	   counter[list[i]] = (counter[list[i]] || 0) + 1;
	}
	return counter
}


function getWordFrequencyList(data){
	var words = []
	for(var i in data){
		var entry = data[i]
		if('modified_text' in entry) {
			var sms = entry['modified_text'].toLowerCase()
			// Remove non alphanumerical characters.
			sms = sms.replace(/\W+/g, ' ');
			sms = sms.split(' ');
			// Filter empty strings.
			sms = sms.filter(function(element) {
		        return element.replace(/\s+/g, ' ') != "";
		    });
		    words = words.concat(sms);
		}
	}
	
 	var counter = Counter(words)
	var word_list = []
	for(var key in counter){
		var c = {text: key, weight: counter[key]}
		word_list.push(c)
	}
	word_list.sort(function(a,b){
		return b["weight"] - a["weight"]
	})
  
  return word_list
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