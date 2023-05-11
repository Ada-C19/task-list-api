const tasksContainer = document.getElementById("tasks-container");
const goalsContainer = document.getElementById("goals-container");
const confirmBtn = document.getElementById('confirm-btn')
const titleInput = document.getElementById("title");
const descriptionInput = document.getElementById("description");
const idInput = document.getElementById("item-id");
const typeInput = document.getElementById("item-type");
const goalsTab = document.getElementById("goals-tab");
const tasksTab = document.getElementById("tasks-tab");
const modal = document.getElementById("modal");
const goalDetails = document.getElementById("goal-details");
const modalTitle = document.getElementById("modal-title");
const modalSubtitle = document.getElementById("modal-subtitle");
const modalSVG = document.getElementById("modal-svg");
const titleGroup = document.getElementById("title-group");
const descriptionGroup = document.getElementById("description-group");
const tasksSelect = document.getElementById("tasks-select");
const selectDisclaimer = document.getElementById("select-disclaimer");
const baseURL = "https://liz-task-list-api.onrender.com/";
titleInput.addEventListener('input', checkForm);
descriptionInput.addEventListener('input', checkForm);

function checkForm() {
    if (titleInput.value && descriptionInput.value || typeInput.value === 'goal' && titleInput.value) {
    confirmBtn.disabled = false;
    confirmBtn.style.backgroundColor = "#16a34a";
    } else {
    confirmBtn.disabled = true;
    confirmBtn.style.backgroundColor = "#d3d3d3";

    }
}

function createItem() {
    url = baseURL + typeInput.value + "s";

    fetch(url, {
    method: "POST",
    headers: {
        "Content-Type": "application/json",
    },
    body: JSON.stringify({
        title: titleInput.value,
        description: descriptionInput.value,
    }),
    })
    .then((response) => response.json())
    .then((data) => {
        typeInput.value === "task" ? createTaskRow(data.task) : createGoalRow(data.goal);
    })
    .catch((error) => {
        console.error("Error:", error);
    });

    hideModal();
}

function getTasks() {
    fetch(`${baseURL}tasks`, {
    method: "GET",
    headers: {
        "Content-Type": "application/json",
    },
    })
    .then((response) => response.json())
    .then((data) => {
        data.forEach((task) => {
        createTaskRow(task)
        });
    }).then(() => {
        document.getElementById('task-loading').classList.add('hidden')
    })
    .catch((error) => {
        console.error("Error:", error);
        // Handle error here
    });
}

function getGoals() {
    fetch(`${baseURL}goals`, {
    method: "GET",
    headers: {
        "Content-Type": "application/json",
    },
    })
    .then((response) => response.json())
    .then((data) => {
        data.forEach((goal) => {
        createGoalRow(goal)
        });
    })
    .catch((error) => {
        console.error("Error:", error);
        // Handle error here
    });
}

function initialize() {
    getTasks();
    getGoals();
}

initialize();

function hideGoalDetails() {
    goalDetails.classList.add("hidden");
    goalDetails.getElementsByTagName('table')[0].innerHTML = ""
}


function createIconsTd(type, item, newRow, tableId) {
    // create and append the third table data element (icons)
    let hideGoalsModal = tableId != "tasks-table" ? true : false;

    const iconsTd = document.createElement("td");
    iconsTd.classList.add("items-center", "mr-6","w-7");
    editContainer = document.createElement("div");
    editContainer.classList.add("cursor-pointer", "mb-3");
    editContainer.innerHTML = `
    <svg viewBox="0 0 24 24"><path fill="currentColor" d="M16.84 2.73c-.39 0-.77.15-1.07.44l-2.12 2.12 5.3 5.31 2.12-2.1c.6-.61.6-1.56 0-2.14L17.9 3.17c-.3-.29-.68-.44-1.06-.44M12.94 6l-8.1 8.11 2.56.28.18 2.29 2.28.17.29 2.56 8.1-8.11m-14 3.74L2.5 21.73l6.7-1.79-.24-2.16-2.31-.17-.18-2.32"></path></svg>
    `
    editContainer.addEventListener("click", () => {
    showModal(`edit-${type}`, item, hideGoalsModal);
    });
    iconsTd.appendChild(editContainer);
    deleteContainer = document.createElement("div");
    deleteContainer.classList.add("cursor-pointer");
    deleteContainer.innerHTML = `
    <svg viewBox="0 0 24 24"><path fill="currentColor" d="M6 19c0 1.1.9 2 2 2h8c1.1 0 2-.9 2-2V7H6v12zm2.46-7.12 1.41-1.41L12 12.59l2.12-2.12 1.41 1.41L13.41 14l2.12 2.12-1.41 1.41L12 15.41l-2.12 2.12-1.41-1.41L10.59 14l-2.13-2.12zM15.5 4l-1-1h-5l-1 1H5v2h14V4z"></path></svg>`;
    iconsTd.appendChild(editContainer);
    iconsTd.appendChild(deleteContainer);
    deleteContainer.addEventListener("click", () => {
    showModal(`delete-${type}`, item, hideGoalsModal);
    });

    newRow.appendChild(iconsTd);
}

