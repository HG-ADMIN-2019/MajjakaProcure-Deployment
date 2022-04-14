    //Display submenu  for purchaser and purchaser assist role
    nav_bar_purchaser();

    $(document).ready(function() {
        $('.table_sort_filter_pagination').DataTable( {
            "lengthChange": false,
            "searching":   false,
            "ordering": false,
            "info":     false
        } );
    } );

    $('.multiple_select').selectpicker();