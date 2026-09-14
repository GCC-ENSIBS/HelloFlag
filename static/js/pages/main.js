function wsUrl() {
    if (window.location.protocol != "https:") {
        return "ws://" + window.location.host
    } else {
        return "wss://" + window.location.host
    }
}

function getCookie(name) {
    var value = "; " + document.cookie;
    var parts = value.split("; " + name + "=");
    if (parts.length == 2) {
        return parts.pop().split(";").shift();
    }
}

function htmlEncode(value) {
    return $('<div/>').text(value).html();
}

// mark the sidebar entry for the page we are on
function markActiveNav() {
    var here = window.location.pathname.replace(/\/$/, "") || "/";
    var best = null;
    $(".hf-nav-item").each(function() {
        var path = ($(this).attr("href") || "").split("?")[0].replace(/\/$/, "");
        if (!path || path.charAt(0) !== "/") {
            return;
        }
        if (here === path || here.indexOf(path + "/") === 0) {
            if (!best || path.length > best.path.length) {
                best = { el: this, path: path };
            }
        }
    });
    if (best) {
        $(best.el).addClass("is-active");
    }
}

// wide data tables scroll inside their card instead of pushing the page
function wrapWideTables() {
    $("table.table").each(function() {
        var table = $(this);
        if (table.parent().hasClass("hf-scroll")) {
            return;
        }
        if (this.scrollWidth > table.parent().width() + 1) {
            table.wrap('<div class="hf-scroll"></div>');
        }
    });
}

// sidebar groups start collapsed; the one holding the current page stays open
function collapsibleNav() {
    var stored = {};
    try {
        stored = JSON.parse(localStorage.getItem("hf-nav-open") || "{}");
    } catch (error) {
        stored = {};
    }
    $(".hf-nav-group").each(function() {
        var group = $(this);
        // a category whose entries are all disabled has nothing left to show
        if (!group.find(".hf-nav-item").length) {
            group.remove();
            return;
        }
        var label = group.children(".hf-nav-label").first();
        if (!label.length) {
            return;
        }
        var links = label.nextAll();
        if (!links.length) {
            return;
        }
        var name = $.trim(label.text());
        links.wrapAll('<div class="hf-nav-links"></div>');
        label.replaceWith(
            $('<button type="button" class="hf-nav-label"></button>')
                .text(name)
                .append('<i class="fa fa-angle-down hf-nav-caret"></i>')
        );
        var open = group.find(".hf-nav-item.is-active").length > 0 || stored[name] === true;
        group.toggleClass("is-open", open);
    });

    $(".hf-nav-label").click(function() {
        var group = $(this).closest(".hf-nav-group").toggleClass("is-open");
        stored[$.trim($(this).text())] = group.hasClass("is-open");
        try {
            localStorage.setItem("hf-nav-open", JSON.stringify(stored));
        } catch (error) {
            /* storage is optional */
        }
    });
}

$(document).ready(function() {
    markActiveNav();
    collapsibleNav();
    wrapWideTables();
    if ($("#logout").length) {
        $("#logout").click(function() {
            $("#logout-form").submit();
        });
    }
});
