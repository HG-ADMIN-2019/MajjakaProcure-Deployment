var numberranges_data = new Array();
var validate_add_attributes = [];
var number_range={};//onclick of add button display myModal popup and set GLOBAL_ACTION button value
function onclick_add_button(button) {
//    $("#error_msg_id").css("display", "none")
//    $("#header_select").prop( "hidden", false );
//    GLOBAL_ACTION = button.value
//    $('#id_popup_table').DataTable().destroy();
//    $("#id_popup_tbody").empty();
//    $('#myModal').modal('show');
//    basic_add_new_html = '<tr ><td><input type="checkbox" required></td><td><input class="form-control" type="text" maxlength="2" onkeypress="return /[0-9]/i.test(event.key)" name="sequence" style="text-transform:uppercase;" required></td><td><input class="form-control" type="text" maxlength="100000000" onkeypress="return /[0-9]/i.test(event.key)" name="starting" style="text-transform:uppercase;" required></td><td><input class="form-control" type="text" maxlength="100000000" onkeypress="return /[0-9]/i.test(event.key)" name="ending" style="text-transform:uppercase;" required></td><td><input class="form-control" type="text" maxlength="100000000" onkeypress="return /[0-9]/i.test(event.key)" name="current" style="text-transform:uppercase;" required></td>><td hidden><input class="form-control" type="text" value=""></td><td class="class_del_checkbox" hidden><input type="checkbox" required></td></tr>';
//    $('#id_popup_tbody').append(basic_add_new_html);
//    table_sort_filter('id_popup_table');
//    $("#id_del_ind_checkbox").prop("hidden", true);
//    document.getElementById("id_del_add_button").style.display = "block";
//    $("#save_id").prop("hidden", false);
//}
  $("#error_msg_id").css("display", "none")
    $("#header_select").prop( "hidden", false );
    GLOBAL_ACTION = button.value
    $('#id_popup_table').DataTable().destroy();
    $("#id_popup_tbody").empty();
    $('#myModal').modal('show');
    console.log(max_sequence)
    basic_add_new_html = '<tr ><td class="number_range_checkbox"><input type="checkbox" required></td><td><input class="form-control" value="' + max_sequence + '" type="text"  name="sequence" style="text-transform:uppercase;" disabled></td><td><input class="form-control" type="text" maxlength="100000000" onkeypress="return /[0-9]/i.test(event.key)" name="starting" style="text-transform:uppercase;" required></td><td><input class="form-control" type="text" maxlength="100000000" onkeypress="return /[0-9]/i.test(event.key)" name="ending" style="text-transform:uppercase;" required></td><td><input class="form-control" type="text" maxlength="100000000" onkeypress="return /[0-9]/i.test(event.key)" name="current" style="text-transform:uppercase;" required></td>><td hidden><input type="text" value=""></td><td class="class_del_checkbox" hidden><input type="checkbox" required></td></tr>';
    $('#id_popup_tbody').append(basic_add_new_html);
    table_sort_filter('id_popup_table');
    $("#id_del_ind_checkbox").prop("hidden", true);
    document.getElementById("id_del_add_button").style.display = "block";
    $("#save_id").prop("hidden", false);
}

