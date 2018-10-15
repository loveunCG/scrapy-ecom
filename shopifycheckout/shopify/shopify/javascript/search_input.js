let event = jQuery.Event( "click" );
 setInterval(function(){
     $('#search_input').click();
     $('#search_input').blur();
     $('#search_input').focus();
     }, 1000);
