var calendarconfig_data = new Array();
var country_list = new Array();
var validate_add_attributes = [];
var calendar={};


//onclick of upload button display id_data_upload popup and set GLOBAL_ACTION button value
function onclick_upload_button() {
    GLOBAL_ACTION = "calendar_upload"
    $("#id_popup_tbody").empty();
    $('#id_data_upload').modal('show');
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


//onclick of cancel empty the popup table body and error messages
$(".remove_upload_data").click(() => {
    $("#id_error_msg").html("");
    $("#id_popup_tbody").empty();
    $("#id_error_msg").empty();
    $('#myModal').modal('hide');
    $("#id_error_msg").prop("hidden", true);
    $("#id_error_msg_calendar_code").prop("hidden", true);
    $("#id_error_msg_calendar_name").prop("hidden", true);
    $("#id_error_msg_calendar_length").prop("hidden", true);
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
    jQuery.grep(validate_add_attributes, function (el) {
        if (jQuery.inArray(el, main_table_low_value) != -1) { common.push(el); }
    });
    if (common.length != 0) {
        error_message = messageConstants["JMSG001"]
        no_duplicate_entries = 'N'
    }
    return [no_duplicate_entries,error_message]
}

// validating the  popup table for duplicate entries
function compare_table_for_duplicate_entries(validate_add_attributes, calendar) {
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
         $.each(calendar, function (i, item) {
            if (item.description.length == 0) {
                error_message = messageConstants["JMSG002"] + "Description";
                no_duplicate_value = 'N'
                return [no_duplicate_value,error_message]
            }
         });
        }
return [no_duplicate_value,error_message]
}
function display_error_message(error_message){

        $('#error_message').text(error_message);
        document.getElementById("error_message").style.color = "Red";
        $("#error_msg_id").css("display", "block");
        $('#id_save_confirm_popup').modal('hide');
        $('#myModal').modal('show');
    }


//onclick of cancel display the table in display mode............
function display_basic_db_data() {
    $('#display_basic_table').DataTable().destroy();
    $('#id_calendar_tbody').empty();
    var edit_basic_data = '';
    var desc = ''; var country_code;
    var wdays = [];
    var wday_array = [];
    var wd_value = '';

    $.each(rendered_calendar_data, function (i, item) {
        wdays = []
        country_code = item.country_code
        for (i = 0; i < render_country_data.length; i++) {
                if (country_code == render_country_data[i].country_code)
                    desc = render_country_data[i].country_name
            }
        wday_array = item.working_days.split(",");
        for(j=0; j<wday_array.length; j++)
        {
            wdays[j] = get_days(wday_array[j]);
         }

        wday_array = [];
        wd_value = '';
        for(i=0; i<wdays.length;i++){
            wd_value += ' <span  class="badge badge-primary wdays_copy"> '+ wdays[i] +'</span>' + '';
        }

        edit_basic_data += '<tr> <td class="class_select_checkbox"><input class="checkbox_check" onclick="valueChanged()" type="checkbox" required> </td> <td>' + item.calender_id + '</td>'+
         '<td>' + item.description + '</td>'+
         '<td>' + desc + '</td> <td>' + item.year + '</td>'+
          '<td>'+ wd_value +'</td>'+
           '<td hidden>' + item.calendar_config_guid + '</td></tr>';
    });
    $('#id_calendar_tbody').append(edit_basic_data);
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

// Function to hide and display save related popups
$('#save_id').click(function () {
    $('#myModal').modal('hide');
     $("#id_popup_table TBODY TR").each(function () {
            var row = $(this);
            calendar = {};

                var workingDay;
                var guid;
                calendar.calender_id = (row.find("TD").eq(1).find('input[type="text"]').val())
                calendar.country = (row.find("TD").eq(3).find('select[type="text"]').val())
                calendar.description = (row.find("TD").eq(2).find('input[type="text"]').val())
                calendar.year = (row.find("TD").eq(4).find('input[type="text"]').val())
                workingDay = (row.find("TD").eq(5).find('select[type="text"]').val())
                calendar.working_days = workingDay.join()
                calendar.del_ind = row.find("TD").eq(6).find('input[type="checkbox"]').is(':checked')
                calendar.calendar_config_guid = row.find("TD").eq(7).find('input[type="text"]').val()

                if(calendar.calendar_config_guid == undefined) {
                   calendar.calendar_config_guid = ''
                }
                if(calendar.calender_id == undefined) {
                   calendar.calender_id = ''
                }
                validate_add_attributes.push(calendar.calender_id);
                calendarconfig_data.push(calendar);

        });
    $('#id_save_confirm_popup').modal('show');
});


//onclick of delete,delete the row.
function application_settings_delete_Row1(myTable) {
    $('#id_popup_table').DataTable().destroy();

    try {
        var table = document.getElementById(myTable);
        var rowCount = table.rows.length;

        for (var i = 0; i < rowCount; i++) {
            var row = table.rows[i];
            var chkbox = row.cells[0].childNodes[0];
            console.log(chkbox);
            if ( true == chkbox.checked) {
                table.deleteRow(i);
                rowCount--;
                i--;
            }
        }
        $("#id_delete_currency").hide();
        $("#id_copy_currency").hide();
        $("#id_update_currency").hide();
        $("#error_msg_id").css("display", "none");
        table_sort_filter_popup('id_popup_table');
        return rowCount;
    } catch (e) {
        alert(e);
    }
}
$('#deleteBtn').click(function(){
     $('#id_popup_table').DataTable().destroy();
    try {
        var myTable = 'id_popup_table'
        var table = document.getElementById(myTable);
        var rowCount = table.rows.length;

        for (var i = 0; i < rowCount; i++) {
            var row = table.rows[i];
            var chkbox = row.cells[0].childNodes[0];
            console.log(chkbox);
            if ( true == chkbox.checked) {
                table.deleteRow(i);
                rowCount--;
                i--;
            }
        }
        $("#id_delete_currency").hide();
        $("#id_copy_currency").hide();
        $("#id_update_currency").hide();
        $("#error_msg_id").css("display", "none");
        table_sort_filter_popup('id_popup_table');
        return rowCount;
    } catch (e) {
        alert(e);
    }
        });