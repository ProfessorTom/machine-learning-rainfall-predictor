async function loadCSV(path) {
    const response = await fetch(path);
    const text = await response.text();
    const lines = text.trim().split("\n");
    const headers = lines[0].split(",");
    const rows = lines.slice(1).map(line => {
        const values = line.split(",");
        let obj = {};
        headers.forEach((h,i) => obj[h] = values[i]);
        return obj;
    });
    return rows;
}

async function main() {
    // Get the table body element
    const tbody = document.getElementById("forecast-table-body");

    // Clear it first
    tbody.innerHTML = "";

    // Example: loop through your data (replace this with your actual CSV or JSON data)
    const data = [
        { date: "2025-08-27", temp_max: 30, temp_min: 18, predicted_rain: 2 },
        { date: "2025-08-28", temp_max: 28, temp_min: 17, predicted_rain: 0 },
    ];

    for (let row of data) {
        const tr = document.createElement("tr");
        tr.innerHTML = `
            <td>${row.date}</td>
            <td>${row.temp_max}</td>
            <td>${row.temp_min}</td>
            <td>${row.predicted_rain}</td>
        `;
        tbody.appendChild(tr);
    }
}

// Run the main function
main();
