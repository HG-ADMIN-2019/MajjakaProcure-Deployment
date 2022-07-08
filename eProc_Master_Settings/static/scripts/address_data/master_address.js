
var address_data = new Array();
var validate_add_attributes = [];
var address={};
// on click copy icon display the selected checkbox data

function onclick_upload_button() {
    GLOBAL_ACTION = "addresstype_upload"
    $("#id_popup_tbody").empty();
    $('#id_data_upload').modal('show');
    document.getElementById('id_file_data_upload').value = "";
}
//onclick of cancel empty the popup table body and error messages
$(".remove_upload_data").click(() => {
    $("#id_error_msg").html("");
    $("#id_popup_tbody").empty();
    $("#id_error_msg").empty();
    $('#myModal').modal('hide');
    $("#id_error_msg").prop("hidden", true);
    $("#id_error_msg_address").prop("hidden", true);
    $("#id_error_msg_description").prop("hidden", true);
    $("#id_error_msg_description_length").prop("hidden", true);
    $("#id_check_error_messages").prop("hidden", true);
    $("#id_check_success_messages").prop("hidden", true);
    $("#id_check_special_character_messages").prop("hidden", true)
    $("#id_check_data").prop("hidden", true);
    $('#id_popup_table').DataTable().destroy();
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

 //onclick of cancel display the table in display mode............
 function display_basic_db_data() {
    console.log("test");
    $('#display_basic_table').DataTable().destroy();

    $('#id_address_tbody').empty();
    var edit_basic_data = '';
    var cntry_name = '';
    var lang = '';
    var time = '';
    //console.log(rendered_address_data);
    $.each(rendered_address_data, function (i, item) {
           for (i = 0; i < render_country_data.length; i++) {
                if (item.country_code == render_country_data[i].country_code)
                    cntry_name = render_country_data[i].country_name;
            }
              for (i = 0; i < render_language_data.length; i++) {
                if (item.language_id == render_language_data[i].language_id)
                    lang = render_language_data[i].description;
            }
             for (i = 0; i < render_timezone_data.length; i++) {
                if (item.time_zone == render_timezone_data[i].time_zone)
                    time = render_timezone_data[i].description;
            }
        edit_basic_data += '<tr><td class="class_select_checkbox"><input class="checkbox_check" onclick="valueChanged()" type="checkbox" required></td>' +
            '<td>' + item.address_number + '</td>' +
            '<td>' + item.title + '</td>' +
            '<td>' + item.name1 + '</td>' +
            '<td>' + item.name2 + '</td>' +
            '<td>' + item.street + '</td>' +
            '<td>' + item.area + '</td>' +
            '<td>' + item.landmark + '</td>' +
            '<td>' + item.city + '</td>' +
            '<td>' + item.postal_code + '</td>' +
            '<td>' + item.region + '</td>' +
            '<td>' + item.mobile_number + '</td>' +
            '<td>' + item.telephone_number + '</td>' +
            '<td>' + item.fax_number + '</td>' +
            '<td>' + item.email + '</td>' +
            '<td>' + cntry_name + '</td>' +
            '<td>' + lang + '</td>' +
            '<td>' + time + '</td>' +
            '<td hidden> <input type="checkbox"></td>' +
            '<td hidden>' + item.address_guid + '</td></tr>';
    });
    $('#id_address_tbody').append(edit_basic_data);
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
function display_error_message(error_message){

        $('#error_message').text(error_message);
        //$("p").css("color", "red");
        //document.getElementById("error_message").innerHTML = error_message;
        document.getElementById("error_message").style.color = "Red";
        $("#error_msg_id").css("display", "block")
        $('#id_save_confirm_popup').modal('hide');
        $('#myModal').modal('show');
         }

///////////
$('#save_id').click(function () {
    $('#myModal').modal('hide');
    validate_add_attributes = [];

     $("#id_popup_table TBODY TR").each(function () {
            var row = $(this);
            address = {};
            address.address_number = row.find("TD").eq(1).find('input[type="text"]').val();
            address.title = row.find("TD").eq(2).find('input[type="text"]').val();
            address.name1 = row.find("TD").eq(3).find('input[type="text"]').val();
            address.name2 = row.find("TD").eq(4).find('input[type="text"]').val();
            address.street = row.find("TD").eq(5).find('input[type="text"]').val();
            address.area = row.find("TD").eq(6).find('input[type="text"]').val();
            address.landmark = row.find("TD").eq(7).find('input[type="text"]').val();
            address.city = row.find("TD").eq(8).find('input[type="text"]').val();
            address.postal_code = row.find("TD").eq(9).find('input[type="text"]').val();
            address.region = row.find("TD").eq(10).find('input[type="text"]').val();
            address.mobile_number = row.find("TD").eq(11).find('input[type="text"]').val();
            address.telephone_number = row.find("TD").eq(12).find('input[type="text"]').val();
            address.fax_number = row.find("TD").eq(13).find('input[type="text"]').val();
            address.email = row.find("TD").eq(14).find('input[type="text"]').val();
            address.country_code = row.find("TD").eq(15).find('select[type="text"]').val();
            address.language_id = row.find("TD").eq(16).find('select[type="text"]').val();
            address.time_zone = row.find("TD").eq(17).find('select[type="text"]').val();
            address.del_ind = row.find("TD").eq(18).find('input[type="checkbox"]').is(':checked');
            address.address_guid = row.find("TD").eq(19).find('input[type="text"]').val();
            console.log(address.address_guid)

            if (address == undefined) {
                address.address_number = row.find("TD").eq(1).find('input[type="text"]').val();
            }
            if(address.address_guid== undefined) {
                   address.address_guid= ''
             }
            validate_add_attributes.push(address.address_number);
            address_data.push(address);
               });
    $('#id_save_confirm_popup').modal('show');
        });