/*
  handler for box ticking event (the filtering action)
*/
function updateData(){
  countries = getSelectedCountries();
  rstations = getSelectedRStations();
  opinions = getSelectedOpinions();
  // progressively filter the texts by country, then by station, then by opinion
  filtered_country = filterByCountry(data_raw, countries)
  filtered_station = filterByStation(filtered_country, rstations)
  data_filtered = filterByOpinion(filtered_station, opinions)
  getWordFrequencyListAjax(data_filtered)
  applyFiltersToTables(countries, rstations, opinions);
}

function getSelectedOpinions(){
  return data_opinions;
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
          return element.toLowerCase() != toRemove
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
          return element.toLowerCase() != toRemove
        });
    }
    updateData()
}

function OnChangeOpinion(checkbox) {
    if (checkbox.checked) {
        data_opinions.push(checkbox.value.toLowerCase());
    }
    else {
        var toRemove = checkbox.value.toLowerCase();
        data_opinions = data_opinions.filter(function(element) {
          return element.toLowerCase() != toRemove
        });
    }
    updateData()
}

function OnChangeWord(checkbox) {
    // When unchecking the box, remove the word from the filter list.
    if (!checkbox.checked) {
        var id = '#word_' + checkbox.value;
        data_clicked_words = data_clicked_words.filter(function(e) {
            return e != checkbox.value;
        });
        $(id).remove();
        if (data_clicked_words.length == 0) {
            $('#filterbyword').hide();
            $('#wordfilter').hide();
        }
        applyWordFilterToTable();
    }
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

function renderSideBars(filters){
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
    $('#countryfilter').append(ul);
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
    $('#stationfilter').append(ul);
    ul = $('<ul/>').addClass('list-unstyled');
    for(var i = 0; i < filters.opinions.length; i++) {
        var li = $('<li/>')
            .appendTo(ul);
        var name = capitalise(filters.opinions[i]);
        var box = $('<input/>').attr({
                type: "checkbox",
                onclick: "OnChangeOpinion(this)",
                checked: "checked",
                value: name
            })
            .appendTo(li);
        var label = $('<label>').html(name)
            .appendTo(li);
    }
    $('#opinionfilter').append(ul);

    ul = $('<ul/>').addClass('list-unstyled');
    $('#wordfilter').append(ul);

    $('#filterbyword').hide();
    $('#wordfilter').hide();
}

function appendWordFilterToSidebar(word) {
    var ul = document.getElementById('wordfilter').getElementsByTagName('ul')
    var li = $('<li/>')
        .attr({id: 'word_'+word})
        .appendTo(ul);
    var box = $('<input/>').attr({
            type: "checkbox",
            onclick: "OnChangeWord(this)",
            checked: "checked",
            value: word
        })
        .appendTo(li);
    var label = $('<label>').html(word)
        .appendTo(li);

    if (data_clicked_words.length == 1) {
        $('#filterbyword').show();
        $('#wordfilter').show();
        showWordFilter = true;
        document.getElementById("arrow4").className="glyphicon glyphicon-triangle-top arrow";
    }
}


var data_raw;
var data_wordfreq;
var data_filtered;
var data_countries;
var data_rstations;
var data_opinions;
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
