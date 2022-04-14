    nav_bar_shop()
    
    const open_change_password_pop_up = () => {
        $('#password_change_form').trigger('reset')
        $('#success_message').hide()
        $('#error_message').hide()
        $('#id_old_password').addClass('form-control')
        $('#id_new_password1').addClass('form-control')
        $('#id_new_password2').addClass('form-control')
        $('#change_password_pop_up').modal('show')
    }