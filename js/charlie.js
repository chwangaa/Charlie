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
		if('SMS' in entry){
			words = words.concat(entry['SMS'].toLowerCase().split(' '))
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
		attribute_list.push(value);
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
		var country_name = e.Country;
		return (country_names.indexOf(e.Country)>=0);
	}
	return data.filter(f);
}

function filterByStation(data, station_names){
	function f(e){
		var station_name = e.Country;
		return (station_names.indexOf(e.RStation)>=0);
	}
	return data.filter(f);	
}