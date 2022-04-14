$(document).ready(function(){
    $("#supplier_form_reset").click(function(){
        $('#configform')[0].reset();
        $('#myModal').modal('hide');
    });

    $('#nav_menu_items').remove();
    $("body").css("padding-top", "4rem");
});

// Function to make user basic data field editable
function edit_user_basic_info() {
    $('#user_basic_update_success').hide();
    $(".hg_edit_display_mode").prop("disabled", false);
    $("#language_id").append(language_opt)
    $("#currency_id").append(currency_opt)
    $("#time_zone").append(timezone_opt)
    $("#decimal_notation").append(decimal_opt)
    $("#date_format").append(date_format_opt)
    document.getElementById("edit_user_info_btn").style.display = "none"
    document.getElementById("save_cancel_user_info_btn").style.display = "block"
}

// Onlick cancel edit user-basic data 
function cancel_user_basic_info() {
    $(".hg_edit_display_mode").prop("disabled", true);
    document.getElementById("edit_user_info_btn").style.display = "block"
    document.getElementById("save_cancel_user_info_btn").style.display = "none"
}

    // Funtion to save basic detail data
    function save_user_basic_info() {
     var name1_val= $('#first_name').val();
     var phone_num_val = $('#phone_num').val();
     var email_val = $('#email').val();
      is_save_form_valid = save_user_form_validation(name1_val, phone_num_val, email_val)
        if (is_save_form_valid != '') {
            $('#save_error_div').html(is_save_form_valid)
            $('#save_error_div').show()
            scroll_top()
            return
        }
        var user_data_dict = {}

        user_data_dict.username = $('#username').val();
        user_data_dict.first_name = $('#first_name').val();
        user_data_dict.last_name= $('#last_name').val();
        user_data_dict.employee_id= $('#employee_id').val();
        user_data_dict.user_type= $('#user_type').val();
        user_data_dict.language_id= $('#language_id').val();
        user_data_dict.currency_id=$('#currency_id').val();
        user_data_dict.time_zone= $('#time_zone').val();
        user_data_dict.email= $('#email').val();
        user_data_dict.phone_num= $('#phone_num').val();
        user_data_dict.date_format= $('#date_format').val();
        user_data_dict.decimal_notation= $('#decimal_notation').val();
        user_data_dict.login_attempts= $('#login_attempts').val();
        user_data_dict.super_user= $('#super_user').prop('checked');
        user_data_dict.user_locke= $('#user_locked').prop('checked');
        user_data_dict.pwd_locked= $('#pwd_locked').prop('checked');

        ajax_update_user_basic_data(user_data_dict)

        document.getElementById('user_basic_update_success').innerHTML = response.message;
          $('#save_error_div').hide()
        $('#user_basic_update_success').show();
        $('html, body').animate({ scrollTop: 0 }, 'slow');
        cancel_user_basic_info();

    }
// Validation function
   const save_user_form_validation = (name1_val, phone_num_val, email_val) => {
        var is_valid = true
        var save_form_errors = ''
        var mailformat = /^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/;
        if (name1_val == '') {
            is_valid = false
            save_form_errors +=  messageConstants["JMSG007"] + "First Name";
        }
        if (phone_num_val == '') {
            is_valid = false
            save_form_errors += messageConstants["JMSG007"] + "Phone number";
        }
        if ((email_val == '') || !(email_val.match(mailformat))) {
            is_valid = false
            save_form_errors += messageConstants["JMSG002"] + "Email Id";
        }


        return is_valid, save_form_errors
    }
