(function myLoop() {
  setTimeout(function() {
    checkCookieSession();
    console.log("on");
    myLoop();   //  decrement i and call myLoop again if i > 0
  }, 3000)
})();

function checkCookieSession () {
  cookie = getCookie('usersession');
  logout = getCookie('logout');
  if (!cookie && !logout) {
    var settings = {
        "async": true,
        "crossDomain": true,
        "url": "logout",
        "method": "GET",
        "headers": {
            "content-type": "application/x-www-form-urlencoded",
            "cache-control": "no-cache"
        }
    }

    $.ajax(settings).done(function (response) {
      (function(send) {
          XMLHttpRequest.prototype.send = function(body) {
              console.log("interception");
          };
      })(XMLHttpRequest.prototype.send);
      document.cookie = "logout=blank; path=/; domain=" + location.hostname;
      console.log("logout");
      location.reload();
    });
  }
  if (cookie) {
    document.cookie = "logout=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/; domain=" + location.hostname;
  }
}

function getCookie(name) {
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);
  if (parts.length === 2) return parts.pop().split(';').shift();
}


$( "#search" ).click(function() {
  if ($("#keyword").val().length > 0) {
    $("#keyword").data("searched", $("#keyword").val());
    $( "#spinner" ).show();
    $( "#wait_time" ).hide();
    $( ".result" ).hide();
    $( "#wait_time" ).delay(3000).show("slow","swing");
    if ($("#search").val() == "desc"){
        search_for_description_report();
    }
    if ($("#search").val() == "tag"){
      search_for_tag_report();
    }
    if ($("#search").val() == "scraper"){
      search_by_keyword_scraper();
    }
    if ($("#search").val() == "kw"){
      search_by_keyword();
    }
    if ($("#search").val() == "descbuilder"){
      search_builder_on_word_typed();
    }
  }
});


function search(){
    var channel = $("#channel").val()
    var quantity = $("#quantity").val()

    var settings = {
        "async": true,
        "crossDomain": true,
        "url": "get-videos-info",
        "method": "GET",
        "headers": {
            "content-type": "application/x-www-form-urlencoded",
            "cache-control": "no-cache"
        },
        "data": {
            "channel_id": channel,
            "quantity": quantity
        }
    }

    $.ajax(settings).done(function (response) {
        console.log(response)
        showTable()
        pagination(response)
    })
}

function search_video(){
    var video_id = $("#video_id").val()

    var settings = {
        "async": true,
        "crossDomain": true,
        "url": "get-video-info",
        "method": "GET",
        "headers": {
            "content-type": "application/x-www-form-urlencoded",
            "cache-control": "no-cache"
        },
        "data": {
            "video_id": video_id
        }
    }

    $.ajax(settings).done(function (response) {
        console.log(response)
        showTable()
        paginationForVideo([response])
    })
}

function search_by_keyword(){
  $("#spinner").show();
  $( "#wait_time" ).hide();
  $( ".result" ).hide();
  $( "#wait_time" ).delay(3000).show("slow","swing");
	$("#tipBody").text("By using this feature, you can find the most occurring tags used on top videos.")

    var keyword = $("#keyword").val()
    var settings = {
        "async": true,
        "crossDomain": true,
        "url": "get-keyword_research-info",
        "method": "GET",
        "headers": {
            "content-type": "application/x-www-form-urlencoded",
            "cache-control": "no-cache"
        },
        "data": {
            "keyword": keyword
        }
    }

    var word = 'You can use these suggested keywords in <a href="/search-for-description-report">OUR KEYWORD SEARCH FEATURE</a> to generate the top keywords that can be used to optimize your YouTube description';
    
	showResult()
    $.ajax(settings).done(function (response) {
        $("#spinner").hide();
        console.log(response)
        $(".result").empty();
        $(".result").show();
        $('#searchLoading').attr("hidden",true);
        var list = to_list_template_new(response,word)
        $(".result").append('<div>'+list+'</div>');
        renderTag();
    })
}

