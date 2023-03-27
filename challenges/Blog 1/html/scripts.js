// Cool JavaScript to show flashing text welcoming visitors to my site

// a function that resolves after waiting for d milliseconds
const sleep = d => new Promise(r => setTimeout(r, d));

async function flashText() {
	// hide the text
	document.getElementById("flashing-text").style.visibility = "hidden";

	// wait 750 milliseconds
	await sleep(750);

	// show the text
	document.getElementById("flashing-text").style.visibility = "visible";
}

flashText();
// flash the text every 1500 milliseconds
setInterval(flashText, 1500);

let flag_part_2 = "Part 2 of the flag: to_f0rm_";