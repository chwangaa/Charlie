document.getElementById('keyword-add-btn').addEventListener('click',
	function() {
		word = document.getElementById('keyword-add-text').value;
		document.getElementById('keyword-add-text').value = "";
		console.log(word);
		data_keywords.push(word);
		console.log(data_keywords);

		// Adding new words to keyword-list.
		var new_item =
			"<li><div class=\"input-group\"><div class=\"input-group-btn\"><span class=\"input-group-addon\"><input type=\"checkbox\"/></span><span class=\"input-group-btn\"><button class=\"btn btn-default\" type=\"button\">Relate</button></span></div><!-- input-group-btn --><span id=\"keyword-entry\">"+word+"</span></div><!-- /input-group --></li>"
		$('#keyword-list').append(new_item);
	});
