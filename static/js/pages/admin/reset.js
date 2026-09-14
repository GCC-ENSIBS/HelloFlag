$(document).ready(function() {
    // destructive admin actions ask before they run
    $(".hf-confirm").click(function(event) {
        if (!confirm("Are you sure?")) {
            event.preventDefault();
        } else {
            document.body.style.cursor = "wait";
        }
    });
});
