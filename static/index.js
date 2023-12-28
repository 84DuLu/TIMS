new gridjs.Grid({
    columns: [
        {id: 'id', hidden: true},
        {id: 'number', name: '编号'},
        {
            id: 'name',
            name: '名称',
            sort: {
                compare: (a, b) => {
                    return a.localeCompare(b, 'zh-Hans-CN');
                }
            }
        },
        {id: 'length', name: '长度'},
        {id: 'province', name: '省份', sort: false},
        {id: 'lane', name: '车道数', sort: false},
        {id: 'year', name: '开通年份'},
        {id: 'highway', name: '公路', sort: false},
        {
            sort: false,
            formatter: (_, row) => gridjs.html(`<a 
            class="btn btn-primary" 
            href="/tunnel/edit/${tunnel_id=row.cells[0].data}" 
            role="button">编辑</a>
            <form class="inline-form" method="post" action="/tunnel/delete/${tunnel_id=row.cells[0].data}">
                <input class="btn btn-danger" type="submit" value="删除" onclick="return confirm('确定删除吗?')">
            </form>`)
        },
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

const head = document.querySelector('.gridjs-head');

const addBtn = document.createElement('a');
addBtn.className = 'btn btn-dark';
addBtn.href = '/tunnel/add';
addBtn.textContent = '添加新条目';
addBtn.style.marginLeft = '1rem';

head.appendChild(addBtn)