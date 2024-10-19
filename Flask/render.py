from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('html.html')


@app.route('/calculate_sjf_arrival', methods=['POST'])
def calculate_sjf_with_arrival():
    processes = request.json
    n = len(processes)

    # Sort processes by arrival time first
    processes.sort(key=lambda x: x['arrival'])

    current_time = 0
    completed = 0
    wt = [0] * n  # Waiting time for each process
    tat = [0] * n  # Turnaround time for each process
    is_completed = [False] * n  # To track completed processes
    total_wt = 0
    total_tat = 0
    execution_order = []

    # Repeat until all processes are completed
    while completed != n:
        # Find the process with the shortest burst time that has arrived and is not completed
        idx = -1
        min_burst_time = float('inf')
        for i in range(n):
            if (processes[i]['arrival'] <= current_time) and (not is_completed[i]):
                if processes[i]['bt'] < min_burst_time:
                    min_burst_time = processes[i]['bt']
                    idx = i

        if idx != -1:  # If a valid process is found
            # Process selected for execution
            execution_order.append(processes[idx]['pid'])
            current_time += processes[idx]['bt']  # Move time forward by burst time

            # Calculate waiting time and turnaround time
            wt[idx] = current_time - processes[idx]['arrival'] - processes[idx]['bt']
            tat[idx] = current_time - processes[idx]['arrival']

            total_wt += wt[idx]
            total_tat += tat[idx]
            is_completed[idx] = True
            completed += 1
        else:
            # No process is available at the current time, so move time forward to the next arriving process
            current_time = min([p['arrival'] for p in processes if not is_completed])

    avg_waiting_time = total_wt / n
    avg_turnaround_time = total_tat / n

    return jsonify({
        'executionOrder': execution_order,
        'avgWaitingTime': avg_waiting_time,
        'avgTurnAroundTime': avg_turnaround_time
    })


if __name__ == '__main__':
    app.run(debug=True)
