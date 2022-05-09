var alv_data = new Array();
var validate_add_attributes = [];
var alv={};
//onclick of add button display myModal popup and set GLOBAL_ACTION button value
function onclick_add_button(button) {
    $("#error_msg_id").css("display", "none")
    $("#header_select").prop( "hidden", false );
    GLOBAL_ACTION = button.value
    $("#id_popup_tbody").empty();
    $('#myModal').modal('show');
    basic_add_new_html = '<tr><td><input type="checkbox" required></td><td><input class="form-control" type="text" maxlength="8" onkeypress="return /[a-z0-9]/i.test(event.key)" name="approver_code" style="text-transform:uppercase;" required></td><td><select class="form-control">'+company_id_dropdown+'</select></td><td><select class="form-control">'+ approval_type_dropdown +'</select></td><td><input class="form-control" type="number" name="upper_limit_value" required></td><td><select class="form-control">'+currency_id_dropdown+'</select></td><td hidden><input type="text" value=""></td><td class="class_del_checkbox" hidden><input type="checkbox" required></td></tr>';
    $('#id_popup_tbody').append(basic_add_new_html);
    table_sort_filter('id_popup_table');
    $("#id_del_ind_checkbox").prop("hidden", true);
    document.getElementById("id_del_add_button").style.display = "block";
    $("#save_id").prop("hidden", false);
}


