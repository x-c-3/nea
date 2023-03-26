/**
 * Try to log in with a given username and password.
 * @param {String} username
 * @param {String} password
 * @returns {Object} success/error message
 */
async function login(username, password) {
	fetch("/api/login", {
		method: "POST",
		headers: {
			"content-type": "application/x-www-form-urlencoded" // required for a POST request with a form body
		},
		body: `username=${encodeURIComponent(username)}&password=${encodeURIComponent(password)}` // uri encode the username and password when submitting the form to defang dangerous characters
	}).then(async r => {
		// extract message from fetch response
		let { message } = await r.json();

		if (r.ok) {
			alert(message);
		}
		else if (!r.ok) alert(message);
	})
}

/**
 * Try to register with a given username and password.
 * @param {String} username
 * @param {String} password
 * @returns {Object} success/error message
 */
async function register(username, password) {
	fetch("/api/register", {
		method: "POST",
		headers: {
			"content-type": "application/x-www-form-urlencoded" // required for a POST request with a form body
		},
		body: `username=${encodeURIComponent(username)}&password=${encodeURIComponent(password)}` // uri encode the username and password when submitting the form to defang dangerous characters
	}).then(async r => {
		// extract message from fetch response
		let { message } = await r.json();

		if (r.ok) {
			alert(message);
		}
		else if (!r.ok) alert(message);
	})
}

/**
 * Fetches info about a single user.
 * @param {String} username
 * @returns {Object} Object containing user information
 */
async function fetchUserInfo(username) {
	return await (await fetch(`/api/user/${username}`)).json()
}

/**
 * Gets a user's rank.
 * Does this by fetching the scoreboard and indexing the user.
 * @param {String} user
 * @returns {int} The user's rank, 1-indexed
 */
async function fetchUserRank(user) {
	let scoreboard = await (await fetch(`/api/scoreboard`)).json();
	for (let [i, { username }] of Object.entries(scoreboard)) {
		if (user === username) return parseInt(i) + 1;
	}
}

/**
 * Get the logged-in user's username.
 * @returns {String} username
 */
async function fetchUsername() {
	return (await (await fetch("/api/user")).json()).username;
}