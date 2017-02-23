$(function(){    
    $this=$(this);
      $('*').bind('click',function(){
        $('.a').toggleClass("paused");            
    });
    function change(s){


    }


    window.addEventListener('scroll',function(){
         var d = document.getElementsByClassName('header')[0];
        var y = window.pageYOffset;
        d.style.top=200+y*0.5+'px';

    })
});