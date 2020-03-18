$(document).ready(function () {
    'use strict';

    //Navbar Background
    $(function () {
        $(document).scroll(function () {
            var $nav = $(".navbar-fixed-top");
            $nav.toggleClass('scrolled', $(this).scrollTop() > $nav.height());
        });
    });


    // new WOW().init();
    new WOW().init({mobile: true});


    
});