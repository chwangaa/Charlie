var fullscreen = false;
document.getElementById('toggle').addEventListener("click",
            function(e){
			if (fullscreen==false){
				$("#wrapper").toggleClass("toggled");
				document.getElementById('toggle').className="glyphicon glyphicon-resize-small full_icon";
				document.getElementById('navbar').style.zIndex=-1;
				document.getElementById('page-content-wrapper').style.top = 0;
				document.getElementById('page-content-wrapper').style.left = 0;
				document.getElementById('page-content-wrapper').style.right = 0;
				fullscreen = true;
			}else{				
				$("#wrapper").toggleClass("toggled");
				document.getElementById('toggle').className="glyphicon glyphicon-fullscreen full_icon";
				document.getElementById('navbar').style.zIndex=5;
				document.getElementById('page-content-wrapper').style.top = "50px";
				document.getElementById('page-content-wrapper').style.left = "250px";
				fullscreen = false;
			}
			
        });
$("#toggle").trigger("click");
