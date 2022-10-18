const ul = document.querySelector(".main>ul");
const lis = ul.getElementsByTagName("li");
const rem = ul.getElementsByClassName("removeTopic");
const deadline = document.getElementsByClassName("deadline")[0];
const op_name = document.getElementById("op-name");
const op_file = document.getElementById("op-file");
const op_sno = document.getElementById("op-sno");
const op_radio = document.getElementById("op-radio");
const op_multipleChoice = document.getElementById("op-multipleChoice");
const btn_for_add = document.querySelector("#btn-for-add");
const popup = document.querySelector(".popup");
const myalert = document.querySelector(".alert");
const cancel = document.querySelector(".popup-header>span");
const btn_for_submit = document.getElementById("btn-for-submit"); //提交按钮
const form = document.getElementById("form");
let dragElement = null; //存放拖拽的元素
let qnum = 1;  //单选编号（区分单选用）
let question_id = 0; //（复选框用）id
let countdown = 3;
//点击“添加题目”按钮，弹出弹窗
btn_for_add.onclick = () => {
  popup.classList.toggle("show");
};

//点击“x"，取消选择
cancel.onclick = () => {
  btn_for_add.onclick();
};

//将需要文档加载完毕后执行的函数加到执行队列
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

//获取当前时间
function getCurrentDatetime() {   
  var now = new Date();  
  var year = now.getFullYear();       //年  
  var month = now.getMonth() + 1;     //月  
  var day = now.getDate();            //日  
  var hh = now.getHours();            //时  
  var mm = now.getMinutes();          //分  
  var clock = year + "-";  
  if(month < 10)  
    clock += "0";  
  clock += month + "-";  
  if(day < 10)  
    clock += "0";  
  clock += day + "T";  
  if(hh < 10)  
    clock += "0";  
  clock += hh + ":";  
  if (mm < 10) clock += '0';   
  clock += mm;   
  return clock;      
} 

//限制截止日期不能比当前时间早
function deadline_limit() {
  let currentDatetime = getCurrentDatetime();
  deadline.min = currentDatetime;
} 

//姓名
op_name.onclick = () => {
  //新建一些元素节点
  let newli = document.createElement("li");
  let newh1 = document.createElement("h1");
  let newinput_topic = document.createElement("input");
  newinput_topic.className = "input-topic";
  newinput_topic.required = "required";
  //TODO 增加 id 属性
  newli.id = (++question_id).toString();
  //TODO 增加 name 属性
  newinput_topic.name = "question_name";
  newinput_topic.type = "text";
  newinput_topic.value = "姓名";
  newinput_topic.maxLength = "20";
  newinput_topic.placeholder = "请输入不超过20个字符的题目";
  let newdetail = document.createElement("textarea");
  newdetail.placeholder = "添加详情描述";
  newdetail.name = "detail";
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
  newli.appendChild(newdetail);
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
  newli.draggable = "true";
  newli.ondragstart = onDragStart;
  newli.ondragover = onDragOver;
  newli.ondrop = onDrop;
};

//学号
op_sno.onclick = () => {
  //新建一些元素节点
  let newli = document.createElement("li");
  let newh1 = document.createElement("h1");
  let newinput_topic = document.createElement("input");
  newinput_topic.className = "input-topic";
  newinput_topic.required = "required";
  //TODO 增加 id 属性
  newli.id = (++question_id).toString();
  //TODO 增加 name 属性
  newinput_topic.name = "question_sno";
  newinput_topic.type = "text";
  newinput_topic.value = "学号";
  newinput_topic.maxLength = "20";
  newinput_topic.placeholder = "请输入不超过20个字符的题目";
  let newdetail = document.createElement("textarea");
  newdetail.placeholder = "添加详情描述";
  newdetail.name = "detail";
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
  newli.appendChild(newdetail);
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
  newli.draggable = "true";
  newli.ondragstart = onDragStart;
  newli.ondragover = onDragOver;
  newli.ondrop = onDrop;
};

