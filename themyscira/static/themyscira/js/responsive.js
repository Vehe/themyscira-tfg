window.addEventListener('load', function() {

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

        // Se ejecuta al hacer la ventana más grande que el modo responsive.
        if(document.body.clientWidth > 888) {
            non_responsive_navigation.removeAttribute( 'style' );
            responsive_ico.className = "fa fa-bars";
        }

    });

    /**
     * Crea el evento para enviar el form de la barra de búsqueda al hacer clic en la lupa.
     */
    document.querySelector('.lupa-search-bar').addEventListener('click', function() {

        this.parentElement.submit();

    });

});
