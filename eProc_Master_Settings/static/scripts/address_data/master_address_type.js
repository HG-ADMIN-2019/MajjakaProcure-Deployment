
var addresstype_data = new Array();
var validate_add_attributes = [];
var duplicate_entry = [];
var addresstype={};


//onclick of add button display myModal popup and set GLOBAL_ACTION button value
function onclick_add_button(button) {
    dropdown_value();
    $("#error_msg_id").css("display", "none")
    $( "#header_select").prop( "hidden", false );
    GLOBAL_ACTION = button.value
    $('#id_popup_table').DataTable().destroy();
    $("#id_popup_tbody").empty();
    $('#myModal').modal('show');
   basic_add_new_html = '<tr><td><input type="checkbox" required></td>' +
        '<td><select class="form-control">'+address_number_dropdwn+'</select></td>' +
        '<td><select class="form-control">'+address_type_dropdown+'</select></td>' +
        '<td><select class="form-control">'+company_dropdwn+'</select></td>' +
        '<td><input  type="date" name = "valid_from" class="form-control"></td>' +
        '<td><input type="date" name = "valid_to"  class="form-control"></td>' +
        '<td class="class_del_checkbox" hidden><input type="checkbox" required></td>' +
        '<td hidden><input  type="text" class="form-control"  name="guid"></td></tr>';
    $('#id_popup_tbody').append(basic_add_new_html);
    table_sort_filter('id_popup_table');
    $("#id_del_ind_checkbox").prop("hidden", true);
    document.getElementById("id_del_add_button").style.display = "block";
    $("#save_id").prop("hidden", false);
}

//onclick of upload button display id_data_upload popup and set GLOBAL_ACTION button value
function onclick_upload_button() {
    GLOBAL_ACTION = "addresstype_upload"
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
    $('#display_basic_table').DataTable().destroy();
    $("#id_popup_tbody").empty();
    $('#display_basic_table').DataTable().destroy();
    //Reference the Table.
    var grid = document.getElementById("display_basic_table");

    //Reference the CheckBoxes in Table.
    var checkBoxes = grid.getElementsByTagName("INPUT");
    var edit_basic_data = "";
    var unique_input = '';
    var address_guid= '';
    var dropdown_array = [];

    //Loop through the CheckBoxes.
    for (var i = 1; i < checkBoxes.length; i++) {
        if (checkBoxes[i].checked) {
            var row = checkBoxes[i].parentNode.parentNode;
             if(GLOBAL_ACTION == "UPDATE"){
                address_guid = 'GUID';
               unique_input = '<select class="form-control" value="' + row.cells[1].innerHTML + '">'+address_number_dropdwn+'</select>'
                edit_basic_data += '<tr><td><input type="checkbox" required></td>' +
                '<td>'+unique_input+'</td>' +
                '<td><select class="form-control" value="' + row.cells[2].innerHTML + '">'+address_type_dropdown_onload+'</select></td>' +
                '<td><select class="form-control" value="' + row.cells[3].innerHTML + '">'+company_dropdwn+'</select></td>'+
                '<td><input  type="date" name = "valid_from" value="' + row.cells[4].innerHTML + '"class="form-control"></td>'
                '<td><input  type="date" name = "valid_to" value="' + row.cells[5].innerHTML + '"class="form-control"></td>'
                '<td class="class_del_checkbox" hidden><input type="checkbox" required></td>' +
                '<td hidden><input  type="text" class="form-control"  value="' + row.cells[5].innerHTML + '"  name="guid"></td></tr>';
                $("#header_select").prop("hidden", true);
            }
            else{
                address_guid = 'GUID';
                unique_input = '<select class="form-control" value="' + row.cells[1].innerHTML + '">'+address_number_dropdwn+'</select>'
                edit_basic_data += '<tr><td><input type="checkbox" required></td>' +
                '<td>'+unique_input+'</td>' +
                '<td><select class="form-control" value="' + row.cells[2].innerHTML + '">'+address_type_dropdown_onload+'</select></td>' +
                '<td><select class="form-control" value="' + row.cells[3].innerHTML + '">'+company_dropdwn+'</select></td>' +
                 '<td><input  type="date" name = "valid_from" value="' + row.cells[4].innerHTML + '"class="form-control"></td>'
                '<td><input  type="date" name = "valid_to" value="' + row.cells[5].innerHTML + '"class="form-control"></td>'
                '<td class="class_del_checkbox" hidden><input type="checkbox" required></td>' +
                '<td hidden><input  type="text" class="form-control"  value="' + row.cells[5].innerHTML + '"  name="guid"></td></tr>';
                 $("#header_select").prop("hidden", false);
            }

            var address_number = row.cells[1].innerHTML
            var address_type = row.cells[2].innerHTML
            var company_id = row.cells[3].innerHTML

            dropdown_array.push([address_number, address_type, company_id])

        }
    }
     $('#id_popup_table').append(edit_basic_data);
     var i = 0;
    $("#id_popup_table TBODY TR").each(function () {
        var row = $(this);
        var address_number = dropdown_array[i][0]
        var address_type = dropdown_array[i][1]
        var company_id = dropdown_array[i][2]

        $(row.find("TD").eq(1).find("select option[value=" + address_number + "]")).attr('selected', 'selected');
        $(row.find("TD").eq(2).find("select option[value=" + address_type + "]")).attr('selected', 'selected');
        $(row.find("TD").eq(3).find("select option[value=" + company_id + "]")).attr('selected', 'selected');

        $(row.find("TD").eq(1).find("select")).change(function () {
            row.find("TD").eq(2).find("select").empty()
            row.find("TD").eq(3).find("select").empty()

        })
        i = i + 1;
    })

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
    $("#id_error_msg_address_type").prop("hidden", true);
    $("#id_error_msg_description").prop("hidden", true);
    $("#id_error_msg_description_length").prop("hidden", true);
    $("#id_check_error_messages").prop("hidden", true);
    $("#id_check_success_messages").prop("hidden", true);
    $("#id_check_special_character_messages").prop("hidden", true)
    $("#id_check_data").prop("hidden", true);
    $('#id_popup_table').DataTable().destroy();


});


