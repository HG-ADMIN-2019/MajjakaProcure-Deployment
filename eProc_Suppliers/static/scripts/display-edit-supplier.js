

var encrypted_supplier

// Global variable - supplier id
var global_supplier_id = document.getElementById('supplier_id').value

// Global variable - delete supplier purchasing info
var delete_supp_purch_data = []

// Global variable - supplier purchasing data
var supplier_org_data = new Array();
$("#supp_org_details_table TBODY TR").each(function() {
    var row = $(this);
    var save_supp_org_data = {};
    save_supp_org_data.supp_id = global_supplier_id;
    save_supp_org_data.supp_org_guid = row.find("TD").eq(0).text().trim();
    save_supp_org_data.porg_id = row.find("TD").eq(1).text().trim();
    save_supp_org_data.currency_id = row.find("TD").eq(2).text().trim();
    save_supp_org_data.payment_term = row.find("TD").eq(3).text().trim();
    save_supp_org_data.incoterm = row.find("TD").eq(4).text().trim();
    save_supp_org_data.gr_inv_vrf = row.find("TD").eq(5).find('input[type="checkbox"]').is(':checked');
    save_supp_org_data.inv_conf_exp = row.find("TD").eq(6).find('input[type="checkbox"]').is(':checked');
    save_supp_org_data.gr_conf_exp = row.find("TD").eq(7).find('input[type="checkbox"]').is(':checked');
    save_supp_org_data.po_resp = row.find("TD").eq(8).find('input[type="checkbox"]').is(':checked');
    save_supp_org_data.ship_notif_exp = row.find("TD").eq(9).find('input[type="checkbox"]').is(':checked');
    save_supp_org_data.purch_block = row.find("TD").eq(10).find('input[type="checkbox"]').is(':checked');
    supplier_org_data.push(save_supp_org_data)
    console.log(save_supp_org_data)
})


// Makes the supplier basic data fields editable
function edit_basic_supp_data(){
    $('#supplier_basic_update_success').hide();
    $(".hg_edit_display_mode").prop( "disabled", false );
    if(GLOBAL_ACTION != 'CREATE'){
            $("#supplier_id").prop( "disabled", true );
    }
    $("#currency_id").append(currency_opt)
    $("#country_code_id").append(country_opt)
    $("#language_id").append(language_opt)
    document.getElementById('sbd_edit_button').style.display = 'none'
    document.getElementById('sbd_save_cancel_button').style.display = 'block'
}

// onclick of cancel button functionality
function cancel_basic_details(){
    $(".hg_edit_display_mode").prop( "disabled", true );
    document.getElementById('sbd_save_cancel_button').style.display = 'none'
    document.getElementById('sbd_edit_button').style.display = 'block'
}

