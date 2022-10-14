// This script gets injected into any opened page
// whose URL matches the pattern defined in the manifest
// (see "content_script" key).
// Several foreground scripts can be declared
// and injected into the same or different pages.

console.log("This prints to the console of the page (injected only if the page url matched)")

var observerRunning = false;
var isDiscordPage = false;

var mainObserver = null;
var observerConfig = {attributes: true, subtree: true, childList: true};

function checkDiscordPage() {
	return window.location.href.indexOf('discord.com/channels/314155682033041408/577607560287485972') != -1;
}

function startObserver() {
	observerRunning = true;
	console.log("start observer")
	mainObserver = new MutationObserver(main);
	mainObserver.observe(document, observerConfig);
}

function stopObserver() {
	console.log("stop observer")
	mainObserver.disconnect();
	observerRunning = false;
}

function initLoop() {
	isDiscordPage = checkDiscordPage();

	setTimeout(() => initLoop(), 100);
	
	if (isDiscordPage && !observerRunning)
		startObserver();
	
	if (!isDiscordPage && observerRunning)
		stopObserver();
	
	//console.log("isDiscordPage = " + isDiscordPage);
	//console.log("observerRunning = " + observerRunning);
}

function main() {
	console.log("called from observer");
	//console.log(document.body.parentElement.innerHTML);
	if (checkDiscordPage())
		sendToServer();
}

function getMessagesDiv() {
	var all_divs = document.getElementsByTagName('div');
	
	var divs = [];
	for (var i = 0; i < all_divs.length; i++) {
		var div = all_divs[i];

		if (div.className.match(/^messagesWrapper.*$/)) {
			return div.innerHTML;
		}
	}
	
	return null;
}

var lastSentPageContent = "random";

function sendToServer() {
	var pageContent = getMessagesDiv();
	if (pageContent == null || pageContent == undefined)
		return;
	
	if (pageContent == lastSentPageContent) {
		console.log("Already sent this content to server")
		return;
	}
	
	let xhr = new XMLHttpRequest();
	xhr.open("POST", "http://localhost:5000/my_node");

	xhr.setRequestHeader("Accept", "application/json");
	xhr.setRequestHeader("Content-Type", "application/json");
	xhr.send(pageContent);
	lastSentPageContent = pageContent;
}

setTimeout(() => initLoop(), 100);
