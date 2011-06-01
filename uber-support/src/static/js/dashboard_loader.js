function loadDashboard(caption, tableId, pagerId) {
	$(tableId).jqGrid({
		url: '/res/async?op=loadDashboard',
		datatype: 'json',
		colNames: ['Requestor', 'Open time', 'Category', 'Subject'],
		colModel: [
		           {name: 'requestor'},
		           {name: 'submitted_on', formatter: 'date', formatoptions: {srcformat:'ISO8601Long', newformat: 'ShortDate'}},
		           {name: 'category'},
		           {name: 'subject'}
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
	})
}
