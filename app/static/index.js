window.onload = function () {
    // load local json file
    function loadJSON(callback) {
        var xobj = new XMLHttpRequest();
        xobj.overrideMimeType("application/json");
        var song_name = document.getElementById("song_name").innerHTML;
        xobj.open('GET', '/api/' + song_name, true);
        //xobj.open('GET', '../static/can-can.json', true);
        xobj.onreadystatechange = function () {
            if (xobj.readyState == 4 && xobj.status == "200") {
                callback(xobj.responseText);
            }
        };
        xobj.send(null);
    }

    loadJSON(function (response) {
        var data = JSON.parse(response);

        // piano
        var whiteKeyWidth = 40;
        var blackKeyWidth = 25;
        var availableKeys = ["q", "w", "e", "r", "t", "y", "u", "i", "o", "p",
            "a", "s", "d", "f", "g", "h", "j", "k", "l", ";",
            "z", "x", "c", "v", "b", "n", "m", ",", ".",
            "1", "2", "3", "4", "5", "6", "7", "8", "9", "0",
            ":", "'", "\"", "?", "/", "[", "]", "-", "=", "+",
            "!", "@", "#", "$", "%", "^", "&", "*", "(", ")"];
        var availableNotes = ["c3", "d3", "e3", "f3", "g3", "a3", "b3",
            "c4", "d4", "e4", "f4", "g4", "a4", "b4",
            "c5", "d5", "e5", "f5", "g5", "a5", "b5", "c6"]

        for (var i = availableNotes.indexOf(data.toneRange[0]); availableNotes[i] !== data.toneRange[1]; i++) {
            var key = document.createElement("div");

            key.classList.add("white");
            key.setAttribute("id", availableNotes[i]);
            document.getElementById("piano").append(key);

            // add black keys
            if (availableNotes[i][0] !== "e" && availableNotes[i][0] != "b" && availableNotes[i + 1] !== data.toneRange[1]) {
                var noteName = availableNotes[i][0] + "-" + availableNotes[i][1];

                var key = document.createElement("div");

                key.classList.add("black");
                key.setAttribute("id", noteName);

                document.getElementById("black-keys").append(key);
                key.style.left = ((i - availableNotes.indexOf(data.toneRange[0]) + 1) * (whiteKeyWidth + 2) - (blackKeyWidth / 2)) + "px";
            }
        }

        // move black key later to top
        var blackKeys = document.getElementById("black-keys");
        document.getElementById("piano").append(blackKeys);

        // TODO: override default key sizes

        // load audio
        var notes = {};
        for (var key in data.keyTone) {
            var note = new Audio("../static/notes/" + data.keyTone[key] + ".mp3");
            notes[key] = note;

            // add key labels
            var label = document.createElement("p");
            label.classList.add("label");
            label.innerHTML = key;

            document.getElementById(data.keyTone[key]).append(label);
        }
        var wrong = new Audio("../static/notes/wrong.mp3");
        function playNote(audio) {
            var clone = audio.cloneNode();
            clone.play();
        }

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

                document.getElementById(data.keyTone[key]).classList.add("pressed");

                return true;
            } else {
                // play a nasty note
                playNote(wrong);
                return false;
            }
        }

        var row = 0;
        var column = 0;

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
                    }
                }
            })

            Mousetrap.bind(key, function (e, combo) {
                document.getElementById(data.keyTone[combo]).classList.remove("pressed");
            }, "keyup");
        }

        // bind unused keys
        for (var i = 0; i < availableKeys.length; i++) {
            if (!notes[availableKeys[i]]) {
                Mousetrap.bind(availableKeys[i], function () {
                    playNote(wrong);
                });
            }
        }
    }); // end callback of loadJSON()
}
