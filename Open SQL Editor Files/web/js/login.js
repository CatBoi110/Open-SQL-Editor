const dropDown = document.querySelector("#Backend-Dropdown");
const inputContainer = document.querySelector(".Container");
const submitButton = document.querySelector("#Submit");

var info = [];

submitButton.addEventListener("click", submitLogin);

function populateInputFields(){
    clearInputFields()

    if (dropDown.value ==  "MySQL" || dropDown.value == "MS Azure"){
        let server = document.createElement("input");
        let database = document.createElement("input"); 
        let username = document.createElement("input");
        let password = document.createElement("input");

        server.placeholder = "Server";
        database.placeholder = "Database";
        username.placeholder = "Username";
        password.placeholder = "Password";
        password.type = "password";

        server.classList.add("Input-Box");
        database.classList.add("Input-Box");
        username.classList.add("Input-Box");
        password.classList.add("Input-Box");

        inputContainer.appendChild(server);
        inputContainer.appendChild(database);
        inputContainer.appendChild(username);
        inputContainer.appendChild(password);

        let submit = submitButton.cloneNode(true);

        submit.style.visibility = "visible";

        submit.addEventListener("click", submitLogin);

        inputContainer.appendChild(submit);
    }
        
}

function clearInputFields(){
    let children = inputContainer.children
    
    for (let i = children.length - 1; i > 0; i --){
        children[i].remove();
    }
}

async function submitLogin(){
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

}
