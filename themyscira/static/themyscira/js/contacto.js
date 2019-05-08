let li_active;
let card_active;

window.addEventListener('load', function() {

    showJSON();

    /**
     * Selecciona los elementos li y su correspondiente card que se inician como activos.
     */
    li_active = document.querySelector('li[data-id-card="add-autor"]');
    card_active = document.getElementById('add-autor');

    document.querySelectorAll( '.contacto-nav-list ul li' ).forEach((li) => {

        /**
         * Añade un evento click a cada elemento li de la navegación.
         */
        li.addEventListener('click', (e) => {

            /**
             * Cambia la clase active sobre los elementos li de la ul.
             */
            const target = e.target;
            li_active.classList.remove('active');
            li_active = e.target;
            if(!target.classList.contains('active')) target.classList.add('active');

            /**
             * Cambia la clase hidden sobre las card correspondientes a cada li.
             */
            const card = document.getElementById(e.target.getAttribute('data-id-card'));
            card_active.classList.add('hidden');
            card_active = card;
            if(card.classList.contains('hidden')) card.classList.remove('hidden');
            

        });

    });

    /**
     * Añade un evento click al botón para volver a la página anterior en el historial.
     */
    document.getElementById('go-back').addEventListener('click', () => {
        window.history.back();
    });

});

function showJSON() {
    const data = {
        "autores": [
            {
                "name": "LiveOverflow",
                "youtube": "https://www.youtube.com/channel/UClcE-kVhqyiHCcjYwcpfj9w",
                "twitter": "https://twitter.com/LiveOverflow",
                "github": "https://github.com/LiveOverflow",
                "twitch": "https://www.twitch.tv/liveoverflow",
                "videos": [
                    {
                        "url": "yq_P3dzGiK4",
                        "title": "Fuzzing Browsers for weird XSS Vectors",
                        "tags": [
                            "fuzzing",
                            "xss",
                            "web",
                            "hacking"
                        ],
                        "timestamp": {
                                "time": [
                                "60",
                                "160",
                                "310"
                            ],
                            "data": [
                                "Chrome Debugger",
                                "Firefox",
                                "JavaScript"
                            ]
                        }
                    }
                ]
            }
        ]
    }

    document.querySelector('pre').innerHTML = JSON.stringify(data, undefined, 2);
}