function search_by_keyword_scraper(){
    var keyword = $("#keyword").val()
    $("#spinner").show();
    $( ".result" ).hide();
    $( "#wait_time" ).hide();
    $( "#wait_time" ).delay(3000).show("slow","swing");
    var settings = {
        "async": true,
        "crossDomain": true,
        "url": "get-keyword-suggestions-webscraper",
        "method": "GET",
        "headers": {
            "content-type": "application/x-www-form-urlencoded",
            "cache-control": "no-cache"
        },
        "data": {
            "keyword": keyword
        }
    }
    
    var word = 'keywords';

	showResult()
    $.ajax(settings).done(function (response) {
        $("#spinner").hide();
        $(".result").empty();
        $(".result").show();
        $('#searchLoading').attr("hidden",true);
        var list = to_list_template_new(response,word)
        $(".result").append('<div>'+list+'</div>');
        renderTag();
    })
}

function search_for_tag_report(){
	$("#tipBody").text("By using this feature, you can find the most occurring tags on top youtube videos.")

    var keyword = $("#keyword").val()
    $("#spinner").show();
    $( ".result" ).hide();
    $( "#wait_time" ).hide();
    $( "#wait_time" ).delay(3000).show("slow","swing");
    var settings = {
        "async": true,
        "crossDomain": true,
        "url": "get-tag-report",
        "method": "GET",
        "headers": {
            "content-type": "application/x-www-form-urlencoded",
            "cache-control": "no-cache"
        },
        "data": {
            "keyword": keyword
        }
    }

    var word = "These are the most used tags associated with your keyword. You can copy to a notepad and use these tags in your video's description";

	showResult()
    $.ajax(settings).done(function (response) {
        $("#spinner").hide();
        console.log(response)
        showNextBtn()
        $(".result").empty();
        $(".result").show();
        $('#searchLoading').attr("hidden",true);
        var list = to_list_template_new(response,word)
        $(".result").append('<div>'+list+'</div>');
        renderTag();
    })
}

function search_for_description_report(){
	$("#tipBody").text("By using this feature, you can find keywords that most occur top video's descriptions.")
    var keyword = $("#keyword").val()
    sessionStorage.setItem("keyword", keyword);
    $("#spinner").show();
    $( ".result" ).hide();
    $( "#wait_time" ).hide();
    $( "#wait_time" ).delay(3000).show("slow","swing");
    var settings = {
        "async": true,
        "crossDomain": true,
        "url": "get-description-report",
        "method": "GET",
        "headers": {
            "content-type": "application/x-www-form-urlencoded",
            "cache-control": "no-cache"
        },
        "data": {
            "keyword": keyword
        }
    }

    var word = 'Please remove the keywords that you feel are not relevant';   

	showResult();
    $.ajax(settings).done(function (response) {
        $("#spinner").hide();
        console.log(response);
        $(".result").empty();
        $(".result").show();
        $('#searchLoading').attr("hidden",true);
        var content = to_list_template_new(response,word)
        
        $(".result").append( '<div>' + content + '<button id="ai_page_button" class="btnbuild" onclick="go_to_ai_page()">Click Here to Write a Description Using These Keywords with AI</button>' + '</div>');
        renderTag();
    })
}

function pagination(data){
    $('#pagination-container').pagination({
        dataSource: data,
        callback: function(data, pagination) {
            // template method of yourself
            var html = simpleTemplating(data);
            $('#data-container').html(html);
        },
        pageSize: 5,
    })

}

function paginationForVideo(data){
    $('#pagination-container').pagination({
        dataSource: data,
        callback: function(data, pagination) {
            // template method of yourself
            var html = simpleTemplatingForVideo(data);
            $('#data-container').html(html);
        },
        pageSize: 5,
    })

}

