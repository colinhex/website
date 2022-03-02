import { configureDefaultButtons, releasePointerBlock  } from "./modules/defaults.mjs";

function configureBackButton(button, href) {
    button.onmouseover = function (event) {
        event.stopPropagation();
        event.target.classList.add("default-button-hover");
    };

    button.onmouseout = function (event) {
        event.stopPropagation();
        event.target.classList.remove("default-button-hover");
    };

    button.onclick = function (event) {
        location.href = href;
    }
}

window.onload = function() {
    configureDefaultButtons();
    configureBackButton(document.getElementById('nbb0'), '/');
    releasePointerBlock({'blocking': document.getElementById('blocking')});
}