new gridjs.Grid({
    columns: [
        {id: 'number', name: '编号'},
        {id: 'name', name: '名称'},
        {id: 'length', name: '长度'},
        {id: 'province', name: '省份', sort: false},
        {id: 'lane', name: '车道数', sort: false},
        {id: 'year', name: '开通年份'},
        {id: 'highway', name: '公路', sort: false},
    ],
    server: {
        url: '/api/data',
        then: results => results.data,
    },
    language: {
        search: {
            placeholder: "输入关键字..."
        },
        sort: {
            sortAsc: "升序排列",
            sortDesc: "降序排列"
        },
        pagination: {
            previous: "上一页",
            next: "下一页",
            navigate: function(e, r) {
                return "第" + e + "页，共" + r + "页"
            },
            page: function(e) {
                return "第" + e + "页"
            },
            showing: "第",
            of: "到",
            to: "条记录，共",
            results: "条"
        },
        loading: "玩命加载中...",
        noRecordsFound: "没找到匹配的项",
        error: "获取数据时发生了错误"
    },
    search: true,
    sort: true,
    pagination: true,
    }).render(document.getElementById('table'));