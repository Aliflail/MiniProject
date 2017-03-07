$(function(){
    if (document.querySelector("input#id_name")){
    document.querySelector("input#id_name").setAttribute("autocomplete","off");
    }
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



    $input.keyup(function(){
        var username =  $(this).val();
        $this=$(this);
        $form =$message.closest("form");
        console.log('/'+$form.attr("data-validate-username-url").slice(1));
        $.ajax({
            url:'/'+$form.attr("data-validate-username-url").slice(1),
            data:$form.serialize(),
            dataType:'json',
            success:function (data){
                if(data.is_taken){
                    $message.removeClass("hidden");

                    $message.html("<div class='alert alert-danger' role='alert' >"+data.error_message+"</div>");

                }

            }
        });
    });
    $input.keydown(function(){
        $message.addClass("hidden");
    });
});