// Function to edit supplier purchasing details data
function edit_supp_org(){
    var supp_org_body_data = '';

    supp_org_header_data = '<tr> <th>Select</th> <th>Purchasing organisation</th> <th>PO Currency</th> <th>Payment Terms</th> <th>Incoterm</th> <th>GR based invoice verification</th> <th>Invoice confirmation expected</th> <th>GR confirmation expected</th> <th>PO response</th> <th>Shipping notification expected</th> <th>Purchase block</th></tr>'

    $.each(supplier_org_data, function (index, data) {

        var gr_inv_vrf_checkbox = ''
        if (data.gr_inv_vrf==true){
            gr_inv_vrf_checkbox += '<input type="checkbox"  checked>'
        } else gr_inv_vrf_checkbox += '<input type="checkbox">'

        var inv_conf_exp_checkbox = ''
        if(data.inv_conf_exp==true){
            inv_conf_exp_checkbox += '<input type="checkbox"  checked>'
        } else inv_conf_exp_checkbox += '<input type="checkbox">'

        var gr_conf_exp_checkbox = ''
        if(data.gr_conf_exp==true){
            gr_conf_exp_checkbox += '<input type="checkbox"  checked>'
        } else gr_conf_exp_checkbox += '<input type="checkbox">'

        var po_resp_checkbox = ''
        if(data.po_resp==true){
            po_resp_checkbox += '<input type="checkbox"  checked>'
        } else po_resp_checkbox += '<input type="checkbox">'

        var ship_notif_exp_checkbox = ''
        if(data.ship_notif_exp==true){
            ship_notif_exp_checkbox += '<input type="checkbox"  checked>'
        } else ship_notif_exp_checkbox += '<input type="checkbox">'

        var purch_block_checkbox = ''
        if(data.purch_block==true){
            purch_block_checkbox += '<input type="checkbox"  checked>'
        } else purch_block_checkbox += '<input type="checkbox">'

        supp_org_body_data += '<tr> <td><input name="supplier_checkbox" type="checkbox" id="'+data.supp_org_guid+'"></td> <td hidden>'+data.supp_org_guid+'</td> <td><select class="form-control"> <option selected="true" disabled="disabled">'+data.porg_id+'</option>'+porg_opt+'</select></td> <td><select class="form-control"> <option selected="true" disabled="disabled">'+data.currency_id+'</option>'+currency_opt+'</select></td> <td><select class="form-control"><option selected="true" disabled="disabled">'+data.payment_term+'</option>'+payterm_opt+'</select></td> <td><select class="form-control"><option selected="true" disabled="disabled">'+data.incoterm+'</option>'+incoterm_opt+'</select></td> <td>'+gr_inv_vrf_checkbox+'</td> <td>'+inv_conf_exp_checkbox+'</td> <td>'+gr_conf_exp_checkbox+'</td> <td>'+po_resp_checkbox+'</td> <td>'+ship_notif_exp_checkbox+'</td> <td>'+purch_block_checkbox+'</td></tr> '
    });

    $('#supp_org_header').empty();
    $('#supp_org_header').append(supp_org_header_data);
    $('#supp_org_body').empty();
    $('#supp_org_body').append(supp_org_body_data);
    document.getElementById("supp_org_edit").style.display = "none";
    document.getElementById("supp_org_add_delete_line").style.display = "block";
    document.getElementById("supp_org_cancel_save").style.display = "block";

}

// Function add a new row of supplier purchasing data
function supp_org_add_new_line(){
    add_new_supp_org_data = ''

    add_new_supp_org_data = '<tr> <td><input type="checkbox" name="supplier_checkbox"></td> <td hidden></td> <td><select class="form-control"><option selected="true" disabled="disabled"> Select </option>'+porg_opt+'</select></td> <td><select class="form-control"><option selected="true" disabled="disabled"> Select </option>'+currency_opt+'</select></td> <td><select class="form-control"><option selected="true" disabled="disabled"> Select </option>'+payterm_opt+'</select></td> <td><select class="form-control"><option selected="true" disabled="disabled"> Select </option>'+incoterm_opt+'</select></td> <td><input type="checkbox"></td> <td><input type="checkbox"></td> <td><input type="checkbox"></td> <td><input type="checkbox"></td> <td><input type="checkbox"></td> <td><input type="checkbox"></td> </tr>'
    $("#supp_org_body").append(add_new_supp_org_data);
}


// Function to cancel Edit operation
function cancel_supp_org_data(){
    display_supp_org_header = ''
    display_supp_org_body = ''
    $('#supp_org_header').empty();
    $('#supp_org_body').empty();

    display_supp_org_header = '<tr> <th>Purchasing organisation</th> <th>PO Currency</th> <th>Payment Terms</th> <th>Incoterm</th> <th>GR based invoice verification</th> <th>Invoice confirmation expected</th> <th>GR confirmation expected</th> <th>PO response</th> <th>Shipping notification expected</th> <th>Purchase block</th></tr>'

    $.each(supplier_org_data, function(index, data){

        var gr_inv_vrf_checkbox = ''
        if (data.gr_inv_vrf==true){
            gr_inv_vrf_checkbox += '<input type="checkbox" checked disabled>'
        } else gr_inv_vrf_checkbox += '<input type="checkbox" disabled>'

        var inv_conf_exp_checkbox = ''
        if(data.inv_conf_exp==true){
            inv_conf_exp_checkbox += '<input type="checkbox" checked disabled>'
        } else inv_conf_exp_checkbox += '<input type="checkbox" disabled>'

        var gr_conf_exp_checkbox = ''
        if(data.gr_conf_exp==true){
            gr_conf_exp_checkbox += '<input type="checkbox" checked disabled>'
        } else gr_conf_exp_checkbox += '<input type="checkbox" disabled>'

        var po_resp_checkbox = ''
        if(data.po_resp==true){
            po_resp_checkbox += '<input type="checkbox" checked disabled>'
        } else po_resp_checkbox += '<input type="checkbox" disabled>'

        var ship_notif_exp_checkbox = ''
        if(data.ship_notif_exp==true){
            ship_notif_exp_checkbox += '<input type="checkbox" checked disabled>'
        } else ship_notif_exp_checkbox += '<input type="checkbox">'

        var purch_block_checkbox = ''
        if(data.purch_block==true){
            purch_block_checkbox += '<input type="checkbox" checked disabled>'
        } else purch_block_checkbox += '<input type="checkbox" disabled>'

        display_supp_org_body += '<tr> <td hidden>'+data.supp_org_guid+'</td> <td>'+data.porg_id+'</td> <td>'+data.currency_id+'</td> <td>'+data.payment_term+'</td> <td>'+data.incoterm+'</td> <td>'+gr_inv_vrf_checkbox+'</td> <td>'+inv_conf_exp_checkbox+'</td> <td>'+gr_conf_exp_checkbox+'</td> <td>'+po_resp_checkbox+'</td> <td>'+ship_notif_exp_checkbox+'</td> <td>'+purch_block_checkbox+'</td></tr> '
    });

    $('#supp_org_header').append(display_supp_org_header);
    $('#supp_org_body').append(display_supp_org_body);
    document.getElementById("supp_org_edit").style.display = "block";
    document.getElementById("supp_org_add_delete_line").style.display = "none";
    document.getElementById("supp_org_cancel_save").style.display = "none";
}


