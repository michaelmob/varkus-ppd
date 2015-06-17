var unslider = $(".banner").unslider({ speed: 300, delay: 8000, keys: true, dots: false, fluid: true });
$(".next").click(function() { unslider.data('unslider').next(); });
$(".prev").click(function() { unslider.data('unslider').prev(); });