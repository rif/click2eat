$(document).bind("mobileinit", function(){
  $.mobile.page.prototype.options.addBackBtn= true;
});
$(document).ajaxError(function(event, request, settings){
  alert("Error sending request!");
});
function uid() {
    // generate unique id for shopping carts items (to be identified when using incr)
    return (new Date()).getTime()
}