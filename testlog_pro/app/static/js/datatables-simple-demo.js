window.addEventListener('DOMContentLoaded', event => {
    // Simple-DataTables
    // https://github.com/fiduswriter/Simple-DataTables/wiki

    const datatablesSimple = document.getElementById('datatablesSimple');
    if (datatablesSimple) {
        new simpleDatatables.DataTable(
            datatablesSimple,
            {
                order: [[0, 'asc']],
                layout: {
                    top: "{search}{info}",
                    bottom: "{select}{pager}"
                },
                fixedHeader: true,
            },
        );
    }

    const datatablesSimple1 = document.getElementById('datatablesSimple1');
    if (datatablesSimple1) {
        new simpleDatatables.DataTable(
            datatablesSimple1,
            {
                fixedHeader: true,
                autoWidth: true,
                layout: {
                    top: "",
                    bottom: "{select}{pager}"
                },
            },
        );
    }

    const child_table = document.getElementById('child_table');
    if (child_table) {
        new simpleDatatables.DataTable(
            child_table,
            {
                fixedHeader: true,
                layout: {
                    top: "",
                    bottom: "{select}{pager}"
                },
            },
        );
    }

    const simpleTable = document.getElementById('simpleTable');
    if (simpleTable) {
        new simpleDatatables.DataTable(
            simpleTable,
            {
                fixedHeader: true,
                layout: {
                    top: "",
                    bottom: ""
                },
            },
        );
    }

    const simpleTable1 = document.getElementById('simpleTable1');
    if (simpleTable1) {
        new simpleDatatables.DataTable(
            simpleTable1,
            {
                fixedHeader: true,
                layout: {
                    top: "",
                    bottom: ""
                },
            },
        );
    }

});
