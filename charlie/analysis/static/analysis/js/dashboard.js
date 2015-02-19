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

var deleteButtons = document.querySelectorAll('.delete');

for (var i = 0; i < deleteButtons.length; i++) {
    deleteButtons[i].addEventListener('click', function(e) {
		createDeleteRequest('#'+e.target.id);
    });
}

function createDeleteRequest(container) {
	// Id in HTML is of form #datasource192, and we only need "192".
	document_id = container.replace("#datasource", "");
    $.ajax({
        url : "delete-datasource/", // the endpoint
        type : "POST", // http method
        data : { document_id : document_id }, // data sent with the post request

        // handle a successful response
        success : function(json) {
            $(container).parent().remove(); // remove the value from the input
        },

        // handle a non-successful response
        error : function(xhr,errmsg,err) {
            $('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: "+errmsg+
                " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
            console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
        }
    });
};