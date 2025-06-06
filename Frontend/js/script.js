// Base URL for your Django API (ensure it matches your Django server address)
const API_BASE_URL = 'http://127.0.0.1:8000/api';

/**
 * Helper function to get the CSRF token from the DOM.
 * Django automatically embeds this in the template if the csrf_token tag is used.
 */
function getCsrfToken() {
    const csrfInput = document.querySelector('input[name="csrfmiddlewaretoken"]');
    return csrfInput ? csrfInput.value : '';
}

// --- Utility Functions ---

/**
 * Displays a temporary message box for notifications.
 * @param {string} message - The message to display.
 * @param {boolean} isError - True if it's an error message, false for success.
 */
function showMessageBox(message, isError = false) {
    const messageBox = document.getElementById('messageBox');
    messageBox.textContent = message;
    messageBox.className = 'message-box'; // Reset classes
    if (isError) {
        messageBox.classList.add('error');
    }
    messageBox.style.display = 'block';
    setTimeout(() => {
        messageBox.style.display = 'none';
    }, 3000); // Hide after 3 seconds
}

/**
 * Fetches data from a given API endpoint.
 * @param {string} endpoint - The API endpoint (e.g., '/students/').
 * @returns {Promise<Array>} - A promise that resolves to an array of data.
 */
async function fetchData(endpoint) {
    try {
        const response = await fetch(`${API_BASE_URL}${endpoint}`);
        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(`HTTP error! Status: ${response.status} - ${JSON.stringify(errorData)}`);
        }
        return await response.json();
    } catch (error) {
        console.error('Error fetching data:', error);
        showMessageBox(`Error fetching data: ${error.message}`, true);
        return []; // Return empty array on error
    }
}

/**
 * Sends data to a given API endpoint (POST/PUT).
 * Includes CSRF token for non-GET requests.
 * @param {string} endpoint - The API endpoint.
 * @param {string} method - HTTP method ('POST', 'PUT', 'PATCH').
 * @param {Object} data - The data to send.
 * @returns {Promise<Object>} - A promise that resolves to the response data.
 */
async function sendData(endpoint, method, data) {
    const headers = {
        'Content-Type': 'application/json',
    };

    // Add CSRF token for unsafe methods (POST, PUT, PATCH, DELETE)
    // Django's CSRF protection is primarily for forms, but good practice for AJAX
    if (['POST', 'PUT', 'PATCH'].includes(method.toUpperCase())) {
        headers['X-CSRFToken'] = getCsrfToken();
    }

    try {
        const response = await fetch(`${API_BASE_URL}${endpoint}`, {
            method: method,
            headers: headers,
            body: JSON.stringify(data),
        });
        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(`HTTP error! Status: ${response.status} - ${JSON.stringify(errorData)}`);
        }
        const contentType = response.headers.get('content-type');
        if (contentType && contentType.includes('application/json')) {
            return await response.json();
        } else {
            return {}; // Return empty object for 204 No Content, etc.
        }
    } catch (error) {
        console.error('Error sending data:', error);
        showMessageBox(`Error saving data: ${error.message}`, true);
        throw error;
    }
}

/**
 * Deletes data from a given API endpoint.
 * Includes CSRF token for DELETE requests.
 * @param {string} endpoint - The API endpoint for deletion.
 * @returns {Promise<void>} - A promise that resolves when deletion is successful.
 */
async function deleteData(endpoint) {
    const headers = {};
    headers['X-CSRFToken'] = getCsrfToken(); // Add CSRF token for DELETE

    try {
        const response = await fetch(`${API_BASE_URL}${endpoint}`, {
            method: 'DELETE',
            headers: headers, // Include headers with CSRF token
        });
        if (!response.ok) {
            const errorText = await response.text();
            throw new Error(`HTTP error! Status: ${response.status} - ${errorText}`);
        }
        showMessageBox('Item deleted successfully!', false);
    } catch (error) {
        console.error('Error deleting data:', error);
        showMessageBox(`Error deleting item: ${error.message}`, true);
        throw error;
    }
}

// --- Tab Navigation ---

/**
 * Shows the selected section and hides others.
 * @param {string} sectionId - The ID of the section to show.
 */
