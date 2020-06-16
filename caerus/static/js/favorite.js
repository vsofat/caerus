let favorite = (type, id) => {
    let xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = async function() {
        if (this.readyState == 4 && this.status == 200) {
            let flash = `
            <div class="alert alert-warning text-align-center alert-dismissible fade show w-100" role="alert"
                id="favorite-${type}-${id}">
                ${this.responseText}
                <button type="button" class="close" data-dismiss="alert" aria-label="Close">
                    <span aria-hidden="true">&times;</span>
               </button>
            </div>`;
            document.getElementById('favorite-side').innerHTML += flash;
            await sleep(1500);
            $(`#favorite-${type}-${id}`).alert('close');
        }
    };
    xhttp.open('GET', `/favorite/${type}/${id}`, true);
    xhttp.send();
};

let unfavorite = (type, id) => {
    let confirmation = confirm(`Are you sure you want to unfavorite this ${type}?`);
    console.log(confirmation)
    if (confirmation) {
        let xhttp = new XMLHttpRequest();
        xhttp.onreadystatechange = function () {
            if (this.readyState == 4 && this.status == 200) {
                let obj = document.getElementById(`${type}-${id}`);
                obj.parentNode.removeChild(obj);
            }
        };
        xhttp.open('GET', `/unfavorite/${type}/${id}`, true);
        xhttp.send();
    };
};

const sleep = (time) => {
    return new Promise(resolve => {
        setTimeout(() => {
            resolve();
        }, time);
    });
};