<script type="text/javascript">
    (function worker() {
        $.get('/data', function(data){
            $('#time').html(data);
            for (let i = 0; i < 15; i++) {
                var table = document.getElementById("members");
                var row = table.insertRow(0);
                var cell1 = row.insertCell(0);
                var cell2 = row.insertCell(1);
                let whatever = "abc"
                cell1.innerHTML = `<a href="${whatever}">${i}</a>`;
            }
            
        
            
            setTimeout(worker, 1000);
        });
    })();
    
    </script>










<script type="text/javascript" src="http://code.jquery.com/jquery-1.8.0.min.js"></script>
    <script type="text/javascript">
    (function worker() {
        $.get('/data', function(data){
            let a = $('#time').html(data);
            for (let i = 0; i < 15; i++) {
                var table = document.getElementById("members");
                var row = table.insertRow(0);
                var cell1 = row.insertCell(0);
                var cell2 = row.insertCell(1);
                let whatever = "abc"
                cell1.innerHTML = `<a href="${whatever}">${a[0]}</a>`;
            }
            
        
            
            setTimeout(worker, 1000);
        });
    })();
    
    </script>























<script type="text/javascript" src="https://ajax.googleapis.com/ajax/libs/jquery/3.2.1/jquery.min.js"></script>
    <script type="text/javascript">
    (function worker() {
        $.ajax({
            url: "/data",
            type: "POST",
            data: {},
            success: function(response) {
                
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