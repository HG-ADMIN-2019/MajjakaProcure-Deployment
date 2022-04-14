var roles_data = new Array();
var validate_add_attributes = [];
var roles={};

//onclick of add button display myModal popup and set GLOBAL_ACTION button value
function onclick_add_button(button) {
    dropdown_value();
    $("#error_msg_id").css("display", "none")
    $("#header_select").prop( "hidden", false );
    GLOBAL_ACTION = button.value
    $("#id_popup_tbody").empty();
    $('#myModal').modal('show');
  //  basic_add_new_html = '<tr ><td><input type="checkbox" required></td><td><select class="form-control">' + roles_id_dropdown + '</select></td><td><select class="form-control">' + roles_desc_dropdown + '</select></td><td class="class_del_checkbox" hidden><input type="checkbox" required></td></tr>';
    basic_add_new_html='<tr><td><input type="checkbox" required></td>'+
         '<td><select type="text" class="input form-control roles" id="roles-1"  name="role" onchange="GetSelectedTextValue(this)"><option value="" disabled selected>Select your option</option>'+ roles_type_dropdown +'</select></td>'+
        '<td><input class="form-control description" type="text"  name="role_desc"  id="description-1" disabled></td>'+
        '<td class="class_del_checkbox" hidden><input type="checkbox" required></td></tr>';
    $('#id_popup_tbody').append(basic_add_new_html);
    table_sort_filter('id_popup_table');
    $("#id_del_ind_checkbox").prop("hidden", true);
    document.getElementById("id_del_add_button").style.display = "block";
    $("#save_id").prop("hidden", false);
}

