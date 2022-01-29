

export function concatArrays(array, arrays) {
    for (var i = 0; i < arrays.length; i++) {
        array.concat(arrays[i]);
    }
    return array;
}

export function collectChildren(element) {
    if (element.hasChildNodes()) {
        return concatArrays(
            [element], Array.prototype.slice.call(element.childNodes).map(e => collectChildren(e))
        );
    }
    return [element];
}

export function removeClassFromElements(className, elements) {
    for (var i = 0; i < elements.length; i++) {
        var element = elements[i];
        element.classList.remove(className);
    }
}

export function addClassToElements(className, elements, timeout) {
    for (var i = 0; i < elements.length; i++) {
        var element = elements[i];
        element.classList.add(className);
    }
    if (timeout != null) {
        setTimeout(function() {
            removeClassFromElements(className, elements);
        }, timeout);
    }
}

export function bubbleUpPage(window, index, nr) {
    for (var i = 0; i < 4; i++) {
        if (
            parseInt(window.getComputedStyle(index.pg[nr]).zIndex, 10)
            < parseInt(window.getComputedStyle(index.pg[i]).zIndex, 10)
            ) {
            var j =  window.getComputedStyle(index.pg[i]).zIndex
            index.pg[i].style.zIndex = window.getComputedStyle(index.pg[nr]).zIndex;
            index.pg[nr].style.zIndex = j;
        }
    }
}

export function nodeIs(className, node) {
    try {
        return node.classList.contains(className);
    } catch (error) {
        console.trace();
        return null;
    }
}

export function relativeIndentLeft(node, parentNode, percentageGain) {
    var left = parentNode.style.left;
    var indent = parseInt(left.substring(0, left.length - 1));
    node.style.left = '' + (indent + percentageGain) + '%';
}
