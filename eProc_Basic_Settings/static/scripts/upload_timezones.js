var timezone_data = new Array();
var validate_add_attributes = [];
var timezone={};

//onclick of add button display myModal popup and set GLOBAL_ACTION button value
function onclick_add_button(button) {
    $("#error_msg_id").css("display", "none")
    $( "#header_select").prop( "hidden", false );
    GLOBAL_ACTION = button.value
     $('#id_popup_table').DataTable().destroy();
    $("#id_popup_tbody").empty();
    $('#myModal').modal('show');
    basic_add_new_html = '<tr ><td><input type="checkbox" required></td><td><input class="form-control"  type="text" pattern="[A-Z]" maxlength="6" onkeypress="return /[a-z]/i.test(event.key)" name="timezonecode" style="text-transform:uppercase;" required></td><td><input class="input form-control" type="text" maxlength="255" onkeypress="return /[a-z ]/i.test(event.key)" name="timezonename" required></td><td><input class="input form-control" type="text" maxlength="15" onkeypress="return /[a-z0-9 :+-]/i.test(event.key)" name="utcdifference"  style="text-transform:uppercase;" required></td><td><input class="input form-control" type="text" maxlength="10" onkeypress="return /[a-z ]/i.test(event.key)" name="daylightsave"  pattern="[A-Z]" style="text-transform:uppercase;"></td><td class="class_del_checkbox" hidden><input type="checkbox" required></td></tr>';
    $('#id_popup_tbody').append(basic_add_new_html);
    table_sort_filter('id_popup_table');
    $("#id_del_ind_checkbox").prop("hidden", true);
    document.getElementById("id_del_add_button").style.display = "block";
    $("#save_id").prop("hidden", false);
}
//******************************************

 //onclick of upload button display id_data_upload popup and set GLOBAL_ACTION button value
function onclick_upload_button() {
    GLOBAL_ACTION = "timezone_upload"
    $("#id_popup_tbody").empty();
    $('#id_data_upload').modal('show');
}
//****************************************

// on click copy icon display the selected checkbox data
function onclick_copy_button() {
    GLOBAL_ACTION = "COPY"
    onclick_copy_update_button("copy")
    document.getElementById("id_del_add_button").style.display = "block";
}
//****************************************

// on click update icon display the selected checkbox data to update
function onclick_update_button() {
    GLOBAL_ACTION = "UPDATE"
    onclick_copy_update_button("update")
    document.getElementById("id_del_add_button").style.display = "none";
}