//onclick of upload button display id_data_upload popup and set GLOBAL_ACTION button value
function onclick_upload_button() {
    GLOBAL_ACTION = "number_range_upload"
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
             if (GLOBAL_ACTION == "COPY") {
                guid = '';
                edit_basic_data += '<tr ><td><input type="checkbox" required></td><td><input type="text" class="form-control" value="' + row.cells[1].innerHTML + '" name="sequence" onkeypress="return /[0-9]/i.test(event.key)" maxlength="2" style="text-transform:uppercase" required></td><td><input class="form-control" value="' + row.cells[2].innerHTML + '" type="text" onkeypress="return /[0-9]/i.test(event.key)" name="starting"  maxlength="100000000" style="text-transform:uppercase" required></td><td><input value="' + row.cells[3].innerHTML + '" type="text" class="form-control" onkeypress="return /[0-9]/i.test(event.key)" name="ending"  maxlength="100000000" style="text-transform:uppercase" required></td><td><input value="' + row.cells[4].innerHTML + '" type="text" class="form-control" onkeypress="return /[0-9]/i.test(event.key)" name="current"  maxlength="100000000" style="text-transform:uppercase" required></td><td hidden><input  type="text" class="form-control" value="' + guid + '"></td><td class="class_del_checkbox" hidden><input type="checkbox" required></td></tr>';

            } else {
                guid = row.cells[5].innerHTML;
                edit_basic_data += '<tr ><td><input type="checkbox" required></td><td><input type="text" class="form-control" value="' + row.cells[1].innerHTML + '" name="sequence" onkeypress="return /[0-9]/i.test(event.key)" maxlength="2" style="text-transform:uppercase" disabled></td><td><input class="form-control" value="' + row.cells[2].innerHTML + '" type="text" onkeypress="return /[0-9]/i.test(event.key)" name="starting"  maxlength="100000000" style="text-transform:uppercase" required></td><td><input value="' + row.cells[3].innerHTML + '" type="text" class="form-control" onkeypress="return /[0-9]/i.test(event.key)" name="ending"  maxlength="100000000" style="text-transform:uppercase" required></td><td><input value="' + row.cells[4].innerHTML + '" type="text" class="form-control" onkeypress="return /[0-9]/i.test(event.key)" name="current"  maxlength="100000000" style="text-transform:uppercase" required></td><td hidden><input  type="text" class="form-control" value="' + guid + '"></td><td class="class_del_checkbox" hidden><input type="checkbox" required></td></tr>';

            }
 //          edit_basic_data += '<tr ><td><input type="checkbox" required></td><td><input type="text" class="form-control" value="' + row.cells[1].innerHTML + '" name="sequence" onkeypress="return /[0-9]/i.test(event.key)" maxlength="2" style="text-transform:uppercase" required></td><td><input class="form-control" value="' + row.cells[2].innerHTML + '" type="text" onkeypress="return /[0-9]/i.test(event.key)" name="starting"  maxlength="100000000" style="text-transform:uppercase" required></td><td><input value="' + row.cells[3].innerHTML + '" type="text" class="form-control" onkeypress="return /[0-9]/i.test(event.key)" name="ending"  maxlength="100000000" style="text-transform:uppercase" required></td><td><input value="' + row.cells[4].innerHTML + '" type="text" class="form-control" onkeypress="return /[0-9]/i.test(event.key)" name="current"  maxlength="100000000" style="text-transform:uppercase" required></td><td hidden><input  type="text" class="form-control" value="' + guid + '"></td><td class="class_del_checkbox" hidden><input type="checkbox" required></td></tr>';
        }

    }
    $('#id_popup_table').append(edit_basic_data);
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


function list_out_of_range(number_range){
    var range_flag = true
    $.each(number_range, function (i, number) {
        if(range_flag){
            range_flag = inRange(number.current,number.starting,number.ending)
        }
    });
    return range_flag
}


function range_check_function(number_range,check_number_range){
    var validation_error = true
     $.each(number_range, function (i, number) {
        if (validation_error){
            $.each(check_number_range, function (j, check_number) {
                if(i!=j){
                    validation_error = inRange(number.starting,check_number.starting,check_number.ending)
                    if(validation_error == false){
                        return validation_error
                    }
                    else{
                        validation_error = inRange(number.ending,check_number.starting,check_number.ending)
                    }
                }
            });
        }
     });
     return validation_error
}

function main_range_check_function(number_range,check_number_range){
    var validation_error = true
     $.each(number_range, function (i, number) {
        if (validation_error){
            $.each(check_number_range, function (j, check_number) {
                validation_error = inRange(number.starting,check_number.starting,check_number.ending)
                if(validation_error == false){
                        return validation_error
                }
                else{
                    validation_error = inRange(number.ending,check_number.starting,check_number.ending)
                }
                if(validation_error == false){
                        return validation_error
                }
            });
        }
     });
     return validation_error
}

function inRange(x, min, max) {
    return !((x-min)*(x-max) <= 0);
}

