$(document).ready(function () {

    nav_bar_admin();

    // Script to generate sort and filter feature for tables
    table_sort_filter_export_excel();

    // Loader implementation on search button
    $('#hg_user_report_search').click(function () {
        $('#hg_loader').modal('show');
    });
});

var default_value = "";
var substitute_type = "";

// Function to store the data into the session
window.onbeforeunload = function () {
    sessionStorage.setItem("USER_REP", $('#id_userrep_type').val());
    sessionStorage.setItem("SUBSTITUTE_TYPE", $('#id_substitute_sub_type').val());
    sessionStorage.setItem("COMPANY_CODE", $('#id_company_code').val());
    // sessionStorage.setItem("ACTIVE",   $('#id_active').val());
}

// Function to retrieve data from session storage
window.onload = function () {
    default_value = sessionStorage.getItem("USER_REP");
    company_code = sessionStorage.getItem("COMPANY_CODE");
    active = sessionStorage.getItem("ACTIVE");

    if (default_value == 'Users_in_company') {
        $('#id_userrep_type').val(default_value).attr('selected', 'selected');
        $('#id_company_code').val(company_code).attr('selected', 'selected');
        // $('#id_active').val(active)
    }
    else {
        $('#substitute_sub_type').show();
        $('#company_code').hide();
        $('#username').hide();
        $('#acive').hide();
    }

    if (substitute_type !== null)
        $('#id_substitute_sub_type').val(substitute_type).attr('selected', 'selected')
}

// At the load of the page this script is executed to remove the Supplier related search fields and
// only show the User related search fields

default_value = sessionStorage.getItem("USER_REP");
substitute_type = sessionStorage.getItem("SUBSTITUTE_TYPE");

if (default_value == 'Users_in_company' || default_value == "" || default_value == null) {
    //Hide the Substitute search fields
    document.getElementById("substitute_sub_type").value = "";
    $('#substitute_sub_type').hide();
}
else {
    // Show only the Substitute related search fields

    document.getElementById("substitute_sub_type").style.display = "block";
    $('select option[value="Substitute"]').attr("selected", true);
    $('#substitute_sub_type').show();

    // Hide the Users_in_company related search fields
    $('#id_userrep_type').val(default_value).attr('selected', 'selected');

    document.getElementById("company_code").value = "";
    document.getElementById("company_code").style.display = "none";

    document.getElementById("username").value = "";
    document.getElementById("username").style.display = "none";

    document.getElementById("active").value = "";
    document.getElementById("active").style.display = "none";

}

// On changing the Report selection show the relevant fields
function getSubReport(value) {
    default_value = value

    if (default_value == 'Users_in_company') {

        // hide the Substitutes table
        // $('#sup_tab').hide();

        // hide the Substitue search fields
        // document.getElementById("substitute_sub_type").value="";
        $('#substitute_sub_type').hide();

        // Show the user fields
        document.getElementById("company_code").style.display = "block";
        $('#company_code').show();

        document.getElementById("username").style.display = "block";
        $('#username_1').show();

        document.getElementById("active").style.display = "block";
        $('#active').show();

    }
    else {
        // It is Substitutes
        // hide the Users in Company table
        // $('#user_tab').hide();

        // hide the Users_in_company fields
        // document.getElementById("company_code").value="";
        $('#company_code').hide();

        //document.getElementById("username").value="";
        $('#username').hide();

        //document.getElementById("active").value="";
        $('#active').hide();

        // Show the Substitute fields
        document.getElementById("substitute_sub_type").style.display = "block";
        $('#substitute_sub_type').show();

        if (substitute_type == 'Approval') {
            // Approval substitutes menu
        }
        else {
            // Good Reciept substitutes menu
        }

    }
}