function createCheckboxTd(task, newRow) {
    const {id, is_complete} = task;
    const checkboxTd = document.createElement("td");
    checkboxTd.classList.add("p-4", "w-1/12");
    const checkbox = document.createElement("input");
    checkbox.setAttribute("type", "checkbox");
    checkbox.setAttribute("aria-label", "Mark Complete");
    checkboxTd.appendChild(checkbox);
    checkbox.checked = is_complete;
    if (is_complete) {
    newRow.classList.add("line-through");
    }
    checkbox.addEventListener("change", (event) => {
    let url = baseURL + "tasks/" + id;
    if (event.target.checked) {
        url = url + "/mark_complete";
        document.querySelectorAll(`.task${id}`).forEach((row) => {
        row.classList.add("line-through");
        });

    } else {
        url = url + "/mark_incomplete";
        document.querySelectorAll(`.task${id}`).forEach((row) => {
        row.classList.remove("line-through");
        });
    }
    fetch(url, {
        method: "PATCH",
        headers: {
        "Content-Type": "application/json",
        },
    })
    });
    newRow.appendChild(checkboxTd);
}

function createTaskRow(task, tableId = "tasks-table") {
    const { title, description, id } = task;
    // get reference to the table
    const table = document.getElementById(tableId);

    // create a new table row element
    const newRow = document.createElement("tr");
    newRow.classList.add("border-b", "border-neutral-300", `task${id}`);
    createCheckboxTd(task, newRow);

    // create and append the second table data element (title and description)
    const titleDescriptionTd = document.createElement("td");
    titleDescriptionTd.innerHTML = `
    <span id="title-task${id}" class="block text-lg font-semibold">${title}</span>
    <span id="description-task${id}" class="text-lg text-neutral-400">${description}</span>
    `;
    newRow.appendChild(titleDescriptionTd);

    iconsTd = createIconsTd("task", task, newRow, tableId);

    const spacingTd = document.createElement("td");
    spacingTd.classList.add("w-2");
    newRow.appendChild(spacingTd);
    table.appendChild(newRow);

}

function createGoalRow(goal, tableId = "goals-table") {
    const { title, id } = goal;
    // get reference to the table
    const table = document.getElementById(tableId);

    // create a new table row element
    const newRow = document.createElement("tr");
    newRow.classList.add("border-b", "border-neutral-300", `goal${id}`);

    // create and append the second table data element (title and description)
    const titleTd = document.createElement("td");
    titleTd.innerHTML = `
    <span id="title-goal${id}" class="block text-lg font-semibold ml-8">${title}</span>
    `;
    const button = document.createElement("button");
    button.setAttribute("id", `viewTasks${id}`);
    button.className = "text-lg text-neutral-400 ml-8";
    button.innerText = "View Tasks";
    button.addEventListener("click", () => {
    goalDetails.classList.remove('hidden');
    document.getElementById('goal-modal-title').innerText = title + ' - Tasks';
    fetch(`${baseURL}goals/${id}/tasks`)
        .then((response) => response.json())
        .then((data) => {
        const tasks = data.tasks;
        if (tasks.length > 0) {
            tasks.forEach((task) => {
            createTaskRow(task, "goal-modal-table");
            document.getElementById('no-tasks-found').classList.add('hidden');
        });
        } else {
            document.getElementById('no-tasks-found').classList.remove('hidden');
        }
        document.getElementById('goal-detail-loading').classList.add('hidden');
        });

    });
    titleTd.appendChild(button);
    newRow.appendChild(titleTd);
    iconsTd = createIconsTd("goal", goal, newRow, tableId);

    const spacingTd = document.createElement("td");
    spacingTd.classList.add("w-2");
    newRow.appendChild(spacingTd);
    table.appendChild(newRow);
}

