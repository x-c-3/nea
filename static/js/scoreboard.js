/**
 * Fetches the scoreboard.
 * @returns {Array} Ordered list in descending order of users on the scoreboard
 */
async function fetchScoreboard() {
	return await (await fetch(`/api/scoreboard`)).json()
}