var accasscat_data = new Array();
var validate_add_attributes = [];
var aac={};


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


//onclick of cancel empty the popup table body and error messages
$(".remove_upload_data").click(() => {
    $("#id_error_msg").html("");
    $("#id_popup_tbody").empty();
    $("#id_error_msg").empty();
    $('#myModal').modal('hide');
    $("#id_error_msg").prop("hidden", true);
    $("#id_error_msg_aac_code").prop("hidden", true);
    $("#id_error_msg_aac_name").prop("hidden", true);
    $("#id_error_msg_aac_length").prop("hidden", true);
    $("#id_check_error_messages").prop("hidden", true);
    $("#id_check_success_messages").prop("hidden", true);
    $("#id_check_special_character_messages").prop("hidden", true)
    $("#id_check_data").prop("hidden", true);
    $('#id_popup_table').DataTable().destroy();

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

//onclick of cancel display the table in display mode............
function display_basic_db_data() {
    $('#display_basic_table').DataTable().destroy();
    $('#id_aac_tbody').empty();
    var edit_basic_data = '';
    $.each(rendered_aac_data, function (i, item) {
        edit_basic_data += '<tr ><td class="class_select_checkbox"><input class="checkbox_check" onclick="valueChanged()" type="checkbox" required></td><td>' + item.account_assign_cat + '</td><td>' + item.description + '</td></tr>';
    });
    $('#id_aac_tbody').append(edit_basic_data);
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

// Function to delete duplicates
function delete_duplicate() {
    $('#id_popup_table').DataTable().destroy();
    var aac_code_check = new Array
    $("#id_popup_table TBODY TR").each(function() {
        var row = $(this);

        //*************** reading data from the pop-up ***************
        description = row.find("TD").eq(2).find('input[type="text"]').val().toUpperCase();
        account_assign_cat = row.find("TD").eq(1).find('input[type="text"]').val().toUpperCase();
        checked_box = row.find("TD").eq(3).find('input[type="checkbox"]').is(':checked')


        if (aac_code_check.includes(account_assign_cat)) {
            $(row).remove();
        }

        aac_code_check.push(account_assign_cat);


    })
    table_sort_filter('id_popup_table')
    check_data()
}
$('#save_id').click(function () {
    $('#myModal').modal('hide');
     accasscat_data = new Array();
     validate_add_attributes = [];
            aac = {};
            $("#id_popup_table TBODY TR").each(function() {
                var row = $(this);
                aac = {};
                aac.del_ind = row.find("TD").eq(3).find('input[type="checkbox"]').is(':checked');
                aac.description = row.find("TD").eq(2).find('input[type="text"]').val().toUpperCase();
                aac.account_assign_cat = row.find("TD").eq(1).find('select[type="text"]').val();
                if (aac == undefined) {
                    aac.account_assign_cat= row.find("TD").eq(1).find('select[type="text"]').val();
                }
                validate_add_attributes.push(aac.account_assign_cat);
                accasscat_data.push(aac);
            });
    $('#id_save_confirm_popup').modal('show');

});