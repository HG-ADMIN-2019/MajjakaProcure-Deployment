var aad_data = new Array();
var validate_add_attributes = [];
var aad={};

function account_assignment_value_find(account_assign) {

    corresponding_values = {};
    corresponding_values.acc_ass_dropdwn = '';
    corresponding_values.company_dropdwn = '';
    acc_ass_val_list = acc_ass_val_list;
    for (var i = 0; i < acc_ass_val_list.length; i++) {
        compare_dict = {};
        compare_dict = acc_ass_val_list[i]
        if (account_assign == compare_dict.account_assign_value) {
            corresponding_values.acc_ass_dropdwn += '<option value="' + compare_dict.account_assign_cat + '">' + compare_dict.account_assign_cat + '</option>'
            corresponding_values.company_dropdwn += '<option  value="' + compare_dict.company_id + '">' + compare_dict.company_id + '</option>'
        }

    }
    return corresponding_values
}

//onclick of add button display myModal popup and set GLOBAL_ACTION button value
function onclick_add_button(button) {
    $("#error_msg_id").css("display", "none")
    $("#header_select").prop( "hidden", false );
    GLOBAL_ACTION = button.value
    $("#id_popup_tbody").empty();
    $('#myModal').modal('show');
    basic_add_new_html = '<tr> <td><input class="input" type="checkbox" required></td> <td><select class="form-control">' + acc_ass_val_dropdwn + ' </select></td> <td><input class="form-control" type="text"  maxlength="255" style="text-transform:uppercase" ></td> <td><select class="form-control"></select></td> <td ><select class="form-control"></select></td> <td><select class="form-control">' + language_dropdwn + '</select></td><td hidden><input value="GUID" hidden></td> <td class="class_del_checkbox" hidden><input type="checkbox" required></td> <td hidden></td> </tr>';
    $('#id_popup_tbody').append(basic_add_new_html);
    table_sort_filter('id_popup_table');
    var account_assign = '';
    $("#id_popup_table TBODY TR").each(function () {
        var row = $(this);
        row.find("TD").eq(3).find("select").empty()
        row.find("TD").eq(4).find("select").empty()
        account_assign = row.find("TD").eq(1).find("select option:selected").val();
        var assign_val = account_assignment_value_find(account_assign)
        row.find("TD").eq(3).find("select").append(assign_val.acc_ass_dropdwn)
        row.find("TD").eq(4).find("select").append(assign_val.company_dropdwn)

        $(row.find("TD").eq(1).find("select")).change(function () {
            row.find("TD").eq(3).find("select").empty()
            row.find("TD").eq(4).find("select").empty()

            account_assign = row.find("TD").eq(1).find("select option:selected").val();

            var assign_val = account_assignment_value_find(account_assign)
            row.find("TD").eq(3).find("select").append(assign_val.acc_ass_dropdwn)
            row.find("TD").eq(4).find("select").append(assign_val.company_dropdwn)
        })
    })


    $("#id_del_ind_checkbox").prop("hidden", true);
    document.getElementById("id_del_add_button").style.display = "block";
    $("#save_id").prop("hidden", false);
}
//*******************************************