function deleteItem() {
    let itemType = typeInput.value;
    const id = document.getElementById('item-id').value;
    const rows = Array.from(document.getElementsByClassName(`${itemType}${id}`));
    fetch(`${baseURL + itemType}s/${id}`, {
    method: "DELETE",
    headers: {
        "Content-Type": "application/json",
    },
    })
    rows.forEach((row) => {
    row.remove();
    });
    hideModal();
}

function editItem () {
    const id = idInput.value;
    const title = titleInput.value;
    const description = descriptionInput.value;
    const itemType = typeInput.value;
    const row = document.getElementById(`${itemType+id}`);
    const titleSpan = document.getElementById(`title-${itemType+id}`);
    const descriptionSpan = document.getElementById(`description-${itemType+id}`);
    let url = baseURL + itemType + "s/" + id;
    let method = "PUT";
    titleSpan.innerText = title;
    let task_ids = [];

    if (itemType === 'task') {
    descriptionSpan.innerText = description;
    } else {
    const options = Array.from(tasksSelect.selectedOptions);
    method = "POST";
    url = url + "/tasks" + "?title=" + title;
    options.forEach((option) => {
        task_ids.push(parseInt(option.value));
    });
    }
    hideModal();
    fetch(url, {
    method: method,
    headers: {
        "Content-Type": "application/json",
    },
    body: JSON.stringify({
        title,
        description,
        task_ids
    }),
    })
    .then((response) => response.json())
    .then((data) => {
        console.log(data);
        hideModal();
    })
    .catch((error) => {
        console.error("Error:", error);
        // Handle error here
    });
}

