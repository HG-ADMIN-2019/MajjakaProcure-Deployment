var approval_limit_data = new Array();
var validate_add_attributes = [];
var approval_limit={};
//function onclick_add_button(button) {
//   $("#error_msg_id").css("display", "none")
//    $("#header_select").prop( "hidden", false );
//    GLOBAL_ACTION = button.value
//    $("#id_popup_tbody").empty();
//    $('#myModal').modal('show');
//    basic_add_new_html = '<tr><td><input type="checkbox" required></td>'+
////    '<td><select class="form-control">'+user_name_dropdown+'</select></td>'+
//    <select type="text" class="input form-control" id="approver_username" name="approver_username">'+
//                                {% for name in user_details %}
//                                '<option value={{name.username}}>{{name.username}}</option>'+
//                                {% endfor %}
//                          //  '</select></td>'+
//    '<td><select class="form-control">'+app_code_id_dropdown+'</select></td>'+
//    '<td><select class="form-control">'+company_id_dropdown+'</select></td>'+
//    '<td hidden><input type="text" value=""></td><td class="class_del_checkbox" hidden><input type="checkbox" required></td></tr>';
//    $('#id_popup_tbody').append(basic_add_new_html);
//    table_sort_filter('id_popup_table');
//    $("#id_del_ind_checkbox").prop("hidden", true);
//    document.getElementById("id_del_add_button").style.display = "block";
//    $("#save_id").prop("hidden", false);
//}

//onclick of upload button display id_data_upload popup and set GLOBAL_ACTION button value
function onclick_upload_button() {
    GLOBAL_ACTION = "approval_limit_upload"
    $("#id_popup_tbody").empty();
    $('#id_data_upload').modal('show');
    document.getElementById('id_file_data_upload').value = "";
}
//******************
// on click copy icon display the selected checkbox data
function onclick_copy_button() {
    GLOBAL_ACTION = "COPY"
    onclick_copy_update_button("copy")
    document.getElementById("id_del_add_button").style.display = "block";
}
//***********************************
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
    var guid = '';
    var dropdown_values = [];
    //Loop through the CheckBoxes.
    for (var i = 1; i < checkBoxes.length; i++) {
        if (checkBoxes[i].checked) {
        var row = checkBoxes[i].parentNode.parentNode;
            if(GLOBAL_ACTION == "COPY"){
                guid = 'GUID';
                edit_basic_data += '<tr><td><input type="checkbox" required></td><td><select class="form-control">'+user_name_dropdown+'</select></td><td><select class="form-control">'+app_code_id_dropdown+'</select></td><td><select class="form-control">'+company_id_dropdown+'</select></td><td hidden><input type="text" value="'+guid+'"></td><td class="class_del_checkbox" hidden><input type="checkbox" required></td></tr>';
                $("#header_select").prop("hidden", false);
            } else{
                guid = row.cells[4].innerHTML;
                edit_basic_data += '<tr><td hidden><input type="checkbox" required></td><td><select class="form-control"disabled>'+user_name_dropdown+'</select></td><td><select class="form-control">'+app_code_id_dropdown+'</select></td><td><select class="form-control" disabled>'+company_id_dropdown+'</select></td><td hidden><input type="text" value="'+guid+'"></td><td class="class_del_checkbox" hidden><input type="checkbox" required></td></tr>';
                $("#header_select").prop("hidden", true);
            }
            var row = checkBoxes[i].parentNode.parentNode;
            var approver_username_value = row.cells[1].innerHTML
            var app_code_id_value = row.cells[2].innerHTML
            var company_type_value = row.cells[3].innerHTML
            dropdown_values.push([approver_username_value,app_code_id_value, company_type_value])

        }
    }
    $('#id_popup_table').append(edit_basic_data);
    var i =0;
    $("#id_popup_table TBODY TR").each(function() {
        var row = $(this);
         var approver_username_value = dropdown_values[i][0]
         console.log(approver_username_value)
        var app_code_id_value = dropdown_values[i][1]
        var company_type_value = dropdown_values[i][2]
        $(row.find("TD").eq(1).find("select option[value="+approver_username_value+"]")).attr('selected','selected');
        $(row.find("TD").eq(2).find("select option[value="+app_code_id_value+"]")).attr('selected','selected');
        $(row.find("TD").eq(3).find("select option[value="+company_type_value+"]")).attr('selected','selected');
        i++;
    });
    $("#id_del_ind_checkbox").prop("hidden", true);
    $('#myModal').modal('show');
    table_sort_filter('display_basic_table');
    table_sort_filter('id_popup_table');
}


//onclick of cancel empty the popup table body and error messages
$(".remove_upload_data").click(() => {
    $("#id_error_msg").html("");
    $("#id_popup_tbody").empty();
    $("#id_error_msg").empty();
    $('#myModal').modal('hide');
    $("#id_error_msg").prop("hidden", true);
    $("#id_error_msg_approval_limit_code").prop("hidden", true);
    $("#id_error_msg_approval_limit_name").prop("hidden", true);
    $("#id_error_msg_approval_limit_length").prop("hidden", true);
    $("#id_check_error_messages").prop("hidden", true);
    $("#id_check_success_messages").prop("hidden", true);
    $("#id_check_special_character_messages").prop("hidden", true)
    $("#id_check_data").prop("hidden", true);
    $('#id_popup_table').DataTable().destroy();
});


