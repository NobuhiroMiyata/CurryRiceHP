// JavaScript Document



$(window).bind("load", function () {
	$(".op1").css({"height":"106%","top":"0"}).transition({"top":"-3%",opacity:1},1000,"easeInSine").transition({"top":"-6%"},1200,"easeOutSine");
	$(".op2").css({y:"0.3em"}).delay(1700).transition({y:0,opacity:1},1200);
	$(".op3").delay(2200).fadeTo(1000,1);
});