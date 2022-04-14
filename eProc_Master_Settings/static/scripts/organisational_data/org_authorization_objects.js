var authobj_data = new Array();
var validate_add_attributes = [];
var auth_obj={};

//onclick of add button display myModal popup and set GLOBAL_ACTION button value
function onclick_add_button(button) {
      dropdown_value();
    $("#error_msg_id").css("display", "none")
    $( "#header_select").prop( "hidden", false );
    GLOBAL_ACTION = button.value
    $('#id_popup_table').DataTable().destroy();
    $("#id_popup_tbody").empty();
    $('#myModal').modal('show');
  basic_add_new_html = '<tr><td><input type="checkbox" required></td>'+
    '<td><select type="text" class="input form-control authobject" id="authobject-1"  name="authobject" onchange="GetSelectedTextValue(this)"><option value="" disabled selected>Select your option</option>'+ auth_obj_id_dropdown +'</select></td>'+
   '<td><input class="form-control description" type="text"  name="description"  id="description-1" disabled></td>'+'<td><select id="authobject_type" name="authobject_type"  class="input form-control">'+auth_type_dropdown+'</select></td>'+
   '<td class="class_del_checkbox" hidden><input type="checkbox" required></td></tr>';
   $('#id_popup_tbody').append(basic_add_new_html);
    table_sort_filter('id_popup_table');
    $("#id_del_ind_checkbox").prop("hidden", true);
    document.getElementById("id_del_add_button").style.display = "block";
    $("#save_id").prop("hidden", false);
}

