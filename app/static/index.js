console.log("Hello world!");

Mousetrap.bind('a', function () { console.log("You pressed a!"); }, 'keydown');
Mousetrap.bind('a', function () { console.log("You released a!"); }, 'keyup');

// load local json file
function loadJSON(callback) {
    var xobj = new XMLHttpRequest();
    xobj.overrideMimeType("application/json");
    xobj.open('GET', '../static/song-data.json', true);
    xobj.onreadystatechange = function () {
        if (xobj.readyState == 4 && xobj.status == "200") {
            callback(xobj.responseText);
        }
    };
    xobj.send(null);
}

loadJSON(function (response) {
    var data = JSON.parse(response);

    var lines = [];

    for (var i = 0; i < data.sequence.length; i += 10) {
        var line;
        if (i + 10 > data.sequence.length) {
            line = data.sequence.substring(i, data.sequence.length);
        } else {
            line = data.sequence.substr(i, 10);
        }
        console.log(line);
        var scrollerP = document.createElement("p");
        for (var j = 0; j < line.length; j++) {
            var charSpan = document.createElement("span");
            charSpan.textContent = line[j];
            scrollerP.append(charSpan);
        }
        document.getElementById("scroller").append(scrollerP);
    }
});