document.querySelectorAll("a[single-game-deleter]").forEach(b => {
    b.addEventListener("click", function(event){
        const targetElement = event.target || event.srcElement;
        const div_id = targetElement.getAttribute('single-game-deleter')

        let found_div = document.querySelector('div[single-game-id="' + div_id + '"]')
        found_div.parentNode.removeChild(found_div);
    });
})