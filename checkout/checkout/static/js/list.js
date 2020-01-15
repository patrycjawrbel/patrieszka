document.addEventListener("DOMContentLoaded", function () {
//pobranie przyciskow Wybierz poprzez ich id
    const select_button0 = document.getElementById('select-button0');
    const select_button1 = document.getElementById('select-button1');
    const select_button2 = document.getElementById('select-button2');
    const select_button3 = document.getElementById('select-button3');
    const select_button4 = document.getElementById('select-button4');

//pobranie nazw poszczegolnych przyciskow Wybierz
    var name0 = $( "#select-button0" ).attr( "name" );
    var name1 = $( "#select-button1" ).attr( "name" );
    var name2 = $( "#select-button2" ).attr( "name" );
    var name3 = $( "#select-button3" ).attr( "name" );
    var name4 = $( "#select-button4" ).attr( "name" );

//metoda wysylajaca do serwera etykiete zdjecia po wcisnieciu pierwszego przycisku Wybierz
    select_button0.addEventListener("click", function () {
            $.ajax({
    url         : "/saveLabel",
    method      : "post",
    contentType : 'application/json',
    dataType    : 'html',
    data        : JSON.stringify({"fruitName": name0 })
});

    })
//metoda wysylajaca do serwera etykiete zdjecia po wcisnieciu drugiego przycisku Wybierz
        select_button1.addEventListener("click", function () {
            $.ajax({
    url         : "/saveLabel",
    method      : "post",
    contentType : 'application/json',
    dataType    : 'html',
    data        : JSON.stringify({"fruitName": name1 })
});

    })
//metoda wysylajaca do serwera etykiete zdjecia po wcisnieciu trzeciego przycisku Wybierz
        select_button2.addEventListener("click", function () {
            $.ajax({
    url         : "/saveLabel",
    method      : "post",
    contentType : 'application/json',
    dataType    : 'html',
    data        : JSON.stringify({"fruitName": name2 })
});

    })
//metoda wysylajaca do serwera etykiete zdjecia po wcisnieciu czwartego przycisku Wybierz
        select_button3.addEventListener("click", function () {
            $.ajax({
    url         : "/saveLabel",
    method      : "post",
    contentType : 'application/json',
    dataType    : 'html',
    data        : JSON.stringify({"fruitName": name3 })
});

    })
//metoda wysylajaca do serwera etykiete zdjecia po wcisnieciu piatego przycisku Wybierz
            select_button4.addEventListener("click", function () {
            $.ajax({
    url         : "/saveLabel",
    method      : "post",
    contentType : 'application/json',
    dataType    : 'html',
    data        : JSON.stringify({"fruitName": name4 })
});

    })
})