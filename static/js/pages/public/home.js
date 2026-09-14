$(document).ready(function() {
    var reader = new commonmark.Parser({smart: true});
    var writer = new commonmark.HtmlRenderer({safe: true});

    // the welcome page content is authored as markdown in the admin configuration
    $(".markdown").each(function() {
        var parsed = reader.parse($(this).text());
        $(this).html(writer.render(parsed).trim());
    });
});
