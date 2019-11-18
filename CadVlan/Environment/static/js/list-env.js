$(document).ready(function() {

	oTable = $("#envtable").dataTable({
		"aaSorting": [],
		"bJQueryUI": true,
		"sPaginationType": "full_numbers",
		"aoColumnDefs": [{ "bSortable": false, "aTargets": [ 5, 6] }]
	});
});