window.addEventListener('load', function() {

    /**
     * Se encarga del evento que muestra y oculta el chat del stream destacado.
     */
    document.getElementById( 'show-chat-embed' ).addEventListener('click', function() {

        const chat_embed = document.getElementById( 'chat-embed' );

        if(chat_embed.style.display == "none" || chat_embed.style.display == "") {
            document.querySelector('.streamer-info').style.display = "none";
            chat_embed.style.display = "block";
            this.textContent = "Hidde Chat";
        } else {
            document.querySelector('.streamer-info').removeAttribute( 'style' );
            chat_embed.removeAttribute( 'style' );
            this.textContent = "Show Chat";
        }

    });

})
