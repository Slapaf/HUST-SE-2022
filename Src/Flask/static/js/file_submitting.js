const questionList = document.querySelector("#question_list");
const collectionTitle = document.querySelector("#collectionTitle");
const collector = document.querySelector("#collector");
const deadline = document.querySelector("#deadline");
const description = document.querySelector("#description");
const myalert = document.querySelector(".alert");
const myblur = document.querySelector("#blur");
const myform = document.querySelector("#myform");
let qnum = 0;
let question_id = 0;
let countdown = 2;

//添加名字/学号/文件
function creatNameOrSnoOrFile(op, topicName, detailText) {
    //要给inputContent加name
    let newli = document.createElement("li");
    let newh = document.createElement("h1");
    let inputTopic = document.createElement("input");
    inputTopic.type = "text";
    inputTopic.value = topicName;
    inputTopic.className = "readOnlyInput";
    inputTopic.readOnly = "true";
    let detail = document.createElement("div");
    detail.className = "detail";
    detail.innerHTML = textareaToDiv(detailText);
    let inputContent = document.createElement("input");
    inputContent.type = op == "file" ? "file" : "text";
    inputContent.className = "inputContent";
    inputContent.required = true;
    inputContent.maxLength = 25;
    questionList.appendChild(newli);
    newli.appendChild(newh);
    newh.appendChild(inputTopic);
    if(detail.innerHTML) {
        newli.appendChild(detail);
    }
    newli.appendChild(inputContent);
    //加id，加name
    newli.id = question_id.toString();
    inputTopic.name = "question_" + op + question_id;
    inputContent.name = "submit_" + op + question_id;
}


//添加单选/多选
function creatSingleOrMultiple(op, topicName, detailText) {
    //要给inputChoice加name
    let newli = document.createElement("li");
    newli.id = question_id.toString();
    let newh = document.createElement("h1");
    let inputTopic = document.createElement("input");
    inputTopic.type = "text";
    inputTopic.value = topicName;
    inputTopic.className = "readOnlyInput";
    inputTopic.readOnly = "true";
    inputTopic.name =
        "question_" + (op === "single" ? "radio" : "multipleChoice") + question_id;
    let detail = document.createElement("div");
    detail.className = "detail";
    detail.innerHTML = textareaToDiv(detailText);
    let qBox = document.createElement("div");
    qBox.className = op === "single" ? "singleQuestionBox" : "multiQuestionBox";
    let ABCD = ["A", "B", "C", "D"];
    for (let i = 0; i < 4; i++) {
        let opBox = document.createElement("div");
        opBox.className = op === "single" ? "singleOption" : "multiOption";
        let inputChoice = document.createElement("input");
        inputChoice.type = op === "single" ? "radio" : "checkbox";
        inputChoice.name =
            "submit_checked_" + (op === "single" ? "radio" : "mulans") + question_id;
        inputChoice.value = ABCD[i];
        inputChoice.required = op === "single" ? true : false;
        let newlabel = document.createElement("label");
        newlabel.innerHTML = ABCD[i];
        opBox.appendChild(inputChoice);
        opBox.appendChild(newlabel);
        qBox.appendChild(opBox);
    }
    questionList.appendChild(newli);
    newli.appendChild(newh);
    newh.appendChild(inputTopic);
    if(detail.innerHTML) {
        console.log(detail.innerHTML);
        newli.appendChild(detail);
    }
    newli.appendChild(qBox);
    //加id，加name
}


//参数：编号，题目，详情描述，选项数，选项内容（数组），选择类型（单选/多选）
function creatQuestionnaire(
    topicName,
    detailText,
    qnOptionNum,
    qnOptionContent,
    chooseType
) {
    let newli = document.createElement("li");
    let newh = document.createElement("h1");
    let inputTopic = document.createElement("input");
    inputTopic.type = "text";
    inputTopic.value = topicName;
    inputTopic.className = "readOnlyInput";
    inputTopic.readOnly = "true";
    inputTopic.id = question_id;
    inputTopic.name = "question_qnaire" + question_id;
    let detail = document.createElement("div");
    detail.className = "detail";
    detail.innerHTML = textareaToDiv(detailText);
    let qBox = document.createElement("div");
    qBox.className = "qnQuestionBox";
    for (let i = 0; i < qnOptionNum; i++) {
        let opBox = document.createElement("div");
        opBox.className = "qnOption";
        let inputChoice = document.createElement("input");
        inputChoice.className = "qnOptionChoice";
        inputChoice.type = chooseType === "single" ? "radio" : "checkbox";
        inputChoice.name = "submit_checked_qnaire" + question_id;
        inputChoice.value = (i + 1).toString();
        inputChoice.required = chooseType === "single" ? true : false;
        let optionContent = document.createElement("div");
        optionContent.className = "qnOptionContent";
        optionContent.innerHTML = textareaToDiv(qnOptionContent[i]);
        opBox.appendChild(inputChoice);
        opBox.appendChild(optionContent);
        qBox.appendChild(opBox);
    }
    questionList.appendChild(newli);
    newli.appendChild(newh);
    newh.appendChild(inputTopic);
    if(detail.innerHTML) {
        newli.appendChild(detail);
    }
    newli.appendChild(qBox);
}


// TODO:按照这个格式传数据
let jsonFromHtml = {
    "1_collectionTitle": "文件收集",
    "2_collector": "凯",
    "3_deadline": "2022-10-28 14:55",
    "4_description": "描述",
    "5_question_name1": "姓名lala",
    "6_detail1": "",
    "7_question_file2": "文件haha",
    "8_detail2": "请提交本次作业",
    "9_checked_topic2": "姓名",
    "10_checked_topic2": "学号",
    "11_question_sno3": "学号xixi",
    "12_detail3": "",
    "13_question_radio4": "单选题nie",
    "14_detail4": "",
    "15_checked_radio4": "",
    "16_question_multipleChoice5": "多选题kk",
    "17_detail5": "",
    "18_checked_mulans5": "C",
    "19_checked_mulans5": "D",
    "20_question_qnaire6": "你喜欢跑步吗？",
    "21_detail6": "请选择一个选项",
    "22_qn_option6": "喜欢",
    "23_qn_option6": "不喜欢",
    "24_qn_option6": "还行",
    "25_choose_type6": "multiple",
};

