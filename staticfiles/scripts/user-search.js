 // Script to generate sort and filter feature for tables
 $(document).ready( function() {
   // nav_bar_admin();
    table_sort_filter_export_excel();
   $('#username').val(localStorage.getItem("username"));
   $('#first_name').val(localStorage.getItem("first_name"));
   $('#last_name').val(localStorage.getItem("last_name"));
   $('#email').val(localStorage.getItem("email"));
   $('#user_type').val(localStorage.getItem("user_type"));
   $('#employee_id').val(localStorage.getItem("employee_id"));
});
//onclick of upload button display id_data_upload popup and set GLOBAL_ACTION button value
function onclick_upload_button() {
    GLOBAL_ACTION = "employee_upload"
  //  $("#user_tab_tbody").empty();
    $('#id_data_upload').modal('show');
    document.getElementById('id_file_data_upload').value = "";
}