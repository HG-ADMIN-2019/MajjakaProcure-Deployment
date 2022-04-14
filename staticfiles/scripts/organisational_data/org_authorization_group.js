var auth_group_data = new Array();
var validate_add_attributes = [];
var auth_group={};
//onclick of add button display myModal popup and set GLOBAL_ACTION button value
function onclick_add_button(button) {

    $("#error_msg_id").css("display", "none")
    $("#header_select").prop( "hidden", false );
    GLOBAL_ACTION = button.value
    $('#id_popup_table').DataTable().destroy();
    $("#id_popup_tbody").empty();
    $('#myModal').modal('show');
    basic_add_new_html = '<tr><td><input type="checkbox" required></td><td><select class="form-control">'+auth_group_id_dropdown+'</select></td><td><select class="form-control">'+auth_obj_id_dropdown+'</select></td><td><select class="form-control">'+auth_group_desc_dropdown+'</select></td><td><select class="form-control">'+auth_level_dropdown+'</select></td><td hidden><input type="text" value="GUID"></td><td class="class_del_checkbox" hidden><input type="checkbox" required></td></tr>';
    $('#id_popup_tbody').append(basic_add_new_html);
    table_sort_filter('id_popup_table');
    $("#id_del_ind_checkbox").prop("hidden", true);
    document.getElementById("id_del_add_button").style.display = "block";
    $("#save_id").prop("hidden", false);
}

