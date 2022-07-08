var message_id_data = new Array();
var validate_add_attributes = [];
//var country={};
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

//***********************************
// on click update icon display the selected checkbox data to update
function onclick_update_button() {
    GLOBAL_ACTION = "UPDATE"
    onclick_copy_update_button()
    document.getElementById("id_del_add_button").style.display = "none";
}


//**********************************************************
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
                 if(GLOBAL_ACTION == "UPDATE"){
                unique_input = '<select class="form-control" type="text" value="' + row.cells[1].innerHTML + '" name="message_id"  disabled>'+ msg_id_dropdown +'</select>'
                edit_basic_data += '<tr><td hidden><input type="checkbox" required></td>' +
                                    '<td>'+ unique_input +'</td>' +
                                    '<td><select id="message_type" class="input form-control" type="text" name="message_type">'+ msg_type_dropdown +'</select></td>'+
                                    '<td class="class_del_checkbox" hidden><input type="checkbox" required></td> <td hidden><input class="form-control" type="text" value="' + row.cells[3].innerHTML + '"></td></tr>';
                                    $("#header_select").prop("hidden", true);
                                    }

                     var message_id_value = row.cells[1].innerHTML
                     var message_type_value = row.cells[2].innerHTML
                    dropdown_values.push([message_type_value, message_id_value])
            }
        }
        $('#id_popup_table').append(edit_basic_data);
         var i =0;
        $("#id_popup_table TBODY TR").each(function() {
        var row = $(this);
         var messagetype_value = dropdown_values[i][0]
         var messageid_value = dropdown_values[i][1]
         $(row.find("TD").eq(1).find("select option[value="+messageid_value+"]")).attr('selected','selected');
         $(row.find("TD").eq(2).find("select option[value="+messagetype_value+"]")).attr('selected','selected');
             i++;
    });

        $("#id_del_ind_checkbox").prop("hidden", true);
        $('#myModal').modal('show');
        table_sort_filter('id_popup_table');
        table_sort_filter('display_basic_table');

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
function display_error_message(error_message){

        $('#error_message').text(error_message);
        //$("p").css("color", "red");
        //document.getElementById("error_message").innerHTML = error_message;
        document.getElementById("error_message").style.color = "Red";
        $("#error_msg_id").css("display", "block");
        $('#id_save_confirm_popup').modal('hide');
        $('#myModal').modal('show');

}

//*******************************************************
 // on click add icon display the row in to add the new entries
    function add_popup_row() {
        basic_add_new_html = '';
        var display_db_data = '';
        $('#id_popup_table').DataTable().destroy();
        $(".modal").on("hidden.bs.modal", function () {
            $("#id_error_msg_id").html("");
        });
        basic_add_new_html = '<tr><td><input type="checkbox" required></td>' +
            '<td><select class="input form-control" type="text"  name="message_id" required>'+ msg_id_dropdown +' </select></td>' +
            '<td><select id="message_type" name="message_type" class="input form-control" type="text">' + msg_type_dropdown +'</select></td>' +
            '<td class="class_del_checkbox" hidden><input type="checkbox" required></td>'+
            '<td hidden></td></tr>';

        $('#id_popup_tbody').append(basic_add_new_html);
        if (GLOBAL_ACTION == "message_id_upload") {
            $(".class_del_checkbox").prop("hidden", false);
        }
        table_sort_filter_popup_pagination('id_popup_table');
    }


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
//onclick of cancel display the table in display mode............
function display_basic_db_data() {
    $('#display_basic_table').DataTable().destroy();
    $('#id_message_tbody').empty();
    var edit_basic_data = '';

    $.each(rendered_message_id_data, function (i, item) {
        edit_basic_data += '<tr ><td class="class_message_checkbox"><input class="checkbox_check" onclick="valueChanged()" type="checkbox" required></td>'+
        '<td>' + item.messages_id + '</td><td>' + item.messages_type + '</td><td hidden>' + item.msg_id_guid + '</td></tr>';
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
  //  $("#id_check_all").hide();
    $("#id_check_all").prop("hidden", true);
    //$('#display_basic_table').append(edit_basic_data);
    table_sort_filter('display_basic_table');
}


function delete_duplicate() {
    $('#id_popup_table').DataTable().destroy();
    var message_id_check = new Array
    $("#id_popup_table TBODY TR").each(function () {
        var row = $(this);

        //*************** reading data from the pop-up ***************
        message_type = row.find("TD").eq(2).find('select[type="text"]').val();
        message_id = row.find("TD").eq(1).find('input[type="text"]').val().toUpperCase();
        checked_box = row.find("TD").eq(3).find('input[type="checkbox"]').is(':checked')


        if (message_id_check.includes(message_id)) {
            $(row).remove();
        }
        message_id_check.push(message_id);
    });
    table_sort_filter_popup_pagination('id_popup_table')
    check_data();
}

 // Functtion to hide and display save related popups
$('#save_id').click(function () {
    $('#myModal').modal('hide');
     message_id_data = new Array();
     validate_add_attributes = [];
    $("#id_popup_table TBODY TR").each(function () {
            var row = $(this);
            message_id={};
            message_id.msg_id_guid = row.find("TD").eq(4).find('input[type="text"]').val();
            message_id.del_ind = row.find("TD").eq(3).find('input[type="checkbox"]').is(':checked');
            message_id.message_type = row.find("TD").eq(2).find('select[type="text"]').val();
            message_id.message_id = row.find("TD").eq(1).find('select[type="text"]').val();
            if (message_id == undefined){
                message_id.message_id = row.find("TD").eq(1).find('input[type="text"]').val();
             }
             if(message_id.msg_id_guid == undefined) {
                   message_id.msg_id_guid = ''
                }
            validate_add_attributes.push(message_id.message_id);
            message_id_data.push(message_id);
        });
    $('#id_save_confirm_popup').modal('show');
});