function paginationForKeywordResearch(data){
    $('#pagination-container').pagination(
        {
            dataSource: data,
            callback: function(data, pagination) {
                // template method of yourself
                var html = simpleTemplatingForSearchByKeyword(data);
                $('#data-container').html(html);
            },
            pageSize: 5,
        }
    )

}

function simpleTemplating(data) {
    var html = '';
    $.each(data, function(index, item){
        html += '<tr>' +
                    '<td>'+ item.snippet.localized.title + '</td>' +
                    '<td>'+ item.statistics.viewCount + '</td>' +
                     '<td>'+ item.statistics.likeCount + '</td>' +
                     '<td>'+ item.statistics.dislikeCount + '</td>' +
                     `<td><a href="get-videos-report?video_id=${item.id}">More</a></td>`
                 +'</tr>';
    });
    return html;
}

function simpleTemplatingForVideo(data) {
    var html = '';
    $.each(data, function(index, item){
        html += '<tr>' +
                    '<td>'+ item.snippet.localized.title + '</td>' +
                    '<td>'+ item.statistics.viewCount + '</td>' +
                     '<td>'+ item.statistics.likeCount + '</td>' +
                     '<td>'+ item.statistics.dislikeCount + '</td>' +
                     `<td><a href="get-video-report?video_id=${item.id}">More</a></td>`
                 +'</tr>';
    });
    return html;
}
/*
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
*/

function to_list_template_new(data) {
    var div = '<div id="tocopy" class="simple-tags" data-simple-tags="';
    var items = '';

    $.each(data, function(index, item){
		items += item + ',';
    });

	div += items.slice(0, -1) + '"> </div> <button class="btnbuild" onclick="copyToClipboard()">Copy</button>';
    return div;
}

function go_to_ai_page(){
    div = document.getElementById('tocopy')
	var txt = '';
    
	var list = div.getElementsByTagName("li");
    
    for (i=0; i<list.length; i++){
        li = list[i];
        txt += (li.textContent || li.innerText) + ', ';
    }
	
    
    sessionStorage.setItem("content", txt);
    window.location.href = '/description-checker';
}

function renderTag () {
  var DOMSimpleTags = document.querySelectorAll(".simple-tags");
  DOMSimpleTags = Array.from(DOMSimpleTags);
  DOMSimpleTags.forEach(function (currentValue) {
    // create Tags
    new Tags(currentValue);
  });
}

function description_report_template(data){
    var ol = '<ol>';
    var li = '';
    $.each(data, function(index, item){
        li += '<li>'+ item +'</li>';
    });
    ol = ol + li;
    ol = ol + '</ol>';
    return ol;
}


function simpleTemplatingForSearchByKeyword(data) {
    var html = '';
    $.each(data, function(index, item){
        html += '<tr>' +
                    '<td><span>'+ item.snippet.title + '</span></td>' +
                     `<td><a href="get-keyword-video-report?video_id=${item.id.videoId}">More</a></td>`
                 +'</tr>';
    });
    return html;
}

function showTable(){
    $('.result').removeAttr('hidden');
}

function showResult(){
    $('.result').removeAttr('hidden');
    $('#searchLoading').removeAttr('hidden');
}
function showNextBtn(){
    $('.next_btn').removeAttr('hidden');
}

$(".search form input").keypress(function(event){
    var keycode = (event.keyCode ? event.keyCode : event.which);
    if(keycode == '13'){
        event.preventDefault();
        $( ".search form button" ).trigger( "click" );
    }
});


