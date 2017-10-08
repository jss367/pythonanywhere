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


function second_table() {
    $('#table2 tr').remove()
    $('#table2 > thead:last').append('<tr><th>' + 'Sentence Number' + '</th><th>' + 'Sentence' + '</th></tr>');
    for (var i = 0; i < results.weak_sent.length; i++) {

        $('#table2 > tbody:last').append('<tr><td>' + results.weak_sent_num[i] + '</td><td>' + results.weak_sent[i] + '</td></tr>');
    }


}