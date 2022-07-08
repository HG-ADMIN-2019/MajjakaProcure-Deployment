var aav_data = new Array();
var validate_add_attributes = [];
var aav={};//onclick of add button display myModal popup and set GLOBAL_ACTION button value
function onclick_add_button(button) {
    $("#error_msg_id").css("display", "none")
    $("#header_select").prop( "hidden", false );
    GLOBAL_ACTION = button.value
    $("#id_popup_tbody").empty();
    $('#myModal').modal('show');
    basic_add_new_html = '<tr> <td><input type="checkbox" required></td> <td><input class="form-control" type="number"  minlength="4" maxlength="40" name="Account Assignment Value" required></td><td><select class="form-control" id="acc_ass_val_dropdw">' + acc_ass_dropdwn + ' </select></td> <td ><select class="form-control" id="company_dropdw">' + company_dropdwn + '</select></td><td><input class="form-control" type="date" maxlength="10" name="Valid From Date" required></td> <td><input class="form-control" type="date" maxlength="10" name="Valid To Date" required></td>  <td hidden><input value=""></td> <td class="class_del_checkbox" hidden><input type="checkbox" required></td></tr>';
    $('#id_popup_tbody').append(basic_add_new_html);
    table_sort_filter('id_popup_table');
    $("#id_del_ind_checkbox").prop("hidden", true);
    document.getElementById("id_del_add_button").style.display = "block";
    $("#save_id").prop("hidden", false);
}

//onclick of upload button display id_data_upload popup and set GLOBAL_ACTION button value
function onclick_upload_button() {
    GLOBAL_ACTION = "aav_upload"
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
    var dropdown_select_array = []
    $("#id_popup_tbody").empty();
    $('#display_basic_table').DataTable().destroy();
    //Reference the Table.
    var grid = document.getElementById("display_basic_table");
     //Reference the CheckBoxes in Table.
    var checkBoxes = grid.getElementsByTagName("INPUT");
    var edit_basic_data = "";
    var guid= '';
    var unique_input = '';
    //Loop through the CheckBoxes.
    for (var i = 1; i < checkBoxes.length; i++) {
        if (checkBoxes[i].checked) {
        var row = checkBoxes[i].parentNode.parentNode;
            if(GLOBAL_ACTION == "COPY"){
                guid = 'GUID';
                unique_input = '<input class="form-control" type="number" value="' + row.cells[1].innerHTML + '" name="Account Assignment Value" maxlength="40" required>'
                edit_basic_data += '<tr> <td><input type="checkbox" required></td> <td>'+unique_input+'</td><td><select id="acc_dropdwn" class="form-control" id="acc_ass_val_dropdw">' + acc_ass_dropdwn + ' </select></td> <td ><select class="form-control" id="company_dropdw">' + company_dropdwn + '</select> </td> <td><input class="form-control" type="date" value="' + row.cells[4].innerHTML + '" maxlength="10" name="Valid From Date" required></td> <td><input class="form-control" type="date" value="' + row.cells[5].innerHTML + '" maxlength="10" name="Valid To Date" required></td> <td hidden><input value="' + guid + '"></td> <td class="class_del_checkbox" hidden><input type="checkbox" required></td></tr>';
                $("#header_select").prop("hidden",false);
            }
            else{
                guid = row.cells[6].innerHTML;
                unique_input = '<input class="form-control" type="number" value="' + row.cells[1].innerHTML + '" name="Account Assignment Value" maxlength="40" disabled>'
                edit_basic_data += '<tr> <td hidden><input type="checkbox" required></td> <td>'+unique_input+'</td><td><select id="acc_dropdwn" class="form-control"  id="acc_ass_val_dropdw" disabled>' + acc_ass_dropdwn + ' </select></td> <td ><select class="form-control" id="company_dropdw" disabled>' + company_dropdwn + '</select> </td> <td><input class="form-control" type="date" value="' + row.cells[4].innerHTML + '" maxlength="10" name="Valid From Date" required></td> <td><input class="form-control" type="date" value="' + row.cells[5].innerHTML + '" maxlength="10" name="Valid To Date" required></td>  <td hidden><input value="' + guid + '"></td> <td class="class_del_checkbox" hidden><input type="checkbox" required></td></tr>';
                $("#header_select").prop("hidden",true);
            }
            var row = checkBoxes[i].parentNode.parentNode;
            var account_assign_cat = row.cells[2].innerHTML
            var company_id = row.cells[3].innerHTML
            dropdown_select_array.push([account_assign_cat, company_id])

            $("#acc_dropdwn").val(row.cells[2])
            console.log(row.cells[2])

        }
    }
    $('#id_popup_table').append(edit_basic_data);
    var i =0;
    $("#id_popup_table TBODY TR").each(function() {
        var row = $(this);
        var account_assign_cat = dropdown_select_array[i][0]
        var company_id = dropdown_select_array[i][1]
        $(row.find("TD").eq(2).find("select option[value="+account_assign_cat+"]")).attr('selected','selected');
        $(row.find("TD").eq(3).find("select option[value="+company_id+"]")).attr('selected','selected');
        i++;
    });
    $("#id_del_ind_checkbox").prop("hidden", true);
    table_sort_filter('display_basic_table');
    table_sort_filter('id_popup_table');
    $('#myModal').modal('show');
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
    basic_add_new_html = '<tr> <td><input type="checkbox" required></td><td><input class="form-control" type="number" minlength="4" maxlength="40" name="Account Assignment Value" required></td><td><select class="form-control" id="acc_ass_val_dropdw">' + acc_ass_dropdwn + ' </select></td> <td ><select class="form-control" id="company_dropdw">' + company_dropdwn + '</select></td><td><input class="form-control" type="date" maxlength="10" name="Valid From Date" required></td> <td><input class="form-control" type="date" maxlength="10" name="Valid To Date" required></td>  <td hidden><input value=""></td> <td class="class_del_checkbox" hidden><input type="checkbox" required></td></tr>';
   $('#id_popup_tbody').append(basic_add_new_html);
    if (GLOBAL_ACTION == "aav_upload") {
        $(".class_del_checkbox").prop("hidden", false);
    }
    table_sort_filter_popup('id_popup_table');

}


