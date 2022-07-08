var detgl_data = new Array();
var validate_add_attributes = [];
var detgl={};


//onclick of add button display myModal popup and set GLOBAL_ACTION button value
function onclick_add_button(button) {
    $("#error_msg_id").css("display", "none")
    $( "#header_select").prop( "hidden", false );
    GLOBAL_ACTION = button.value
    $('#id_popup_table').DataTable().destroy();
    $("#id_popup_tbody").empty();
    $('#myModal').modal('show');
    basic_add_new_html = '<tr ><td><input type="checkbox" required></td>'+
    '<td><select class="form-control">' + prod_cat_dropdown + '</select></td>'+
    '<td><select class="form-control">' + glacc_dropdown + '</select></td>'+
    '<td><input type="checkbox" name="gl_acc_default" required></td>><td><select class="form-control">' + accasscat_dropdown + '</select></td>'+
    '<td><select class="form-control">' + company_dropdown + '</select></td>'+
    '<td><input class="form-control" type="number" onkeypress="return event.charCode >= 48" min="1" name="From_value"  required></td>'+
    '<td><input class="form-control" type="number" onkeypress="return event.charCode >= 48" min="1" name="To_value"  required></td>'+
    '<td><select class="form-control">' + currency_dropdown + '</select></td><td hidden><input type="text" class="form-control"  value="GUID"</td><td class="class_del_checkbox" hidden><input type="checkbox" required></td></tr>';
    $('#id_popup_tbody').append(basic_add_new_html);
    table_sort_filter('id_popup_table');
    $("#id_del_ind_checkbox").prop("hidden", true);
    document.getElementById("id_del_add_button").style.display = "block";
    $("#save_id").prop("hidden", false);
}


