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
  return fetch("/create-checkout-session", {
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
parent = document.getElementById('offers-parent-div');
cards = Array.from( parent.getElementsByClassName("card"));
cards.forEach((card) => {
  
button = card.getElementsByClassName("purchase-button")[0];
button.addEventListener("click", function(evt) {
text = card.getElementsByClassName("card-text")[0];
text = text.textContent;
fetch("/setup", {
  method: 'PUT',
  body: JSON.stringify(text)
  
})
  .then(handleFetchResult)
  .then(function(json) {
    var publishableKey = json.publishableKey;
    var tagSearchPriceId = json.tagSearchPriceId;

    var stripe = Stripe(publishableKey);
    // Setup event handler to create a Checkout Session when button is clicked
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
                createCheckoutSession(tagSearchPriceId).then(function(data) {
                  stripe.redirectToCheckout({
                    sessionId: data.sessionId
                  }).then(handleResult);
                });
          }
          else {
            $('#exampleModal').modal('show');
          }
        });
        });
    });
  });
