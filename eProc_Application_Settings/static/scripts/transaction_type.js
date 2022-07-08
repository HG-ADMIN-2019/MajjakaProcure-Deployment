var transaction_types_data = new Array();
var validate_add_attributes = [];
var TransactionTypes={};


//onclick of add button display myModal popup and set GLOBAL_ACTION button value
function onclick_add_button(button) {
     dropdown_value();
    $("#error_msg_id").css("display", "none")
    $( "#header_select").prop( "hidden", false );
    GLOBAL_ACTION = button.value
    $('#id_popup_table').DataTable().destroy();
    $('#myModal').modal('show');
    $("#id_popup_tbody").empty();
    $('#myModal').modal('show');
    eliminate_used_sequence()
    basic_add_new_html = '<tr><td><input type="checkbox" required></td><td><input class="input form-control" type="text" maxlength="15" onkeypress="return /[A-Z0-9 ]/i.test(event.key)" name="transaction type" style="text-transform:uppercase;" required></td><td><input type="text" class="form-control" maxlength="10" onkeypress="return /[a-z0-9 ]/i.test(event.key)" name="transaction description"  required></td><td><select class="input form-control" disabled>'+ document_type_dropdown +'</select></td><td><select class="input form-control">' + sequence_dropdown + '</select></td><td><input type="checkbox"  name="active_inactive" required></td><td hidden><input type="text" class= "form-control" name=" guid "></td><td hidden><input type="checkbox" required></td></tr>';
    $('#id_popup_tbody').append(basic_add_new_html);
    table_sort_filter('id_popup_table');
    $("#id_del_ind_checkbox").prop("hidden", true);
    document.getElementById("id_del_add_button").style.display = "block";
    $("#save_id").prop("hidden", false);
}

// on click add icon display the row in to add the new entries
function add_popup_row() {
    dropdown_value();
    $("#error_msg_id").css("display", "none")
    basic_add_new_html = '';
    var display_db_data = '';
    $('#id_popup_table').DataTable().destroy();
    $(".modal").on("hidden.bs.modal", function () {
        $("#id_error_msg").html("");
    });
    eliminate_used_sequence()
    basic_add_new_html = '<tr><td><input type="checkbox" required></td><td><input class="input form-control" type="text" maxlength="15" onkeypress="return /[A-Z0-9 ]/i.test(event.key)" name="transaction type" style="text-transform:uppercase;" required></td><td><input type="text" class="form-control" maxlength="10" onkeypress="return /[a-z0-9 ]/i.test(event.key)" name="transaction description"  required></td><td><select class="input form-control" disabled>'+ document_type_dropdown +'</select></td><td><select class="input form-control">' + sequence_dropdown + '</select></td><td><input type="checkbox"  name="active_inactive" required></td><td hidden><input type="text" class= "form-control" name=" guid "></td><td hidden><input type="checkbox" required></td></tr>';

    $('#id_popup_tbody').append(basic_add_new_html);

    if (GLOBAL_ACTION == "transaction_types_upload") {
        $(".class_del_checkbox").prop("hidden", false);
    }
    table_sort_filter_popup('id_popup_table');
}



//**********************************
function read_sequence() {
    rendered_sequence_array = [];
    sequence_remove_array = [];
    $.each(rendered_transaction_types_data, function (i, value) {
        sequence_remove_array.push(value.sequence)
    });

    $.each(rendered_sequence, function (i, item) {
        rendered_sequence_array.push(item.sequence)
    });
    console.log(rendered_sequence_array);
}

//*************************************


