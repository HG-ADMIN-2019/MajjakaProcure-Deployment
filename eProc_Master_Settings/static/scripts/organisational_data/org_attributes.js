var orgattr_data = new Array();
var validate_add_attributes = [];
var org_attr={};


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

                edit_basic_data +=  '<tr><td hidden><input type="checkbox" required></td><td><select type="text" class="input form-control" id="attributeid"  name="attributeid" disabled>'+ attribute_id_dropdown_onload +'</select></td></td><td><input class="form-control attribute_name" type="text" value="' + row.cells[2].innerHTML + '" name="attribute_name" id="attribute_name-1" disabled></td><td><input type="checkbox"  name="range_indicator" required></td><td><input type="checkbox"  name="multiple_value" required></td><td><input type="checkbox" name="allow_defaults" required></td><td><input type="checkbox"  name="inherit_values" required></td><td><input type="number" value="' + row.cells[7].innerHTML + '" name="maxlength"></td><td class="class_del_checkbox" hidden><input type="checkbox" required></td></tr>';
	             $("#header_select").prop("hidden", true);

            }
            else{

               edit_basic_data +=  '<tr><td><input type="checkbox" required></td><td><select type="text" class="input form-control attribute" id="attribute-1"  name="attribute" onchange="GetSelectedTextValue(this)"><option value="" disabled selected>Select your option</option>'+ attribute_id_dropdown +'</select></td><td><input class="form-control attribute_name" type="text" value="' + row.cells[2].innerHTML + '" name="attribute_name" id="attribute_name-1" disabled></td><td><input type="checkbox"  name="range_indicator" required></td><td><input type="checkbox"  name="multiple_value" required></td><td><input type="checkbox"  name="allow_defaults" required></td><td><input type="checkbox" name="inherit_values" required></td><td><input type="number" value="' + row.cells[7].innerHTML + '" name="maxlength"></td><td class="class_del_checkbox" hidden><input type="checkbox" required></td></tr>';
	           $("#header_select").prop("hidden", false);
            }
            var attribute = row.cells[1].innerHTML
            var range_indicator = row.cells[3].innerHTML
            var multiple_value = row.cells[4].innerHTML
            var allow_defaults = row.cells[5].innerHTML
            var inherit_values = row.cells[6].innerHTML
            dropdown_values.push([ attribute,range_indicator,multiple_value,allow_defaults,inherit_values])
      }
    }
    $('#id_popup_table').append(edit_basic_data);
    var i = 0;
    $("#id_popup_table TBODY TR").each(function () {
        var row = $(this);
        var attribute = dropdown_values[i][0]
        var range_indicator = dropdown_values[i][1]
        var multiple_value = dropdown_values[i][2]
        var allow_defaults = dropdown_values[i][3]
        var inherit_values = dropdown_values[i][4]



      $(row.find("TD").eq(1).find("select option[value=" + attribute + "]")).attr('selected', 'selected');
        if (range_indicator == "checkbox.checked") {
                            $(row.find("TD").eq(3).find('input[type="checkbox"]')).attr('checked', 'checked');
                        }
        if (multiple_value  == "true") {
                            $(row.find("TD").eq(4).find('input[type="checkbox"]')).attr('checked', 'checked');
                        }
        if (allow_defaults == "true") {
                            $(row.find("TD").eq(5).find('input[type="checkbox"]')).attr('checked', 'checked');
                        }
          if (inherit_values == "true") {
                            $(row.find("TD").eq(6).find('input[type="checkbox"]')).attr('checked', 'checked');
                        }

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
    $("#id_error_msg_org_attr_code").prop("hidden", true);
    $("#id_error_msg_org_attr_name").prop("hidden", true);
    $("#id_error_msg_org_attr_length").prop("hidden", true);
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
    return  [no_duplicate_entries,error_message]
}

// validating the  popup table for duplicate entries
function compare_table_for_duplicate_entries(validate_add_attributes, org_attr) {
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
        $.each(org_attr, function (i, item) {
    
             if (item.maximum_length.length == 0) {
                 error_message = messageConstants["JMSG002"] +"Maximum length";
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
    $("#error_msg_id").css("display", "block")
    $('#id_save_confirm_popup').modal('hide');
    $('#myModal').modal('show');

}


//onclick of cancel display the table in display mode............
function display_basic_db_data() {
    $('#display_basic_table').DataTable().destroy();
    $('#id_org_attr_tbody').empty();
    var edit_basic_data = '';

    $.each(rendered_org_attr_data, function (i, item) {
            var data = '';
            var data1 = '';
            var data2 = '';
            var data3 = '';
            if (item.range_indicator == true){
                data = '<input type="checkbox" name="range_indicator" value="" checked disabled>'
            } else{
                data = '<input type="checkbox" name="range_indicator" value="" disabled>'
            }
             if (item.multiple_value == true){
                data1 = '<input type="checkbox" name="multiple_value" value="" checked disabled>'
            } else{
                data1 = '<input type="checkbox" name="multiple_value" value="" disabled>'
            }
             if (item.allow_defaults == true){
                data2 = '<input type="checkbox" name="allow_defaults" value="" checked disabled>'
            } else{
                data2 = '<input type="checkbox" name="allow_defaults" value="" disabled>'
            }
            if (item.inherit_values == true){
                data3 = '<input type="checkbox" name="inherit_values" value="" checked disabled>'
            } else{
                data3 = '<input type="checkbox" name="inherit_values" value="" disabled>'
            }
        edit_basic_data += '<tr ><td class="class_select_checkbox"><input class="checkbox_check" onclick="valueChanged()" type="checkbox" required></td><td>' + item.attribute_id + '</td><td>' + item.attribute_name + '</td>'+
        '<td>' + data + '</td>' +
        '<td>' + data1 + '</td>' +
        '<td>' + data2 + '</td>' +
        '<td>' + data3 + '</td>' +
        '<td>' + item.maximum_length + '</td>' +
        '<td hidden> '+ item.del_ind+'</td></tr>';
    });
    $('#id_org_attr_tbody').append(edit_basic_data);
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
    var org_attr_code_check = new Array
    $("#id_popup_table TBODY TR").each(function () {
        var row = $(this);

        //*************** reading data from the pop-up ***************
        attribute_id = row.find("TD").eq(1).find('input[type="text"]').val().toUpperCase();

        if (org_attr_code_check.includes(attribute_id)) {
            $(row).remove();
        }
        org_attr_code_check.push(attribute_id);
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
        org_attr = {};
        org_attr.del_ind = row.find("TD").eq(8).find('input[type="checkbox"]').is(':checked');
        org_attr.attribute_id = row.find("TD").eq(1).find('select[type="text"]').val();
        org_attr.attribute_name = row.find("TD").eq(2).find('input[type="text"]').val();
        org_attr.range_indicator =row.find("TD").eq(3).find('input[type="checkbox"]').is(':checked');
        org_attr.multiple_value = row.find("TD").eq(4).find('input[type="checkbox"]').is(':checked');
        org_attr.allow_defaults = row.find("TD").eq(5).find('input[type="checkbox"]').is(':checked');
        org_attr.inherit_values =row.find("TD").eq(6).find('input[type="checkbox"]').is(':checked');
        org_attr.maximum_length = row.find("TD").eq(7).find('input[type="number"]').val()
        if (org_attr == undefined) {
            org_attr.attribute_id = row.find("TD").eq(1).find('input[type="text"]').val();
        }

        

        validate_add_attributes.push(org_attr.attribute_id);
        orgattr_data.push(org_attr);
    });


    $('#id_save_confirm_popup').modal('show');
});