//onclick of cancel display the table in display mode............
function display_basic_db_data() {
    $('#display_basic_table').DataTable().destroy();
    $('#id_aav_tbody').empty();
    var edit_basic_data = '';
    $.each(rendered_account_assignment_value, function(index, value) {

         edit_basic_data += '<tr><td class="class_select_checkbox"><input class="checkbox_check" onclick="valueChanged()" type="checkbox" required></td><td>' + value.account_assign_value + '</td><td>' + value.account_assign_cat + '</td><td>' + value.company_id + '</td><td>' + value.valid_from + '</td><td>' + value.valid_to+ '</td><td hidden>' + value.account_assign_guid + '</td></tr>'
    });

    $('#display_basic_table').append(edit_basic_data);

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


function check_date_error(check_dates){
    date_error = "N"
    $.each(check_dates, function(index, value){
        var d1=new Date(value[0]); //yyyy-mm-dd
        var d2=new Date(value[1]); //yyyy-mm-dd
        if (d2< d1){

               
                var msg = "JMSG017";
                var msg_type ;
              msg_type = message_config_details(msg);
              $("#error_msg_id").prop("hidden", false)

              if(msg_type.message_type[0] == "ERROR"){
                    display_message("error_msg_id", msg_type.messages_id_desc[0])
              }
              else if(msg_type.message_type[0] == "WARNING"){
                 display_message("id_warning_msg_id", msg_type.messages_id_desc[0])
              }
              else if(msg_type.message_type[0] == "INFORMATION"){
                 display_message("id_info_msg_id", msg_type.messages_id_desc[0])
              }
                    var display = msg_type.messages_id_desc[0];
                document.getElementById("id_error_msg").innerHTML = display;
                document.getElementById("id_error_msg").style.color = "Red";


            $('#id_save_confirm_popup').modal('hide');
            $('#myModal').modal('show');
            date_error = 'Y'
        }
    })
    return date_error
}

$(".remove_upload_data").click(() => {
    $("#id_error_msg").html("");
    $("#id_popup_tbody").empty();
    $("#id_error_msg").empty();
    $('#myModal').modal('hide');
    $("#id_error_msg").prop("hidden", true);
    $("#id_error_msg_aav_code").prop("hidden", true);
    $("#id_error_msg_aav_name").prop("hidden", true);
    $("#id_error_msg_aav_length").prop("hidden", true);
    $("#id_check_error_messages").prop("hidden", true);
    $("#id_check_success_messages").prop("hidden", true);
    $("#id_check_special_character_messages").prop("hidden", true)
    $("#id_check_data").prop("hidden", true);
    $('#id_popup_table').DataTable().destroy();
});


 //**********************************************
 function delete_duplicate() {
    $('#id_popup_table').DataTable().destroy();
    var aav_code_check = new Array
    $("#id_popup_table TBODY TR").each(function() {
        var row = $(this);

        //*************** reading data from the pop-up ***************

        account_assign_value = row.find("TD").eq(1).find('input[type="number"]').val();
        valid_from = row.find("TD").eq(4).find('input[type="date"]').val()
        valid_to = row.find("TD").eq(5).find('input[type="date"]').val()
        account_assign_cat = row.find("TD").eq(2).find('Select').val()
        company_id = row.find("TD").eq(3).find('Select').val()

        var compare = account_assign_value + '-' + account_assign_cat + '-' + company_id

        if (aav_code_check.includes(compare)) {
            $(row).remove();
        }

        aav_code_check.push(compare);


    })
    table_sort_filter_popup_pagination('id_popup_table')
    check_data()
}

// Functtion to hide and display save related popups
$('#save_id').click(function () {
    $('#myModal').modal('hide');
    var aav={};
     validate_add_attributes = [];
     $("#id_popup_table TBODY TR").each(function () {
            var row = $(this);
            aav={};
            aav.del_ind = row.find("TD").eq(7).find('input[type="checkbox"]').is(':checked');
                aav.account_assign_value = row.find("TD").eq(1).find('input[type="number"]').val();
                aav.valid_from = row.find("TD").eq(4).find('input[type="date"]').val()
                aav.valid_to = row.find("TD").eq(5).find('input[type="date"]').val()
                aav.account_assign_cat = row.find("TD").eq(2).find('Select').val()
                aav.company_id = row.find("TD").eq(3).find('Select').val()
                aav.account_assign_guid = row.find("TD").eq(6).find('input[type="text"]').val();
                if (aav == undefined) {
                    aav.account_assign_value = row.find("TD").eq(1).find('input[type="text"]').val();
                }
                 if(aav.account_assign_guid == undefined) {
                   aav.account_assign_guid = ''
                 }


            validate_add_attributes.push(aav.account_assign_value);
            aav_data.push(aav);
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
function check_date(aav) {
    var validDate = 'Y';
    var error_message = ''
     $.each(aav, function (i, item) {
        if ((Date.parse(item.valid_to) < Date.parse(item.valid_from)) == true) {
        $("#id_error_msg").prop("hidden", false)
       
                var msg = "JMSG017";
                var msg_type ;
              msg_type = message_config_details(msg);
              $("#error_msg_id").prop("hidden", false)

              if(msg_type.message_type[0] == "ERROR"){
                    display_message("error_msg_id", msg_type.messages_id_desc[0])
              }
              else if(msg_type.message_type[0] == "WARNING"){
                 display_message("id_warning_msg_id", msg_type.messages_id_desc[0])
              }
              else if(msg_type.message_type[0] == "INFORMATION"){
                 display_message("id_info_msg_id", msg_type.messages_id_desc[0])
              }
              var display = msg_type.messages_id_desc[0];
              error_message = display;

        $('#id_save_confirm_popup').modal('hide');
        onclick_copy_update_button(item.account_assign_value);
        $('#myModal').modal('show');
        validDate = 'N'
    }
    });
    return [validDate,error_message]
}



