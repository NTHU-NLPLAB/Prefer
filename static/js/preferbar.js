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
		

		/*
		$('.menu li').find('a')
		.animate( { paddingLeft: defpadLeft, paddingRight: defpadRight}, { queue:false, duration:100 } )
		.animate( { backgroundColor: colorOut }, { queue:false, duration:200 });
		
		$(this).find('a')
		.animate( { paddingLeft: padLeft, paddingRight: padRight}, { queue:false, duration:100 } )
		.animate( { backgroundColor: colorOver }, { queue:false, duration:200 });
		*/
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
		
	//login validate	
	
	$.ajax({
	  url: "validate.html",
	  error: function(xhr){
		  alert("您尚未登入!!");
	  },
	  success: function(response){

		  $('#login').html(response);
	  }
	});	
	
	// for preview
	$.ajax({
          url: "preview.html",
          data: { 'qphrase': $('#qphrase').val() },
          error: function(xhr){
            	//alert("AJAX problem , please try again later!!");
          },
          success: function(response){
              $('#tab_ctn_container').html(response).hide();
              $('#tab_ctn_container').fadeIn(1000);;
              
          },
          complete: function(){
          		// after loading finished, display
				$.ajax({
					  url: "similar.html",
					  data: { 'qphrase': $('#qphrase').val() },
					  error: function(xhr){
						  //alert("AJAX problem , please try again later!!");
					  },
					  success: function(response){
						  $('#tab_ctn_container').html(response).fadeIn(1000);
					  }
				});
          }
    });

	
	
	
	//tab js
	$("#tab1_btn").click(function(){
		//$('#tab_ctn_container').html('<p style="text-align:center; position:relative; top:200px;"><img src="images/wait.gif" /></p>');
		var qp=$('#qphrase').val();
		$('#tab_ctn_container').html('<p style="text-align:center; position:relative; top:200px;"><img src="images/wait.gif" /></p>');
		
		$.ajax({
          url: "similar.html",
          data: { 'qphrase': $('#qphrase').val() },
          error: function(xhr){
              alert("AJAX problem , please try again later!!");
          },
          success: function(response){
              $('#tab_ctn_container').html(response).hide();
              $('#tab_ctn_container').fadeIn(1000);;
          }
      	});
      	
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
		$('#tab_ctn_container').html('<p style="text-align:center; position:relative; top:200px;"><img src="images/wait.gif" /></p>');
		//var qp=$('#qphrase').val();
		//$('#tab_ctn_container').html('preview.html?qphrase='+qp);
		
      	
		$.ajax({
          url: "extended.html",
          data: { 'qphrase': $('#qphrase').val() },
          error: function(xhr){
              alert("AJAX problem , please try again later!!");
          },
          success: function(response){
              $('#tab_ctn_container').html(response).hide();
              $('#tab_ctn_container').fadeIn(1000);;
          }
      	});
	
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
		
		$('#tab_ctn_container').html('<p style="text-align:center; position:relative; top:200px;"><img src="images/wait.gif" /></p>');
		$.ajax({
          url: "pattern.html",
          data: { 'qphrase': $('#qphrase').val() },
          error: function(xhr){
              alert("AJAX problem , please try again later!!");
          },
          success: function(response){
              $('#tab_ctn_container').html(response).hide();
              $('#tab_ctn_container').fadeIn(1000);
          }
      	});	
      	
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




	$( "#dialog:ui-dialog" ).dialog( "destroy" );
	
	var name = $( "#name" ),
		password = $( "#password" );
	
	$( "#dialog-form" ).dialog({
		autoOpen: false,
		height: 230,
		width: 380,
		modal: true,
		buttons: {
			"Login": function() {
				$.ajax({
				  url: "login.html",
				  data: { 'name': $('#name').val(), 'password': $('#password').val() },
				  type:"POST",
				  error: function(xhr){
					  alert("錯誤的帳號或密碼");
				  },
				  success: function(response){
					  $('#login').html(response);
					  $(  "#dialog-form"  ).dialog( "close" );
				  }
				});	
			},
			Cancel: function() {
				$( this ).dialog( "close" );
			}
		},
		close: function() {
			allFields.val( "" ).removeClass( "ui-state-error" );
		}
	});
	$( "#login" ).click(function() {
				$( "#dialog-form" ).dialog( "open" );
	});


	
});