//**********************************************************
function onclick_copy_update_button(data) {
        $("#error_msg_id").css("display", "none")
        $("#id_popup_tbody").empty();
        $('#display_basic_table').DataTable().destroy();
        //Reference the Table.
        var grid = document.getElementById("display_basic_table");

    //Reference the CheckBoxes in Table.
    var checkBoxes = grid.getElementsByTagName("INPUT");
    var edit_basic_data = "";
    var unique_input = '';
    //Loop through the CheckBoxes.
    for (var i = 1; i < checkBoxes.length; i++) {
        if (checkBoxes[i].checked) {
            var row = checkBoxes[i].parentNode.parentNode;
            if(GLOBAL_ACTION == "UPDATE"){
                unique_input = '<input class="form-control" type="text" value="' + row.cells[1].innerHTML + '" name="time_zone" onkeypress="return /[a-z]/i.test(event.key)" maxlength="6" style="text-transform:uppercase" disabled>'
                 edit_basic_data += '<tr ><td hidden><input type="checkbox" required></td>'+
                 '<td>'+ unique_input +'</td>'+
                 '<td><input class="form-control" value="' + row.cells[2].innerHTML + '" type="text" onkeypress="return /[a-z ]/i.test(event.key)" name="description"  maxlength="255" required></td>'+
                 '<td><input class="form-control" value="' + row.cells[3].innerHTML + '" type="text" onkeypress="return /[a-z0-9 +:-]/i.test(event.key)" name="utcdifference"  maxlength="15" style="text-transform:uppercase" required></td>'+
                 '<td><input class="form-control" value="' + row.cells[4].innerHTML + '" type="text" onkeypress="return /[a-z]/i.test(event.key)" name="daylightsave"  maxlength="10" style="text-transform:uppercase"</td><td class="class_del_checkbox" hidden><input type="checkbox" required></td></tr>';
                 $("#header_select").prop("hidden", true);
            }
            else{
                unique_input = '<input class="form-control" type="text" value="' + row.cells[1].innerHTML + '" name="time_zone" onkeypress="return /[a-z]/i.test(event.key)" maxlength="6" style="text-transform:uppercase" required>'
                 edit_basic_data += '<tr ><td><input type="checkbox" required></td>'+
                 '<td>'+ unique_input +'</td>'+
                 '<td><input class="form-control" value="' + row.cells[2].innerHTML + '" type="text" onkeypress="return /[a-z ]/i.test(event.key)" name="description"  maxlength="255" required></td>'+
                 '<td><input class="form-control" value="' + row.cells[3].innerHTML + '" type="text" onkeypress="return /[a-z0-9 +:-]/i.test(event.key)" name="utcdifference"  maxlength="15" style="text-transform:uppercase" required></td>'+
                 '<td><input class="form-control" value="' + row.cells[4].innerHTML + '" type="text" onkeypress="return /[a-z]/i.test(event.key)" name="daylightsave"  maxlength="10" style="text-transform:uppercase"</td><td class="class_del_checkbox" hidden><input type="checkbox" required></td></tr>';
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

//onclick of cancel empty the popup table body and error messages
$(".remove_upload_data").click(() => {
    $("#id_error_msg").html("");
    $("#id_popup_tbody").empty();
    $("#id_error_msg").empty();
    $('#myModal').modal('hide');
    $("#id_error_msg").prop("hidden", true);
    $("#id_error_msg_timezone_code").prop("hidden", true);
    $("#id_error_msg_timezone_name").prop("hidden", true);
    $("#id_error_msg_timezone_length").prop("hidden", true);
    $("#id_check_error_messages").prop("hidden", true);
    $("#id_check_success_messages").prop("hidden", true);
    $("#id_check_special_character_messages").prop("hidden", true)
    $("#id_check_data").prop("hidden", true);
    $('#id_popup_table').DataTable().destroy();
});


//validate by comparing  main table values and popup table values
function maintable_validation(validate_add_attributes, main_table_low_value) {
    var no_duplicate_entries = 'Y'
    var error_message =''
    var common = [];
    jQuery.grep(validate_add_attributes, function(el) {
        if (jQuery.inArray(el, main_table_low_value) != -1) {
            common.push(el);
        }
    });
    if (common.length != 0) {
        error_message = messageConstants["JMSG001"]

        no_duplicate_entries = 'N'
    }
    return [no_duplicate_entries,error_message]
}


// validating the  popup table for duplicate entries
function compare_table_for_duplicate_entries(validate_add_attributes, timezone) {
    add_attr_duplicates = false;
    var error_message = ''
    var add_attr_duplicates_list = [];
    var add_attr_unique_list = [];
    var no_duplicate_value = 'Y'
    $.each(validate_add_attributes, function(index, value) {
        if ($.inArray(value, add_attr_unique_list) == -1) {
            add_attr_unique_list.push(value);
        } else {
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
         $.each(timezone, function (i, item) {
            if (item.time_zone.length == 0) {
                error_message = messageConstants["JMSG002"] + "Timezone";
                no_duplicate_value = 'N'
                return [no_duplicate_value,error_message]
            }
            if (item.description.length == 0) {
                error_message = messageConstants["JMSG002"] + "Description";
                no_duplicate_value = 'N'
                return [no_duplicate_value,error_message]
            }
            if (item.utc_difference.length == 0) {
                error_message = messageConstants["JMSG002"] + "UTC Difference";
                no_duplicate_value = 'N'
                return [no_duplicate_value,error_message]
            }
            utc_difference = item.utc_difference.replace(/\s\s+/g, ' ')
            if (utc_difference == " ") {
            error_message = messageConstants["JMSG002"] + "UTC Difference Name";
             no_duplicate_value = 'N'
             return [no_duplicate_value,error_message]
           }
         });
     }
        
       
    return [no_duplicate_value,error_message]
}
function display_error_message(error_message){
        $("#error_msg_id").css("display", "none")
        $('#error_message').text(error_message);
        //$("p").css("color", "red");
        //document.getElementById("error_message").innerHTML = error_message;
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
    $(".modal").on("hidden.bs.modal", function() {
        $("#id_error_msg").html("no records found");
    });
    basic_add_new_html = '<tr ><td><input type="checkbox" required></td>'+
    '<td><input class="input form-control" type="text" pattern="[A-Z]" maxlength="6" onkeypress="return /[a-z]/i.test(event.key)" name="timezonecode" style="text-transform:uppercase;" required></td>'+
    '<td><input class="input form-control" type="text" maxlength="255" onkeypress="return /[a-z ]/i.test(event.key)" name="timezonename"  required></td>'+
    '<td><input class="input form-control" type="text" maxlength="15" onkeypress="return /[a-z0-9 +:-]/i.test(event.key)" name="utcdifference"  pattern="[A-Z]" style="text-transform:uppercase;" required></td>'+
    '<td><input class="input form-control" type="text" maxlength="10" onkeypress="return /[a-z ]/i.test(event.key)" name="daylightsave"  pattern="[A-Z]" style="text-transform:uppercase;" required></td><td class="class_del_checkbox" hidden><input type="checkbox" required></td></tr>';
    $('#id_popup_tbody').append(basic_add_new_html);
    if (GLOBAL_ACTION == "timezone_upload") {
        $(".class_del_checkbox").prop("hidden", false);
    }
    table_sort_filter_popup('id_popup_table');
}


//onclick of cancel display the table in display mode............
function display_basic_db_data() {
    $('#display_basic_table').DataTable().destroy();
    $('#id_timezone_tbody').empty();
    var edit_basic_data = '';
  
    $.each(rendered_timezone_data, function(i, item) {
        edit_basic_data += '<tr ><td class="class_select_checkbox"><input class="checkbox_check" onclick="valueChanged()" type="checkbox" required></td><td>' + item.time_zone + '</td><td>' + item.description + '</td><td>' + item.utc_difference + '</td><td>' + item.daylight_save_rule + '</td></tr>';
    });
    $('#id_timezone_tbody').append(edit_basic_data);
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


//deletes he duplicate data
function delete_duplicate() {
    $('#id_popup_table').DataTable().destroy();
    var time_zone_check = new Array
    $("#id_popup_table TBODY TR").each(function() {
        var row = $(this);

        //*************** reading data from the pop-up ***************
        time_zone = row.find("TD").eq(1).find('input[type="text"]').val().toUpperCase();
        description = row.find("TD").eq(2).find('input[type="text"]').val().toUpperCase();
        utc_difference = row.find("TD").eq(3).find('input[type="text"]').val().toUpperCase();
        daylight_save_rule = row.find("TD").eq(4);
        checked_box = row.find("TD").eq(5).find('input[type="checkbox"]').is(':checked')


        if (time_zone_check.includes(time_zone)) {
            $(row).remove();
        }

        time_zone_check.push(time_zone);


    })
    table_sort_filter_popup_pagination('id_popup_table')
    check_data()
}

// Functtion to hide and display save related popups
$('#save_id').click(function () {
    $('#myModal').modal('hide');
    timezone_data = new Array();
    validate_add_attributes = [];
   $("#id_popup_table TBODY TR").each(function () {
           var row = $(this);
           timezone={};
           timezone.time_zone = row.find("TD").eq(1).find('input[type="text"]').val().toUpperCase();
           timezone.description = row.find("TD").eq(2).find('input[type="text"]').val().toUpperCase();
           timezone.utc_difference = row.find("TD").eq(3).find('input[type="text"]').val().toUpperCase();
           timezone.daylight_save_rule = row.find("TD").eq(4).find('input[type="text"]').val().toUpperCase();
           timezone.del_ind = row.find("TD").eq(5).find('input[type="checkbox"]').is(':checked');

           if (timezone == undefined) {
                timezone.time_zone = row.find("TD").eq(1).find('input[type="text"]').val();
           }
           validate_add_attributes.push(timezone.time_zone);
           timezone_data.push(timezone);
       });
    $('#id_save_confirm_popup').modal('show');
});


