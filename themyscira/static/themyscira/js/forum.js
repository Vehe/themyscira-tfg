$( document ).ready(function() {

    /**
     * Evento para detectar el scroll sobre la ventana, de tal manera que si baja 300px, muestra
     * el botón para añadir una nueva pregunta.
     */
    $( window ).scroll(function(){

        ( $( window ).scrollTop() > 300 ) ? $( '.add-new-question-button' ).fadeIn(500) : $( '.add-new-question-button' ).fadeOut(500);
    
    });

    $( '.add-new-question-button button' ).click(function() {

        $( '.add-new-question-window' ).toggle();

    });

    /**
     * Añade un evento click sobre el botón de mostrar las respuestas para cada pregunta, selecciona
     * el apartado de respuestas de la pregunta correspondiente, y lo muestra u oculta.
     */
    $( 'article button' ).click(function() {

        let element = $( this ).next().next();
        let flecha = $( this ).children();

        if(element.css( 'display' ) == "none") {

            element.slideDown();
            flecha.removeClass( 'fa-arrow-circle-down' ).addClass( 'fa-arrow-circle-up' );

        }else {

            element.slideUp();
            flecha.removeClass( 'fa-arrow-circle-up' ).addClass( 'fa-arrow-circle-down' );

        }

    });

    /**
     * Añade un evento click a la campana para activar las notificaciones sobre una pregunta determinada.
     * A el medio segundo aproximadamente abrimos el cuadro emergente para activar las notificaciones de pregunta.
     */
    $( '.notificacion' ).click(function() {

        const campana = $( this );
        campana.css( 'color', '#efb810' );

        setTimeout(function(){

            campana.closest('article').find('.active-notifications-bell').show();

        }, 700);
        
    });

    /**
     * Añade un evento al fondo negro que sale para mostrar el cartel de activar notificación, en caso de pulsarlo,
     * cierra dicho cartel.
     */
    $( '.opacity-bg-message' ).click(function() {

        $( this ).parent().parent().toggle();

    });

    /**
     * Crea el evento para borrar el cartel de mensaje al usuario el click del botón,
     * también crea un timeout para que el cartel se vaya automáticamente a los 3s.
     */
    $( '.notification-box-user button' ).click(function() {

        $( this ).parent().remove();

    });

    setTimeout(function() {

        $( '.notification-box-user' ).fadeOut(400, function() {

            $( this ).remove();

        });

    }, 3000);

});
