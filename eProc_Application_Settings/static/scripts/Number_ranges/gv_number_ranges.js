$(document).ready(function () {
    $('#nav_menu_items').remove();
    $("body").css("padding-top", "3.7rem");
    table_sort_filter('display_basic_table');
});

// on click edit icon display the data in edit mode
function onclick_edit_button() {
    //display the add,cancel and upload buttons and select all checkbox,select heading and checkboxes for each row
    $('#display_basic_table').DataTable().destroy();
    $("#hg_select_checkbox").prop("hidden", false);
    $(".class_number_range_checkbox").prop("hidden", false);
    $("#id_cancel_number_range").show();
    //hide the edit,delete,copy and update buttons
    $("#id_edit_number_range").hide();
    $("#id_check_all").show();
    table_sort_filter('display_basic_table');
}


//onclick of add button display myModal popup and set GLOBAL_ACTION button value
function onclick_add_button(button) {
    GLOBAL_ACTION = button.value
    $("#id_popup_tbody").empty();
    $('#myModal').modal('show');
    basic_add_new_html = '<tr ><td><input type="checkbox" required></td><td><input class="form-control" type="text" maxlength="2" onkeypress="return /[0-9]/i.test(event.key)" name="sequence" style="text-transform:uppercase;" required></td><td><input class="form-control" type="text" maxlength="100000000" onkeypress="return /[0-9]/i.test(event.key)" name="starting" style="text-transform:uppercase;" required></td><td><input class="form-control" type="text" maxlength="100000000" onkeypress="return /[0-9]/i.test(event.key)" name="ending" style="text-transform:uppercase;" required></td><td><input class="form-control" type="text" maxlength="100000000" onkeypress="return /[0-9]/i.test(event.key)" name="current" style="text-transform:uppercase;" required></td>><td hidden><input type="text" value=""></td><td class="class_del_checkbox" hidden><input type="checkbox" required></td></tr>';
    $('#id_popup_tbody').append(basic_add_new_html);
    $("#id_del_ind_checkbox").prop("hidden", true);
    document.getElementById("id_del_add_button").style.display = "block";
    $("#save_id").prop("hidden", false);
}


//onclick of upload button display id_data_upload popup and set GLOBAL_ACTION button value
function onclick_upload_button() {
    GLOBAL_ACTION = "number_range_upload"
    $("#id_popup_tbody").empty();
    ('#id_data_upload').modal('show');
}

// on click copy icon display the selected checkbox data
function onclick_copy_button() {
    GLOBAL_ACTION = "number_range_copy"
    onclick_copy_update_button()
    document.getElementById("id_del_add_button").style.display = "block";
}

// on click update icon display the selected checkbox data to update
function onclick_update_button() {
    GLOBAL_ACTION = "number_range_update"
    onclick_copy_update_button()
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
    //Loop through the CheckBoxes.
    for (var i = 1; i < checkBoxes.length; i++) {
        if (checkBoxes[i].checked) {
            var row = checkBoxes[i].parentNode.parentNode;
            edit_basic_data += '<tr ><td><input type="checkbox" required></td><td><input class="form-control" type="text" value="' + row.cells[1].innerHTML + '" name="sequence" onkeypress="return /[0-9]/i.test(event.key)" maxlength="2" style="text-transform:uppercase" required></td><td><input class="form-control" value="' + row.cells[2].innerHTML + '" type="text" onkeypress="return /[0-9]/i.test(event.key)" name="starting"  maxlength="100000000" style="text-transform:uppercase" required></td><td><input class="form-control" value="' + row.cells[3].innerHTML + '" type="text" onkeypress="return /[0-9]/i.test(event.key)" name="ending"  maxlength="100000000" style="text-transform:uppercase" required></td><td><input class="form-control" value="' + row.cells[4].innerHTML + '" type="text" onkeypress="return /[0-9]/i.test(event.key)" name="current"  maxlength="100000000" style="text-transform:uppercase" required></td><td hidden><input class="form-control" type="text" value="' + row.cells[5].innerHTML + '"></td></tr>';
        }
    }
    $('#id_popup_table').append(edit_basic_data);
    $("#id_del_ind_checkbox").prop("hidden", true);
    table_sort_filter('id_popup_table');
    table_sort_filter('display_basic_table');
    $('#myModal').modal('show');
}

