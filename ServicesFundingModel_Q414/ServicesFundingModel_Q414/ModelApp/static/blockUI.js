$(document).ready(function() { 
    $(".block").change(function() { 
        setTimeout(function() {
		$.blockUI({overlayCSS: { 
        backgroundColor: '#000', 
		opacity: 0.5, 
		cursor: 'wait' },
		css: {
		border: 'none',
		backgroundColor: 'none',
		opacity: .8,
		color: '#fff' },
		message: "<h1>The gremlins are hard at work!<p>Your patience is greatly appreciated.</p></h1>", 
		fadeIn: 1200})},
		4000); 
    }); 
}); 


$(document).ready(function() { 
    $(".block1").click(function() { 
        setTimeout(function() {
		$.blockUI({overlayCSS: { 
        backgroundColor: '#000', 
		opacity: 0.5, 
		cursor: 'wait' },
		css: {
		border: 'none',
		backgroundColor: 'none',
		opacity: .8,
		color: '#fff' },
		message: "<h1>The gremlins are hard at work!<p>Your patience is greatly appreciated.</p></h1>", 
		fadeIn: 1200})},
		4000); 
    }); 
}); 
