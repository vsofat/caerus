let favorite = (type, id) => {
    let xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            // let flash = `
            // <div class="sidenav alert alert-success text-align-center alert-dismissible fade show" role="alert">
            //     ${this.responseText}
            //     <button type="button" class="close" data-dismiss="alert" aria-label="Close">
            //         <span aria-hidden="true">&times;</span>
            //    </button>
            // </div>`;
            // document.body.innerHTML += flash;
        }
    };
    xhttp.open('GET', `/favorite/${type}/${id}`, true);
    xhttp.send();
};