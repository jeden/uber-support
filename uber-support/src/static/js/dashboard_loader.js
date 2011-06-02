function loadDashboard(caption, tableId, pagerId, status) {
	var table = $(tableId)
	table.jqGrid({
		url: '/res/async?op=loadDashboard&status=' + status,
		datatype: 'json',
		colNames: ['Requestor', 'Open time', 'Category', 'Subject'],
		colModel: [
		           {name: 'requestor'},
		           {name: 'submitted_on', align: 'center', formatter: 'date', formatoptions: {srcformat:'ISO8601Long', newformat: 'ShortDate'}},
		           {name: 'category'},
		           {name: 'subject', sortable: false}
		],
		rowNum: 25,
		rowList: [25, 50, 100],
		pager: pagerId,
		sortName: 'rank',
		viewrecords: true,
		caption: caption,
		autowidth: true,
		height: '500px',
		jsonReader: {
			repeatitems: false
		},
		toolbar: [true, 'top'],
	})
	
	table.before("<a href='#' onclick=\"$('" + tableId + "').setGridParam({sortname: 'rank'}).trigger('reloadGrid')\">Sort by rank</a>");
}

function sortDashboard(tableId, column) {
	$(tableId).sortGrid(column, true);
}