function display_error_message(error_message){

    $('#error_message').text(error_message);
 
    document.getElementById("error_message").style.color = "Red";
    $("#error_msg_id").css("display", "block")
    $('#id_save_confirm_popup').modal('hide');
    $('#myModal').modal('show');

}

// on click add icon display the row in to add the new entries
function add_popup_row() {
    $("#error_msg_id").css("display", "none")
    basic_add_new_html = '';
    var display_db_data = '';
    $('#id_popup_table').DataTable().destroy();
    $(".modal").on("hidden.bs.modal", function () {
        $("#id_error_msg").html("");
    });
 basic_add_new_html = '<tr><td><input type="checkbox" required></td>' +
        '<td><select class="form-control">'+address_number_dropdwn+'</select></td>' +
        '<td><select class="form-control">'+address_type_dropdown+'</select></td>' +
        '<td><select class="form-control">'+company_dropdwn+'</select></td>' +
        '<td><input  type="date" name = "valid_from" class="form-control"></td>' +
        '<td><input type="date" name = "valid_to"  class="form-control"></td>' +
        '<td class="class_del_checkbox" hidden><input type="checkbox" required></td>' +
        '<td hidden><input  type="text" class="form-control"  name="guid"></td></tr>';
    $('#id_popup_tbody').append(basic_add_new_html);
    if (GLOBAL_ACTION == "addresstype_upload") {
        $(".class_del_checkbox").prop("hidden", false);
    }
    table_sort_filter_popup_pagination('id_popup_table');
}

//***********************************
//onclick of cancel display the table in display mode............
function display_basic_db_data() {
    $('#display_basic_table').DataTable().destroy();
    $('#id_address_type_tbody').empty();
    var edit_basic_data = '';
    $.each(rendered_address_type_data, function (i, item) {
        edit_basic_data += '<tr><td class="class_select_checkbox"><input class="checkbox_check" onclick="valueChanged()" type="checkbox" required></td>' +
            '<td>' + item.address_number + '</td>' +
            '<td>' + item.address_type + '</td>' +
            '<td>'+ item.company_id +'</td>'+
            '<td>'+ item.valid_from +'</td>'+
            '<td>'+ item.valid_to +'</td>'+
            '<td hidden> <input type="checkbox"></td>' +
            '<td hidden>' + item.address_guid + '</td></tr>';
    });
    $('#id_address_type_tbody').append(edit_basic_data);
    $("#hg_select_checkbox").prop("hidden", true);
    $(".class_select_checkbox").prop("hidden", true);
    $('input:checkbox').removeAttr('checked');
    $('#id_edit_data').show();
    $('#id_cancel_data').hide();
    $('#id_delete_data').hide();
    $('#id_copy_data').hide();
    $('#id_update_data').hide();
    $('#id_save_confirm_popup').hide();
    $('#id_delete_confirm_popup').hide();
    $('#id_check_all').hide();
    table_sort_filter('display_basic_table');
}
    //***************************

    // Functtion to hide and display save related popups
$('#save_id').click(function () {
    $('#myModal').modal('hide');

    validate_add_attributes = [];
   $("#id_popup_table TBODY TR").each(function () {
           var row = $(this);
          addresstype={};
          addresstype.del_ind = row.find("TD").eq(4).find('input[type="checkbox"]').is(':checked');
          addresstype.address_guid = row.find("TD").eq(5).find('input').val();
          addresstype.address_number = row.find("TD").eq(1).find('select').val();
          addresstype.address_type = row.find("TD").eq(2).find('select').val();
           addresstype.company_id = row.find("TD").eq(3).find('select').val();
           addresstype.valid_from = row.find("TD").eq(3).find('input').val();
           addresstype.valid_to = row.find("TD").eq(3).find('input').val();
           if (addresstype == undefined){
            addresstype.address_number = row.find("TD").eq(2).find('input').val();
            }
            if(addresstype.address_guid == undefined) {
                addresstype.address_guid = ''
            }
            var attribute_dup = {};
            attribute_dup.address_number = addresstype.address_number;
            attribute_dup.address_type = addresstype.address_type;
            duplicate_entry.push(attribute_dup);

           validate_add_attributes.push(addresstype.address_number);
           addresstype_data.push(addresstype);
       });
    $('#id_save_confirm_popup').modal('show');
});

