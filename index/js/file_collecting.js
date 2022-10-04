const ul = document.querySelector(".main>ul");
const lis = ul.getElementsByTagName("li");
const li1=lis[0];
const li2=lis[1];
const rem = ul.getElementsByClassName("removeTopic");
const rem1=rem[0];
const rem2=rem[1];
const op_name = document.getElementById("op-name");
const op_file = document.getElementById("op-file");
const op_sno = document.getElementById("op-sno");
const btn_for_add = document.querySelector("#btn-for-add");
const popup = document.querySelector(".popup");

btn_for_add.onclick = () => {
  popup.classList.toggle("show");
};

rem1.addEventListener("click",()=>{
    ul.removeChild(li1);
})
rem2.addEventListener("click",()=>{
    ul.removeChild(li2);
})

op_name.addEventListener("click", () => {
  //新建一些元素节点
  let newli = document.createElement("li");
  let newh1 = document.createElement("h1");
  let newinput_title = document.createElement("input");
  newinput_title.type = "text";
  newinput_title.value = "姓名";
  let newinput_content = document.createElement("input");
  newinput_content.type = "text";
  newinput_content.disabled = "disabled";
  newinput_content.placeholder = "此项由提交者填写";
  let newbtn = document.createElement("button");
  newbtn.className = "removeTopic";
  //把各元素节点插到其父元素下
  newbtn.appendChild(document.createTextNode("删除题目"));
  newh1.appendChild(newinput_title);
  newli.appendChild(newh1);
  newli.appendChild(newinput_content);
  newli.appendChild(newbtn);
  ul.appendChild(newli);
  btn_for_add.onclick();
  //给新增的题目添加删除事件
  newbtn.addEventListener("click",()=>{
    ul.removeChild(newli);
  })
});

op_sno.addEventListener("click", () => {
  //新建一些元素节点
  let newli = document.createElement("li");
  let newh1 = document.createElement("h1");
  let newinput_title = document.createElement("input");
  newinput_title.type = "text";
  newinput_title.value = "学号";
  let newinput_content = document.createElement("input");
  newinput_content.type = "text";
  newinput_content.disabled = "disabled";
  newinput_content.placeholder = "此项由提交者填写";
  let newbtn = document.createElement("button");
  newbtn.className = "removeTopic";
  //把各元素节点插到其父节点下
  newbtn.appendChild(document.createTextNode("删除题目"));
  newh1.appendChild(newinput_title);
  newli.appendChild(newh1);
  newli.appendChild(newinput_content);
  newli.appendChild(newbtn);
  ul.appendChild(newli);
  btn_for_add.onclick();
  //给新增的题目添加删除事件
  newbtn.addEventListener("click",()=>{
    ul.removeChild(newli);
  })
});
