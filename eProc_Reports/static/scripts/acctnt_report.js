    // Script to generate sort and filter feature for tables
    $(document).ready(function () {
        table_sort_filter_export_excel();
        nav_bar_admin();

        // Loader implementation on search button
        $('#hg_accnt_report_search').click(function () {
            $('#hg_loader').modal('show');
        });
    });


    // Function to store the data into the session
    window.onbeforeunload = function () {
        sessionStorage.setItem("COMP_CODE", $('#id_comp_code_app').val());
        sessionStorage.setItem("ACC_ASSGN_CAT", $('#id_acc_assgn_cat').val());
        sessionStorage.setItem("LANG", $('#id_language').val());
    }

    
    $('#hg_accnt_report_search').click(function () {
        OpenLoaderPopup();
    })
