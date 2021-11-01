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
