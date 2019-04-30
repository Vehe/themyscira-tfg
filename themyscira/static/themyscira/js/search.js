window.addEventListener('load', function() {

    /**
     * Añade un evento click sobre el botón de mostrar los tag de cada video, selecciona
     * el apartado de tags de el video correspondiente, y lo muestra u oculta.
     */
    document.querySelectorAll( '.a-video-info button' ).forEach(function(button) {
        button.addEventListener('click', function() {
            let tag_container_display = this.parentElement.parentElement.nextElementSibling;
            (tag_container_display.style.display == "" || tag_container_display.style.display == "none") ? tag_container_display.style.display = "block" : tag_container_display.style.display = "none";
        });
    });
    
});