let tmp_json = document.getElementById('collection').innerHTML;
tmp_json = eval("(" + tmp_json + ")"); // ! 有风险
// console.log(typeof tmp_json);
// console.log(tmp_json);
// console.log(typeof jsonFromHtml);
// console.log(jsonFromHtml);
let formData = JSON.parse(JSON.stringify(tmp_json));
let formDataArr = [];
let formDataObj = {};
let formDataLen = 0;
const reg = /(\d+)$/;
let lastNum = 1;

function processFormData() {
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

function creatQuestion() {
    collectionTitle.innerHTML = Object.values(formData)[0];
    collector.innerHTML = Object.values(formData)[1];
    deadline.innerHTML = Object.values(formData)[2];
    description.innerHTML = Object.values(formData)[3];
    for (let i = 0; i < formDataLen; i++) {
        let q = formDataArr[i];
        let keys = Object.keys(formDataArr[i]);
        let values = Object.values(formDataArr[i]);
        // console.log(keys);
        // console.log(values);
        question_id++;
        if (keys[0].indexOf("question_name") != -1) {
            creatNameOrSnoOrFile("name", values[0], values[1]);
        } else if (keys[0].indexOf("question_sno") != -1) {
            creatNameOrSnoOrFile("sno", values[0], values[1]);
        } else if (keys[0].indexOf("question_file") != -1) {
            creatNameOrSnoOrFile("file", values[0], values[1]);
        } else if (keys[0].indexOf("question_radio") != -1) {
            creatSingleOrMultiple("single", values[0], values[1]);
        } else if (keys[0].indexOf("question_multipleChoice") != -1) {
            creatSingleOrMultiple("multiple", values[0], values[1]);
        } else {
            let qnOptionNum = 0;
            let qnOptionContent = [];
            for (let j = 0; j < keys.length; j++) {
                if (keys[j].indexOf("qn_option") != -1) {
                    qnOptionNum++;
                    qnOptionContent.push(values[j]);
                }
            }
            creatQuestionnaire(
                values[0],
                values[1],
                qnOptionNum,
                qnOptionContent,
                values[values.length - 1]
            );
        }
    }
}


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

//提交前检查
function check() {
    let errorNum = 0;
    let arr = [];
    //检查多选是否至少选了两个
    let multiQuestionBoxes = document.querySelectorAll(".multiQuestionBox");
    for (let i = 0; i < multiQuestionBoxes.length; i++) {
        let checkBoxes = multiQuestionBoxes[i].querySelectorAll("input[type='checkbox']");
        let cnt = 0;
        for (let i = 0; i < checkBoxes.length; i++) {
            if (checkBoxes[i].checked) cnt++;
        }
        if (cnt < 2) {
            errorNum = 1;
        }
    }
    //检查问卷多选是否至少选了两个
    let qnQuestionBoxes = document.querySelectorAll(".qnQuestionBox");
    for (let i = 0; i < qnQuestionBoxes.length; i++) {
        console.log(qnQuestionBoxes[i]);
        let checkBoxes = qnQuestionBoxes[i].querySelectorAll("input[type='checkbox']");
        let cnt = 0;
        for (let i = 0; i < checkBoxes.length; i++) {
            if (checkBoxes[i].checked) cnt++;
        }
        if (cnt < 2 && checkBoxes.length > 0) {
            errorNum = 2;
        }
    }
    //出错提示弹窗
    if (errorNum) {
        let h1 = myalert.getElementsByTagName("h1")[0];
        if (errorNum === 1) {
            h1.innerHTML = "多选题请至少选择两个选项";
        } else if (errorNum === 2) {
            h1.innerHTML = "多选题请至少选择两个选项!";
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
myform.onsubmit = () => {
    if (checkDeadline()&&check())
        return true;
    else
        return false;
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

//比较收集是否截止
function checkDeadline() {
    let nowtime = new Date().getTime(); // 现在时间转换为时间戳
    let futruetime = new Date(Object.values(formData)[2]).getTime(); // 截止时间转换为时间戳
    let msec = futruetime - nowtime; // 毫秒 截止时间-现在时间
    let time = (msec / 1000);  // 毫秒/1000
    let day = parseInt(time / 86400); // 天  24*60*60*1000
    let hour = parseInt(time / 3600) - 24 * day;    // 小时 60*60 总小时数-过去的小时数=现在的小时数
    let minute = parseInt(time % 3600 / 60); // 分 -(day*24) 以60秒为一整份 取余 剩下秒数 秒数/60 就是分钟数
    let second = parseInt(time % 60);  // 以60秒为一整份 取余 剩下秒数
    if (time <= 0) {
        document.getElementById("refuse-submit").style.display = "flex";
        return false;
    }
    return true;
}

//将文本域中换行显示在div中
function textareaToDiv(val) {
    val = val.replace(/\r\n/g, '<br/>'); //IE9、FF、chrome
    val = val.replace(/\n/g, '<br/>'); //IE7-8
    val = val.replace(/\s/g, ' '); //空格处理
    return val;
}

addLoadEvent(checkDeadline);
addLoadEvent(processFormData);
addLoadEvent(creatQuestion);
addLoadEvent(()=>{
    description.innerHTML = textareaToDiv(description.innerHTML);
});