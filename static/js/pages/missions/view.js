$(document).ready(function() {
    barcolor();
});

function barcolor() {
    $("a[id^=unlock-game-level-button]").click(function() {
        var buyout = $(this).data("buyout");
        var banking = $(this).data("banking");
        $("#unlock-game-level-uuid").val($(this).data("uuid"));
        var description = "Would you like to unlock this level for ";
        if (banking) {
            description += "$" + buyout + "?";
        } else {
            description += buyout + " point(s)";
        }
        $("#description").text(description);
    });

    $("#unlock-game-level-submit").click(function() {
        $("#unlock-game-level-form").submit();
    });
    
    $(".minibar").each(function() {
        // let the active theme pick the colours, see .minibar-full / .minibar-partial
        var full = this.style.width == "100%";
        $(this).toggleClass('minibar-full', full).toggleClass('minibar-partial', !full);
    });
}