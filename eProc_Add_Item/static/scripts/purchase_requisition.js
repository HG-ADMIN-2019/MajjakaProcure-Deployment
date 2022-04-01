    nav_bar_shop();
    let url = window.location.href;
    is_edit = false;
    split_url = url.split('/');
    last_index = split_url.slice(-1)[0];
    let document_number = 'create';

    if(last_index.includes('doc_number')){
        is_edit = true
        document_number = last_index.split('-')[1]
    }

    $(document).ready(function (){
        if(is_edit){
            no_slide_menu_style()
            $('#edit_message').html(messageConstants["JMSG033"] + document_number_decrypted + '<a href="#" onclick="go_back_to_sc()"> go back to shopping cart</a>')
            $('#edit_message').show()
        }
    })
    
    // Function to open and initiate data-table for Product category table
    $('#choose_product_cat').click(function(){
        $('#select_prod_cat_modal').modal('show');
        setTimeout(function() {
            $('.prod_cat_datatable').DataTable( {
                "scrollY": "300px",
                "scrollCollapse": true,
            } );
        }, 500);
    })

    // Function to update Product category value
    $('#select_product_category').click(function(){
        var prod_cat_value = ''
        $('#product_category_table TBODY TR').each(function(){
            var row = $(this);
            var check = row.find("TD").eq(0).find('input[type="radio"]').is(':checked');
            if (check){
                prod_cat_id = row.find("TD").eq(1).text();
                prod_cat_desc = row.find("TD").eq(2).text();
                prod_cat_value = prod_cat_id.concat(' - ', prod_cat_desc);

                document.getElementById('choose_product_cat').value = prod_cat_value;
                $('#select_prod_cat_modal').modal('hide');
            }
        });
        $('.prod_cat_datatable').DataTable().destroy()
    });

    const go_back_to_sc = () => {
        get_document_url = localStorage.getItem('opened_document-' + document_number);
        location.href = get_document_url + '/edit';
    }