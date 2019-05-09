let btn_active;
let panel_active;

$(document).ready(function(){

    btn_active = $('.selection-requests .active');
    panel_active = $('.content.active');
    
    $('.selection-requests .option-requests').click(function() {

        /**
         * Cambia la clase active entre los botones de la navegación.
         */
        if( !$(this).hasClass('active')) {

            $(this).addClass('active');
            $(btn_active).removeClass('active');
            btn_active = this;

            $('#' + $(this).attr('data-asociated-panel')).removeClass('hidden');
            $(panel_active).addClass('hidden');
            panel_active = $('#' + $(this).attr('data-asociated-panel'));
            
        }

    });

    /**
     * Añade los eventos para borrar el cartel de notificación al usuario.
     */
    $('.notificacion-usuario div p span').click(function() {

        $( this ).parent().parent().parent().remove();

    });

    setTimeout(function() {

        $( '.notificacion-usuario' ).fadeOut(400, function() {

            $( this ).remove();

        });

    }, 3000);

});