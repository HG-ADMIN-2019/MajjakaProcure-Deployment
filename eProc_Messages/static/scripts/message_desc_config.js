var message_id_desc_data = new Array();
var validate_add_attributes = [];
var duplicate_entry = [];
var lang_values = [];
var message_id_desc={};
$(document).ready(function () {
    $('#nav_menu_items').remove();
    $("body").css("padding-top", "3.7rem");
    table_sort_filter('display_basic_table');
});

//**********************************
//onclick of upload button display id_data_upload popup and set GLOBAL_ACTION button value
function onclick_upload_button() {
    GLOBAL_ACTION = "message_upload"
    $("#id_popup_tbody").empty();
    $('#id_data_upload').modal('show');
}

//******************
// on click copy icon display the selected checkbox data
function onclick_copy_button() {
    GLOBAL_ACTION = "COPY"
    onclick_copy_update_button()
    document.getElementById("id_del_add_button").style.display = "block";
}

//***********************************
// on click update icon display the selected checkbox data to update
function onclick_update_button() {
    GLOBAL_ACTION = "UPDATE"
    onclick_copy_update_button()
    document.getElementById("id_del_add_button").style.display = "none";
}



//************************
//onclick of cancel empty the popup table body and error messages
$(".remove_upload_data").click(() => {
    $("#id_error_msg_id").html("");
    $("#id_popup_tbody").empty();
    $("#id_error_msg_id").empty();
    $('#myModal').modal('hide');
    $("#id_error_msg_id").prop("hidden", true);
    $("#id_error_msg_id").prop("hidden", true);
//    $("#id_error_msg").prop("hidden", true);
    $("#id_error_msg_length").prop("hidden", true);
    $("#id_check_error_messages").prop("hidden", true);
    $("#id_check_success_messages").prop("hidden", true);
    $("#id_check_special_character_messages").prop("hidden", true)
    $("#id_check_data").prop("hidden", true);
    $('#id_popup_table').DataTable().destroy();


});

//*************************
// on click edit icon display the data in edit mode
function onclick_edit_button() {
    //display the add,cancel and upload buttons and select all checkbox,select heading and checkboxes for each row
    $('#display_basic_table').DataTable().destroy();
    $("#hg_select_checkbox").prop("hidden", false);
    $(".class_message_checkbox").prop("hidden", false);
    $("#hg_select_checkbox").show();
    //hide the edit,delete,copy and update buttons
    $("#id_edit_data").hide();
    $("#id_check_all").show();
    $("#id_cancel_data").show();
    table_sort_filter('display_basic_table');
}


//********************************
//onclick of select all checkbox
function checkAll(ele) {
    $('#display_basic_table').DataTable().destroy();
    var checkboxes = document.getElementsByTagName('input');
    if (ele.checked) {
        for (var i = 0; i < checkboxes.length; i++) {
            if (checkboxes[i].type == 'checkbox') {
                checkboxes[i].checked = true;
                $("#id_delete_data").show();
                $("#id_copy_data").show();
                $("#id_update_data").show();
            }
        }
    } else {
        for (var i = 0; i < checkboxes.length; i++) {
            if (checkboxes[i].type == 'checkbox') {
                checkboxes[i].checked = false;
                $("#id_delete_data").hide();
                $("#id_copy_data").hide();
                $("#id_update_data").hide();
            }
        }
    }
    table_sort_filter('display_basic_table');
}


//**********************************
//onclick of checkbox display delete,update and copy Buttons
function valueChanged() {
    if ($('.checkbox_check').is(":checked")) {
        $("#id_delete_data").show();
        $("#id_copy_data").show();
        $("#id_update_data").show();
    }
    else {
        $("#id_delete_data").hide();
        $("#id_copy_data").hide();
        $("#id_update_data").hide();
    }
}


//#############################
//*******************************************************


//***************************
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

        $("#id_delete_data").hide();
        $("#id_copy_data").hide();
        $("#id_update_data").hide();
        table_sort_filter_popup_pagination('id_popup_table');
        return rowCount;
    } catch (e) {
        alert(e);
    }
}


//***********************************

