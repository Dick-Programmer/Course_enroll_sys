
//不透明度焦点函数
function item_opacity(){
	//不透明度焦点
	$("#mycarousel li, .portfolio li").hover(function() {
		$(this).siblings().stop().fadeTo(400,0.6);
	}, function() {
		$(this).siblings().stop().fadeTo(400,1);
	});
};
	

// 幻灯片放映效果
function item_hover(){
	$('ul#mycarousel li').hover(function(){		 
		$(this).children('.caption').animate({bottom:"0px"},{queue:false,duration:200});		 
		$(this).children('.lightbox').animate({top:"0px"},{queue:false,duration:200});
		$(this).children('.more').animate({top:"0px"},{queue:false,duration:200})	}, 
		function() {         
			$(this).children('.caption').animate({bottom:"-30px"},{queue:false,duration:200});		 
			$(this).children('.lightbox').animate({top:"-25px"},{queue:false,duration:200});	
			$(this).children('.more').animate({top:"-25px"},{queue:false,duration:200})
		});	
}

// 画廊悬停效果
function gallery_hover(){
	$('.gallery-item').hover(function(){		 
		$(this).children('a').animate({'opacity':0.5}, 200);
		$(this).children('.rollover').fadeIn(200); },	 
		function() {         
			$(this).children('a').animate({'opacity':1}, 200);
			$(this).children('.rollover').fadeOut(200);
		});	
}

// nivo-slider
$(window).load(function() {
	$('#slider').nivoSlider({
	    afterLoad: function(){
        var $slider = $('#slider');
        $slider.css('opacity',0);
        $('#preloader').fadeOut(500, function(){
           $slider.animate({'opacity':1}, 500);
        });
    }
	});
	
	item_hover();
	gallery_hover();
	item_opacity();
});

$(document).ready(function(){
// z-index for header
	var zIndexNumber = 1000;
		$('#top div').each(function() {
			$(this).css('zIndex', zIndexNumber);
			zIndexNumber -= 10;
		});	
		
// scrolltop按钮效果		
	$('.totop').hover(function(){	
	$(this).animate({bottom:"-5px"},{queue:false,duration:200}); },
	function() {         
		$(this).animate({bottom:"-10px"},{queue:false,duration:200})
	});
		
// 回到顶部
	$('.totop').click(function(){
            $("html, body").animate({ scrollTop: 0 }, 600);
            return false;
        });	
});
  
// 组合分类
	(function($) {
		$.fn.sorted = function(customOptions) {
			var options = {
				reversed: false,
				by: function(a) {
					return a.text();
				}
			};
	
			$.extend(options, customOptions);
	
			$data = jQuery(this);
			arr = $data.get();
			arr.sort(function(a, b) {
				var valA = options.by($(a));
				var valB = options.by($(b));
		
				if (options.reversed) {
					return (valA < valB) ? 1 : (valA > valB) ? -1 : 0;				
				} else {		
					return (valA < valB) ? -1 : (valA > valB) ? 1 : 0;	
				}
			});
			return $(arr);
		};
	})(jQuery);
	
	jQuery(function() {
		var read_button = function(class_names) {
			var r = {
				selected: false,
				type: 0
			};
			for (var i=0; i < class_names.length; i++) {
				if (class_names[i].indexOf('selected') == 0) {
					r.selected = true;
				}
			};
			return r;
		};
		var determine_sort = function($buttons) {
			var $selected = $buttons.parent().filter('[class*="selected"]');
			return $selected.find('a').attr('data-value');
		};
		var determine_kind = function($buttons) {
			var $selected = $buttons.parent().filter('[class*="selected"]');
			return $selected.find('a').attr('data-value');
		};
		var $preferences = {
			duration: 500,
			adjustHeight: 'dynamic'
		}
		var $list = jQuery('.portfolio');
		var $data = $list.clone();
		var $controls = jQuery('#filters');
			
		$controls.each(function(i) {
			var $control = jQuery(this);
			var $buttons = $control.find('a');
	
			$buttons.bind('click', function(e) {
				var $button = jQuery(this);
				var $button_container = $button.parent();
				var button_properties = read_button($button_container.attr('class').split(' '));      
				var selected = button_properties.selected;
				var button_segment = button_properties.segment;
	
				if (!selected) {
					$buttons.parent().removeClass();
					$button_container.addClass('selected');
					var sorting_type = determine_sort($controls.eq(1).find('a'));
					var sorting_kind = determine_kind($controls.eq(0).find('a'));
					if (sorting_kind == 'all') {
						var $filtered_data = $data.find('li');
					} else {
						var $filtered_data = $data.find('li.' + sorting_kind);
					}
					var $sorted_data = $filtered_data.sorted({
						by: function(v) {
							return parseInt(jQuery(v).find('.count').text());
						}
					});
					$list.quicksand($sorted_data, $preferences, function () {
						item_opacity();
						item_hover();
					});
				}
				e.preventDefault();
			});
		}); 
	});
