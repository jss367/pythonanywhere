// Variable to hold request
var request = null;

$(document).ready(function() {
    console.log('The main_page.js has loaded');

    //Grab DOM elements to use later
    analyzeTextButton = $("#analyze-button");
    text = $("user-text");
    //Attempt number one
    analyzeTextButton.click(function() {
        text = $("#user-text").val();

        $.ajax({
            type: 'POST',
            url: "analyze",
            // Encode data as JSON.
            data: {
                html: text
            },
            // This is the type of data expected back from the server.
            dataType: 'json',
            success: function(ret) {
                //alert('JSON posted: ' + JSON.stringify(ret));
                results = ret.results
                console.log("What follows is what the main_page.js received:")
                console.log(results)
                    // verbs = ret.verbs
                    // console.log(verbs)
                displayText();
                if (results.weak_sent.length > 0) {
                    second_table();
                }
                
            }
        });
    })

});

function myFunction() {
    var x = document.getElementById("container2");
    if (x.style.display === "none") {
        x.style.display = "block";
    } else {
        x.style.display = "none";
    }
}

function displayText() {
    console.log("The displayText function has been called")
    $("#num-words").text(results.num_words);
    $("#ave-words").text(results.ave_word_size);
    $("#fk-score").text(results['Flesch Kincaid']);
    $("#unique-words").text(results.num_unique_words);
    $("#num-sentences").text(results.num_sentences);
    $("#noms").text(results['noms']);
    $("#light-verbs").text(results['light_verbs']);
    $("#weak-sent").text(results['weak_sent']);
    $("#weak-sent-num").text(results['weak_sent_num']);
    console.log(results.weak_sent.length);
}

function generate_table() {
    // get the reference for the body
    var body = document.getElementsByTagName("body")[0];

    // creates a <table> element and a <tbody> element
    var tbl = document.createElement("table");
    //var header = document.createElement("header");
    var header = '<tr><th>Sentence number</th><th>Sentence</th></tr>';

    //var header = "<th>Header</th>";
    var tblBody = document.createElement("tbody");


    // creating all cells
    for (var i = 0; i < results.weak_sent.length; i++) {
        // creates a table row
        var row = document.createElement("tr");

        for (var j = 0; j < 2; j++) {
            // Create a <td> element and a text node, make the text
            // node the contents of the <td>, and put the <td> at
            // the end of the table row
            var cell = document.createElement("td");
            if (j == 0) {
                var cellText = document.createTextNode(results.weak_sent_num[i]);
            } else {
                var cellText = document.createTextNode(results.weak_sent[i]);
            }


            cell.appendChild(cellText);
            row.appendChild(cell);
        }

        // add the row to the end of the table body
        tblBody.appendChild(row);
    }
    // This is for the quick solution
    tbl.innerHTML = header
    // put the <tbody> in the <table>
    tbl.appendChild(tblBody);



    // appends <table> into <body>
    body.appendChild(tbl);
    // sets the border attribute of tbl to 2;
    tbl.setAttribute("border", "2");
}

function second_table() {

    for (var i=0; i< results.weak_sent.length; i++)
    {
        $('#table2 > tbody:last').append('<tr><td>' + results.weak_sent_num[i] +'</td><td>' + results.weak_sent[i] + '</td>');
    }


}