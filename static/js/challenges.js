/**
 * Fetches challenges info from the api. If no challenges are provided, information about all challenges are fetched.
 * @param {Array} Array of challenges names to fetch information about
 * @returns {Array} Array of objects containing challenge information
 */
async function fetchChallengeInfos(challengeNames) {

	// if challengeNames not provided, then fetch every challenge
	if (challengeNames === undefined) {
		return await (await fetch("/api/challenges?infos=true")).json();
	}

	// otherwise, fetch only the challenges in challengeNames
	else {
		return (await (await fetch("/api/challenges?infos=true")).json())
			.filter(challengeInfo => challengeNames.includes(challengeInfo.challengeName));
	}

}

/**
 * Fetches challenge info for a specific challenge from the api.
 * @param {String} challengeName
 * @returns {Object} Object containing challenge information
 */
async function fetchChallengeInfo(challengeName) {
	return await (await fetch(`/api/challenge/${challengeName}`)).json()
}

/**
 * Fetches all the challenges from the api.
 * @returns {Array} Array of challenge names
 */
async function fetchChallengeNames() {
	return await (await fetch("/api/challenges")).json();
}

/**
 * Fetches all the solved challenges from the api of a particular user.
 * @param {String} username
 * @returns {Array} Array of solved challenge names
 */
async function fetchSolvedChallengeNames(username) {
	return await (await fetch(`/api/challenges?username=${username}`)).json();
}

/**
 * Try submitting a flag to a challenge.
 * @param {String} challengeName
 * @param {String} flag
 * @returns {Object} error/success depending on outcome
 */
async function tryFlag(challengeName, flag) {
	// submit the flag
	let resp = await fetch(`/api/challenge/${challengeName}/flag`, {
		method: "POST",
		headers: {
			"content-type": "application/x-www-form-urlencoded" // required for a POST request with a form body
		},
		body: `flag=${encodeURIComponent(flag)}` // uri encode the flag when submitting the form to defang dangerous characters
	});
	
	// extract message from fetch response
	let { message } = await resp.json();

	// if error status code, return the error - probably wrong flag
	if (!resp.ok) return { error: message };

	// otherwise, return success
	else return { success: message };
}