const chartPanel = document.querySelector("#chartPanel");
let chartId = 0;
let responseData = {};
let choiceData = {};
let qnaireData = {};

//创建饼状图
function createPieChart(chartContainer, chartData) {
  let newChart = document.createElement("div");
  newChart.className = "pieChart";
  newChart.id = "chartdiv" + ++chartId;
  chartContainer.appendChild(newChart);
  let root = am5.Root.new(newChart.id);
  root.setThemes([am5themes_Animated.new(root)]);
  var chart = root.container.children.push(
    am5percent.PieChart.new(root, {
      endAngle: 270,
    })
  );
  var series = chart.series.push(
    am5percent.PieSeries.new(root, {
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
    let newdiv = document.createElement("div");
    nameListContainer.appendChild(newdiv);
    let listHeaders = document.createElement("ul");
    listHeaders.className = "listHeaders";
    newdiv.appendChild(listHeaders);
    let listBodies = document.createElement("ul");
    listBodies.className = "listBodies";
    newdiv.appendChild(listBodies);
    let ABCD = ["A", "B", "C", "D"];
    ABCD.forEach((e) => {
      let listTitle = document.createElement("li");
      listTitle.className = "listTitle";
      listTitle.innerHTML = "选择" + e + "选项名单";
      listHeaders.appendChild(listTitle);
      let listContent = document.createElement("li");
      listContent.className = "listContent";
      listBodies.appendChild(listContent);
      nameList[e].forEach((name) => {
        listContent.innerHTML += name + " ";
      });
    });
  } else if (op === "qnaire") {
    let values = Object.values(nameList);
    let listHeaders = document.createElement("ul");
    listHeaders.className = "listHeaders";
    nameListContainer.appendChild(listHeaders);
    let listBodies = document.createElement("ul");
    listBodies.className = "listBodies";
    nameListContainer.appendChild(listBodies);
    values.forEach((e) => {
      let listTitle = document.createElement("li");
      listTitle.className = "listTitle";
      listTitle.innerHTML = '选择"' + e.optionName + '"选项名单';
      let listContent = document.createElement("li");
      listContent.className = "listContent";
      e.people.forEach((name) => {
        listContent.innerHTML += name + " ";
      });
      listHeaders.appendChild(listTitle);
      listBodies.appendChild(listContent);
    });
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
  let chartTitle = document.createElement("div");
  chartTitle.className = "chartTitle";
  chartTitle.innerHTML = question.questionName;
  newChartContainer.appendChild(chartTitle);
  createPieChart(newChartContainer, chartData);
  delete question.questionName;
  delete question.accuracy;
  nameList = question;
  createNameList(newChartContainer, "choice", nameList);
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
  let chartTitle = document.createElement("div");
  chartTitle.className = "chartTitle";
  chartTitle.innerHTML = question.questionName;
  newChartContainer.appendChild(chartTitle);
  createPieChart(newChartContainer, chartData);
  delete question.questionName;
  delete question.optionNumber;
  nameList = question;
  createNameList(newChartContainer, "qnaire", nameList);
}

function sendRequest() {
  // XMLHttpRequest对象用于在后台与服务器交换数据
  var xhr = new XMLHttpRequest();
  let url = "/statistics?collectionId=" + getCollectionId();
  xhr.open("GET", url, false);
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
            let values = Object.values(qnaireData);
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

function getCollectionId() {
  let url = document.location.toString();
  var arrUrl = url.split("//");
  var start = arrUrl[1].lastIndexOf("/");
  var relUrl = arrUrl[1].substring(start + 1); //stop省略，截取从start开始到结尾的所有字符
  if (relUrl.indexOf("?") != -1) {
    relUrl = relUrl.split("?")[0];
  }
  console.log(relUrl);
  return relUrl;
}

/*
 * 加密函数
 * @param message: 待加密的信息
 * @return: 加密后的信息
 */
function encryption(message) {
    return window.btoa(encodeURIComponent(message));
}

/*
 * 解密函数
 * @param message: 待解密的信息
 * @return: 解密后的信息
 */
function decryption(message) {
    return decodeURIComponent(window.atob(message));
}