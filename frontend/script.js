let currentPage = 1;

function loadObservations() {

    fetch(`http://127.0.0.1:5000/observations?page=${currentPage}`)
        .then(response => response.json())
        .then(result => {

            const observations = result.data;
            const meta = result.meta;

            const container = document.getElementById("observationsContainer");
            container.innerHTML = "";

            observations.forEach(obs => {

                const div = document.createElement("div");

                div.innerHTML = `
                    <h2>${obs.title}</h2>
                    <h3>Category: ${obs.category}</h3>
                    <p>Date: ${obs.date}</p>
                    <p>Duration(minutes): ${obs.duration_minutes}</p>
                    <p>Notes: ${obs.notes}</p>
                    <h3>Created at: ${obs.created_at}</h3>

                    <button onclick="deleteObservation(${obs.id})">
                        🗑 Delete
                    </button>
                    <hr style="margin:20px 0;">
                `;

                container.appendChild(div);

            });

            document.getElementById("pageInfo").innerText =
                `Page ${meta.page} of ${meta.pages}`;

            const prevBtn = document.getElementById("prevBtn");
            const nextBtn = document.getElementById("nextBtn");

            prevBtn.disabled = !meta.has_prev;
            nextBtn.disabled = !meta.has_next;

        });

}

document.getElementById("loadBtn").addEventListener("click", function () {
    loadObservations();
});


document.getElementById("prevBtn").addEventListener("click", function () {
    if (currentPage > 1) {
        currentPage--;
        loadObservations();
    }
});

document.getElementById("nextBtn").addEventListener("click", function () {
    currentPage++;
    loadObservations();
});


document.getElementById("observationForm").addEventListener("submit", function(event){
    event.preventDefault();

    const title = document.getElementById("title").value
    const category = document.getElementById("category").value
    const date = document.getElementById("date").value
    const duration = parseInt(document.getElementById("duration").value) || 0
    const notes = document.getElementById("notes").value

    const observationData = {
        title: title,
        category: category,
        date: date,
        duration_minutes: duration,
        notes: notes
    };

    fetch("http://127.0.0.1:5000/observations", {
        method: "POST",

        headers: {
            "Content-type": "application/json"
        },

        body: JSON.stringify(observationData)
    })

    .then(response => response.json)
    .then(result => {
        alert("Observation added successfully!");
        document.getElementById("observationForm").reset();
        currentPage = 1;
        loadObservations();
    })

    .catch(error => {
        console.error("Error:", error);
    });
});

function deleteObservation(id) {

    if (!confirm("Are you sure you want to delete this observation?")) {
        return;
    }

    fetch(`http://127.0.0.1:5000/observations/${id}`, {
        method: "DELETE"
    })
    .then(response => response.json())
    .then(result => {
        console.log("Deleted:", result);
        loadObservations()
    })
    .catch(error => {
        console.error("Error deleting observation:", error);
    });
}

window.onload = function () {
    loadObservations();
};