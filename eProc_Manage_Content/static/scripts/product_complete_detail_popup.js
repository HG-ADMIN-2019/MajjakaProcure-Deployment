function view_detail(prd_detail, prd_catalog_id){
    GLOBAL_PRODUCT_ID = prd_detail;
    product_cat_id={}
    product_cat_id["prod_id"] = prd_detail;
    product_cat_id["catalog_id"] = prd_catalog_id
    GLOBAL_FROM_ID = ''
    var view_detail_response = ajax_view_prod_detail(product_cat_id);
    var response = view_detail_response.prod_detail[0]
    if(response) {
        currency_id = response[0].currency_id
        $("#id_currency").text(response[0].currency_id + ' ');
        $("#id_prod_desc").text(response[0].long_desc);
        $("#id_prod_desc").attr("disabled", "disabled");
        $("#id_desc").text(response[0].short_desc + ' ');
        $("#id_lead_time").text(response[0].lead_time);
        $("#id_lot_size").text(response[0].price_unit);
        $("#id_quantity").val("1");
        $("#id_unspsc_cat").text(response[0].unspsc);
        $("#eform_id").text(response[0].eform_id);
        $("#id_price").text(response[0].price);
        GLOBAL_BASE_PRICE = response[0].price;
        $("#id_unit").text(response[0].unit);
        $("#id_supp").text(response[0].supplier_id);
        var eform_detail = view_detail_response.eform_detail
        GLOBAL_QUANTITY = view_detail_response.quantity_dictionary
        var product_specification = view_detail_response.product_specification
        GLOBAL_FROM_ID = response[0].eform_id
        $('#eform_body').empty();
        update_eform_data(eform_detail)
        if (product_specification.length != 0){
            update_product_specification(product_specification)
        }
        else{
            document.getElementById('prod_spec_div_id').style.display = 'none';
        }
        static_url = '/media/';
        prod_img_detail = view_detail_response.prod_img_detail
        for(i=0; i<prod_img_detail.length; i++){
            var num = i+1
            var num_increment = num.toString()
            var image_id = '#img_'+num_increment
            if (prod_img_detail[i]){
                $(image_id).attr('src',static_url+ prod_img_detail[i].image_url);
            }
        }
        image_visible_div = 0
        // show_image_div()
        $('#prod_detail_popup').modal('show');
    }
}




