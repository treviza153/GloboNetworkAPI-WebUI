$(document).ready(function() {

    $("#dialog-form").dialog({
        width: 600,
        height: 300,
        modal: true,
        autoOpen: false,
        draggable: false,
        resizable: false,
        buttons: {}
    });

    autocomplete("/autocomplete/equipment/", true, "search_equip", false);

    $("#search_form").submit(function(event) {
        event.preventDefault();
        console.log("log:");
        console.log(event);
        url = "/interface/connect/{{ id_interface }}/{{ front_or_back }}/0";
        form = $("#search_form").serialize();
        $.ajax({
            url: url,
            data: form,
            type: "GET",
            complete: function(xhr, status) {
                if (xhr.status == "500") {
                    $("#dialog-form").dialog("close");
                    location.reload();
                } else if (xhr.status == "278" || xhr.status == "302") {
                    $("#dialog-form").dialog("close");
                    window.location = xhr.getResponseHeader('Location');
                } else if (xhr.status == "200") {
                    $("#dialog-form").html(xhr.responseText);
                    $("#dialog-form").dialog("open");
                } else {
                    $("#dialog-form").dialog("close");
                }
            }
        });
    });

    $("#btn_search").button({ icons: {primary: "ui-icon-check"} }).click(function(){ $("#search_form").submit(); });
});