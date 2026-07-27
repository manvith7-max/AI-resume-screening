/* AI Resume Screening System - JavaScript Interactive Controls */

document.addEventListener("DOMContentLoaded", function () {
    initDragAndDrop();
    initTableFilters();
});

// Drag and Drop File Uploader
function initDragAndDrop() {
    const uploadZone = document.getElementById("uploadZone");
    const fileInput = document.getElementById("resumeFiles");
    const fileListContainer = document.getElementById("fileList");

    if (!uploadZone || !fileInput) return;

    uploadZone.addEventListener("click", () => fileInput.click());

    ["dragenter", "dragover"].forEach((eventName) => {
        uploadZone.addEventListener(eventName, (e) => {
            e.preventDefault();
            e.stopPropagation();
            uploadZone.classList.add("dragover");
        });
    });

    ["dragleave", "drop"].forEach((eventName) => {
        uploadZone.addEventListener(eventName, (e) => {
            e.preventDefault();
            e.stopPropagation();
            uploadZone.classList.remove("dragover");
        });
    });

    uploadZone.addEventListener("drop", (e) => {
        const dt = e.dataTransfer;
        const files = dt.files;
        fileInput.files = files;
        updateFileList(files, fileListContainer);
    });

    fileInput.addEventListener("change", (e) => {
        updateFileList(e.target.files, fileListContainer);
    });
}

function updateFileList(files, container) {
    if (!container) return;
    container.innerHTML = "";
    if (files.length === 0) return;

    const listGroup = document.createElement("div");
    listGroup.className = "mt-3 d-flex flex-column gap-2";

    Array.from(files).forEach((file) => {
        const item = document.createElement("div");
        item.className = "d-flex align-items-center justify-content-between p-2 rounded glass-card text-light small";
        
        const sizeMB = (file.size / (1024 * 1024)).toFixed(2);
        item.innerHTML = `
            <div>
                <i class="fas ${file.name.endsWith('.pdf') ? 'fa-file-pdf text-danger' : 'fa-file-word text-primary'} me-2 fs-5"></i>
                <strong>${file.name}</strong> (${sizeMB} MB)
            </div>
            <span class="badge bg-indigo text-light"><i class="fas fa-check me-1"></i>Ready</span>
        `;
        listGroup.appendChild(item);
    });

    container.appendChild(listGroup);
}

// Results Table Filtering
function initTableFilters() {
    const searchInput = document.getElementById("searchCandidate");
    const filterSelect = document.getElementById("filterStatus");
    const tableRows = document.querySelectorAll(".candidate-row");

    if (!tableRows.length) return;

    function filterTable() {
        const query = searchInput ? searchInput.value.toLowerCase().trim() : "";
        const statusFilter = filterSelect ? filterSelect.value : "ALL";

        tableRows.forEach((row) => {
            const name = row.getAttribute("data-name") || "";
            const email = row.getAttribute("data-email") || "";
            const status = row.getAttribute("data-status") || "";

            const matchesQuery = name.includes(query) || email.includes(query);
            const matchesStatus = statusFilter === "ALL" || status === statusFilter;

            if (matchesQuery && matchesStatus) {
                row.style.display = "";
            } else {
                row.style.display = "none";
            }
        });
    }

    if (searchInput) searchInput.addEventListener("input", filterTable);
    if (filterSelect) filterSelect.addEventListener("change", filterTable);
}

// Plotly Donut Chart helper for Dashboard
function renderDashboardDonutChart(containerId, donutData) {
    if (!document.getElementById(containerId) || !window.Plotly) return;

    const data = [{
        values: donutData.values,
        labels: donutData.labels,
        type: 'pie',
        hole: .6,
        marker: {
            colors: donutData.marker_colors
        },
        textinfo: "label+percent",
        textfont: { color: "#ffffff", size: 12 },
        hoverinfo: "label+value+percent"
    }];

    const layout = {
        paper_bgcolor: 'transparent',
        plot_bgcolor: 'transparent',
        showlegend: false,
        margin: { t: 10, b: 10, l: 10, r: 10 },
        height: 240
    };

    Plotly.newPlot(containerId, data, layout, { responsive: true, displayModeBar: false });
}

// Plotly Bar Chart helper for Candidate Breakdown
function renderCandidateBreakdownChart(containerId, chartData) {
    if (!document.getElementById(containerId) || !window.Plotly) return;

    const data = [{
        x: chartData.labels,
        y: chartData.values,
        type: 'bar',
        marker: {
            color: ['#6366f1', '#06b6d4', '#10b981']
        },
        text: chartData.values.map(v => v + "%"),
        textposition: 'auto',
        textfont: { color: '#ffffff', weight: 'bold' }
    }];

    const layout = {
        paper_bgcolor: 'transparent',
        plot_bgcolor: 'transparent',
        margin: { t: 20, b: 40, l: 40, r: 20 },
        yaxis: {
            range: [0, 105],
            gridcolor: 'rgba(255, 255, 255, 0.1)',
            tickfont: { color: '#94a3b8' }
        },
        xaxis: {
            tickfont: { color: '#94a3b8', size: 11 }
        },
        height: 260
    };

    Plotly.newPlot(containerId, data, layout, { responsive: true, displayModeBar: false });
}
