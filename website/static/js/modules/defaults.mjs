

export function configureDefaultButton(button) {
    button.onmouseover = function (event) {
        event.stopPropagation();
        event.target.classList.add("default-button-hover");
    };

    button.onmouseout = function (event) {
        event.stopPropagation();
        event.target.classList.remove("default-button-hover");
    };
}


export function configureDefaultButtons() {
    const buttons = document.getElementsByClassName("default-button");
    for (var i = 0; i < buttons.length; i++) {
        var button = buttons[i];
        configureDefaultButton(button);
    }
}

export function blockPointer(elementsOfPage) {
    elementsOfPage.blocking.style.pointerEvents = "all";
}

export function releasePointerBlock(elementsOfPage) {
    elementsOfPage.blocking.style.pointerEvents = "none";
}