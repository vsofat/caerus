let deleteObject = (type, id) => {
    let confirmation = confirm(`Are you sure you want to delete this ${type}?`);
    if (confirmation) {
        let xhttp = new XMLHttpRequest();
        xhttp.onreadystatechange = async function() {
            if (this.readyState == 4 && this.status == 200) {
                let obj = document.getElementById(`${type}-${id}`);
                obj.parentNode.removeChild(obj);
            }
        };
        xhttp.open('GET', `/delete/${type}/${id}`, true);
        xhttp.send();
    }
};