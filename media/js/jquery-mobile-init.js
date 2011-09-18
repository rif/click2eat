$(document).bind("mobileinit", function(){
  $.mobile.page.prototype.options.addBackBtn= true;
});
$(document).ajaxError(function(event, request, settings){
  alert("Error sending request!");
});