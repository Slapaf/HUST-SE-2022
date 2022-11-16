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
function createNameOrSnoOrFile(op, topicName, detailText, submitContent) {
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
  inputContent.innerHTML = submitContent;
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
function createSingleOrMultiple(
  op,
  topicName,
  detailText,
  checkedChoiceArr,
  correctAnswerArr
) {
  let newli = document.createElement("li");
  newli.id = question_id.toString();
  let newh = document.createElement("h1");
  let inputTopic = document.createElement("div");
  inputTopic.innerHTML = topicName;
  inputTopic.className = "readOnlyInput";
  let detail = document.createElement("div");
  detail.className = "detail";
  detail.innerHTML = textareaToDiv(detailText);
  let qBox = document.createElement("div");
  qBox.className = op === "single" ? "singleQuestionBox" : "multiQuestionBox";
  if (op === "single") {
    qBox = addChoice_for_filePreview(0, checkedChoiceArr, correctAnswerArr);
  } else {
    qBox = addChoice_for_filePreview(1, checkedChoiceArr, correctAnswerArr);
  }
  let correctAnswerBox = document.createElement("div");
  correctAnswerBox.className = "correctAnswerBox";
  correctAnswerBox.innerHTML = "正确答案：";
  for (let i = 0; i < correctAnswerArr.length; i++) {
    correctAnswerBox.innerHTML += " " + correctAnswerArr[i] + " ";
  }
  questionList.appendChild(newli);
  newli.appendChild(newh);
  newh.appendChild(inputTopic);
  if (detail.innerHTML) {
    newli.appendChild(detail);
  }
  newli.appendChild(qBox);
  newli.appendChild(correctAnswerBox);
}

//添加单选题/多选题
function addChoice_for_filePreview(op, checkedChoiceArr, correctAnswerArr) {
  let newqbox = document.createElement("div");
  let optionArr = ["A", "B", "C", "D"];
  let correctClass = op === 0 ? "correctSingle" : "correctMulti";
  let wrongClass = op === 0 ? "wrongSingle" : "wrongMulti";
  for (let i = 0; i < 4; i++) {
    let inputChoice = document.createElement("input");
    inputChoice.type = op === 0 ? "radio" : "checkbox"; //op=0是单选，op=1是多选
    inputChoice.value = optionArr[i];
    inputChoice.disabled = true;
    inputChoice.className = op === 0 ? "singleOption" : "multiOption";
    let newop = document.createElement("span");
    newop.className = "optionContent";
    newop.appendChild(document.createTextNode(optionArr[i]));
    newqbox.appendChild(inputChoice);
    newqbox.appendChild(newop);
    if (checkedChoiceArr.indexOf(optionArr[i].charCodeAt() - 65) != -1) {
      if (correctAnswerArr.indexOf(optionArr[i]) != -1) {
        inputChoice.classList.toggle(correctClass);
      } else {
        inputChoice.classList.toggle(wrongClass);
      }
    }
  }
  for (let i = 0; i < checkedChoiceArr.length; i++) {
    newqbox.children[checkedChoiceArr[i] * 2].checked = "true";
  }
  for (let i = 0; i < checkedChoiceArr.length; i++) {
    checkedChoiceArr[i] = String.fromCharCode(checkedChoiceArr[i] + 65);
  }
  return newqbox;
}

//参数：编号，题目，详情描述，选项数，选项内容（数组），选择类型（单选/多选）
function createQuestionnaire(
  topicName,
  detailText,
  qnOptionArr,
  checkedChoiceArr,
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
  let flag = 0;
  for (let i = 0; i < qnOptionArr.length; i++) {
    flag = 0;
    for (let j = 0; j < checkedChoiceArr.length; j++) {
      if (checkedChoiceArr[j] - 1 === i) {
        flag = 1;
        break;
      }
    }
    if (flag) {
      qBox.appendChild(
        addQuestion_for_filePreview(chooseType, qnOptionArr[i], true)
      );
    } else {
      qBox.appendChild(
        addQuestion_for_filePreview(chooseType, qnOptionArr[i], false)
      );
    }
  }
  questionList.appendChild(newli);
  newli.appendChild(newh);
  newh.appendChild(inputTopic);
  if (detail.innerHTML) {
    newli.appendChild(detail);
  }
  newli.appendChild(qBox);
}

//添加一个问卷选项(传参触发)
function addQuestion_for_filePreview(chooseType, qnOptionText, if_checked) {
  let opBox = document.createElement("div");
  opBox.className = "qnOption";
  let inputChoice = document.createElement("input");
  inputChoice.className = "qnOptionChoice";
  inputChoice.type = chooseType === "single" ? "radio" : "checkbox";
  inputChoice.disabled = "disabled";
  inputChoice.checked = if_checked;
  let optionContent = document.createElement("div");
  optionContent.className = "qnOptionContent";
  optionContent.innerHTML = textareaToDiv(qnOptionText);
  opBox.appendChild(inputChoice);
  opBox.appendChild(optionContent);
  return opBox;
}

// TODO:按照这个格式传数据
let sample_json = {
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
  "17_submit_radio4": "C",
  "18_question_multipleChoice5": "多选题",
  "19_detail5": "",
  "20_checked_mulans5": "A",
  "21_checked_mulans5": "C",
  "22_submit_mulans5": "A",
  "23_submit_mulans5": "C",
  "24_submit_mulans5": "D",
  "25_question_qnaire6": "问卷题目",
  "26_detail6": "是否已做核酸",
  "27_qn_option6": "是",
  "28_qn_option6": "否",
  "29_submit_qnaire6": "1",
  "30_submit_qnaire6": "2",
};

let tmp_json = document.getElementById("collection").innerHTML;
tmp_json = eval("(" + tmp_json + ")"); // ! 有风险
console.log(tmp_json);
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

function createQuestion() {
  collectionTitle.innerHTML = Object.values(formData)[0];
  collector.innerHTML = Object.values(formData)[1];
  deadline.innerHTML = Object.values(formData)[2];
  description.innerHTML = Object.values(formData)[3];
  for (let i = 0; i < formDataLen; i++) {
    let q = formDataArr[i];
    let keys = Object.keys(formDataArr[i]);
    let values = Object.values(formDataArr[i]);
    question_id++;
    if (keys[0].indexOf("question_name") != -1) {
      createNameOrSnoOrFile("name", values[0], values[1], values[2]);
    } else if (keys[0].indexOf("question_sno") != -1) {
      createNameOrSnoOrFile("sno", values[0], values[1], values[2]);
    } else if (keys[0].indexOf("question_file") != -1) {
      createNameOrSnoOrFile("file", values[0], values[1], values[2]);
    } else if (keys[0].indexOf("question_radio") != -1) {
      let k =
        values[values.length - 1].toString().charCodeAt() - "A".charCodeAt();
      let t = values[values.length - 2].toString();
      createSingleOrMultiple("single", values[0], values[1], [k], [t]);
    } else if (keys[0].indexOf("question_multipleChoice") != -1) {
      let submitArr = [];
      let correctArr = [];
      for (let j = 0; j < keys.length; j++) {
        if (keys[j].indexOf("submit_mulans") != -1) {
          submitArr.push(values[j].toString().charCodeAt() - "A".charCodeAt());
        } else if (keys[j].indexOf("checked_mulans") != -1) {
          correctArr.push(values[j].toString());
        }
      }
      createSingleOrMultiple(
        "multiple",
        values[0],
        values[1],
        submitArr,
        correctArr
      );
    } else {
      let qnOptionArr = [];
      let checkedChoiceArr = [];
      for (let j = 0; j < keys.length; j++) {
        if (keys[j].indexOf("qn_option") != -1) {
          qnOptionArr.push(values[j]);
        } else if (keys[j].indexOf("submit_qnaire") != -1) {
          checkedChoiceArr.push(values[j]);
        }
      }
      let chooseType = checkedChoiceArr.length > 1 ? "multiple" : "single";
      createQuestionnaire(
        values[0],
        values[1],
        qnOptionArr,
        checkedChoiceArr,
        chooseType
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
console.log(formDataArr);
addLoadEvent(createQuestion);
// addLoadEvent(() => {
//   description.innerHTML = textareaToDiv(description.innerHTML);
// });
