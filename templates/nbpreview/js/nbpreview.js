(function () {
    var root = this;
    var $file_input = document.querySelector("input#file");
    var $holder = document.querySelector("#notebook-holder");
	var $header = document.querySelector("#header");

    var render_notebook = function (ipynb) {
        var notebook = root.notebook = nb.parse(ipynb);
        while ($holder.hasChildNodes()) {
            $holder.removeChild($holder.lastChild);
        }
        $holder.appendChild(notebook.render());
        Prism.highlightAll();
    };

    var load_file = function (file) {
        var reader = new FileReader();
        reader.onload = function (e) {
            var parsed = JSON.parse(this.result);
            render_notebook(parsed);
        };
        reader.readAsText(file);
    };

    $file_input.onchange = function (e) {
        load_file(this.files[0]);
    };

    window.addEventListener('dragover', function (e) {
        e.stopPropagation();
        e.preventDefault();
        e.dataTransfer.dropEffect = 'copy';
        root.document.body.style.opacity = 0.5;
    }, false);

    window.addEventListener('dragleave', function (e) {
        root.document.body.style.opacity = 1;
    }, false);

    window.addEventListener('drop', function (e) {
        e.stopPropagation();
        e.preventDefault();
        load_file(e.dataTransfer.files[0]);
        $file_input.style.display = "none";
        root.document.body.style.opacity = 1;
    }, false);






	//Another function: input notebook filename from url
	/*init when input file from url*/
	// get parameter from url: http://localhost:8001/?filename=data/w.step1.Figure3.CD4_global_diffmap.ipynb
	function getUrlParam(name) {
		var reg = new RegExp("(^|&)" + name + "=([^&]*)(&|$)");
		var r = window.location.search.substr(1).match(reg);
		if (r != null) return unescape(r[2]); return null;
	}
	
	// ajax function
	function ajax(filename, fn_success, fail_success=console.log){
		//1 create obj
		let xhr=new XMLHttpRequest();
		//2.bind function
		xhr.onreadystatechange = function(){
			if(xhr.readyState==4){
				if((xhr.status>=200 && xhr.status <300)  || xhr.status==304 ){
					fn_success(xhr.responseText);
				}else{
					fn_fail(xhr.status)
				}
			}
		};
		//3.open resource
		xhr.open("get", filename, true);
		//4.send data
		xhr.send();
	}

	// run this when ajax success
	function fn_success(dat){
		var parsed = JSON.parse(dat);
		render_notebook(parsed);
	}
	
	// bind event
    window.addEventListener('load', function (e) {
		var filename=getUrlParam("filename");
		console.log("[01] filename: ", filename)
		var arr=filename.split("\.")
		if("ipynb"==arr[arr.length-1]){
			console.log("[02] this is a notebook file")
			$header.innerHTML += ": <b style='color:red;'>"+filename +"</b>" + " [<a href='/'>Back to home</a>]"
			ajax(filename, fn_success)
		}
    }, false);

}).call(this);