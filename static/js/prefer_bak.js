$(document).ready(function() {	

	//Background color, mouseover and mouseout
	var colorOver = '#31b8da';
	var colorOut = '#1f1f1f';

	//Padding, mouseover
	var padLeft = '20px';
	var padRight = '20px';
	
	//Default Padding
	var defpadLeft = $('.menu li a').css('paddingLeft');
	var defpadRight = $('.menu li a').css('paddingRight');
		
	//Animate the LI on mouse over, mouse out
	$('.menu li').click(function () {	
		//Make LI clickable
		window.location = $(this).find('a').attr('href');
		
		to_show = $(this).find('a').attr('value');
		
		$(".exsent").fadeOut(0)
		$('#'+to_show).fadeIn(1000);
		
		
		$('.menu li').find('a')
		.animate( { paddingLeft: defpadLeft, paddingRight: defpadRight}, { queue:false, duration:100 } )
		.animate( { backgroundColor: colorOut }, { queue:false, duration:200 });
		
		$(this).find('a')
		.animate( { paddingLeft: padLeft, paddingRight: padRight}, { queue:false, duration:100 } )
		.animate( { backgroundColor: colorOver }, { queue:false, duration:200 });
		
	}).mouseover(function (){
		
		//mouse over LI and look for A element for transition
		/*$(this).find('a')
		.animate( { paddingLeft: padLeft, paddingRight: padRight}, { queue:false, duration:100 } )
		.animate( { backgroundColor: colorOver }, { queue:false, duration:200 });*/

	}).mouseout(function () {
	
		//mouse oout LI and look for A element and discard the mouse over transition
		/*$(this).find('a')
		.animate( { paddingLeft: defpadLeft, paddingRight: defpadRight}, { queue:false, duration:100 } )
		.animate( { backgroundColor: colorOut }, { queue:false, duration:200 });*/
	});	
	
	//Scroll the menu on mouse move above the #sidebar layer
	/*$('#sidebar').mousemove(function(e) {

		//Sidebar Offset, Top value
		var s_top = parseInt($('#sidebar').offset().top + 100);		
		
		//Sidebar Offset, Bottom value
		var s_bottom = parseInt($('#sidebar').height() + s_top);
	
		//Roughly calculate the height of the menu by multiply height of a single LI with the total of LIs
		var mheight = parseInt($('#menu li').height() * $('#menu li').length);
	
		//I used this coordinate and offset values for debuggin
		$('#debugging_mouse_axis').html("X Axis : " + e.pageX + " | Y Axis " + e.pageY);
		$('#debugging_status').html(Math.round(((s_top - e.pageY)/100) * mheight / 2));
			
		//Calculate the top value
		//This equation is not the perfect, but it 's very close	
		var top_value = Math.round(( (s_top - e.pageY) /100) * mheight / 2);
		
		//Animate the #menu by chaging the top value
		$('#menu').animate({top: top_value}, { queue:false, duration:500});
	});
	
	
	$('#sidebar2').mousemove(function(e) {

		//Sidebar Offset, Top value
		var s_top = parseInt($('#sidebar2').offset().top + 100);		
		
		//Sidebar Offset, Bottom value
		var s_bottom = parseInt($('#sidebar2').height() + s_top);
	
		//Roughly calculate the height of the menu by multiply height of a single LI with the total of LIs
		var mheight = parseInt($('#menu2 li').height() * $('#menu2 li').length);
	
		//I used this coordinate and offset values for debuggin
		$('#debugging_mouse_axis').html("X Axis : " + e.pageX + " | Y Axis " + e.pageY);
		$('#debugging_status').html(Math.round(((s_top - e.pageY)/100) * mheight / 2));
			
		//Calculate the top value
		//This equation is not the perfect, but it 's very close	
		var top_value = Math.round(( (s_top - e.pageY) /100) * mheight / 2);
		
		//Animate the #menu by chaging the top value
		$('#menu2').animate({top: top_value}, { queue:false, duration:500});
	});*/
	
	
	
	//Fixed menu
	/*$(window).scroll(function(){
					var scrollTop = $(window).scrollTop();
					if(scrollTop != 0)
						$('#nav').stop().animate({'opacity':'0.2'},400);
					else	
						$('#nav').stop().animate({'opacity':'1'},400);
				});
				
				$('#nav').hover(
					function (e) {
						var scrollTop = $(window).scrollTop();
						if(scrollTop != 0){
							$('#nav').stop().animate({'opacity':'1'},400);
						}
					},
					function (e) {
						var scrollTop = $(window).scrollTop();
						if(scrollTop != 0){
							$('#nav').stop().animate({'opacity':'0.2'},400);
						}
					}
	);*/
				
	//tab js
	$("#tab1_btn").click(function(){
		$(".tab_btn").animate({
				opacity: 0.5,
				borderWidth: 1
		}, 600 );
		$(this).animate({
				opacity: 1.0,
				borderWidth: 3
		}, 200 );
		$(".tab_ctn")
				.css({
						display: "none"
				});
		$("#tab1_ctn").fadeIn(1000);
				
     });
	$("#tab2_btn").click(function(){
		$(".tab_btn").animate({
				opacity: 0.5,
				borderWidth: 1
		}, 600 );
		$(this).animate({
				opacity: 1.0,
				borderWidth: 3
		}, 200 );
		$(".tab_ctn")
				.css({
						display: "none"
				});
		$("#tab2_ctn").fadeIn(1000);             
     });
	$("#tab3_btn").click(function(){
		$(".tab_btn").animate({
				opacity: 0.5,
				borderWidth: 1
		}, 600 );
		$(this).animate({
				opacity: 1.0,
				borderWidth: 3
		}, 200 );
		$(".tab_ctn")
				.css({
						display: "none"
				});
		$("#tab3_ctn").fadeIn(1000);             
     });


	// tooltip
	$('span.wordlist').cluetip({
		cluezIndex:500,
		arrows: false,
		dropShadow: false,
		hoverIntent: false,
		sticky: false,
		mouseOutClose: true,
		fx: {             
            open:       'fadeIn', // can be 'show' or 'slideDown' or 'fadeIn'
        	openSpeed:  '300'
    	},
		tracking: true,

	});

	$('a.expl_sent').cluetip({
		cluezIndex:500,
 
		width: 650,
		arrows: false,
		dropShadow: false,
		hoverIntent: false,
		sticky: false,
		mouseOutClose: true,
				fx: {             
            open:       'fadeIn', // can be 'show' or 'slideDown' or 'fadeIn'
        	openSpeed:  '300'
    	},
    	tracking: true,

	});
	
	$('span.translate').cluetip({
 
		cluezIndex:500,
		arrows: false,
		dropShadow: false,
		hoverIntent: false,
		sticky: false,
		mouseOutClose: true,
		fx: {             
            open:       'fadeIn', // can be 'show' or 'slideDown' or 'fadeIn'
        	openSpeed:  '300'
    	},
    	tracking: true,

	});


	
});