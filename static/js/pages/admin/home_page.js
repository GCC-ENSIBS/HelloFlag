$(document).ready(function() {

    // each toggle is a btn-group writing "true"/"false" into its hidden input
    function toggle(name) {
        var input = $("#" + name);
        var enable = $("#" + name + "-enable");
        var disable = $("#" + name + "-disable");

        function paint() {
            var on = input.val() === "true";
            enable.toggleClass("active", on);
            disable.toggleClass("active", !on);
            $("#" + name + "-enable-icon")
                .toggleClass("fa-check-square-o", on)
                .toggleClass("fa-square-o", !on);
            $("#" + name + "-disable-icon")
                .toggleClass("fa-check-square-o", !on)
                .toggleClass("fa-square-o", on);
        }

        enable.click(function() {
            input.val("true");
            paint();
        });
        disable.click(function() {
            input.val("false");
            paint();
        });
        paint();
    }

    toggle("home-show-login");
    toggle("home-show-scoreboard");

    // picking a new file drops the "remove current image" checkbox, they conflict
    $("#game_icon, #home_background").change(function() {
        $(this).closest(".controls").find("input[type=checkbox]").prop("checked", false);
    });
});
