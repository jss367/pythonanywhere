// Variable to hold request
var request = null;

$(document).ready(function(){
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
            data: {html:text},
            // This is the type of data expected back from the server.
            dataType: 'json',
            success: function (ret) {
            	//alert('JSON posted: ' + JSON.stringify(ret));
            	results = ret.results
            	console.log("What follows is what the main_page.js received:")
            	console.log(results)
            	// verbs = ret.verbs
            	// console.log(verbs)
            	displayText();
            }
        });
	})

});

function displayText() {
    console.log("The displayText function has been called")
    $("#num-words").text(results.num_words);
    $("#ave-words").text(results.ave_word_size);
    $("#fk-score").text(results['Flesch Kincaid']);
    $("#unique-words").text(results.num_unique_words);
    $("#num-sentences").text(results['num_sentences']);
    $("#noms").text(results['noms']);
    $("#light-verbs").text(results['light_verbs']);
    $("#weak-sent").text(results['weak_sent']);
    $("#weak-sent-num").text(results['weak_sent_num']);
    // if (results.weak_sent.length > 1) {

    // }




    //     obj = JSON.parse(results['weak_sent'])
    //     console.log("Here are the weak sentences:")
    //     for (var i=0; i<obj.length; i++) {
    //         $("#ba").text(obj[i]);
    //         console.log(obj[i]);
    //     }



	//$("#num-words").text(results['num_words']toString());

}