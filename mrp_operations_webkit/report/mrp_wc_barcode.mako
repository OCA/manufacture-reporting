<html>
    <head>
        <style type="text/css" media="screen">
              body {
                    font-family:Times New Roman;
                    width:"100%"
                    padding-top:15%;
                    padding-bottom:15%;
                    padding-left:15%;
                    padding-right:15%;
                }
               .barcode39 {
                    font-family: "wasp 39 m";
                    font-size: 36pt;
                    height:50px;
                    text-align:left;
                    padding-bottom:0px;
                    padding-left:10px;
                }
         </style>       
    </head>
<body>
    %for o in objects:
        </br></br>
        <table width="100%">
                <tr>
                    <td width="25%">
                    </td>
                    <td align="center" style="background-color:lightgrey ;border:1.8px solid black;width:50%;font-size:10px;padding-bottom:0px;height=100%;">
                        ${ str(o.name) }
                        </br></br></br></br></br></br></br></br></br>
                        </br>
                        </br>
                        </br>
                        <%
                            id = generate_barcode('ID'+str(o.id))
                        %>
                        <p class="barcode39">
                        <img src='${id}' height="50px" width="130px"/>
                        </p>  
                    </td>
                    <td width="25%">
                    </td>    
                </tr>
            </table>
            <p style="page-break-after:always;"></p>
      %endfor
</body>
</html>

