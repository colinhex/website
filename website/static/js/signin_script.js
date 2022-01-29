import { configureDefaultButtons, releasePointerBlock  } from "./modules/defaults.mjs";
import { getElements, configureBackButton } from "./modules/blog.mjs";

window.onload = function() {
    const blogPageElements = getElements();
    configureDefaultButtons();
    configureBackButton(blogPageElements, '/');
    releasePointerBlock(blogPageElements);
}