$(document).ready(function(){    
	//console.log("build-page :: load")
	_delayTimsMS = 4000;
	$("#click").click(function(){
		//console.log("build-page :: click_btn");
		$("tr.data-row").each(function(idx, elm) {
			let libparamurl = $(elm).data('libparamurl');
			window.setTimeout(function() {  window.open(libparamurl, "_blank");  }, (_delayTimsMS||1500) * idx);
		});
	});
	$("#gen_identifier").click(function(){
		window.open($("#identifier_url").text(), "_blank"); 
	});
});