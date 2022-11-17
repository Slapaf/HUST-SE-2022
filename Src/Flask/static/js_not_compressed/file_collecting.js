const ul = document.querySelector(".main>ul");
const lis = ul.getElementsByTagName("li");
const rem = ul.getElementsByClassName("removeTopic");
const collectionTitle = document.querySelector(".collectionTitle");
const collector = document.querySelector(".collector");
const deadline = document.querySelector(".deadline");
const description = document.querySelector(".description");
const op_name = document.getElementById("op-name");
const op_file = document.getElementById("op-file");
const op_sno = document.getElementById("op-sno");
const op_radio = document.getElementById("op-radio");
const op_multipleChoice = document.getElementById("op-multipleChoice");
const op_qnaire = document.getElementById("op-qnaire");
const btn_for_add = document.querySelector("#btn-for-add");
const popup = document.querySelector(".popup");
const myalert = document.querySelector(".alert");
const myblur = document.querySelector("#blur");
const cancel = document.querySelector(".popup-header>span");
const btn_for_submit = document.getElementById("btn-for-submit"); //提交按钮
const form = document.getElementById("form");
let dragElement = null; //存放拖拽的元素
let qnum = 1;  //单选编号（区分单选用）
let question_id = 0; //（复选框用）id
let countdown = 2;
//点击“添加题目”按钮，弹出弹窗
btn_for_add.onclick = () => {
    popup.style.display = "block";
    myblur.style.display = "block";
};

//点击“x"，取消选择
cancel.onclick = () => {
    // btn_for_add.onclick();
    popup.style.display = "none";
    myblur.style.display = "none";
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
    var ss = now.getSeconds();          //秒
    var clock = year + "-";
    if (month < 10)
        clock += "0";
    clock += month + "-";
    if (day < 10)
        clock += "0";
    clock += day + "T";
    if (hh < 10)
        clock += "0";
    clock += hh + ":";
    if (mm < 10) clock += '0';
    clock += mm + ":";
    if (ss < 10) clock += '0';
    clock += ss;
    return clock;
}

//限制截止日期不能比当前时间早
//同时设置最晚截止时间
function deadline_limit() {
    let currentDatetime = getCurrentDatetime();
    deadline.min = currentDatetime;
    deadline.max = "2050-12-31T23:59:59";
}


/**
 * 根据topicName和detailText创建一个“姓名”类型的题目
 * @param {string} topicName 题目名称
 * @param {string} detailText 详情描述的内容 
 */
