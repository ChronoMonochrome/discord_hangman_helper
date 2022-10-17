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

const CHAT_MSG_TAG = "chat-messages___chat-messages-";

var msgsList = [];

function getMsgId(msgDiv) {
	var itemId = msgDiv.getAttribute("data-list-item-id");
	if (itemId)
		return itemId.split(CHAT_MSG_TAG)[1];

	return null;
}

function sendToServer() {
	var allMsgs = document.querySelectorAll(`[data-list-item-id^="${CHAT_MSG_TAG}"]`);
	
	
	allMsgs.forEach((msg) => {
		var msgId = getMsgId(msg);
		if (msgsList.indexOf(msgId) == -1) {
			msgsList.push(msgId);
			let xhr = new XMLHttpRequest();
			xhr.open("POST", "http://localhost:5000/my_node");
			xhr.setRequestHeader("Accept", "application/json");
			xhr.setRequestHeader("Content-Type", "application/json");
			xhr.send(msg.innerHTML);
		}
	});
}

setTimeout(() => initLoop(), 100);
