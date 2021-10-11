$(document).on("click", ".follow", function(e) {
    $(this).removeClass("follow btn-light");
    $(this).addClass("following btn-success");
    $(this).html("&check; Following");
});

$(document).on("mouseover", ".follow", function(e) {
    $(this).removeClass("btn-light");
    $(this).addClass("btn-success");
});

$(document).on("mouseout", ".follow", function(e) {
    $(this).removeClass("btn-success");
    $(this).addClass("btn-light");
});

$(document).on("click", ".following", function(e) {
    $(this).removeClass("following btn-danger");
    $(this).addClass("follow btn-light");
    $(this).html("Follow");
});

$(document).on("mouseover", ".following", function(e) {
    $(this).removeClass("btn-success");
    $(this).addClass("btn-danger");
    $(this).html("&cross; Unfollow");
});

$(document).on("mouseout", ".following", function(e) {
    $(this).removeClass("btn-danger");
    $(this).addClass("btn-success");
    $(this).html("&check; Following");
});
