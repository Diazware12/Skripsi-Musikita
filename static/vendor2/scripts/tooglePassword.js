$("#show_hide_password a").on('click', function(event) {
    event.preventDefault();
    if($('#show_hide_password input').attr("type") == "text"){
        $('#show_hide_password input').attr('type', 'password');
        $('#show_hide_password i').addClass( "fa-eye-slash" );
        $('#show_hide_password i').removeClass( "fa-eye" );
    }else if($('#show_hide_password input').attr("type") == "password"){
        $('#show_hide_password input').attr('type', 'text');
        $('#show_hide_password i').removeClass( "fa-eye-slash" );
        $('#show_hide_password i').addClass( "fa-eye" );
    }
});

$("#show_hide_password_confirm a").on('click', function(event) {
    event.preventDefault();
    if($('#show_hide_password_confirm input').attr("type") == "text"){
        $('#show_hide_password_confirm input').attr('type', 'password');
        $('#show_hide_password_confirm i').addClass( "fa-eye-slash" );
        $('#show_hide_password_confirm i').removeClass( "fa-eye" );
    }else if($('#show_hide_password_confirm input').attr("type") == "password"){
        $('#show_hide_password_confirm input').attr('type', 'text');
        $('#show_hide_password_confirm i').removeClass( "fa-eye-slash" );
        $('#show_hide_password_confirm i').addClass( "fa-eye" );
    }
});