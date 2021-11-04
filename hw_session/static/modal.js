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
    let modal = document.getElementById("session-modal");
    let clickInsideModal = modal.contains(clickEvent.target);
    if (!clickInsideModal){
        modalContainer.classList.add("hide");
    }
}

function startSession(){
    // listen for a click on the start session button
        // show the running session modal
        console.log("triggered start session");
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

