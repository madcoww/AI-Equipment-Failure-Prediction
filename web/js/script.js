let box = document.getElementById('box');
let position =0;

function moveBox() {
    if (position <300) {
        position+=10
        box.style.left = position + 'px';
        requestAnimationFrame(moveBox)
    }
}
box.style.position = 'absolute';
moveBox();