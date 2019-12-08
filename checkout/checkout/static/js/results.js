var pictures=["images/apple_apricot_peach_peach(flat)_pomegranate_pear_plum_3.jpg", "images/Bananas(lady_finger)2.jpg"]

function load(){
    var gallery = document.getElementsByClassName("gallery")[0];
    gallery.getElementsByTagName("img")[0].src=pictures[1];
    gallery.getElementsByTagName("a")[0].href=pictures[1];
}