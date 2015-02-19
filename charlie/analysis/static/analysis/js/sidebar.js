/*
  handler for box ticking event (the filtering action)
*/
function updateData(){
  countries = getSelectedCountries();
  rstations = getSelectedRStations();
  // progressively filter the texts by country and then by station
  filtered_country = filterByCountry(data_raw, countries)
  data_filtered = filterByStation(filtered_country, rstations)
  data_wordcloud = getWordFrequencyList(data_filtered)
  drawCloudMap(data_wordcloud, '#cloud_tags')
  updateList(data_filtered)
}

function getSelectedCountries(){
  return data_countries;
}

function getSelectedRStations(){
  return data_rstations;
}

function OnChangeCountry(checkbox) {
    if (checkbox.checked) {
        data_countries.push(checkbox.value.toLowerCase())
    }
    else {
        var toRemove = checkbox.value.toLowerCase();
        data_countries = data_countries.filter(function(element) {
          return element != toRemove
        });
    }
    updateData()
}

function OnChangeStation(checkbox) {
    if (checkbox.checked) {
        data_rstations.push(checkbox.value.toLowerCase());
    }
    else {
        var toRemove = checkbox.value.toLowerCase();
        data_rstations = data_rstations.filter(function(element) {
          return element != toRemove
        });
    }
    updateData()
}

function capitalise(string)
{
    words = string.split(" ");
    for (var i = 0; i < words.length; i++) {
        words[i] = words[i].charAt(0).toUpperCase() + words[i].slice(1);
    }
    string = words.join(" ");
    return string;
}

function renderSideBars(filters, sidebar_id){
    $(sidebar_id).append("Countries:<br>");
        for(var i = 0; i < filters.countries.length; i++) {
            var name = capitalise(filters.countries[i]);
            var box = $('<input/>').attr({
                type: "checkbox",
                onclick: "OnChangeCountry(this)",
                checked: "checked",
                value: name
        });
        $(sidebar_id).append(box);
        $(sidebar_id).append(" " + name + "<br>");
    }
    $(sidebar_id).append("Stations:<br>");
    for(var i = 0; i < filters.stations.length; i++) {
        var name = capitalise(filters.stations[i]);
        var box = $('<input/>').attr({
            type: "checkbox",
            onclick: "OnChangeStation(this)",
            checked: "checked",
            value: name
        });
        $(sidebar_id).append(box);
        $(sidebar_id).append(" " + name + "<br>");
    }
}