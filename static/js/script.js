$(function () {
    var index = 0;
    $('.num li').click(function () {
        $('#passdots li:eq('+index+')').addClass('active');
        index++;

        if(index>$('#passdots li').length){
            $('#passdots li').removeClass('active');
            index=0;
        }
    })


    $('.doorbell').click(function(){
        $.post('/bell',{},function(){
            
        })
    })
})