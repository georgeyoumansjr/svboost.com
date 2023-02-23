function search_for_keyword_description_builder(){
    /*
	$("#tipBody").text("This tool helps you to build your YouTube video description. Just key in your topic, " +
	"hit search and top keyword suggestions will fill up the suggestion box. Optimize these keywords to your linking " +
	"and the remaining ones will be used to guide you on how to build your video description.")
    */
    var keyword = $("#keyword").val()
    var keywords = $("#keywords").val()
    //var checked_language = $("input[type='radio'][name='language']:checked").val();
    var checked_language = "";

    var settings = {
        "async": true,
        "crossDomain": true,
        "url": "get-description-builder-keywords",
        "method": "GET",
        "headers": {
            "content-type": "application/x-www-form-urlencoded",
            "cache-control": "no-cache"
        },
        "data": {
            "keyword": keyword,
            "language": [checked_language]
        }
    }
    if( keywords != '' ){
        settings['data']['keywords'] = keywords;
    }

	$('.load-animation').attr("hidden",false);
    $.ajax(settings).done(function (response) {
        if( response == 'error' ){
            return
        }
        $(".result").empty();
        $("#spinner").hide();
        $(".result").show();

        const token_amount = document.querySelector('#token_amount');
        const description_amount = document.querySelector('#description_amount');

        let value = parseInt(token_amount.textContent);
        let description_value = parseInt(description_amount.textContent);

        value-=5;
        description_value--;

        token_amount.textContent = value.toString();
        description_amount.textContent = description_value.toString();
        
        
        //re = response.slice(0, 6 + 1);
        var list = [];
        //console.log(response);
        try{
            //list = to_list_template_new(response);
            for(i=1;i<4;i++) {

                desc = '<div> Your Description: </div>'
                +'<div id="tocopy" style=" border: 1px solid gray; padding: 5px; background-color: white; box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.3); ">'+response[i]+
                '</div> <button class="btnbuild" onclick="copyToClipboard()">Copy</button>';
                
                $(".result").append(
                '<div>'
                +desc
                +'</div>'
                );
            }
           //
        }catch(error){
            //list = response;
            console.error(error)
        };
		renderTag();
    })
}

function search_builder_on_word_typed() {
	if ($("#keyword").val().length > 0) {
		timer = setTimeout(function(){search_for_keyword_description_builder()}, 1600)
	}
}

function validation_builder () {

	var elm = document.getElementById("textarea_descri");
    var txt = elm.value.trim();
		var resultSear = []

    var keywords = $("#tocopy")[0].dataset.simpleTags.split(",")
		var searchedK = $("#keyword").data().searched.split(" ");

    var result = keywords.filter(filterOut(txt.split(" ")));

		if (result.length == keywords.length) {
    	resultSear = searchedK.filter(filterOut(txt.split(" "), true, result));
		}

	if ($(".result").text().length > 0 ) {
        $("#suggestions").attr("hidden",false);
        $("#progress").attr("hidden",false);
        $("#sugList").empty();
        $("#sugList").append(list_html_generator(keywords, result));
				$("#searList").empty();
        $("#searList").append(list_html_generator(searchedK, resultSear));

				klen = keywords.length
				rlen = result.length + 0.001

				ksearLen = searchedK.length
				rsearLen = resultSear.length + 0.001

				if (resultSear.length > 0) {
					percentage = (((rlen + rsearLen) / (klen + ksearLen)) * 100)
				} else {
					percentage = ((rlen / klen) * 70)
				}
				$("#progresscheker").width(percentage + "%");
				$("#progresscheker").text(percentage.toFixed(1) + "%");
    }
    else {
        $("#suggestions").attr("hidden",true);
    }
    console.log(result);

}

function list_html_generator(data, result){
    var ol = '';
    var li = '';
    $.each(data, function(index, item){
        if (result.includes(item)){
            li += '<li><del>'+ item +'</del></li>';
        } else {
            li += '<li>'+ item +'</li>';
        }
    });
    ol = ol + li;
    ol = ol + '';
    return ol;
}
function step_one(){
	var elm = document.getElementById("textarea_descri");
    var txt = elm.value;

    var key = $("#keyword").val();

	var keywords = $("#tocopy")[0].dataset.simpleTags.split(",")
    var result = keywords.filter(filterOut(txt.split(" ")));

	console.log(key);
	console.log(keywords);
	console.log(result);

	if (result.length == keywords.length) {
		//document.cookie = "words=" + JSON.stringify(keywords);

		var settings = {
		    "async": true,
		    "crossDomain": true,
		    "url": "save-result",
		    "method": "POST",
		    "headers": {
		        "content-type": "application/x-www-form-urlencoded",
		        "cache-control": "no-cache"
		    },
		    "data": {
		        "result": txt,
		        "term": key,
		        "resource": "/description-checker"
		    }
		}

		$.ajax(settings).done(function (response) {
			$("#displayMessageDescriptionBuilder").empty();
			$("#displayMessageDescriptionBuilder").append(response.trim());

            setTimeout(function () {  $("#displayMessageDescriptionBuilder").attr("hidden",false); }, 500);
            setTimeout(function () {  $("#displayMessageDescriptionBuilder").attr("hidden",true); }, 6000);
		})
	} else {
		console.log("not enough")
	}

}