//文件
op_file.onclick = () => {
  //新建一些元素节点
  let newli = document.createElement("li");
  let newh1 = document.createElement("h1");
  let newinput_topic = document.createElement("input");
  newinput_topic.className = "input-topic";
  newinput_topic.required = "required";
  //TODO 增加 id 属性
  newli.id = (++question_id).toString();
  //TODO 增加 name 属性
  newinput_topic.name = "question_file";
  newinput_topic.type = "text";
  newinput_topic.value = "文件";
  newinput_topic.maxLength = "20";
  newinput_topic.placeholder = "请输入不超过20个字符的题目";
  let newdetail = document.createElement("textarea");
  newdetail.placeholder = "添加详情描述";
  newdetail.name = "detail";
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
  newli.appendChild(newdetail);
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
  newli.draggable = "true";
  newli.ondragstart = onDragStart;
  newli.ondragover = onDragOver;
  newli.ondrop = onDrop;
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
//当有题目的增加/删除/修改/交换顺序时，调用此函数
//option有四种取值："add","remove","modify","swap"
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
        if(value === 0) {
          selectBox.appendChild(drag);
          selectBox.appendChild(drag_txt);
          return;
        } 
        selectBox.insertBefore(drag_txt, drop);
        selectBox.insertBefore(drag, drag_txt);
      }
    }
  }
}

//单选
op_radio.onclick = () => {
  let newli = document.createElement("li");
  let newh1 = document.createElement("h1");
  let newinput_topic = document.createElement("input");
  newinput_topic.className = "input-topic";
  newinput_topic.required = "required";
  //TODO 增加 id 属性
  newli.id = (++question_id).toString();
  //TODO 增加 name 属性
  newinput_topic.name = "question_radio";
  newinput_topic.type = "text";
  newinput_topic.value = "单选题";
  newinput_topic.maxLength = "20";
  newinput_topic.placeholder = "请输入不超过20个字符的题目";
  let newdetail = document.createElement("textarea");
  newdetail.placeholder = "添加详情描述";
  newdetail.name = "detail";
  let newbtn = document.createElement("button");
  newbtn.className = "removeTopic";
  newbtn.appendChild(document.createTextNode("删除题目"));
  newh1.appendChild(newinput_topic);
  newli.appendChild(newh1);
  newli.appendChild(newdetail);
  let newqbox = addChoice(0);
  newli.appendChild(newqbox);
  newli.appendChild(newbtn);
  ul.appendChild(newli);
  //使弹窗消失
  btn_for_add.onclick();
  //给新增的题目添加删除事件
  newbtn.addEventListener("click", () => {
    ul.removeChild(newli);
  });
  //添加拖拽效果
  newli.draggable = "true";
  newli.ondragstart = onDragStart;
  newli.ondragover = onDragOver;
  newli.ondrop = onDrop;
};

//添加单选题/多选题
function addChoice(op) {
  let newqbox = document.createElement("div");
  newqbox.className = "questionBox";
  let optionArr = ["A", "B", "C", "D"];
  for (let i = 0; i < 4; i++) {
    let newinput_radio = document.createElement("input");
    newinput_radio.type =(op===0?"radio":"checkbox");  //op=0是单选，op=1是多选
    newinput_radio.name = qnum.toString();
    newinput_radio.value = optionArr[i];
    if(op === 0) {  //单选必须选择一个
      newinput_radio.required = "required";
    }
    let newop = document.createElement("span");
    newop.appendChild(document.createTextNode(optionArr[i]));
    newqbox.appendChild(newinput_radio);
    newqbox.appendChild(newop);
  }
  qnum++;
  return newqbox;
}

//多选
op_multipleChoice.onclick = () => {
  let newli = document.createElement("li");
  let newh1 = document.createElement("h1");
  let newinput_topic = document.createElement("input");
  newinput_topic.className = "input-topic";
  newinput_topic.required = "required";
  //TODO 增加 id 属性
  newli.id = (++question_id).toString();
  //TODO 增加 name 属性
  newinput_topic.name = "question_multipleChoice";
  newinput_topic.type = "text";
  newinput_topic.value = "多选题";
  newinput_topic.maxLength = "20";
  newinput_topic.placeholder = "请输入不超过20个字符的题目";
  let newdetail = document.createElement("textarea");
  newdetail.placeholder = "添加详情描述";
  newdetail.name = "detail";
  let newbtn = document.createElement("button");
  newbtn.className = "removeTopic";
  newbtn.appendChild(document.createTextNode("删除题目"));
  newh1.appendChild(newinput_topic);
  newli.appendChild(newh1);
  newli.appendChild(newdetail);
  let newqbox = addChoice(1);
  newli.appendChild(newqbox);
  newli.appendChild(newbtn);
  ul.appendChild(newli);
  //使弹窗消失
  btn_for_add.onclick();
  //给新增的题目添加删除事件
  newbtn.addEventListener("click", () => {
    ul.removeChild(newli);
  });
  //添加拖拽效果
  newli.draggable = "true";
  newli.ondragstart = onDragStart;
  newli.ondragover = onDragOver;
  newli.ondrop = onDrop;
};

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
  if(dragElement === dropElement) return;
  if (dragElement != null) {
    ul.insertBefore(dragElement, dropElement);
  }
  //交换复选框中的位置
  let dragId = dragElement.id;
  let dropId = dropElement.id;
  let dragElementType = dragElement.getElementsByClassName("input-topic")[0].name;
  let dropElementType = dropElement.getElementsByClassName("input-topic")[0].name;
  if(dragElementType ==="question_name" || dragElementType ==="question_sno") {
    if(dropElementType==="question_name"||dropElementType==="question_sno") {
      for_checkbox("swap", dragId, dropId);
    }else {
      let next = dropElement.nextSibling;
      let nextType = null;
      let flag = 0;
      while(next) {
        nextType = next.getElementsByClassName("input-topic")[0].name;
        if(nextType&&nextType!="question_file"&&nextType!="question_radio") {
          for_checkbox("swap", dragId, next.id);
          flag = 1;
          break;
        }
        next=next.nextSibling;
      }
      if(!flag) {
        for_checkbox("swap",dragId,0);
      }
    }
  }
  
}