function loadTasksforGoal(id) {
    fetch(`${baseURL}tasks`)
    .then((response) => response.json())
    .then((data) => {
        data.forEach((task) => {
        if (task.goal_id === id) {
            tasksSelect.innerHTML += `
            <option value="${task.id}" selected>${task.title}</option>
            `;
        } else if (!task.goal_id){
            tasksSelect.innerHTML += `
            <option value="${task.id}">${task.title}</option>
        `;
        }
        });
        document.getElementById('goal-detail-loading').classList.add('hidden');
        if (tasksSelect.options.length === 0) {
        tasksSelect.classList.add('hidden');
        selectDisclaimer.classList.add('hidden');
        }
    });
}
function showModal(type, item, hideGoalModal = false) {
    hideGoalModal ? goalDetails.classList.add('hidden') : null;

    [action, itemType ] = type.split("-")
    idInput.value = item?.id || "";
    titleInput.value = item?.title || "";
    descriptionInput.value = item?.description || "";
    typeInput.value = itemType;

    if (action != 'delete') {
    checkForm();
    modalTitle.innerText = `${action} ${itemType} Details`;
    modalTitle.style.textTransform = 'capitalize'
    modalSubtitle.innerText = "Please fill in the form below.";
    titleGroup.classList.remove("hidden");
    itemType === 'task' ? descriptionGroup.classList.remove("hidden") : null;
    confirmBtn.onclick = action === 'edit' ? editItem : createItem;
    if (action === 'edit') {
        if (itemType === 'goal') {
        loadTasksforGoal(item.id);
        tasksSelect.classList.remove('hidden');
        selectDisclaimer.classList.remove('hidden');
        }
    }
    } else {
    confirmBtn.style.backgroundColor = '#dc2626'
    modalTitle.innerText = `Are you sure to remove this ${itemType}?`;
    modalTitle.style.textTransform = 'none'
    modalSubtitle.innerText = "This action cannot be undone.";
    confirmBtn.onclick = deleteItem;
    }
    if (itemType === 'task' && action != 'delete') {
    modalSVG.innerHTML = `<path fill="currentColor" d="M17.75 2.001a2.25 2.25 0 0 1 2.245 2.096L20 4.25v10.128c-.12.08-.235.174-.341.28l-3.409 3.408l-.908-.91a2.242 2.242 0 0 0-1.5-.657h2.408a.75.75 0 1 0 0-1.5h-5.004a.75.75 0 0 0 0 1.5h2.413a2.25 2.25 0 0 0-1.5 3.838L13.817 22H6.25a2.25 2.25 0 0 1-2.245-2.096L4 19.75V4.251a2.25 2.25 0 0 1 2.096-2.245l.154-.005h11.5ZM9 7.751a1 1 0 1 0-2 0a1 1 0 0 0 2 0ZM11.246 7a.75.75 0 0 0 0 1.5h5.004a.75.75 0 1 0 0-1.5h-5.004Zm-.75 4.75c0 .414.336.75.75.75h5.004a.75.75 0 1 0 0-1.5h-5.004a.75.75 0 0 0-.75.75ZM9 11.75a1 1 0 1 0-2 0a1 1 0 0 0 2 0Zm0 3.998a1 1 0 1 0-2 0a1 1 0 0 0 2 0Zm7.25 4.441l4.47-4.47a.75.75 0 1 1 1.06 1.061l-5 5a.75.75 0 0 1-1.06 0l-2.5-2.501a.75.75 0 0 1 1.06-1.06l1.97 1.97Z"/>`;
    } else if (itemType === 'goal'&& action != 'delete') {
    modalSVG.innerHTML = `<path fill="currentColor" d="M12 2A10 10 0 0 0 2 12a10 10 0 0 0 10 10a10 10 0 0 0 10-10c0-1.16-.21-2.31-.61-3.39l-1.6 1.6c.14.59.21 1.19.21 1.79a8 8 0 0 1-8 8a8 8 0 0 1-8-8a8 8 0 0 1 8-8c.6 0 1.2.07 1.79.21L15.4 2.6C14.31 2.21 13.16 2 12 2m7 0l-4 4v1.5l-2.55 2.55C12.3 10 12.15 10 12 10a2 2 0 0 0-2 2a2 2 0 0 0 2 2a2 2 0 0 0 2-2c0-.15 0-.3-.05-.45L16.5 9H18l4-4h-3V2m-7 4a6 6 0 0 0-6 6a6 6 0 0 0 6 6a6 6 0 0 0 6-6h-2a4 4 0 0 1-4 4a4 4 0 0 1-4-4a4 4 0 0 1 4-4V6Z"/>`;
    } else if (action === 'delete') {
    modalSVG.innerHTML = `<path fill="currentColor" d="M6 19c0 1.1.9 2 2 2h8c1.1 0 2-.9 2-2V7H6v12zm2.46-7.12 1.41-1.41L12 12.59l2.12-2.12 1.41 1.41L13.41 14l2.12 2.12-1.41 1.41L12 15.41l-2.12 2.12-1.41-1.41L10.59 14l-2.13-2.12zM15.5 4l-1-1h-5l-1 1H5v2h14V4z"></path>`;
    }
    document.getElementById("modal").classList.remove("hidden");
}

function hideModal() {
    modal.classList.add("hidden");
    titleGroup.classList.add("hidden");
    descriptionGroup.classList.add("hidden");
    tasksSelect.classList.add("hidden");
    tasksSelect.innerHTML = '';
    selectDisclaimer.classList.add('hidden');
}

function tasksActive () {
    goalsTab.classList.remove('active');
    tasksTab.classList.add('active');
    tasksContainer.classList.remove('hidden');
    goalsContainer.classList.add('hidden');
}

function goalsActive () {
    goalsTab.classList.add('active');
    tasksTab.classList.remove('active');
    tasksContainer.classList.add('hidden');
    goalsContainer.classList.remove('hidden');
}

goalsTab.addEventListener("click", goalsActive);
tasksTab.addEventListener("click", tasksActive);