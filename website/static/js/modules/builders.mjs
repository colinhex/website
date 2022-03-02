import { configureDefaultButton } from "./defaults.mjs";

export const type_post = 0;
export const type_comment = 1;
export const type_comment_editor = 2;


export class DynamicBlogElementBuilder {
    #title;
    #date;
    #author;
    #text;
    #href;
    #bottomNode;
    #pinned;
    #commentable;
    #moveFunction;
    #arguments;
    #predecessor;

    checkIntegrity(obj) {
        var hasIntegrity = !(typeof obj === 'undefined' || obj === '') && (typeof obj == 'string')
        return hasIntegrity;
    }

    constructor() {
        this.id = '';
        this.title = '';
        this.date = '';
        this.author = '';
        this.text = '';
        this.imageSrc = '';
        this.predecessor = null;
        this.bottomNode = null;
        this.pinned = false;
        this.orderReference = '';
        this.commentable = false;
        this.commentOnClick = null;
    }

    setPredecessor(predecessor) {
        this.predecessor = predecessor;
        return this;
    }

    setID(id) {
        this.id = id;
        return this;
    }

    setTitle(title) {
        this.title = title;
        return this;
    }

    setDate(date) {
        this.date = date;
        return this;
    }

    setAuthor(author) {
        this.author = author;
        return this;
    }

    setText(text) {
        this.text = text;
        return this;
    }

    setHref(href) {
        this.href = href;
        return this;
    }

    setBottomNode(bottomNode) {
        this.bottomNode = bottomNode;
        return this;
    }

    setPinned(pinned) {
        this.pinned = pinned;
        return this;
    }

    setCommentable() {
        this.commentable = true;
        return this;
    }

    buildElement() {
        const dynamicBlogElement = document.createElement('div');
        dynamicBlogElement.className = 'dyn-blog-element';

        if (this.checkIntegrity(this.id)) {
            dynamicBlogElement.id = this.id;
        }

        if (this.checkIntegrity(this.title)) {
            const blogPostTitle = document.createElement('p');
            blogPostTitle.className = 'blog-text';
            blogPostTitle.appendChild(document.createTextNode(this.title));
            dynamicBlogElement.appendChild(blogPostTitle);
        }

        if (this.checkIntegrity(this.author) && this.checkIntegrity(this.date)) {
            const blogPostInfo = document.createElement('p');
            blogPostInfo.className = 'blog-post-info';
            blogPostInfo.appendChild(document.createTextNode(
                ((this.pinned) ? 'PINNED':'') + this.author + ' : ' + this.date)
            );
            dynamicBlogElement.appendChild(blogPostInfo);
        }  else if (this.pinned) {
            blogPostInfo.appendChild(document.createTextNode('PINNED'));
        }

        if (this.checkIntegrity(this.href)) {
            const topContainer = document.createElement('div');
            topContainer.className = 'topContainer';
            const image = document.createElement('img');
            image.src = this.href;
            var ratio = this.width/this.height;
            image.style.width = '300px';
            image.style.height = 'calc(300px*' + ratio + ')';
            topContainer.appendChild(image);
            dynamicBlogElement.appendChild(topContainer);
        }

        if (this.checkIntegrity(this.text)) {
            const blogText = document.createElement('p');
            blogText.className = 'blog-text';
            blogText.appendChild(document.createTextNode(this.text));
            dynamicBlogElement.appendChild(blogText);
        }

        if (this.bottomNode != null) {
            this.bottomNode.classList.add('bottom-node');
            dynamicBlogElement.appendChild(this.bottomNode);
        }

        if (this.commentable) {
            const commentButton = document.createElement('button');
            commentButton.classList.add('default-button');
            commentButton.classList.add('reply-button');
            dynamicBlogElement.appendChild(commentButton);
        }

        return dynamicBlogElement;
    }
}

export class EditorBuilder {
    #textareaData;
    #buttonData;
    #formValueHolders;

    constructor() {
        this.textareaData = new Array();
        this.buttonData = new Array();
        this.formValueHolders = new Array();
    }

    addTextarea(name, height, placeholder) {
        this.textareaData.push({
            'height': height,
            'name': name,
            'placeholder': placeholder
        });
        return this;
    }

    addButton(name, submit, id, button, value) {
        this.buttonData.push({
            'name': name,
            'submit': submit,
            'id': id,
            'button': button,
            'value': value
        });
        return this;
    }

    addFormValueHolder(element) {
        this.formValueHolders.push(element)
        return this;
    }

    setID(id) {
        this.id = id;
        return this;
    }

    buildEditor() {
        const editor = document.createElement('form');
        editor.className = 'editor';
        editor.method = 'POST';

        for (var i = 0; i < this.textareaData.length; i++) {
            var textarea = document.createElement('textarea');
            textarea.className = 'editor-textarea';
            textarea.placeholder = this.textareaData[i].placeholder;
            textarea.id = this.id + '-textarea-' + i;
            textarea.name = this.textareaData[i].name.toLowerCase();

            var textareaContainer = document.createElement('div');
            textareaContainer.className = 'textarea-container';
            textareaContainer.appendChild(textarea);

            var editorContainer = document.createElement('div');
            editorContainer.className = 'editor-container';

            editorContainer.appendChild(textareaContainer);
            editorContainer.style.height = this.textareaData[i].height;

            editor.appendChild(editorContainer);
        }

        const editorButtonContainer = document.createElement('div');
        editorButtonContainer.className = 'editor-button-container';

        for (var i = 0; i < this.buttonData.length; i++) {
            let id = this.buttonData[i].id;
            let name = this.buttonData[i].name;
            let submit = this.buttonData[i].submit;
            let button = this.buttonData[i].button;
            let value = this.buttonData[i].value;
            button.classList.add('default-button');
            button.classList.add('editor-button');
            button.innerHTML = name;
            button.name = name.toLowerCase();
            button.id = id;
            button.value = value;

            if (submit) {
                button.type = 'submit';
            } else {
                button.type = 'button';
            }

            configureDefaultButton(button);
            editorButtonContainer.appendChild(button);
        }

        editor.appendChild(editorButtonContainer);

        for (var i = 0; i < this.formValueHolders.length; i++) {
            console.log(this.formValueHolders[i])
            editor.appendChild(this.formValueHolders[i])
        }

        return editor;
    }

}
