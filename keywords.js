document.getElementById('keyword-add-btn').addEventListener('click',
	function() {
		textbox = document.getElementById('keyword-add-text');
		word = textbox.innerHTML;
		textbox.clear();
		console.log(word);
		data_keywords.push(word);
	});

function addKeyword(word) {
	data_keywords.push(word);	
}