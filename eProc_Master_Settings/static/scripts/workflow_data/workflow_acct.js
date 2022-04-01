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

//validate by comparing  main table values and popup table values
function maintable_validation(wfacc_data, main_table_low_value) {
    var no_duplicate_entries = 'Y'
    var error_message =''

    var dup_entry = "";

     $.each(wfacc_data, function (i, item) {
        $.each(main_table_low_value, function (j, item1) {
            if((item.app_username == item1.app_username) && (item.account_assign_cat == item1.account_assign_cat) &&
            (item.acc_value == item1.acc_value) && (item.company_id == item1.company_id) && (item.sup_account_assign_cat == item1.sup_account_assign_cat) && (item.sup_acc_value == item1.sup_acc_value)
            && (item.sup_company_id == item1.sup_company_id) && (item.sup_currency_id == item1.sup_currency_id) ){
                dup_entry = "1"
            }
        });
     });
         if((dup_entry == "1"))
        {
        error_message = messageConstants["JMSG001"]
        no_duplicate_entries = 'N'
        }
    return [no_duplicate_entries,error_message]

}

// validating the  popup table for duplicate entries
function compare_table_for_duplicate_entries(validate_add_attributes, wfacc) {
    add_attr_duplicates = false;
    var error_message = ''
    var add_attr_duplicates_list = [];
    var add_attr_unique_list = [];
    var no_duplicate_value = 'Y'
    $.each(validate_add_attributes, function (index, value) {
        if ($.inArray(value, add_attr_unique_list) == -1) {
            add_attr_unique_list.push(value);
        }
        else {
            if ($.inArray(value, add_attr_duplicates_list) == -1) {
                add_attr_duplicates_list.push(value);
            }
        }
    });
    if (add_attr_duplicates_list.length != 0) {

        error_message = messageConstants["JMSG001"];
        no_duplicate_value = 'N'
   }
    else {
         $.each(wfacc, function (i, item) {
            if (item.acc_value.length == 0) {
                error_message = messageConstants["JMSG002"] + " Account Assignment Value";
        no_duplicate_value = 'N'
        return [no_duplicate_value,error_message]
        }
         if (item.sup_acc_value.length == 0) {
                error_message = messageConstants["JMSG002"] + " Superior Account Assignment Value";
                no_duplicate_value = 'N'
                return [no_duplicate_value,error_message]
            }
         if((item.acc_value==item.sup_acc_value) && (item.account_assign_cat == item.sup_account_assign_cat)){
          error_message = " Superior Account Assignment Value and Account Assignment Value cant be same";
                no_duplicate_value = 'N'
                return [no_duplicate_value,error_message]
         }
         });
    }
    return [no_duplicate_value,error_message]
}


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