function setHooks(selectors, successCallback, errorCallback) {
    document.querySelectorAll(selectors).forEach(item => {
        item.addEventListener('click', event => {
            event.preventDefault();
            event.stopPropagation();
            loadGameDetails(event)
                .then(response => {
                    const contentType = response.headers.get("content-type");
                    if (contentType && contentType.indexOf("application/json") !== -1){
                        return response.json()
                    }else{
                        return response.text()
                    }
                })
                .then(result => successCallback(result))
                .catch(error => errorCallback(error))
        })
    })
}

function loadGameDetails(event) {
    let target = event.target || event.srcElement || event;
    let game_id = target.getAttribute("single-game-id");
    if (game_id == null) {
        return new Promise((resolve, reject) => {
            reject("game_id == null");
        })
    }
    const options = {
        method: 'GET',
        mode: 'cors',
        cache: 'no-cache',
        credentials: 'include',
        redirect: 'follow',
        referrerPolicy: 'no-referrer',
        headers: {
            "X-CSRFToken": getCookie("csrftoken"),
            "Accept": "application/json",
            "Content-Type": "application/json"
        }
    }
    return fetch("/game_details/" + game_id, options);
}

function getCookie(cname) {
    let name = cname + "=";
    let ca = document.cookie.split(';');
    for (let i = 0; i < ca.length; i++) {
        let c = ca[i];
        while (c.charAt(0) === ' ') {
            c = c.substring(1);
        }
        if (c.indexOf(name) === 0) {
            return c.substring(name.length, c.length);
        }
    }
    return "";
}