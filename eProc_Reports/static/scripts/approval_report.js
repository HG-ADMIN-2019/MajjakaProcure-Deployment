    // Script to generate sort and filter feature for tables
    $(document).ready(function () {
        nav_bar_admin();
        table_sort_filter_export_excel();

        // Loader implementation on search button
        $('#hg_approval_report_search').click(function () {
            $('#hg_loader').modal('show');
        });
    });

    // Function to store the data into the session
    window.onbeforeunload = function () {
        sessionStorage.setItem("COMP_CODE", $('#id_comp_code_app').val());
        sessionStorage.setItem("ACC_ASSGN_CAT", $('#id_acc_assgn_cat').val());
    }

    // Function to retrieve data from session storage
    window.onload = function () {
        comp_code = sessionStorage.getItem("COMP_CODE");
        acc_assgn_cat = sessionStorage.getItem("ACC_ASSGN_CAT");

        $('#id_comp_code_app').val(comp_code).attr('selected', 'selected');
        $('#id_acc_assgn_cat').val(acc_assgn_cat).attr('selected', 'selected');
    }