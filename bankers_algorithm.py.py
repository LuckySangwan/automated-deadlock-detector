import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt
import networkx as nx
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def calculate_need(maximum, allocation):
    need = []
    for i in range(len(maximum)):
        row = []
        for j in range(len(maximum[0])):
            row.append(maximum[i][j] - allocation[i][j])
        need.append(row)
    return need

def is_safe(available, allocation, need):
    work = available[:]
    finish = [False] * len(allocation)
    safe_sequence = []

    while True:
        allocated = False
        for i in range(len(allocation)):
            if not finish[i] and all(need[i][j] <= work[j] for j in range(len(work))):
                for j in range(len(work)):
                    work[j] += allocation[i][j]
                finish[i] = True
                safe_sequence.append(f'P{i}')
                allocated = True
        if not allocated:
            break

    if all(finish):
        return True, safe_sequence
    else:
        return False, []

def run_simulation():
    try:
        allocation = [[int(x) for x in row.split()] for row in alloc_text.get("1.0", "end-1c").splitlines()]
        maximum = [[int(x) for x in row.split()] for row in max_text.get("1.0", "end-1c").splitlines()]
        available = [int(x) for x in available_entry.get().split()]

        need = calculate_need(maximum, allocation)
        safe, sequence = is_safe(available, allocation, need)

        if safe:
            result_label.config(text="✅ Safe State!\nSafe Sequence: " + " → ".join(sequence), fg="green")
        else:
            result_label.config(text="❌ Deadlock Detected!\nNo Safe Sequence found.", fg="red")

        draw_edge_graph(allocation, need)
    except Exception as e:
        messagebox.showerror("Input Error", "Please enter valid numbers.\nEach row should have the same number of values as resources.")

def draw_edge_graph(allocation, need):
    G = nx.DiGraph()
    
    num_processes = len(allocation)
    num_resources = len(allocation[0])
    
    for i in range(num_processes):
        G.add_node(f'P{i}', color='lightblue')
    for j in range(num_resources):
        G.add_node(f'R{j}', color='lightcoral')
    
    for i in range(num_processes):
        for j in range(num_resources):
            if allocation[i][j] > 0:
                G.add_edge(f'R{j}', f'P{i}', weight=allocation[i][j])
            if need[i][j] > 0:
                G.add_edge(f'P{i}', f'R{j}', weight=need[i][j])
    
    fig, ax = plt.subplots(figsize=(6, 4))
    pos = nx.spring_layout(G)
    colors = [G.nodes[n]['color'] for n in G.nodes]
    nx.draw(G, pos, with_labels=True, node_color=colors, node_size=1000, edge_color='gray', ax=ax)
    
    for (u, v, d) in G.edges(data=True):
        ax.text((pos[u][0] + pos[v][0]) / 2, (pos[u][1] + pos[v][1]) / 2, str(d['weight']), color='black')
    
    for widget in chart_frame.winfo_children():
        widget.destroy()
    
    canvas = FigureCanvasTkAgg(fig, master=chart_frame)
    canvas.draw()
    canvas.get_tk_widget().pack()

root = tk.Tk()
root.title("Banker's Algorithm Simulator with Edge Graph")
root.geometry("800x800")
root.config(bg="#f9f9f9")

tk.Label(root, text="Banker's Algorithm Deadlock Detection Tool", font=("Arial", 16, "bold"), bg="#f9f9f9").pack(pady=10)

tk.Label(root, text="🧮 Allocation Matrix", font=("Arial", 12), bg="#f9f9f9").pack()
alloc_text = tk.Text(root, height=6, width=60)
alloc_text.insert("1.0", "0 1 0\n2 0 0\n3 0 2\n2 1 1\n0 0 2")
alloc_text.pack()

tk.Label(root, text="🎯 Maximum Matrix", font=("Arial", 12), bg="#f9f9f9").pack()
max_text = tk.Text(root, height=6, width=60)
max_text.insert("1.0", "7 5 3\n3 2 2\n9 0 2\n2 2 2\n4 3 3")
max_text.pack()

tk.Label(root, text="📦 Available Resources", font=("Arial", 12), bg="#f9f9f9").pack()
available_entry = tk.Entry(root, width=40)
available_entry.insert(0, "3 3 2")
available_entry.pack(pady=5)

tk.Button(root, text="🔍 Run Simulation", font=("Arial", 12, "bold"), bg="#4CAF50", fg="white", command=run_simulation).pack(pady=10)

result_label = tk.Label(root, text="", font=("Arial", 14), bg="#f9f9f9")
result_label.pack(pady=10)

chart_frame = tk.Frame(root, bg="#f9f9f9")
chart_frame.pack(pady=10)

tk.Label(root, text="✍ Modify matrix values and click Run Simulation again.", font=("Arial", 10), bg="#f9f9f9", fg="gray").pack(pady=5)

root.mainloop()
