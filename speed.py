# -*- coding: utf-8 -*-
import subprocess
import re
import json
import threading
import time
import os
from datetime import datetime
from flask import Flask, render_template_string, jsonify

# === CONFIGURAZIONE ===
CONFIG_PATH = "config.json"
HISTORY_PATH = "history.json"

with open(CONFIG_PATH) as f:
    CONFIG = json.load(f)

HISTORY_LIMIT = CONFIG.get("history_limit", 30)
INTERVAL = CONFIG.get("interval_seconds", 60)
PORT = CONFIG.get("web_port", 5050)

# === MEMORIA SPEEDTEST ===
speedtest_history = []

def load_history():
    global speedtest_history
    if os.path.exists(HISTORY_PATH):
        try:
            with open(HISTORY_PATH, "r") as f:
                speedtest_history = json.load(f)
        except Exception:
            speedtest_history = []

def save_history():
    with open(HISTORY_PATH, "w") as f:
        json.dump(speedtest_history, f, indent=2)

# === FLASK APP ===
app = Flask(__name__)

# === HTML TEMPLATE CON MODIFICHE ===
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Speedtest Dashboard</title>
  <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap" rel="stylesheet">
  <style>
    :root {
      --bg: #ffffff;
      --fg: #1a1a1a;
      --primary: #1e88e5;
      --secondary: #43a047;
      --accent: #fbc02d;
      --loss: #e53935;
      --border: #e0e0e0;
    }

    [data-theme="dark"] {
      --bg: #121212;
      --fg: #f0f0f0;
      --border: #333;
    }

    html, body {
      margin: 0;
      padding: 0;
      background-color: var(--bg);
      color: var(--fg);
      font-family: 'Inter', sans-serif;
      height: 100%;
    }

    .container {
      display: flex;
      flex-direction: column;
      height: 100vh;
      padding: 20px;
      box-sizing: border-box;
    }

    .top-bar {
      display: flex;
      flex-wrap: wrap;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 16px;
      border-bottom: 1px solid var(--border);
      padding-bottom: 10px;
      gap: 10px;
    }

    .metrics {
      display: flex;
      flex-wrap: wrap;
      gap: 10px;
      font-size: 14px;
    }

    .metrics div {
      background: var(--border);
      padding: 5px 10px;
      border-radius: 6px;
    }

    h2 {
      margin: 0;
      font-weight: 600;
    }

    .buttons {
      display: flex;
      gap: 10px;
    }

    button {
      padding: 8px 12px;
      background-color: var(--primary);
      color: #fff;
      border: none;
      border-radius: 6px;
      cursor: pointer;
      font-weight: 600;
      transition: background-color 0.3s ease;
    }

    button:hover {
      background-color: #1565c0;
    }

    canvas {
      flex: 1;
      max-height: calc(100vh - 140px);
    }

    @media (max-width: 600px) {
      .top-bar {
        flex-direction: column;
        align-items: flex-start;
      }

      canvas {
        max-height: 60vh;
      }
    }
  </style>
