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
  applyFiltersToTables(countries, rstations);
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

function OnChangeStation(checkbox) {
    console.log("Changed opinion!");
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
    $(sidebar_id).append("<h5>Countries:</h5>");
    var ul = $('<ul/>').addClass('list-unstyled');
    for(var i = 0; i < filters.countries.length; i++) {
        var li = $('<li/>')
            .appendTo(ul);
        var name = capitalise(filters.countries[i]);
        var box = $('<input/>').attr({
                type: "checkbox",
                onclick: "OnChangeCountry(this)",
                checked: "checked",
                value: name
            })
            .appendTo(li);
        var label = $('<label>').html(name)
            .appendTo(li);
    }

    $(sidebar_id).append(ul);
    $(sidebar_id).append("<h5>Stations:</h5>");
    ul = $('<ul/>').addClass('list-unstyled');
    for(var i = 0; i < filters.stations.length; i++) {
        var li = $('<li/>')
            .appendTo(ul);
        var name = capitalise(filters.stations[i]);
        var box = $('<input/>').attr({
                type: "checkbox",
                onclick: "OnChangeStation(this)",
                checked: "checked",
                value: name
            })
            .appendTo(li);
        var label = $('<label>').html(name)
            .appendTo(li);
    }
    $(sidebar_id).append(ul);
}


var data_raw;
var data_wordfreq;
var data_filtered;
var data_countries;
var data_rstations;
var data_answers;
var data_question;
var data_options;
var table;

// global state variables
var WINDOW = {
    HOME: {id: 'page_dashboard'},
    UPLOAD: {id: 'page_upload'},
    CHART: {id: 'page_charts'},
    CLOUD: {id: 'page_cloudmap'},
    LIST: {id: 'page_text'}
}

var CTR_WINDOW;
var CTR_TABLE_INITIALIZED;
$("#wrapper").toggleClass("toggled");
switchView();


$("#menu-toggle").click(function(e) {
    e.preventDefault();
    $("#wrapper").toggleClass("toggled");
});

$('[switch-view]').click(function (e) {
    e.preventDefault();
    var x = $(this).attr('switch-view');
    if(x == 'page_cloudmap'){
        CTR_WINDOW = WINDOW.CLOUD
    }
    else if(x == 'page_charts'){
        CTR_WINDOW = WINDOW.CHART
    }
    else if(x == 'page_text'){
        CTR_WINDOW  = WINDOW.LIST
    }
    switchView()
});
/* 
    to change the page based on the value of CTR_WINDOW
*/
function switchView(){
    //TODO: precise FSM specification
    $(' .view').hide();
/*
    if(CTR_WINDOW == WINDOW.CHART){
        $('#filters').hide()
    }
    else{
        $('#filters').show()
    }
*/
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

// TODO(Daria): Delete this? Seems to be just for testing. Talk to others.
function create_post() {
    console.log("create post is working!") // sanity check
    $.ajax({
        url : "/analysis/1/update/", // the endpoint
        type : "POST", // http method
        data : { the_post : "haha" }, // data sent with the post request

        // handle a successful response
        success : function(json) {
            $('#post-text').val(''); // remove the value from the input
            console.log(json); // log the returned json to the console
            console.log("success"); // another sanity check
        },

        // handle a non-successful response
        error : function(xhr,errmsg,err) {
            $('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: "+errmsg+
                " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
            console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
        }
    });
};
    
//Collapse filters - if you're here to clean up, this only exists here atm