function update_eform_data(eform_configured){
    console.log(eform_configured);
    if (eform_configured.length > 0) {
        GLOBAL_EFORM_FLAG = true
        $('#eform_body').empty()
        var div_content = '';
        $.each(eform_configured, function (index, value) {
            var line_separator = '';
            eform_field_datatype = value['eform_field_datatype']
            eform_field_name = value['eform_field_name']
            eform_field_count = value['eform_field_count']
            required_flag = value['required_flag']
            var eform_guid = value['eform_field_config_guid']
            GLOBAL_EFORM_GUID.push(eform_guid)
            if ((index + 1) % 2 == 0) {
                line_separator = '<div class="w-100"></div>'
            }

            var options = ''

            if (eform_field_datatype == 'DROPDOWN') {
				var eform_field_data = value['eform_field_data']
				if (eform_field_data){
                    get_dropdown = eform_field_data.split('|~#')
                }
                else{
                    get_dropdown = eform_field_data
                }
				var eform_price_flag = value['price_flag']
				if(eform_price_flag){
                    get_dropdown_price = value['pricing']
                }
                else{
                    get_dropdown_price = []
                }

                var product_description =''
				if(get_dropdown_price.length>0){
					for (i = 0; i < get_dropdown_price.length; i++) {
					    var price_dictionary = get_dropdown_price[i]
					    if ((price_dictionary['pricing_type'] == 'VARIANT_BASE_PRICING') && (price_dictionary['pricing_data_default'] == true)){
					        GLOBAL_BASE_PRICE = price_dictionary['price']
					        //$("#id_desc").text(get_dropdown_price[0].product_description + ' ');
					    }
					    if (price_dictionary['pricing_type'] == 'VARIANT_BASE_PRICING'){
					        $("#id_prod_desc").text(get_dropdown_price[0].product_description + ' ');
					        product_description = price_dictionary['product_description']
					        console.log(price_dictionary)
					    }
					    else{
					        product_description = '';
					    }


						options += '<option value="' + eform_field_name + '|' + price_dictionary['pricing_type'] + '|'+price_dictionary['price']+'|'+price_dictionary['pricing_data']+'|'+price_dictionary['operator']+'|'+eform_field_count+'|'+product_description+'">' + price_dictionary['pricing_data'] + ' </option>'

					}
				}
				else{
				    options = '<option value="" selected>Select</option>'
					for (i = 0; i < get_dropdown.length; i++)
					{
						options += '<option value="' + eform_field_name + '|' + get_dropdown[i] + '|'+eform_field_count+'">' + get_dropdown[i] + ' </option>'
					}

				}


                if (get_dropdown_price.length>0){
                div_content = '<div id="array_index-' + index + '" class="form-group col-6"><label  for="' + eform_field_name + '">' + eform_field_name + ':' + '</label><span id="span_' + eform_field_name + '" ></span><br><select id="' + eform_guid + '" class="form-control toggle_mode '+value['drop_down_type']+' dummy_eform_class" onchange = "change_price(this.value)">' + options + '</select></div>' + line_separator
                }
                else{
                div_content = '<div id="array_index-' + index + '" class="form-group col-6"><label  for="' + eform_field_name + '">' + eform_field_name + ':' + '</label><span id="span_' + eform_field_name + '" ></span><br><select id="' + eform_guid + '" class="form-control toggle_mode '+value['drop_down_type']+' dummy_eform_class">' + options + '</select></div>' + line_separator
                }
            }
            else if (eform_field_datatype == 'checkbox') {
                div_content = '<div id="array_index-' + index + '" class="form-group col-6"><label  for="' + eform_field_name + '">' + eform_field_name + ':' + '</label><span id="span_' + eform_field_name + '" ></span><br><input class="form-control toggle_mode dummy_eform_class" type="' + eform_field_datatype + '"><button style="margin-top:0.5rem" id="' + eform_field_name + '-' + index + '" type="button" onclick="remove_element(this.id)"  class="btn btn-danger btn-sm btn-delete"><i class="far fa-trash-alt"></i></button></div>' + line_separator
            }
            else {
                div_content = '<div id="array_index-' + index + '" class="form-group col-6"><label  for="' + eform_field_name + '">' + eform_field_name + ':' + '</label><span id="span_' + eform_field_name + '" ></span><br><input class="form-control toggle_mode dummy_eform_class" type="' + eform_field_datatype + '"><button style="margin-top:0.5rem" id="' + eform_field_name + '-' + index + '" type="button" onclick="remove_element(this.id)"  class="btn btn-danger btn-sm btn-delete"><i class="far fa-trash-alt"></i></button></div>' + line_separator
            }

            $('#eform_body').append(div_content)
            if (required_flag) {
                document.getElementById('span_' + eform_field_name).classList.add("hg_required")
                // $('#span_' + eform_field_name).html('*')
            }
        });
        $('#eform_details').show()
    }
}


function update_product_specification(product_specification){
    $('#product_spec_main_tbody').empty();
    var prod_spec_main_html = ''
    $.each(product_specification, function (i, item) {
        prod_spec_main_html += '<tr ><td>' + item.product_info_key + '</td><td>' + item.product_info_value + '</td></tr>';
    });
    $('#product_spec_main_tbody').append(prod_spec_main_html);
    document.getElementById('prod_spec_div_id').style.display = 'block';
}
//onclick of upload button display id_data_upload popup and set GLOBAL_ACTION button value
function onclick_upload_button() {
    GLOBAL_ACTION = "product_upload"
    $("#id_popup_tbody").empty();
    $('#id_data_upload').modal('show');
    document.getElementById('id_file_data_upload').value = "";
}