// Function to delete row
function delete_supplier_purch_data() {
    delete_supp_purch_data = []
        del_seq = document.getElementsByName("supplier_checkbox")
        for (index = 0; index < del_seq.length; index++) {
            if (del_seq[index].checked) {
                delete_supp_purch_data.push(del_seq[index].id)
            }
        }
        application_settings_delete_Row('supp_org_details_table')
        console.log(delete_supp_purch_data)
}


// Function to delete rows from UI
function application_settings_delete_Row(myTable) {
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
        return rowCount;
    } catch (e) {
        alert(e);
    }
}

// Function to save edited supplier basic details data
function save_basic_details() {
    OpenLoaderPopup();
    var name1_val= $('#name1').val();
    var city_val = $('#city_id').val();
    var email_val = $('#email_id').val();
    is_save_form_valid = save_basic_form_validation(name1_val, city_val, email_val)
    if (is_save_form_valid != '') {
        $('#save_error_div').html(is_save_form_valid)
        $('#save_error_div').show()
        scroll_top()
        return
    }

    formdata = new FormData();
    formdata.append("supplier_image",  $('#supplier_image_id').prop('files')[0]);
    formdata.append("supplier_guid",   $('#supplier_guid').val());
    formdata.append("supplier_id",   $('#supplier_id').val());
    formdata.append("registration_number",   $('#supplier_regnum').val());
    formdata.append("name1",$('#name1').val());
    formdata.append("name2",$('#name2').val());
    formdata.append("city_id",   $('#city_id').val());
    formdata.append("postal_code_id",   $('#postal_code_id').val());
    formdata.append("street_id",   $('#street_id').val());
    formdata.append("country_code_id",   $('#country_code_id').val());
    formdata.append("currency_id",   $('#currency_id').val());
    formdata.append("language_id",   $('#language_id').val());
    formdata.append("landline_id",   $('#landline_id').val());
    formdata.append("mobile_num_id",   $('#mobile_num_id').val());
    formdata.append("fax_id",   $('#fax_id').val());
    formdata.append("email_id",   $('#email_id').val());
    formdata.append("search_term1_id",   $('#search_term1_id').val());
    formdata.append("search_term2_id",   $('#search_term2_id').val());
    formdata.append("working_days_id",   $('#working_days_id').val());
    formdata.append("duns_number_id",   $('#duns_number_id').val());
    formdata.append("email1_id",   $('#email1_id').val());
    formdata.append("email2_id",   $('#email2_id').val());
    formdata.append("email3_id",   $('#email3_id').val());
    formdata.append("email4_id",   $('#email4_id').val());
    formdata.append("email5_id",   $('#email5_id').val());
    formdata.append("output_medium_id",   $('#output_medium_id').val());
    formdata.append("status",   GLOBAL_ACTION);
    response = ajax_update_supplier_basic_details(formdata)
    encrypted_supplier = response.encrypted_supplier
    message = response.message
    // ajax success response
    if(message.success){
        document.getElementById('supplier_basic_update_success').innerHTML = message.success;
        $('#supplier_basic_update_success').show();
        $('#save_error_div').hide();
        CloseLoaderPopup();
    }
    if(message.error){
        document.getElementById('save_error_div').innerHTML = message.error;
        $('#save_error_div').show();
        $('#supplier_basic_update_success').hide()
    }

    $('html, body').animate({ scrollTop: 0 }, 'slow');
    cancel_basic_details();
    if(GLOBAL_ACTION == 'CREATE'){
        var url = '/admin_tool/supplier_management/supplier_details/' + encrypted_supplier + '';
        location.href = url
    }
    return false;
}

