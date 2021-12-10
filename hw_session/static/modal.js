var INTERVAL_THREAD = null;

/******************************************************************
* Sets up after the HTML loads
******************************************************************/
window.addEventListener("load", (event) => {
    let startBtn = document.getElementById("start-btn");
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
    let thirdModal = document.getElementById("break-modal");
    let clickInsideFirst = firstModal.contains(clickEvent.target);
    let clickInsideSecond = secondModal.contains(clickEvent.target);
    let clickInsideThird = thirdModal.contains(clickEvent.target);
    if (!clickInsideFirst && !clickInsideSecond && !clickInsideThird){
        modalContainer.classList.add("hide");
    }
}

/******************************************************************
* Logic to start a session
******************************************************************/
function startSession(){
    // listen for a click on the start session button
        // show the running session modal
        let goal = document.getElementById("id_goal");
        let goalText = goal.value;
        document.getElementById("goal-text").textContent = goalText;

        checkAssignmentList();

        const startModal = document.getElementById("start-modal");
        startModal.classList.remove("hide");
}

/******************************************************************
* Gets the list of checked checkboxes from first modal and 
* builds them on the second modal. Sends the count of selected
* assignments to ghost input field selected assignment count
* on hw session form.
******************************************************************/
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
                <input class="chosenCB" type="checkbox" name="chosenTasks[]">
                <p class="assign-name">${taskName.textContent}</p>
                <p class="due-date">${taskDate.textContent}</p>
            </div>`;
        ul.appendChild(li);
    })

    document.getElementById("id_selected_assignment_count").value = checkboxList.length;
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
    document.getElementById("id_start_time").value = JSON.stringify(startTime);
    INTERVAL_THREAD = setInterval(() => {handleBreakInterval(startTime)}, 1000);
    displayEndTime();
}

/******************************************************************
* Gets the hours to add and minutes to add to starting time of
* session and then populates end time on second form.
******************************************************************/
function displayEndTime(){
    let startTime = JSON.parse(document.getElementById("id_start_time").value);
    let hoursToAdd = document.getElementById("id_time_limit_hours").value;
    let minsToAdd = document.getElementById("id_time_limit_mins").value;
    
    let endTimeObj = timeArith(startTime, {"hour": hoursToAdd, "min": minsToAdd});
    document.getElementById("end-time").innerHTML = endTimeObj.hour + ":" + endTimeObj.min;
}

/******************************************************************
* Helper function to provide ability to do basic operations
* on time
******************************************************************/
function timeArith(baseTime, timeDiff){
    let baseSec = parseInt(baseTime.sec);
    let baseMins = parseInt(baseTime.min);
    let baseHour = parseInt(baseTime.hour);

    let diffSec = parseInt(timeDiff.sec);
    let diffMin = parseInt(timeDiff.min);
    let diffHour = parseInt(timeDiff.hour);

    let endHour = baseHour + diffHour;
    let endMin = baseMins + diffMin;
    let endSec = baseSec + diffSec;

    // Tell if the hour is greater than 12 
    if (endHour > 12){
        endHour -= 12;
    }
    
    // Tell if we need to increment hour when we add minutes
    if (endMin >= 60){
        endHour += 1;
        endMin -= 60;
        if (endMin < 10){
            endMin = "0" + endMin;
        }
    }

    if (endSec >= 60){
        endMin += 1;
        endSec -= 60;
        if (endSec < 10){
            endSec = "0" + endSec;
        }
    }
    
    return {"hour": endHour, "min": endMin, "sec": endSec};
}

/******************************************************************
* Logic to finish the session
******************************************************************/
function finishSession(){
    let finishedList = document.querySelectorAll(".chosenCB:checked");
    document.getElementById("id_completed_count").value = finishedList.length;


    const startModal = document.getElementById("start-modal");
    startModal.classList.add("hide");
}

/******************************************************************
* Checks to see if the time passed since start or last break
* is equal to the break interval so it can trigger the pop-up
******************************************************************/
function handleBreakInterval(startTime){
    let value = document.getElementById("id_break_interval").value;

    let intervalMin = value * 60;
    let date = new Date();
    let curTime = {"hour": date.getHours(), "min": date.getMinutes(), "sec": date.getSeconds()};
    
    let timeDiff = timeArith(curTime, {"hour": (startTime.hour) * -1, "min": (startTime.min) * -1, "sec": (startTime.sec) * -1});
    
    if (timeDiff.min % intervalMin == 0 && timeDiff.sec == 0){
        renderBreakPopUp();
    } 
}

/******************************************************************
* renders a pop-up to the screen
******************************************************************/
function renderBreakPopUp(){
    pauseInterval();
    document.getElementById("break-modal").classList.remove("hide")
    document.getElementById('modal-container').classList.add('ignore-click');
}

/******************************************************************
* triggers a break pop-up
******************************************************************/
function takeABreak(){
    renderBreakPopUp();
}

/******************************************************************
* Pauses the inteval thread that is checking the current time
* while you are in a break pop-up
******************************************************************/
function pauseInterval(){
    clearInterval(INTERVAL_THREAD);
}

/******************************************************************
* Resets the interval thread to resume homework session
******************************************************************/
function resumeSession(){
    // get the current time
    let date = new Date();
    let curTime = {
        "hour": date.getHours(), 
        "min": date.getMinutes(), 
        "sec": date.getSeconds()
    };

    // set interval for each second with the new start time
    INTERVAL_THREAD = setInterval(() => {handleBreakInterval(curTime)}, 1000);
    document.getElementById("break-modal").classList.add("hide")
    document.getElementById('modal-container').classList.remove('ignore-click');
}