function tourSearchForTagPage () {
	let myTour = new Shepherd.Tour({
        defaultStepOptions: {
			classes: 'shadow-md bg-purple-dark',
			scrollTo: true
		}
    });

	myTour.addStep({
        id: 'keyword',
        title: 'Step 1',
        text: 'Enter any keyword or phrase.',
        attachTo: {
            element: '.step1',
            on: 'top'
        },
        buttons: [
            {
                text: 'Next',
                action: myTour.next
            }
        ],
        scrollTo: false
    });

    myTour.addStep({
        id: 'keyword',
        title: 'Step 2',
        text: 'Hit Enter or the Search Button to see top trending tags related to your search term.',
        attachTo: {
            element: '.step1',
            on: 'bottom'
        },
        buttons: [
            {
                text: "Close",
                action: myTour.next,
                secondary: true
            },
            {

                text: 'Do not show this again',
                action: function () {
                    var settings = {
                        "async": true,
                        "crossDomain": true,
                        "url": "set-guide-status",
                        "method": "POST",
                        "headers": {
                            "content-type": "application/x-www-form-urlencoded",
                            "cache-control": "no-cache"
                        },
                        "data": {
                            "show": false,
                            'resource': 'tag'
                        }
                    }
                    $.ajax(settings)
                    this.complete()
                }
            }
        ],
        scrollTo: false
    });
	myTour.start();
}

function tourSearchForDescriptionPage () {
	let myTour = new Shepherd.Tour({
        defaultStepOptions: {
			classes: 'shadow-md bg-purple-dark',
			scrollTo: true
		}
    });

	myTour.addStep({
        id: 'keyword',
				title: 'Step 1',
        text: 'Enter any keyword or phrase.',
        attachTo: {
            element: '.step1',
            on: 'top'
        },
        buttons: [
            {
                text: 'Next',
                action: myTour.next
            }
        ],
        scrollTo: false
    });

    myTour.addStep({
        id: 'keyword',
				title: 'Step 2',
        text: 'Hit Enter or the Search Button to see top trending keywords from all descriptions across YouTube related to your search term.',
        attachTo: {
            element: '.step1',
            on: 'bottom'
        },
        buttons: [
            {
                text: "Close",
                action: myTour.next,
                secondary: true
            },
            {
                text: 'Do not show this again',
                action: function () {
                    var settings = {
                        "async": true,
                        "crossDomain": true,
                        "url": "set-guide-status",
                        "method": "POST",
                        "headers": {
                            "content-type": "application/x-www-form-urlencoded",
                            "cache-control": "no-cache"
                        },
                        "data": {
                            "show": false,
                            'resource': 'description'
                        }
                    }
                    $.ajax(settings)
                    this.complete()
                }
            }
        ],
        scrollTo: false
    });
	myTour.start();
}

function tourSearchForSuggestionsPage () {
	let myTour = new Shepherd.Tour({
        defaultStepOptions: {
			classes: 'shadow-md bg-purple-dark',
			scrollTo: true
		}
    });

	myTour.addStep({
        id: 'keyword',
        title: 'Step 1',
        text: 'Enter any keyword or phrase.',
        attachTo: {
            element: '.step1',
            on: 'top'
        },
        buttons: [
            {
                text: 'Next',
                action: myTour.next
            }
        ],
        scrollTo: false
    });

    myTour.addStep({
        id: 'keyword',
        title: 'Step 2',
        text: 'Hit Enter or the Search Button to see top trending keyword suggestins related to your search term.',
        attachTo: {
            element: '.step1',
            on: 'bottom'
        },
        buttons: [
            {
                text: "Close",
                action: myTour.next,
                secondary: true
            },
            {

                text: 'Do not show this again',
                action: function () {
                    var settings = {
                        "async": true,
                        "crossDomain": true,
                        "url": "set-guide-status",
                        "method": "POST",
                        "headers": {
                            "content-type": "application/x-www-form-urlencoded",
                            "cache-control": "no-cache"
                        },
                        "data": {
                            "show": false,
                            'resource': 'suggestion'
                        }
                    }
                    $.ajax(settings)
                    this.complete()
                }
            }
        ],
        scrollTo: false
    });
	myTour.start();
}

function tourShowTutorialModal () {
	let myTour = new Shepherd.Tour({
        defaultStepOptions: {
			classes: 'shadow-md bg-purple-dark',
			scrollTo: true
		}
    });

	myTour.addStep({
        id: 'keyword',
        title: 'Tutorial',
        text: 'Click this button to know more about how to use these tools.',
        attachTo: {
            element: '.show-modal-button',
            on: 'right'
        },
        buttons: [
            {
                text: 'Next',
                action: myTour.next
            }
        ],
        scrollTo: false
    });

    myTour.addStep({
        id: 'keyword',
        title: 'Ready?',
        text: "All set? Just click the Close or X Button.",
        attachTo: {
            element: '.show-modal-button',
            on: 'right'
        },
        buttons: [
            {
                text: "Close",
                action: myTour.next,
                secondary: true
            },
            {

                text: 'Do not show this again',
                action: function () {
                    var settings = {
                        "async": true,
                        "crossDomain": true,
                        "url": "set-guide-status",
                        "method": "POST",
                        "headers": {
                            "content-type": "application/x-www-form-urlencoded",
                            "cache-control": "no-cache"
                        },
                        "data": {
                            "show": false,
                            'resource': 'showTutorial'
                        }
                    }
                    $.ajax(settings)
                    this.complete()
                }
            }
        ],
        scrollTo: false
    });
	myTour.start();
}
