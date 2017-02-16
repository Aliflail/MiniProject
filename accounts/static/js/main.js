$(function(){    
    $this=$(this);
      $('*').bind('click',function(){
        $('.a').toggleClass("paused");            
    });
});