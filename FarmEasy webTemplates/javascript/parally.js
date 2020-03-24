/*! parally | v1.0.0 | MIT | github.com/davismiculis/parally | @DavisMiculis */
(function($){
	var $window = $(window),
		windowHeight = $window.height();

	$window.resize(function(){
		windowHeight = $window.height();
	});

	$.fn.parally = function(params) {

		defaults = {
			speed: 0.2,
			mode: 'background',
			xpos: '50%',
			outer: true,
			offset: 0
		};

		function getHeight (el) {
			return params.outer ? el.outerHeight(true) : el.height();
		};

		// Set defaults and apply new params on top of them
		params = $.extend({}, defaults, params);

		$(this).each(function(){

			var $this = $(this),
		    	firstTop = $this.offset().top;

			// When the window is scrolled or resized
			function update(){
				var pos = $window.scrollTop(),
					top = $this.offset().top,
					height = getHeight($this),
					ypos = 0;

				// Check if above or below viewport
				if (top + height < pos || top > pos + windowHeight) {
					return;
				}

				// Calculate new Y position
				ypos = (firstTop - pos) * params.speed + params.offset;

				// Apply effect based on mode

				// CSS background-image
				if (params.mode == 'background'){
					$this.css('background-position', params.xpos+' '+ypos+'px');
				// CSS transform
				} else if (params.mode == 'transform') {
					$this.css({
						'-webkit-transform': 'translate(0,'+ypos+'px)',
						'-moz-transform': 'translate(0,'+ypos+'px)',
						'-ms-transform': 'translate(0,'+ypos+'px)',
						'transform': 'translate(0,'+ypos+'px)'
					});
				// Custom callback
				} else if (typeof params.mode === 'function') {
					params.mode(params.xpos,ypos);
				}
			}

			$window.bind('scroll', update).resize(update);
			update();

		});
	};
})(jQuery);