function showSection(sectionId) {
    document.querySelectorAll('.form-section').forEach(section => {
        section.classList.remove('active');
    });
    document.getElementById(sectionId).classList.add('active');

    document.querySelectorAll('.tab-button').forEach(button => {
        button.classList.remove('active');
    });
    // event is a global object in browser, currentTarget refers to the element that the event listener is attached to
    event.currentTarget.classList.add('active');

    // Reload data when switching tabs
    if (sectionId === 'students') {
        loadStudents();
    } else if (sectionId === 'subjects') {
        loadSubjects();
    } else if (sectionId === 'grades') {
        loadGrades();
        populateStudentAndSubjectDropdowns(); // Ensure dropdowns are updated for grades
    }
}

// --- Confirmation Modal Logic ---
let deleteCallback = null;

/**
 * Opens the confirmation modal.
 * @param {Function} callback - The function to execute if confirmed.
 */
function openModal(callback) {
    deleteCallback = callback;
    document.getElementById('confirmationModal').style.display = 'flex';
}

/**
 * Closes the confirmation modal.
 */
function closeModal() {
    document.getElementById('confirmationModal').style.display = 'none';
    deleteCallback = null;
}

document.getElementById('confirmDeleteBtn').onclick = () => {
    if (deleteCallback) {
        deleteCallback();
        closeModal();
    }
};

// --- Student Management ---

/**
 * Loads and displays all students from the API.
 */
async function loadStudents() {
    const studentList = document.getElementById('studentList');
    studentList.innerHTML = `<tr><td colspan="6" class="text-center py-4 table-cell">Loading students...</td></tr>`;
    const students = await fetchData('/students/');
    studentList.innerHTML = ''; // Clear loading message

    if (students.length === 0) {
        studentList.innerHTML = `<tr><td colspan="6" class="text-center py-4 table-cell text-gray-500">No students found. Add one above!</td></tr>`;
        return;
    }

    students.forEach(student => {
        const row = `
            <tr class="table-row">
                <td class="table-cell font-semibold">${student.student_id}</td>
                <td class="table-cell">${student.full_name}</td>
                <td class="table-cell">${student.email}</td>
                <td class="table-cell">${student.date_of_birth || 'N/A'}</td>
                <td class="table-cell">${new Date(student.enrollment_date).toLocaleDateString()}</td>
                <td class="table-cell">
                    <button class="btn btn-secondary text-sm px-3 py-1 mr-2" onclick="editStudent(${student.id})">Edit</button>
                    <button class="btn btn-danger text-sm px-3 py-1" onclick="openModal(() => deleteStudent(${student.id}))">Delete</button>
                </td>
            </tr>
        `;
        studentList.insertAdjacentHTML('beforeend', row);
    });
}

/**
 * Handles student form submission (add/update).
 * @param {Event} event - The form submission event.
 */
document.getElementById('studentForm').addEventListener('submit', async (event) => {
    event.preventDefault();
    const studentId = document.getElementById('studentId').value;
    const studentData = {
        student_id: document.getElementById('student_id').value,
        first_name: document.getElementById('first_name').value,
        last_name: document.getElementById('last_name').value,
        email: document.getElementById('email').value,
        date_of_birth: document.getElementById('date_of_birth').value || null, // Send null if empty
    };

    try {
        if (studentId) {
            // Update existing student
            await sendData(`/students/${studentId}/`, 'PUT', studentData);
            showMessageBox('Student updated successfully!', false);
        } else {
            // Create new student
            await sendData('/students/', 'POST', studentData);
            showMessageBox('Student added successfully!', false);
        }
        clearStudentForm();
        loadStudents(); // Reload the list
    } catch (error) {
        // Error already handled by sendData function, just prevent further actions
    }
});

/**
 * Populates the student form for editing.
 * @param {number} id - The ID of the student to edit.
 */
async function editStudent(id) {
    const student = await fetchData(`/students/${id}/`);
    if (student) {
        document.getElementById('studentId').value = student.id;
        document.getElementById('student_id').value = student.student_id;
        document.getElementById('first_name').value = student.first_name;
        document.getElementById('last_name').value = student.last_name;
        document.getElementById('email').value = student.email;
        document.getElementById('date_of_birth').value = student.date_of_birth;
        showMessageBox(`Editing student: ${student.full_name}`);
    }
}

/**
 * Clears the student form.
 */
function clearStudentForm() {
    document.getElementById('studentId').value = '';
    document.getElementById('studentForm').reset();
    showMessageBox('Student form cleared.');
}

