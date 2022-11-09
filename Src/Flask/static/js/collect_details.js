var arr = [];//存放应交名单
var len = arr.length;
var arr2 = [];//存放文件名
arr2 = ["wgk.pdf", "wgk.docx", "wgk.xls"];

var tab_list = document.querySelector(".tab_list");
var lis = tab_list.querySelectorAll("li");
var items = document.querySelectorAll(".item");
const x = document.getElementById("list_body");

function idx_str_to_int(idx_str) {
    if (idx_str >= '0' && idx_str <= '9') {
        return parseInt(idx_str);
    }
    return parseInt(idx_str) - 10 + 'a'.charCodeAt();
}

function id_str_transfer(id_str) {
    if (id_str >= '0' && id_str <= '9') {
        return id_str;
    }
    return String.fromCharCode(parseInt(id_str) - 10 + 'a'.charCodeAt());
}

// TODO 获取提交信息更新页面，从 mycollection 页面进入
// function getData() {
//     let tmp_json = JSON.parse(document.getElementById('json_object').innerHTML);
//     let json_length = document.getElementById('json_length').innerHTML;
//     console.log(tmp_json);
//     for (let i = 0; i < json_length; i++) {
//         // ! 未验证正确性
//         addmember(tmp_json[i].submitter_order_idx, tmp_json[i].submitter_name,
//             tmp_json[i].submit_time, tmp_json[i].file_submitted_count, tmp_json[i].file_submitted_list);
//     }
// }

Array.prototype.indexOf = function (val) {
    for (var i = 0; i < this.length; i++) {
        if (this[i] == val) return i;
    }
    return -1;
};
Array.prototype.remove = function (val) {
    var index = this.indexOf(val);
    if (index > -1) {
        this.splice(index, 1);
    }
};

for (var i = 0; i < lis.length; i++) {
    lis[i].setAttribute("index", i);
    lis[i].onclick = function () {
        for (var i = 0; i < lis.length; i++) {
            lis[i].className = "";
        }
        this.className = "current";
        const index = this.getAttribute("index");
        for (var i = 0; i < items.length; i++) {
            items[i].style.display = "none";
        }
        items[index].style.display = "block";
    }
}//实现tab栏切换

// * 添加姓名弹窗
function click0() {
    let popLayer = document.getElementById('popLayer');
    popLayer.style.display = "block";
    let popup = document.getElementById("popup");
    popup.style.display = "block";
}

// * 在 namebox 中添加名字，关闭弹窗
function click1() {
    let popup = document.getElementById("popup");
    popup.style.display = "none";
    addname();
    document.getElementById("textarea").value = "";
    let popLayer = document.getElementById('popLayer');
    popLayer.style.display = "none";
}

function click2() {
    let popup1 = document.getElementById("popup1");
    let del = document.getElementById("return");
    popup1.style.display = "none";
    let popLayer = document.getElementById('popLayer');
    popLayer.style.display = "none";
    del.remove();
}

// * 添加名字
function addname() {
    var str = document.getElementById("textarea").value;
    // * 赋值
    document.getElementById("name_data").value = str;
    if (str != "") {
        var n = str.split(/[\s\n]|\,/);//将 textarea 中字符串以,和换行符切分
        var flag = 0;
        let d1 = document.getElementById("name_box");
        while (flag < n.length) {
            if (n[flag] != "") {
                if (arr.includes(n[flag])) {
                    flag++;
                    continue;
                }
                arr.push(n[flag]);
                let para = document.createElement("div");
                let node1 = document.createElement("div");
                let node2 = document.createTextNode(n[flag]);
                let delbtn = document.createElement("button");
                //生成子节点
                para.className = "paraname";
                para.id = n[flag];
                node1.className = "div1";
                delbtn.className = "del";
                node1.title = n[flag];
                //添加样式和数据,数组n存放名字字符串
                // delbtn.appendChild(document.createTextNode("X"));
                para.appendChild(node1);
                node1.appendChild(node2);
                d1.appendChild(para);
                para.appendChild(delbtn);
                //给子节点添加父节点
                para.onmouseover = function () {
                    delbtn.style.display = "block";
                }//光标移动至相应元素则显示按钮
                para.onmouseout = function () {
                    delbtn.style.display = "none";
                }//光标移动至相应元素外则按钮隐藏
                delbtn.onclick = function () {
                    document.getElementById("hidden-input").value = "delete " + node1.title;
                    arr.remove(node1.title);
                    d1.removeChild(para);
                    document.getElementById("hidden").submit();
                }//点击删除节点
            }
            flag++;
        }
    }
}

function addfile(file_submitted_list) {
    let popup = document.getElementById("return");
    let i = 0;
    while (i < file_submitted_list.length) {
        let para = document.createElement("div");
        para.title = file_submitted_list[i];
        para.className = "filelist";
        popup.appendChild(para);
        para.appendChild(document.createTextNode(para.title));
        i++;
    }
}

//TODO 待添加参数
function addmember(submitter_order_idx, submitter_name, submit_time, file_submitted_count, file_submitted_list) {
    //新建元素节点
    let listmember = document.createElement("div");
    let membername = document.createElement("div");
    let memberdate = document.createElement("div");
    let membernumber = document.createElement("div");
    let membercondition = document.createElement("div");
    // ! 11/08 添加 idx
    let memberid = document.createElement("div");
    // ! 11/08
    //连接节点
    x.appendChild(listmember);
    // ! 11/08
    listmember.appendChild(memberid);
    // ! 11/08
    listmember.appendChild(membername);
    listmember.appendChild(memberdate);
    listmember.appendChild(membernumber);
    listmember.appendChild(membercondition);
    //给节点赋值
    // membername.title = "王广凯";
    membername.title = submitter_name;
    // memberdate.title = "2022-10-01 23:59";
    memberdate.title = submit_time;
    // membernumber.title = "211";
    membernumber.title = file_submitted_count;
    membercondition.title = "查看";
    // ! 11/08 memberid
    memberid.title = id_str_transfer(submitter_order_idx);
    // ! 11/08
    membername.appendChild(document.createTextNode(membername.title));
    // ! 11/08
    memberdate.appendChild(document.createTextNode(memberdate.title));
    membernumber.appendChild(document.createTextNode(membernumber.title));
    membercondition.appendChild(document.createTextNode(membercondition.title));
    listmember.className = "list_member";
    membername.className = "member_name";
    memberdate.className = "member_date";
    membernumber.className = "member_number";
    membercondition.className = "member_condition";
    // ! 11/08
    memberid.style.display = "none";
    // ! 11/08
    membercondition.onclick = function () {
        let popup1 = document.getElementById("popup1");
        popup1.style.display = "block";
        let popLayer = document.getElementById('popLayer');
        popLayer.style.display = "block";
        let wgk = document.getElementById("popup-content");
        let jsx = document.createElement("div");
        jsx.id = "return";
        wgk.appendChild(jsx);
        addfile(file_submitted_list);
    }
}
