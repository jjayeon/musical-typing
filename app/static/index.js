<<<<<<< HEAD
=======
Mousetrap.bind(
    "a",
    function () {
        console.log("You pressed a!");
    },
    "keydown"
);
Mousetrap.bind(
    "a",
    function () {
        console.log("You released a!");
    },
    "keyup"
);

>>>>>>> master
// load local json file
function loadJSON(callback) {
    var xobj = new XMLHttpRequest();
    var song_name = document.getElementById("song_name").innerHTML;
    console.log(song_name);

    xobj.overrideMimeType("application/json");
    xobj.open("GET", "/api/" + song_name, true);
    xobj.onreadystatechange = function () {
        if (xobj.readyState == 4 && xobj.status == "200") {
            callback(xobj.responseText);
        }
    };
    xobj.send(null);
}

<<<<<<< HEAD
loadJSON(function (response) {
    var data = JSON.parse(response);

    // load notes
    var notes = {};
    for (var key in data.keyTone) {
        var note = new Audio("../static/notes/" + data.keyTone[key] + ".mp3");
        notes[key] = note;
    }
    var wrong = new Audio("../static/notes/wrong.mp3");
    function playNote(audio) {
        var clone = audio.cloneNode();
        clone.play();
    }
=======
window.onload = function () {
    loadJSON(function (response) {
        var data = JSON.parse(response);
>>>>>>> master

        // load notes
        var notes = {};
        for (var key in data.keyTone) {
            var note = new Audio(
                "../static/notes/" + data.keyTone[key] + ".mp3"
            );
            notes[key] = note;
        }
        function playNote(audio) {
            var clone = audio.cloneNode();
            clone.play();
        }
<<<<<<< HEAD
        document.getElementById("scroller-content").append(scrollerP);
        lines.push(line);
    }

    // key checking logic
    function checkKey(row, column, key) {
        if (key === lines[row][column]) {
            playNote(notes[key]);
            // scroll progress bar
            document.getElementById("progress-bar").style.width = (100 * (row * lines[0].length + column + 1) / data.sequence.length) + "%";
            // change color of typed letters
            document.querySelector("#scroller-content p:nth-child(" + (row + 1) + ") span:nth-child(" + (column + 1) + ")").classList.add("typed");
            return true;
        } else {
            // play a nasty note
            playNote(wrong);
            return false;
=======

        // load scroller lines
        var lines = [];
        for (var i = 0; i < data.sequence.length; i += 10) {
            var line;
            if (i + 10 > data.sequence.length) {
                line = data.sequence.substring(i, data.sequence.length);
            } else {
                line = data.sequence.substr(i, 10);
            }
            var scrollerP = document.createElement("p");
            for (var j = 0; j < line.length; j++) {
                var charSpan = document.createElement("span");
                charSpan.textContent = line[j];
                scrollerP.append(charSpan);
            }
            document.getElementById("scroller").append(scrollerP);
            lines.push(line);
>>>>>>> master
        }

        // key checking logic
        function checkKey(row, column, key) {
            if (key === lines[row][column]) {
                playNote(notes[key]);
                return true;
            } else {
                // play a nasty note
                return false;
            }
        }

        var row = 0;
        var column = 0;

<<<<<<< HEAD
    // scrolling functionality
    document.getElementById("scroller-content").style.top = "40px";
    function scroll() {
        var animation = setInterval(frame, 5);
        var content = document.getElementById("scroller-content");
        var pos = parseInt(content.style.top);
        var goto = pos - 40;
        function frame() {
            if (pos <= goto) {
                clearInterval(animation);
            } else {
                pos--;
                content.style.top = pos + "px";
            }
        }
    }

    // bind keys
    for (var key in notes) {
        Mousetrap.bind(key, function (e, combo) {
            if (checkKey(row, column, combo)) {
                column++;
                if (column === 10) {
                    row++;
                    column = 0;
                    scroll();
=======
        // bind keys
        for (var key in notes) {
            Mousetrap.bind(key, function (e, combo) {
                if (checkKey(row, column, combo)) {
                    column++;
                    if (column === 10) {
                        row++;
                        column = 0;
                    }
>>>>>>> master
                }
            });
        }
    });
};