// Function to save edited or updated supplier organizational details data
function supp_org_data_save(){
    OpenLoaderPopup();
    var supplierid = global_supplier_id
    var save_supplier_purch_details = new Array();

    $("#supp_org_details_table TBODY TR").each(function() {
        var row = $(this);
        var get_supp_purch_data = {};
        get_supp_purch_data.delete_supplier = delete_supp_purch_data;
        get_supp_purch_data.supp_id = supplierid;
        get_supp_purch_data.supp_org_guid = row.find("TD").eq(1).text();
        get_supp_purch_data.porg_id = row.find("TD").eq(2).find("select option:selected").val();
        get_supp_purch_data.currency_id = row.find("TD").eq(3).find("select option:selected").val();
        get_supp_purch_data.payment_term = row.find("TD").eq(4).find("select option:selected").val();
        get_supp_purch_data.incoterm = row.find("TD").eq(5).find("select option:selected").val();
        get_supp_purch_data.gr_inv_vrf = row.find("TD").eq(6).find('input[type="checkbox"]').is(':checked');
        get_supp_purch_data.inv_conf_exp = row.find("TD").eq(7).find('input[type="checkbox"]').is(':checked');
        get_supp_purch_data.gr_conf_exp = row.find("TD").eq(8).find('input[type="checkbox"]').is(':checked');
        get_supp_purch_data.po_resp = row.find("TD").eq(9).find('input[type="checkbox"]').is(':checked');
        get_supp_purch_data.ship_notif_exp = row.find("TD").eq(10).find('input[type="checkbox"]').is(':checked');
        get_supp_purch_data.purch_block = row.find("TD").eq(11).find('input[type="checkbox"]').is(':checked');
        save_supplier_purch_details.push(get_supp_purch_data)
    })
    console.log(save_supplier_purch_details)

    $.ajax({
        type: 'POST',
        url: ajax_update_supplier_org_details_url,
        data: JSON.stringify(save_supplier_purch_details),
        dataType: 'json',
        success: function (response) {
            document.getElementById('supplier_org_update_success').innerHTML = response.message;
            $('#supplier_org_update_success').show();
            if (save_supplier_purch_details.length==0){
                edit_supp_org();
            } else{
                supplier_org_data = []
                for (i = 0; i < save_supplier_purch_details.length; i++){
                    supplier_org_data.push(save_supplier_purch_details[i])
                }
                cancel_supp_org_data();
                delete_supp_purch_data = []
            }
            CloseLoaderPopup();
        },
        error: function (error) {
            console.log(error);
        }
    })
    
}
   // Validation function
   const save_basic_form_validation = (name1, city_id, email_id) => {
        var is_valid = true
        var save_form_errors = ''
        var mailformat = /^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/;
        if (name1 == '') {
            is_valid = false
            save_form_errors += messageConstants["JMSG007"];
        }
        if (city_id == '') {
            is_valid = false
            save_form_errors += messageConstants["JMSG007"] + "City";
        }
        if ((email_id == '') || !(email_id.match(mailformat))) {
            is_valid = false
            save_form_errors += messageConstants["JMSG002"] + "Email Id";
        }


        return is_valid, save_form_errors
    }

function enable_disable(action){
    $(".dummy_ft_button_class").hide();
    if(action == 'EDIT'){
        $("#ft_save").show();
        $("#ft_cancel").show();
        $('.toggle_mode').prop('disabled', false)
    }
    else{
        $("#ft_edit").show();
        $('.toggle_mode').prop('disabled', true)
    }
}