function step_two_word_monitoring(event) {
	var text = $("#textarea").val();
	var words = getCookie('words');
    words = JSON.parse(words);
    var list = to_list_template_simple(words);

	if (text.length >= 0) {
		$("#suggestions > span").html(list);
		$("#suggestions").removeAttr('hidden');

	}

	if (text.length >= 50) {
        $("#next_btn").removeAttr('hidden');
        $("#next_btn").removeAttr('disabled');
    }

	$("#counter").html(text.length);

}

var ignorecheck = false;

function step_two(event) {
	var text = $("#textarea").val();
	text_lower = text.toLowerCase();
	text_list = text_lower.split(" ");
	var words = JSON.parse(getCookie('words'));

    var result = words.filter(filterOut(text_list));
    var x = document.getElementById("gcheck");
	console.log(result.length);
    if (result.length == words.length) {
		var settings = {
            "async": true,
            "crossDomain": true,
            "url": "description-checker-step-three",
            "method": "POST",
            "headers": {
                "content-type": "application/x-www-form-urlencoded",
                "cache-control": "no-cache"
            },
            "data": {
                "intro": [text]
            }
        }

		if (!ignorecheck){
	        $.ajax(settings).done(function (response) {
	            if (Array.isArray(response)){
	                console.log(response);
	                ignorecheck = false;
	                var feedback = grammar_feedback(response);
	                $(".feedback").html(feedback);
	                $(".feedback").removeAttr('hidden');

	            } else {
	                ignorecheck = false;
	                document.open();
	                document.write(response);
	                document.close();
	            }
	        })
        } else {
            settings.data.ignorecheck = [true]
            console.log("got ignorecheck")
             $.ajax(settings).done(function (response) {
                ignorecheck = false;
                document.open();
                document.write(response);
                document.close();
            })
        }
    } else {
        console.log("Error");
    }

}

ignorecheck = false
function step_three_word_monitoring(event) {
	var text = $("#textarea").val();
	var words = getCookie('words');
    words = JSON.parse(words);
    var list = to_list_template_simple(words.slice(0, 10));

	if (text.length >= 0) {
		$("#suggestions > span").html(list);
		$("#suggestions").removeAttr('hidden');
	}

	if (text.length >= 200) {
        $("#next_btn").removeAttr('hidden');
        $("#next_btn").removeAttr('disabled');
    }

	$("#counter").html(text.length);

}


function step_three(event) {
	var text = $("#textarea").val();
	text_lower = text.toLowerCase();
	text_list = text_lower.split(" ");
	var words = JSON.parse(getCookie('words'));
	words = words.slice(0, 10);

    var result = words.filter(filterOut(text_list));
    console.log(words);
    console.log(result);
    var x = document.getElementById("gcheck");

    if (result.length == words.length) {
		var settings = {
            "async": true,
            "crossDomain": true,
            "url": "description-checker-step-four",
            "method": "POST",
            "headers": {
                "content-type": "application/x-www-form-urlencoded",
                "cache-control": "no-cache"
            },
            "data": {
                "dbody": [text]
            }
        }
		console.log(!ignorecheck);
		if (!ignorecheck){
	        $.ajax(settings).done(function (response) {
	            if (Array.isArray(response)){
	                console.log(response);
	                ignorecheck = false;
	                var feedback = grammar_feedback(response);
	                $(".feedback").html(feedback);
	                $(".feedback").removeAttr('hidden');

	            } else {
	                ignorecheck = false;
	                document.open();
	                document.write(response);
	                document.close();
	            }
	        })
        } else {
            settings.data.ignorecheck = [true]
            console.log("got ignorecheck")
            ignorecheck = false;
             $.ajax(settings).done(function (response) {
                document.open();
                document.write(response);
                document.close();
            })
        }
    } else {
        console.log("Error");
    }

}

