const ul = document.querySelector(".main>ul");
const lis = ul.getElementsByTagName("li");
const rem = ul.getElementsByClassName("removeTopic");
const op_name = document.getElementById("op-name");
const op_file = document.getElementById("op-file");
const op_sno = document.getElementById("op-sno");
const op_radio = document.getElementById("op-radio");
const btn_for_add = document.querySelector("#btn-for-add");
const popup = document.querySelector(".popup");
const cancel = document.querySelector(".popup-header>span");
var tnum = 1;
let dragElement = null; //存放拖拽的元素

// 提交按钮
// const btn_for_submit = document.getElementById("submit")

var question_id = 0;

//点击“添加题目”按钮，弹出弹窗
btn_for_add.onclick = () => {
  popup.classList.toggle("show");
};

//点击“x"，取消选择
cancel.onclick = () => {
  btn_for_add.onclick();
};

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
  //TODO 增加 id 属性
  newli.id = (++question_id).toString();
  //TODO 增加 name 属性
  newinput_topic.name = "question_name"+(tnum++);
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
  for_checkbox("add", newli.id, newinput_topic.value);
  //给新增的题目添加删除事件
  newbtn.addEventListener("click", () => {
    //删除对应复选框
    for_checkbox("remove", newli.id, newinput_topic.value);
    ul.removeChild(newli);
  });
  //实时监听内容变化，并且改变复选框中的值
  newinput_topic.onchange = () => {
    for_checkbox("modify", newli.id, newinput_topic.value);
  };
  //添加拖拽效果
  // newli.draggable = "true";
  // newli.ondragstart = onDragStart;
  // newli.ondragover = onDragOver;
  // newli.ondrop = onDrop;
};

op_sno.onclick = () => {
  //新建一些元素节点
  let newli = document.createElement("li");
  let newh1 = document.createElement("h1");
  let newinput_topic = document.createElement("input");
  newinput_topic.className = "input-topic";
  //TODO 增加 id 属性
  newli.id = (++question_id).toString();
  //TODO 增加 name 属性
  newinput_topic.name = "question_sno";
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
  for_checkbox("add", newli.id, newinput_topic.value);
  btn_for_add.onclick();
  //给新增的题目添加删除事件
  newbtn.addEventListener("click", () => {
    //删除对应复选框
    for_checkbox("remove", newli.id, newinput_topic.value);
    ul.removeChild(newli);
  });
  //实时监听内容变化，并且改变复选框中的值
  newinput_topic.onchange = () => {
    for_checkbox("modify", newli.id, newinput_topic.value);
  };
  //添加拖拽效果
  // newli.draggable = "true";
  // newli.ondragstart = onDragStart;
  // newli.ondragover = onDragOver;
  // newli.ondrop = onDrop;
};

op_file.onclick = () => {
  //新建一些元素节点
  let newli = document.createElement("li");
  let newh1 = document.createElement("h1");
  let newinput_topic = document.createElement("input");
  newinput_topic.className = "input-topic";
  //TODO 增加 id 属性
  newli.id = (++question_id).toString();
  //TODO 增加 name 属性
  newinput_topic.name = "question_file";
  newinput_topic.type = "text";
  newinput_topic.value = "文件";
  let newspan = document.createElement("span");
  newspan.appendChild(document.createTextNode("重命名规则："));
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
  newli.appendChild(newspan);
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
  //添加拖拽效果
  // newli.draggable = "true";
  // newli.ondragstart = onDragStart;
  // newli.ondragover = onDragOver;
  // newli.ondrop = onDrop;
};

//当增加一个“文件”题目时，调用此函数
function updateCheckbox(selectBox) {
  // let len = selectBox.children.length;
  // for (let i = 0; i < len; i++) {
  //     selectBox.children[0].remove();
  // }
  for (let i = 0; i < lis.length; i++) {
    let input_topic = lis[i].getElementsByClassName("input-topic")[0];
    let input_content = lis[i].getElementsByClassName("input-content")[0];
    if (!input_content) continue;
    if (input_content.type === "file") continue;
    let newcheckbox = document.createElement("input");
    let newspan = document.createElement("span");
    newcheckbox.type = "checkbox";
    //设为同一id
    newcheckbox.id = lis[i].id;
    newcheckbox.name = "checked_topic";
    newcheckbox.value = input_topic.value;
    newspan.appendChild(document.createTextNode(input_topic.value));
    selectBox.appendChild(newcheckbox);
    selectBox.appendChild(newspan);
  }
}

