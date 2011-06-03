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
		onSelectRow: function(rowid, status) { viewRequest('#dialog', rowid); },
		toolbar: [true, 'top'],
	})
	
	table.before("<a href='#' onclick=\"$('" + tableId + "').setGridParam({sortname: 'rank'}).trigger('reloadGrid')\">Sort by rank</a>");
}

function sortDashboard(tableId, column) {
	$(tableId).sortGrid(column, true);
}

function viewRequest(dialogId, requestId) {
	if (requestId) {
		$(dialogId).dialog({
			autoOpen: false,
			minHeight: 300,
			minWidth: 500,
			modal: true,
			title: 'View Request',
			open: function(event, ui) {
				$.ajax({
					url: '/res/async/request/view/id/' + requestId,
					cache: false,
					success: function(html) {
						$(dialogId).html(html);
					}
				});
			},
			close: function(event, ui) {
				$(dialogId).html('Loading...');
			}
		});
		
		$(dialogId).dialog('open');
	}
}