/// on click copy icon display the selected checkbox data
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
    $('#id_popup_table').DataTable().destroy();
    $("#id_popup_tbody").empty();
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
            var auth_obj_id = row.cells[1].innerHTML;
            var auth_level= row.cells[3].innerHTML;
            dropdown_values.push([auth_obj_id, auth_level])
            if (GLOBAL_ACTION == "UPDATE") {
                edit_basic_data += '<tr><td hidden><input type="checkbox" required></td><td><select type="text" class="input form-control" id="authobjectid"  name="authobjectid" disabled>'+ auth_obj_id_db_values_onload +'</select></td><td><input class="input form-control description" id="description-1" value="' + row.cells[2].innerHTML + '" type="text"  name="description" disabled></td><td><select id="authobject_type" name="authobject_type" class="input form-control"><option selected="true">' + row.cells[3].innerHTML + '</option>' + auth_type_dropdown + '</select></td><td class="class_del_checkbox" hidden><input type="checkbox" required></td></tr>';
                $("#header_select").prop("hidden", true);
            }
            else{
               
                unique_input = '<select class="form-control">' + auth_obj_id_add_dropdown + '</select>'
                edit_basic_data += '<tr ><td><input type="checkbox" required></td><td><select class="form-control">' + auth_obj_id_dropdown + '</select></td><td><select class="form-control">' + auth_obj_level_dropdown + '</select></td><td><select class="form-control">' + auth_obj_level_id_dropdown + '</select></td><td class="class_del_checkbox" hidden><input type="checkbox" required></td></tr>';
                $("#header_select").prop("hidden", false);
            }
        }
    }
    $('#id_popup_table').append(edit_basic_data);
    var i = 0;
    $("#id_popup_table TBODY TR").each(function () {
        var row = $(this);
        var auth_obj_id = dropdown_values[i][0]
        var auth_level= dropdown_values[i][1]

        $(row.find("TD").eq(3).find("select option[value=" + auth_level + "]")).attr('selected', 'selected');
        $(row.find("TD").eq(1).find("select option[value=" + auth_obj_id + "]")).attr('selected', 'selected');
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
    $("#id_error_msg_auth_obj_code").prop("hidden", true);
    $("#id_error_msg_auth_obj_level").prop("hidden", true);
    $("#id_error_msg_auth_obj_length").prop("hidden", true);
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
function compare_table_for_duplicate_entries(validate_add_attributes, auth_obj) {
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
     else{
         $.each(auth_obj, function (i, item) {
//            if (item.auth_obj_id.length == 0) {
//                error_message = messageConstants["JMSG002"] + "Authorization Object ID";
//                no_duplicate_value = 'N'
//                return [no_duplicate_value,error_message]
//            }
//
//            if (item.auth_level_desc.length == 0) {
//
//                error_message = messageConstants["JMSG002"] + "Authorization Level Description";
//                no_duplicate_value = 'N'
//                return [no_duplicate_value,error_message]
//            }
//
//               if (item.auth_level_ID.length == 0) {
//
//                error_message = messageConstants["JMSG002"] + "Authorization Level ID";
//                no_duplicate_value = 'N'
//                return [no_duplicate_value,error_message]
//            }

        });
        
    } 

    return [no_duplicate_value,error_message]
}

function display_error_message(error_message){

    $('#error_message').text(error_message);
 

    document.getElementById("error_message").style.color = "Red";
    $("#error_msg_id").css("display", "block")
    $('#id_save_confirm_popup').modal('hide');
    $('#myModal').modal('show');

}

// on click add icon display the row in to add the new entries
function add_popup_row() {
    dropdown_value();
     $("#error_msg_id").css("display", "none")
    basic_add_new_html = '';
    var display_db_data = '';
    var getid = $(".authobject:last").attr("id");
    var getindex = getid.split("-")[1]
    var inc_index = Number(getindex)+1
    $('#id_popup_table').DataTable().destroy();
    $(".modal").on("hidden.bs.modal", function () {
        $("#id_error_msg").html("");
    });
    basic_add_new_html = '<tr ><td><input type="checkbox" required></td>'+
    '<td><select type="text" class="input form-control authobject" id="authobject-'+inc_index+'" name="authobject" onchange="GetSelectedTextValue(this)"><option value="" disabled selected>Select your option</option>'+ auth_obj_id_dropdown +'</select></td>'+
   '<td><input class="form-control description" type="text" id="description-'+inc_index+'" name="description" disabled></td>'+'<td><select id="authobject_type" name="authobject_type"  class="input form-control">'+auth_type_dropdown+'</select></td>'+
   '<td class="class_del_checkbox" hidden><input type="checkbox" required></td></tr>';
        $('#id_popup_tbody').append(basic_add_new_html);
    if (GLOBAL_ACTION == "auth_obj_upload") {
        $(".class_del_checkbox").prop("hidden", false);
    }
    table_sort_filter_popup_pagination('id_popup_table');
}

//onclick of cancel display the table in display mode............
function display_basic_db_data() {
    $('#display_basic_table').DataTable().destroy();
    $('#id_auth_obj_tbody').empty();
    var edit_basic_data = '';
    $.each(rendered_auth_obj_data, function (i, item) {
        edit_basic_data += '<tr ><td class="class_select_checkbox"><input class="checkbox_check" onclick="valueChanged()" type="checkbox" required></td><td>' + item.auth_obj_id + '</td><td>' + item.auth_level_ID + '</td><td>' + item.auth_level + '</td><td hidden>'+ item.del_ind +'</td>/tr>';
    });
    $('#id_auth_obj_tbody').append(edit_basic_data);
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
    var auth_obj_code_check = new Array
    $("#id_popup_table TBODY TR").each(function () {
        var row = $(this);

        //*************** reading data from the pop-up ***************
        auth_obj_id = row.find("TD").eq(1).find("select option:selected").val().toUpperCase();


        if (auth_obj_code_check.includes(auth_obj_id)) {
            $(row).remove();
        }

        auth_obj_code_check.push(auth_obj_id);


    })
    table_sort_filter_popup_pagination('id_popup_table')
    check_data()
}

// Function to hide and display save related popups
$('#save_id').click(function () {
    $('#myModal').modal('hide');
    validate_add_attributes = [];
    $("#id_popup_table TBODY TR").each(function() {
        var row = $(this);
        auth_obj = {};
        auth_obj.del_ind = row.find("TD").eq(4).find('input[type="checkbox"]').is(':checked');
        auth_obj.auth_obj_id = row.find("TD").eq(1).find("select option:selected").val();
        auth_obj.auth_level_ID = row.find("TD").eq(2).find("input").val();
        auth_obj.auth_level = row.find("TD").eq(3).find("select option:selected").val();

        if (auth_obj == undefined) {
            auth_obj.auth_obj_id = row.find("TD").eq(1).find("select option:selected").val();
        }
        validate_add_attributes.push(auth_obj.auth_obj_id);
        authobj_data.push(auth_obj);
    });


    $('#id_save_confirm_popup').modal('show');
});

 function GetSelectedTextValue(authobject) {
        var selectedText = authobject.options[authobject.selectedIndex].innerHTML;
        var selectedValue = authobject.value;
        var selectedId = (authobject.id).split('-')[1];
         $.each(rendered_auth_obj_id, function(i, item){
            if(selectedValue == item.field_type_id){
                $('#description-'+selectedId).val(item.field_type_desc);
            }
        });

    }