read_sequence()
function eliminate_used_sequence() {
    sequence_dropdown = '';


    $.each(rendered_sequence_array, function (i, item) {
        if (sequence_remove_array.includes(item)) {
            rendered_sequence_array = $.grep(rendered_sequence_array, function (value) {
                return value != item;
            });
        }
    });

    $("#id_popup_table TBODY TR").each(function () {
        var row = $(this);
        sequence_popup = row.find("TD").eq(4).find("select option:selected").val();
        rendered_sequence_array = $.grep(rendered_sequence_array, function (item) {
            return item != sequence_popup;
        });

    })
    console.log("rendered_sequence_array",rendered_sequence_array);
    $.each(rendered_sequence_array, function (i, value) {
        sequence_dropdown += '<option value="' + value + '">' + value + '</option>'

    });
    console.log("sequence_dropdown",sequence_dropdown)


}

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
     $('#display_basic_table').DataTable().destroy();
    $("#id_popup_tbody").empty();
    $('#display_basic_table').DataTable().destroy();
    //Reference the Table.
    var grid = document.getElementById("display_basic_table");

    //Reference the CheckBoxes in Table.
    var checkBoxes = document.getElementsByClassName("checkbox_check");
    var edit_basic_data = "";
    var dropdown_val = [];
    //Loop through the CheckBoxes.
    for (var i = 0; i < checkBoxes.length; i++) {
        if (checkBoxes[i].checked) {
            var row = checkBoxes[i].parentNode.parentNode;
            var document_type = row.cells[3].innerHTML
            var sequence = row.cells[4].innerHTML
            var active_inactive = row.cells[5].children.active_inactive.checked
            dropdown_val.push([document_type, sequence, active_inactive])

            sequence_remove_array = $.grep(sequence_remove_array, function (value) {
                return value != sequence;
            });
            rendered_sequence_array.push(sequence)


            guid = ''
            if (GLOBAL_ACTION == "UPDATE") {
                guid = row.cells[6].innerHTML

            eliminate_used_sequence()
            edit_basic_data += '<tr ><td><input type="checkbox" required></td><td><input class="input form-control" type="text" maxlength="15" value="' + row.cells[1].innerHTML + '" onkeypress="return /[a-z0-9 ]/i.test(event.key)" name="transaction type" style="text-transform:uppercase;" disabled></td><td><input type="text" class= "form-control" maxlength="100" value="' + row.cells[2].innerHTML + '" onkeypress="return /[a-z0-9 ]/i.test(event.key)" name="transaction description"  required></td><td><select class="input form-control" disabled>' + document_type_dropdown + '</select></td><td><select class="input form-control" disabled>' + sequence_dropdown + '</select></td><td><input type="checkbox"  name="active_inactive" required></td><td hidden><input type="text" class= "form-control" value="' + guid + '"></td><td hidden><input type="checkbox" required></td></tr>';
            }
            else{
            eliminate_used_sequence()
            edit_basic_data += '<tr ><td><input type="checkbox" required></td><td><input class="input form-control" type="text" maxlength="15" value="' + row.cells[1].innerHTML + '" onkeypress="return /[a-z0-9 ]/i.test(event.key)" name="transaction type" style="text-transform:uppercase;"></td><td><input type="text" class= "form-control" maxlength="100" value="' + row.cells[2].innerHTML + '" onkeypress="return /[a-z0-9 ]/i.test(event.key)" name="transaction description"  required></td><td><select class="input form-control" disabled>' + document_type_dropdown + '</select></td><td><select class="input form-control">' + sequence_dropdown + '</select></td><td><input type="checkbox"  name="active_inactive" required></td><td hidden><input type="text" class= "form-control" value="' + guid + '"></td><td hidden><input type="checkbox" required></td></tr>';
            }

        }
    }
    $('#id_popup_table').append(edit_basic_data);
    var i = 0;
    $("#id_popup_table TBODY TR").each(function () {
        var row = $(this);
        var document_type = dropdown_val[i][0]
        var sequence = dropdown_val[i][1]
        var active_inactive = dropdown_val[i][2]

        $(row.find("TD").eq(1).find("select option[value=" + document_type + "]")).attr('selected', 'selected');
        $(row.find("TD").eq(4).find("select option[value=" + sequence + "]")).attr('selected', 'selected');
        if(active_inactive) {
            $(row.find("TD").eq(5).find('input[name="active_inactive"]').attr('checked', 'checked'));
        }
       
        i++;
    })
    $("#id_del_ind_checkbox").prop("hidden", true);
    $('#myModal').modal('show');
    table_sort_filter('display_basic_table');
    table_sort_filter('id_popup_table');
}
//********************************************************

//onclick of cancel empty the popup table body and error messages
$(".remove_upload_data").click(() => {
    $("#id_error_msg").html("");
    $("#id_popup_tbody").empty();
    $("#id_error_msg").empty();
    $('#myModal').modal('hide');
    $("#id_error_msg").prop("hidden", true);
    $("#id_error_msg_transaction_types_code").prop("hidden", true);
    $("#id_error_msg_transaction_types_name").prop("hidden", true);
    $("#id_error_msg_transaction_types_length").prop("hidden", true);
    $("#id_check_error_messages").prop("hidden", true);
    $("#id_check_success_messages").prop("hidden", true);
    $("#id_check_special_character_messages").prop("hidden", true)
    $("#id_check_data").prop("hidden", true);
    sequence_dropdown = '';
    read_sequence()
    $('#id_popup_table').DataTable().destroy();


});



function display_error_message(error_message){

    $('#error_message').text(error_message);
   
    document.getElementById("error_message").style.color = "Red";
    $("#error_msg_id").css("display", "block")
    $('#id_save_confirm_popup').modal('hide');
    $('#myModal').modal('show');

}
//******************************************************

function delete_duplicate() {
    $('#id_popup_table').DataTable().destroy();
    var transaction_types_code_check = new Array
    $("#id_popup_table TBODY TR").each(function () {
        var row = $(this);

        //*************** reading data from the pop-up ***************
        transaction_type = row.find("TD").eq(2).find('input[type="text"]').val().toUpperCase();


        if (transaction_types_code_check.includes(country_code)) {
            $(row).remove();
        }

        transaction_types_code_check.push(transaction_type);


    })
    table_sort_filter_popup_pagination('id_popup_table')
    check_data()
}


// Functtion to hide and display save related popups

$('#save_id').click(function () {
    transaction_types_data = new Array();
    validate_add_attributes = [];
    $('#myModal').modal('hide');
     $("#id_popup_table TBODY TR").each(function() {
        var row = $(this);
        transaction_types = {};
        transaction_types.del_ind = row.find("TD").eq(7).find('input[type="checkbox"]').is(':checked');
        transaction_types.document_type = row.find("TD").eq(3).find("select option:selected").val();
        transaction_types.transaction_type = row.find("TD").eq(1).find('input[type="text"]').val();
        transaction_types.description = row.find("TD").eq(2).find('input[type="text"]').val();
        transaction_types.sequence = row.find("TD").eq(4).find("select option:selected").val();
        transaction_types.active_inactive = row.find("TD").eq(5).find('input[type="checkbox"]').is(':checked');
        transaction_types.guid = row.find("TD").eq(6).find('input[type="text"]').val();
        transaction_types.attribute_id ='FC_TRANS_TYPE'

        if (transaction_types == undefined) {
            transaction_types.transaction_type = row.find("TD").eq(2).find('input[type="text"]').val().toUpperCase();
        }
        if (transaction_types.guid == undefined){
            transaction_types.guid = ''
        }


        validate_add_attributes.push(transaction_types.transaction_type);
        transaction_types_data.push(transaction_types);
    });
    
    $('#id_save_confirm_popup').modal('show');
});


