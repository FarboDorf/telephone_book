"use strict";


// URL = "http://192.168.1.65:8080"
URL = "http://127.0.0.1:5000/"
let fields = document.getElementsByTagName("input");

function getSettings(source){
    let params = {};
    for(let i=0; i<fields.length; i++){
        let value = fields[i].value;
        if(source == "add" && !value){
            value = "NULL";
        }
        if(value){
            if(typeof value === "string"){
                value = value.toString();
            }
            params[fields[i].id] = value;
        }
    };

    let settings = {
        url: URL + "/" + source,
        method: "GET",
        timeout: 0,
	    data: params,
    };
    console.log(settings)
    return settings
}


function selectReq(){
    //delete old table
    let table = document.getElementsByTagName("table");
    console.log(table)
    if(table.length > 0){
        table[0].remove();
    }

    $.ajax(getSettings("select")).done(function(response){
        let res = JSON.parse(response);

        //add table
        let table = document.createElement('table');
        table.setAttribute("class", "table text-white");
        let thead = document.createElement('thead');
        let tbody = document.createElement('tbody');
        table.appendChild(thead);
        table.appendChild(tbody);
        let tr = document.createElement('tr');

        //create head of table
        for (let i = 0; i < 8; i++) {
                let th = document.createElement('th');
                let head = fields[i].id;
                th.setAttribute("scope", "col");
                if(head == "f_val"){
                    head = "family";
                }
                if(head == "n_val"){
                    head = "name";
                }
                if(head == "p_val"){
                    head = "patronymic";
                }
                if(head == "s_val"){
                    head = "street";
                }
                th.innerHTML = head;
                tr.appendChild(th);
        }
        thead.appendChild(tr);


        for(let i = 0; i < Object.keys(res).length; i++){
            console.log(res[i.toString()]);
            let tr = document.createElement('tr');

            for (let j = 0; j < 8; j++) {
                let td = document.createElement('td');
                td.innerHTML = res[i][j.toString()];
                tr.appendChild(td);
	        }
	        tbody.appendChild(tr);
        }


        // Adding the entire table to the body card-body
        document.getElementById("card-body").appendChild(table);

    })
}


function addReq(){
     $.ajax(getSettings("add")).done(function(response){
        console.log(response);
        alert("New contact was added");
     })
}


function deleteReq(){
    $.ajax(getSettings("delete")).done(function(response){
        console.log(response);
        if(response.code == 200){
            alert("Contact was deleted");
        }
        if(response.code == 404){
            alert("Contact not found")
        }
        if(response.code == 400){
            alert("there is more than one contract with these parameters in the phone book\nplease enter more data")
        }
    })
}

selectBtn.onclick = selectReq;
addBtn.onclick = addReq;
deleteBtn.onclick = deleteReq;