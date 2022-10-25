const questionList = document.querySelector("#question_list");
const collectionTitle = document.querySelector("#collectionTitle");
const collector = document.querySelector("#collector");
const deadline = document.querySelector("#deadline");
const discription = document.querySelector("#discription");
let qnum = 0;

//添加名字/学号/文件
function creatNameOrSnoOrFile(op, topicName, detailText) {
  //要给inputContent加name
  let newli = document.createElement("li");
  let newh = document.createElement("h1");
  let inputTopic = document.createElement("input");
  inputTopic.type = "text";
  inputTopic.value = topicName;
  inputTopic.className = "disabledInput";
  inputTopic.disabled = "disabled";
  let detail = document.createElement("div");
  detail.className = "detail";
  detail.innerHTML = detailText;
  let inputContent = document.createElement("input");
  inputContent.type = op == "file" ? "file" : "text";
  inputContent.className = "inputContent";
  questionList.appendChild(newli);
  newli.appendChild(newh);
  newh.appendChild(inputTopic);
  newli.appendChild(detail);
  newli.appendChild(inputContent);
}

// creatNameOrSnoOrFile("file","文件","hahahahahahaha");
creatNameOrSnoOrFile("sno","学号","hahahahahahaha");

//添加单选/多选
function creatSingleOrMultiple(op, topicName, detailText) {
  //要给inputChoice加name
  let newli = document.createElement("li");
  let newh = document.createElement("h1");
  let inputTopic = document.createElement("input");
  inputTopic.type = "text";
  inputTopic.value = topicName;
  inputTopic.className = "disabledInput";
  inputTopic.disabled = "disabled";
  let detail = document.createElement("div");
  detail.className = "detail";
  detail.innerHTML = detailText;
  let qBox = document.createElement("div");
  qBox.className = op === "single" ? "singleQuestionBox" : "multiQuestionBox";
  let ABCD = ["A", "B", "C", "D"];
  for (let i = 0; i < 4; i++) {
    let opBox = document.createElement("div");
    opBox.className = op === "single" ? "radioOption" : "multiOption";
    let inputChoice = document.createElement("input");
    inputChoice.type = op === "single" ? "radio" : "checkbox";
    let newlabel = document.createElement("label");
    newlabel.innerHTML = ABCD[i];
    opBox.appendChild(inputChoice);
    opBox.appendChild(newlabel);
    qBox.appendChild(opBox);
  }
  questionList.appendChild(newli);
  newli.appendChild(newh);
  newh.appendChild(inputTopic);
  newli.appendChild(detail);
  newli.appendChild(qBox);
}

// creatSingleOrMultiple(0,"single", "单选", "这是单选");
creatSingleOrMultiple("multiple", "多选", "这是多选");

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
  inputTopic.className = "disabledInput";
  inputTopic.disabled = "disabled";
  let detail = document.createElement("div");
  detail.className = "detail";
  detail.innerHTML = detailText;
  let qBox = document.createElement("div");
  qBox.className = "qnQuestionBox";
  for (let i = 0; i < qnOptionNum; i++) {
    let opBox = document.createElement("div");
    opBox.className = "qnOption";
    let inputChoice = document.createElement("input");
    inputChoice.type = chooseType == "single" ? "radio" : "checkbox";
    let optionContent = document.createElement("div");
    optionContent.className = "qnOptionContent";
    optionContent.innerHTML = qnOptionContent[i];
    opBox.appendChild(inputChoice);
    opBox.appendChild(optionContent);
    qBox.appendChild(opBox);
  }
  questionList.appendChild(newli);
  newli.appendChild(newh);
  newh.appendChild(inputTopic);
  newli.appendChild(detail);
  newli.appendChild(qBox);
}

creatQuestionnaire("问卷","你喜欢吃饭吗？",3,["喜欢","不喜欢","随便"],"single");
// creatQuestionnaire(0,"问卷","你喜欢吃饭吗？",3,["喜欢","不喜欢","随便"],"multiple");
