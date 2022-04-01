// Script to generate sort and filter feature for tables
$(document).ready( function() {
  
  table_sort_filter_export_excel();
  $('#name1').val(localStorage.getItem("name1"));
  $('#name2').val(localStorage.getItem("name2"));
  $('#supplier_id').val(localStorage.getItem("supplier_id"));
  $('#search_term1').val(localStorage.getItem("search_term1"));
  $('#search_term2').val(localStorage.getItem("search_term2"));
  $('#city').val(localStorage.getItem("city"));
  $('#country_code').val(localStorage.getItem("country_code"));
  nav_bar_admin();
});