var nextval = max_sequence ;
function add_popup_row() {
  $("#error_msg_id").css("display", "none")
    basic_add_new_html = '';
    var display_db_data = '';
    $('#id_popup_table').DataTable().destroy();
    $(".modal").on("hidden.bs.modal", function () {
        $("#id_error_msg").html("");
    });
    nextval += 1;
    basic_add_new_html = '<tr ><td class="number_range_checkbox"><input type="checkbox" required></td><td><input class="form-control"  type="text" maxlength="2" value = '+ nextval +' onkeypress="return /[0-9]/i.test(event.key)" name="sequence" style="text-transform:uppercase;" required></td><td><input class="form-control" type="text" maxlength="100000000" onkeypress="return /[0-9]/i.test(event.key)" name="starting" style="text-transform:uppercase;" required></td><td><input class="form-control" type="text" maxlength="100000000" onkeypress="return /[0-9]/i.test(event.key)" name="ending" style="text-transform:uppercase;" required></td><td><input class="form-control" type="text" maxlength="100000000" onkeypress="return /[0-9]/i.test(event.key)" name="current" style="text-transform:uppercase;" required></td>><td hidden><input class="form-control" type="text" value=""></td><td class="class_del_checkbox" hidden><input type="checkbox" required></td></tr>';
    $('#id_popup_tbody').append(basic_add_new_html);
    if (GLOBAL_ACTION == "number_range") {
        $(".class_del_checkbox").prop("hidden", false);
    }
    table_sort_filter('id_popup_table');
}

////onclick of delete,delete the row.
//function application_settings_delete_Row(myTable) {
//    $('#id_popup_table').DataTable().destroy();
//    try {
//        var table = document.getElementById(myTable);
//        var rowCount = table.rows.length;
//
//        for (var i = 0; i < rowCount; i++) {
//            var row = table.rows[i];
//            var chkbox = row.cells[0].childNodes[0];
//            if (null != chkbox && true == chkbox.checked) {
//                table.deleteRow(i);
//                rowCount--;
//                i--;
//            }
//        }
//
//        $("#id_delete_number_range").hide();
//        $("#id_copy_number_range").hide();
//        $("#id_update_number_range").hide();
//        table_sort_filter_popup_pagination('id_popup_table');
//        return rowCount;
//    } catch (e) {
//        alert(e);
//    }
//}


//onclick of cancel display the table in display mode............
function display_basic_db_data() {
    $('#display_basic_table').DataTable().destroy();
    $('#id_number_range_tbody').empty();
    var edit_basic_data = '';
    $.each(rendered_number_range_data, function (i, item) {
        edit_basic_data += '<tr ><td class="class_select_checkbox"><input class="checkbox_check" onclick="valueChanged()" type="checkbox" required></td><td>' + item.sequence + '</td><td>' + item.starting + '</td><td>' + item.ending + '</td><td>' + item.current + '</td><td hidden>' + item.guid + '</td></tr>';
    });
    $('#id_number_range_tbody').append(edit_basic_data);
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
$('#save_id').click(function () {
    $('#myModal').modal('hide');
     numberranges_data = new Array();
     validate_add_attributes = [];
    $("#id_popup_table TBODY TR").each(function () {
            var row = $(this);
            number_range={};

            number_range.del_ind = row.find("TD").eq(6).find('input[type="checkbox"]').is(':checked');
            number_range.sequence = row.find("TD").eq(1).find('input[type="text"]').val();
            number_range.starting = row.find("TD").eq(2).find('input[type="text"]').val().toUpperCase();
            number_range.ending = row.find("TD").eq(3).find('input[type="text"]').val().toUpperCase();
            number_range.current= row.find("TD").eq(4).find('input[type="text"]').val().toUpperCase();
            number_range.document_type = "DOC02"
            number_range.guid = row.find("TD").eq(5).find('input[type="text"]').val();
            if (number_range == undefined){
                number_range.sequence = row.find("TD").eq(1).find('input[type="text"]').val();
             }
             if(number_range.guid == undefined) {
                   number_range.guid = ''
             }
            validate_add_attributes.push(number_range.sequence);
          numberranges_data.push(number_range);
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