//onclick of upload button display id_data_upload popup and set GLOBAL_ACTION button value role_desc
function onclick_upload_button() {
    GLOBAL_ACTION = "roles_upload"
    $("#id_popup_tbody").empty();
    $('#id_data_upload').modal('show');
    document.getElementById('id_file_data_upload').value = "";
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

    $('#display_basic_table').DataTable().destroy();
    $('#id_popup_table').DataTable().destroy();
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
            if(GLOBAL_ACTION == "UPDATE"){
            edit_basic_data += '<tr><td hidden><input type="checkbox" required></td>'+
            '<td><select type="text" class="input form-control" id="roles" name="roles" disabled>'+ roles_type_dropdown +'</select></td>'+
            '<td><input class="form-control" value="' + row.cells[2].innerHTML + '" type="text" onkeypress="return /[a-z ]/i.test(event.key)" name="roles_desc"  maxlength="30" style="text-transform:uppercase" required></td>'+
            '<td class="class_del_checkbox" hidden><input type="checkbox" required></td></tr>';
            $("#header_select").prop("hidden", true);
        }
         else{
               edit_basic_data += '<tr><td><input type="checkbox" required></td>'+
            '<td><select type="text" class="input form-control roles" id="roles-1"  name="roles" onchange="GetSelectedTextValue(this)">'+ roles_type_dropdown +'</select></td>'+
            '<td><input class="input form-control description" id="description-1" value="' + row.cells[2].innerHTML + '" type="text"  name="roles_desc" disabled></td>'+
            '<td class="class_del_checkbox" hidden><input type="checkbox" required></td></tr>';
         $("#header_select").prop("hidden", false);
         }
         var roles_type_value = row.cells[1].innerHTML
            dropdown_values.push([roles_type_value])
}
    }
    $('#id_popup_table').append(edit_basic_data);
    var i =0;
        $("#id_popup_table TBODY TR").each(function() {
        var row = $(this);
         var roletype_value = dropdown_values[i][0]
        $(row.find("TD").eq(1).find("select option[value="+roletype_value+"]")).attr('selected','selected');
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
    $("#id_error_msg_roles_code").prop("hidden", true);
    $("#id_error_msg_roles_name").prop("hidden", true);
    $("#id_error_msg_roles_length").prop("hidden", true);
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
function compare_table_for_duplicate_entries(validate_add_attributes, roles) {
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
    else {
        $.each(roles, function (i, item) {
        if (item.role.length == 0) {
        error_message = messageConstants["JMSG002"] + "Roles";
                no_duplicate_value = 'N'
                return [no_duplicate_value,error_message]
            }
         if (item.role_desc.length == 0) {
           error_message = messageConstants["JMSG002"] + "Roles description";
                no_duplicate_value = 'N'
                return [no_duplicate_value,error_message]

    }
     });
    }

    return [no_duplicate_value,error_message]
}
//    role_desc = roles.role_desc.replace(/\s\s+/g, ' ')
//    if (role_desc == " ") {
//        $("#id_error_msg").prop("hidden", false)
//        Error_msg = "";
//        Error_msg = messageConstants["JMSG002"] + "Role Description";
//        document.getElementById("id_error_msg").innerHTML = Error_msg;
//        document.getElementById("id_error_msg").style.color = "Red";
//        $('#id_save_confirm_popup').modal('hide')
//        $('#myModal').modal('show');
//        no_duplicate_value = 'N'
//    }
//    return no_duplicate_value
//}

// on click add icon display the row in to add the new entries
function add_popup_row() {
    $("#error_msg_id").css("display", "none")
    basic_add_new_html = '';
    var display_db_data = '';
    var getid = $(".roles:last").attr("id");
    var getindex = getid.split("-")[1]
    var inc_index = Number(getindex)+1
    $('#id_popup_table').DataTable().destroy();
    $(".modal").on("hidden.bs.modal", function () {
        $("#id_error_msg").html("");
    });
    basic_add_new_html = '<tr><td><input type="checkbox" required></td>'+
         '<td><select type="text" class="input form-control roles" id="roles-"  name="roles" onchange="GetSelectedTextValue(this)"><option value="" disabled selected>Select your option</option>'+ roles_type_dropdown +'</select></td>'+
        '<td><input class="form-control description" type="text"  name="description"  id="description-" disabled></td>'+
        '<td class="class_del_checkbox" hidden><input type="checkbox" required></td></tr>';
   // basic_add_new_html = '<tr ><td><input type="checkbox" required></td><td><input class="form-control"  type="text" pattern="[A-Z]" maxlength="40" onkeypress="return /[a-z ]/i.test(event.key)" name="role" style="text-transform:uppercase;" required></td><td><input class="form-control" type="text" maxlength="60" onkeypress="return /[a-z ]/i.test(event.key)" name="role_name"  pattern="[A-Z]" style="text-transform:uppercase;" required></td><td class="class_del_checkbox" hidden><input type="checkbox" required></td></tr>';
    $('#id_popup_tbody').append(basic_add_new_html);
    if (GLOBAL_ACTION == "roles_upload") {
        $(".class_del_checkbox").prop("hidden", false);
    }
    table_sort_filter_popup_pagination('id_popup_table');
}

//onclick of cancel display the table in display mode............
function display_basic_db_data() {
    $('#display_basic_table').DataTable().destroy();
    $('#id_roles_tbody').empty();
    var edit_basic_data = '';
    $.each(rendered_roles_data, function (i, item) {
     edit_basic_data += '<tr ><td class="class_select_checkbox"><input class="checkbox_check" onclick="valueChanged()" type="checkbox" required></td><td>' + item.role + '</td><td>' + item.role_desc + '</td></tr>';
    });
    $('#id_roles_tbody').append(edit_basic_data);
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

        document.getElementById("error_message").style.color = "Red";
        $("#error_msg_id").css("display", "block")
        $('#id_save_confirm_popup').modal('hide');
        $('#myModal').modal('show');

}


function delete_duplicate() {
    $('#id_popup_table').DataTable().destroy();
    var roles_code_check = new Array
    $("#id_popup_table TBODY TR").each(function () {
        var row = $(this);
        //*************** reading data from the pop-up ***************

        role = row.find("TD").eq(1).find('input[type="text"]').val().toUpperCase();
        if (roles_code_check.includes(role)) {
            $(row).remove();
        }
        roles_code_check.push(role);
    })
    table_sort_filter_popup_pagination('id_popup_table')
    check_data()
}
$('#save_id').click(function () {
    $('#myModal').modal('hide');
     validate_add_attributes = [];
      var roles = {};
    $("#id_popup_table TBODY TR").each(function () {
            var row = $(this);
            roles = {};
            roles.del_ind = row.find("TD").eq(3).find('input[type="checkbox"]').is(':checked');
            roles.role = row.find("TD").eq(1).find('select[type="text"]').val();
            roles.role_desc = row.find("TD").eq(2).find('input[type="text"]').val().toUpperCase();
            if (roles == undefined) {
                roles.role = row.find("TD").eq(1).find('select[type="text"]').val();
            }
            validate_add_attributes.push(roles.role);
            roles_data.push(roles);
        });
    $('#id_save_confirm_popup').modal('show');
});