//onclick of cancel empty the popup table body and error messages
$(".remove_upload_data").click(() => {
    $("#id_error_msg").html("");
    $("#id_popup_tbody").empty();
    $("#id_error_msg").empty();
    $('#myModal').modal('hide');
    $("#id_error_msg").prop("hidden", true);
    $("#id_error_msg_sequence").prop("hidden", true);
    $("#id_error_msg_starting").prop("hidden", true);
    $("#id_error_msg_ending").prop("hidden", true);
    $("#id_error_msg_current").prop("hidden", true);
    $("#id_check_error_messages").prop("hidden", true);
    $("#id_check_success_messages").prop("hidden", true);
    $("#id_check_special_character_messages").prop("hidden", true)
    $("#id_check_data").prop("hidden", true);
    $('#id_popup_table').DataTable().destroy();
});


//onclick of select all checkbox
function checkAll(ele) {
    var checkboxes = document.getElementsByTagName('input');
    if (ele.checked) {
        for (var i = 0; i < checkboxes.length; i++) {
            if (checkboxes[i].type == 'checkbox') {
                checkboxes[i].checked = true;
                $("#id_delete_number_range").show();
                $("#id_copy_number_range").show();
                $("#id_update_number_range").show();
            }
        }
    } else {
        for (var i = 0; i < checkboxes.length; i++) {
            if (checkboxes[i].type == 'checkbox') {
                checkboxes[i].checked = false;
                $("#id_delete_number_range").hide();
                $("#id_copy_number_range").hide();
                $("#id_update_number_range").hide();

            }
        }
    }
}

//onclick of checkbox display delete,update and copy Buttons
function valueChanged() {
    if ($('.checkbox_check').is(":checked")) {
        $("#id_delete_number_range").show();
        $("#id_copy_number_range").show();
        $("#id_update_number_range").show();
    } else {
        $("#id_delete_number_range").hide();
        $("#id_copy_number_range").hide();
        $("#id_update_number_range").hide();
    }
}


//validate by comparing  main table values and popup table values
function maintable_validation(validate_add_attributes, main_table_low_value) {
    var no_duplicate_entries = 'Y'
    var common = [];
    jQuery.grep(validate_add_attributes, function (el) {
        if (jQuery.inArray(el, main_table_low_value) != -1) {
            common.push(el);
        }
    });
    if (common.length != 0) {
        $("#id_error_msg").prop("hidden", false)
        document.getElementById("id_error_msg").innerHTML = messageConstants["JMSG001"];
        document.getElementById("id_error_msg").style.color = "Red";
        $('#id_save_confirm_popup').modal('hide');
        $('#myModal').modal('show');
        no_duplicate_entries = 'N'
    }
    return no_duplicate_entries
}

// validating the  popup table for duplicate entries
function compare_table_for_duplicate_entries(validate_add_attributes, number_range) {
    add_attr_duplicates = false;
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
        $("#id_error_msg").prop("hidden", false)
        document.getElementById("id_error_msg").innerHTML = messageConstants["JMSG001"];
        document.getElementById("id_error_msg").style.color = "Red";
        $('#id_save_confirm_popup').modal('hide');
        $('#myModal').modal('show');
        no_duplicate_value = 'N'
    } else if (number_range.sequence.length == 0) {
        $("#id_error_msg").prop("hidden", false)
        Error_msg = "";
        Error_msg = messageConstants["JMSG002"] + "Sequence";
        document.getElementById("id_error_msg").innerHTML = Error_msg;
        document.getElementById("id_error_msg").style.color = "Red";
        $('#id_save_confirm_popup').modal('hide');
        $('#myModal').modal('show');
        no_duplicate_value = 'N'
    } else if (number_range.starting.length == 0) {
        $("#id_error_msg").prop("hidden", false)
        Error_msg = "";
        Error_msg = messageConstants["JMSG002"] + "Starting";
        document.getElementById("id_error_msg").innerHTML = Error_msg;
        document.getElementById("id_error_msg").style.color = "Red";
        $('#id_save_confirm_popup').modal('hide');
        $('#myModal').modal('show');
        no_duplicate_value = 'N'
    } else if (number_range.ending.length == 0) {
        $("#id_error_msg").prop("hidden", false)
        Error_msg = "";
        Error_msg = messageConstants["JMSG002"] + "Ending";
        document.getElementById("id_error_msg").innerHTML = Error_msg;
        document.getElementById("id_error_msg").style.color = "Red";
        $('#id_save_confirm_popup').modal('hide');
        $('#myModal').modal('show');
        no_duplicate_value = 'N'
    } else if (number_range.current.length == 0) {
        $("#id_error_msg").prop("hidden", false)
        Error_msg = "";
        Error_msg = messageConstants["JMSG002"] + "Current";
        document.getElementById("id_error_msg").innerHTML = Error_msg;
        document.getElementById("id_error_msg").style.color = "Red";
        $('#id_save_confirm_popup').modal('hide');
        $('#myModal').modal('show');
        no_duplicate_value = 'N'
    }

    return no_duplicate_value
}

