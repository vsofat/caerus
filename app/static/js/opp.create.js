let container = document.getElementById('links-container');

document.querySelector('#links-container').addEventListener('click', function(e) {
    if(e.target.id.substring(0,8) == 'add-link') {
        let count = container.childElementCount;
        container.innerHTML += `
        <div class="input-group mb-3">
            <input type="text" class="form-control" placeholder="Link" id="link${count}">
            <div class="input-group-append">
                <button class="btn btn-outline-secondary" type="button" id="add-link-${count}">Add Link</button>
            </div>
        </div>`;
        document.getElementById(`link${count}`).focus();
    }
})