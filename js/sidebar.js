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
}

function getSelectedCountries(){
  return data_countries;
}

function getSelectedRStations(){
  return data_rstations;
}

function OnChangeCountry(checkbox) {
  if (checkbox.checked) {
      data_countries[data_countries.length] = checkbox.value;
  }
  else {
      var toRemove = checkbox.value;
      var i = 0;
      var newList = [];
      for (i = 0; i < data_countries.length; i++) {
          if (data_countries[i] == checkbox.value) {
              break;
          } else {
              newList[i] = data_countries[i];
          }
      }
      ++i;
      for (; i < data_countries.length; i++) {
          newList[i-1] = data_countries[i];
      }
      data_countries = newList;
  }
  updateData()
}

function OnChangeStation(checkbox) {
    if (checkbox.checked) {
        data_rstations[data_rstations.length] = checkbox.value;
    }
    else {
        var toRemove = checkbox.value;
        var i = 0;
        var newList = [];
        for (i = 0; i < data_rstations.length; i++) {
            if (data_rstations[i] == checkbox.value) {
                break;
            } else {
                newList[i] = data_rstations[i];
            }
        }
        ++i;
        for (; i < data_rstations.length; i++) {
            newList[i-1] = data_rstations[i];
        }
        data_rstations = newList;
    }
    updateData()
}

function renderSideBars(filters, sidebar_id){
    $(sidebar_id).append("Countries:<br>");
        for(var i = 0; i < filters.countries.length; i++) {
            var name = filters.countries[i];
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
        var name = filters.stations[i];
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