//onclick of upload button display id_data_upload popup and set GLOBAL_ACTION button value
function onclick_upload_button() {
    GLOBAL_ACTION = "auth_group_upload"
    $("#id_popup_tbody").empty();
    $('#id_data_upload').modal('show');
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
    var dropdown_values = [];
    //Loop through the CheckBoxes.
    for (var i = 1; i < checkBoxes.length; i++) {
        if (checkBoxes[i].checked) {
            var row = checkBoxes[i].parentNode.parentNode;
            var auth_obj = row.cells[2].innerHTML
            var auth_level = row.cells[4].innerHTML
            var auth_group_id = row.cells[1].innerHTML
            var auth_group_desc = row.cells[3].innerHTML
            dropdown_values.push([auth_obj,auth_level,auth_group_id,auth_group_desc])
            if(GLOBAL_ACTION == "COPY"){
                guid = 'GUID';
                edit_basic_data += '<tr ><td><input type="checkbox" required></td><td><select class="form-control">'+auth_group_id_dropdown+'</select></td><td><select class="form-control">'+auth_obj_id_dropdown+'</select></td><td><select class="form-control">'+auth_group_desc_dropdown+'</select></td><td><select class="form-control">'+auth_level_dropdown+'</select></td><td hidden><input type="text" value="'+guid+'"></td><td class="class_del_checkbox" hidden><input type="checkbox" required></td></tr>'
            } else{
                guid = row.cells[5].innerHTML;
                edit_basic_data += '<tr ><td><input type="checkbox" required></td><td><select class="form-control">'+auth_group_id_dropdown+'</select></td><td><select class="form-control">'+auth_obj_id_dropdown+'</select></td><td><select class="form-control">'+auth_group_desc_dropdown+'</select></td><td><select class="form-control">'+auth_level_dropdown+'</select></td><td hidden><input type="text" value="'+guid+'"></td><td class="class_del_checkbox" hidden><input type="checkbox" required></td></tr>'
            }

        }
    }
    $('#id_popup_table').append(edit_basic_data);
    var i =0;
    $("#id_popup_table TBODY TR").each(function() {
        var row = $(this);
        var auth_obj = dropdown_values[i][0]
        var auth_level = dropdown_values[i][1]
        var auth_group_id = dropdown_values[i][2]
        var auth_group_desc = dropdown_values[i][3]
        $(row.find("TD").eq(2).find("select option[value="+auth_obj+"]")).attr('selected','selected');
        $(row.find("TD").eq(4).find("select option[value="+auth_level+"]")).attr('selected','selected');
        $(row.find("TD").eq(1).find("select option[value="+auth_group_id+"]")).attr('selected','selected');
        $(row.find("TD").eq(3).find("select option[value='"+auth_group_desc+"']")).attr('selected','selected');
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
    $("#id_error_msg_auth_group_code").prop("hidden", true);
    $("#id_error_msg_auth_group_name").prop("hidden", true);
    $("#id_error_msg_auth_group_length").prop("hidden", true);
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

// validating the  popup table for duplicate entries
function compare_table_for_duplicate_entries(validate_add_attributes, auth_group) {
    add_attr_duplicates = false;
    var error_message =''
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

    } else { $.each(auth_group, function (i, item) {
     if (item.auth_obj_grp.length == 0) {
         error_message = messageConstants["JMSG002"] + "Authorization Object Group";
                no_duplicate_value = 'N'
                return [no_duplicate_value,error_message]
            }
    if (item.auth_grp_desc.length == 0) {
       error_message = messageConstants["JMSG002"] + "Discription";
                no_duplicate_value = 'N'
                return [no_duplicate_value,error_message]
            }
     });
    }

    return [no_duplicate_value,error_message]
}


// on click add icon display the row in to add the new entries
function add_popup_row() {
    $("#error_msg_id").css("display", "none")
    basic_add_new_html = '';
    var display_db_data = '';
    $('#id_popup_table').DataTable().destroy();
    $(".modal").on("hidden.bs.modal", function() {
        $("#id_error_msg").html("");
    });
    basic_add_new_html = '<tr><td><input type="checkbox" required></td><td><select class="form-control">'+auth_group_id_dropdown+'</select></td><td><select class="form-control">'+auth_obj_id_dropdown+'</select></td><td><select class="form-control">'+auth_group_desc_dropdown+'</select></td><td><select class="form-control">'+auth_level_dropdown+'</select></td><td hidden><input type="text" value="GUID"></td><td class="class_del_checkbox" hidden><input type="checkbox" required></td></tr>';
    $('#id_popup_tbody').append(basic_add_new_html);
    if (GLOBAL_ACTION == "auth_group_upload") {
        $(".class_del_checkbox").prop("hidden", false);
    }
    table_sort_filter_popup_pagination('id_popup_table');
}

//onclick of cancel display the table in display mode............
function display_basic_db_data() {
    $('#display_basic_table').DataTable().destroy();
    $('#id_auth_group_tbody').empty();
    var edit_basic_data = '';
    $.each(rendered_auth_group_data, function(i, item) {
        edit_basic_data += '<tr><td class="class_select_checkbox"><input class="checkbox_check" onclick="valueChanged()" type="checkbox" required></td><td>' + item.auth_obj_grp + '</td><td>' + item.auth_obj_id + '</td><td>' + item.auth_grp_desc + '</td><td>' + item.auth_level + '</td><td hidden>' + item.auth_grp_guid + '</td></tr>';
    });
    $('#id_auth_group_tbody').append(edit_basic_data);
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
    var auth_group_code_check = new Array
    $("#id_popup_table TBODY TR").each(function() {
        var row = $(this);

        //*************** reading data from the pop-up ***************
        auth_obj_grp = row.find("TD").eq(1).find("select option:selected").val();
        auth_obj_id = row.find("TD").eq(2).find("select option:selected").val();
        auth_grp_desc = row.find("TD").eq(3).find("select option:selected").val();
        auth_level = row.find("TD").eq(4).find("select option:selected").val();

        var compare = auth_obj_grp+'-'+auth_grp_desc+'-'+auth_obj_id+'-'+auth_level


        if (auth_group_code_check.includes(compare)) {
            $(row).remove();
        }

        auth_group_code_check.push(compare);


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
$('#save_id').click(function () {
    $('#myModal').modal('hide');
    var auth_group = {};
   validate_add_attributes = [];

      $("#id_popup_table TBODY TR").each(function () {
     var row = $(this);
            var row = $(this);
            auth_group = {};
            auth_group.del_ind = row.find("TD").eq(6).find('input[type="checkbox"]').is(':checked');
            auth_group.auth_obj_grp = row.find("TD").eq(1).find("select option:selected").val();
            auth_group.auth_obj_id = row.find("TD").eq(2).find("select option:selected").val();
            auth_group.auth_grp_desc = row.find("TD").eq(3).find("select option:selected").val();
            auth_group.auth_level = row.find("TD").eq(4).find("select option:selected").val();
            auth_group.auth_grp_guid = row.find("TD").eq(5).find('input[type="text"]').val().toUpperCase();
            if (auth_group == undefined) {
                auth_group.auth_obj_grp = row.find("TD").eq(1).find('input[type="text"]').val();
            }
            if (auth_group.auth_grp_guid == undefined) {
                auth_group.auth_grp_guid = ''
            }
            var compare = auth_group.auth_obj_grp + ' - ' + auth_group.auth_obj_id + ' - ' + auth_group.auth_grp_desc+ ' - ' +auth_group.auth_level+
            validate_add_attributes.push(compare);
            auth_group_data.push(auth_group);
        });
    $('#id_save_confirm_popup').modal('show');
});
