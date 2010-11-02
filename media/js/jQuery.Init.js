$(function() {
	$("#menu #menu-list li img").hover(
		function (){
			var src = $(this).attr("src").match(/[^\.]+/) + "-o.gif";
			$(this).attr("src", src);
		},

		function (){
			var src = $(this).attr("src").replace("-o", "");
            $(this).attr("src", src);
		}
	);
});