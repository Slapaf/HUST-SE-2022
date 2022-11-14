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
  let newli = document.createElement("li");
  let newh = document.createElement("h1");
  let inputTopic = document.createElement("div");
  inputTopic.innerHTML = topicName;
  inputTopic.className = "readOnlyInput";
  let detail = document.createElement("div");
  detail.className = "detail";
  detail.innerHTML = textareaToDiv(detailText);
  let inputContent = document.createElement("div");
  inputContent.className = "inputContent";
  questionList.appendChild(newli);
  newli.appendChild(newh);
  newh.appendChild(inputTopic);
  if (detail.innerHTML) {
    newli.appendChild(detail);
  }
  newli.appendChild(inputContent);
  //加id，加name
  newli.id = question_id.toString();
}

//添加单选/多选
function creatSingleOrMultiple(op, topicName, detailText) {
  let newli = document.createElement("li");
  newli.id = question_id.toString();
  let newh = document.createElement("h1");
  let inputTopic = document.createElement("div");
  inputTopic.value = topicName;
  inputTopic.className = "readOnlyInput";
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
    inputChoice.disabled = "disabled";
    let newlabel = document.createElement("label");
    newlabel.innerHTML = ABCD[i];
    opBox.appendChild(inputChoice);
    opBox.appendChild(newlabel);
    qBox.appendChild(opBox);
  }
  questionList.appendChild(newli);
  newli.appendChild(newh);
  newh.appendChild(inputTopic);
  if (detail.innerHTML) {
    newli.appendChild(detail);
  }
  newli.appendChild(qBox);
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
  let inputTopic = document.createElement("div");
  inputTopic.innerHTML = topicName;
  inputTopic.className = "readOnlyInput";
  inputTopic.id = question_id;
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
    inputChoice.disabled = "disabled";
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
  if (detail.innerHTML) {
    newli.appendChild(detail);
  }
  newli.appendChild(qBox);
}

// TODO:按照这个格式传数据
let jsonFromHtml = {
  "1_collectionTitle": "核酸检测",
  "2_collector": "张三",
  "3_deadline": "2022-11-15 15:23:09",
  "4_description": "",
  "5_question_name1": "姓名",
  "6_detail1": "",
  "7_submit_name1": "王广凯",
  "8_question_sno2": "学号",
  "9_detail2": "",
  "10_submit_sno2": "U202012345",
  "11_question_file3": "文件",
  "12_detail3": "",
  "13_submit_file3": "系统设计.md",
  "14_question_radio4": "单选题",
  "15_detail4": "",
  "16_checked_radio4": "A",
  "17_submit_radio4": "B",
  "18_question_multipleChoice5": "多选题",
  "19_detail5": "",
  "20_checked_mulans5": "C",
  "21_checked_mulans5": "D",
  "22_submit_mulans5": "A",
  "23_submit_mulans5": "B",
  "24_question_qnaire6": "问卷题目",
  "25_detail6": "是否已做核酸",
  "26_qn_option6": "是",
  "27_qn_option6": "否",
  "28_submit_qnaire6": "2",
};

let tmp_json = document.getElementById("collection").innerHTML;
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

//将文本域中换行显示在div中
function textareaToDiv(val) {
  val = val.replace(/\r\n/g, "<br/>"); //IE9、FF、chrome
  val = val.replace(/\n/g, "<br/>"); //IE7-8
  val = val.replace(/\s/g, " "); //空格处理
  return val;
}

addLoadEvent(processFormData);
addLoadEvent(creatQuestion);
addLoadEvent(() => {
  description.innerHTML = textareaToDiv(description.innerHTML);
});

function loadXMLDoc() {
  let xmlhttp;
  if (window.XMLHttpRequest) {
    // IE7+, Firefox, Chrome, Opera, Safari 浏览器执行代码
    xmlhttp = new XMLHttpRequest();
  } else {
    // IE6, IE5 浏览器执行代码
    xmlhttp = new ActiveXObject("Microsoft.XMLHTTP");
  }
  xmlhttp.onreadystatechange = function () {
    if (xmlhttp.readyState == 4 && xmlhttp.status == 200) {
      document.getElementById("myDiv").innerHTML = xmlhttp.responseText;
    }
  };
  xmlhttp.open("GET", "/try/ajax/demo_get.php", true);
  xmlhttp.send();
}
