const x = document.getElementById("list_body");

function getData() {
    let tmp_json = JSON.parse(document.getElementById('json_object').innerHTML);
    let json_length = document.getElementById('json_length').innerHTML;
    for (let i = 0; i < json_length; i++) {
        addmember(tmp_json[i].collection_title, tmp_json[i].username, tmp_json[i].collection_status, tmp_json[i].submit_count, tmp_json[i].deadline);
    }
}

// collection_title, username, collection_status, submit_count, time_before_ddl
function addmember(collection_title, username, collection_status, submit_count, deadline) {
    // let collection_title = document.getElementById('data-id').getAttribute('collection_title')
    // let username = document.getElementById('data-id').getAttribute('username')
    // let collection_status = document.getElementById('data-id').getAttribute('collection_status')
    // let submit_count = document.getElementById('data-id').getAttribute('submit_count')
    // let time_before_ddl = document.getElementById('data-id').getAttribute('time_before_ddl')
    //新建元素节点
    let listmember = document.createElement("div");
    let membertitle = document.createElement("div");
    let membername = document.createElement("div");
    let membercondition = document.createElement("div");
    let membertimes = document.createElement("div");
    let memberdate = document.createElement("div");
    let memberoperate = document.createElement("div");
    let op1 = document.createElement("div");
    let op2 = document.createElement("div");
    let op3 = document.createElement("div");
    let op4 = document.createElement("div");
    let op5 = document.createElement("div");
    //连接节点
    x.appendChild(listmember);
    listmember.appendChild(membertitle);
    listmember.appendChild(membername);
    listmember.appendChild(membercondition);
    listmember.appendChild(membertimes);
    listmember.appendChild(memberdate);
    listmember.appendChild(memberoperate);
    memberoperate.appendChild(op1);
    memberoperate.appendChild(op2);
    memberoperate.appendChild(op3);
    memberoperate.appendChild(op4);
    memberoperate.appendChild(op5);
    //给节点赋值
    // membertitle.title = "CS2003软工作业收集";//! 更改为membertitle的值
    // membername.title = "王广凯";//! 更改为membername的值
    // membercondition.title = "进行中";//! 更改为membercondition的值(只能填"进行中"和"已截止"！！！)
    // membertimes.title = "10份";//! 更改为membertimes的值
    // memberdate.title = "2022-10-01 23:59";//! 更改为memberdate的值
    membertitle.title = collection_title;//! 更改为membertitle的值
    membername.title = username;//! 更改为membername的值
    membercondition.title = collection_status;//! 更改为membercondition的值(只能填"进行中"和"已截止"！！！)
    membertimes.title = submit_count + "份";//! 更改为membertimes的值
    memberdate.title = deadline;//! 更改为memberdate的值
    membertitle.appendChild(document.createTextNode(membertitle.title));
    membername.appendChild(document.createTextNode(membername.title));
    membercondition.appendChild(document.createTextNode(membercondition.title));
    membertimes.appendChild(document.createTextNode(membertimes.title));
    memberdate.appendChild(document.createTextNode(memberdate.title));
    op1.appendChild(document.createTextNode("分享"));
    op2.appendChild(document.createTextNode("统计"));
    op4.appendChild(document.createTextNode("复制"));
    if (membercondition.title == "进行中") {
        op3.appendChild(document.createTextNode("编辑"));
        op5.appendChild(document.createTextNode("停止"));
        membercondition.style.color = "green";
    }
    else {
        op3.appendChild(document.createTextNode("重启"));
        op5.appendChild(document.createTextNode("删除"));
        membertitle.style.color = "gray";
        membername.style.color = "gray";
        membercondition.style.color = "gray";
        membertimes.style.color = "gray";
        memberdate.style.color = "gray";
    }
    //给节点添加样式
    listmember.className = "list_member";
    membertitle.className = "member_title";
    membername.className = "member_name";
    membercondition.className = "member_condition";
    membertimes.className = "member_times";
    memberdate.className = "member_date";
    memberoperate.className = "member_operate";
    op1.className = "operate";
    op2.className = "operate";
    op3.className = "operate";
    op4.className = "operate";
    op5.className = "operate";
    //添加点击事件
    membertitle.onclick = function () {
        //!此处需添加参数，跳转对应收集详情界面
        window.location.href = 'collection_details.html';
    }
    membername.onclick = function () {
        //!此处需添加参数，跳转对应收集详情界面
        window.location.href = 'collection_details.html';
    }
    membercondition.onclick = function () {
        //!此处需添加参数，跳转对应收集详情界面
        window.location.href = 'collection_details.html';
    }
    membertimes.onclick = function () {
        //!此处需添加参数，跳转对应收集详情界面
        window.location.href = 'collection_details.html';
    }
    memberdate.onclick = function () {
        //!此处需添加参数，跳转对应收集详情界面
        window.location.href = 'collection_details.html';
    }
    op1.onclick = function () {
        //分享按钮
        let x = document.getElementById("box");
        document.getElementById("link").innerText = "https://www.baidu.com";//!此处修改为收集链接
        let popLayer = document.getElementById('popLayer');
        popLayer.style.width = "100%";
        popLayer.style.height = "100%";
        popLayer.style.display = "block";
        x.style.display = "block";
    }
    op2.onclick = function () {
        //!此处需添加参数，跳转对应收集详情界面
        //统计按钮
        window.location.href = 'collection_details.html';
    }
    op3.onclick = function () {
        //!此处需添加参数，跳转对应收集详情界面
        if (membercondition.title == "进行中") {
            //编辑按钮
            window.location.href = 'file_collecting.html';
        }
        else {
            //重启按钮
            window.location.href = 'file_collecting.html';
        }
    }
    op4.onclick = function () {
        //!此处需添加参数，跳转对应收集详情界面
        //复制按钮
        window.location.href = 'file_collecting.html';
    }
    op5.onclick = function () {
        if (membercondition.title == "进行中") {
            //停止按钮
            op3.innerHTML = "重启";
            op5.innerHTML = "删除";
            membertitle.style.color = "gray";
            membername.style.color = "gray";
            membercondition.style.color = "gray";
            membertimes.style.color = "gray";
            memberdate.style.color = "gray";
            membercondition.title = "已截止";
            membercondition.innerHTML = "已截止";
        }
        else {
            //删除按钮
            x.removeChild(listmember);
        }
    }
}

function closebox() {
    let x = document.getElementById("box");
    x.style.display = "none";
    let popLayer = document.getElementById('popLayer');
    popLayer.style.display = "none";
}

getData();