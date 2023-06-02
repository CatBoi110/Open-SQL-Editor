const table = document.querySelector(".Table");
const refreshButton = document.querySelector("#Refresh");
const editButton = document.querySelector("#Edit");
const delButton = document.querySelector("#Delete");
const applyButton = document.querySelector("#Apply");
const revertButton = document.querySelector("#Revert");
const newButton = document.querySelector("#New");
const cancelButton = document.querySelector("#Cancel");
const dropDown = document.querySelector("#Table-Dropdown");

var dataFields = [];
var keyFields = []; 

var inputTemplate = "<input class = 'Input-Field' size = '5' placeholder = '";
var dateInputTemplate = '<input type = "date" class = "Input-Field">';

newButton.addEventListener("click", addRowPrompt);

loginIn();

async function loginIn(){
    if (await eel.isLoginEmpty()() == false){
        let failedLoginAttempts = 0;

        while (true){

            psk = askForPassword();

            if (psk == null){
                break;
            }

            if (await eel.connectToBackend(psk)()){
                initTable();   
                break;
            } else {
                if (failedLoginAttempts < 3){
                    alert("Please Try Again.");
                    failedLoginAttempts ++;
                } else {
                    alert("Please Verify Server Login. Use the Login tab to reset saved login information.");
                    break;
                }
            }
        }
    } else {
        alertMissingLogin();
    }
}

async function initTable(){
    clearTable();

    await new Promise(resolve => setTimeout(resolve, 1000)); 

    let listOfTables = await eel.getAvailableTables()();

    if (dropDown.length == 1){
        for (let k = 0; k < listOfTables.length; k ++){
            let option = document.createElement("option");
            dropDown.appendChild(option);
        }
    }

    for (let j = 1; j <= listOfTables.length; j ++){
        dropDown.options[j].innerHTML = listOfTables[j - 1];
    }

    if (dropDown.value != "Select A Table"){
        eel.setTable(dropDown.value);
        let allFields = await eel.initTable()();

        dataFields = allFields[0];
        keyFields = allFields[1];

        let columnNum = 0;

        let row = table.insertRow(0);

        for(let k = 0; k < keyFields.length; k ++){
            row.insertCell(columnNum);
            row.cells[columnNum].innerHTML = keyFields[k][0]; 
            row.cells[columnNum].style = "padding: 0px 10px 0px 10px;";
            columnNum ++;
        }
        
        for (let i = 0 ; i < dataFields.length; i ++){
            row.insertCell(columnNum);
            row.cells[columnNum].innerHTML = dataFields[i][0]; 
            row.cells[columnNum].style = "padding: 0px 10px 0px 10px;";
            columnNum ++;
        }

        row.insertCell(columnNum);

        let refresh = refreshButton.cloneNode(true);

        refresh.style.visibility = "visible";
        row.cells[columnNum].appendChild(refresh);

        refresh.addEventListener("click", function(){refreshTable()});

        refreshTable();

    } else {
        clearTable();
    }
}

async function refreshTable(){
    clearTable();

    await new Promise(resolve => setTimeout(resolve, 1000)); 

    let tableData = []
    tableData = await eel.refresh()();

    let rowNum = 0;
    let columnNum = 0;

    for (rowNum = 0; rowNum < tableData.length; rowNum ++){

        let row = table.insertRow(rowNum + 1);

        for (columnNum = 0; columnNum < tableData[rowNum].length; columnNum ++){
            row.insertCell(columnNum)
            row.cells[columnNum].innerHTML = tableData[rowNum][columnNum];
        }

        row.insertCell(columnNum);

        let edit = editButton.cloneNode(true);
        let del = delButton.cloneNode(true);

        edit.style.visibility = "visible";
        del.style.visibility = "visible";

        row.cells[columnNum].appendChild(edit);
        row.cells[columnNum].appendChild(del);

        edit.addEventListener("click", function(){editRowPrompt(row)});
        del.addEventListener("click", function(){deleteRowPrompt(del)});

    }

    newButton.style.visibility = "visible";

}

function clearTable(){
    for (let i = 0; i < table.rows.length; i ++){
        if (i > 0){
            table.deleteRow(i);
            i --;
        }

        if (table.rows.length == 2){
            i++;
        }
    }

}


function addRowPrompt(){
    newButton.style.visibility = "hidden";
    let rowIndex = table.rows.length - 1;
    let row = table.insertRow(rowIndex);

    let columnNum = 0;

    for (let k = 0 ; k < keyFields.length; k ++){
        row.insertCell(columnNum);
        row.cells[columnNum].innerHTML = "N/A";

        columnNum ++;
    }

    for (let i = 0; i < dataFields.length; i ++){
        row.insertCell(columnNum);

        let columnName = dataFields[i][0];
        let dataType = dataFields[i][1]

        if (dataType.match("date")){print
            row.cells[columnNum].innerHTML = dateInputTemplate;
        } else if (dataType.match("datetime")){
            row.cells[columnNum].innerHTML = dateTimeInputTemplate
        } else {
            row.cells[columnNum].innerHTML = inputTemplate + columnName + "'>";
        }

        columnNum ++;
    }


    let cancel = cancelButton.cloneNode(true);
    let apply = applyButton.cloneNode(true);

    apply.style.visibility = "visible";
    cancel.style.visibility = "visible";

    row.appendChild(apply);
    row.appendChild(cancel);

    cancel.addEventListener("click", function(){
        table.deleteRow(cancel.parentElement.rowIndex);
        newButton.style.visibility = "visible";
    });

    apply.addEventListener("click", function() {
        let valuesArray = [];

        let dataFieldIndex = 0; 

        for (let i = 0; i < row.cells.length; i++){
            if (row.cells[i].firstChild.value != null){
                let inputFieldValue = row.cells[i].firstChild.value;

                if (checkField(inputFieldValue, dataFields[dataFieldIndex][1], i)){
                    valuesArray.push(inputFieldValue);
                }

                dataFieldIndex ++;
            }
        }

        if (valuesArray.length === dataFields.length){
            eel.addRow(valuesArray);

            refreshTable();

        }
    });
}

