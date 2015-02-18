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
        // Initial speed in [x, y] direction.
        initial: [0.2, 0.2],
        // Minimum speed when mouse leaves canvas.
        minSpeed: 0.02,
        maxSpeed: 0.02,
        weight: true,
        weightFrom: 'data-weight'
    });
}

/*
    Scale the frequencies to be in the range 20-120 (font size), but keep proportions.
    Values are chosen after trying different weight ranges, so they are hardcoded.
*/
function reWeigh(words) {
    var highest_freq = words[0].weight;
    var lowest_freq = words[words.length - 1].weight;
    var interval = highest_freq - lowest_freq;
    for (var i = 0; i < words.length; i++) {
        // Rescale by (100/interval) and translate by 20 (minimum weight).
        words[i].weight = 20 + Math.round(((words[i].weight - lowest_freq) * 100) / interval);
    }
    return words;
}

/*
    Appends list of words into HTML as a list, then calls function to set up canvas.
    The tag container should be different than the canvas container, as required by the TagCanvas library.
    TODO(Daria): Pass appropriate container here (might need multiple ones).
*/
function drawCloudMap(words, container) {
    var colour;
    words = words.slice(0,30);

    // TODO: Remove this, but only once strings only containing whitespace are filtered elsewhere!
    words = words.filter(function(element) {
        return element.text.replace(/\s+/g, ' ') != "";
    });

    words = reWeigh(words);
    list = "<ul>";
    for(var i = 0; i < words.length; i++) {
        text = words[i].text;
        weight = words[i].weight;
        topic = words[i].topic;
        if (words[i].topic != null) {
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