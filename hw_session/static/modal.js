window.addEventListener("load", (event) => {
    let modalContainer = document.getElementById("modal-container")
    modalContainer.addEventListener("click", (clickEvent) => {
        hideModal(modalContainer, clickEvent);
    });
})

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

function startSession(){
    // listen for a click on the start session button
        // show the running session modal
        console.log("triggered start session");
        let goal = document.getElementById("id_goal");
        let goalText = goal.value;
        document.getElementById("goal-text").textContent = goalText;
        const startModal = document.getElementById("start-modal");
        startModal.classList.remove("hide");
}

function finishSession(){
    // listen for a click on the finish session button
        // Hide the running session modal 
        console.log("triggered finish session");
        const startModal = document.getElementById("start-modal");
        startModal.classList.add("hide");
}

