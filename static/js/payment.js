// If a fetch error occurs, log it to the console and show it in the UI.
var handleFetchResult = function(result) {
  if (!result.ok) {
    return result.json().then(function(json) {
      if (json.error && json.error.message) {
        throw new Error(result.url + ' ' + result.status + ' ' + json.error.message);
      }
    }).catch(function(err) {
      showErrorMessage(err);
      throw err;
    });
  }
  return result.json();
};

// Create a Checkout Session with the selected plan ID
var createCheckoutSession = function(priceId) {
  console.log(priceId);
  return fetch("create-checkout-session", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({
      priceId: priceId
    })
  }).then(handleFetchResult);
};

// Handle any errors returned from Checkout
var handleResult = function(result) {
  if (result.error) {
    showErrorMessage(result.error.message);
  }
};

var showErrorMessage = function(message) {
  //var errorEl = document.getElementById("error-message")
  //errorEl.textContent = message;
  //errorEl.style.display = "block";
  console.log(message);
};

/* Get your Stripe publishable key to initialize Stripe.js */
fetch("setup")
  .then(handleFetchResult)
  .then(function(json) {
    var publishableKey = json.publishableKey;
    var monthlyPriceId = json.monthlyPriceId;
    var annualyPriceId = json.annualyPriceId;

    var stripe = Stripe(publishableKey);
    // Setup event handler to create a Checkout Session when button is clicked
    document.getElementById("offer1")
      .addEventListener("click", function(evt) {
			var settings = {
			    "async": true,
			    "crossDomain": true,
			    "url": "user",
			    "method": "GET",
			    "headers": {
			        "content-type": "application/x-www-form-urlencoded",
			        "cache-control": "no-cache"
			    }
			}
	    $.ajax(settings).done(function (response) {
		    console.log(response);
			  if(response.authenticated){
			        createCheckoutSession(monthlyPriceId).then(function(data) {
			          stripe.redirectToCheckout({
			            sessionId: data.sessionId
			          }).then(handleResult);
			        });
				}
				else {
          $('#goToLogin').attr('href', function (i, a){
            return a + "?offer=offer1"
          })
					$('#exampleModal').modal('show');
				}
			});
    });

    document.getElementById("offer2")
      .addEventListener("click", function(evt) {
			var settings = {
			    "async": true,
			    "crossDomain": true,
			    "url": "user",
			    "method": "GET",
			    "headers": {
			        "content-type": "application/x-www-form-urlencoded",
			        "cache-control": "no-cache"
			    }
			}
	    $.ajax(settings).done(function (response) {
		    console.log(response);
			  if(response.authenticated){
			        createCheckoutSession(annualyPriceId).then(function(data) {
			          stripe.redirectToCheckout({
			            sessionId: data.sessionId
			          }).then(handleResult);
			        });
				}
				else {
          $('#goToLogin').attr('href', function (i, a){
            return a + "?offer=offer2"
          })
					$('#exampleModal').modal('show');
				}
			});
    });
  });
