var cust_prod_cat_desc_data = new Array();
var validate_add_attributes = [];
var cusprodcatdesc={};

//onclick of add button display myModal popup and set GLOBAL_ACTION button value
function onclick_add_button(button) {
    GLOBAL_ACTION = button.value
    $("#id_popup_tbody").empty();
    $('#myModal').modal('show');
    basic_add_new_html = '<tr><td><input type="checkbox" required></td><td><select class="form-control">'+prod_cat_id_dropdown+'</select></td><td><input class="form-control" type="text" maxlength="8" onkeypress="return /[a-z0-9]/i.test(event.key)" name="description" style="text-transform:uppercase;" required></td><td><select class="form-control">'+language_id_dropdown+'</select></td><td hidden></td><td hidden> del_ind</td></tr>';
    $('#id_popup_tbody').append(basic_add_new_html);
    $("#id_del_ind_checkbox").prop("hidden", true);
    document.getElementById("id_del_add_button").style.display = "block";
    $("#save_id").prop("hidden", false);
}


//onclick of upload button display id_data_upload popup and set GLOBAL_ACTION button value
function onclick_upload_button() {
    GLOBAL_ACTION = "cusprodcatdesc_upload"
    $("#id_popup_tbody").empty();
    $('#id_data_upload').modal('show');
    document.getElementById('id_file_data_upload').value = "";
}
//***************************

// on click copy icon display the selected checkbox data
function onclick_copy_button() {
    GLOBAL_ACTION = "cusprodcatdesc_copy"
    onclick_copy_update_button("copy")
    document.getElementById("id_del_add_button").style.display = "block";
}

// on click update icon display the selected checkbox data to update
function onclick_update_button() {
    GLOBAL_ACTION = "cusprodcatdesc_update"
    onclick_copy_update_button("update")
    document.getElementById("id_del_add_button").style.display = "none";
}

//**********************************************************
function onclick_copy_update_button(data){
        $("#id_popup_tbody").empty();
        $('#display_basic_table').DataTable().destroy();
        //Reference the Table.
        var grid = document.getElementById("display_basic_table");

        //Reference the CheckBoxes in Table.
        var checkBoxes = grid.getElementsByTagName("INPUT");
        var edit_basic_data = "";
        var unique_input = '';
        var dropdown_values = [];
        //Loop through the CheckBoxes.
        for (var i = 1; i < checkBoxes.length; i++){
            if (checkBoxes[i].checked){
                var row = checkBoxes[i].parentNode.parentNode;
                var prod_cat_id_value = row.cells[1].innerHTML
                var language_id_value = row.cells[3].innerHTML
                dropdown_values.push([prod_cat_id_value, language_id_value])

                if(GLOBAL_ACTION == "cusprodcatdesc_update"){
                    unique_input = '<select class="form-control" disabled><option selected="true" disabled="disabled">' + row.cells[1].innerHTML + '</option>' + prod_cat_id_dropdown + '</select>'
                    edit_basic_data += '<tr><td hidden><input type="checkbox"></td><td>'+unique_input+' </td><td><input class="form-control" value="' + row.cells[2].innerHTML + '" type="text" onkeypress="return /[a-z ]/i.test(event.key)" name="description"  maxlength="100" style="text-transform:uppercase" required></td><td><select class="form-control" disabled><option selected="true" disabled="disabled">' + row.cells[3].innerHTML + '</option>' +language_id_dropdown + ' </select></td><td hidden></td><td class="class_del_checkbox" hidden><input type="checkbox" required></td></tr>';
                    $("#header_select").prop("hidden", true);
                }
                else{
                    unique_input = '<select class="form-control"><option selected="true">' + row.cells[1].innerHTML + '</option>' + prod_cat_id_dropdown + '</select>'
                    edit_basic_data += '<tr><td><input type="checkbox" required></td><td>'+unique_input+'</td><td><input class="form-control" value="' + row.cells[2].innerHTML + '" type="text" onkeypress="return /[a-z ]/i.test(event.key)" name="description"  maxlength="100" style="text-transform:uppercase" required></td><td><select class="form-control"><option selected="true">' + row.cells[3].innerHTML + '</option>' +language_id_dropdown + ' </select></td><td hidden></td><td class="class_del_checkbox" hidden><input type="checkbox" required></td></tr>';
                    $("#header_select").prop("hidden", false);
                }
            }
        }

        $('#id_popup_tbody').append(edit_basic_data);
        $("#id_del_ind_checkbox").prop("hidden", true);
        $('#myModal').modal('show');
        table_sort_filter('id_popup_table');
        table_sort_filter('display_basic_table');

  }

 //************************currency code
