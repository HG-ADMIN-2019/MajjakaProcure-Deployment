
var payment_term_data = new Array();
var validate_add_attributes = [];
var payment_term={};//onclick of add button display myModal popup and set GLOBAL_ACTION button value
function onclick_add_button(button) {
    $("#error_msg_id").css("display", "none")
    $( "#header_select").prop( "hidden", false );
    GLOBAL_ACTION = button.value
    $("#id_popup_tbody").empty();
    $('#myModal').modal('show');
    basic_add_new_html = '<tr><td><input type="checkbox" required></td><td><input class="form-control" type="number" onkeypress="return /[a-zA-Z0-9]/i.test(event.key)" name="payment_term_key" style="text-transform:uppercase;" required></td><td class="class_del_checkbox" hidden><input type="checkbox" required></td><td hidden><input  type="text"  name="guid"></td></tr>';
    $('#id_popup_tbody').append(basic_add_new_html);
    table_sort_filter('id_popup_table');
    $("#id_del_ind_checkbox").prop("hidden", true);
    document.getElementById("id_del_add_button").style.display = "block";
    $("#save_id").prop("hidden", false);
}

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


function onclick_copy_update_button() {
    $("#error_msg_id").css("display", "none")
    $("#id_popup_tbody").empty();
    $('#display_basic_table').DataTable().destroy();
    //Reference the Table.
    var grid = document.getElementById("display_basic_table");

    //Reference the CheckBoxes in Table.
    var checkBoxes = grid.getElementsByTagName("INPUT");
    var edit_basic_data = "";
    //Loop through the CheckBoxes.
    for (var i = 1; i < checkBoxes.length; i++) {
        if (checkBoxes[i].checked) {
            var row = checkBoxes[i].parentNode.parentNode;
            if (GLOBAL_ACTION == "COPY") {
                guid = '';
                  edit_basic_data += '<tr ><td><input type="checkbox" required></td><td><input class="form-control" type="number" value="' + row.cells[1].innerHTML + '" name="payment_term_key"   style="text-transform:uppercase" required></td><td class="class_del_checkbox" hidden><input type="checkbox" required></td><td hidden><input  type="text"  name="guid" value="' + row.cells[2].innerHTML + '"></td></tr>';

            } else {
                guid = row.cells[2].innerHTML;
                   edit_basic_data += '<tr ><td><input type="checkbox" required></td><td><input class="form-control" type="number" value="' + row.cells[1].innerHTML + '" name="payment_term_key"   style="text-transform:uppercase" required></td><td class="class_del_checkbox" hidden><input type="checkbox" required></td><td hidden><input  type="text"  name="guid" value="' + row.cells[2].innerHTML + '"></td></tr>';

            }
            //edit_basic_data += '<tr ><td><input type="checkbox" required></td><td><input class="form-control" type="text" value="' + row.cells[1].innerHTML + '" name="payment_term_key"   style="text-transform:uppercase" required></td><td class="class_del_checkbox" hidden><input type="checkbox" required></td><td hidden><input  type="text"  name="guid" value="' + row.cells[3].innerHTML + '"></td></tr>';
        }
    }
    $('#id_popup_table').append(edit_basic_data);
    $("#id_del_ind_checkbox").prop("hidden", true);
    table_sort_filter('display_basic_table');
    table_sort_filter('id_popup_table');
    $('#myModal').modal('show');

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
function maintable_validation(validate_add_attributes, main_table_low_value) {
    var no_duplicate_entries = 'Y'
    var error_message =''
    var common = [];
    jQuery.grep(validate_add_attributes, function (el) {
        if (jQuery.inArray(el, main_table_low_value) != -1) { common.push(el); }
    });
    if (common.length != 0) {
//        $("#id_error_msg").prop("hidden", false)
//        document.getElementById("id_error_msg").innerHTML = messageConstants["JMSG001"];
//        document.getElementById("id_error_msg").style.color = "Red";
//        $('#id_save_confirm_popup').modal('hide');
//        $('#myModal').modal('show');
        error_message = messageConstants["JMSG001"]
        no_duplicate_entries = 'N'
    }
      return [no_duplicate_entries,error_message]
}


// validating the  popup table for duplicate entries
function compare_table_for_duplicate_entries(validate_add_attributes, payment_term) {
    add_attr_duplicates = false;
    var add_attr_duplicates_list = [];
    var add_attr_unique_list = [];
    var error_message = ''
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
    else{
         $.each(payment_term, function (i, item) {
             if (payment_term.payment_term_key.length == 0) {
                error_message = messageConstants["JMSG002"] + "Payment Term Key ";
                no_duplicate_value = 'N'
                return [no_duplicate_value,error_message]
        }
    });
}
    return no_duplicate_value
}

// on click add icon display the row in to add the new entries
function add_popup_row() {
    $("#error_msg_id").css("display", "none")
    basic_add_new_html = '';
    var display_db_data = '';
    $('#id_popup_table').DataTable().destroy();
    $(".modal").on("hidden.bs.modal", function () {
        $("#id_error_msg").html("");
    });
    basic_add_new_html = '<tr><td><input type="checkbox" required></td><td><input class="form-control" type="number" name="payment_term_key"  required></td><td class="class_del_checkbox" hidden><input type="checkbox" required></td><td hidden><input  type="text"  name="guid"></td></tr>';
    $('#id_popup_tbody').append(basic_add_new_html);
    if (GLOBAL_ACTION == "payment_term_upload") {
        $(".class_del_checkbox").prop("hidden", false);
    }
    table_sort_filter('id_popup_table');
}


//onclick of cancel display the table in display mode............
function display_basic_db_data() {
    $('#display_basic_table').DataTable().destroy();
    $('#id_payment_term_tbody').empty();
    var edit_basic_data = '';
    $.each(rendered_payment_term_data, function (i, item) {
        edit_basic_data += '<tr><td class="class_select_checkbox"><input class="checkbox_check" onclick="valueChanged()" type="checkbox" required></td>' +
            '<td>' + item.payment_term_key + '</td>' +
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
function display_error_message(error_message){

        $('#error_message').text(error_message);
        //$("p").css("color", "red");
        //document.getElementById("error_message").innerHTML = error_message;
        document.getElementById("error_message").style.color = "Red";
        $("#error_msg_id").css("display", "block")
        $('#id_save_confirm_popup').modal('hide');
        $('#myModal').modal('show');

}
$('#save_id').click(function () {
    $('#myModal').modal('hide');
    payment_term_data = new Array();
    validate_add_attributes = [];
   $("#id_popup_table TBODY TR").each(function () {
           var row = $(this);
           var countries_data = new Array();
            payment_term = {};
            payment_term.payment_term_guid = row.find("TD").eq(3).find('input[type="text"]').val();
            payment_term.del_ind = row.find("TD").eq(2).find('input[type="checkbox"]').is(':checked');
            payment_term.payment_term_key = row.find("TD").eq(1).find('input[type="number"]').val();
            if (payment_term == undefined) {
                payment_term.payment_term_key = row.find("TD").eq(1).find('input[type="number"]').val();
            }
             if(payment_term.payment_term_guid == undefined) {
                   payment_term.payment_term_guid = ''
             }
            validate_add_attributes.push(payment_term.payment_term_key);
            countries_data.push(payment_term);
       });
    $('#id_save_confirm_popup').modal('show');
});

