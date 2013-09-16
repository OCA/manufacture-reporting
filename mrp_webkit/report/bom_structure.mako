<!DOCTYPE html SYSTEM "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">

<html xmlns="http://www.w3.org/1999/xhtml">
    <head>
        <style type="text/css">
            ${css}
        </style>
        <title>BOM Structure.pdf</title>        
    </head>
    <body>
       <table  width="100%">
            <tr>
                <td style="text-align:center;">
                    <h2><b>${ _('BOM Structure') }  </b></h2>
                </td>
            </tr>
       </table>
            
       <table width="100%" class="basic_table">
            <tr >
                <td style="text-align:left;" width="35%"><b>${ _('BOM Name') }</b></td>
                <td style="text-align:left;" width="35%"><b>${ _('Product Name') }</b></td>
                <td style="text-align:right;" width="15%"><b>${ _('Quantity') }<b></td>
                <td style="text-align:center;" width="15%"><b>${ _('BOM Ref') }</b></td>
            </tr>
       </table>
       %for o in objects:
            <table width="100%" class="list_table1">
                <tr >
                    <td style="text-align:left;" width="35%"><b>
                        ${o.name}</b>
                    </td>
                    <td style="text-align:left;" width="35%"><b>
                       [ ${(o.product_id.default_code) or removeParentNode('font')}] ${o.product_id.name}</b>
                    </td>
                    <td style="text-align:right;" width="15%"><b>
                        ${o.product_qty} ${o.product_uom.name}</b>
                    </td>
                    <td style="text-align:center;" width="15%"><b>
                        ${o.code or ''}</b>
                    </td><br/>
                </tr>
            </table>
            
            %for l in get_children(o.bom_lines):
                <table width="100%" class="list_table">
                    <tr>
                        <td style="text-align:left ; padding-left:10px" width="35%" class="cell_extended_gray">
                            <font color="white" >${'... '*(l['level'])}</font> - ${l['name']}
                        </td>
                        <td style="text-align:left;" width="35%" class="cell_extended_gray">
                            ${ (l['pcode']) or '' } ${l['pname']}
                        </td>
                        <td style="text-align:right;" width="15%" class="cell_extended_gray">
                            ${l['pqty']} ${l['uname']}
                        </td>
                        <td style="text-align:center;" width="15%" class="cell_extended_gray">
                            ${l['code'] or ''}
                        </td>
                   </tr>
              </table>
           %endfor
           </br>
      %endfor
</body>
</html>