new gridjs.Grid({
    columns: [
        {id: 'id', hidden: true},
        {id: 'tunnel_name', name: '隧道名称', sort: false},
        {id: 'check_program', name: '检查项目', sort: false},
        {id: 'check_time', name: '检查时间'},
        {id: 'check_name', name: '检查公司', sort: false},
        {id: 'enter_man', name: '录入人员', sort: false},
        {id: 'conclusion', name: '检查结论', sort: false},
        {
            sort: false,
            formatter: (_, row) => gridjs.html(`<a 
            class="btn btn-primary" 
            href="/maintain/edit/${maintain_id=row.cells[0].data}" 
            role="button">编辑</a>
            <form class="inline-form" method="post" action="/maintain/delete/${maintain_id=row.cells[0].data}">
                <input class="btn btn-danger" type="submit" value="删除" onclick="return confirm('确定删除吗?')">
            </form>`)
        },
    ],
    server: {
        url: '/api/data2',
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
addBtn.href = '/maintain/add';
addBtn.textContent = '添加新条目';
addBtn.style.marginLeft = '1rem';

head.appendChild(addBtn)