//修改复选框中的内容
//当有题目的增加/删除/修改时，调用此函数
//option有三种取值："add","remove","modify"
function for_checkbox(option, id, value) {
  for (let i = 0; i < lis.length; i++) {
    let input_content = lis[i].getElementsByClassName("input-content")[0];
    if (!input_content) continue;
    if (input_content.type === "file") {
      let selectBox = lis[i].getElementsByClassName("selectTopic")[0];
      let childrenLength = selectBox.children.length;
      if (option === "add") {
        //新增
        let newcheckbox = document.createElement("input");
        let newspan = document.createElement("span");
        newcheckbox.type = "checkbox";
        //设为同一id
        newcheckbox.id = id;
        //给复选框增添 name和 value
        newcheckbox.name = "checked_topic";
        newcheckbox.value = value;
        newspan.appendChild(document.createTextNode(value));
        selectBox.appendChild(newcheckbox);
        selectBox.appendChild(newspan);
      } else if (option === "remove") {
        //删除
        for (let j = 0; j < selectBox.children.length; j++) {
          if (selectBox.children[j].id && selectBox.children[j].id === id) {
            selectBox.removeChild(selectBox.children[j].nextSibling);
            selectBox.removeChild(selectBox.children[j]);
          }
        }
      } else if (option === "modify") {
        //修改
        for (let j = 0; j < selectBox.children.length; j++) {
          if (selectBox.children[j].id && selectBox.children[j].id === id) {
            selectBox.children[j].nextSibling.innerHTML = value;
            selectBox.children[j].value = value;
          }
        }
      } else {
        //交换位置
        let drag = null,
          drop = null,
          drag_txt = null;
        for (let j = 0; j < selectBox.children.length; j++) {
          if (selectBox.children[j].id && selectBox.children[j].id === id) {
            drag = selectBox.children[j];
            drag_txt = selectBox.children[j].nextSibling;
          } else if (
            selectBox.children[j].id &&
            selectBox.children[j].id === value
          ) {
            drop = selectBox.children[j];
          }
        }
        selectBox.insertBefore(drag_txt, drop);
        selectBox.insertBefore(drag, drag_txt);
      }
    }
  }
}

op_radio.onclick = () => {
  let qnum = 1;
  let newli = document.createElement("li");
  let newh1 = document.createElement("h1");
  let newinput_topic = document.createElement("input");
  newinput_topic.className = "input-topic";
  //TODO 增加 id 属性
  newli.id = (++question_id).toString();
  //TODO 增加 name 属性
  newinput_topic.name = "question_radio";
  newinput_topic.type = "text";
  newinput_topic.value = "单选题";
  let newbtn = document.createElement("button");
  newbtn.className = "removeTopic";
  newbtn.appendChild(document.createTextNode("删除题目"));
  newh1.appendChild(newinput_topic);
  newli.appendChild(newh1);
  let newqbox = addRadio(newinput_topic.value);
  newli.appendChild(newqbox);
  newli.appendChild(newbtn);
  ul.appendChild(newli);
  //使弹窗消失
  btn_for_add.onclick();
  //给新增的题目添加删除事件
  newbtn.addEventListener("click", () => {
    ul.removeChild(newli);
  });
  //修改题目名字
  newinput_topic.onchange = () => {
    for (let i = 0; i < newqbox.children.length; i++) {
      newqbox.children[i].name = newinput_topic.value;
    }
  };
  //添加拖拽效果
  // newli.draggable = "true";
  // newli.ondragstart = onDragStart;
  // newli.ondragover = onDragOver;
  // newli.ondrop = onDrop;
};

//添加单选题
function addRadio(tname) {
  let newqbox = document.createElement("div");
  newqbox.className = "questionBox";
  let optionArr = ["A", "B", "C", "D"];
  for (let i = 0; i < 4; i++) {
    let newinput_radio = document.createElement("input");
    newinput_radio.type = "radio";
    newinput_radio.name = tname;
    newinput_radio.value = optionArr[i];
    let newop = document.createElement("span");
    newop.appendChild(document.createTextNode(optionArr[i]));
    newqbox.appendChild(newinput_radio);
    newqbox.appendChild(newop);
  }
  return newqbox;
}

// 点击了“创建收集”按钮
// btn_for_submit.onclick = () => {
//     // var question_data = [];
//     // 获取题目列表
//     // var question_list = document.getElementsByTagName("ul").getElementsByTagName("li");
//     // for (var i = 0; i < question_list.length; i++) {
//         document.getElementsByName("form").submit();
//     // }
// }

addLoadEvent(op_name.onclick);
addLoadEvent(op_file.onclick);

function onDragStart(e) {
  // 获取当前拖拽元素
  dragElement = e.currentTarget;
}
function onDragOver(e) {
  // 默认的当你dragover的时候会阻止你做drop的操作，所以需要取消这个默认
  e.preventDefault();
}
function onDrop(e) {
  // 当拖动结束的时候，给拖动div所在的位置下面的div做drop事件
  let dropElement = e.currentTarget;
  if (dragElement != null && dragElement != dropElement) {
    // // 临时 div 用于存储 box
    // let temp = document.createElement("li");
    // // 添加 temp 到父元素 wrapper 中
    // ul.appendChild(temp);
    // // 交换
    // ul.replaceChild(temp, dropElement);
    // ul.replaceChild(dropElement, dragElement);
    // ul.replaceChild(dragElement, temp);
    ul.insertBefore(dragElement, dropElement);
  }
  //交换复选框中的位置
  let dragId = dragElement.id;
  let dropId = dropElement.id;
  for_checkbox("swap", dragId, dropId);
}
