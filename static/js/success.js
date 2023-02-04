var urlParams = new URLSearchParams(window.location.search);
var sessionId = urlParams.get("session_id");
var customerId;

var billing = document.getElementById("billing");
if (billing) {
	billing.addEventListener('click', function(event) {
		event.preventDefault();
		var settings = {
	        "async": true,
	        "crossDomain": true,
	        "url": "customer-portal",
	        "method": "GET",
	        "headers": {
	            "Content-Type": "application/json",
	            "cache-control": "no-cache"
	        }
	    };
		$.ajax(settings)
	  .done(function(response){
	    window.location.href = response.url;
	  });
	});
}