function createName(topicName, detailText) {
    //新建一些元素节点
    let newli = document.createElement("li");
    let newh1 = document.createElement("h1");
    let newinput_topic = document.createElement("input");
    newinput_topic.className = "input-topic";
    newinput_topic.required = "required";
    // 增加 id 属性
    newli.id = (++question_id).toString();
    // 增加 name 属性
    newinput_topic.name = "question_name";
    newinput_topic.type = "text";
    newinput_topic.value = topicName;
    newinput_topic.maxLength = "20";
    newinput_topic.placeholder = "添加题目名称";
    let newdetail = document.createElement("textarea");
    newdetail.placeholder = "添加详情描述";
    newdetail.name = "detail";
    newdetail.value = detailText;
    let newinput_content = document.createElement("input");
    newinput_content.className = "input-content";
    newinput_content.type = "text";
    // 此项由提交者填写，所以属性添加disabled
    newinput_content.disabled = "disabled";
    newinput_content.placeholder = "此项由提交者填写";
    let newbtn = document.createElement("button");
    newbtn.className = "removeTopic";
    // 把各元素节点插到其父元素下
    newbtn.appendChild(document.createTextNode("删除题目"));
    newh1.appendChild(newinput_topic);
    newli.appendChild(newh1);
    newli.appendChild(newdetail);
    newli.appendChild(newinput_content);
    newli.appendChild(newbtn);
    ul.appendChild(newli);
    cancel.onclick();
    // 在所有的文件重命名选项增加这个选项
    for_checkbox("add", newli.id, newinput_topic.value);
    // 给新增的题目添加删除事件
    newbtn.addEventListener("click", () => {
        // 在所有的文件重命名选项增加这个选项
        for_checkbox("remove", newli.id, newinput_topic.value);
        ul.removeChild(newli);
    });
    // 实时监听题目的名称变化
    // 以便于实时修改其在文件重命名选项中的对应名称
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
function createSno(topicName, detailText) {
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
    newinput_topic.value = topicName;
    newinput_topic.maxLength = "20";
    newinput_topic.placeholder = "添加题目名称";
    let newdetail = document.createElement("textarea");
    newdetail.placeholder = "添加详情描述";
    newdetail.name = "detail";
    newdetail.value = detailText;
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
    cancel.onclick();
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

/**
 * 根据topicName和detailText创建一个“文件”类型的题目
 * @param {string} topicName 题目名称
 * @param {string} detailText 详情描述的内容
 */
function createFile(topicName, detailText) {
    // 新建一些元素节点
    let newli = document.createElement("li");
    let newh1 = document.createElement("h1");
    let newinput_topic = document.createElement("input");
    newinput_topic.className = "input-topic";
    newinput_topic.required = "required";
    // 增加 id 属性
    newli.id = (++question_id).toString();
    // 增加 name 属性
    newinput_topic.name = "question_file";
    newinput_topic.type = "text";
    newinput_topic.value = topicName;
    newinput_topic.maxLength = "20";
    newinput_topic.placeholder = "添加题目名称";
    let newdetail = document.createElement("textarea");
    newdetail.placeholder = "添加详情描述";
    newdetail.name = "detail";
    newdetail.value = detailText;
    let newspan = document.createElement("span");
    newspan.className = "nameRules";
    // 鼠标经过问好时显示的文字
    newspan.setAttribute("data-hint", "提交的文件将按照勾选的选项自动重命名");
    newspan.appendChild(document.createTextNode("重命名规则："));
    // 重命名规则的勾选框
    let newselect = document.createElement("div");
    newselect.className = "selectTopic";
    let newinput_content = document.createElement("input");
    newinput_content.className = "input-content";
    // 创建收集者不提交文件，所以设为disabled
    newinput_content.disabled = "disabled";
    newinput_content.type = "file";
    let newbtn = document.createElement("button");
    newbtn.className = "removeTopic";
    // 把各元素节点插到其父节点下
    newbtn.appendChild(document.createTextNode("删除题目"));
    newh1.appendChild(newinput_topic);
    newli.appendChild(newh1);
    newli.appendChild(newdetail);
    newli.appendChild(newspan);
    // 添加重命名勾选框中的内容
    updateCheckbox(newselect);
    newli.appendChild(newselect);
    newli.appendChild(newinput_content);
    newli.appendChild(newbtn);
    ul.appendChild(newli);
    cancel.onclick();
    // 给新增的题目添加删除事件
    newbtn.addEventListener("click", () => {
        ul.removeChild(newli);
    });
    // 添加拖拽效果
    newli.draggable = "true";
    newli.ondragstart = onDragStart;
    newli.ondragover = onDragOver;
    newli.ondrop = onDrop;
};


/**
 * 给文件重命名勾选框加入内容
 * 当新建一个“文件”类型题目时，调用此函数
 * @param {object} selectBox 勾选框对象
 */
function updateCheckbox(selectBox) {
    for (let i = 0; i < lis.length; i++) {
        let input_topic = lis[i].getElementsByClassName("input-topic")[0];
        let input_content = lis[i].getElementsByClassName("input-content")[0];
        // 只有姓名和学号类型的题目要加入重命名勾选框
        if (!input_content) continue;
        if (input_content.type === "file") continue;
        let newcheckbox = document.createElement("input");
        let newspan = document.createElement("span");
        newspan.className = "checked_topic_text";
        newcheckbox.type = "checkbox";
        // 将勾选框选项的id与该题目的id设为相同的值
        // 以便于修改勾选框选项内容和交换顺序
        newcheckbox.id = lis[i].id;
        newcheckbox.name = "checked_topic";
        newcheckbox.value = input_topic.value;
        newspan.appendChild(document.createTextNode(input_topic.value));
        selectBox.appendChild(newcheckbox);
        selectBox.appendChild(newspan);
    }
}



/**
 * 修改复选框中的内容
*  当有题目的增加/删除/修改/交换顺序时，调用此函数
 * @param {string} option 操作类型，
 *                        有四种取值："add","remove","modify","swap"
 * @param {string} id 勾选框选项的id
 * @param {string} value 勾选框选项的内容
 * @returns null
 */
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
                if (value === 0) {
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
function createSingleChoice(topicName, detailText, checkedChoiceAmount, checkedChoice) {
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
    newinput_topic.value = topicName;
    newinput_topic.maxLength = "20";
    newinput_topic.placeholder = "添加题目名称";
    let newdetail = document.createElement("textarea");
    newdetail.placeholder = "添加详情描述";
    newdetail.name = "detail";
    newdetail.value = detailText;
    let newbtn = document.createElement("button");
    newbtn.className = "removeTopic";
    newbtn.appendChild(document.createTextNode("删除题目"));
    newh1.appendChild(newinput_topic);
    newli.appendChild(newh1);
    newli.appendChild(newdetail);
    let newqbox = addChoice_for_fileEditing(0, checkedChoiceAmount, checkedChoice);  //0单选
    newli.appendChild(newqbox);
    newli.appendChild(newbtn);
    ul.appendChild(newli);
    //使弹窗消失
    cancel.onclick();
    //给新增的题目添加删除事件
    newbtn.addEventListener("click", () => {
        ul.removeChild(newli);
    });
    //添加拖拽效果
    newli.draggable = "true";
    newli.ondragstart = onDragStart;
    newli.ondragover = onDragOver;
    newli.ondrop = onDrop;
}

//添加单选题/多选题
function addChoice_for_fileEditing(op, checkedChoiceAmount, checkedChoice) {
    let newqbox = document.createElement("div");
    newqbox.className = "questionBox1";
    let optionArr = ["A", "B", "C", "D"];
    for (let i = 0; i < 4; i++) {
        let newinput_radio = document.createElement("input");
        newinput_radio.type = (op === 0 ? "radio" : "checkbox");  //op=0是单选，op=1是多选
        newinput_radio.name = qnum.toString();
        newinput_radio.value = optionArr[i];
        if (op === 0) {  //单选必须选择一个
            newinput_radio.required = "required";
        }
        let newop = document.createElement("span");
        newop.appendChild(document.createTextNode(optionArr[i]));
        newqbox.appendChild(newinput_radio);
        newqbox.appendChild(newop);
    }
    for (let i = 0; i < checkedChoice.length; i++) {
        newqbox.children[checkedChoice[i] * 2].checked = "true";
    }
    qnum++;
    return newqbox;
}

//多选
function createMultipleChoice(topicName, detailText, checkedChoiceAmount, checkedChoice) {
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
    newinput_topic.value = topicName;
    newinput_topic.maxLength = "20";
    newinput_topic.placeholder = "添加题目名称";
    let newdetail = document.createElement("textarea");
    newdetail.placeholder = "添加详情描述";
    newdetail.name = "detail";
    newdetail.value = detailText;
    let newbtn = document.createElement("button");
    newbtn.className = "removeTopic";
    newbtn.appendChild(document.createTextNode("删除题目"));
    newh1.appendChild(newinput_topic);
    newli.appendChild(newh1);
    newli.appendChild(newdetail);
    let newqbox = addChoice_for_fileEditing(1, checkedChoiceAmount, checkedChoice);
    newli.appendChild(newqbox);
    newli.appendChild(newbtn);
    ul.appendChild(newli);
    //使弹窗消失
    cancel.onclick();
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
    if (dragElement === dropElement) return;
    //交换复选框中的位置
    let dragId = dragElement.id;
    let dropId = dropElement.id;
    let dragElementType = dragElement.getElementsByClassName("input-topic")[0].name;
    let dropElementType = dropElement.getElementsByClassName("input-topic")[0].name;
    if (dragElementType === "question_name" || dragElementType === "question_sno") {
        if (dropElementType === "question_name" || dropElementType === "question_sno") {
            if(dragElement.nextSibling === dropElement) {
                for_checkbox("swap",dropId,dragId);
            } else {
                for_checkbox("swap", dragId, dropId);
            }
        } else {
            let next = dropElement.nextSibling;
            let nextType = null;
            let flag = 0;
            while (next) {
                nextType = next.getElementsByClassName("input-topic")[0].name;
                if (nextType && (nextType === "question_name" || nextType === "question_sno")) {
                    for_checkbox("swap", dragId, next.id);
                    flag = 1;
                    break;
                }
                next = next.nextSibling;
            }
            if (!flag) {
                for_checkbox("swap", dragId, 0);
            }
        }
    }
    //实际交换位置
    if (dragElement != null) {
        if(dragElement.nextSibling === dropElement) {
            ul.insertBefore(dropElement, dragElement);
        } else {
            ul.insertBefore(dragElement, dropElement);
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
        let radioBoxes = lis[i].getElementsByClassName("questionBox1")[0];
        if (radioBoxes && radioBoxes.children[0].type == "radio") {
            let c = radioBoxes.children;
            for (let j = 0; j < c.length; j++) {
                if (c[j].name) {
                    c[j].name = "checked_radio" + finalId; //单选题选项的name
                }
            }
        }
        let mulBoxes = lis[i].getElementsByClassName("questionBox1")[0];
        if (mulBoxes && mulBoxes.children[0].type == "checkbox") {
            let c = mulBoxes.children;
            for (let j = 0; j < c.length; j++) {
                if (c[j].name) {
                    c[j].name = "checked_mulans" + finalId; //多选题选项的name
                }
            }
        }
        let qn_options = lis[i].getElementsByClassName("qnaire_textarea");
        if (qn_options) {
            for (let j = 0; j < qn_options.length; j++) {
                if (qn_options[j].name) {
                    qn_options[j].name = qn_options[j].name + finalId; //问卷选项的name
                }
            }
        }
        let choose_type = lis[i].querySelectorAll(".hidden_radio");
        if (choose_type) {
            console.log(choose_type.length);
            for (let i = 0; i < choose_type.length; i++) {
                choose_type[i].name = "choose_type" + finalId;
            }
        }
        finalId++;
    }
    return true;
}

//问卷
function createQuestionnaire(topicName, detailText, qnOptionArr, multi) {
    let newli = document.createElement("li");
    let newh1 = document.createElement("h1");
    let newinput_topic = document.createElement("input");
    newinput_topic.className = "input-topic";
    //TODO 增加 id 属性
    newli.id = (++question_id).toString();
    //TODO 增加 name 属性
    newinput_topic.name = "question_qnaire";
    newinput_topic.type = "text";
    newinput_topic.value = topicName;
    newinput_topic.maxLength = "20";
    newinput_topic.placeholder = "添加题目名称";
    let newdetail = document.createElement("textarea");
    newdetail.placeholder = "添加详情描述";
    newdetail.name = "detail";
    newdetail.value = detailText;
    let newqbox = document.createElement("div");
    newqbox.className = "questionBox";
    let newbtn = document.createElement("button");
    newbtn.className = "removeTopic";
    newbtn.appendChild(document.createTextNode("删除题目"));
    let newadd = document.createElement("div");
    newadd.className = "qnaire_addop";
    newadd.appendChild(document.createTextNode("添加选项"));
    let newdiv = document.createElement("div");
    newdiv.className = "if_multi";
    let if_multi = document.createElement("input");
    if_multi.type = "checkbox";
    let newlabel = document.createElement("label");
    newlabel.appendChild(document.createTextNode("多选"));
    let hidden_radio1 = document.createElement("input");
    let hidden_radio2 = document.createElement("input");
    hidden_radio1.type = "radio";
    hidden_radio2.type = "radio";
    hidden_radio1.className = "hidden hidden_radio";
    hidden_radio2.className = "hidden hidden_radio";
    hidden_radio1.value = "single";
    hidden_radio2.value = "multiple";
    hidden_radio1.name = "choose_type" + newli.id;
    hidden_radio2.name = "choose_type" + newli.id;
    hidden_radio1.checked = "checked";
    newh1.appendChild(newinput_topic);
    newli.appendChild(newh1);
    newli.appendChild(newdetail);
    newli.appendChild(newqbox);  //qbox里动态添加选项
    newli.appendChild(newadd);
    newdiv.appendChild(if_multi);
    newdiv.appendChild(newlabel);
    newdiv.appendChild(hidden_radio1);
    newdiv.appendChild(hidden_radio2);
    newli.appendChild(newdiv);
    newli.appendChild(newbtn);
    ul.appendChild(newli);
    //使弹窗消失
    cancel.onclick();
    //默认添加两个选项
    // newqbox.appendChild(addQuestion(if_multi.checked));
    // newqbox.appendChild(addQuestion(if_multi.checked));
    //给新增的题目添加删除事件
    newbtn.addEventListener("click", () => {
        ul.removeChild(newli);
    });
    //给“添加选项”按钮添加事件
    newadd.onclick = () => {
        newqbox.appendChild(addQuestion(if_multi.checked));
    };
    //给“多选”复选框添加事件
    if (multi) {
        if_multi.checked = true;
        hidden_radio1.removeAttribute("checked");
        hidden_radio2.checked = "checked";
    }
    //按照传过来的参数添加选项
    for (let i = 0; i < qnOptionArr.length; i++) {
        newqbox.appendChild(addQuestion_for_fileEditing(if_multi.checked, qnOptionArr[i]));
    }
    if_multi.onchange = () => {
        let qnaire_check = newli.getElementsByClassName("qnaire_check");
        if (if_multi.checked) {
            for (let i = 0; i < qnaire_check.length; i++) {
                qnaire_check[i].type = "checkbox";
            }
            hidden_radio1.removeAttribute("checked");
            hidden_radio2.checked = "checked";
        } else {
            for (let i = 0; i < qnaire_check.length; i++) {
                qnaire_check[i].type = "radio";
            }
            hidden_radio2.removeAttribute("checked");
            hidden_radio1.checked = "checked";
        }
    }
    //添加拖拽效果
    newli.draggable = "true";
    newli.ondragstart = onDragStart;
    newli.ondragover = onDragOver;
    newli.ondrop = onDrop;
}

//添加一个问卷选项(添加按钮触发)
function addQuestion(check_status) {
    let newoption = document.createElement("div");
    newoption.className = "qnaire_option";
    let newcheck = document.createElement("input");
    if (check_status == false) {
        newcheck.type = "radio";
    } else {
        newcheck.type = "checkbox";  //新增的选项要改type
    }
    newcheck.className = "qnaire_check";
    newcheck.disabled = "disabled";
    let newta = document.createElement("textarea");
    newta.className = "qnaire_textarea";
    newta.placeholder = "请输入选项的内容";
    newta.name = "qn_option";
    let newremove = document.createElement("span");
    newremove.className = "qnaire_removeop";
    // newremove.appendChild(document.createTextNode("X"));
    newoption.appendChild(newcheck);
    newoption.appendChild(newta);
    newoption.appendChild(newremove);
    newremove.onclick = () => {
        newoption.parentNode.removeChild(newoption);
    }
    newta.addEventListener("input", () => {
        newta.style.height = 'auto';
        newta.style.height = newta.scrollHeight + 'px';
    })
    return newoption;
}


//添加一个问卷选项(传参触发)
function addQuestion_for_fileEditing(check_status, qnOptionText) {
    let newoption = document.createElement("div");
    newoption.className = "qnaire_option";
    let newcheck = document.createElement("input");
    if (check_status == false) {
        newcheck.type = "radio";
    } else {
        newcheck.type = "checkbox";  //新增的选项要改type
    }
    newcheck.className = "qnaire_check";
    newcheck.disabled = "disabled";
    let newta = document.createElement("textarea");
    newta.className = "qnaire_textarea";
    newta.placeholder = "请输入选项的内容";
    newta.name = "qn_option";
    newta.value = qnOptionText;
    let newremove = document.createElement("span");
    newremove.className = "qnaire_removeop";
    // newremove.appendChild(document.createTextNode("X"));
    newoption.appendChild(newcheck);
    newoption.appendChild(newta);
    newoption.appendChild(newremove);
    newremove.onclick = () => {
        newoption.parentNode.removeChild(newoption);
    }
    newta.addEventListener("input", () => {
        newta.style.height = 'auto';
        newta.style.height = newta.scrollHeight + 'px';
    })
    return newoption;
}

//提交前检查
function check() {
    //检查是否有重复题目
    let errorNum = 0;
    let currentDatetime = getCurrentDatetime();
    if( currentDatetime >= deadline.value) {
        errorNum = 6;
    }
    let arr = [];
    let topics = document.getElementsByClassName("input-topic");
    for (let i = 0; i < topics.length; i++) {
        if (arr.indexOf(topics[i].value) == -1) {
            arr.push(topics[i].value);
        } else {
            errorNum = 1;
        }
    }
    //检查多选是否至少选了两个
    for (let i = 0; i < topics.length; i++) {
        if (topics[i].name != "question_multipleChoice") continue;
        let checkBoxes = lis[i].querySelectorAll("input[type='checkbox']");
        let cnt = 0;
        for (let i = 0; i < checkBoxes.length; i++) {
            if (checkBoxes[i].checked) cnt++;
        }
        if (cnt < 2) {
            errorNum = 2;
        }
    }
    //检查问卷是否至少有两个选项
    for (let i = 0; i < topics.length; i++) {
        if (topics[i].name != "question_qnaire") continue;
        let qnaire_options = lis[i].querySelectorAll(".qnaire_option");
        let qnaire_textareas = lis[i].querySelectorAll(".qnaire_textarea");
        if (qnaire_options.length < 2) {
            errorNum = 3;
        } else {
            //检查问卷选项是否为空
            for (let j = 0; j < qnaire_textareas.length; j++) {
                if (qnaire_textareas[j].value == '') {
                    errorNum = 4;
                }
            }
        }
    }
    //检查是否至少有一个题目
    if (topics.length === 0) {
        errorNum = 5;
    }
    //出错提示弹窗
    if (errorNum) {
        let h1 = myalert.getElementsByTagName("h1")[0];
        if (errorNum === 1) {
            h1.innerHTML = "不能有重复标题!";
        } else if (errorNum === 2) {
            h1.innerHTML = "多选题请至少选择两个选项!";
        } else if (errorNum === 3) {
            h1.innerHTML = "问卷选项不能少于两个！";
        } else if (errorNum === 4) {
            h1.innerHTML = "问卷选项内容不能为空！";
        } else if (errorNum === 5) {
            h1.innerHTML = "至少有一个题目！";
        } else if (errorNum === 6) {
            h1.innerHTML = "截止时间不能早于当前时间！";
        }
        myalert.style.display = "block";
        myblur.style.display = "block";
        countdown = 2;
        timeOutClose();
        return false;
    }
    return true;
}

//表单提交前触发检查和编号程序
form.onsubmit = () => {
    if (check()) {
        return numberQuestion();
    } else {
        return false;
    }
}

//弹窗倒计时
function timeOutClose() {
    // document.getElementById("timeOutClose").innerHTML = countdown;
    if (countdown > 0) {
        setTimeout("timeOutClose();", 1000);
    } else {
        myalert.style.display = "none";
        myblur.style.display = "none";
    }
    countdown--;
}

//添加点击事件，保持原有功能
op_name.onclick = () => {
    createName("姓名", "");
};

op_sno.onclick = () => {
    createSno("学号", "");
};

op_file.onclick = () => {
    createFile("文件", "");
};

op_radio.onclick = () => {
    createSingleChoice("单选题", "", 0, []);
};

op_multipleChoice.onclick = () => {
    createMultipleChoice("多选题", "", 0, []);
};

op_qnaire.onclick = () => {
    createQuestionnaire("问卷题目", "", ["", ""], false);
};

let tmp_json = document.getElementById('collection').innerHTML;
// 处理数据
// let formData = JSON.parse(JSON.stringify(jsonFromHtml));
let formData = JSON.parse(JSON.stringify(tmp_json));
let formDataArr = [];
let formDataObj = {};
let formDataLen = 0;
const reg = /(\d+)$/;
let lastNum = 1;

function processFormData() {
    if (!tmp_json) return;
    tmp_json = eval("(" + tmp_json + ")");
    formData = JSON.parse(JSON.stringify(tmp_json));
    for (item in formData) {
        let result = reg.exec(item);
        if (result) {
            let num = result[1];
            if (num != lastNum) {
                formDataArr.push(formDataObj);
                formDataObj = new Object();
            }
            let key = item;
            let value = formData[item];
            formDataObj[key] = value;
            lastNum = num;
        }
    }
    formDataArr.push(formDataObj);
    formDataLen = formDataArr.length;
}

function createQuestion() {
    if (formDataLen === 0) {
        collectionTitle.value = "文件收集";
        // collector.value = "";
        op_name.onclick();
        op_sno.onclick();
        op_file.onclick();
        return;
    }
    collectionTitle.value = Object.values(formData)[0];
    collector.value = Object.values(formData)[1];
    deadline.value = Object.values(formData)[2];
    description.value = Object.values(formData)[3];
    for (let i = 0; i < formDataLen; i++) {
        let q = formDataArr[i];
        let keys = Object.keys(formDataArr[i]);
        let values = Object.values(formDataArr[i]);
        if (keys[0].indexOf("question_name") != -1) {
            createName(values[0], values[1]);
        } else if (keys[0].indexOf("question_sno") != -1) {
            createSno(values[0], values[1]);
        } else if (keys[0].indexOf("question_file") != -1) {
            createFile(values[0], values[1]);
        } else if (keys[0].indexOf("question_radio") != -1) {
            let k = values[values.length - 1].toString().charCodeAt() - 'A'.charCodeAt();
            createSingleChoice(values[0], values[1], 1, [k]);
        } else if (keys[0].indexOf("question_multipleChoice") != -1) {
            let cnt = 0;
            let tmp = [];
            for (let j = 0; j < keys.length; j++) {
                if (keys[j].indexOf("checked_mulans") != -1) {
                    cnt++;
                    tmp.push(values[j].toString().charCodeAt() - 'A'.charCodeAt());
                }
            }
            createMultipleChoice(values[0], values[1], cnt, tmp);
        } else {
            let qnOptionNum = 0;
            let qnOptionContent = [];
            for (let j = 0; j < keys.length; j++) {
                if (keys[j].indexOf("qn_option") != -1) {
                    qnOptionNum++;
                    qnOptionContent.push(values[j]);
                }
            }
            let multi = values[values.length - 1] == "multiple";
            createQuestionnaire(
                values[0],
                values[1],
                qnOptionContent,
                multi
            );
        }
    }
    for (let i = 0; i < formDataLen; i++) {
        let q = formDataArr[i];
        let keys = Object.keys(formDataArr[i]);
        let values = Object.values(formDataArr[i]);
        let texts = lis[i].querySelectorAll(".checked_topic_text");
        if (keys[0].indexOf("question_file") != -1) {
            for (let j = 0; j < keys.length; j++) {
                if (keys[j].indexOf("checked_topic") != -1) {
                    for (let k = 0; k < texts.length; k++) {
                        if (texts[k].innerHTML == values[j])
                            texts[k].previousSibling.checked = "checked";
                    }
                }
            }
        }
    }
}

addLoadEvent(processFormData);
addLoadEvent(createQuestion);
addLoadEvent(deadline_limit);