//onclick of cancel empty the popup table body and error messages
$(".remove_upload_data").click(() => {
    $("#id_error_msg").html("");
    $("#id_popup_tbody").empty();
    $("#id_error_msg").empty();
    $('#myModal').modal('hide');
    $("#id_error_msg").prop("hidden", true);
    $("#id_error_msg_country_code").prop("hidden", true);
    $("#id_error_msg_country_name").prop("hidden", true);
    $("#id_error_msg_country_length").prop("hidden", true);
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
    jQuery.grep(validate_add_attributes, function (el) {
        if (jQuery.inArray(el, main_table_low_value) != -1) { common.push(el); }
    });
    if (common.length != 0) {
        $("#id_error_msg").prop("hidden", false)
        $('#id_error_msg').text(messageConstants["JMSG001"])
        document.getElementById("id_error_msg").style.color = "Red";
        $('#id_save_confirm_popup').modal('hide');
        $('#myModal').modal('show');
        no_duplicate_entries = 'N'
    }
    return no_duplicate_entries
}

// validating the  popup table for duplicate entries
function compare_table_for_duplicate_entries(validate_add_attributes, cusprodcatdesc) {
    add_attr_duplicates = false;
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
        $("#id_error_msg").prop("hidden", false)
       document.getElementById("id_error_msg").innerHTML = messageConstants["JMSG001"];
       document.getElementById("id_error_msg").style.color = "Red";
        $('#id_save_confirm_popup').modal('hide');
        $('#myModal').modal('show');
        no_duplicate_value = 'N'
    }

<!--   else if (cusprodcatdesc.cusprodcatdesc_prod_cat_desc.length == 0) {-->
<!--       $("#id_error_msg").prop("hidden", false)-->
<!--       Error_msg = "";-->
<!--       Error_msg = messageConstants["JMSG002"] + "CUSPRODCATDESC Name";-->
<!--       document.getElementById("id_error_msg").innerHTML = Error_msg;-->
<!--       document.getElementById("id_error_msg").style.color = "Red";-->
<!--       $('#id_save_confirm_popup').modal('hide');-->
<!--       $('#myModal').modal('show');-->
<!--   }-->

    return no_duplicate_value
}

//*******************************************************
// on click add icon display the row in to add the new entries
function add_popup_row() {
    basic_add_new_html = '';
    var display_db_data = '';
    $('#id_popup_table').DataTable().destroy();
    $(".modal").on("hidden.bs.modal", function () {
    $("#id_error_msg").html(" ");
     });
    basic_add_new_html = '<tr><td><input type="checkbox" required></td><td><select class="form-control">'+prod_cat_id_dropdown+'</select></td><td><input class="form-control" type="text" maxlength="8" onkeypress="return /[a-z0-9]/i.test(event.key)" name="prod_cat_desc" style="text-transform:uppercase;" required></td><td><select class="form-control">'+language_id_dropdown+'</select></td><td hidden><guid></td><td hidden>< del_ind></td></tr>';
     $('#id_popup_tbody').append(basic_add_new_html);
    if (GLOBAL_ACTION == "cusprodcatdesc_upload") {
        $(".class_del_checkbox").prop("hidden", false);
    }
    table_sort_filter_popup('id_popup_table');
}
//onclick of cancel display the table in display mode............

