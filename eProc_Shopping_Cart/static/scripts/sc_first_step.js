// display shop role sub menu in nav bar
nav_bar_shop()

$(document).ready(function(){
    $('#sc-proceed-checkout').click(function () {
        $('#hg_loader').modal('show');
    });

    $('body').css('padding-top', '7rem');
});

// Function to add favourite cart items
function add_favourite_cart(){
    
    $('#fav_name_error_message').html('');
    $('#fav_name_error_message').hide();
    $('#fav_name_success_message').html('');
    $('#fav_name_success_message').hide();
    favourite_sc_data = {}; 
    favourite_sc_data.total_cart_value = $('#total_cart_value').html();
    favourite_sc_data.total_cart_currency = $('#total_cart_currency').html();
    favourite_sc_data.favourite_cart_name = $('#favourite_sc_name_input').val();
    var fsc_result = ajax_add_favourite_cart(favourite_sc_data); 

    if(fsc_result) {
        if(response.success_message){
            $('#fav_name_success_message').html(response.success_message);
            $('#fav_name_success_message').show();
            $("#favourite_sc_button").find('.material-icons').html("favorite").css("color", "red");
        } else if (response.error_message) {
            $('#fav_name_error_message').html(response.error_message);
            $('#fav_name_error_message').show();
        }
    }

}