//onclick of upload button display id_data_upload popup and set GLOBAL_ACTION button value
function onclick_upload_button() {
    GLOBAL_ACTION = "aad_upload"
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
//**********************************************************

function onclick_copy_update_button() {
     $("#error_msg_id").css("display", "none")
    $('#myModal').modal('show');
    $("#id_popup_tbody").empty();
    $('#display_basic_table').DataTable().destroy();
    //Reference the Table.
    var grid = document.getElementById("display_basic_table");

    //Reference the CheckBoxes in Table.
    var checkBoxes = grid.getElementsByTagName("INPUT");
    var edit_basic_data = "";
    var dropdown_array = [];
    var unique_input = '';
    var guid= '';
    //Loop through the CheckBoxes.
    for (var i = 1; i < checkBoxes.length; i++) {
        if (checkBoxes[i].checked) {
            var row = checkBoxes[i].parentNode.parentNode;
            if (GLOBAL_ACTION == "COPY") {
                guid = 'GUID';
                unique_input = '<input class="form-control" type="number" value="' + row.cells[1].innerHTML + '" name="Account Assignment Value" maxlength="40" required>'
                edit_basic_data += '<tr><td><input class="input" type="checkbox" required></td> <td><select class="form-control" id="acc_ass_val_dropdw">' + acc_ass_val_dropdwn + ' </select></td><td><input class="form-control" type="text" value="' + row.cells[2].innerHTML + '"  maxlength="255" onkeypress="return /[a-z ]/i.test(event.key)" style="text-transform:uppercase" ></td><td><select id="acc_ass_dropdw" class="form-control"></select></td> <td ><select id="company_dropdw" class="form-control">'+ company_dropdwn +'</select></td> <td><select id="language_dropdw" class="form-control">' + language_dropdwn + '</select></td><td hidden><input value="' + guid + '"></td> <td class="class_del_checkbox" hidden><input type="checkbox" required></td> <td hidden> </td></tr>'
                $("#header_select").prop("hidden",false);

            } else {
                guid = row.cells[6].innerHTML;
                unique_input = '<input class="form-control" type="number" value="' + row.cells[1].innerHTML + '" name="Account Assignment Value" maxlength="40" disabled>'
                edit_basic_data += '<tr><td hidden><input class="input" type="checkbox" required></td> <td><select class="form-control" id="acc_ass_val_dropdw" disabled>' + acc_ass_val_dropdwn + ' </select></td><td><input class="form-control" type="text" value="' + row.cells[2].innerHTML + '"  maxlength="255" onkeypress="return /[a-z ]/i.test(event.key)" style="text-transform:uppercase" ></td><td><select id="acc_ass_dropdw" class="form-control" disabled></select></td> <td ><select id="company_dropdw" class="form-control" disabled>'+ company_dropdwn +'</select></td> <td><select id="language_dropdw" class="form-control"'+ company_dropdwn +' disabled>' + language_dropdwn + '</select></td><td hidden><input value="' + guid + '"></td> <td class="class_del_checkbox" hidden><input type="checkbox" required></td> <td hidden> </td></tr>'
                $("#header_select").prop("hidden",true);

            }
            var account_assgn_val = row.cells[1].innerHTML
            var acc_cat = row.cells[3].innerHTML
            var company_id = row.cells[4].innerHTML
            var langauge_id = row.cells[5].innerHTML
            dropdown_array.push([account_assgn_val, acc_cat, company_id, langauge_id])

        }
    }
    $('#id_popup_table').append(edit_basic_data);
    var i = 0;
    $("#id_popup_table TBODY TR").each(function () {
        var row = $(this);
        var account_assgn_val = dropdown_array[i][0]
        var acc_cat = dropdown_array[i][1]
        var company_id = dropdown_array[i][2]
        var langauge_id = dropdown_array[i][3]
        $(row.find("TD").eq(1).find("select option[value=" + account_assgn_val + "]")).attr('selected', 'selected');
        var assign_val = account_assignment_value_find(account_assgn_val)
        row.find("TD").eq(3).find("select").append(assign_val.acc_ass_dropdwn)
        row.find("TD").eq(4).find("select").append(assign_val.company_dropdwn)
        $(row.find("TD").eq(3).find("select option[value=" + acc_cat + "]")).attr('selected', 'selected');
        $(row.find("TD").eq(4).find("select option[value=" + company_id + "]")).attr('selected', 'selected');
        $(row.find("TD").eq(5).find("select option[value=" + langauge_id + "]")).attr('selected', 'selected');

        $(row.find("TD").eq(1).find("select")).change(function () {
            row.find("TD").eq(3).find("select").empty()
            row.find("TD").eq(4).find("select").empty()

            account_assign = row.find("TD").eq(1).find("select option:selected").val();

            var assign_val = account_assignment_value_find(account_assign)
            row.find("TD").eq(3).find("select").append(assign_val.acc_ass_dropdwn)
            row.find("TD").eq(4).find("select").append(assign_val.company_dropdwn)
        })
        i = i + 1;
    })
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
    $("#id_error_msg_aad_code").prop("hidden", true);
    $("#id_error_msg_aad_name").prop("hidden", true);
    $("#id_error_msg_aad_length").prop("hidden", true);
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
function compare_table_for_duplicate_entries(validate_add_attributes, aad) {
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
        } else{
        $.each(aad, function (i, item) {
        if (aad.account_assign_value == 0) {
        error_message = messageConstants["JMSG002"] + "Account Assignment  Category";
                no_duplicate_value = 'N'
                return [no_duplicate_value,error_message]
        }
    if (aad.description.length == 0) {
         error_message = messageConstants["JMSG002"] + "Description";
                no_duplicate_value = 'N'
                return [no_duplicate_value,error_message]
    }
    });
   }
//    description = aad.description.replace(/\s\s+/g, ' ')
//    if (description == " ") {
//        $("#id_error_msg").prop("hidden", false)
//        Error_msg = "";
//        Error_msg = "Enter Valid data in Description";
//        document.getElementById("id_error_msg").innerHTML = Error_msg;
//        document.getElementById("id_error_msg").style.color = "Red";
//        $('#id_save_confirm_popup').modal('hide');
//        $('#myModal').modal('show');
//        no_duplicate_value = 'N'
//    }
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
    $(".modal").on("hidden.bs.modal", function () {
        $("#id_error_msg").html("");
    });
    basic_add_new_html = '<tr> <td><input class="input" type="checkbox" required></td> <td><select class="form-control">' + acc_ass_val_dropdwn + ' </select></td> <td><input class="form-control" type="text"  maxlength="255" style="text-transform:uppercase"></td> <td><select class="form-control"></select></td> <td ><select class="form-control"></select></td> <td><select class="form-control">' + language_dropdwn + '</select></td> <td hidden><input value="GUID"></td><td class="class_del_checkbox" hidden><input type="checkbox" required></td><td hidden> </td></tr>';
    $('#id_popup_tbody').append(basic_add_new_html);

    var account_assign = '';
    $("#id_popup_table TBODY TR").each(function () {
        var row = $(this);
        row.find("TD").eq(3).find("select").empty()
        row.find("TD").eq(4).find("select").empty()
        account_assign = row.find("TD").eq(1).find("select option:selected").val();
        var assign_val = account_assignment_value_find(account_assign)
        row.find("TD").eq(3).find("select").append(assign_val.acc_ass_dropdwn)
        row.find("TD").eq(4).find("select").append(assign_val.company_dropdwn)

        $(row.find("TD").eq(1).find("select")).change(function () {
            row.find("TD").eq(3).find("select").empty()
            row.find("TD").eq(4).find("select").empty()

            account_assign = row.find("TD").eq(1).find("select option:selected").val();

            var assign_val = account_assignment_value_find(account_assign)
            console.log(assign_val)
            row.find("TD").eq(3).find("select").append(assign_val.acc_ass_dropdwn)
            row.find("TD").eq(4).find("select").append(assign_val.company_dropdwn)
        })
    })

    if (GLOBAL_ACTION == "aad_upload") {
        $(".class_del_checkbox").prop("hidden", false);
    }
    table_sort_filter_popup_pagination('id_popup_table');
}


//onclick of cancel display the table in display mode............
function display_basic_db_data() {
    $('#display_basic_table').DataTable().destroy();
    $('#id_aad_tbody').empty();
    var edit_basic_data = '';
    $.each(rendered_accdatadescs_data, function (i, item) {
        edit_basic_data += '<tr ><td class="class_select_checkbox"><input class="checkbox_check" onclick="valueChanged()" type="checkbox" required></td><td>' + item.account_assign_value + '</td><td>' + item.description + '</td><td> ' + item.account_assign_cat + '</td><td >' + item.company_id + '</td><td>' + item.language_id + '</td><td hidden>' + item.acc_desc_guid + '</td></tr>';
    });
    $('#id_aad_tbody').append(edit_basic_data);
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
    var aad_code_check = new Array
    $("#id_popup_table TBODY TR").each(function () {
        var row = $(this);

        //*************** reading data from the pop-up ***************

        account_assign_value = row.find("TD").eq(1).find("select option:selected").val();
        description = (row.find("TD").eq(2).find('input[type="text"]').val()).toUpperCase();
        account_assign_cat = row.find("TD").eq(3).find("select option:selected").val();
        company_id = row.find("TD").eq(4).find("select option:selected").val();
        language_id = row.find("TD").eq(5).find("select option:selected").val();

        var compare = account_assign_value + '-' + account_assign_cat + '-' + company_id + '-' + language_id

        if (aad_code_check.includes(compare)) {
            $(row).remove();
        }

        aad_code_check.push(compare);


    })
    table_sort_filter_popup_pagination('id_popup_table')
    check_data()
}

//********************************************

function delete_invalid_aav() {
    $('#id_popup_table').DataTable().destroy();
    var aad_code_check = new Array
    $("#id_popup_table TBODY TR").each(function () {
        var row = $(this);

        //*************** reading data from the pop-up ***************

        account_assign_value = row.find("TD").eq(1).find("select option:selected").val();
        description = (row.find("TD").eq(2).find('input[type="text"]').val()).toUpperCase();
        account_assign_cat = row.find("TD").eq(3).find("select option:selected").val();
        company_id = row.find("TD").eq(4).find("select option:selected").val();
        language_id = row.find("TD").eq(5).find("select option:selected").val();
        check_value = row.find("TD").eq(8).html()

        if (check_value == "0") {
            $(row).remove();
        }
    })
    table_sort_filter_popup_pagination('id_popup_table')
    check_data()
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

// Function to hide and display save related popups
$('#save_id').click(function () {
    $('#myModal').modal('hide');
    aad_data = new Array();
     validate_add_attributes = [];
      $("#id_popup_table TBODY TR").each(function () {
     var row = $(this);
            aad = {};
            aad.del_ind = row.find("TD").eq(7).find('input[type="checkbox"]').is(':checked');
            aad.account_assign_value = row.find("TD").eq(1).find("select option:selected").val();
            aad.description = (row.find("TD").eq(2).find('input[type="text"]').val()).toUpperCase();
            aad.account_assign_cat = row.find("TD").eq(3).find("select option:selected").val();
            aad.company_id = row.find("TD").eq(4).find("select option:selected").val();
            aad.language_id = row.find("TD").eq(5).find("select option:selected").val();
            aad.acc_desc_guid = row.find("TD").eq(6).find('input[type="text"]').val();
            if (aad == undefined) {
                aad.account_assign_value = row.find("TD").eq(1).find('input[type="text"]').val();
            }
            if(aad.acc_desc_guid == undefined) {
                   aad.acc_desc_guid = ''
             }
            var compare = aad.account_assign_value + '-' + aad.account_assign_cat + '-' + aad.company_id +
            validate_add_attributes.push(compare);

          });
    $('#id_save_confirm_popup').modal('show');
});
