const chartPanel = document.querySelector("#chartPanel");
let chartId = 0;
let responseData = {};
let choiceData = {};
let qnaireData = {};

//创建饼状图
function createPieChart(chartContainer, chartTitle, chartData) {
  let newChart = document.createElement("div");
  newChart.className = "pieChart";
  newChart.id = "chartdiv" + ++chartId;
  chartContainer.appendChild(newChart);
  let root = am5.Root.new(newChart.id);
  root.setThemes([am5themes_Animated.new(root)]);
  var chart = root.container.children.push(
    am5percent.PieChart.new(root, {
      title: chartTitle,
      endAngle: 270,
    })
  );

  var series = chart.series.push(
    am5percent.PieSeries.new(root, {
      titleField: chartTitle,
      valueField: "value",
      categoryField: "category",
      endAngle: 270,
    })
  );

  series.states.create("hidden", {
    endAngle: -90,
  });

  series.data.setAll(chartData);
  series.appear(1000, 100);
}

//创建柱状图
function createColumnChart(chartTitle, chartData) {
  let newChart = document.createElement("div");
  newChart.className = "columnChart";
  newChart.id = "chartdiv" + ++chartId;
  chartPanel.appendChild(newChart);
  var root = am5.Root.new(newChart.id);
  root.setThemes([am5themes_Animated.new(root)]);
  var chart = root.container.children.push(
    am5xy.XYChart.new(root, {
      panX: true,
      panY: true,
      wheelX: "panX",
      wheelY: "zoomX",
      pinchZoomX: true,
    })
  );

  var cursor = chart.set("cursor", am5xy.XYCursor.new(root, {}));
  cursor.lineY.set("visible", false);

  var xRenderer = am5xy.AxisRendererX.new(root, { minGridDistance: 30 });
  xRenderer.labels.template.setAll({
    rotation: -90,
    centerY: am5.p50,
    centerX: am5.p100,
    paddingRight: 15,
  });

  var xAxis = chart.xAxes.push(
    am5xy.CategoryAxis.new(root, {
      maxDeviation: 0.3,
      categoryField: "question",
      renderer: xRenderer,
      tooltip: am5.Tooltip.new(root, {}),
    })
  );

  var yAxis = chart.yAxes.push(
    am5xy.ValueAxis.new(root, {
      maxDeviation: 0.3,
      renderer: am5xy.AxisRendererY.new(root, {}),
    })
  );

  var series = chart.series.push(
    am5xy.ColumnSeries.new(root, {
      name: "题目正确率",
      xAxis: xAxis,
      yAxis: yAxis,
      valueYField: "accuracy",
      sequencedInterpolation: true,
      categoryXField: "question",
      tooltip: am5.Tooltip.new(root, {
        labelText: "正确率：" + "{valueY}",
      }),
    })
  );

  series.columns.template.setAll({ cornerRadiusTL: 5, cornerRadiusTR: 5 });
  series.columns.template.adapters.add("fill", function (fill, target) {
    return chart.get("colors").getIndex(series.columns.indexOf(target));
  });

  series.columns.template.adapters.add("stroke", function (stroke, target) {
    return chart.get("colors").getIndex(series.columns.indexOf(target));
  });

  xAxis.data.setAll(chartData);
  series.data.setAll(chartData);

  series.appear(1000);
  chart.appear(1000, 100);
}

function createNameList(chartContainer, op, nameList) {
  let nameListContainer = document.createElement("div");
  nameListContainer.className = "nameListContainer";
  if (op === "choice") {
    let answerContainer = document.createElement("div");
    answerContainer.className = "answerContainer";
    answerContainer.innerHTML = "正确答案：" + nameList.correctAnswer;
    nameListContainer.appendChild(answerContainer);
    let ABCD = ["A", "B", "C", "D"];
    ABCD.forEach((e) => {
      let listHeader = document.createElement("ul");
      listHeader.className = "listHeader";
      let listBody = document.createElement("li");
      listBody.className = "listBody";
      listHeader.innerHTML = "选择" + e + "选项名单";
      nameList[e].forEach((name) => {
        listBody.innerHTML += name + " ";
      });
      listHeader.appendChild(listBody);
      nameListContainer.appendChild(listHeader);
      listHeader.onclick = () => {
        listBody.classList.toggle("show");
      };
    });
  }else if(op === "qnaire"){
    let values = Object.values(nameList);
    values.forEach(e => {
      let listHeader = document.createElement("ul");
      listHeader.className = "listHeader";
      let listBody = document.createElement("li");
      listBody.className = "listBody";
      listHeader.innerHTML = "选择\"" + e.optionName + "\"选项名单";
      e.people.forEach((name) => {
        listBody.innerHTML += name + " ";
      });
      listHeader.appendChild(listBody);
      nameListContainer.appendChild(listHeader);
      listHeader.onclick = () => {
        listBody.classList.toggle("show");
      };
    })
  }
  chartContainer.appendChild(nameListContainer);
}