// on click add icon display the row in to add the new entries
function add_popup_row() {
    basic_add_new_html = '';
    var display_db_data = '';
    $('#id_popup_table').DataTable().destroy();
    $(".modal").on("hidden.bs.modal", function () {
        $("#id_error_msg").html("");
    });
    basic_add_new_html = '<tr ><td><input type="checkbox" required></td><td><input class="form-control" type="text" maxlength="2" onkeypress="return /[0-9]/i.test(event.key)" name="sequence" style="text-transform:uppercase;" required></td><td><input class="form-control" type="text" maxlength="100000000" onkeypress="return /[0-9]/i.test(event.key)" name="starting" style="text-transform:uppercase;" required></td><td><input class="form-control" type="text" maxlength="100000000" onkeypress="return /[0-9]/i.test(event.key)" name="ending" style="text-transform:uppercase;" required></td><td><input class="form-control" type="text" maxlength="100000000" onkeypress="return /[0-9]/i.test(event.key)" name="current" style="text-transform:uppercase;" required></td><td class="class_del_checkbox" hidden><input type="checkbox" required></td></tr>';
    $('#id_popup_tbody').append(basic_add_new_html);
    if (GLOBAL_ACTION == "number_range") {
        $(".class_del_checkbox").prop("hidden", false);
    }
    table_sort_filter_popup_pagination('id_popup_table');
}

//onclick of delete,delete the row.
function application_settings_delete_Row(myTable) {
    $('#id_popup_table').DataTable().destroy();
    try {
        var table = document.getElementById(myTable);
        var rowCount = table.rows.length;

        for (var i = 0; i < rowCount; i++) {
            var row = table.rows[i];
            var chkbox = row.cells[0].childNodes[0];
            if (null != chkbox && true == chkbox.checked) {
                table.deleteRow(i);
                rowCount--;
                i--;
            }
        }

        $("#id_delete_number_range").hide();
        $("#id_copy_number_range").hide();
        $("#id_update_number_range").hide();
        table_sort_filter_popup_pagination('id_popup_table');
        return rowCount;
    } catch (e) {
        alert(e);
    }
}

//onclick of cancel display the table in display mode............
function display_basic_db_data() {
    $('#display_basic_table').DataTable().destroy();
    $('#id_number_range_tbody').empty();
    var edit_basic_data = '';
    $.each(rendered_number_range_data, function (i, item) {
        edit_basic_data += '<tr ><td class="class_number_range_checkbox"><input class="checkbox_check" onclick="valueChanged()" type="checkbox" required></td><td>' + item.sequence + '</td><td>' + item.starting + '</td><td>' + item.ending + '</td><td>' + item.current + '</td><td hidden>' + item.guid + '</td></tr>';
    });
    $('#id_number_range_tbody').append(edit_basic_data);
    $("#hg_select_checkbox").prop("hidden", true);
    $(".class_number_range_checkbox").prop("hidden", true);
    $('input:checkbox').removeAttr('checked');

    $("#id_edit_number_range").show();
    $("#id_cancel_number_range").hide();
    $("#id_delete_number_range").hide();
    $("#id_copy_number_range").hide();
    $("#id_update_number_range").hide();
    $('#id_save_confirm_popup').modal('hide');
    $("#id_delete_confirm_popup").hide();
    $("#id_check_all").hide();
    table_sort_filter('display_basic_table');
}

function delete_duplicate() {
    $('#id_popup_table').DataTable().destroy();
    var sequence_check = new Array
    $("#id_popup_table TBODY TR").each(function () {
        var row = $(this);

        //*************** reading data from the pop-up ***************
        sequence = row.find("TD").eq(1).find('input[type="text"]').val().toUpperCase();

        if (sequence_check.includes(sequence)) {
            $(row).remove();
        }

        sequence_check.push(sequence);

    })
    table_sort_filter_popup_pagination('id_popup_table')
    check_data()
}

// Function to hide and display save related popups
$('#save_id').click(function () {
    $('#myModal').modal('hide');
    $('#id_save_confirm_popup').modal('show');
});
