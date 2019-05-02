const all_yt_players = {};

/**
 * Establecer la conexión con la API de YT.
 */
var tag = document.createElement('script');
tag.src = "https://www.youtube.com/iframe_api";
var firstScriptTag = document.getElementsByTagName('script')[0];
firstScriptTag.parentNode.insertBefore(tag, firstScriptTag);

/**
 * Seleccionamos todos los containers para los iframe de yt, por cada uno de ellos, crea un nuevo player
 * a través de la API de YT, y les establecemos el video que queremos ver.
 */
const players = document.querySelectorAll( 'div[data-iframe-yt]' );
function onYouTubeIframeAPIReady() {
    players.forEach(p => {
        var player = new YT.Player(p.id, {
            videoId: p.id,
        });
        all_yt_players[p.id] = player;
    });
}

/**
 * Seleccionamos todos los elementos li que tienen el timestamp.
 * Añade un evento de clic a cada uno de ellos, cuando este es pulsado, se establece el segundo
 * indicado en el atributo en el video player correspondiente.
 */
const timestamps = document.querySelectorAll( 'li[data-timestamp-yt]' );
timestamps.forEach(x => {
    x.addEventListener('click', function() {
        all_yt_players[this.parentElement.parentElement.parentElement.previousElementSibling.children[0].id].seekTo(this.getAttribute('data-timestamp-yt'));
    });
});