//处理正确率，并建立“题目-正确率”柱状图
//在这里调用processChoiceData()
function processAccuracy(data_choice) {
  let values = Object.values(data_choice);
  let chartData = [];
  let optionData = {};
  values.forEach((e) => {
    optionData = {
      question: e.questionName,
      accuracy: e.accuracy,
    };
    chartData.push(optionData);
  });
  createColumnChart("", chartData);
  values.forEach((e) => {
    processChoiceData(e);
  });
}

//处理选择题数据，并建立“选项-选择人数”饼状图
function processChoiceData(question) {
  let chartData = [];
  let nameList = {};
  let optionData = {};
  let optionIndex = "";
  let peopleNumber = 0;
  let ABCD = ["A", "B", "C", "D"];
  ABCD.forEach((e) => {
    optionIndex = e;
    peopleNumber = question[e].length;
    optionData = {
      category: optionIndex,
      value: peopleNumber,
    };
    chartData.push(optionData);
  });
  let newChartContainer = document.createElement("div");
  newChartContainer.className = "chartContainer";
  chartPanel.appendChild(newChartContainer);
  createPieChart(newChartContainer, question.questionName, chartData);
  delete question.questionName;
  delete question.accuracy;
  nameList = question;
  createNameList(newChartContainer,"choice",nameList);
}

function processQnaireData(question) {
  let chartData = [];
  let nameList = {};
  let optionData = {};
  for (let i = 0; i < question["optionNumber"]; i++) {
    let option = question["option_" + (i + 1)];
    optionData = {
      category: option.optionName,
      value: option.peopleNumber,
    };
    chartData.push(optionData);
  }
  let newChartContainer = document.createElement("div");
  newChartContainer.className = "chartContainer";
  chartPanel.appendChild(newChartContainer);
  createPieChart(newChartContainer, question.questionName, chartData);
  delete question.questionName;
  delete question.optionNumber;
  nameList = question;
  createNameList(newChartContainer,"qnaire",nameList);
}

let data_choice = {
  question_1: {
    questionName: "单选题1",
    correctAnswer: "A",
    accuracy: 0.2,
    A: ["张庙松", "黄俊杰"],
    B: ["王广凯", "王梓熙"],
    C: ["张隽翊"],
    D: [],
  },
  question_2: {
    questionName: "多选题1",
    correctAnswer: "A B C D",
    accuracy: 0.8,
    A: ["张庙松", "黄俊杰"],
    B: ["王广凯", "王梓熙"],
    C: ["王广凯", "张隽翊", "张庙松"],
    D: ["张隽翊", "计胜翔", "张庙松"],
  },
};

let a = {
  questionName: "单选题1",
  correctAnswer: "A",
  accuracy: 0.2,
  A: ["张庙松", "黄俊杰"],
  B: ["王广凯", "王梓熙"],
  C: ["张隽翊"],
  D: [],
};

let b = {
  questionName: "你喜欢吃饭吗？",
  optionNumber: 3,
  option_1: {
    optionName: "喜欢",
    peopleNumber: 3,
    people: ["王广凯", "张隽翊", "王梓熙"],
  },
  option_2: {
    optionName: "不喜欢",
    peopleNumber: 0,
    people: [],
  },
  option_3: {
    optionName: "我喜欢吃屎",
    peopleNumber: 1,
    people: ["计胜翔"],
  },
};

let c = {
  correctAnswer: "A",
  A: ["张庙松", "黄俊杰"],
  B: ["王广凯", "王梓熙"],
  C: ["张隽翊"],
  D: [],
};

function sendRequest() {
  // XMLHttpRequest对象用于在后台与服务器交换数据
  var xhr = new XMLHttpRequest();
  xhr.open("GET", "/test", false);
  xhr.onreadystatechange = function () {
    // readyState == 4说明请求已完成
    if (xhr.readyState == 4) {
      if (xhr.status == 200 || xhr.status == 304) {
        responseData = JSON.parse(xhr.responseText);
        if (responseData) {
          choiceData = responseData.data_choice;
          qnaireData = responseData.data_qnaire;
          if (choiceData) {
            processAccuracy(choiceData);
          }
          if (qnaireData) {
            let values = Object.values(data_qnaire);
            values.forEach((e) => {
              processQnaireData(e);
            });
          }
        }
      }
    }
  };
  xhr.send();
}

processAccuracy(data_choice);
processQnaireData(b);
