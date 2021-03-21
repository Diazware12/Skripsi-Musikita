let star = document.querySelectorAll('input');
let showValue = document.querySelector('#rating-value');

for (let i = 0; i < star.length; i++) {
	star[i].addEventListener('click', function() {
		i = this.value;
        showValue.innerHTML = "Thank You";
	});
}

$(document).on('click', '.dropdown-menu', function (e) {
	e.stopPropagation();
  });
  
  // make it as accordion for smaller screens
  if ($(window).width() < 992) {
	$('.dropdown-menu a').click(function(e){
	  e.preventDefault();
		if($(this).next('.submenu').length){
		  $(this).next('.submenu').toggle();
		}
		$('.dropdown').on('hide.bs.dropdown', function () {
	   $(this).find('.submenu').hide();
	})
	});
  }