</head>
<body data-theme="light">
  <div class="container">
    <div class="top-bar">
      <h2>Speedtest Monitor</h2>
      <div class="buttons">
        <button onclick="toggleTheme()">🌓 Tema</button>
        <button onclick="togglePoints()">🎯 Punti</button>
      </div>
      <div class="metrics" id="metrics"></div>
    </div>
    <canvas id="speedChart"></canvas>
  </div>

  <script>
    const theme = localStorage.getItem('theme') || 'dark';
    document.body.setAttribute('data-theme', theme);
    let showPoints = false;

    function toggleTheme() {
      const current = document.body.getAttribute('data-theme');
      const next = current === 'dark' ? 'light' : 'dark';
      document.body.setAttribute('data-theme', next);
      localStorage.setItem('theme', next);
    }

    function togglePoints() {
      showPoints = !showPoints;
      update();
    }

    async function fetchData() {
      try {
        const res = await fetch('/data');
        return await res.json();
      } catch (e) {
        console.error("Errore nel fetch dati:", e);
        return [];
      }
    }

    function calculateStats(data, key) {
      const values = data.map(d => d[key]);
      const max = Math.max(...values).toFixed(2);
      const min = Math.min(...values).toFixed(2);
      const avg = (values.reduce((a, b) => a + b, 0) / values.length).toFixed(2);
      return `📈 ${key}: max ${max}, min ${min}, avg ${avg}`;
    }

    function updateMetrics(data) {
      const metricsDiv = document.getElementById('metrics');
      metricsDiv.innerHTML = [
        calculateStats(data, 'download'),
        calculateStats(data, 'upload'),
        calculateStats(data, 'latency'),
        calculateStats(data, 'packet_loss'),
      ].map(txt => `<div>${txt}</div>`).join('');
    }

    let chart;

    function createChart(data) {
      const ctx = document.getElementById('speedChart').getContext('2d');
      const labels = data.map(d => d.timestamp);

      const datasets = [
        {
          label: 'Download (Mbps)',
          data: data.map(d => d.download),
          borderColor: '#1e88e5',
          backgroundColor: 'rgba(30, 136, 229, 0.1)',
          borderWidth: 2,
          tension: 0.3,
          pointRadius: showPoints ? 4 : 0,
          yAxisID: 'y',
        },
        {
          label: 'Upload (Mbps)',
          data: data.map(d => d.upload),
          borderColor: '#43a047',
          backgroundColor: 'rgba(67, 160, 71, 0.1)',
          borderWidth: 2,
          tension: 0.3,
          pointRadius: showPoints ? 4 : 0,
          yAxisID: 'y',
        },
        {
          label: 'Latency (ms)',
          data: data.map(d => d.latency),
          borderColor: '#fbc02d',
          backgroundColor: 'rgba(251, 192, 45, 0.1)',
          borderWidth: 2,
          tension: 0.3,
          pointRadius: showPoints ? 4 : 0,
          yAxisID: 'latencyAxis',
        },
        {
          label: 'Packet Loss (%)',
          data: data.map(d => d.packet_loss),
          borderColor: '#e53935',
          backgroundColor: 'rgba(229, 57, 53, 0.1)',
          borderWidth: 2,
          tension: 0.3,
          pointRadius: showPoints ? 4 : 0,
          yAxisID: 'lossAxis',
        }
      ];

      if (chart) chart.destroy();

      chart = new Chart(ctx, {
        type: 'line',
        data: {
          labels,
          datasets
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          animation: false,
          plugins: {
            legend: {
              labels: {
                color: getComputedStyle(document.body).getPropertyValue('--fg')
              }
            }
          },
          scales: {
            x: {
              ticks: {
                color: getComputedStyle(document.body).getPropertyValue('--fg')
              },
              grid: {
                color: getComputedStyle(document.body).getPropertyValue('--border')
              }
            },
            y: {
              beginAtZero: true,
              ticks: {
                color: getComputedStyle(document.body).getPropertyValue('--fg')
              },
              grid: {
                color: getComputedStyle(document.body).getPropertyValue('--border')
              },
              title: {
                display: true,
                text: 'Mbps'
              }
            },
            latencyAxis: {
              position: 'right',
              beginAtZero: true,
              ticks: {
                color: getComputedStyle(document.body).getPropertyValue('--fg')
              },
              grid: {
                drawOnChartArea: false
              },
              title: {
                display: true,
                text: 'Latency (ms)'
              }
            },
            lossAxis: {
              position: 'right',
              beginAtZero: true,
              offset: true,
              ticks: {
                color: getComputedStyle(document.body).getPropertyValue('--fg')
              },
              grid: {
                drawOnChartArea: false
              },
              title: {
                display: true,
                text: 'Packet Loss (%)'
              }
            }
          }
        }
      });
    }

    async function update() {
      const data = await fetchData();
      updateMetrics(data);
      createChart(data);
    }

    update();
    setInterval(update, 60000);
  </script>
</body>
</html>
"""

# === FUNZIONE SPEEDTEST ===
def run_speedtest():
    try:
        result = subprocess.run(["speedtest"], capture_output=True, text=True, timeout=120)
        output = result.stdout

        data = {
            "timestamp": datetime.now().strftime("%H:%M:%S"),
            "latency": float(re.search(r"Idle Latency:\s+([\d.]+)", output).group(1)),
            "download": float(re.search(r"Download:\s+([\d.]+)", output).group(1)),
            "upload": float(re.search(r"Upload:\s+([\d.]+)", output).group(1)),
            "packet_loss": float(re.search(r"Packet Loss:\s+([\d.]+)", output).group(1)),
        }

        speedtest_history.append(data)
        if len(speedtest_history) > HISTORY_LIMIT:
            speedtest_history.pop(0)

        save_history()
        print(f"[{data['timestamp']}] ↓ {data['download']} Mbps ↑ {data['upload']} Mbps 🕒 {data['latency']} ms")

    except Exception as e:
        print("Errore nello speedtest:", e)

# === THREAD ESECUZIONE PERIODICA ===
def background_worker():
    while True:
        run_speedtest()
        time.sleep(INTERVAL)

# === ROUTES ===
@app.route("/")
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route("/data")
def data():
    return jsonify(speedtest_history)

# === AVVIO ===
if __name__ == "__main__":
    load_history()
    threading.Thread(target=background_worker, daemon=True).start()
    app.run(host="0.0.0.0", port=PORT)
