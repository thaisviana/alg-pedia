$(function() {	
	/*tinyMCE.init({
		// General options
		mode : "textareas",
		plugins : "autolink,lists,spellchecker,pagebreak,style,layer,table,save,advhr,advimage,advlink,emotions,iespell,inlinepopups,insertdatetime,preview,media,searchreplace,print,contextmenu,paste,directionality,fullscreen,noneditable,visualchars,nonbreaking,xhtmlxtras,template",
		
		// Theme options
		theme_advanced_buttons1 : "",
	});*/

	$("#logout").click(function(event) {
		event.preventDefault();
		bootbox.alert("Thank you for using AlgPedia.");
		setTimeout(function () {
			document.location.href = $("#logout").attr('href'); // redireciona pra url nova
        }, 5000);
		
	});	
	$("#contact").click(function() {
		bootbox.prompt("What is your name?", function(result) {                
		if (result === null) {                                             
			Example.show("Prompt dismissed");                              
		} else {
			bootbox.alert("Hi <b>"+result+"</b>");                       
		}
		});
	});
		
		
	$("#add_implementation").css( "padding-left", "+=900" );
		
	$("#add_implementation").click(function(){
		if($('#logged').val()== 'false'){
			bootbox.alert("You have to login first");
		}else{			
			var form = document.forms[0];
			var alg_id = form['algorithm_id'].value;			
			window.location = "http://localhost:8000/add/alg/id/"+alg_id;
		}
	});
	
	$("#add_algorithm").css( "padding-left", "+=800" );
	$("#add_algorithm").click(function() {
		event.preventDefault();
		if($('#logged').val()== 'false'){
			bootbox.alert("You have to login first");
		}else{	
			var form = document.forms[0];
			var classification_id = form['classification_id'].value;
			
			window.location = "http://localhost:8000/add/cat/id/"+classification_id;
		}		
	});
	$("#add_algorithm").mouseover(function () {
		return overlib("Add an algorithm", ABOVE);
	});
	$("#add_algorithm").mouseout(function () {
		return nd();
	});	
	$("#add_implementation").mouseover(function () {
		return overlib("Add implementation", ABOVE);
	});
	$("#add_implementation").mouseout(function () {
		return nd();
	});
	$("#rdf").mouseover(function () {
		return overlib("This content is available in RDF", ABOVE);
	});
	$("#rdf").mouseout(function () {
		return nd();
	});
});