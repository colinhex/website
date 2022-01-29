import { configureDefaultButtons, releasePointerBlock } from "./modules/defaults.mjs";
import { getElements, runBannerAnimation, configureNavbarAnimations } from "./modules/index.mjs";


window.onload = function() {
    const elementsOfIndexPage = getElements();
    configureDefaultButtons();
    runBannerAnimation(elementsOfIndexPage);
    configureNavbarAnimations(elementsOfIndexPage);
    releasePointerBlock(elementsOfIndexPage);
}
