

// Use global variable for status so we know if we need to send ajax if change
var button_pressed = '';

$(document).ready(function() {
// define handlers
$('#vol-inc').click(function(){ButtonVolumeInc()});
$('#vol-dec').click(function(){ButtonVolumeDec()});
$('#audio-play').click(function(){ButtonPlay()});
$('#audio-pause').click(function(){ButtonPause()});
$('#audio-stop').click(function(){ButtonStop()});

$('#sw_1_2').click(function(){ButtonClicked2('1')});


}); // end ready


function ButtonVolumeInc() {
    $.get ('/volumeup', '', volumeResponse);
}

function ButtonVolumeDec() {
    $.get ('/volumedown', '', volumeResponse);
}

function ButtonPlay() {
    $.get ('/play', '', statusResponse);
}

function ButtonPause() {
    $.get ('/pause', '', statusResponse);
}

function ButtonStop() {
    $.get ('/stop', '', statusResponse);
}

// handle button 1 (eg. up)
function ButtonClicked1 (button) {
    $.get ('/play', 'point='+button+"&position=1", statusResponse);
}


// handle button 2 (eg. down)
function ButtonClicked2 (button) {
    $.get ('/stop', 'point='+button+"&position=2", displayResponse);
}


function statusResponse (data) {
    $('#status').html(data);
}

function volumeResponse (data) {
    $('#status').html("Volume: "+data);
}