/**
 * A simple templating procedure which replaces the innerHTML of an element with a templating variable (denoted with $$var$$).
 * @param {Element} element
 * @param {Object} replacements
 */
function template(element, replacements) {
	// k is the variable name to replace
	// v is the thing that is replacing it
	for (const [k, v] of Object.entries(replacements)) {
		element.innerHTML = element.innerHTML.replaceAll(`$$${k}$$`, v)
	}
}

/**
 * Get the saved page number on a course.
 * @param {String} courseName
 * @returns {Object} pageNo, levelNo
 */
function getPage(courseName) {
	let courseBookmarks = JSON.parse(localStorage.getItem("courseBookmarks"));

	// Optional chaining here required since the page number may be null if the user has never visited this course before. In that case, return the first page/level
	let pageInfo = courseBookmarks?.[courseName];
	return {
		pageNo: pageInfo?.pageNo ?? 1,
		levelNo: pageInfo?.levelNo ?? 1
	}
}

/**
 * Set the saved page on a course.
 * @param {String} courseName
 * @param {Object} options = pageNo, levelNo
 */
function setPage(courseName, data) {
	let { pageNo, levelNo } = data;
	let courseBookmarks = JSON.parse(localStorage.getItem("courseBookmarks"));

	// If there are no course bookmarks, create an empty object
	if (!courseBookmarks) courseBookmarks = {};
	courseBookmarks[courseName] = {};
	courseBookmarks[courseName].pageNo = pageNo;
	courseBookmarks[courseName].levelNo = levelNo;

	// Re-stringify and set on localStorage
	localStorage.setItem("courseBookmarks", JSON.stringify(courseBookmarks))
}

/**
 * Get the page number and level number of the final page in the final level given a courseInfo object.
 * "maxPageNo" is a bit of a misnomer since earlier levels can have higher page numbers, however the meaning gets across.
 * @param {Object} courseInfo
 * @returns {Object} maxPageNo, maxLevelNo
 */
function getMaxPageInfo(courseInfo) {
	// convert the levels into an array of arrays, the first item being the level number and the second being the level data
	// this has to be done since objects in JavaScript have a lot of extraneous magic properties thanks to the Object prototype
	let levels = Object.entries(courseInfo.levels);

	let levelNos = levels.map(level => parseInt(level[0]) + 1);
	let pageNos = levels.map(level => level[1].challenges.length + level[1].infos.length);

	return {
		maxLevelNo: Math.max(...levelNos),
		maxPageNo: pageNos.slice(-1)[0]
	}
}

/**
 * Get the highest page number in a particular level given the array of levels.
 * @param {Array} levels
 * @param {int} levelNo
 * @returns {int} maxPageNo
 */
function getMaxPageNoInLevelFromLevels(levels, levelNo) {
	for (let level of levels) {
		if (level.levelNo === levelNo) {
			// number of challenge pages + number of information pages
			return level.challenges.length + level.infos.length;
		}
	}
}

/**
 * Takes in the output from fetching course info and converts it to the "pages" in that course.
 * @param {String} courseInfo
 * @returns {Object} Mappings of levelNo to arrays of strings.
 * Each string is fully styled and structured in HTML. It can be inserted directly into the page.
 * The string may encode information about challenges or encode information given in the infos.
 */
function courseInfoToPages(courseInfo) {
	let pages = {};
	let { levels } = courseInfo;

	for (let { infos, challenges, levelNo } of levels) {

		let pagesInLevel = [];
		
		// Pagify infos first
		for (let info of infos) pagesInLevel.push(infoToPage(info));

		// Pagify challenges second
		for (let challengeName of challenges) pagesInLevel.push(challengeNameToPage(challengeName));

		pages[levelNo] = pagesInLevel;
	}

	return pages;
}

/**
 * Helper function for courseInfoToPages to convert info-strings to fully formatted HTML pages.
 * Does this by parsing the string as Markdown using marked.js.
 * @see courseInfoToPages
 * @param {String} info
 * @returns {String} page
 */
function infoToPage(info) {
	return marked.parse(info);
}

/**
 * Helper function for courseInfoToPages to fetch a given challenge name and convert the resulting content into a fully formatted HTML page.
 * To do this, embed the challenge page in a borderless iframe. Add a postMessage listener that will trigger once the frame loads.
 * @see courseInfoToPages
 * @see showContent
 * @param {String} challengeName
 * @returns {String} page
 */
function challengeNameToPage(challengeName) {
	return `
		<p id="loadingText" class="mb-0">Loading...</p>
		<iframe class="challenge-embed d-none" frameBorder="0" src="/challenge/${challengeName}" id="challengeEmbed"></iframe>
	`
}

/**
 * Utility to tell if the window this function is called from is being embedded.
 * This works due to the fact that if a window isn't being embedded, window will be its own parent.
 */
function isEmbedded() {
	return !(window === window.parent);
}

/**
 * Unhide the content of the page. Must be called whenever a page finished loading.
 * This combats the unrendered template showing due to the delay in AJAX loading.
 */
function showContent() {
	content.classList.remove("opacity-0");

	// If we're in an iframe, tell the parent that we've finished loading
	if (isEmbedded()) parent.postMessage("Loaded", "*");
}