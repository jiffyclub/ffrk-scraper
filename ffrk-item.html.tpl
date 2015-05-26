<!doctype html>
<html>
<head>
    <meta charset="utf-8">
    <title>FFRK Items {{sub | upper}}</title>
    <link rel="stylesheet" href="https://cdn.datatables.net/1.10.7/css/jquery.dataTables.css">
    <script src="https://code.jquery.com/jquery-1.11.1.min.js"></script>
    <script src="https://cdn.datatables.net/1.10.7/js/jquery.dataTables.min.js"></script>
</head>
<body>
    <div id="table_div">
        <table cellpadding="0" cellspacing="0" border="0" class="display" id="item-table">
        </table>
    </div>
    <script>
        var itemData = [
            {{ data | join(',')}}
        ];
        $(document).ready(function() {
        $('#item-table').dataTable({
            'data': itemData,
            'columns': [
                {
                    'title': '',
                    'type': 'html',
                    'searchable': false,
                    'orderable': false
                },
                {'title': 'Name', 'type': 'html'},
                {'title': 'Type'},
                {'title': 'Rarity', 'type': 'num'},
                {'title': 'Max Attack', 'type': 'num', 'searchable': false},
                {'title': 'Max Defense', 'type': 'num', 'searchable': false},
            ],
            'order': [1, 'asc'],
            'paging': false
          });
        });
    </script>
</body>
</html>
