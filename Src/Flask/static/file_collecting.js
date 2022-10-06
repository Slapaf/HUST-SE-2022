const ul = document.querySelector(".main>ul");
const lis = ul.getElementsByTagName("li");
// const li1 = lis[0];
// const li2 = lis[1];
const rem = ul.getElementsByClassName("removeTopic");
// const rem1 = rem[0];
// const rem2 = rem[1];
const op_name = document.getElementById("op-name");
const op_file = document.getElementById("op-file");
const op_sno = document.getElementById("op-sno");
const btn_for_add = document.querySelector("#btn-for-add");
const popup = document.querySelector(".popup");
const cancel = document.querySelector(".popup-header>span");

//点击“添加题目”按钮，弹出弹窗
btn_for_add.onclick = () => {
  popup.classList.toggle("show");
};

//点击“x"，取消选择
cancel.onclick = () => {
  btn_for_add.onclick();
};

// rem1.addEventListener("click", () => {
//   ul.removeChild(li1);
// });
// rem2.addEventListener("click", () => {
//   ul.removeChild(li2);
// });

function addLoadEvent(func) {
  var oldonload = window.onload;
  if (typeof window.onload != "function") {
    window.onload = func;
  } else {
    window.onload = function () {
      oldonload();
      func();
    };
  }
}

op_name.onclick = () => {
  //新建一些元素节点
  let newli = document.createElement("li");
  let newh1 = document.createElement("h1");
  let newinput_topic = document.createElement("input");
  newinput_topic.className = "input-topic";
  newinput_topic.type = "text";
  newinput_topic.value = "姓名";
  let newinput_content = document.createElement("input");
  newinput_content.className = "input-content";
  newinput_content.type = "text";
  newinput_content.disabled = "disabled";
  newinput_content.placeholder = "此项由提交者填写";
  let newbtn = document.createElement("button");
  newbtn.className = "removeTopic";
  //把各元素节点插到其父元素下
  newbtn.appendChild(document.createTextNode("删除题目"));
  newh1.appendChild(newinput_topic);
  newli.appendChild(newh1);
  newli.appendChild(newinput_content);
  newli.appendChild(newbtn);
  ul.appendChild(newli);
  btn_for_add.onclick();
  //更新checkbox;
  for_checkbox();
  //给新增的题目添加删除事件
  newbtn.addEventListener("click", () => {
    ul.removeChild(newli);
    //删除对应复选框
    for_checkbox();
  });

  //实时监听内容变化，并且改变复选框中的值
  newinput_topic.onchange = () => {
    alert("changed!");
  };
};

op_sno.onclick = () => {
  //新建一些元素节点
  let newli = document.createElement("li");
  let newh1 = document.createElement("h1");
  let newinput_topic = document.createElement("input");
  newinput_topic.className = "input-topic";
  newinput_topic.type = "text";
  newinput_topic.value = "学号";
  let newinput_content = document.createElement("input");
  newinput_content.className = "input-content";
  newinput_content.type = "text";
  newinput_content.disabled = "disabled";
  newinput_content.placeholder = "此项由提交者填写";
  let newbtn = document.createElement("button");
  newbtn.className = "removeTopic";
  //把各元素节点插到其父节点下
  newbtn.appendChild(document.createTextNode("删除题目"));
  newh1.appendChild(newinput_topic);
  newli.appendChild(newh1);
  newli.appendChild(newinput_content);
  newli.appendChild(newbtn);
  ul.appendChild(newli);
  //更新checkbox
  for_checkbox();
  btn_for_add.onclick();
  //给新增的题目添加删除事件
  newbtn.addEventListener("click", () => {
    ul.removeChild(newli);
    //删除对应复选框
    for_checkbox();
  });
};

op_file.onclick = () => {
  //新建一些元素节点
  let newli = document.createElement("li");
  let newh1 = document.createElement("h1");
  let newinput_topic = document.createElement("input");
  newinput_topic.className = "input-topic";
  newinput_topic.type = "text";
  newinput_topic.value = "文件";
  let newselect = document.createElement("div");
  newselect.className = "selectTopic";
  let newinput_content = document.createElement("input");
  newinput_content.className = "input-content";
  newinput_content.disabled = "disabled";
  newinput_content.type = "file";
  let newbtn = document.createElement("button");
  newbtn.className = "removeTopic";
  //把各元素节点插到其父节点下
  newbtn.appendChild(document.createTextNode("删除题目"));
  newh1.appendChild(newinput_topic);
  newli.appendChild(newh1);
  //维护复选框
  updateCheckbox(newselect);
  newli.appendChild(newselect);
  newli.appendChild(newinput_content);
  newli.appendChild(newbtn);
  ul.appendChild(newli);
  btn_for_add.onclick();
  //给新增的题目添加删除事件
  newbtn.addEventListener("click", () => {
    ul.removeChild(newli);
  });
};

//维护复选框：根据已有的题目动态增加/修改复选框
function updateCheckbox(selectBox) {
  let len=selectBox.children.length;
  for(let i=0;i<len;i++) {
    selectBox.children[0].remove();
  }
  for (let i = 0; i < lis.length; i++) {
    let input_topic = lis[i].getElementsByClassName("input-topic")[0];
    let input_content = lis[i].getElementsByClassName("input-content")[0];
    if (input_content.type === "file") continue;
    let newcheckbox = document.createElement("input");
    let newspan = document.createElement("span");
    newcheckbox.type = "checkbox";
    newspan.appendChild(document.createTextNode(input_topic.value));
    selectBox.appendChild(newcheckbox);
    selectBox.appendChild(newspan);
  }
}

function for_checkbox() {
  for (let i = 0; i < lis.length; i++) {
    let input_content = lis[i].getElementsByClassName("input-content")[0];
    if (input_content.type === "file") {
      updateCheckbox(lis[i].getElementsByClassName("selectTopic")[0]);
    }
  }
}

addLoadEvent(op_name.onclick);
addLoadEvent(op_file.onclick);
