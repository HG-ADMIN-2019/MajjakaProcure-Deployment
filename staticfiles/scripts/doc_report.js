
$(document).ready( function() {

    // display admin role submenu
    nav_bar_admin()

    // Script to generate sort and filter feature for tables
    table_sort_filter_export_excel();


    // Loader implementation on search button
    $('#hg_doc_report_search').click(function() {
        $('#hg_loader').modal('show');
    });
    //  $("#err_msg").prop("hidden",true)

});

// Function to store the data into the session
window.onbeforeunload = function() {
        sessionStorage.setItem("DOC_TYPE", $('#id_doc_type').val());
        sessionStorage.setItem("FROM_DATE",$('#id_from_date').val());
        sessionStorage.setItem("TO_DATE",$('#id_to_date').val());
       // sessionStorage.setItem("COMPANY",$('#id_company_code').val());
        sessionStorage.setItem("REQUESTER",$('#id_requester').val());
        sessionStorage.setItem("CREATED_BY",$('#id_created_by').val());
}

// Function to retrieve data from session storage
window.onload = function () {
    default_value = sessionStorage.getItem("DOC_TYPE");
    frm_date = sessionStorage.getItem("FROM_DATE");
    to_date = sessionStorage.getItem("TO_DATE");
    requester = sessionStorage.getItem("REQUESTER");
    created_by = sessionStorage.getItem("CREATED_BY");
   // company = sessionStorage.getItem("COMPANY");

    // if the previously selected doctype is same as now then do not reset the dates
    // else we need to reset the date to today's date

    if (default_value !== null)
    {
        if (default_value !== $('#id_doc_type').val())
            {
            $('#id_doc_type').val(default_value).attr('selected', 'selected');
            $('#id_doc_list').hide();

            if(frm_date !== null )
            {    $('#id_from_date').val(frm_date);  }

            if(to_date !==null )
            {    $('#id_to_date').val(to_date);    }

            if(requester !== null)
            {   $('#id_requester').val(requester);   }

            if('created_by' !== null)
            {   $('#id_created_by').val(created_by);  }

//            if('company' !== null)
//            {   $('#id_company_code').val(company).attr('selected', 'selected'); }
//            }
            else
            {
            $('#id_doc_type').val(default_value).attr('selected', 'selected');

            if(frm_date !== null )
            {    $('#id_from_date').val(frm_date);  }

            if(to_date !==null )
            {    $('#id_to_date').val(to_date);    }

            if(requester !== null)
            {   $('#id_requester').val(requester);   }

            if('created_by' !== null)
            {   $('#id_created_by').val(created_by);  }

//            if('company' !== null)
//            {   $('#id_company_code').val(company).attr('selected', 'selected'); }

        }
    }
}
function search_click(){
          $("#err_msg").prop("hidden",false)
}