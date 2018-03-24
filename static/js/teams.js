// $(document).ready(function (e) {
//    $('.teams-list').toggle("slow");
// });


$(".league-row" ).click(function() {
	var arrow = $(this).find('i');
    // $(this).next('.teams-list').fadeToggle(600);
    $(this).next('.teams-list').toggle();
    arrow.toggleClass('fa-chevron-right');
	arrow.toggleClass('fa-chevron-down');
});