function display_basic_db_data(){
$('#display_basic_table').DataTable().destroy();
    $('#id_cusprodcatdesc_tbody').empty();
    var edit_basic_data = '';
    $.each(rendered_cust_prod_cat_desc_data, function (i, item) {
        edit_basic_data += '<tr><td class="class_select_checkbox" ><input class="checkbox_check" onclick="valueChanged()" type="checkbox" required></td><td>' + item.prod_cat_id + '</td><td>' + item.prod_cat_desc + '</td><td>' + item.language_id + '</td>><td hidden>' + item.prod_cat_desc_guid + '</td><td hidden>' + item.prod_cat_desc_del_ind + '</td></tr>';
    });
    $('#id_cusprodcatdesc_tbody').append(edit_basic_data);
    $( "#hg_select_checkbox").prop( "hidden", true );
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
    var cusprodcatdesc_code_check = new Array
    $("#id_popup_table TBODY TR").each(function () {
        var row = $(this);

        //*************** reading data from the pop-up ***************
        cusprodcatdesc_prod_cat_desc = row.find("TD").eq(2).find('input[type="text"]').val().toUpperCase();
        cusprodcatdesc_prod_cat_id = row.find("TD").eq(1).find('input[type="text"]').val().toUpperCase();
        checked_box = row.find("TD").eq(3).find('input[type="checkbox"]').is(':checked')


        if (cusprodcatdesc_prod_cat_id_check.includes(cusprodcatdesc_prod_cat_id)) {
            $(row).remove();
        }
        cusprodcatdesc_check.push(cusprodcatdesc_prod_cat_id);
    })
    table_sort_filter_popup_pagination('id_popup_table')
    check_data()
}

// Function to hide and display save related popups
$('#save_id').click(function () {
    $('#myModal').modal('hide');
    $('#id_save_confirm_popup').modal('show');
});

//delete the selected row in db................
var main_table_cusprodcatdesc_checked = [];
function main_table_delete(){

    var Tabledata = { "Dbl_clck_tbl_id": 'upload_custprodcatdesc' };
    $('#display_basic_table').DataTable().destroy();
    $("#display_basic_table TBODY TR").each(function () {
        var row = $(this);
        var cusprodcatdesc_arr_obj ={};
            cusprodcatdesc_arr_obj.del_ind = row.find("TD").eq(0).find('input[type="checkbox"]').is(':checked');
            if(cusprodcatdesc_arr_obj.del_ind){
            cusprodcatdesc_arr_obj.prod_cat_id = row.find("TD").eq(1).html();
            cusprodcatdesc_arr_obj.prod_cat_desc = row.find("TD").eq(2).html();
            cusprodcatdesc_arr_obj.language_id = row.find("TD").eq(3).html();
            cusprodcatdesc_arr_obj.prod_cat_desc_guid = row.find("TD").eq(4).html();
            main_table_cusprodcatdesc_checked.push(cusprodcatdesc_arr_obj);
            }
    });
    $('#id_delete_confirm_popup').modal('hide');

    $.ajax({
        type: 'POST',
        url: "{% url 'eProc_Master_Settings:save_master_settings_data' %}",
            data:
                JSON.stringify($.extend({}, main_table_cusprodcatdesc_checked, Tabledata)),
            contentType: "application/json; charset=utf-8",
            dataType: "json",
            success: function (Response) {
            rendered_cusprodcatdesc_data = Response[0];
            display_basic_db_data();
            $("#err_msg_app_settings_t").prop("hidden",false)
            document.getElementById("err_msg_app_settings_t").innerHTML = Response[2];
            setTimeout(function(){$("#err_msg_app_settings_t").prop("hidden",true);},5000)
        }
    });
}