var approval_type_data = new Array();
var validate_add_attributes = [];

//onclick of upload button display id_data_upload popup and set GLOBAL_ACTION button value
function onclick_upload_button() {
    GLOBAL_ACTION = "approval_type_upload"
    $("#id_popup_tbody").empty();
    $('#id_data_upload').modal('show');
}

// on click copy icon display the selected checkbox data
function onclick_copy_button() {
    GLOBAL_ACTION = "COPY"
    onclick_copy_update_button()
    document.getElementById("id_del_add_button").style.display = "block";
}

// on click update icon display the selected checkbox data to update
function onclick_update_button() {
    GLOBAL_ACTION = "UPDATE"
    onclick_copy_update_button()
    document.getElementById("id_del_add_button").style.display = "none";
}

//validate by comparing  main table values and popup table values
function maintable_validation(validate_add_attributes, main_table_low_value) {
    var no_duplicate_entries = 'Y'
    var common = [];
    jQuery.grep(validate_add_attributes, function(el) {
        if (jQuery.inArray(el, main_table_low_value) != -1) {
            common.push(el);
        }
    });
    if (common.length != 0) {
        $("#id_error_msg").prop("hidden", false)
         error_message = messageConstants["JMSG001"]
        no_duplicate_entries = 'N'
    }
    return [no_duplicate_entries,error_message]
}

function compare_table_for_duplicate_entries(validate_add_attributes, approval_type) {
    add_attr_duplicates = false;
    var error_message = ''
    var add_attr_duplicates_list = [];
    var add_attr_unique_list = [];
    var no_duplicate_value = 'Y'
    $.each(validate_add_attributes, function(index, value) {
        if ($.inArray(value, add_attr_unique_list) == -1) {
            add_attr_unique_list.push(value);
        } else {
            if ($.inArray(value, add_attr_duplicates_list) == -1) {
                add_attr_duplicates_list.push(value);
            }
        }
    });
    if (add_attr_duplicates_list.length != 0) {
       error_message = messageConstants["JMSG001"];
        no_duplicate_value = 'N'
  }
    else {
         $.each(approval_type, function (i, item) {
        if (item.app_types.length == 0) {

        error_message = messageConstants["JMSG002"] + "Approval Type";

        no_duplicate_value = 'N'
         return [no_duplicate_value,error_message]
    } if (item.appr_type_desc.length == 0) {
        error_message = messageConstants["JMSG002"] + "Description";
        no_duplicate_value = 'N'
        return [no_duplicate_value,error_message]
            }
      });
    }

      return [no_duplicate_value,error_message]
}
function display_error_message(error_message){

        $('#error_message').text(error_message);

        document.getElementById("error_message").style.color = "Red";
        $("#error_msg_id").css("display", "block");
        $('#id_save_confirm_popup').modal('hide');
        $('#myModal').modal('show');
}


//onclick of cancel empty the popup table body and error messages
$(".remove_upload_data").click(() => {
    $("#id_error_msg").html("");
    $("#id_popup_tbody").empty();
    $("#id_error_msg").empty();
    $('#myModal').modal('hide');
    $("#id_error_msg").prop("hidden", true);
    $("#id_error_msg_approval_type_code").prop("hidden", true);
    $("#id_error_msg_approval_type_name").prop("hidden", true);
    $("#id_error_msg_approval_type_length").prop("hidden", true);
    $("#id_check_error_messages").prop("hidden", true);
    $("#id_check_success_messages").prop("hidden", true);
    $("#id_check_special_character_messages").prop("hidden", true)
    $("#id_check_data").prop("hidden", true);
    $('#id_popup_table').DataTable().destroy();

});

//onclick of cancel display the table in display mode............
function display_basic_db_data() {
    $('#display_basic_table').DataTable().destroy();
    $('#id_approval_type_tbody').empty();
    var edit_basic_data = '';
    $.each(rendered_approval_type_data, function(i, item) {
        edit_basic_data += '<tr ><td class="class_select_checkbox"><input class="checkbox_check" onclick="valueChanged()" type="checkbox" required></td><td>' + item.app_types + '</td><td>' + item.appr_type_desc + '</td></tr>';
    });
    $('#id_approval_type_tbody').append(edit_basic_data);
    $("#hg_select_checkbox").prop("hidden", true);
    $(".class_select_checkbox").prop("hidden", true);
    $('input:checkbox').removeAttr('checked');
    $('#id_edit_data').show();
    $('#id_cancel_data').hide();
    $('#id_delete_data').hide();
    $('#id_copy_data').hide();
    $('#id_update_data').hide();
    $('#id_save_confirm_popup').modal('hide');
    $('#id_delete_confirm_popup').modal('hide');
    $('#id_check_all').hide();
    table_sort_filter('display_basic_table');
}


function delete_duplicate() {
    $('#id_popup_table').DataTable().destroy();
    var approval_type_code_check = new Array
    $("#id_popup_table TBODY TR").each(function() {
        var row = $(this);

        //*************** reading data from the pop-up ***************
        appr_type_desc = row.find("TD").eq(2).find('input[type="text"]').val().toUpperCase();
        app_types = row.find("TD").eq(1).find('input[type="text"]').val().toUpperCase();
        checked_box = row.find("TD").eq(3).find('input[type="checkbox"]').is(':checked')


        if (approval_type_code_check.includes(app_types)) {
            $(row).remove();
        }

        approval_type_code_check.push(app_types);


    })
    table_sort_filter_popup('id_popup_table')
    check_data()
}

// Functtion to hide and display save related popups
$('#save_id').click(function () {
    $('#myModal').modal('hide');
    validate_add_attributes = [];
            var approval_type = {};
            $("#id_popup_table TBODY TR").each(function() {
                var row = $(this);
                approval_type = {};
                approval_type.del_ind = row.find("TD").eq(3).find('input[type="checkbox"]').is(':checked');
                approval_type.appr_type_desc = row.find("TD").eq(2).find('input[type="text"]').val().toUpperCase();
                approval_type.app_types = row.find("TD").eq(1).find('select[type="text"]').val();
                if (approval_type == undefined) {
                    approval_type.app_types = row.find("TD").eq(1).find('select[type="text"]').val();
                }
                validate_add_attributes.push(approval_type.app_types);
                approval_type_data.push(approval_type);
            });
    $('#id_save_confirm_popup').modal('show');
});