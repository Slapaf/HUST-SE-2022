const questionList = document.querySelector("#question_list");
const collectionTitle = document.querySelector("#collectionTitle");
const collector = document.querySelector("#collector");
const deadline = document.querySelector("#deadline");
const discription = document.querySelector("#discription");
let qnum = 0;
let question_id = 0;

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
    detail.innerHTML = detailText;
    let inputContent = document.createElement("input");
    inputContent.type = op == "file" ? "file" : "text";
    inputContent.className = "inputContent";
    // ! DEBUG
    // if (op == "file") {
    //     inputContent.formEnctype = "multipart/form-data";
    // }
    questionList.appendChild(newli);
    newli.appendChild(newh);
    newh.appendChild(inputTopic);
    newli.appendChild(detail);
    newli.appendChild(inputContent);
    //加id，加name
    newli.id = question_id.toString();
    inputTopic.name = "question_" + op + question_id;
    inputContent.name = "submit_" + op + question_id;
}

// creatNameOrSnoOrFile("file","文件","hahahahahahaha");
// creatNameOrSnoOrFile("sno", "学号", "hahahahahahaha");

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
    detail.innerHTML = detailText;
    let qBox = document.createElement("div");
    qBox.className = op === "single" ? "singleQuestionBox" : "multiQuestionBox";
    let ABCD = ["A", "B", "C", "D"];
    for (let i = 0; i < 4; i++) {
        let opBox = document.createElement("div");
        opBox.className = op === "single" ? "radioOption" : "multiOption";
        let inputChoice = document.createElement("input");
        inputChoice.type = op === "single" ? "radio" : "checkbox";
        inputChoice.name =
            "submit_checked_" + (op === "single" ? "radio" : "mulans") + question_id;
        inputChoice.value = ABCD[i];
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
    //加id，加name
}

// creatSingleOrMultiple(0,"single", "单选", "这是单选");
// creatSingleOrMultiple("multiple", "多选", "这是多选");

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
    detail.innerHTML = detailText;
    let qBox = document.createElement("div");
    qBox.className = "qnQuestionBox";
    for (let i = 0; i < qnOptionNum; i++) {
        let opBox = document.createElement("div");
        opBox.className = "qnOption";
        let inputChoice = document.createElement("input");
        inputChoice.type = chooseType == "single" ? "radio" : "checkbox";
        inputChoice.name = "submit_checked_qnaire" + question_id;
        inputChoice.value = (i + 1).toString();
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

// creatQuestionnaire(
//   "问卷",
//   "你喜欢吃饭吗？",
//   3,
//   ["喜欢", "不喜欢", "随便"],
//   "single"
// );
// creatQuestionnaire(0,"问卷","你喜欢吃饭吗？",3,["喜欢","不喜欢","随便"],"multiple");

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
    discription.innerHTML = Object.values(formData)[3];
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

processFormData();
creatQuestion();
console.log(formDataArr);
console.log(formData);
