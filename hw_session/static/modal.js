window.addEventListener("load", (event) => {
    let startBtn = document.getElementById("start-btn");
    // startBtn.addEventListener("click", sendStartTime);
    startBtn.addEventListener("click", getStartTime);
    let modalContainer = document.getElementById("modal-container")
    modalContainer.addEventListener("click", (clickEvent) => {
        hideModal(modalContainer, clickEvent);
    });
})


/******************************************************************
* Modal Logic to hide/show them
******************************************************************/
function showModal(){
    let modalContainer = document.getElementById("modal-container");
    modalContainer.classList.remove("hide");
}

function hideModal(modalContainer, clickEvent){
    let firstModal = document.getElementById("session-modal");
    let secondModal = document.getElementById("start-modal");
    let clickInsideFirst = firstModal.contains(clickEvent.target);
    let clickInsideSecond = secondModal.contains(clickEvent.target);
    if (!clickInsideFirst && !clickInsideSecond){
        modalContainer.classList.add("hide");
    }
}

/******************************************************************
* Logic to start a session
******************************************************************/
function startSession(){
    // listen for a click on the start session button
        // show the running session modal
        console.log("triggered start session");
        let goal = document.getElementById("id_goal");
        let goalText = goal.value;
        document.getElementById("goal-text").textContent = goalText;

        checkAssignmentList();

        const startModal = document.getElementById("start-modal");
        startModal.classList.remove("hide");
}

function checkAssignmentList(){
    let checkboxList = document.querySelectorAll(".checkBox:checked")
    let ul = document.querySelector(".selected-list")
    ul.innerHTML = '';
    checkboxList.forEach(checkBox => {
        let taskName = checkBox.nextElementSibling;
        let taskDate = taskName.nextElementSibling;
        let li = document.createElement('li');
        li.innerHTML = `
            <div class="assignment">
                <input type="checkbox" name="chosenTasks[]">
                <p class="assign-name">${taskName.textContent}</p>
                <p class="due-date">${taskDate.textContent}</p>
            </div>`;
        ul.appendChild(li);
    })
}

/**********************************************************************
 * Create a date time object. It will convert that date time object into 
 * a JSON string so we can use into the database.
 *********************************************************************/
function getStartTime(){
    let start = new Date();
    let startTime = {
        "day" : start.getDate(), 
        "hour": start.getHours(), 
        "min": start.getMinutes(),
        "sec": start.getSeconds()
    }
    console.log(startTime)
    document.getElementById("id_start_time").value = JSON.stringify(startTime);
    displayEndTime();
}

function displayEndTime(){
    let startTime = JSON.parse(document.getElementById("id_start_time").value);
    let hoursToAdd = document.getElementById("id_time_limit_hours").value;
    console.log("hrsTo Add", hoursToAdd)
    let minsToAdd = document.getElementById("id_time_limit_mins").value;
    
    let endTimeObj = timeArith(startTime, {"hour": hoursToAdd, "min": minsToAdd});
    document.getElementById("end-time").innerHTML = endTimeObj.hour + ":" + endTimeObj.min;
}

function timeArith(baseTime, timeDiff){

    let baseMins = baseTime.min;
    let baseHour = baseTime.hour;
    let diffMin = timeDiff.min;
    let diffHour = timeDiff.hour;

    let endHour = baseHour + diffHour;
    let endMin = baseMins + diffMin;

    // Tell if the hour is greater than 12 
    if (endHour > 12){
        console.log("End hour before:", endHour)
        endHour -= 12;
        console.log("End hour after:", endHour)
    }
    
    // Tell if we need to increment hour when we add minutes
    if (endMin >= 60){
        endHour += 1;
        endMin -= 60;
    }
    
    return {"hour": endHour, "min": endMin};
}


/******************************************************************
* Logic to finish the session
******************************************************************/
function finishSession(){
    // listen for a click on the finish session button
        // Hide the running session modal 
        console.log("triggered finish session");
        const startModal = document.getElementById("start-modal");
        startModal.classList.add("hide");
}

