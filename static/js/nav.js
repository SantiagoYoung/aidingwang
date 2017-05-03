$(function(){
   var index = window.location.href.split("/").length-2;
   var href = window.location.href.split("/")[index];
   var dprz = window.location.href.split("/")[4];
   var home = window.location.href.split("/")[3];
	 // $("#content #nav ul li a[href='"+ href +"']").addClass("on");

    if(home == "") {
        $(".first-nav-item").eq(0).addClass("cur");
    }

    if(href == "get_meassage") {
        $(".first-nav-item").eq(2).addClass("cur");
        $("#gl_1").removeClass("cur");
    }

    if(dprz == "store_apply") {
        $(".first-nav-item").eq(1).addClass("cur");
        $("#gl_1").removeClass("cur");
    }


});
