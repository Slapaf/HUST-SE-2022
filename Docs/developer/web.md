# Web 网页设计

## 1. 网页跳转逻辑

网页之间的关联结构如下图所示。

![网页跳转逻辑](../images/%E7%BD%91%E9%A1%B5%E8%B7%B3%E8%BD%AC%E9%80%BB%E8%BE%91.png)

## 2. 关键 JS 代码

### 2.1 复选框更新逻辑

```javascript
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
```

### 2.2 收集题目创建逻辑

```javascript
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
      let k =
        values[values.length - 1].toString().charCodeAt() - "A".charCodeAt();
      createSingleChoice(values[0], values[1], 1, [k]);
    } else if (keys[0].indexOf("question_multipleChoice") != -1) {
      let cnt = 0;
      let tmp = [];
      for (let j = 0; j < keys.length; j++) {
        if (keys[j].indexOf("checked_mulans") != -1) {
          cnt++;
          tmp.push(values[j].toString().charCodeAt() - "A".charCodeAt());
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
      createQuestionnaire(values[0], values[1], qnOptionContent, multi);
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
```

### 2.3 可拖拽实现逻辑

```javascript
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
  let dragElementType =
    dragElement.getElementsByClassName("input-topic")[0].name;
  let dropElementType =
    dropElement.getElementsByClassName("input-topic")[0].name;
  if (
    dragElementType === "question_name" ||
    dragElementType === "question_sno"
  ) {
    if (
      dropElementType === "question_name" ||
      dropElementType === "question_sno"
    ) {
      if (dragElement.nextSibling === dropElement) {
        for_checkbox("swap", dropId, dragId);
      } else {
        for_checkbox("swap", dragId, dropId);
      }
    } else {
      let next = dropElement.nextSibling;
      let nextType = null;
      let flag = 0;
      while (next) {
        nextType = next.getElementsByClassName("input-topic")[0].name;
        if (
          nextType &&
          (nextType === "question_name" || nextType === "question_sno")
        ) {
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
    if (dragElement.nextSibling === dropElement) {
      ul.insertBefore(dropElement, dragElement);
    } else {
      ul.insertBefore(dragElement, dropElement);
    }
  }
}
```
