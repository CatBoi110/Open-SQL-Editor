const dropDown = document.querySelector("#Backend-Dropdown");
const inputContainer = document.querySelector(".Container");
const submitButton = document.querySelector("#Submit");

var info = [];

submitButton.addEventListener("click", submitLogin);

window.onunload = function(){
    eel.returnHome();
}

async function submitLogin(){
    if (dropDown.value != "Select a SQL Backend"){
        info.push(dropDown.value);

        for (let i = 1; i < 5; i ++){
            if (inputContainer.children[i].value == ""){
                alert("Please enter a value for " + inputContainer.children[i].placeholder);
            } else {
                info.push(inputContainer.children[i].value);
            }
        }

        if (info.length == 5){
            eel.saveLogin(info);
            info = [];
            alert("Login Saved.");
        }

    } else {
        alert("Please Select a SQL Backend");
    }
}
