/*  
    Each topic has its specific colour, and the "undefined" class of words has a different colour (words that have not been categorized into one topic or the other.)
    This supports 2 topics. We should handle this list separately in order to support more flexibility. 
*/
var topicColour = ["grey", "red", "green"];

/*
    The following function using the TagCanvas library to set up a canvas. Must be called only after the list of tags is rendered in HTML.
*/
function setUpCanvas() {
    TagCanvas.Start('cloud_canvas','cloud_tags',{
        textColour: null,
        outlineColour: '#ff00ff',
        reverse: true,
        depth: 0.8,
        maxSpeed: 0.05,
        weight: true,
        weightFrom: 'data-weight'
    });
}

/*
    Appends list of words into HTML as a list, then calls function to set up canvas.
    The tag container should be different than the canvas container, as required by the TagCanvas library.
    TODO(Daria): Pass appropriate container here (might need multiple ones).
*/
function drawCloudMap(words, container) {
    var colour;
    words = words.slice(0,30);
    list = "<ul>";
    for(w in words){
        text = words[w].text;
        weight = words[w].weight;
        topic = words[w].topic;
        if (words[w].topic != null) {
            colour = topicColour[topic];
        } else {
            colour = topicColour[0];
        }
        new_item = "<li> <a data-weight="+weight+" id=" +text+ " style=\"color:"+colour+"\" href=\"#\">"+text+"</a></li>"
        list = list.concat(new_item)
    }
    list = list.concat("</ul>");
    $(container).empty().append(list)
    try {
      setUpCanvas();
    } catch(e) {
      // If something went wrong, hide the canvas container.
      document.getElementById('#page_cloudmap').style.display = 'none';
    }
}

function resizeCanvas() {
	var canvas = document.getElementById('cloud_canvas'),
            context = canvas.getContext('2d');
	var canvas_container = document.getElementById('canvas_container');
	canvas.width = canvas_container.offsetWidth - 40;
	canvas.height = canvas_container.offsetHeight - 40;
}