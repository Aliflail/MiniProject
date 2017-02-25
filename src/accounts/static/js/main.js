$(function(){    
    $this=$(this);
      $('*').bind('click',function(){
        $('.a').toggleClass("paused");            
    });
    function change(s){


    }
     $message=$(".errors");
    $input = $('#id_name');
    window.addEventListener('scroll',function(){
         var d = document.getElementsByClassName('header')[0];
        var y = window.pageYOffset;
        if (d){
            d.style.top=200+y*0.5+'px';
        }
    })



    $input.change(function(){
        var username =  $(this).val();
        $this=$(this);
        $.ajax({
            url:"validate_username",
            data:{
                'username':username
            },
            dataType:'json',
            success:function (data){
                if(data.is_taken){
                    $message.removeClass("hidden");
                    $message.html("<div class='alert alert-danger' role='alert' >this username exists</div>");
                }
            }
        });
    });
    $input.focus(function(){
        $message.addClass("hidden");
    });
});