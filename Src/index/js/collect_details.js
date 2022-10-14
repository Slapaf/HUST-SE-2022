var arr = [];
var len = arr.length;

var tab_list = document.querySelector(".tab_list");
var lis = tab_list.querySelectorAll("li");
var items = document.querySelectorAll(".item");

for (var i = 0; i < lis.length; i++) {
    lis[i].setAttribute("index", i);
    lis[i].onclick = function () {
        for (var i = 0; i < lis.length; i++) {
            lis[i].className = "";
        }
        this.className = "current";
        var index = this.getAttribute("index");
        for (var i = 0; i < items.length; i++) {
            items[i].style.display = "none";
        }
        items[index].style.display = "block";
    }
}//实现tab栏切换

function click0() {
    var popup = document.getElementById("popup");
    popup.style.display = "block";
}//添加姓名弹窗

function click1() {
    var popup = document.getElementById("popup");
    popup.style.display = "none";
    addname();
    document.getElementById("textarea").value = "";
}//在namebox中添加名字，关闭弹窗

function addname() {
    var str = document.getElementById("textarea").value;
    if (str != "") {
        var n = str.split(/[\s\n]|\,/);//将textarea中字符串以,和换行符切分
        var flag = 0;
        let d1 = document.getElementById("name_box");
        while (flag < n.length) {
            if (!arr.includes(n[flag])) {
                if (n[flag] != "") {
                    arr.push(n[flag]);
                    let para = document.createElement("div");
                    let node1 = document.createElement("div");
                    let node2 = document.createTextNode(n[flag]);
                    let delbtn = document.createElement("button");
                    //生成子节点
                    para.className = "name";
                    node1.className = "div1";
                    delbtn.className = "del";
                    node1.title = n[flag];
                    //添加样式和数据,数组n存放名字字符串
                    delbtn.appendChild(document.createTextNode("X"));
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
                        d1.removeChild(para);
                    }//点击删除节点
                }
            }
            else {
                if (n[flag] != "") {
                    let i = 1;
                    while (arr.includes(n[flag] + "(" + i + ")")) {
                        i++;
                    }
                    n[flag] = n[flag] + "(" + i + ")";
                    arr.push(n[flag]);
                    let para = document.createElement("div");
                    let node1 = document.createElement("div");
                    let node2 = document.createTextNode(n[flag]);
                    let delbtn = document.createElement("button");
                    //生成子节点
                    para.className = "name";
                    node1.className = "div1";
                    delbtn.className = "del";
                    node1.title = n[flag];
                    //添加样式和数据,数组n存放名字字符串
                    delbtn.appendChild(document.createTextNode("X"));
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
                        d1.removeChild(para);
                    }//点击删除节点
                }
            }
            flag++;
        }
    }
}//添加名字