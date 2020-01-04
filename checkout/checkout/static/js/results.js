document.addEventListener("DOMContentLoaded", function () {
    const home_button = document.getElementById('home');

    home_button.addEventListener("click", function () {
            $.ajax({
    url         : "/",
    method      : "get",
    dataType    : 'html',
    success     :  function(data){
       $('#content').html(data);
};
    })
})