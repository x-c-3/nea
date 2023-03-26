/**
 * Fetches course info from the api. If no courses are provided, information about all courses are fetched.
 * @param {Array} courseNames
 * @returns {Array} Array of objects containing course information
 */
async function fetchCourseInfos(courseNames) {

	// if courseNames not provided, then fetch every course
	if (courseNames === undefined) {
		return await (await fetch("/api/courses?infos=true")).json();
	}

	// otherwise, fetch only the challenges in challengeNames
	else {
		return (await (await fetch("/api/courses?infos=true")).json())
			.filter(courseInfo => courseNames.includes(courseInfo.courseName));
	}

}

/**
 * Fetches course info for a specific course from the api.
 * @param {String} courseName
 * @returns {Object} Object containing course information
 */
async function fetchCourseInfo(courseName) {
	return await (await fetch(`/api/course/${courseName}`)).json();
}

/**
 * Fetches all the course names from the api.
 * @returns {Array} Array of course names
 */
async function fetchCourseNames() {
	return await (await fetch("/api/courses")).json();
}

/**
 * Fetches all the solved course names from the api of a particular user.
 * @param {String} username
 * @returns {Array} Array of solved course names
 */
async function fetchSolvedCourseNames(username) {
	return await (await fetch(`/api/courses?username=${username}`)).json();
}

/**
 * Try solving a course.
 * @param {String} courseName
 * @returns {Object} error/success depending on outcome
 */
async function trySolve(courseName) {
	let resp = await fetch(`/api/course/${courseName}/solve`, { method: "POST" });
	
	// extract message from fetch response
	let { message } = await resp.json();

	// if error status code, return the error
	if (!resp.ok) return { error: message };

	// otherwise, return success
	else return { success: message };
}