<!doctype html>
<html>
<head>
    <title>FFRK Characters English</title>
    <link rel="stylesheet" href="https://cdn.datatables.net/1.10.7/css/jquery.dataTables.css">
    <script src="https://code.jquery.com/jquery-1.11.1.min.js"></script>
    <script src="https://cdn.datatables.net/1.10.7/js/jquery.dataTables.min.js"></script>
</head>
<body>
    <div id="table_div">
        <table cellpadding="0" cellspacing="0" border="0" class="display" id="char-table">
        </table>
    </div>
    <script>
        var charData = [
            {{ data | join(',')}}
        ];
        $(document).ready(function() {
        $('#char-table').dataTable({
            'data': charData,
            'columns': [
                {'title': 'Name', 'type': 'html'},
                {'title': 'Game'},
                {%- for ct in col_titles %}
                {'title': '{{ct}}', 'type': 'num', 'searchable': false},
                {%- endfor %}
            ],
            'order': [0, 'asc'],
            'paging': false
          });
        });
    </script>
</body>
</html>
