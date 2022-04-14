var payment_term_data = new Array();
var validate_add_attributes = [];
var duplicate_entry = [];
var lang_values = [];
var payment_term={};


// on click copy icon display the selected checkbox data
function onclick_copy_button() {
    GLOBAL_ACTION = "COPY"
    onclick_copy_update_button("copy")
    document.getElementById("id_del_add_button").style.display = "block";
}

// on click update icon display the selected checkbox data to update
function onclick_update_button() {
    GLOBAL_ACTION = "UPDATE"
    onclick_copy_update_button("update")
    document.getElementById("id_del_add_button").style.display = "none";
}
//onclick of upload button display id_data_upload popup and set GLOBAL_ACTION button value
function onclick_upload_button() {
    GLOBAL_ACTION = "payterm_desc_upload"
    $("#id_popup_tbody").empty();
    $('#id_data_upload').modal('show');
    //document.getElementById('id_file_data_upload').value = "";
}


//onclick of cancel empty the popup table body and error messages
$(".remove_upload_data").click(() => {
    $("#id_error_msg").html("");
    $("#id_popup_tbody").empty();
    $("#id_error_msg").empty();
    $('#myModal').modal('hide');
    $("#id_error_msg").prop("hidden", true);
    $("#id_error_msg_payment_term_key").prop("hidden", true);
    $("#id_error_msg_description").prop("hidden", true);
    $("#id_error_msg_description_length").prop("hidden", true);
    $("#id_check_error_messages").prop("hidden", true);
    $("#id_check_success_messages").prop("hidden", true);
    $("#id_check_special_character_messages").prop("hidden", true)
    $("#id_check_data").prop("hidden", true);
    $('#id_popup_table').DataTable().destroy();
});

//validate by comparing  main table values and popup table values
function maintable_validation(payment_term_data, main_table_low_value){
    var no_duplicate_entries = 'Y'
    var error_message =''

    var dup_entry = "";

     $.each(payment_term_data, function (i, item) {
        $.each(main_table_low_value, function (j, item1) {
            if((item.payment_term_key == item1.payment_term_key) && (item.language_id == item1.language_id)){
                dup_entry = "1"
            }
        });
     });
         if((dup_entry == "1"))
        {
        error_message = messageConstants["JMSG001"]
        no_duplicate_entries = 'N'
        }
    return [no_duplicate_entries,error_message]

}

// validating the  popup table for duplicate entries
function compare_table_for_duplicate_entries(validate_add_attributes, payment_term) {
    add_attr_duplicates = false;
    var error_message = ''
    var add_attr_duplicates_list = [];
    var add_attr_unique_list = [];
    var no_duplicate_value = 'Y'
    $.each(validate_add_attributes, function (index, value) {
        if ($.inArray(value, add_attr_unique_list) == -1) {
            add_attr_unique_list.push(value);
        }
        else {
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
         $.each(payment_term, function (i, item) {
            if (item.payment_term_key.length == 0) {
                error_message = messageConstants["JMSG002"] + "Payment Term Key";
        no_duplicate_value = 'N'
        return [no_duplicate_value,error_message]
    }
        if (item.day_limit.length == 0) {
                error_message = messageConstants["JMSG002"] + " Day Limit";
        no_duplicate_value = 'N'
        return [no_duplicate_value,error_message]
    }
     if (item.description.length == 0) {
                error_message = messageConstants["JMSG002"] + " Description";
        no_duplicate_value = 'N'
        return [no_duplicate_value,error_message]
    }
         });
    }
    return [no_duplicate_value,error_message]
}

function display_error_message(error_message){

        $('#error_message').text(error_message);
        $('#error_msg_id').text(error_message);
        document.getElementById("error_msg_id").style.color = "Red";
        $("#error_msg_id").css("display", "block");
        $('#id_save_confirm_popup').modal('hide');
        $('#myModal').modal('show');
}
//onclick of cancel display the table in display mode............
function display_basic_db_data() {
    $('#display_basic_table').DataTable().destroy();
    $('#id_payment_term_tbody').empty();
    var edit_basic_data = '';
    var desc = ''; var lang_code;
    $.each(rendered_payment_term_data, function (i, item) {
    lang_code = item.language_id;
            for (i = 0; i < render_language_data.length; i++) {
                if (lang_code == render_language_data[i].language_id)
                    desc = render_language_data[i].description
            }
        edit_basic_data += '<tr><td class="class_select_checkbox"><input class="checkbox_check" onclick="valueChanged()" type="checkbox" required></td>'+
            '<td>' + item.payment_term_key + '</td>' +
            '<td>' + item.day_limit + '</td>' +
            '<td>' + item.description + '</td>' +
            '<td>' + desc + '</td>' +
            '<td hidden> <input type="checkbox"</td>' +
            '<td hidden>' + item.payment_term_guid + '</td></tr>';
    });
    $('#id_payment_term_tbody').append(edit_basic_data);
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

// Functtion to hide and display save related popups
$('#save_id').click(function () {
    $('#myModal').modal('hide');
     validate_add_attributes = [];
     duplicate_entry = [];
     lang_values = [];
     var desc='';
    $("#id_popup_table TBODY TR").each(function () {
            var row = $(this);
            payment_term = {};
            payment_term.payment_term_guid = row.find("TD").eq(6).find('input[type="text"]').val();
            payment_term.payment_term_key = row.find("TD").eq(1).find('select[type="text"]').val();
            payment_term.day_limit = row.find("TD").eq(2).find('input[type="number"]').val();
            payment_term.description = row.find("TD").eq(3).find('input[type="text"]').val();
            payment_term.language_id = row.find("TD").eq(4).find('select[type="text"]').val();
            payment_term.del_ind = row.find("TD").eq(0).find('input[type="checkbox"]').is(':checked');
            if (payment_term == undefined) {
                payment_term.payment_term_key = row.find("TD").eq(1).find('input[type="text"]').val();
            }
            if (payment_term.payment_term_guid == undefined) {
                payment_term.payment_term_guid = '';
            }
            for (i = 0; i < render_language_data.length; i++) {
                if (payment_term.language_id == render_language_data[i].language_id)
                    desc = render_language_data[i].description;
            }
            var attribute_dup = {};
            attribute_dup.payment_term_key = payment_term.payment_term_key;
            attribute_dup.language_id = desc;
            duplicate_entry.push(attribute_dup);

            validate_add_attributes.push(payment_term.payment_term_key);
            //lang_values.push(desc);
            payment_term_data.push(payment_term);
        });
    $('#id_save_confirm_popup').modal('show');
});