//onclick of cancel empty the popup table body and error messages
$(".remove_upload_data").click(() => {
    $("#id_error_msg").html("");
    $("#id_popup_tbody").empty();
    $("#id_error_msg").empty();
    $("#myModal").modal('hide');
    $("#id_error_msg").prop("hidden", true);
    $("#id_error_Prod_cat_id").prop("hidden", true);
    $("#id_error_Fromvalue_lesserthan_Tovalue").prop("hidden", true);
    $("#id_error_FromvalueTovalue_positive_num").prop("hidden", true);
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
    

//onclick of upload button display id_data_upload popup and set GLOBAL_ACTION button value
function onclick_upload_button() {
    GLOBAL_ACTION = "detgl_upload"
    $("#id_popup_tbody").empty();
    $('#id_data_upload').modal('show');
    document.getElementById('id_file_data_upload').value = "";

}
//******************
// on click copy icon display the selected checkbox data
function onclick_copy_button() {
    GLOBAL_ACTION = "COPY"
    onclick_copy_update_button('copy')
    document.getElementById("id_del_add_button").style.display = "block";
}
//***********************************
// on click update icon display the selected checkbox data to update
function onclick_update_button() {
    GLOBAL_ACTION = "UPDATE"
    onclick_copy_update_button('update')
    document.getElementById("id_del_add_button").style.display = "none";
}
//**********************************************************
function onclick_copy_update_button() {

      $("#error_msg_id").css("display", "none")
      $('#display_basic_table').DataTable().destroy();
      $("#id_popup_tbody").empty();

    //Reference the Table.
    var grid = document.getElementById("display_basic_table");

    //Reference the CheckBoxes in Table.
    var checkBoxes = document.getElementsByClassName("checkbox_check");
    var edit_basic_data = "";
    var dropdown_array = [];
  
    //Loop through the CheckBoxes.
    for (var i = 0; i < checkBoxes.length; i++) {
        if (checkBoxes[i].checked) {
            var row = checkBoxes[i].parentNode.parentNode;

            if (GLOBAL_ACTION == "UPDATE") {
                guid = 'GUID';
                unique_input = '<select class="form-control"><option selected="true" disabled="disabled">' + row.cells[1].innerHTML + '</option>' + prod_cat_dropdown + ' </select>'
                edit_basic_data += '<tr ><td hidden><input type="checkbox" required></td>'+
                '<td>'+unique_input+'</td>'+
                 '<td><input class="form-control" type="number" value="' + row.cells[2].innerHTML + '" onkeypress="return event.charCode >= 48" min="1" name="From_value"  required></td><td><input class="form-control" type="number" value="' + row.cells[3].innerHTML + '" onkeypress="return event.charCode >= 48" min="1" name="To_value"  required></td><td><select class="form-control"><option selected="true">' + row.cells[4].innerHTML + '</option>' + glacc_dropdown + '</select></td><td><input type="checkbox" name="default" required></td>'+
                 '<td><select class="form-control"><option selected="true" disabled="disabled">' + row.cells[6].innerHTML + '</option>' + company_dropdown + ' </select></td>'+
                 '<td><select class="form-control"><option selected="true">' + row.cells[7].innerHTML + '</option>' + accasscat_dropdown + '</select></td><td><select class="form-control"><option selected="true">' + row.cells[8].innerHTML + '</option>' + currency_dropdown + '</select></td><td hidden><input type="text" class ="form-control"  value="' + guid + '"</td><td class="class_del_checkbox" hidden><input type="checkbox" required></td></tr>';
                 $("#header_select").prop("hidden", true);
          
            } else {
                guid = row.cells[9].innerHTML;
                unique_input = '<select class="form-control"><option selected="true">' + row.cells[1].innerHTML + '</option>' + prod_cat_dropdown + ' </select>'
                edit_basic_data += '<tr ><td><input type="checkbox" required></td>'+
                '<td>'+unique_input+'</td><td><select class="form-control"><option selected="true">' + row.cells[2].innerHTML + '</option>' + glacc_dropdown + '</select></td><td><input type="checkbox" name="gl_acc_default" required></td>'+
                 '<td><select class="form-control"><option selected="true">' + row.cells[4].innerHTML + '</option>' + accasscat_dropdown + '</select></td>' +
                 '<td><select class="form-control"><option selected="true" disabled="disabled">' + row.cells[5].innerHTML + '</option>' + company_dropdown + ' </select></td>'+
                 '<td><input class="form-control" type="number" value="' + row.cells[6].innerHTML + '" onkeypress="return event.charCode >= 48" min="1" name="From_value"  required></td><td><input class="form-control" type="number" value="' + row.cells[7].innerHTML + '" onkeypress="return event.charCode >= 48" min="1" name="To_value"  required></td>' +
                 '<td><select class="form-control"><option selected="true">' + row.cells[8].innerHTML + '</option>' + currency_dropdown + '</select></td><td hidden><input type="text" class ="form-control"></td><td class="class_del_checkbox" hidden><input type="checkbox" required></td></tr>';
                  $("#header_select").prop("hidden", false);
        
            }
            var prod_cat = row.cells[1].innerHTML
            var gl_acc = row.cells[2].innerHTML
            var gl_acc_default = row.cells[3].children.gl_acc_default.checked
            var acc_ass_cat = row.cells[4].innerHTML
            var company_id = row.cells[5].innerHTML
            var currency_id = row.cells[8].innerHTML
            dropdown_array.push([prod_cat,gl_acc, gl_acc_default, acc_ass_cat,company_id,currency_id])

          

         
        }
    }
    $('#id_popup_table').append(edit_basic_data);

    var i = 0;
    $("#id_popup_table TBODY TR").each(function () {
        var row = $(this);
        var prod_cat = dropdown_array[i][0]
        var gl_acc = dropdown_array[i][1];
        var gl_acc_default = dropdown_array[i][2];
        var acc_ass_cat =dropdown_array[i][3];
        var company_id = dropdown_array[i][4];
        var currency_id = dropdown_array[i][5];

        $(row.find("TD").eq(1).find("select option[value=" + prod_cat + "]")).attr('selected', 'selected');
        $(row.find("TD").eq(2).find("select option[value=" + gl_acc + "]")).attr('selected', 'selected');      
       
        if(gl_acc_default) {
            $(row.find("TD").eq(3).find('input[name="gl_acc_default"]').attr('checked', 'checked'));
        }
        $(row.find("TD").eq(4).find("select option[value=" + acc_ass_cat + "]")).attr('selected', 'selected');
        $(row.find("TD").eq(5).find("select option[value=" +  company_id  + "]")).attr('selected', 'selected');
        $(row.find("TD").eq(8).find("select option[value=" + currency_id  + "]")).attr('selected', 'selected');
        
        
        i++;
      });
   
   
    $("#id_del_ind_checkbox").prop("hidden", true);
    $("#myModal").modal('show');
    table_sort_filter('display_basic_table');
    table_sort_filter('id_popup_table');


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
    basic_add_new_html = '<tr ><td><input type="checkbox" required></td>'+
    '<td><select class="form-control">' + prod_cat_dropdown + '</select></td>'+
    '<td><select class="form-control">' + glacc_dropdown + '</select></td>'+
    '<td><input type="checkbox" name="gl_acc_default" required></td><td><select class="form-control">' + accasscat_dropdown + '</select></td>'+
    '<td><select class="form-control">' + company_dropdown + '</select></td>'+
    '<td><input class="form-control" type="number" onkeypress="return event.charCode >= 48" min="1" name="From_value"  required></td>'+
    '<td><input class="form-control" type="number" onkeypress="return event.charCode >= 48" min="1" name="To_value"  required></td>'+
    '<td><select class="form-control">' + currency_dropdown + '</select></td><td hidden><input type="text" class="form-control"  value="GUID"</td><td class="class_del_checkbox" hidden><input type="checkbox" required></td></tr>';
    $('#id_popup_tbody').append(basic_add_new_html);
    if (GLOBAL_ACTION == "detgl_upload") {
        $(".class_del_checkbox").prop("hidden", false);
    }
    table_sort_filter_popup_pagination('id_popup_table');
}


function delete_duplicate() {
    $('#id_popup_table').DataTable().destroy();
    var detgl_code_check = new Array
    $("#id_popup_table TBODY TR").each(function () {
        var row = $(this);

        //*************** reading data from the pop-up ***************
        prod_cat_id = row.find("TD").eq(1).find('input[type="text"]').val().toUpperCase();
        gl_acc_num = row.find("TD").eq(2).find("select option:selected").val();
        gl_acc_default = row.find("TD").eq(3).find('input[type="checkbox"]').is(':checked');
        account_assign_cat = row.find("TD").eq(4).find("select option:selected").val();
        company_id = row.find("TD").eq(5).find("select option:selected").val();
        from_value = row.find("TD").eq(6).find('input[type="number"]').val();
        to_value = row.find("TD").eq(7).find('input[type="number"]').val();
        currency_id = row.find("TD").eq(8).find("select option:selected").val();
        checked_box = row.find("TD").eq(3).find('input[type="checkbox"]').is(':checked');

        var compare = gl_acc_num + '-' + company_id + '-' + account_assign_cat


        if (detgl_code_check.includes(compare)) {
            $(row).remove();
        }

        detgl_code_check.push(compare);


    })
    table_sort_filter_popup_pagination('id_popup_table')
    check_data()
}

// Functtion to hide and display save related popups
$('#save_id').click(function () {
    $('#myModal').modal('hide');
    detgl_data = new Array();
    validate_add_attributes = [];
    $("#id_popup_table TBODY TR").each(function () {
        var row = $(this);
        detgl = {};
        detgl.del_ind = row.find("TD").eq(10).find('input[type="checkbox"]').is(':checked');
        detgl.prod_cat_id = row.find("TD").eq(1).find('select').val();
        detgl.gl_acc_num = row.find("TD").eq(2).find("select option:selected").val();
        detgl.gl_acc_default = row.find("TD").eq(3).find('input[type="checkbox"]').is(':checked');
        detgl.account_assign_cat = row.find("TD").eq(4).find("select option:selected").val();
        detgl.company_id = row.find("TD").eq(5).find("select option:selected").val();
        detgl.from_value = row.find("TD").eq(6).find('input[type="number"]').val();
        detgl.to_value = row.find("TD").eq(7).find('input[type="number"]').val();
        detgl.currency_id = row.find("TD").eq(8).find("select option:selected").val();
        detgl.det_gl_acc_guid = row.find("TD").eq(9).find('input[type="text"]').val();
        var compare = detgl.gl_acc_num + '-' + detgl.company_id + '-' + detgl.account_assign_cat
        if (detgl == undefined) {
            detgl.prod_cat_id = row.find("TD").eq(1).find('input[type="text"]').val();
        }
        validate_add_attributes.push(compare);
        detgl_data.push(detgl);
    });
    $('#id_save_confirm_popup').modal('show');
});


