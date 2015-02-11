  var poll

  function handleFileSelect(evt) {
    var file = evt.target.files[0];
 
    Papa.parse(file, {
      header: true,
      complete: function(results) {
        var data = results.data;
        poll = new Poll(data, options)
        poll.renderChart()
        $('#container').show()
      }
    });
  }

  function initialize(){
  	poll = null;
  	$('#container').hide();
  	$('#example').hide();
  }

  function updatePollOption(poll, op){
  	if(op in poll){
  		poll[op] += 1
  	}
  	else{
  		poll[op] = 1
  	}
  }

  // needs to be user input
  var options = {"aids": "aids",
					"hiv": "aids",
					"malaria": "malaria",
					"maleria": "malaria"}

  function Poll(data, options){
  	var poll = {}
  	for(var d in data){
  		sms = data[d]
  		if('SMS' in sms){
  			var text = sms['SMS']
  			// console.log(text)
        opinionFound = false;
  			for(var op in options){
  				if(text.toLowerCase().indexOf(op) != -1){
  					// the SMS contains this keywords
  					updatePollOption(poll, options[op])
  					sms["opinion"] = options[op]
            opinionFound = true;
  					break
  				}
  			}
        if(opinionFound == false){
          sms["opinion"] = ''
        }
  		}
  	}
  	this.poll = poll
  	this.data = data

  	this.getPollSeries = function(){
  		var list_data = []
  		for(var entry in this.poll){
  			var pair = []
  			pair.push(entry)
  			pair.push(this.poll[entry])
  			list_data.push(pair)
  		}
  		return list_data
  	}



  	this.renderChart = function(){
  	return new Highcharts.Chart({
        chart: {
            renderTo: "page_charts",
            type: 'pie'
        },

        title: {
            text: data_question
        },

        plotOptions: {
        	pie: {
        		allowPointSelect: true
        	},
            series: {
                cursor: 'pointer',
                point: {
                    events: {
                        click: function () {
                            var opinion = this.name
                            // bugged
                            renderCloud(opinion)
                        }
                    }
                }
            }
        },

        series: [{
            type: 'pie',
            name: 'Group Charlie Test',
            data: this.getPollSeries()
        }]
	});
  }
  }


  function Counter(list){
  	var counter = {}
  	for(var i = 0, j = list.length; i < j; i++){
  		counter[list[i]] = (counter[list[i]] || 0) + 1;
  	}
  	return counter
  }


function generateCloud(word_array){
      $(function() {
        // When DOM is ready, select the container element and call the jQCloud method, passing the array of words as the first argument.
        $("#example").jQCloud(word_array);
      });
}


  	function getCounter(data){
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