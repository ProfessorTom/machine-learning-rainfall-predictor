async function loadCSV(path) {
    const response = await fetch(path);
    if (!response.ok) {
        throw new Error(`Failed to load ${path}: ${response.status}`);
    }
    const text = await response.text();
    const lines = text.trim().split("\n");
    const headers = lines[0].split(",");
    const rows = lines.slice(1).map(line => {
        const values = line.split(",");
        let obj = {};
        headers.forEach((h, i) => obj[h.trim()] = values[i]?.trim());
        return obj;
    });
    return rows;
}

async function main() {
    console.log("new main from Tomas");
    const tbody = document.getElementById("forecast-table-body");
    tbody.innerHTML = "";

    try {
        // Path is relative to index.html
        const data = await loadCSV("data/centreville_forecast.csv");

        if (data.length === 0) {
            tbody.innerHTML = "<tr><td colspan='4'>No data found in CSV</td></tr>";
            return;
        }

        for (let row of data) {
            const tr = document.createElement("tr");
            // Handle both possible column names
            const rain = row.predicted_precipitation ?? row.predicted_rain ?? "N/A";
            tr.innerHTML = `
                <td>${row.date}</td>
                <td>${row.temp_max}</td>
                <td>${row.temp_min}</td>
                <td>${rain}</td>
            `;
            tbody.appendChild(tr);
        }
        console.log(`Loaded ${data.length} rows successfully`);
    } catch (error) {
        console.error(error);
        tbody.innerHTML = `<tr><td colspan="4">Error: ${error.message}. Check console (F12).</td></tr>`;
    }
}

main();
