$(".tournament-name").click(function () {
    $(this).next('.round-group').toggle();
});


// Submit tournament on submit
$('#tournament-form').on('submit', function (event) {
    event.preventDefault();
    create_tournament();
});

// Submit clone tournament on submit
$('#clone-tournament-form').on('submit', function (event) {
    event.preventDefault();
    clone_tournament();
});

// Submit create round on click button or link
$(document).on('click', '.new-round', function (event) {
    event.preventDefault();
    var tournament_id = $(this).data('tournament-id');
    create_round(tournament_id);
});


$('#id_team1').change(function () {
    var src = $(this).find(':selected').data('src');
    if (src) {
        $('#team1_logo').attr("src", src);
    } else {
        // TODO: set class instead of attr
        $('#team1_logo').attr("src", "/static/assets/img/default-team-logo-500.png");
    }
});


$('#id_team2').change(function () {
    var src = $(this).find(':selected').data('src');
    if (src) {
        $('#team2_logo').attr("src", src);
    } else {
        // TODO: set class instead of attr
        $('#team2_logo').attr("src", "/static/assets/img/default-team-logo-500.png");
    }
});

$(function () {
    var curTab = "";
    $("#menu a").click(function () {
        $('#results').html("");
        if (curTab.length) {
            $("#" + curTab).hide();
        }
        curTab = $(this).data("tab");
        if (curTab != "container-forms") {
            $("#container-forms").hide();
        }
        $("#" + curTab).show();
    });
});

function generate_info(info, state, isSuccess) {
    var success = isSuccess;
    var state, message;

    if (state === 'success' && success) {
        state = 'success';
    } else if (state === 'danger') {
        state = 'danger';
    } else {
        state = 'warning';
    }

    message = '<fieldset class="info"><label><p class="label label-'
        + state + '">' + info
        + '</p><span class="fa fa-exclamation-triangle" aria-hidden="true"></span></label></fieldset>';

    $('form .info').remove();
    return message;
}

function create_tournament() {
    $.ajax({
        url: $('#tournament-form').data("tournament-url"),
        type: "POST",
        dataType: 'json',
        data: {
            tournament_name: $('#id_tournament_name').val(),
            tournament_prize: $('#id_prize').val()
        },
        success: function (json) {
            $('#id_tournament_name').val('');
            $('#id_prize').val('');
            $('form').append(generate_info(json.result, 'success', json.created));
            add_tournament_to_list(json);
        },
        error: function (xhr, errmsg, err) {
            handle_errors(xhr, errmsg, err);
        }
    });
}

function clone_tournament() {
    $.ajax({
        url: $('#clone-tournament-form').data("tournament-url"),
        type: "POST",
        dataType: 'json',
        data: {
            tournament_id: $('#id_clone_name').val(),
            tournament_name: $('#id_your_tournament_name').val(),
            tournament_prize: $('#id_clone_prize').val()
        },
        success: function (json) {
            $('#id_clone_prize').val('');
            $('form').append(generate_info(json.result, 'success', json.created));
            add_tournament_to_list_without_addround(json);
        },
        error: function (xhr, errmsg, err) {
            handle_errors(xhr, errmsg, err);
        }
    });
}

function create_round(tournament_id) {
    $('#rounds-list-' + tournament_id).fadeIn(600);
    $.ajax({
        url: $('#new-round-' + tournament_id).data("round-url"),
        type: "POST",
        dataType: 'json',
        data: {},
        success: function (json) {
            if (json.result != "") {
                $('form').append(generate_info(json.result, 'success', json.created));
            }
            add_round_to_list(json);
        },
        error: function (xhr, errmsg, err) {
            handle_errors(xhr, errmsg, err);
        }
    });
}

function add_tournament_to_list(json) {
    if (json.created) {
        $("#tournaments-list").prepend(
            "<div class='tournament-row'>" +
            "<div class='buttons-group tournament-buttons'>" +
            "<a class='button-yellow new-round' id='new-round-" + json.tournament_id + "' title='Add Round' href='#new-round' data-tournament-id='" + json.tournament_id + "' " +
            "data-round-url='/add_round/" + json.tournament_id + "'>+R</a>" +
            "<a class='button-yellow' title='Add Friend' href='/addfriendstotournament/" + json.tournament_id + "' >+<i class='fa fa-user'></i></a>" +
            "<a class='button-yellow' title='Remove Tournament' href='/removetournament/" + json.tournament_id + "'><i class='fa fa-trash'></i></a></div>" +
            "<h1 class='tournament-name'>" + json.name + "</h1><ul class='round-group' id='rounds-list-" + json.tournament_id + "'></ul></div>"
        );
    }
}

function add_tournament_to_list_without_addround(json) {
    if (json.created) {
        var tournament_and_rounds = "<div class='tournament-row'>" +
            "<div class='buttons-group tournament-buttons'>" +
            "<a class='button-yellow' title='Add Friend' href='/addfriendstotournament/" + json.tournament_id + "' >+<i class='fa fa-user'></i></a>" +
            "<a class='button-yellow' title='Remove Tournament' href='/removetournament/" + json.tournament_id + "'><i class='fa fa-trash'></i></a></div>" +
            "<h1 class='tournament-name'>" + json.name + "</h1><ul class='round-group' id='rounds-list-" + json.tournament_id + "'>";
        var rounds = json.rounds;
        for (var r = 0; r < rounds.length; r++) {
            tournament_and_rounds = tournament_and_rounds +
                "<li class='round-row'><h3>" + rounds[r].name + "</h3><div class='buttons-group'>" +
                "<a class='link-yellow' href='/clonedresults/" + json.tournament_id + "/" + rounds[r].id + "'>View matches</a></div></li>"
        }

        $("#tournaments-list").prepend(
            tournament_and_rounds + "</ul></div>"
        );
    }
}

function add_round_to_list(json) {
    if (!json.show_add_round) {
        $("#new-round-" + json.tournament_id).hide();
    }
    if (json.created) {
        $("#rounds-list-" + json.tournament_id).prepend(
            "<li class='round-row' >" +
            "<h3>" + json.round_name + "</h3>" +
            "<div class='buttons-group'>" +
            "<a class='link-yellow' href='/addmatch/" + json.round_id + "'>Add match</a>" +
            "</div></li>"
        );
    }
}

function handle_errors(xhr, errmsg, err) {
    var message = errmsg + " err:" + err;
    $('form').append(generate_info(message, 'danger', false));
    //console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
}

function outputUpdate() {
    var hours = $('#hours').val();
    var minutes = $('#minutes').val();
    var time;

    if (hours < 10) {
        hours = '0' + hours;
    }

    if (minutes < 10) {
        minutes = '0' + minutes;
    }

    time = hours + ':' + minutes;
    document.querySelector('#id_start_time').value = time;
}

