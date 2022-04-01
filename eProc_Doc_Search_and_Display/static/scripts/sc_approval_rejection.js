// Script to generate sort and filter feature for tables
$(document).ready( function() {
    table_sort_filter();
    $('.multiple_select').selectpicker();
});

nav_bar_approvals();

// Function to approve/ reject sc's
function approve_status(value){

    var manage_multi_status = {}
    manage_multi_status['status'] = value.id;

    $('#hg_loader').modal('show');
    var status_result = ajax_approve_status(manage_multi_status);
    
    if(status_result) {
        location.reload();
    }
}

// Function to display notes
function approver_note(data){

    var get_text_data = {};
    get_text_data.get_approver_text = 'get_approver_text';
    get_text_data.header_guid = data.split("-")[1];

    var approver_text_result = ajax_get_approver_note(get_text_data)

    if(approver_text_result) {
        console.log(response.approver_note)
        if(response.approver_note === ""){
            $('#approval_note').empty();
            $('#approval_note').append("<h4><span class='badge badge-light'>No approver note available</span></h4>");
            $('#approver_note_modal').modal('show');
        } else {
            $('#approval_note').empty();
            $('#approval_note').append(response.approver_note);
            $('#approver_note_modal').modal('show');
        }
        
    }
    
}