/**
 * lockScroll plugin for JQuery
 * @author Anthony McLin
 * @website http://anthonymclin.com
 * Allows you to make an element toggle between fixed and absolute layouts
 * This exposes far more options than the original
 * 
 * Based on FixedScroll JQuery plugin
 * by Dan Bentley with example at http://csswizardry.com/
 * 
 *  @options
 *   triggerElement : Optional element that will be the threshold that triggers change in scrolling behavior
 *   triggerPosition: If no triggerElement is provided, an exact pixel value is necessary for how far the page scrolls before triggering the change in scrolling behavior
 *   triggerThreshold : Override the calculated point where the scrolling page elements trigger the change in scrolling behavior
 *   offsetTop : Optionally force the distance from the top of the window for positioning the moving element
**/
(function($) {
	$.fn.lockScroll = function( settings ) {
		//Configuration
		var options = $.extend({
			triggerElement : null,
			triggerPosition: null,
			triggerThreshold : null,
			offsetTop : null
		}, settings);

		return this.each(function() {
			//Grab the element to speed up dom acess
			var el = $(this);
			
			//Make sure things can actually run
			if( options.triggerElement.length == 0 && options.triggerPosition == null ) $.error('Threshold scrolling element or value required');	//We don't have element or distance to trigger the behavior change
			if( el.css('position') != 'fixed') $.error('The element to be locked must have position:fixed');									//This won't work if the locked element isn't fixed to begin with
	
			//Get the offset of the locked element
			options.offsetTop = (!options.offsetTop) ? el.offset().top : options.offsetTop;
					
			//Find the top of the element that triggers the change
			if(!options.triggerPosition) {
				options.triggerPosition = $(options.triggerElement).offset().top;
			};
			
			//Set the threshold where the change happens
			if(!options.triggerThreshold) {
				options.triggerThreshold = options.triggerPosition - el.outerHeight();
			};
			
			//Bind to the window scroll event
			$(window).bind('load scroll', function(e) {
				if($(window).scrollTop() + options.offsetTop >= options.triggerThreshold) {
					//threshold object is above the bottom of our locked element
					el.css({ position: "absolute", top: options.triggerThreshold });
				} else {
					//threshold object is below the bottom of our locked element
					el.css({ position: "fixed", top: options.offsetTop });
				}
			});
		
		});
	};	
})(jQuery);