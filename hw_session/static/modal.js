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
    // console.log(startTime)
    document.getElementById("id_start_time").value = JSON.stringify(startTime);
    setInterval(() => {handleBreakInterval(startTime)}, 1000);
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
        console.log("End hour before:", endHour)
        endHour -= 12;
        console.log("End hour after:", endHour)
    }
    
    // Tell if we need to increment hour when we add minutes
    if (endMin >= 60){
        endHour += 1;
        console.log("End min before:", endMin);
        endMin -= 60;
        console.log("End min after:", endMin);
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
    // listen for a click on the finish session button
        // Hide the running session modal 
        console.log("triggered finish session");
        const startModal = document.getElementById("start-modal");
        startModal.classList.add("hide");
}

function handleBreakInterval(startTime){
    let value = document.getElementById("id_break_interval").value;

    let intervalMin = value * 60;
    let date = new Date();
    let curTime = {"hour": date.getHours(), "min": date.getMinutes(), "sec": date.getSeconds()};
    
    let timeDiff = timeArith(curTime, {"hour": (startTime.hour) * -1, "min": (startTime.min) * -1, "sec": (startTime.sec) * -1});
    console.log(timeDiff);
    
    if (timeDiff.min % intervalMin == 0 && timeDiff.sec == 0){
        window.open("/mindfullness", "_blank");

        // sleep time expects milliseconds
        function sleep (time) {
            return new Promise((resolve) => setTimeout(resolve, time));
        }
        
        // Usage!
        sleep(3000).then(() => {
            alert("Break time! \n\nWe opened the Mindfulness page to inspire you. Check it out! \n\nClick OK when you're ready to continue your session.")
        });
        
    } 
}