function copyToClipboard(elm) {
	/* Get the text field */
	//var elm = document.getElementById(elm_name);
	//var newEl = document.createElement("textarea");
	var txt = '';
    var display_message = '';
    try{
        var list = elm.getElementsByTagName("li");

        if (list.length > 0) {
            for (i=0; i<list.length; i++){
                li = list[i];
                txt += (li.textContent || li.innerText) + ', ';
            }
            txt = txt.slice(0, -2);
            
        } else {
            elm.focus();
            elm.select();
        }
    }catch(error){
        display_message = elm.id.slice(-1);
        txt = elm.innerText;
    }
    navigator.clipboard.writeText(txt)
    .then(function() {
        $("#displayMessage"+display_message).empty();
        $("#displayMessage"+display_message).append("Copied content to clipboard");
        setTimeout(function () {  $("#displayMessage"+display_message).attr("hidden",false); }, 100);
        setTimeout(function () {  $("#displayMessage"+display_message).attr("hidden",true); }, 4000);

    })
    .catch(function() {
        console.error('Failed to copy text to clipboard');
        $("#displayMessage"+display_message).empty();
        $("#displayMessage"+display_message).append("Failed to copy content to clipboard");
        setTimeout(function () {  $("#displayMessage"+display_message).attr("hidden",false); }, 100);
        setTimeout(function () {  $("#displayMessage"+display_message).attr("hidden",true); }, 4000);
    });

}
function validate(event) {
    var password = document.getElementById("newpassword").value;
    var confirmPassword = document.getElementById("repeatpassword").value;
    if (password != confirmPassword) {
        alert("Passwords do not match.");
        return false;
    }
    return true;
}

function raiseTipsModal() {
    event.preventDefault();
	$('#tipsModal').modal('show')
}

var timer;
function search_tag_on_word_typed() {
	if ($("#keyword").val().length > 0) {
		timer = setTimeout(function(){search_for_tag_report()}, 100)
	}
}

function search_keyword_on_word_typed() {
	if ($("#keyword").val().length > 0) {
		timer = setTimeout(function(){search_by_keyword()}, 100)
	}
}

function search_description_on_word_typed() {
	if ($("#keyword").val().length > 0) {
		timer = setTimeout(function(){search_for_description_report()}, 100)
	}
}

function stop_search() {
	clearTimeout(timer)
}

function getShowTour(resource){
    var settings = {
        "async": true,
        "crossDomain": true,
        "url": "get-guide-status",
        "method": "POST",
        "headers": {
            "content-type": "application/x-www-form-urlencoded",
            "cache-control": "no-cache"
        },
        "data": {
            "resource": resource
        }
    }
    return $.ajax(settings)
}

function to_list_template_new(data, text) {
    var div = '<div><p style="margin-left:20px;"> <strong> <em> These suggestions may help your videos rank higher on YouTube search. <strong><a href="#" onclick="raiseTipsModal(event)">See more ></a></strong></em> </strong></p>'+
    '<p style="margin-left:20px;">'+text+'.</p>'+'</div>' +
    '<div id="tocopy" class="simple-tags" data-simple-tags="';
    var items = '';

    $.each(data, function(index, item){
		items += item + ',';
    });

	div += items.slice(0, -1) + '"></div>' +
	 '<div class="" style="text-align:right;"> <button type="button" style="" class="btn btn-light btn-sty" onclick="copyToClipboard(tocopy)">Copy</button> &nbsp;&nbsp; <button type="button" style="float:right" class="btn btn-secondary btn-sty" onclick="save()">Save</button></div>'+
	 '<div hidden class="alert alert-secondary mt-2" role="alert" id="displayMessage"></div>';
    return div;
}


function downloadCSVFile(csv_data) {

	// Create CSV file object and feed our
	// csv_data into it
  console.log(csv_data)
  csv_data = csv_data.replace(', ', ',\n')
  console.log(csv_data)
	CSVFile = new Blob([csv_data], { type: "text/csv" });

	// Create to temporary link to initiate
	// download process
	var temp_link = document.createElement('a');

	// Download csv file
	temp_link.download = "email-list.csv";
	var url = window.URL.createObjectURL(CSVFile);
	temp_link.href = url;

	// This link should not be displayed
	temp_link.style.display = "none";
	document.body.appendChild(temp_link);

	// Automatically click the link to trigger download
	temp_link.click();
	document.body.removeChild(temp_link);
}
