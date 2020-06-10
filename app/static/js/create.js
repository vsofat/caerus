let container = document.getElementById('links-container');

document.getElementById('add-link').onclick = function add() {
    let count = container.childElementCount;
    let el = document.createElement('div');
    el.classList.add('input-group');
    el.classList.add('mb-3');

    let input = document.createElement('input');
    input.type = 'text';
    input.classList.add('form-control');
    input.id = `link${count}`;
    input.name = `link${count}`;
    input.placeholder = "Add Link";

    el.appendChild(input);

    document.getElementById('links-container').appendChild(el);
    document.getElementById(`link${count}`).focus();
};