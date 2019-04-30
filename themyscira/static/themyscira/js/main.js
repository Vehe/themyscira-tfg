let has_been_added = false;

window.addEventListener('load', function() {

    const lista_elementos_nav = document.querySelector( '.nav-non-responsive ul' );
    const non_responsive_navigation = document.querySelector( '.nav-non-responsive' );
    const responsive_ico = document.getElementById( 'responsive-ico' );
    
    /**
     * Crea el evento para la pulsación del botón del modo responsive.
     */
    document.querySelector( '.nav-responsive' ).addEventListener('click',  function() {

        // Crear el icono X para cuando la página es responsive
        responsive_ico.classList.value.includes( 'fa-bars' ) ? responsive_ico.className = "fa fa-times" : responsive_ico.className = "fa fa-bars";

        // Mostrar la lista de los items al pulsar sobre el botón responsive
        (non_responsive_navigation.style.display == "none" || non_responsive_navigation.style.display == "") ? non_responsive_navigation.style.display = "block" : non_responsive_navigation.style.display = "none";

    });

    /**
     * Crea el evento para cuando se hace un resize de la ventana.
     */
    window.addEventListener('resize', function() {

        // Se ejecuta si se entra en modo responsive.
        if(document.body.clientWidth <= 888 && has_been_added == false) insert_search_element( lista_elementos_nav );

        // Se ejecuta al hacer la ventana más grande que el modo responsive.
        if(document.body.clientWidth > 888 && has_been_added == true) {
            non_responsive_navigation.removeAttribute( 'style' );
            responsive_ico.className = "fa fa-bars";
            has_been_added = false;
        }

    });

    /**
     * Se encarga del evento que muestra y oculta el chat del stream destacado.
     */
    document.getElementById( 'show-chat-embed' ).addEventListener('click', function() {

        const chat_embed = document.getElementById( 'chat-embed' );

        if(chat_embed.style.display == "none" || chat_embed.style.display == "") {
            chat_embed.style.display = "block";
            this.textContent = "Hidde Chat";
        } else {
            chat_embed.removeAttribute( 'style' );
            this.textContent = "Show Chat";
        }

    });

})