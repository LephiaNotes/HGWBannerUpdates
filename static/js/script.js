document.addEventListener('DOMContentLoaded', function() {
    function setBackgroundImage(game) {
        let bodyElement = document.getElementById('body');
        if (game === 'genshin') {
            bodyElement.style.backgroundImage = "url('/static/images/genshin.jpg')";
        } else if (game === 'wuthering') {
            bodyElement.style.backgroundImage = "url('/static/images/wuthering.jpg')";
        } else if (game === 'hsr') {
            bodyElement.style.backgroundImage = "url('/static/images/hsr.jpg')";
        }
    }

    document.getElementById('genshin-tab').addEventListener('click', function() {
        setBackgroundImage('genshin');
    });

    document.getElementById('wuthering-tab').addEventListener('click', function() {
        setBackgroundImage('wuthering');
    });

    document.getElementById('hsr-tab').addEventListener('click', function() {
        setBackgroundImage('hsr');
    });

    // Set default background image
    setBackgroundImage('genshin');
});