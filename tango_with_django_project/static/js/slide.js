$(document).ready(function(){
  $('li.mainlevel').mousemove(function(){
  $(this).find('ul').slideDown(200);//you can give it a speed
  });
  $('li.mainlevel').mouseleave(function(){
  $(this).find('ul').slideUp(200);
  });
  
});


var mySwiper = new Swiper('.swiper-container', {
	autoplay: 5000,
	pagination : '.swiper-pagination',
	height: 300,
	prevButton:'.swiper-button-prev',
    nextButton:'.swiper-button-next',
})

$('.search i').click(function(){
  	$('.search-box').fadeIn(200);
})
$('.search-close i').click(function(){
  	$('.search-box').hide();
})

$('.banner').mouseover(function(){
	   $('.swiper-button-prev,.swiper-button-next').fadeIn();
	})
$('.banner').mouseleave(function(){
	   $('.swiper-button-prev,.swiper-button-next').fadeOut();
	})

var scrolltop = new Array();  
var i = 0;  
scrolltop[0] = 0;  
$(document).scroll(function(){  
	i++;  
	scrolltop[i] = $(document).scrollTop();  
	if (scrolltop[i] > scrolltop[i-1]) {  
		$("#tophead").fadeOut(200)  
	}else{  
		$("#tophead").fadeIn(200)  
	};  
}) 


jQuery(document).ready(function($){
	var offset = 300,
		offset_opacity = 1200,
		scroll_top_duration = 700,
		$back_to_top = $('#backtop');

	$(window).scroll(function(){
		( $(this).scrollTop() > offset ) ? $back_to_top.addClass('cd-is-visible') : $back_to_top.removeClass('cd-is-visible cd-fade-out');
		if( $(this).scrollTop() > offset_opacity ) { 
			$back_to_top.addClass('cd-fade-out');
		}
	});
});

//smooth scroll to top
$('#backtop').click(function(){
	$('body,html').animate({
			scrollTop: 0 ,
		 	},500
		);
})

$('#tooltip-f-weixin,.social-link-wechat').click(function(){
   	$('.f-weixin-dropdown').toggleClass('is-visible');
})
$('.close_tip').click(function(){
   	$('.f-weixin-dropdown').toggleClass('is-visible');
})

$('.pay-author').click(function(){
	$('.panel-reward').slideToggle(300);
	$('.action-share').toggle(false)
});

$('.J_showAllShareBtn').click(function(){
	$('.action-share').slideToggle(300);
	$('.panel-reward').toggle(false)
});


$('.closex,.mask').click(function(){
  	$('.menu').animate({left:'-100%'},200);
	$('.mask').fadeOut();
	$('#nav').hide();
	$('html,body').css('overflow','');
})
$('#mobilemenu').click(function(){
	$('#nav').show();
  	$('.menu').animate({left:'0'},200);
	$('.mask').fadeIn();
	$('html,body').css('overflow','hidden');
})