let processes = [];

function addProcess() {
    const pid = document.getElementById('pid').value;
    const arrivalTime = document.getElementById('arrivalTime').value;
    const burstTime = document.getElementById('burstTime').value;

    if (pid && burstTime && arrivalTime) {
        processes.push({
            pid: parseInt(pid),
            arrival: parseInt(arrivalTime),
            bt: parseInt(burstTime),
        });

        displayProcesses();
        document.getElementById('processForm').reset();
    } else {
        alert('Please fill all fields.');
    }
}

function displayProcesses() {
    const tableBody = document.querySelector('#processTable tbody');
    tableBody.innerHTML = '';

    processes.forEach((process) => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${process.pid}</td>
            <td>${process.arrival}</td>
            <td>${process.bt}</td>
        `;
        tableBody.appendChild(row);
    });
}

async function submitProcesses() {
    try {
        const response = await fetch('/calculate_sjf_arrival', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(processes),
        });

        const result = await response.json();
        displayResults(result);
    } catch (error) {
        console.error('Error:', error);
    }
}

function displayResults(result) {
    const resultsDiv = document.getElementById('results');
    resultsDiv.innerHTML = `
        <p>Order of Execution: ${result.executionOrder.join(', ')}</p>
        <p>Average Waiting Time: ${result.avgWaitingTime.toFixed(2)}</p>
        <p>Average Turnaround Time: ${result.avgTurnAroundTime.toFixed(2)}</p>
    `;
}

