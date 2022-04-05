var AutoSave = (function(){

	var timer = null;

	function getEditor(){

		var elems = document.getElementById("durat").innerHTML
		if (elems.length <= 0)
			return null;

		return elems[0];
	}


	function save(){

		var editor = getEditor(); 
                if (editor) {
		    localStorage.setItem("AUTOSAVE_" + document.location, editor.value )
                }

	}


	function restore(){

		var saved = localStorage.getItem("AUTOSAVE_" + document.location)
		var editor = getEditor();
		if (saved && editor){

			editor.value = saved; 
		}
	}

	return { 

		start: function(){

			var editor = getEditor(); 

		 
			if (editor.value.length == 0)
				restore();

			if (timer != null){
				clearInterval(timer);
				timer = null;
			}

			timer = setInterval(save, 1000);


		},

		stop: function(){

			if (timer){ 
				clearInterval(timer);
				timer = null;
			}

		}
	}

}())