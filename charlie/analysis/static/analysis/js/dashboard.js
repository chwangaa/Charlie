document.getElementById('addbutton').addEventListener("click",
            function(e){
                document.getElementById("overlay").style.display='block';
				document.getElementById("upload_data").style.display='block';  
        });
		
document.getElementById('cancel').addEventListener("click",
            function(e){
                document.getElementById("overlay").style.display='none';
				document.getElementById("upload_data").style.display='none';  
        });
		
document.getElementById('delete').addEventListener("click",
	function(e){
		//TODO: Remove data from data source, rerender page
	});