<html>
    <head>
        <style type="text/css">
            ${css}
        </style>
        <title>qutation_order.pdf</title>        
    </head>
    <body>
        %for o in objects:
            <table class="add">
                 <tr>
                    <td width="70%">
                    </br>
                        <b>Shipping address :</b></br>
                        ${ o.partner_id.name }</br>
                        ${ o.address_id.street or '' }</br>
                        ${ o.address_id.city or '' }&nbsp;${ o.address_id.zip or '' }</br>
                        ${ o.address_id.country_id.name or '' }</br>
                        %if (o.address_id.phone):
                            Tel. : ${ o.address_id.phone or '' }</br>
                        %endif
                        %if o.address_id.fax:
                            Fax : ${ o.address_id.fax or '' }</br>
                        %endif
                        %if o.address_id.vat:
                            ${ o.address_id.vat or '' }</br>
                        %endif
                      
                        
                    </td>
                    <td width="30%" colspan="2">
                        ${ o.partner_id.name or '' }
                        ${ o.default_address_id.street or '' }</br>
                        ${ o.default_address_id.city or '' }&nbsp;${ o.default_address_id.zip or '' }</br>
                        ${ o.default_address_id.country_id.name or '' }</br>
                        %if (o.default_address_id.phone):
                            Tel. : ${ o.default_address_id.phone or '' }</br>
                        %endif
                        %if o.default_address_id.fax:
                            Fax : ${ o.default_address_id.fax or '' }</br>
                        %endif
                        %if o.default_address_id.vat:
                            ${ o.default_address_id.vat or '' }
                        %endif
                    </td>
                  </tr>
                  <tr>
                        <td>
                            <b>Invoice address :</b></br>
                            ${ o.partner_id and o.partner_id.property_payment_term.name or ''}</br>
                            ${ o.partner_invoice_id.name or ''}</br>
                            ${ o.partner_invoice_id.street or '' }</br>
                            ${ o.partner_invoice_id.city or '' }&nbsp;${ o.partner_invoice_id.zip or '' }</br>
                            ${ o.partner_invoice_id.country_id.name or '' }</br>
                            %if (o.partner_invoice_id.phone):
                                Tel. : ${ o.partner_invoice_id.phone or '' }</br>
                            %endif
                            %if o.partner_invoice_id.fax:
                                Fax : ${ o.partner_invoice_id.fax or '' }</br>
                            %endif
                            %if o.partner_invoice_id.vat:
                                ${ o.partner_invoice_id.vat or '' }
                            %endif
                       
                        </td>
                  </tr>
            </table>
            <p class="title"> 
            %if  o.state <> 'draft' or '':
                    Repair Quotation N° : ${ o.name }
            %endif
            %if  o.state=='draft' or '' :
                Repair Order N° :  ${ o.name }
            %endif
            </p>
            <table class="basic_table">
                <tr>
                    <td class="25%">
                        <b>${_("Product to Repair")} </b>
                    </td>
                    <td class="25%">
                        <b>${_("Lot Number")}</b>
                    </td>
                    <td class="25%">
                        <b>${_("Guarantee Limit")}</b>
                    </td>
                    <td class="25%">
                        <b>${_("Printing Date")}</b>
                    </td>
                </tr>
                <tr>
                    <td class="25%">
                        ${ o.product_id.name or '' }
                    </td>
                    <td class="25%">
                        ${ o.prodlot_id.name or ' ' }
                    </td>
                    <td class="25%">
                        ${ formatLang(o.guarantee_limit,date = True) }
                    </td>
                    <td class="25%">
                        ${ formatLang(time.strftime('%Y-%m-%d'),date = True)}
                    </td>
                </tr>
            </table>
            </br>
                <table class="list_table">
                    <tr>
                        <td width="57%">
                          ${_("Description")}
                        </td>
                        <td width="10%">
                          ${_("Tax")}
                        </td>
                        <td width="10%" align="right">
                            ${_("Quantity")}
                        </td>
                        <td width="8%" align="right">
                            ${_("Unit Price")}
                        </td>
                        <td width="15%" align="right">
                            ${_("Price")}
                        </td>
                    </tr>
                </table>
                <h3><b>Operation Line(s)</b></h3>
                %for line in o.operations:
                    %if line['to_invoice']==True:
                        <table class="tr_bottom_line_dark_grey">
                            <tr>
                                <td width="57%">
                                    %if line.type == 'add' or '':
                                            (Add)${ line.name }    
                                    %endif
                                    %if line.type == 'remove' or '':
                                        (Remove) ${ line.name }
                                    %endif
                                </td>
                                <td width="10%">
                                    ${ ','.join(map( lambda x: x.name, line.tax_id)) }
                                  </td>
                                  <td width="10%" align="right">
                                    ${ formatLang(line.product_uom_qty) } ${ line.product_uom.name }
                                  </td>
                                  <td width="8%" align="right">
                                    ${ formatLang(line.price_unit) }
                                  </td>
                                  <td width="15%" align="right">
                                    ${ formatLang(line.price_subtotal, currency_obj = o.pricelist_id.currency_id) }
                                  </td>
                            </tr>
                        </table>
                     %endif 
                %endfor
                %if len(o.fees_lines) != 0 :
                        
                     <h3><b>Fees Line(s)</b></h3> 
                     %for fees in o.fees_lines:
                        %if fees.to_invoice==True:
                            <table class="tr_bottom_line_dark_grey">
                                <tr>
                                    <td width="57%">
                                       ${ fees.name }
                                    </td>
                                    <td width="10%">
                                      ${ ','.join(map( lambda x: x.name, fees.tax_id)) }
                                    </td>
                                    <td width="10%" align="right">
                                      ${ formatLang(fees.product_uom_qty) } ${ fees.product_uom.name }
                                    </td>
                                    <td width="8" align="right"> 
                                      ${ formatLang(fees.price_unit) }
                                    </td>
                                    <td width="15%" align="right">
                                      ${ formatLang(fees.price_subtotal, currency_obj = o.pricelist_id.currency_id) }
                                    </td>
                                  </tr>
                            </table>
                        %endif
                     %endfor
                %endif
                <table width="100%">
                    <tr>
                        <td width="70%">
                        </td>
                        <td width="30%">
                            <table class="tr_top">
                                <tr>
                                    <td>
                                      <b>Net Total :</b>
                                    </td>
                                    <td  align="right">
                                       ${ formatLang(o.amount_untaxed, dp='Sale Price', currency_obj=o.pricelist_id.currency_id) }
                                    </td>
                                  </tr>
                                  <tr>
                                    <td>
                                        <b>${_("Taxes:")}</b>
                                    </td>
                                    <td  align="right">
                                        ${ formatLang(o.amount_tax, dp='Account', currency_obj=o.pricelist_id.currency_id) }
                                    </td>
                                  </tr>
                             </table>
                        </td>
                    </tr>
                    <tr>
                        <td width="70%">
                        </td>
                        <td width="30%">
                            <table class="tr_top">
                                <tr>
                                <td><b>
                                    ${_("Total :")}</b>
                                </td>
                                <td align="right"> <b>
                                    ${ formatLang(total(o), dp='Sale Price', currency_obj=o.pricelist_id.currency_id) }</b>
                                </td>
                              </tr>
                            </table>
                        </td>
                    </tr>
                </table>
                <table width="100%">
                    <tr>
                        <td class="td_f12">
                          ${ o.quotation_notes or '' }
                        </td>
                     </tr>
                </table>
              <p style="page-break-after:always">
        </p>
         %endfor
    </body>
</html>