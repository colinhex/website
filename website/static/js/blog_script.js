import { configureDefaultButtons, releasePointerBlock  } from "./modules/defaults.mjs";
import { getElements, configureBackButton, load, CommentEditor, PostEditor } from "./modules/blog.mjs";

window.onload = function() {
    const blogPageElements = getElements();
    configureDefaultButtons();
    configureBackButton(blogPageElements, '/');
    releasePointerBlock(blogPageElements);
}

window.render = function(posts, comments) {
    /* Construct Comments from Data */
    load(posts, 0);
    load(comments, 1);
}

window.configureReplyButtons = function(replyButtons, imageSrc) {
    /* Bind Reply Buttons to Comment Editor */
    var lastPressedReplyButton;

    const commentEditor = new CommentEditor();
    commentEditor.discard.onclick = function() {
        lastPressedReplyButton.classList.remove('hidden-reply-button');
        commentEditor.remove();
    }
    /* Todo submit comment */

    for (var i = 0; i < replyButtons.length; i++) {
        replyButtons[i].style.backgroundImage = imageSrc;
        replyButtons[i].onclick = function(event) {
            event.target.classList.add('hidden-reply-button');
            if (lastPressedReplyButton != null) {
                lastPressedReplyButton.classList.remove('hidden-reply-button');
            }
            lastPressedReplyButton = event.target;
            commentEditor.move(event.target.parentNode);
        }
    }
}

window.loadPostEditor = function() {
    const postEditor = new PostEditor();
    postEditor.toggle.onclick = function() {
        postEditor.toggleView();
    }
    postEditor.discard.onclick = function() {
        postEditor.toggleView();
    }
    /* Todo submit post */
}