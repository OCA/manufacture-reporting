<!DOCTYPE html SYSTEM "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">

<html xmlns="http://www.w3.org/1999/xhtml">
    <head>
        <style type="text/css">
            ${css}
        </style>
        <title>Production Order.pdf</title>        
    </head>
    <body>
        %for o in objects:
            <table class="title" width="100%">
                    <tr>
                        <td width="100%">
                             <h3><b>${ _('Production Order N°') } : ${o.name}</b></h3>
                        </td>
                    </tr>
            </table>
       
            <table width="100%" class="list_table2">
                <tr>
                    <td width="35%">
                        <b>${ _('Source Document') }</b>
                    </td>
                    <td width="40%">
                        <b>${ _('Product') }</b>
                    </td>
                    <td width="25%">
                        <b>${ _('Quantity') }</b>
                    </td>
                </tr>
            </table>
            <table width="100%" class="list_table2">
                <tr>
                    <td width="35%">
                        ${o.origin or ''}
                    </td>
                    <td width="40%">
                        ${o.product_id and o.product_id.code or ''} ${o.product_id and o.product_id.name or ''}
                    </td>
                    <td width="25%">
                        ${formatLang(o.product_qty)} ${o.product_id and o.product_uom and o.product_uom.name or ''}
                    </td>
                </tr>
            </table>
            <br/>
            
            <table width="100%" class="list_table2">
                <tr>
                    <td width="35%">
                        <b>${ _('Scheduled Date') }</b>
                    </td>
                    <td width="18%">
                        <b>${ _('Printing date') }</b>
                    </td>
                    <td width="22%">
                        <b>${ _('Partner Ref') }</b>
                    </td>
                    <td width="25%">
                        <b>${ _('SO Number') }</b>
                    </td>
                </tr>
            </table>
            <table width="100%" class="list_table2">
                <tr>
                     <td width="35%">
                        ${formatLang(o.date_planned, date_time = True)}
                    </td>
                    <td width="18%">
                        ${formatLang(time.strftime('%Y-%m-%d'),date = True)}
                    </td>
                    <td width="22%">
                        ${'sale_ref' in o._columns.keys() and o.sale_ref or ''}
                    </td>
                    <td width="25%">
                        ${'sale_name' in o._columns.keys() and o.sale_name or ''}
                    </td>
                </tr>
            </table>
            <br/>
            
            %if o.workcenter_lines ==[]:
                
            %else:
                <table  width="100%">
                    <tr>
                        <td style="text-align:left;" width="100%">
                             <h4><b>${ _('Work Orders') }</b></h4>
                        </td>
                    </tr>
                </table>
                <table width="100%" class="list_table2">
                    <tr>
                        <td width="15%">
                            <b>${ _('Sequence') }</b>
                        </td>
                        <td width="30%">
                            <b>${ _('Name') }</b>
                        </td>
                        <td width="30%">
                            <b>${ _('WorkCenter') }</b>
                        </td>
                        <td width="12%">
                            <b>${ _('No. Of Cycles') }</b>
                        </td>
                        <td width="13%">
                            <b>${ _('No. Of Hours') }</b>
                        </td>
                    </tr>
                </table>
                %for line2 in o.workcenter_lines:
                    <table width="100%" class="list_table2">
                        <tr>
                            <td width="15%">
                                ${str(line2.sequence)}
                            </td>
                            <td width="30%">
                                ${line2.name}
                            </td>
                            <td width="30%">
                                ${line2.workcenter_id and line2.workcenter_id.name or ''}
                            </td>
                            <td width="12%">
                                ${formatLang(line2.cycle)}
                            </td>
                            <td width="13%">
                                ${formatLang(line2.hour)}
                            </td>
                        </tr>
                    </table><br/>
                %endfor
            %endif
            
            <table class="title" width="100%">
                   <tr>
                       <td width="100%">
                            <h3>${ _('Bill Of Material') }</h3>
                       </td>
                   </tr>
           </table>
           <table style="border-bottom:2px solid black;font-family: Helvetica; font-size:11px;" width="100%" >
                <tr>
                    <td style="text-align:left; " width="55%">
                        <b>${ _('Product') }</b>
                    </td>
                    <td style="text-align:right;" width="10%">
                        <b>${ _('Quantity') }</b>
                    </td>
                    <td style="text-align:center;" width="20%">
                        <b>${ _('Source Location') }</b>
                    </td>
                    <td style="text-align:center;" width="15%">
                        <b>${ _('Destination Location') }</b>
                    </td>
                </tr>
            </table>
            
             %if o.move_lines ==[]:
             
             %else:
                <table   style="font-family: Helvetica; font-size:11px;" width="100%">
                   <tr>
                       <td  width="100%">
                            <b>${ _('Products to Consume') }</b>
                       </td>
                   </tr>
                </table>
                %for line in o.move_lines:
                    <table width="100%" class="list_table">
                        <tr>
                            <td style="text-align:left;" width="55%">
                                ${line.product_id and line.product_id.code or ''} ${line.product_id and line.product_id.name or ''} 
                            </td>
                            <td style="text-align:right;" width="10%">
                                ${formatLang( line.product_qty)} ${line.product_uom and line.product_uom.name or ''}
                            </td>
                            <td style="text-align:center;"width="20%">
                                ${line.location_id and line.location_id.name or ''}
                            </td>
                            <td style="text-align:center;"width="15%">
                                ${line.location_dest_id and line.location_dest_id.name or ''}
                            </td>
                        </tr>
                    </table>
                %endfor
             %endif
               
             %if o.move_lines2 ==[]:
             
             %else:
                 <table class="title" width="100%">
                    <tr>
                        <td width="100%">
                            <h5><b>${ _('Consumed Products') }</b></h5>
                       </td>
                   </tr>
                 </table>
                 %for line2 in o.move_lines2:
                    <table width="100%" class="list_table1">
                        <tr>
                            <td style="text-align:left;"width="55%">
                                ${line2.product_id and line2.product_id.code or ''} ${line2.product_id and line2.product_id.name or ''} 
                            </td>
                            <td style="text-align:right;"width="10%">
                                ${formatLang( line2.product_qty)} ${line2.product_uom and line2.product_uom.name or ''}
                            </td>
                            <td style="text-align:center;"width="20%">
                                ${line2.location_id and line2.location_id.name or ''}
                            </td>
                            <td style="text-align:center;"width="15%">
                                ${line2.location_dest_id and line2.location_dest_id.name or ''}
                            </td>
                        </tr>
                    </table>
                %endfor
             %endif
             <p style="page-break-after:always"></p>
        %endfor 
    </body>
</html>