function grammar_feedback(grammar_correction) {
	var html = '' + '<h5>You have some grammars problems</h5>'
	+ '<div id="do_check" onclick="yn()">'
	+ 'Want to see grammar suggestions?&nbsp;'
	+ '<label for="yes">Yes</label><input type="radio" id="yes" name="gc" value="yes">&nbsp;'
	+ '<label for="no">No</label><input type="radio" id="no" name="gc" value="no">'
	+ '</div>'
	+ '<div hidden id="gcheck">'
	+ ask_grammar_check(grammar_correction)
	+ '</div>';


	return html;

}

function yn () {
	var yesno = $("input[type='radio'][name='gc']:checked").val();
	if (yesno === "yes") {
		$("#gcheck").removeAttr('hidden');
		ignorecheck = false;
	} else {
		ignorecheck = true;
	}
}

function ask_grammar_check(grammar_correction) {
	var html = ''
	+ 'Suggestion are as follow: error (correction)';
    	grammar_correction.forEach(
    		function (item, index) {
    			console.log(item);
    			html += '<div>'
    			+ item.errors + ' (' + ((item.corrections.length > 1)? item.corrections.join(', ') : item.corrections[0]) + ')'
    			+'</div>';
    		}
    	);

    	return html;
}

function filterOut(txt, moreMatch = false, aux = []) {
	return function (e) {
		i = -1;
		txt.forEach(function (element, index, array) {
			var r = new RegExp("\\b" + e.toLowerCase() + "\\b", "g")
			var res = array.join(" ").toLowerCase().match(r);
      if (res){
          if(moreMatch == false && res.length >= 1) {
              i = index;
          } else if (moreMatch == true && res.length >= 4) {
							i = index;
					}
					else if (moreMatch == true && res.length >= 3 && !aux.includes(e.toLowerCase())) {
							i = index;
					}
      }
    });

    if (i >= 0){
        return txt[i];
    } else {
        return false;
    }

	}
}


$("#textarea").keydown(function(event) {
	var text = $("#textarea").val();
    if (event.keyCode === 8 || event.keyCode === 46) {
        $("#counter").html(text.length);
    }

    if (text.length < 120) {
        $("#warning").attr('hidden', true);
    }
});

function getCookie(cname) {
  var name = cname + "=";
  var decodedCookie = decodeURIComponent(document.cookie);
  var ca = decodedCookie.split(';');
  for(var i = 0; i <ca.length; i++) {
    var c = ca[i];
    while (c.charAt(0) == ' ') {
      c = c.substring(1);
    }
    if (c.indexOf(name) == 0) {
      return c.substring(name.length, c.length);
    }
  }
  return "";
}

function to_list_template_simple(data) {
    var html = '';
    $.each(data, function(index, item){
        html +=  item + '; ';
    });
    return html;
}

function to_list_template(data) {
    var ol = '<ol class="list-inline">';
    var li = '';
    $.each(data, function(index, item){
        index = index + 1
        if (index < 6){
            li += '<li class="list-inline-item"><span class="badge badge-success p-2 m-2">' + index + ' - ' + item +'</span></li>';
        } else {
            li += '<li class="list-inline-item"><span class="badge badge-secondary p-2 m-2">' + index + ' - ' + item +'</span></li>';
        }
    });
    ol = ol + li;
    ol = ol + '</ol>';
    return ol;
}

function save(){
    var key = $("#keyword").val();

	var keywords = $("#tocopy")[0].dataset.simpleTags.split(",")

    var resource = window.location.pathname;
    console.log(resource);
    console.log(key);
    console.log(keywords);

	var settings = {
	    "async": true,
	    "crossDomain": true,
	    "url": "save-result",
	    "method": "POST",
	    "headers": {
	        "content-type": "application/x-www-form-urlencoded",
	        "cache-control": "no-cache"
	    },
	    "data": {
	        "result": keywords,
	        "term": key,
	        "resource": resource
	    }
	}

	$.ajax(settings).done(function (response) {
		$("#displayMessage").empty();
		$("#displayMessage").append(response);

		setTimeout(function () {  $("#displayMessage").attr("hidden",false); }, 500);
		setTimeout(function () {  $("#displayMessage").attr("hidden",true); }, 6000);

	})

}


function renderTag () {
  var DOMSimpleTags = document.querySelectorAll(".simple-tags");
  DOMSimpleTags = Array.from(DOMSimpleTags);
  DOMSimpleTags.forEach(function (currentValue) {
    // create Tags
    new Tags(currentValue);
  });
}
