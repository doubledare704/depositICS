var transparent = true;

var transparentDemo = true;
var fixedTop = false;

var navbar_initialized = false;

function initEditSwot() {
    $('a.swot-form-link, a.edit-form').click(function(event) {
        var link = $(this);
        var body = $("body");
        $.ajax({
            'url': link.attr('href'),
            'dataType': 'html',
            'type': 'get',
            'ajaxStart': function() {
                body.addClass("loading");
            },
            'ajaxStop': function() {
                body.removeClass("loading");
            },
            'success': function(data, status, xhr) {
                // check if we got successfull response from the server
                if (status != 'success') {
                    alert('There was an error on the server. Please, try again a bit later.');
                    return false;
                }

                // update modal window with arrived content from the server
                var modal = $('#myModal'),
                    html = $(data),
                    form = html.find('.col-md-4 form');
                modal.find('.modal-title').html(html.find('#content-column h2').text());
                modal.find('.modal-body').html(form);

                // init our edit form
                initEditForm(form, modal);

                // setup and show modal window finally
                modal.modal({
                    'keyboard': true,
                    'backdrop': false,
                    'show': true
                });
            },
            'error': function() {
                alert('There was an error on the server. Please, try again a bit later.');
                return false
            }
        });

        return false;
    });
}

function initEditForm(form, modal) {

    // close modal window on Cancel button click
    form.find('a.btn-warning, a.btn-info').click(function(event) {
        modal.modal('hide');
        return false;
    });

    // make form work in AJAX mode
    form.ajaxForm({
        'dataType': 'html',
        'error': function() {
            alert('There was an error on the server. Please, try again a bit later.');
            return false;
        },
        'success': function(data, status, xhr) {
            var html = $(data),
                newform = html.find('.col-md-4 form');

            // copy alert to modal window
            modal.find('.modal-body').html(html.find('.alert'));

            // copy form to modal if we found it in server response
            if (newform.length > 0) {
                modal.find('.modal-body').append(newform);

                // initialize form fields and buttons
                initEditForm(newform, modal);
            } else {
                // if no form, it means success and we need to reload page
                // to get updated students list;
                // reload after 2 seconds, so that user can read success message
                setTimeout(function() {
                    location.reload(true);
                }, 900);
            }
        }
    });
}

$(document).ready(function(){

    // Init Material scripts for buttons ripples, inputs animations etc, more info on the next link https://github.com/FezVrasta/bootstrap-material-design#materialjs
    $.material.init();
    initEditSwot();


    //  Activate the Tooltips
    $('[data-toggle="tooltip"], [rel="tooltip"]').tooltip();

    // Activate Datepicker
    if($('.datepicker').length != 0){
        $('.datepicker').datepicker({
             weekStart:1
        });
    }

    // Activate Popovers
    $('[data-toggle="popover"]').popover();

    // Active Carousel
	$('.carousel').carousel({
      interval: 400000
    });

});

materialKit = {
    misc:{
        navbar_menu_visible: 0
    },

    checkScrollForTransparentNavbar: debounce(function() {
            if($(document).scrollTop() > 260 ) {
                if(transparent) {
                    transparent = false;
                    $('.navbar-color-on-scroll').removeClass('navbar-transparent');
                }
            } else {
                if( !transparent ) {
                    transparent = true;
                    $('.navbar-color-on-scroll').addClass('navbar-transparent');
                }
            }
    }, 17),

    initSliders: function(){
        // Sliders for demo purpose
        $('#sliderRegular').noUiSlider({
            start: 40,
            connect: "lower",
            range: {
                min: 0,
                max: 100
            }
        });

        $('#sliderDouble').noUiSlider({
            start: [20, 60] ,
            connect: true,
            range: {
                min: 0,
                max: 100
            }
        });
    }
}


var big_image;

materialKitDemo = {
    checkScrollForParallax: debounce(function(){
        var current_scroll = $(this).scrollTop();

        oVal = ($(window).scrollTop() / 3);
        big_image.css({
            'transform':'translate3d(0,' + oVal +'px,0)',
            '-webkit-transform':'translate3d(0,' + oVal +'px,0)',
            '-ms-transform':'translate3d(0,' + oVal +'px,0)',
            '-o-transform':'translate3d(0,' + oVal +'px,0)'
        });

    }, 6)

}
// Returns a function, that, as long as it continues to be invoked, will not
// be triggered. The function will be called after it stops being called for
// N milliseconds. If `immediate` is passed, trigger the function on the
// leading edge, instead of the trailing.

function debounce(func, wait, immediate) {
	var timeout;
	return function() {
		var context = this, args = arguments;
		clearTimeout(timeout);
		timeout = setTimeout(function() {
			timeout = null;
			if (!immediate) func.apply(context, args);
		}, wait);
		if (immediate && !timeout) func.apply(context, args);
	};
};
