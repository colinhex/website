import { configureDefaultButton } from "./defaults.mjs";
import { nodeIs, relativeIndentLeft } from "./utils.mjs";
import { type_post, type_comment, type_comment_editor, EditorBuilder, DynamicBlogElementBuilder }
    from "./builders.mjs";


/* -----------------------------------------  */
/*              POST EDITOR                   */
/* -----------------------------------------  */
/*
TODO imitate singleton pattern.
*/


export class PostEditor {

    constructor() {
        /* Toggle Boolean */
        this.editorShown = false;

        /* Elements to be bound to event listeners... */
        this.discard = document.createElement('button');
        this.submit = document.createElement('button');

        /* Construct Div */
        const editorForm = (new EditorBuilder())
            .addTextarea('Title', '30px', 'Title...')
            .addTextarea('Link', '30px', 'Optionally reference a website...')
            .addTextarea('Text', '150px', 'Write a post...')
            .addButton('Submit', true, 'post-editor-submit-button', this.submit)
            .addButton('Discard', false, 'post-editor-discard-button', this.discard)
            .buildEditor();
        this.editorElement = (new DynamicBlogElementBuilder())
            .setTitle('Post Editor')
            .setBottomNode(editorForm)
            .buildElement();
        /* Style Changes */

        /* Placeholder Toggle Element */
        this.toggle = document.createElement('button');
        this.toggle.className = 'default-button';
        this.toggle.classList.add('post-editor-toggle-button');
        this.toggle.textContent = 'create a post';
        configureDefaultButton(this.toggle);

        this.toggleElement = (new DynamicBlogElementBuilder()).buildElement();
        this.toggleElement.classList.add('post-editor-toggle-element');
        this.toggleElement.appendChild(this.toggle);

        /* Insert Toggle in Document */
        document.getElementById('blog').prepend(this.toggleElement);
    }

    removeEditor() {
        this.editorElement.remove();
    }

    removeToggleElement() {
        this.toggleElement.remove()
    }

    toggleView() {
        if (this.editorShown) {
            this.removeEditor();
            this.editorElement.classList.remove('post-editor-appearance');
            document.getElementById('blog').prepend(this.toggleElement);
            this.editorShown = false;
        } else {
            this.removeToggleElement();
            this.editorElement.classList.add('post-editor-appearance');
            document.getElementById('blog').prepend(this.editorElement);
            this.editorShown = true;
        }
    }

}


/* -----------------------------------------  */
/*              COMMENT EDITOR                */
/* -----------------------------------------  */

export class CommentEditor {

    hasPredecessor() {
        return this.predecessor != null;
    }

    remove() {
        /* Remove from Document */
        this.commentEditorDynElement.classList.remove('element-appearance');
        this.commentEditorDynElement.remove();
        this.predecessor = null;
        console.log('Debug CommentEditor ClassList after Remove: ' + this.commentEditorDynElement.classList)
    }

    move(newPredecessor) {
        if (this.hasPredecessor()) {
            this.remove();
        }
        /* Indent to new Predecessor */
        if (nodeIs('comment', newPredecessor)) {
            relativeIndentLeft(this.commentEditorDynElement, newPredecessor, 5);
        }

        /* Insert after new Predecessor */
        newPredecessor.parentNode.insertBefore(this.commentEditorDynElement, newPredecessor.nextSibling);
        this.predecessor = newPredecessor;
        this.commentEditorDynElement.classList.add('element-appearance');
    }

    constructor() {
        /* Elements to be bound to event listeners... */
        this.discard = document.createElement('button');
        this.submit = document.createElement('button');

        /* Construct Div */
        let editorForm = (new EditorBuilder())
            .addTextarea('Text', '100px', 'Write a comment...')
            .addButton('submit', true, 'comment-editor-submit-button', this.submit)
            .addButton('discard', false, 'comment-editor-discard-button', this.discard)
            .buildEditor();
        this.commentEditorDynElement = (new DynamicBlogElementBuilder())
            .setTitle('Comment Editor')
            .setBottomNode(editorForm)
            .buildElement();
        /* Style Changes */
        this.commentEditorDynElement.classList.add('comment-editor');
        /* this.commentEditorDynElement.classList.add('editor-dynamic-blog-element'); */

        /* Predecessor of Comment Acts as Toggle */
        this.predecessor = null;
    }

}

/* -----------------------------------------  */
/*              POST AND COMMENT              */
/* -----------------------------------------  */


function createComment(data) {
    var predecessor = document.getElementById(data.parent_id);
    var element = (new DynamicBlogElementBuilder())
        .setID('e_' + data.element_id)
        .setPredecessor(predecessor)
        .setAuthor(data.element_author)
        .setDate(data.element_date)
        .setText(data.element_text)
        .setCommentable()
        .buildElement();
    element.classList.add('comment');

    if (nodeIs('comment', predecessor)) {
        relativeIndentLeft(element, predecessor, 5);
        predecessor.parentNode.insertBefore(element, predecessor.nextSibling);
    } else {
        element.style.left = '5%';  /* Todo move style changes to css*/
        predecessor.nextSibling.appendChild(element);
    }
}

function createPost(data) {
    var element = (new DynamicBlogElementBuilder())
        .setID('e_' + data.element_id)
        .setAuthor(data.element_author)
        .setDate(data.element_date)
        .setText(data.element_text)
        .setTitle(data.post_title)
        .setPinned(data.pinned)
        .setHref(data.post_href)
        .setCommentable()
        .buildElement();

    var commentSection = (new DynamicBlogElementBuilder()).buildElement()
    commentSection.classList.add('comment-section');
    var blog = document.getElementById('blog');
    blog.appendChild(element);
    blog.appendChild(commentSection);
}

function createDynamicBlogElement(data, type) {
    switch(type) {
        case type_comment:
            createComment(data);
            break;
        case type_post:
            createPost(data);
            break;
        default:
            console.log('No type found for dynamicBlogElement in construction:' + data + 'Type:' + type);
    }
}

export function getElements() {
    return {
        "blocking": document.getElementById("blocking"),
        "ni": {
            0: document.getElementById("ni0")
        },
        "nbb": {
            0: document.getElementById("nbb0")
        }
    };
}

export function configureBackButton(blogPageElements, href) {
    blogPageElements.nbb[0].onmouseover = function (event) {
        event.stopPropagation();
        event.target.classList.add("default-button-hover");
    };

    blogPageElements.nbb[0].onmouseout = function (event) {
        event.stopPropagation();
        event.target.classList.remove("default-button-hover");
    };

    blogPageElements.nbb[0].onclick = function (event) {
        location.href = href;
    }
}


export function load(data, type) {
    for (var i = 0; i < data.length; i++) {
        createDynamicBlogElement(data[i], type);
    }
}