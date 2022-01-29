import { releasePointerBlock, blockPointer } from "./defaults.mjs";
import { concatArrays, collectChildren, removeClassFromElements, addClassToElements, bubbleUpPage } from "./utils.mjs";

export function getElements() {
    return {
        "banner": document.getElementById("banner"),
        "bannerText": document.getElementById("banner-text"),
        "blocking": document.getElementById("blocking"),
        // navbar buttons
        "nbb": {
            0: document.getElementById("nbb0"),
            1: document.getElementById("nbb1"),
            2: document.getElementById("nbb2"),
            3: document.getElementById("nbb3")
        },
        // pages
        "pg": {
            0: document.getElementById("pg0"),
            1: document.getElementById("pg1"),
            2: document.getElementById("pg2"),
            3: document.getElementById("pg3")
        },
        // page content
        "spc": {
            0: document.getElementById("spc0"),
            1: document.getElementById("spc1"),
            2: document.getElementById("spc2"),
            3: document.getElementById("spc3")
        }
    };
}

export function runBannerAnimation(elementsOfIndexPage) {
    elementsOfIndexPage.banner.classList.add("slide-banner");
    elementsOfIndexPage.bannerText.style.visibility = "hidden";
    setTimeout(function() {
        elementsOfIndexPage.bannerText.classList.add("fade-in-banner-text");
        elementsOfIndexPage.bannerText.style.visibility = "visible";
    }, 3000);
    setTimeout(function() {
        elementsOfIndexPage.banner.classList.remove("slide-banner");
        elementsOfIndexPage.bannerText.classList.remove("fade-in-banner-text");
    }, 6000);
}



export function configureNavbarAnimations(elementsOfIndexPage) {
    var last_pressed = null;
    var timeout = null;
    for (var i = 0; i < 4; i++) {
        var button = elementsOfIndexPage.nbb[i];

        button.onmouseover = function (event) {
            if (last_pressed != null && last_pressed == parseInt(this.id.slice(-1), 10)) {
                return false;
            }
            event.stopPropagation();
            event.target.classList.add("default-button-hover");
        };

        button.onmouseout = function (event) {
            if (last_pressed != null && last_pressed == parseInt(this.id.slice(-1), 10)) {
                return false;
            }
            event.stopPropagation();
            event.target.classList.remove("default-button-hover");
        };

        button.onclick = function (event) {
            var now_pressed = parseInt(this.id.slice(-1), 10);

            if (last_pressed == now_pressed) {
                return false;
            }

            this.classList.remove("default-button-hover");

            // block pointer events
            blockPointer(elementsOfIndexPage);

            // if timeout remove
            if (timeout != null) {
                clearTimeout(timeout)
                timeout = null;
                removeClassFromElements(
                    "fade-in-slide-page-content", collectChildren(elementsOfIndexPage.spc[last_pressed])
                );
            }

            // bring to front
            bubbleUpPage(window, elementsOfIndexPage, now_pressed);

            elementsOfIndexPage.pg[now_pressed].style.visibility = "visible";
            elementsOfIndexPage.pg[now_pressed].classList.add("roll-down");

            // remove roll down animation and fix page
            setTimeout(function() {
                elementsOfIndexPage.pg[now_pressed].classList.remove("roll-down");
                elementsOfIndexPage.pg[now_pressed].classList.add("fixed-page");
                releasePointerBlock(elementsOfIndexPage);
            }, 1000);

            // fade in page content
            setTimeout(function() {
                addClassToElements("fade-in-slide-page-content", collectChildren(elementsOfIndexPage.spc[now_pressed]));
                elementsOfIndexPage.spc[now_pressed].style.visibility = "visible";
            }, 1000);

            // remove fade in page content animation
            timeout = setTimeout(function() {
                removeClassFromElements("fade-in-slide-page-content", collectChildren(elementsOfIndexPage.spc[now_pressed]));
            }, 2000);

            // hide other pages
            setTimeout(function() {
                for (var j = 0; j < 4; j++) {
                    if (j != now_pressed) {
                        elementsOfIndexPage.spc[j].style.visibility = "hidden";
                        elementsOfIndexPage.pg[j].style.visibility = "hidden";
                        if (elementsOfIndexPage.pg[j].classList.contains("fixed-page")) {
                            elementsOfIndexPage.pg[j].classList.remove("fixed-page");
                        }
                    }
                }
            }, 1000);

            last_pressed = now_pressed;

        };
    }
}