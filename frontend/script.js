let currentPage = 1;

function formatTimestamp(timestamp) {

    const date = new Date(timestamp);

    const options = {
        year: "numeric",
        month: "short",
        day: "numeric"
    };

    const formattedDate = date.toLocaleDateString(undefined, options);

    const formattedTime = date.toLocaleTimeString([], {
        hour: "2-digit",
        minute: "2-digit"
    });

    return `${formattedDate} • ${formattedTime}`;
}

function loadObservations() {

    const category = document.getElementById("filterCategory").value;
    const date = document.getElementById("filterDate").value;
    const minDuration = document.getElementById("filterMinDuration").value;
    const maxDuration = document.getElementById("filterMaxDuration").value;

    let url = `/observations?page=${currentPage}`;

    if (category) {
        url += `&category=${category}`;
    }

    if (date) {
        url += `&date=${date}`;
    }

    if (minDuration) {
        url += `&min_duration=${minDuration}`;
    }

    if (maxDuration) {
        url += `&max_duration=${maxDuration}`;
    }

    fetch(url)
        .then(response => response.json())
        .then(result => {

            const observations = result.data || [];
            const meta = result.meta;

            const container = document.getElementById("observationsContainer");
            container.innerHTML = "";

            if (observations.length === 0) {
                container.innerHTML =
                    `<p class="no-results">No observations found for the selected filters.</p>`;
            }
            else {
                observations.forEach(obs => {

                    const div = document.createElement("div");
                    div.classList.add("observation-card");
                    const durationHTML = obs.duration_minutes && obs.duration_minutes > 0
                    ? `<p>Duration: ${obs.duration_minutes} minutes</p>`
                    : "";

                    div.innerHTML = `
                        <h2 class="obs-title">${obs.title}</h2>

                        <div class="obs-meta">
                            <p><strong>Category:</strong> ${obs.category}</p>
                            <p><strong>Date:</strong> ${obs.date}</p>
                            ${durationHTML}
                            <p><strong>Created:</strong> ${formatTimestamp(obs.created_at)}</p>
                        </div>

                        <div class="notes-block">
                            <strong>Notes</strong>
                            <p>${obs.notes || "No notes provided."}</p>
                        </div>

                        <button onclick="deleteObservation(${obs.id})">🗑 Delete</button>
                    `;

                    container.appendChild(div);

                });
            }

            const pageInfo = document.getElementById("pageInfo");
            if (meta.pages === 0) {
                pageInfo.innerText = "No pages available";
            } else {
                pageInfo.innerText = `Page ${meta.page} of ${meta.pages}`;
            }
            const prevBtn = document.getElementById("prevBtn");
            const nextBtn = document.getElementById("nextBtn");

            prevBtn.disabled = meta.pages === 0 || !meta.has_prev;
            nextBtn.disabled = meta.pages === 0 || !meta.has_next;

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

    fetch("/observations", {
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

    fetch(`/observations/${id}`, {
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

document.getElementById("applyFilters").addEventListener("click", function () {

    currentPage = 1;
    loadObservations();

});

document.getElementById("clearFilters").addEventListener("click", function () {

    document.getElementById("filterCategory").value = "";
    document.getElementById("filterDate").value = "";
    document.getElementById("filterMinDuration").value = "";
    document.getElementById("filterMaxDuration").value = "";

    currentPage = 1;
    loadObservations();

});

window.onload = function () {
    loadObservations();
};