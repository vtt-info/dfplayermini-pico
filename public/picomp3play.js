

// Use global variable for status so we know if we need to send ajax if change
var button_pressed = '';

$(document).ready(function() {
// define handlers
$('#vol-inc').click(function(){ButtonVolumeInc()});
$('#vol-dec').click(function(){ButtonVolumeDec()});

$('#audio-play').click(function(){ButtonPlay()});
$('#audio-pause').click(function(){ButtonPause()});
$('#audio-stop').click(function(){ButtonStop()});


// Get number of buttons and generate list
$.get('/numfiles', '', numFilesResponse);

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

function ButtonPlayTrack(track_num) {
    //console.log("Play pressed "+track_num);
    $.get ('/play', 'track='+track_num, statusResponse);
}

function ButtonPause() {
    $.get ('/pause', '', statusResponse);
}

function ButtonStop() {
    $.get ('/stop', '', statusResponse);
}

function statusResponse (data) {
    $('#status').html(data);
}

function volumeResponse (data) {
    // If response is False then ignore
    if (data == "False") return;
    $('#vol-current').attr("alt", "Volume: "+data);
    $('#vol-current').attr("src", "audio-vol.svg?vol="+data);
}

function numFilesResponse (data) {
    var num_files = parseInt(data)
    // check it's a valid number
    if (num_files >= 0 && num_files < 999) {
        // loop over number adding image and registering as a button
        for (i=1; i < num_files+1; i++) {
            $("#tracks").append('<li><img id="track_'+i+'" src="audio-track.svg?track='+i+'" alt="Track number '+i+'"  onclick="ButtonPlayTrack('+i+');" /></li>');
            // Using javascript handler below does not work as i continues
            // to be updated prior to the anonymous function being called
            //$("#track_"+i).click(function(){ButtonPlayTrack(i)});
        }
    }
}
    