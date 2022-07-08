var wfacc_data = new Array();
var validate_add_attributes = [];
var wfacc = {};

//onclick of upload button display id_data_upload popup and set GLOBAL_ACTION button value
function onclick_upload_button() {
    GLOBAL_ACTION = "workflowacc_upload"
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

function display_error_message(error_message){

        $('#error_message').text(error_message);

        document.getElementById("error_message").style.color = "Red";
        $("#error_msg_id").css("display", "block");
        $('#id_save_confirm_popup').modal('hide');
        $('#myModal').modal('show');
}


//onclick of cancel empty the popup table body and error messages
$(".remove_upload_data").click(() => {
    $("#id_error_msg").html("");
    $("#id_popup_tbody").empty();
    $("#id_error_msg").empty();
    $('#myModal').modal('hide');
    $("#id_error_msg").prop("hidden", true);
    $("#id_error_msg_wfacc").prop("hidden", true);
   // $("#id_error_msg_approval_type_name").prop("hidden", true);
    //$("#id_error_msg_approval_type_length").prop("hidden", true);
    $("#id_check_error_messages").prop("hidden", true);
    $("#id_check_success_messages").prop("hidden", true);
    $("#id_check_special_character_messages").prop("hidden", true)
    $("#id_check_data").prop("hidden", true);
    $('#id_popup_table').DataTable().destroy();

});


// Functtion to hide and display save related popups
$('#save_id').click(function () {
    $('#myModal').modal('hide');
    wfacc_data = new Array();
    validate_add_attributes = [];
            var wfacc = {};
            $("#id_popup_table TBODY TR").each(function() {
                var row = $(this);
                wfacc = {};
                wfacc.del_ind = row.find("TD").eq(0).find('input[type="checkbox"]').is(':checked');
                wfacc.app_username = row.find("TD").eq(1).find('select[type="text"]').val();
                wfacc.acc_value = row.find("TD").eq(3).find('input[type="text"]').val();
                wfacc.sup_acc_value = row.find("TD").eq(6).find('input[type="text"]').val();
                wfacc.account_assign_cat = row.find("TD").eq(2).find('select[type="text"]').val();
                wfacc.sup_account_assign_cat = row.find("TD").eq(5).find('select[type="text"]').val();
                wfacc.company_id = row.find("TD").eq(4).find('select[type="text"]').val();
                wfacc.sup_company_id = row.find("TD").eq(7).find('select[type="text"]').val();
                wfacc.sup_currency_id = row.find("TD").eq(8).find('select[type="text"]').val();
                wfacc.workflow_acc_guid = row.find("TD").eq(10).find('input[type="text"]').val();
                if (wfacc == undefined) {
                    wfacc.app_username = row.find("TD").eq(1).find('select[type="text"]').val();
                }
                if(wfacc.workflow_acc_guid == undefined) {
                   wfacc.workflow_acc_guid = ''
                }
                validate_add_attributes.push(wfacc.acc_value);
                wfacc_data.push(wfacc);
            });
    $('#id_save_confirm_popup').modal('show');
});