function deleteRowPrompt(btn){

    let row = btn.parentElement.parentElement;

    if (confirm("Are you sure you want to delete this row?")){
        valuesArray = []


        for (let i = 0; i < row.children.length; i++){
            valuesArray.push(row.cells[i].innerHTML);
        }
        
        valuesArray.pop(valuesArray.length - 1);

        eel.deleteRow(valuesArray);
    }

    refreshTable();
}

function editRowPrompt(row){
    if (keyFields.length > 0){
        let oldData = [];

        let columnNum = 0;

        for (let k = 0 ; k < keyFields.length; k ++){
            oldData.push(row.cells[columnNum].innerHTML);
            columnNum ++;
        }

        for (let i = 0; i < dataFields.length; i++){
            oldData.push(row.cells[columnNum].innerHTML);
            columnNum ++;
        }
        
        row.cells[columnNum].innerHTML = "";

        let apply = applyButton.cloneNode(true);
        let revert = revertButton.cloneNode(true);

        apply.style.visibility = "visible";
        revert.style.visibility = "visible";
        
        columnNum = 0;

        for (let k = 0 ; k < keyFields.length; k ++){
            row.cells[columnNum].innerHTML = "N/A";

            columnNum ++;
        }

        for (let i = 0; i < dataFields.length; i ++){
            let columnName = dataFields[i][0];
            let dataType = dataFields[i][1]

            if (dataType.match("date")){print
                row.cells[columnNum].innerHTML = dateInputTemplate;
            } else if (dataType.match("datetime")){
                row.cells[columnNum].innerHTML = dateTimeInputTemplate
            } else {
                row.cells[columnNum].innerHTML = inputTemplate + columnName + "'>";
            }

            columnNum ++;
        }

        row.cells[columnNum].appendChild(apply);
        row.cells[columnNum].appendChild(revert);

        apply.addEventListener("click", function(){
            let newData = [];
            let keyData = null;

            let dataFieldIndex = 0 

            for (let i = 0; i < row.children.length - 1; i++){
                if (row.cells[i].firstChild.value != null){
                    let inputFieldValue = row.cells[i].firstChild.value;

                    if (checkField(inputFieldValue, dataFields[dataFieldIndex][1], i)){
                        newData.push(inputFieldValue);
                    }

                    dataFieldIndex ++;
                }
            }

            for (let i = 0; i < oldData.length - 1; i ++){
                if (table.rows[0].cells[i].innerHTML === keyFields[0][0]){
                    keyData = oldData[i];
                }

            }

            if (newData.length === dataFields.length){
                eel.editRow(newData, keyData);

                refreshTable();
            }
        });

        revert.addEventListener("click", function(){
            for (let i = 0; i < oldData.length; i++){
                row.cells[i].innerHTML = oldData[i];
            }

            row.cells[oldData.length].innerHTML = "";

            let edit = editButton.cloneNode(true);
            let del = delButton.cloneNode(true);

            edit.style.visibility = "visible";
            del.style.visibility = "visible";

            row.cells[oldData.length].appendChild(edit);
            row.cells[oldData.length].appendChild(del);

            edit.addEventListener("click", function(){editRowPrompt(row)});
            del.addEventListener("click", function(){deleteRowPrompt(del)});
        });

    } else {
        alert("This table does not have a key field. The update row function will not work unless the table has a key field. Please try again.");
    }
}


function checkField(value, field, index){
    if (value == ""){
        alert("Please Enter a value for " + table.rows[0].cells[index].innerHTML);

    } else if (field.match("char|varchar|binary|varbinary|tinyblob|tinytext|text|blob|meduimtext|mediumblob|longtext|longblob|nchar|nvarchar|ntext") && value.match("0|1|2|3|4|5|6|7|8|9")){
        alert("Please Enter a Text Value For " + table.rows[0].cells[index].innerHTML);

    } else if (field.match("decimal|numeric|smallmoney|money|float|double|dec") && value.indexOf(".") == -1){
        alert("Please Enter A Decimal Number For " + table.rows[0].cells[index].innerHTML);

    } else if (field.match("bit|tinyint|bool|boolean|meduimint|int|integer|bigint|float|double|doubleprecision") && isNaN(value)){
        alert("Please Enter A Whole Number Value For " + table.rows[0].cells[index].innerHTML);

    } else {
        return true;
    }

    return false;
}

eel.expose(askForPassword);
function askForPassword(){
    while (true){
        let psk = prompt("Enter password to Database");

        if (psk != null){
            if (psk !== ""){
                return psk;
            } else {
                alert("Password Must Not Be Empty.");
            }
        } else {
            alert("Reload this page to return to password prompt");
            break;
        }
    }
}

function alertMissingLogin(){
    alert("No Login Information was found. Please enter login info in the Login Tab");
}

eel.expose(alertCorrectLogin);
function alertCorrectLogin(){
    alert("Login Success!");
}

eel.expose(alertSuccessfulQuery);
function alertSuccessfulQuery(){
    alert("Success!");
}

eel.expose(alertErrorCode);
function alertErrorCode(msg){
    alert("Error: " + msg);
}