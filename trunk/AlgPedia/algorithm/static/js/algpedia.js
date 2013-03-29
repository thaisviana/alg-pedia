
	$(function() {	
	$("#inputAuthor").attr("readonly", true);
		$("#Unknown").attr("checked", true);
		/*$('#algorithm_about').wysihtml5({
			"font-styles": true, //Font styling, e.g. h1, h2, etc. Default true
			"emphasis": true, //Italics, bold, etc. Default true
			"lists": true, //(Un)ordered lists, e.g. Bullets, Numbers. Default true
			"html": false, //Button which allows you to edit the generated HTML. Default false
			"link": true, //Button to insert a link. Default true
			"image": true, //Button to insert an image. Default true,
			"color": false //Button to change color of font  
		});*/

		$("#Unknown").click(function() {
			if ($('#Unknown').attr('checked')) {
				$("#inputAuthor").val("");
				$("#inputAuthor").attr("readonly", true);
				$("#Unknown").attr("checked", true);
			} else {
				$("#inputAuthor").attr("readonly", false);
				$("#Unknown").attr("checked", false);
			}
		});
		$("#add_imp").click(function() {
			var form = document.forms[0];
			
			var imp_code = tinymce.get('algorithm_code').getContent();
		
			var p_lang_id = form['programming_languages'].value;
			var alg_id = form['algorithm_id'].value;
			//window.location = "http://localhost:8000/show/alg/id/"+alg_id;
			window.location = "http://localhost:8000/added/imp/alg/"+alg_id+"/"+p_lang_id+"/"+imp_code;
			
			//alg_id / language_id / implementation /
			
		});
			
			tinyMCE.init({
					// General options
					mode : "textareas",
					theme : "advanced",
					plugins : "autolink,lists,spellchecker,pagebreak,style,layer,table,save,advhr,advimage,advlink,emotions,iespell,inlinepopups,insertdatetime,preview,media,searchreplace,print,contextmenu,paste,directionality,fullscreen,noneditable,visualchars,nonbreaking,xhtmlxtras,template",

					// Theme options
					theme_advanced_buttons1 : "fontsizeselect,fullscreen",
					theme_advanced_buttons2 : "cut,copy,paste,|,search,replace,|,outdent,indent",
					theme_advanced_toolbar_location : "top",
					theme_advanced_toolbar_align : "left",
					theme_advanced_statusbar_location : "bottom",
					theme_advanced_resizing : true,

					// Skin options
					skin : "o2k7",
					skin_variant : "silver",
			});
		$("#add_implementation").click(function(){
		if($('#logged').val()== 'false'){
			bootbox.alert("You have to login first");
		}else{			
			var form = document.forms[0];
			var alg_id = form['algorithm_id'].value;
				
			window.location = "http://localhost:8000/add/alg/id/"+alg_id;
		}
			});
		$("#add_algorithm").click(function() {
		if($('#logged').val()== 'false'){
			bootbox.alert("You have to login first");
		}else{	
			var form = document.forms[0];
			var classification_id = form['classification_id'].value;
			
			window.location = "http://localhost:8000/add/cat/id/"+classification_id;
		}		
		});
		tinyMCE.init({
					// General options
					mode : "textareas",
					//elements: "algorithm_about",
					theme : "advanced",
					readonly : true
			});

	
		$("#add_alg").click(function() {
			var form = document.forms[0];
			
			var algorithm_author = form['author_name'].value;
			var algorithm_about = tinymce.get('algorithm_about').getContent();
			var classification_id = form['classification_id'].value;
			var algorithm_name = form['algorithm_name'].value;
			
			alert(algorithm_about);
			
			//window.location = "http://localhost:8000//show/cat/id/"+classification_id;
			window.location = "http://localhost:8000/added/alg/cat/"+classification_id+"/"+algorithm_name+"/"+algorithm_author+"/"+algorithm_about;
			
			//class_id / name / author / about
			
			
			
		});
		
		function save_implementation(){
				alert("I was saved!");
				window.location = "http://www.google.com";
			}
			
			tinyMCE.init({
					// General options
					mode : "textareas",
					theme : "advanced",
					plugins : "autolink,lists,spellchecker,pagebreak,style,layer,table,save,advhr,advimage,advlink,emotions,iespell,inlinepopups,insertdatetime,preview,media,searchreplace,print,contextmenu,paste,directionality,fullscreen,noneditable,visualchars,nonbreaking,xhtmlxtras,template",

					// Theme options
					theme_advanced_buttons1 : "save,newdocument,|,bold,italic,underline,strikethrough,|,justifyleft,justifycenter,justifyright,justifyfull,|,fontselect,fontsizeselect",
					theme_advanced_buttons2 : "cut,copy,paste,pastetext,pasteword,|,search,replace,|,bullist,numlist,|,outdent,indent,|,undo,redo,",
					theme_advanced_buttons3 : "sub,sup,|,charmap,emotions,iespell,media,advhr,|,print,|,ltr,rtl,|,fullscreen",
					theme_advanced_buttons4 : "styleprops,spellchecker",
					theme_advanced_toolbar_location : "top",
					theme_advanced_toolbar_align : "left",
					theme_advanced_statusbar_location : "bottom",
					theme_advanced_resizing : true,

					// Skin options
					skin : "o2k7",
					skin_variant : "silver",

					// Example content CSS (should be your site CSS)
					content_css : "./tiny_mce/css/content.css",

					// Drop lists for link/image/media/template dialogs
					template_external_list_url : "./tiny_mce/lists/js/template_list.js",
					external_link_list_url : "./tiny_mce/lists/js/link_list.js",
					external_image_list_url : "./tiny_mce/lists/js/image_list.js",
					media_external_list_url : "./tiny_mce/lists/js/media_list.js",

					save_onsavecallback : "save_implementation",
					
					// Replace values for the template plugin
					template_replace_values : {
							username : "Some User",
							staffid : "991234"
					}
			});
		
		
	});