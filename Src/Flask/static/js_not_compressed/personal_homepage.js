const nav_item1 = document.querySelector("#item1");
const nav_item2 = document.querySelector("#item2");
const nav_item3 = document.querySelector("#item3");
const user_information = document.querySelector(".user_information");
const change_password = document.querySelector(".change_password");
const data1 = document.getElementById("data1");
const data2 = document.getElementById("data2");
let countdown = 1;

nav_item1.onclick = () => {
    user_information.style.display = "flex";
    change_password.style.display = "none";
};

nav_item2.onclick = () => {
    user_information.style.display = "none";
    change_password.style.display = "flex";
};

nav_item3.onclick = () => {
    window.location.href = 'index';
}

function changedata() {
    data1.style.display = "none";
    data2.style.display = "block";
    if (document.querySelector("#input7").value === "未设置") {
        document.querySelector("#input7_1").value = '';
    }
}

function data2ToData1() {
    data2.style.display = "none";
    data1.style.display = "flex";
}

// function checkKey_0() {
//     let k = document.getElementById("tip1");
//     console.log(k);
//     let U0 = input0.value;
//     // TODO 待修改
//     if (U0 === "123456") {
//         //此处"123456"要换成用户密码的值!
//         k.innerHTML = "";
//     } else {
//         k.innerHTML = "请输入正确的密码！";
//         k.style.display = "block";
//         countdown = 1;
//         timeOutClose(k);
//     }
// }

function checkKey_1() {
    let k = document.getElementById("tip2");
    let Ukey1 = input1.value;
    if (Ukey1.match(/^[a-zA-Z0-9]{6,16}$/)) {
        k.innerHTML = "";
    } else {
        k.innerHTML = "请输入英文字母,数字组成6-16位的密码！";
        k.style.display = "block";
        countdown = 1;
        timeOutClose(k);
    }
}

function checkKey_2() {
    let k = document.getElementById("tip3");
    let Ukey1 = input1.value;
    let Ukey2 = input2.value;
    if (Ukey1 === Ukey2) {
        k.innerHTML = "";
    } else {
        k.innerHTML = "两次密码不一致,请重新输入！";
        k.style.display = "block";
        countdown = 1;
        timeOutClose(k);
    }
}

function checkKey_3() {
    let k = document.getElementById("tip4");
    let U4 = input4.value;
    if (U4.match(/^[\u4E00-\u9FA5a-zA-Z0-9_]{1,12}$/)) {
        k.innerHTML = "";
    } else {
        k.innerHTML = "请输入汉字,英文字母,数字和下划线组成1-12位的用户名";
        k.style.display = "block";
        countdown = 1;
        timeOutClose(k);
    }
}

function checkAll1() {
    let U1 = input1.value;
    let U2 = input2.value;
    if (U1.match(/^[a-zA-Z0-9]{6,16}$/) && U1 === U2) {
        //"123456"要换成用户密码！
        return true;
    }
    return false;
}

function checkAll2() {
    let U4 = input3.value;
    let U5 = input4.value;
    if (U4.match(/^[\u4E00-\u9FA5a-zA-Z0-9_]{1,12}$/) && (U5.match(/^[0-9_]{11}/) || U5 === "未设置" || U5 === "")) {
        return true;
    }
    return false;
}

//弹窗倒计时
function timeOutClose(tip) {
    // document.getElementById("timeOutClose").innerHTML = countdown;
    if (countdown > 0) {
        setTimeout(() => {
            timeOutClose(tip);
        }, 1000);
    } else {
        console.log(tip);
        tip.style.display = "none";
    }
    countdown--;
}

function getCollectionId() {
    let url = document.location.toString();
    console.log(url)
    let arrUrl = url.split("//");
    let start = arrUrl[1].lastIndexOf("personal_homepage");
    let relUrl = arrUrl[1].substring(start);//stop省略，截取从start开始到结尾的所有字符
    if (relUrl.indexOf("?") !== -1) {
        relUrl = relUrl.split("?")[1];
    }
    if (relUrl === "personal_homepage") relUrl = true;
    else if (relUrl === "r_code=0") relUrl = false;
    return relUrl;
}