/**
 * Deletes a student.
 * @param {number} id - The ID of the student to delete.
 */
async function deleteStudent(id) {
    try {
        await deleteData(`/students/${id}/`);
        loadStudents(); // Reload the list
    } catch (error) {
        // Error already handled by deleteData function
    }
}

// --- Subject Management ---

/**
 * Loads and displays all subjects from the API.
 */
async function loadSubjects() {
    const subjectList = document.getElementById('subjectList');
    subjectList.innerHTML = `<tr><td colspan="4" class="text-center py-4 table-cell">Loading subjects...</td></tr>`;
    const subjects = await fetchData('/subjects/');
    subjectList.innerHTML = ''; // Clear loading message

    if (subjects.length === 0) {
        subjectList.innerHTML = `<tr><td colspan="4" class="text-center py-4 table-cell text-gray-500">No subjects found. Add one above!</td></tr>`;
        return;
    }

    subjects.forEach(subject => {
        const row = `
            <tr class="table-row">
                <td class="table-cell font-semibold">${subject.code}</td>
                <td class="table-cell">${subject.name}</td>
                <td class="table-cell">${subject.description || 'N/A'}</td>
                <td class="table-cell">
                    <button class="btn btn-secondary text-sm px-3 py-1 mr-2" onclick="editSubject(${subject.id})">Edit</button>
                    <button class="btn btn-danger text-sm px-3 py-1" onclick="openModal(() => deleteSubject(${subject.id}))">Delete</button>
                </td>
            </tr>
        `;
        subjectList.insertAdjacentHTML('beforeend', row);
    });
}

/**
 * Handles subject form submission (add/update).
 * @param {Event} event - The form submission event.
 */
document.getElementById('subjectForm').addEventListener('submit', async (event) => {
    event.preventDefault();
    const subjectId = document.getElementById('subjectId').value;
    const subjectData = {
        name: document.getElementById('subject_name').value,
        code: document.getElementById('subject_code').value,
        description: document.getElementById('subject_description').value,
    };

    try {
        if (subjectId) {
            await sendData(`/subjects/${subjectId}/`, 'PUT', subjectData);
            showMessageBox('Subject updated successfully!', false);
        } else {
            await sendData('/subjects/', 'POST', subjectData);
            showMessageBox('Subject added successfully!', false);
        }
        clearSubjectForm();
        loadSubjects();
    } catch (error) {
        // Error handled by sendData
    }
});

/**
 * Populates the subject form for editing.
 * @param {number} id - The ID of the subject to edit.
 */
async function editSubject(id) {
    const subject = await fetchData(`/subjects/${id}/`);
    if (subject) {
        document.getElementById('subjectId').value = subject.id;
        document.getElementById('subject_name').value = subject.name;
        document.getElementById('subject_code').value = subject.code;
        document.getElementById('subject_description').value = subject.description;
        showMessageBox(`Editing subject: ${subject.name}`);
    }
}

/**
 * Clears the subject form.
 */
function clearSubjectForm() {
    document.getElementById('subjectId').value = '';
    document.getElementById('subjectForm').reset();
    showMessageBox('Subject form cleared.');
}

/**
 * Deletes a subject.
 * @param {number} id - The ID of the subject to delete.
 */
async function deleteSubject(id) {
    try {
        await deleteData(`/subjects/${id}/`);
        loadSubjects();
    } catch (error) {
        // Error handled by deleteData
    }
}

// --- Grade Management ---

/**
 * Loads and displays all grades from the API.
 */
async function loadGrades() {
    const gradeList = document.getElementById('gradeList');
    gradeList.innerHTML = `<tr><td colspan="6" class="text-center py-4 table-cell">Loading grades...</td></tr>`;
    const grades = await fetchData('/grades/');
    gradeList.innerHTML = ''; // Clear loading message

    if (grades.length === 0) {
        gradeList.innerHTML = `<tr><td colspan="6" class="text-center py-4 table-cell text-gray-500">No grades found. Add one above!</td></tr>`;
        return;
    }

    grades.forEach(grade => {
        const row = `
            <tr class="table-row">
                <td class="table-cell">${grade.student.full_name || 'N/A'}</td>
                <td class="table-cell">${grade.subject.name || 'N/A'} (${grade.subject.code || 'N/A'})</td>
                <td class="table-cell">${grade.grade_type.charAt(0).toUpperCase() + grade.grade_type.slice(1)}</td>
                <td class="table-cell font-semibold">${grade.score}</td>
                <td class="table-cell">${new Date(grade.date_recorded).toLocaleDateString()}</td>
                <td class="table-cell">
                    <button class="btn btn-secondary text-sm px-3 py-1 mr-2" onclick="editGrade(${grade.id})">Edit</button>
                    <button class="btn btn-danger text-sm px-3 py-1" onclick="openModal(() => deleteGrade(${grade.id}))">Delete</button>
                </td>
            </tr>
        `;
        gradeList.insertAdjacentHTML('beforeend', row);
    });
}

