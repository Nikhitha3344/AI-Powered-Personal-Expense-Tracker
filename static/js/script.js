

const form = document.getElementById("transactionForm");

form.addEventListener("submit", function(event) {
    event.preventDefault();

    const description = document.getElementById("description").value.trim();
    const amount = document.getElementById("amount").value;
    const category = document.getElementById("category").value;
    const type = document.getElementById("type").value;
    const date = document.getElementById("date").value;

    if (description === "" || amount === "" || Number(amount) <= 0 ||
        category === "" || type === "" || date === "") {
        alert("Please fill all fields correctly!");
        return;
    }
    const formData = new FormData(form);

fetch("/add", {
    method: "POST",
    body: formData
})
.then(response => response.text())
.then(data => {
    console.log(data);
});

    const table = document.getElementById("transactionList");
    const newRow = table.insertRow();

    newRow.innerHTML = `
    <td>${description}</td>
    <td>${category}</td>
    <td>${date}</td>
    <td>₹${Number(amount).toFixed(2)}</td>
    <td>${type}</td>
    <td>
        <button onclick="editTransaction(this)">Edit</button>
        <button onclick="deleteTransaction(this)">Delete</button>
    </td>
`;

    alert("Transaction added successfully!");

    form.reset();
});

function deleteTransaction(button) {
    const row = button.parentElement.parentElement;
    const transactionId = row.dataset.id;

    if (confirm("Are you sure you want to delete this transaction?")) {

        fetch(`/delete/${transactionId}`, {
            method: "POST"
        })
        .then(response => response.text())
        .then(data => {
            row.remove();
            alert(data);
        });
    }
}


function editTransaction(button) {
    const row = button.parentElement.parentElement;
    const transactionId = row.dataset.id;

    const description = prompt("Enter Description:", row.cells[0].innerText);
    if (description === null) return;

    const amount = prompt("Enter Amount:", row.cells[3].innerText.replace("₹", ""));
    if (amount === null) return;

    const category = prompt("Enter Category:", row.cells[1].innerText);
    if (category === null) return;

    const type = prompt("Enter Type (Income/Expense):", row.cells[4].innerText);
    if (type === null) return;

    const date = prompt("Enter Date (YYYY-MM-DD):", row.cells[2].innerText);
    if (date === null) return;

    if (description.trim() === "" || Number(amount) <= 0 ||
        category.trim() === "" ||
        !["Income", "Expense"].includes(type.trim()) ||
        date.trim() === "") {
        alert("Please enter valid details!");
        return;
    }

    const formData = new FormData();
    formData.append("description", description.trim());
    formData.append("amount", amount);
    formData.append("category", category.trim());
    formData.append("type", type.trim());
    formData.append("date", date.trim());

    fetch(`/update/${transactionId}`, {
        method: "POST",
        body: formData
    })
    .then(response => response.text())
    .then(data => {
        row.cells[0].innerText = description.trim();
        row.cells[1].innerText = category.trim();
        row.cells[2].innerText = date.trim();
        row.cells[3].innerText = "₹" + Number(amount).toFixed(2);
        row.cells[4].innerText = type.trim();

        alert(data);
    });
}


const searchInput = document.getElementById("searchInput");
const filterType = document.getElementById("filterType");

function applyFilters() {
    const searchValue = searchInput.value.toLowerCase();
    const selectedType = filterType.value;

    const table = document.getElementById("transactionList");
    const rows = table.getElementsByTagName("tr");

    for (let i = 0; i < rows.length; i++) {
        const description = rows[i].cells[0].innerText.toLowerCase();
        const category = rows[i].cells[1].innerText.toLowerCase();
        const type = rows[i].cells[4].innerText;

        const matchesSearch =
            description.includes(searchValue) ||
            category.includes(searchValue);

        const matchesType =
            selectedType === "All" || type === selectedType;

        rows[i].style.display =
            matchesSearch && matchesType ? "" : "none";
    }
}

searchInput.addEventListener("input", applyFilters);
filterType.addEventListener("change", applyFilters);

// Income vs Expenses Chart
const incomeExpenseCanvas = document.getElementById("incomeExpenseChart");

new Chart(incomeExpenseCanvas, {
    type: "bar",

    data: {
        labels: ["Income", "Expenses"],

        datasets: [{
            label: "Amount (₹)",
            data: [totalIncome, totalExpenses],
            backgroundColor: ["#22c55e", "#ef4444"],
            borderRadius: 8
        }]
    },

    options: {
        responsive: true,
        maintainAspectRatio: false
    }
});

// Category-wise Expenses Chart
const categoryExpenseCanvas = document.getElementById("categoryExpenseChart");

new Chart(categoryExpenseCanvas, {
    type: "pie",

    data: {
        labels: categoryLabels,

        datasets: [{
            label: "Expenses (₹)",
            data: categoryAmounts,
            backgroundColor: [
                "#3b82f6",
                "#f59e0b",
                "#22c55e",
                "#ef4444",
                "#a855f7"
            ]
        }]
    },

    options: {
        responsive: true,
        maintainAspectRatio: false
    }
});
function sendMessage() {
    const input = document.getElementById("chatInput");
    const message = input.value.trim();

    if (message === "") {
        alert("Please enter a question.");
        return;
    }

    const chatMessages = document.getElementById("chatMessages");

    // Display user's message
    const userMessage = document.createElement("p");
    userMessage.textContent = "You: " + message;
    chatMessages.appendChild(userMessage);

    input.value = "";

    // Send message to Flask
    fetch("/chat", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ message: message })
    })
    .then(response => response.json())
    .then(data => {
        const aiMessage = document.createElement("p");
        aiMessage.textContent = "AI: " + data.reply;
        chatMessages.appendChild(aiMessage);
    })
    .catch(error => {
        alert("Unable to get AI response. Please try again.");
        console.error(error);
    });
}