//validate by comparing  main table values and popup table values
function maintable_validation(validate_add_attributes, main_table_low_value) {
    var no_duplicate_entries = 'Y'
    var common = [];
    var error_message =''
    jQuery.grep(validate_add_attributes, function(el) {
        if (jQuery.inArray(el, main_table_low_value) != -1) {
            common.push(el);
        }
    });
    if (common.length != 0) {
        error_message = messageConstants["JMSG001"]
        no_duplicate_entries = 'N'
    }
    return [no_duplicate_entries,error_message]
}

// validating the  popup table for duplicate entries
function compare_table_for_duplicate_entries(validate_add_attributes, approval_limit) {
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
        return [no_duplicate_value,error_message]

    }
//     else{
//    $.each(approval_limit, function (i, item) {
//        if(item.approval_limit.approver_username.length !== 0) {
//        error_message = messageConstants["JMSG002"] + "Approver Username";
//                no_duplicate_value = 'N'
//                return [no_duplicate_value,error_message]
//            }
//             });
//             }

             /////////////////////
//    approver_username = approval_limit.approver_username.replace(/\s\s+/g, ' ')
//    if (approver_username == " ") {
//        $("#id_error_msg").prop("hidden", false)
//        Error_msg = "";
//        Error_msg = messageConstants["JMSG002"] + "Approver Username";
//        document.getElementById("id_error_msg").innerHTML = Error_msg;
//        document.getElementById("id_error_msg").style.color = "Red";
//        $('#id_save_confirm_popup').modal('hide');
//        $('#myModal').modal('show');
//        no_duplicate_value = 'N'
//    }
//
//    return no_duplicate_value
return [no_duplicate_value,error_message]
}
//*******************************************************

// on click add icon display the row in to add the new entries
function add_popup_row() {
$("#error_msg_id").css("display", "none")
    basic_add_new_html = '';
    var display_db_data = '';
    $('#id_popup_table').DataTable().destroy();
    $(".modal").on("hidden.bs.modal", function() {
        $("#id_error_msg").html("");
    });
    basic_add_new_html = '<tr><td><input type="checkbox" required></td>'+
    '<td><select class="form-control">'+user_name_dropdown+'</select></td>'+
    '<td><select class="form-control">'+app_code_id_dropdown+'</select></td>'+
    '<td><select class="form-control">'+company_id_dropdown+'</select></td>'+
    '<td hidden><input type="text" value=""></td><td class="class_del_checkbox" hidden><input type="checkbox" required></td></tr>';
    $('#id_popup_tbody').append(basic_add_new_html);
    if (GLOBAL_ACTION == "UPLOAD") {
        $(".class_del_checkbox").prop("hidden", false);
    }
    table_sort_filter_popup_pagination('id_popup_table');
}

//onclick of cancel display the table in display mode............
function display_basic_db_data() {
    $('#display_basic_table').DataTable().destroy();
    $('#id_approval_limit_tbody').empty();
    var edit_basic_data = '';
    $.each(rendered_approval_limit_data, function(i, item) {
        edit_basic_data += '<tr ><td class="class_select_checkbox"><input class="checkbox_check" onclick="valueChanged()" type="checkbox" required></td><td>' + item.approver_username + '</td><td>' + item.app_code_id + '</td><td>' + item.company_id + '</td><td hidden>' + item.app_guid + '</td></tr>';
    });
    $('#id_approval_limit_tbody').append(edit_basic_data);
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
    var approval_limit_code_check = new Array
    $("#id_popup_table TBODY TR").each(function() {
        var row = $(this);

        //*************** reading data from the pop-up ***************
        aapprover_username = row.find("TD").eq(1).find('input[type="text"]').val().toUpperCase();
        app_code_id = row.find("TD").eq(2).find("select option:selected").val();
        company_id = row.find("TD").eq(3).find("select option:selected").val();
        app_guid = row.find("TD").eq(4).find('input[type="text"]').val().toUpperCase()
        approval_limit_compare = approver_username +'-'+ app_code_id +'-'+ company_id


        if (approval_limit_code_check.includes(approval_limit_compare)) {
            $(row).remove();
        }

        approval_limit_code_check.push(approval_limit_compare);

    })
    table_sort_filter_popup('id_popup_table')
    check_data()
}

// Functtion to hide and display save related popups

$('#save_id').click(function () {
    $('#myModal').modal('hide');
    validate_add_attributes = [];
    var approval_limit={};
      $("#id_popup_table TBODY TR").each(function () {
      var row = $(this);
            approval_limit = {};
            approval_limit.del_ind = row.find("TD").eq(5).find('input[type="checkbox"]').is(':checked');
            approval_limit.approver_username = row.find("TD").eq(1).find("select option:selected").val();
            approval_limit.app_code_id = row.find("TD").eq(2).find("select option:selected").val();
            approval_limit.company_id = row.find("TD").eq(3).find("select option:selected").val();
            approval_limit.app_guid = row.find("TD").eq(4).find('input[type="text"]').val().toUpperCase()
            var approval_limit_compare = approval_limit.approver_username +'-'+ approval_limit.app_code_id +'-'+ approval_limit.company_id
            if (approval_limit == undefined) {
                approval_limit.approver_username = row.find("TD").eq(1).find("select option:selected").val();
            }
            if(approval_limit.app_guid == undefined) {
                  approval_limit.app_guid = ''
             }
            validate_add_attributes.push(approval_limit_compare);
            approval_limit_data.push(approval_limit);
           });

    $('#id_save_confirm_popup').modal('show');
});

function display_error_message(error_message){

        $('#error_message').text(error_message);

        document.getElementById("error_message").style.color = "Red";
        $("#error_msg_id").css("display", "block")
        $('#id_save_confirm_popup').modal('hide');
        $('#myModal').modal('show');

}