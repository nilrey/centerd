
function getContentHeight(){
    $('.content_content').each(function( index ){
        // alert( $(this).closest('td').attr('id') );
        if( parseInt( $(this).css('height') ) > 25){
            $($(this).closest('td')).append('<div class="contentScrollShow" onclick=\'contentScrollShow( this )\'></div>');
        }
    });
    if ( $(".contentScrollShow").length > 0 ){
        $('#subheader-right').css('float', 'right');
        $('#subheader-right').append('<div class="contentScrollShowAll" onclick=\'contentScrollShowAll()\'></div>');
    }
}

function contentScrollShow( scrollElem ){
    $(scrollElem).toggleClass('contentScrollHide');
    $(scrollElem).closest("td").find(".content_wrapper").toggleClass('content_wrapper_show');
    if ( $(".contentScrollHide").length > 0 ){
        $('.contentScrollShowAll').addClass('contentScrollHideAll');
    }else{
        $('.contentScrollShowAll').removeClass('contentScrollHideAll');
    }
}

function contentScrollShowAll(){
    $('.contentScrollShowAll').toggleClass('contentScrollHideAll');
    if ( $(".contentScrollHideAll").length > 0 ){
        $(".contentScrollShow").each(function( index ){
            $(this).addClass('contentScrollHide');
            $(this).closest("td").find(".content_wrapper").addClass('content_wrapper_show');
        });
    }else{
        $(".contentScrollShow").each(function( index ){
            $(this).removeClass('contentScrollHide');
            $(this).closest("td").find(".content_wrapper").removeClass('content_wrapper_show');
        });
    }
}
