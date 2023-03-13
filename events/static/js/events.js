// Connect to WebSockets server

const myWebSocket = new WebSocket(`${document.body.dataset.scheme === 'http' ? 'ws' : 'wss'}://${document.body.dataset.host}/ws/events/`);
const inputTitle = document.querySelector("#event-form__title");
const inputOverview = document.querySelector("#event-form__overview");
const inputDate = document.querySelector("#event-form__date");
const inputStreet = document.querySelector("#event-form__street");
const inputCity = document.querySelector("#event-form__city");
const inputState = document.querySelector("#event-form__state");
const inputCountry = document.querySelector("#event-form__country");
const inputZipcode = document.querySelector("#event-form__zipcode");
const inputSubmit = document.querySelector("#event-form__submit")

// getData({ "action": "list events", "data": {} }, myWebSocket)

/*
    FUNCTIONS
*/

/**
 * Send an event to retrieve data from WebSockets server
 * @param {string} event
 * @param {WebSocket} webSocket
 * @return {void}
 */
function getData(event, webSocket) {
    webSocket.send(JSON.stringify(event));
}

/**
 * Send data to WebSockets server
 * @param {string} event
 * @param {WebSocket} webSocket
 * @return {void}
 */
function sendData(event, webSocket) {
    webSocket.send(JSON.stringify(event));
}

/**
 * Send new event
 * @param {Event} event
 * @return {void}
 */
function sendNewEvent(event) {
    event.preventDefault();
    // Prepare the information we will send
    const newData = {
        "action": "add event",
        "data": {
            "title": inputTitle.value,
            "overview": inputOverview.value,
            "date": inputDate.value,
            "street": inputStreet.value,
            "city": inputCity.value,
            "state": inputState.value,
            "country": inputCountry.value,
            "zipcode": inputZipcode.value
        }
    };
    // Send the data to the server
    sendData(newData, myWebSocket);
    // Clear event form
    inputTitle.value = "";
    inputOverview.value = "";
    inputDate.value = "";
    inputStreet.value = "";
    inputCity.value = "";
    inputState.value = "";
    inputCountry.value = "";
    inputZipcode.value = "";
}

/*
    EVENTS
*/

// Event when a new message is received by WebSockets
myWebSocket.addEventListener("message", (event) => {
    // Parse the data received
    const data = JSON.parse(event.data);
    console.log(data.selector);
    console.log(data.html);
    // Renders the HTML received from the Consumer
    document.querySelector(data.selector).innerHTML = data.html;
});

// Event when a new message is received by WebSockets
inputSubmit.addEventListener("click", sendNewEvent);