//onclick of upload button display id_data_upload popup and set GLOBAL_ACTION button value
function onclick_upload_button() {
    GLOBAL_ACTION = "alv_upload"
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
    $("#id_popup_tbody").empty();
    $('#display_basic_table').DataTable().destroy();
    //Reference the Table.
    var grid = document.getElementById("display_basic_table");

    //Reference the CheckBoxes in Table.
    var checkBoxes = grid.getElementsByTagName("INPUT");
    var edit_basic_data = "";
    var guid = '';
    var dropdown_values = [];
    //Loop through the CheckBoxes.
    for (var i = 1; i < checkBoxes.length; i++) {
        if (checkBoxes[i].checked) {
        var row = checkBoxes[i].parentNode.parentNode;
            if(GLOBAL_ACTION == "COPY"){
                guid = 'GUID';
                  edit_basic_data += '<tr><td><input type="checkbox" required></td><td><input class="form-control" type="text" value="'+row.cells[1].innerHTML+'" maxlength="8" onkeypress="return /[a-z0-9]/i.test(event.key)" name="approver_code" style="text-transform:uppercase;" required></td><td><select class="form-control">'+company_id_dropdown+'</select></td><td><select class="form-control">'+approval_type_dropdown+'</select></td><td><input class="form-control" type="number" value="'+row.cells[4].innerHTML+'" name="upper_limit_value" required></td><td><select class="form-control">'+currency_id_dropdown+'</select></td><td hidden><input type="text" value="'+guid+'"></td><td class="class_del_checkbox" hidden><input type="checkbox" required></td></tr>';

            } else{
                guid = row.cells[6].innerHTML;
                  edit_basic_data += '<tr><td hidden><input type="checkbox" required></td><td><input class="form-control" type="text" value="'+row.cells[1].innerHTML+'" maxlength="8" onkeypress="return /[a-z0-9]/i.test(event.key)" name="approver_code" style="text-transform:uppercase;" disabled></td><td><select class="form-control" disabled>'+company_id_dropdown+'</select></td><td><select class="form-control" disabled>'+approval_type_dropdown+'</select></td><td><input class="form-control" type="number" value="'+row.cells[4].innerHTML+'" name="upper_limit_value" required></td><td><select class="form-control" disabled>'+currency_id_dropdown+'</select></td><td hidden><input type="text" value="'+guid+'"></td><td class="class_del_checkbox" hidden><input type="checkbox" required></td></tr>';
                   $("#header_select").prop("hidden", true);
            }
            var row = checkBoxes[i].parentNode.parentNode;
            var company_type_value = row.cells[2].innerHTML
            var approval_type_value = row.cells[3].innerHTML
            var currency_type_value = row.cells[5].innerHTML

            dropdown_values.push([company_type_value,approval_type_value, currency_type_value ])
            //edit_basic_data += '<tr><td><input type="checkbox" required></td><td><input class="form-control" type="text" value="'+row.cells[1].innerHTML+'" maxlength="8" onkeypress="return /[a-z0-9]/i.test(event.key)" name="approver_code" style="text-transform:uppercase;" required></td><td><input class="form-control" type="number" value="'+row.cells[2].innerHTML+'" name="upper_limit_value" required></td><td><select class="form-control">'+approval_type_dropdown+'</select></td><td><select class="form-control">'+currency_id_dropdown+'</select></td><td><select class="form-control">'+company_id_dropdown+'</select></td><td hidden><input type="text" value="'+guid+'"></td><td class="class_del_checkbox" hidden><input type="checkbox" required></td></tr>';
        }
    }
    $('#id_popup_table').append(edit_basic_data);
    var i =0;
    $("#id_popup_table TBODY TR").each(function() {
        var row = $(this);
        var company_type_value = dropdown_values[i][0]
        var approval_type_value = dropdown_values[i][1]
        var currency_type_value = dropdown_values[i][2]
        $(row.find("TD").eq(2).find("select option[value="+company_type_value+"]")).attr('selected','selected');
        $(row.find("TD").eq(3).find("select option[value="+approval_type_value+"]")).attr('selected','selected');
        $(row.find("TD").eq(5).find("select option[value="+currency_type_value+"]")).attr('selected','selected');

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
    $('#myModal').modal('hide');;
    $("#id_error_msg").prop("hidden", true);
    $("#id_error_msg_alv_code").prop("hidden", true);
    $("#id_error_msg_alv_name").prop("hidden", true);
    $("#id_error_msg_alv_length").prop("hidden", true);
    $("#id_check_error_messages").prop("hidden", true);
    $("#id_check_success_messages").prop("hidden", true);
    $("#id_check_special_character_messages").prop("hidden", true)
    $("#id_check_data").prop("hidden", true);
    $('#id_popup_table').DataTable().destroy();
});

//validate by comparing  main table values and popup table values
function maintable_validation(validate_add_attributes, main_table_low_value) {
    var no_duplicate_entries = 'Y'
    var common = [];
    var error_message =''
    jQuery.grep(validate_add_attributes, function(el) {
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
function compare_table_for_duplicate_entries(validate_add_attributes, alv) {
    add_attr_duplicates = false;
    var error_message = ''
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
    } else{
           $.each(alv, function (i, item) {
           if(item.app_code_id.length == 0) {
           error_message = messageConstants["JMSG002"] + "Approver Code ID";
                no_duplicate_value = 'N'
                return [no_duplicate_value,error_message]
           }
          if (item.upper_limit_value <= 0) {
              error_message = messageConstants["JMSG002"] + "upper_limit_value";
                no_duplicate_value = 'N'
                return [no_duplicate_value,error_message]
                 }
         });
}
return [no_duplicate_value,error_message]
}
//*******************************************************

// on click add icon display the row in to add the new entries
function add_popup_row() {
    basic_add_new_html = '';
    var display_db_data = '';
    $('#id_popup_table').DataTable().destroy();
    $(".modal").on("hidden.bs.modal", function() {
        $("#id_error_msg").html("");
    });
    basic_add_new_html = '<tr><td><input type="checkbox" required></td><td><input class="form-control" type="text" maxlength="8" onkeypress="return /[a-z0-9]/i.test(event.key)" name="approver_code" style="text-transform:uppercase;" required></td><td><select class="form-control">'+company_id_dropdown+'</select class="form-control"></td><td><select class="form-control" >'+approval_type_dropdown+'</select></td><td><input class="form-control" type="number" name="upper_limit_value" required></td><td><select class="form-control">'+currency_id_dropdown+'</select></td><td hidden><input type="text" value=""></td><td class="class_del_checkbox" hidden><input type="checkbox" required></td></tr>';
    $('#id_popup_tbody').append(basic_add_new_html);
    if (GLOBAL_ACTION == "alv_upload") {
        $(".class_del_checkbox").prop("hidden", false);
    }
    table_sort_filter_popup_pagination('id_popup_table');
}


//onclick of cancel display the table in display mode............
function display_basic_db_data() {
    $('#display_basic_table').DataTable().destroy();
    $('#id_alv_tbody').empty();
    var edit_basic_data = '';
    $.each(rendered_alv_data, function(i, item) {
        edit_basic_data += '<tr ><td class="class_select_checkbox"><input class="checkbox_check" onclick="valueChanged()" type="checkbox" required></td><td>' + item.app_code_id + '</td><td>' + item.company_id + '</td><td>' + item.app_types + '</td><td>' + item.upper_limit_value + '</td><td>' + item.currency_id + '</td><td hidden>' + item.app_lim_dec_guid + '</td></tr>';
    });
    $('#id_alv_tbody').append(edit_basic_data);
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
    var alv_code_check = new Array
    $("#id_popup_table TBODY TR").each(function() {
        var row = $(this);

        //*************** reading data from the pop-up ***************
        app_code_id = row.find("TD").eq(1).find('input[type="text"]').val().toUpperCase();
        upper_limit_value = row.find("TD").eq(4).find('input[type="number"]').val().toUpperCase();
        app_types = row.find("TD").eq(3).find("select option:selected").val();
        currency_id = row.find("TD").eq(5).find("select option:selected").val();
        company_id = row.find("TD").eq(2).find("select option:selected").val();
        app_lim_dec_guid = row.find("TD").eq(6).find('input[type="text"]').val().toUpperCase()
        alv_compare = alv.app_code_id +'-'+ alv.app_types +'-'+ alv.company_id

        if (alv_code_check.includes(alv_compare)) {
            $(row).remove();
        }
        alv_code_check.push(alv_compare);
    })
    table_sort_filter_popup_pagination('id_popup_table')
    check_data()
}
$('#save_id').click(function () {
    $('#myModal').modal('hide');
     validate_add_attributes = [];
     var alv={};
      $("#id_popup_table TBODY TR").each(function () {
    var row = $(this);
            alv = {};
            alv.del_ind = row.find("TD").eq(7).find('input[type="checkbox"]').is(':checked');
            alv.app_code_id = row.find("TD").eq(1).find('input[type="text"]').val().toUpperCase();
            alv.upper_limit_value = row.find("TD").eq(4).find('input[type="number"]').val();
            alv.app_types = row.find("TD").eq(3).find("select option:selected").val();
            alv.currency_id = row.find("TD").eq(5).find("select option:selected").val();
            alv.company_id = row.find("TD").eq(2).find("select option:selected").val();
            alv.app_lim_dec_guid = row.find("TD").eq(6).find('input[type="text"]').val().toUpperCase()

            if (alv == undefined) {
                alv.app_code_id = row.find("TD").eq(1).find('input[type="text"]').val();
            }
            if(alv.app_lim_dec_guid  == undefined) {
                  alv.app_lim_dec_guid  = ''
             }
             var alv_compare = alv.app_code_id +'-'+ alv.company_id +'-'+ alv.app_types+'-'+alv.currency_id
            validate_add_attributes.push(alv_compare);
            alv_data.push(alv);
});
 $('#id_save_confirm_popup').modal('show');
});
function display_error_message(error_message){

        $('#error_message').text(error_message);
        //$("p").css("color", "red");
        //document.getElementById("error_message").innerHTML = error_message;
        document.getElementById("error_message").style.color = "Red";
        $("#error_msg_id").css("display", "block")
        $('#id_save_confirm_popup').modal('hide');
        $('#myModal').modal('show');

}