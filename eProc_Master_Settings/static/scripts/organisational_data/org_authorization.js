
var auth_data = new Array();
var validate_add_attributes = [];
var auth={};//**************************************

function corresponding_auth_group(auth_type_val) {
    corresponding_values = {};
    corresponding_values.auth_group_dropdown = '';
    for (var i = 0; i < auth_val_list.length; i++) {
        compare_dict = {};
        compare_dict = auth_val_list[i]
        if (auth_type_val == compare_dict.auth_type) {
            corresponding_values.auth_group_dropdown += '<option value="' + compare_dict.auth_obj_grp + '">' + compare_dict.auth_obj_grp + '</option>'
        }
    }
    return corresponding_values
}

//onclick of add button display myModal popup and set GLOBAL_ACTION button value
function onclick_add_button(button) {
   dropdown_value();
    $("#error_msg_id").css("display", "none")
    $("#header_select").prop( "hidden", false );
    GLOBAL_ACTION = button.value
    $("#id_popup_tbody").empty();
    $('#myModal').modal('show');
    basic_add_new_html = '<tr><td><input type="checkbox" required></td><td><select class="form-control">' + auth_group_dropdown + '</select></td><td><select class="form-control">' + auth_type_dropdown + '</select></td><td><select class="form-control">' + roles_dropdown + '</select></td><td hidden><input class="input" type="text" value="GUID"></td><td class="class_del_checkbox" hidden><input type="checkbox" required></td></tr>';
    $('#id_popup_tbody').append(basic_add_new_html);
    table_sort_filter('id_popup_table');
    $("#id_del_ind_checkbox").prop("hidden", true);
    document.getElementById("id_del_add_button").style.display = "block";
    $("#save_id").prop("hidden", false);
//    var auth_type_val = '';
//    $("#id_popup_table TBODY TR").each(function () {
//        var row = $(this);
//        row.find("TD").eq(2).find("select").empty()
//        auth_type_val = row.find("TD").eq(1).find("select option:selected").val();
//        var assign_val = corresponding_auth_group(auth_type_val)
//        row.find("TD").eq(2).find("select").append(assign_val.auth_group_dropdown)
//
//        $(row.find("TD").eq(1).find("select")).change(function () {
//            row.find("TD").eq(2).find("select").empty()
//
//            auth_type_val = row.find("TD").eq(1).find("select option:selected").val();
//
//            var assign_val = corresponding_auth_group(auth_type_val)
//            row.find("TD").eq(2).find("select").append(assign_val.auth_group_dropdown)
//        })
//    })
}
//**********************************
//onclick of upload button display id_data_upload popup and set GLOBAL_ACTION button value
function onclick_upload_button() {
    GLOBAL_ACTION = "auth_upload"
    $("#id_popup_tbody").empty();
    $('#id_data_upload').modal('show');
}
//******************
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

//function onclick_copy_update_button() {
//    $("#id_popup_tbody").empty();
//    $('#display_basic_table').DataTable().destroy();
//    //Reference the Table.
//    var grid = document.getElementById("display_basic_table");
//
//    //Reference the CheckBoxes in Table.
//    var checkBoxes = grid.getElementsByTagName("INPUT");
//    var edit_basic_data = "";
//    var dropdown_values = [];
//    dropdown_value();
//    //Loop through the CheckBoxes.
//    for (var i = 1; i < checkBoxes.length; i++) {
//        if (checkBoxes[i].checked) {
//            var row = checkBoxes[i].parentNode.parentNode;
//            if (GLOBAL_ACTION == "UPDATE") {
//                guid = 'GUID';
//            } else {
//                guid = row.cells[4].innerHTML;
//            }
//            var auth_group = row.cells[1].innerHTML;
//            var roles = row.cells[3].innerHTML;
//            var auth_types = row.cells[2].innerHTML;
//            dropdown_values.push([auth_group, roles, auth_types])
//
//            edit_basic_data += '<tr><td><input type="checkbox" required></td><td><select class="form-control" disabled>' + auth_group_dropdown  + '</select></td><td><select class="form-control">' + auth_type_dropdown + '</select></td><td><select class="form-control">' + roles_dropdown + '</select></td><td hidden><input class="input" type="text" value="' + guid + '"></td><td class="class_del_checkbox" hidden><input type="checkbox" required></td></tr>';
//        }
//    }
//    $('#id_popup_table').append(edit_basic_data);
//    var i = 0;
//    $("#id_popup_table TBODY TR").each(function () {
//        var row = $(this);
//        var auth_group = dropdown_values[i][0];
//        var roles = dropdown_values[i][1];
//        var auth_types = dropdown_values[i][1];
//
//        auth_type_val = row.find("TD").eq(1).find("select option:selected").val();
//        var assign_val = corresponding_auth_group(auth_type_val)
//        row.find("TD").eq(2).find("select").append(assign_val.auth_group_dropdown)
//
//        $(row.find("TD").eq(2).find("select option[value=" + auth_group + "]")).attr('selected', 'selected');
//        $(row.find("TD").eq(3).find("select option[value=" + roles + "]")).attr('selected', 'selected');
//        $(row.find("TD").eq(1).find("select option[value=" + auth_types + "]")).attr('selected', 'selected');
//        i++;
//
//        $(row.find("TD").eq(1).find("select")).change(function () {
//            row.find("TD").eq(2).find("select").empty()
//
//            auth_type_val = row.find("TD").eq(1).find("select option:selected").val();
//
//            var assign_val = corresponding_auth_group(auth_type_val)
//            row.find("TD").eq(2).find("select").append(assign_val.auth_group_dropdown)
//        })
//    });
//    $("#id_del_ind_checkbox").prop("hidden", true);
//    $('#myModal').modal('show');
//    table_sort_filter('display_basic_table');
//    table_sort_filter('id_popup_table');
//}