/**
 * Populates the student and subject dropdowns in the grade form.
 */
async function populateStudentAndSubjectDropdowns() {
    const studentSelect = document.getElementById('grade_student');
    const subjectSelect = document.getElementById('grade_subject');

    // Clear previous options
    studentSelect.innerHTML = '<option value="">Select Student</option>';
    subjectSelect.innerHTML = '<option value="">Select Subject</option>';

    const students = await fetchData('/students/');
    students.forEach(student => {
        const option = document.createElement('option');
        option.value = student.id;
        option.textContent = student.full_name;
        studentSelect.appendChild(option);
    });

    const subjects = await fetchData('/subjects/');
    subjects.forEach(subject => {
        const option = document.createElement('option');
        option.value = subject.id;
        option.textContent = `${subject.name} (${subject.code})`;
        subjectSelect.appendChild(option);
    });
}

/**
 * Handles grade form submission (add/update).
 * @param {Event} event - The form submission event.
 */
document.getElementById('gradeForm').addEventListener('submit', async (event) => {
    event.preventDefault();
    const gradeId = document.getElementById('gradeId').value;
    const gradeData = {
        student_id: parseInt(document.getElementById('grade_student').value),
        subject_id: parseInt(document.getElementById('grade_subject').value),
        grade_type: document.getElementById('grade_type').value,
        score: parseFloat(document.getElementById('grade_score').value),
        notes: document.getElementById('grade_notes').value,
    };

    try {
        if (gradeId) {
            await sendData(`/grades/${gradeId}/`, 'PUT', gradeData);
            showMessageBox('Grade updated successfully!', false);
        } else {
            await sendData('/grades/', 'POST', gradeData);
            showMessageBox('Grade added successfully!', false);
        }
        clearGradeForm();
        loadGrades();
    } catch (error) {
        // Error handled by sendData
    }
});

/**
 * Populates the grade form for editing.
 * @param {number} id - The ID of the grade to edit.
 */
async function editGrade(id) {
    const grade = await fetchData(`/grades/${id}/`);
    if (grade) {
        document.getElementById('gradeId').value = grade.id;
        // Ensure dropdowns are populated BEFORE setting selected values
        await populateStudentAndSubjectDropdowns();
        document.getElementById('grade_student').value = grade.student.id;
        document.getElementById('grade_subject').value = grade.subject.id;
        document.getElementById('grade_type').value = grade.grade_type;
        document.getElementById('grade_score').value = grade.score;
        document.getElementById('grade_notes').value = grade.notes;
        showMessageBox(`Editing grade for ${grade.student.full_name} in ${grade.subject.name}`);
    }
}

/**
 * Clears the grade form.
 */
function clearGradeForm() {
    document.getElementById('gradeId').value = '';
    document.getElementById('gradeForm').reset();
    // Reset dropdowns to default option
    document.getElementById('grade_student').value = '';
    document.getElementById('grade_subject').value = '';
    document.getElementById('grade_type').value = '';
    showMessageBox('Grade form cleared.');
}

/**
 * Deletes a grade.
 * @param {number} id - The ID of the grade to delete.
 */
async function deleteGrade(id) {
    try {
        await deleteData(`/grades/${id}/`);
        loadGrades();
    } catch (error) {
        // Error handled by deleteData
    }
}

// --- Initial Load ---
// Load students and subjects when the page loads, and then hide the loading message for the first active tab.
window.onload = () => {
    loadStudents(); // Load initial data for the default active tab (Students)
    populateStudentAndSubjectDropdowns(); // Also load these for the Grades tab's dropdowns
};
