$(document).ready(function() {
    // Configure/customize these variables.
    var showChar = 100;  // How many characters are shown by default
    var ellipsestext = "...";
    var moretext = "Show more";
    var lesstext = "Show less";
    var showCharDesc = 190;
    var showCharprod = 16;
    

    $('.more').each(function() {
        var content = $(this).html();
 
        if(content.length > showChar) {
 
            var c = content.substr(0, showChar);
            var h = content.substr(showChar, content.length - showChar);
 
            var html = c + '<span class="moreellipses">' + ellipsestext+ '&nbsp;</span><span class="morecontent"><span>' + h + '</span>&nbsp;&nbsp;<a href="" class="morelink">' + moretext + '</a></span>';
 
            $(this).html(html);
        }
 
    });

    $('.moreDesc').each(function() {
        var content = $(this).html();
 
        if(content.length > showCharDesc) {
 
            var c = content.substr(0, showCharDesc);
            var h = content.substr(showCharDesc, content.length - showCharDesc);
 
            var html = c + '<span class="moreellipses">' + ellipsestext+ '&nbsp;</span><span class="morecontent"><span>' + h + '</span>&nbsp;&nbsp;<a href="" class="morelink">' + moretext + '</a></span>';
 
            $(this).html(html);
        }
 
    });

    $('.moreProduct').each(function() {
        var content = $(this).html();
 
        if(content.length > showCharprod) {
 
            var c = content.substr(0, showCharprod);
            var h = content.substr(showCharprod, content.length - showCharprod);
 
            var html = c + '<span class="moreellipses">' + ellipsestext+ '&nbsp;</span>';
 
            $(this).html(html);
        }
 
    });
 
    $(".morelink").click(function(){
        if($(this).hasClass("less")) {
            $(this).removeClass("less");
            $(this).html(moretext);
        } else {
            $(this).addClass("less");
            $(this).html(lesstext);
        }
        $(this).parent().prev().toggle();
        $(this).prev().toggle();
        return false;
    });
});