//提交表单时给每个问题加上编号
function numberQuestion() {
  let finalId = 1;
  for (let i = 0; i < lis.length; i++) {
    let topic = lis[i].getElementsByClassName("input-topic")[0];
    lis[i].id = "" + finalId;
    topic.name = topic.name + finalId; //题目的name
    let detail = lis[i].getElementsByTagName("textarea")[0];
    detail.name = detail.name + finalId;  //textarea的name
    let checkBoxes = lis[i].getElementsByClassName("selectTopic")[0];
    if (checkBoxes) {
      let c = checkBoxes.children;
      for (let j = 0; j < c.length; j++) {
        if (c[j].name) {
          c[j].name = c[j].name + finalId; //复选框的name
        }
      }
    }
    let radioBoxes = lis[i].getElementsByClassName("questionBox")[0];
    if (radioBoxes) {
      let c = radioBoxes.children;
      for (let j = 0; j < c.length; j++) {
        if (c[j].name) {
          c[j].name = "checked_radio" + finalId; //单选题选项的name
        }
      }
    }
    let mulBoxes = lis[i].getElementsByClassName("questionBox")[0];
    if(mulBoxes) {
      let c = mulBoxes.children;
      for (let j = 0; j < c.length; j++) {
        if (c[j].name) {
          c[j].name = "checked_mulans" + finalId; //多选题选项的name
        }
      }
    }
    finalId++;
  }
  return true;
}

//提交前检查
function check() {
  //检查是否有重复题目
  let errorNum = 0;
  let arr=[];
  let topics = document.getElementsByClassName("input-topic");
  for(let i=0;i<topics.length;i++) {
    if(arr.indexOf(topics[i].value)==-1) {
      arr.push(topics[i].value);
    }else {
      errorNum = 1;
    }
  }
  //检查多选是否至少选了两个
  for(let i=0;i<topics.length;i++) {
    if(topics[i].name != "question_multipleChoice") continue;
    let checkBoxes = lis[i].querySelectorAll("input[type='checkbox']");
    let cnt = 0;
    for(let i=0;i<checkBoxes.length;i++) {
      if(checkBoxes[i].checked) cnt++;
    }
    if(cnt < 2) {
      errorNum = 2;
    }
  }
  //出错提示弹窗
  if(errorNum) {
    let h1 = myalert.getElementsByTagName("h1")[0];
    if(errorNum === 1) {
      h1.innerHTML = "不能有重复标题";
    }else if(errorNum === 2){
      h1.innerHTML = "多选题至少选择两个选项";
    }
    myalert.classList.toggle("show");
    btn_for_submit.disabled = "disabled";
    countdown = 3;
    timeOutClose();
    return false;
  }
  return true;
}

//表单提交前触发检查和编号程序
form.onsubmit = ()=>{
  if(check()) {
    return numberQuestion();
  }else {
    return false;
  }
}

//弹窗倒计时
function timeOutClose() {
  document.getElementById("timeOutClose").innerHTML = countdown;
  if(countdown > 0) {
    setTimeout("timeOutClose();",1000);
  }else {
    myalert.classList.toggle("show");
    btn_for_submit.removeAttribute("disabled");
  }
  countdown--;
}

addLoadEvent(op_name.onclick);
addLoadEvent(op_file.onclick);
addLoadEvent(deadline_limit);