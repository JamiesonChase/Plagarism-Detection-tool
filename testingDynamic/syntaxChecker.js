    <script type="text/javascript">
    (function worker() {
        $.ajax({
            url: "/data",
            type: "POST",
            data: {},
            success: function(response) {
                var body = document.getElementsByTageName("body")[0];
                
                for (var[v1] of response.map) {
                    
                    var table = document.getElementById("members");
                    
                    var row = table.insertRow(1);
                    var cell1 = row.insertCell(0);
                    var cell2 = row.insertCell(1);
                    let whatever = "abc"
                    cell1.innerHTML = `<a href="${whatever}">${v1}</a>`;
                }
                setTimeout(worker, 1000);
            }
        })
    })();
    
    </script>