function delete_duplicate() {
    $('#id_popup_table').DataTable().destroy();
    var message_id_check = new Array
    $("#id_popup_table TBODY TR").each(function () {
        var row = $(this);

        //*************** reading data from the pop-up ***************
        message_type = row.find("TD").eq(2).find('select[type="text"]').val();
        message_id = row.find("TD").eq(1).find('input[type="text"]').val().toUpperCase();
        checked_box = row.find("TD").eq(3).find('input[type="checkbox"]').is(':checked')


        if (message_id_check.includes(messages_id)) {
            $(row).remove();
        }
        message_id_check.push(messages_id);
    })
    table_sort_filter_popup_pagination('id_popup_table')
    check_data()
}



//onclick of cancel display the table in display mode............
function display_basic_db_data() {
    $('#display_basic_table').DataTable().destroy();
    $('#id_message_tbody').empty();
    var edit_basic_data = '';
    var desc = ''; var lang_code;

    $.each(rendered_message_id_desc_data, function (i, item) {

           lang_code = item.language_id;
            for (i = 0; i < render_language_data.length; i++) {
                if (lang_code == render_language_data[i].language_id)
                    desc = render_language_data[i].description
            }
        edit_basic_data += '<tr><td class="class_message_checkbox"><input class="checkbox_check" onclick="valueChanged()" type="checkbox" required></td>'+
        '<td>' + item.messages_id + '</td><td>' + item.messages_id_desc + '</td>'+
         '<td>' + desc + '</td>'+
        '<td hidden>' + item.msg_id_desc_guid + '</td>'+
       '</tr>';
    });
    $('#id_message_tbody').append(edit_basic_data);

    $("#hg_select_checkbox").prop("hidden", true);
    $(".class_message_checkbox").prop("hidden", true);
    $('input:checkbox').removeAttr('checked');
    $("#id_edit_data").show();
    $("#id_cancel_data").hide();
    $("#id_delete_data").hide();
    $("#id_copy_data").hide();
    $("#id_update_data").hide();
    $('#id_save_confirm_popup').modal('hide');
    $("#id_delete_confirm_popup").hide();
    $("#id_check_all").hide();
    table_sort_filter('id_popup_table');
    table_sort_filter('display_basic_table');
}

function display_error_message(error_message){

        $('#error_message').text(error_message);

        document.getElementById("error_message").style.color = "Red";
        $("#error_msg_id").css("display", "block");

        $('#id_save_confirm_popup').modal('hide');
        $('#myModal').modal('show');
}

 // Functtion to hide and display save related popups
$('#save_id').click(function () {
    $('#myModal').modal('hide');
     message_id_desc_data = new Array();
     validate_add_attributes = [];
     lang_values = [];
     duplicate_entry = [];
    $("#id_popup_table TBODY TR").each(function () {
            var row = $(this);
            message_id_desc={};
            message_id_desc.msg_id_desc_guid = row.find("TD").eq(5).find('input[type="text"]').val();
            message_id_desc.del_ind = row.find("TD").eq(4).find('input[type="checkbox"]').is(':checked');
            message_id_desc.language_id = row.find("TD").eq(3).find('select[type="text"]').val();
            message_id_desc.message_id_desc = row.find("TD").eq(2).find('input[type="text"]').val();
            message_id_desc.messages_id = row.find("TD").eq(1).find('select[type="text"]').val();

            if (message_id_desc == undefined){
                message_id_desc.messages_id = row.find("TD").eq(1).find('select[type="text"]').val();
             }
            if(message_id_desc.msg_id_desc_guid == undefined) {
                   message_id_desc.msg_id_desc_guid = ''
                }
            var desc='';
            for (i = 0; i < render_language_data.length; i++) {
                if (message_id_desc.language_id == render_language_data[i].language_id)
                    desc = render_language_data[i].description;
            }

             var attribute_dup = {};
            attribute_dup.messages_id = message_id_desc.messages_id;
            attribute_dup.language_id = desc;
            duplicate_entry.push(attribute_dup);

             validate_add_attributes.push(message_id_desc.messages_id);
            //lang_values.push(desc);
            message_id_desc_data.push(message_id_desc);
        });
    $('#id_save_confirm_popup').modal('show');
});

