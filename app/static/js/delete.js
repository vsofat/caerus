let deleteObject = (t, id) => {
    let confirmation = confirm(`Are you sure you want to delete this ${t}?`);
    console.log(confirmation);
    if (confirmation) {
        let xhttp = new XMLHttpRequest();
        xhttp.onreadystatechange = function() {
            if (this.readyState == 4 && this.status == 200) {
                let obj = document.getElementById(`${id}`);
                obj.parentNode.removeChild(obj);
            }
        };
        xhttp.open('GET', `/delete/${t}/${id}`, true);
        xhttp.send();
    }
};