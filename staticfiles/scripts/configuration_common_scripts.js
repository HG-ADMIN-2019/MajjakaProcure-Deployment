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
    $(".class_select_checkbox").prop("hidden", false);

    //hide the edit,delete,copy and update buttons
    $('#id_cancel_data').show();
    $('#id_edit_data').hide();
    $('#id_check_all').show();
    table_sort_filter('display_basic_table');
}

//onclick of select all checkbox
function checkAll(ele) {
    $('#display_basic_table').DataTable().destroy();
    var checkboxes = document.getElementsByTagName('input');
    if (ele.checked) {
        for (var i = 0; i < checkboxes.length; i++) {
            if (checkboxes[i].type == 'checkbox') {
                checkboxes[i].checked = true; 
                $('#id_delete_data').show();
                $('#id_copy_data').show();
                $('#id_update_data').show();
            }
        }
    } else {
        for (var i = 0; i < checkboxes.length; i++) {
            if (checkboxes[i].type == 'checkbox') {
                checkboxes[i].checked = false; 
                $('#id_delete_data').hide();
                $('#id_copy_data').hide();
                $('#id_update_data').hide(); 
            }
        }
    }
    table_sort_filter('display_basic_table');
}

//onclick of checkbox display delete,update and copy Buttons
function valueChanged() {
    if ($('.checkbox_check').is(":checked")) {
        $('#id_delete_data').show();
        $('#id_copy_data').show();
        $('#id_update_data').show();
    } else {
        $('#id_delete_data').hide();
        $('#id_copy_data').hide();
        $('#id_update_data').hide();
    }
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
        $("#id_delete_currency").hide();
        $("#id_copy_currency").hide();
        $("#id_update_currency").hide();
        $("#error_msg_id").css("display", "none");
        table_sort_filter_popup('id_popup_table');
        return rowCount;
    } catch (e) {
        alert(e);
    }
}









//// Function to hide and display save related popups
//$('#save_id').click(function () {
//    $('#myModal').modal('hide');
//    $('#id_save_confirm_popup').modal('show');
//});