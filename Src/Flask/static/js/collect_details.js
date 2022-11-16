var arr = []; //存放应交名单
var len = arr.length;

var tab_list = document.querySelector(".tab_list");
var lis = tab_list.querySelectorAll("li");
var items = document.querySelectorAll(".item");
const x = document.getElementById("list_body");

// function idx_str_to_int(idx_str) {
//   if (idx_str >= "0" && idx_str <= "9") {
//     return parseInt(idx_str);
//   }
//   return parseInt(idx_str) - 10 + "a".charCodeAt();
// }
//
// function id_str_transfer(id_str) {
//   if (id_str >= "0" && id_str <= "9") {
//     return id_str;
//   }
//   return String.fromCharCode(parseInt(id_str) - 10 + "a".charCodeAt());
// }

// TODO 获取提交信息更新页面，从 mycollection 页面进入
// function getData() {
//     let tmp_json = JSON.parse(document.getElementById('json_object').innerHTML);
//     let json_length = document.getElementById('json_length').innerHTML;
//     console.log(tmp_json);
//     for (let i = 0; i < json_length; i++) {
//         // ! 未验证正确性
//         addmember(tmp_json[i].submitter_order_idx, tmp_json[i].submitter_name,
//             tmp_json[i].submit_time, tmp_json[i].file_submitted_count, tmp_json[i].file_submitted_list);
//     }
// }

Array.prototype.indexOf = function (val) {
  for (var i = 0; i < this.length; i++) {
    if (this[i] == val) return i;
  }
  return -1;
};
Array.prototype.remove = function (val) {
  var index = this.indexOf(val);
  if (index > -1) {
    this.splice(index, 1);
  }
};

for (var i = 0; i < lis.length; i++) {
  lis[i].setAttribute("index", i);
  lis[i].onclick = function () {
    for (var i = 0; i < lis.length; i++) {
      lis[i].className = "";
    }
    this.className = "current";
    const index = this.getAttribute("index");
    for (var i = 0; i < items.length; i++) {
      items[i].style.display = "none";
    }
    items[index].style.display = "block";
  };
} //实现tab栏切换

// * 添加姓名弹窗
function click0() {
  let popLayer = document.getElementById("popLayer");
  popLayer.style.display = "block";
  let popup = document.getElementById("popup");
  popup.style.display = "block";
}

// * 在 namebox 中添加名字，关闭弹窗
function click1() {
  let popup = document.getElementById("popup");
  popup.style.display = "none";
  addname();
  document.getElementById("textarea").value = "";
  let popLayer = document.getElementById("popLayer");
  popLayer.style.display = "none";
}

function click2() {
  let popup1 = document.getElementById("popup1");
  let del = document.getElementById("return");
  popup1.style.display = "none";
  let popLayer = document.getElementById("popLayer");
  popLayer.style.display = "none";
  del.remove();
}

// * 添加名字
function addname() {
  let str = document.getElementById("textarea").value;
  // * 赋值
  document.getElementById("name_data").value = str;
  if (str != "") {
    let n = str.split(/[\s\n]+|\,+|[\r\n]+/); //将 textarea 中字符串以,和换行符切分
    let flag = 1;
    if (n.length != 0) {
      let list = n[0];
      while (flag < n.length) {
        list = list + " " + n[flag];
        flag++;
      }
      document.getElementById("name_data").value = list;
    }
  }
}

function addfile(file_submitted_list) {
  let popup = document.getElementById("return");
  let i = 0;
  while (i < file_submitted_list.length) {
    let para = document.createElement("div");
    para.title = file_submitted_list[i];
    para.className = "filelist";
    popup.appendChild(para);
    para.appendChild(document.createTextNode(para.title));
    i++;
  }
}

function addmember(
  submitter_order_idx,
  submitter_name,
  submit_time,
  file_submitted_count,
  file_submitted_list
) {
  //新建元素节点
  let listmember = document.createElement("div");
  let membername = document.createElement("div");
  let memberdate = document.createElement("div");
  let membernumber = document.createElement("div");
  let membercondition = document.createElement("div");
  let memberpreview = document.createElement("a");
  // ! 11/08 添加 idx
  let memberid = document.createElement("div");
  // ! 11/08
  //连接节点
  x.appendChild(listmember);
  // ! 11/08
  listmember.appendChild(memberid);
  // ! 11/08
  listmember.appendChild(membername);
  listmember.appendChild(memberdate);
  listmember.appendChild(membernumber);
  listmember.appendChild(membercondition);
  listmember.appendChild(memberpreview);
  //给节点赋值
  // membername.title = "王广凯";
  membername.title = submitter_name;
  // memberdate.title = "2022-10-01 23:59";
  memberdate.title = submit_time;
  // membernumber.title = "211";
  membernumber.title = file_submitted_count;
  membercondition.title = "查看文件";
  memberpreview.title = "查看";
  // ! 11/08 memberid
  // memberid.title = id_str_transfer(submitter_order_idx);
  memberid.title = encryption(submitter_order_idx);
  // ! 11/08
  membername.appendChild(document.createTextNode(membername.title));
  // ! 11/08
  memberdate.appendChild(document.createTextNode(memberdate.title));
  membernumber.appendChild(document.createTextNode(membernumber.title));
  membercondition.appendChild(document.createTextNode(membercondition.title));
  memberpreview.appendChild(document.createTextNode(memberpreview.title));
  listmember.className = "list_member";
  membername.className = "member_name";
  memberdate.className = "member_date";
  membernumber.className = "member_number";
  membercondition.className = "member_condition";
  memberpreview.className = "member_preview";
  // ! 11/08
  memberid.style.display = "none";
  // ! 11/08
  if (membernumber.title !== "0") {
    membercondition.onclick = function () {
      let popup1 = document.getElementById("popup1");
      popup1.style.display = "block";
      let popLayer = document.getElementById("popLayer");
      popLayer.style.display = "block";
      let wgk = document.getElementById("popup-content");
      let jsx = document.createElement("div");
      jsx.id = "return";
      wgk.appendChild(jsx);
      addfile(file_submitted_list);
    };
  } else {
    membercondition.className = "member_condition1";
  }
  //查看提交详情
  memberpreview.onclick = () => {
    memberpreview.href =
      "/file_preview?collectionId=" +
      getCollectionId() +
      "&submissionId=" +
      memberid.title;

    memberpreview.target = "_blank";
  };
}

function getCollectionId() {
  let url = document.location.toString();
  var arrUrl = url.split("//");
  var start = arrUrl[1].lastIndexOf("/");
  var relUrl = arrUrl[1].substring(start + 1); //stop省略，截取从start开始到结尾的所有字符
  if (relUrl.indexOf("?") != -1) {
    relUrl = relUrl.split("?")[0];
  }
  return relUrl;
}

let downloadFile = document.querySelector("#downloadFile");
let downloadExcel = document.querySelector("#downloadExcel");

function getExcel() {
  downloadExcel.href =
    "/download?collectionId=" + getCollectionId() + "&fileType=excel";
}

function getfile() {
  downloadFile.href =
    "/download?collectionId=" + getCollectionId() + "&fileType=zip";
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