//onclick of cancel empty the popup table body and error messages
$(".remove_upload_data").click(() => {
    $("#id_error_msg").html("");
    $("#id_popup_tbody").empty();
    $("#id_error_msg").empty();
    $('#myModal').modal('hide');
    $("#id_error_msg").prop("hidden", true);
    $("#id_error_msg_auth_code").prop("hidden", true);
    $("#id_error_msg_auth_name").prop("hidden", true);
    $("#id_error_msg_auth_length").prop("hidden", true);
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

// val
//****************************
// validating the  popup table for duplicate entries
function compare_table_for_duplicate_entries(validate_add_attributes, auth) {
    add_attr_duplicates = false;
     var error_message = ''
    var add_attr_duplicates_list = [];
    var add_attr_unique_list = [];
    var no_duplicate_value = 'Y'
    $.each(validate_add_attributes, function (index, value) {
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

    return [no_duplicate_value,error_message]
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
    basic_add_new_html = '<tr><td><input type="checkbox" required></td><td><select class="form-control">' +auth_group_dropdown  + '</select></td><td><select class="form-control">' + auth_type_dropdown + '</select></td><td><select class="form-control">' + roles_dropdown + '</select></td><td hidden><input class="input" type="text" value="GUID"></td><td class="class_del_checkbox" hidden><input type="checkbox" required></td></tr>';
    $('#id_popup_tbody').append(basic_add_new_html);
    if (GLOBAL_ACTION == "auth_upload") {
        $(".class_del_checkbox").prop("hidden", false);
    }
    var auth_type_val = '';
    $("#id_popup_table TBODY TR").each(function () {
        var row = $(this);
        row.find("TD").eq(2).find("select").empty()
        auth_type_val = row.find("TD").eq(1).find("select option:selected").val();
        var assign_val = corresponding_auth_group(auth_type_val)
        row.find("TD").eq(2).find("select").append(assign_val.auth_group_dropdown)

        $(row.find("TD").eq(1).find("select")).change(function () {
            row.find("TD").eq(2).find("select").empty()

            auth_type_val = row.find("TD").eq(1).find("select option:selected").val();

            var assign_val = corresponding_auth_group(auth_type_val)
            row.find("TD").eq(2).find("select").append(assign_val.auth_group_dropdown)
        })
    })
    table_sort_filter_popup_pagination('id_popup_table');
}


//onclick of cancel display the table in display mode............
function display_basic_db_data() {
    $('#display_basic_table').DataTable().destroy();
    $('#id_auth_tbody').empty();
    var edit_basic_data = '';
    $.each(rendered_auth_data, function (i, item) {
        edit_basic_data += '<tr ><td class="class_select_checkbox"><input class="checkbox_check" onclick="valueChanged()" type="checkbox" required></td><td>' + item.auth_obj_grp + '</td><td>' + item.auth_type + '</td><td>' + item.role + '</td><td hidden>' + item.auth_guid + '</td></tr>';
    });
    $('#id_auth_tbody').append(edit_basic_data);
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
    var auth_code_check = new Array
    $("#id_popup_table TBODY TR").each(function () {
        var row = $(this);

        //*************** reading data from the pop-up ***************
        auth_obj_grp = row.find("TD").eq(1).find("select option:selected").val();
        auth_type = row.find("TD").eq(2).find('input[type="text"]').val().toUpperCase();
        role = row.find("TD").eq(3).find("select option:selected").val();
        checked_box = row.find("TD").eq(3).find('input[type="checkbox"]').is(':checked')
        var compare = auth_obj_grp + '-' + role

        if (auth_code_check.includes(role)) {
            $(row).remove();
        }

        auth_code_check.push(role);


    })
    table_sort_filter_popup_pagination('id_popup_table')
    check_data()
}
function display_error_message(error_message){

        $('#error_message').text(error_message);

        document.getElementById("error_message").style.color = "Red";
        $("#error_msg_id").css("display", "block")
        $('#id_save_confirm_popup').modal('hide');
        $('#myModal').modal('show');

}
var auth_data = new Array();
var validate_add_attributes = [];
var auth={};
$('#save_id').click(function () {
    $('#myModal').modal('hide');
    var auth = {};
   validate_add_attributes = [];
   $("#id_popup_table TBODY TR").each(function () {
            var row = $(this);
            auth = {};
            auth.del_ind = row.find("TD").eq(5).find('input[type="checkbox"]').is(':checked');
            auth.auth_obj_grp = row.find("TD").eq(1).find("select option:selected").val();
            auth.auth_type = row.find("TD").eq(2).find("select option:selected").val();
            auth.role = row.find("TD").eq(3).find("select option:selected").val();
            auth.auth_guid = row.find("TD").eq(4).find('input[type="text"]').val().toUpperCase();
            if (auth == undefined) {
                auth.auth_obj_grp = row.find("TD").eq(1).find('input[type="text"]').val();
            }
            if (auth.auth_guid == undefined) {
                auth.auth_guid = ''
            }
            validate_add_attributes.push( auth.auth_obj_grp);
            auth_data.push(auth);
        });
    $('#id_save_confirm_popup').modal('show');
});
function onclick_copy_update_button() {
    $("#error_msg_id").css("display", "none")
    $("#id_popup_tbody").empty();
    $('#display_basic_table').DataTable().destroy();
    //Reference the Table.
    var grid = document.getElementById("display_basic_table");

    //Reference the CheckBoxes in Table.
    var checkBoxes = grid.getElementsByTagName("INPUT");
    var edit_basic_data = "";
    var dropdown_values = [];
        dropdown_value();
    //Loop through the CheckBoxes.
    for (var i = 1; i < checkBoxes.length; i++) {
        if (checkBoxes[i].checked) {
            var row = checkBoxes[i].parentNode.parentNode;
            var auth_obj_grp = row.cells[1].innerHTML
            var auth_type = row.cells[2].innerHTML
            var role = row.cells[3].innerHTML

            dropdown_values.push([auth_obj_grp,auth_type,role])
            if(GLOBAL_ACTION == "COPY"){
                guid = 'GUID';
                edit_basic_data += '<tr ><td><input type="checkbox" required></td><td><select class="form-control">'+auth_group_dropdown+'</select></td><td><select class="form-control">'+auth_type_dropdown+'</select></td><td><select class="form-control">'+roles_dropdown_dropdown+'</select></td><td hidden><input type="text" value="'+guid+'"></td><td class="class_del_checkbox" hidden><input type="checkbox" required></td></tr>'
            } else{
                guid = row.cells[4].innerHTML;
                edit_basic_data += '<tr ><td><input type="checkbox" required></td><td><select class="form-control" disable>'+auth_group_dropdown+'</select></td><td><select class="form-control">'+auth_type_dropdown+'</select></td><td><select class="form-control">'+roles_dropdown+'</select></td><td hidden><input type="text" value="'+guid+'"></td><td class="class_del_checkbox" hidden><input type="checkbox" required></td></tr>'
            }

        }
    }
    $('#id_popup_table').append(edit_basic_data);
    var i =0;
    $("#id_popup_table TBODY TR").each(function() {
        var row = $(this);
        var auth_obj_grp = dropdown_values[i][0]
        var auth_type = dropdown_values[i][1]
        var role = dropdown_values[i][2]
        $(row.find("TD").eq(1).find("select option[value="+auth_obj_grp+"]")).attr('selected','selected');
        $(row.find("TD").eq(2).find("select option[value="+auth_type+"]")).attr('selected','selected');
        $(row.find("TD").eq(3).find("select option[value="+role+"]")).attr('selected','selected');

        i++;
    });
    $("#id_del_ind_checkbox").prop("hidden", true);
    $('#myModal').modal('show');
    table_sort_filter('display_basic_table');
    table_sort_filter('id_popup_table');
}