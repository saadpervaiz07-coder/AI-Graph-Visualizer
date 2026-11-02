
import streamlit as st
import random
import heapq
import time
import graphviz

# ==================== PAGE CONFIGURATION ====================

st.set_page_config(
    page_title="Graph Traversal & Search Engine",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================== DARK LICORICE THEME ====================

st.markdown("""
<style>

/* Main Application */
.stApp {
    background: #100C16;
    color: #F1EAF8;
    font-family: 'Inter', sans-serif;
}

/* Main Content */
.main .block-container {
    padding: 2rem 2.5rem;
    max-width: 1600px;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: #17111F;
    border-right: 1px solid #352442;
}

[data-testid="stSidebar"] * {
    color: #E9DDF3;
}

/* Main Title */
.main-title {
    font-size: 2.5rem;
    font-weight: 800;
    letter-spacing: -1px;
    color: #E5C9FF;
    margin-bottom: 0.3rem;
}

.sub-text {
    color: #A99BB8;
    font-size: 1rem;
    margin-bottom: 2rem;
}

/* Section Headings */
h1, h2, h3 {
    color: #E5D4F5 !important;
    font-weight: 700 !important;
}

/* General Text */
p, label, span {
    color: #D7C9E3;
}

/* Cards and Containers */
[data-testid="stVerticalBlockBorderWrapper"] {
    background: #1B1425;
    border: 1px solid #382748;
    border-radius: 14px;
}

/* Metrics */
[data-testid="stMetric"] {
    background: #21172E;
    border: 1px solid #49305F;
    padding: 17px;
    border-radius: 12px;
}

[data-testid="stMetricLabel"] {
    color: #BCA9CE !important;
}

[data-testid="stMetricValue"] {
    color: #D9B8FF !important;
}

/* Buttons */
.stButton > button {
    background: linear-gradient(135deg, #7141A0, #542B7B);
    color: white !important;
    border: 1px solid #9868C5;
    border-radius: 10px;
    font-weight: 650;
    min-height: 43px;
    transition: all 0.2s ease;
}

.stButton > button:hover {
    background: linear-gradient(135deg, #905CC2, #7141A0);
    border-color: #C59BEA;
    color: white !important;
    transform: translateY(-2px);
}

/* Input Fields */
.stTextInput input,
.stNumberInput input {
    background: #241A30 !important;
    color: #F1EAF8 !important;
    border: 1px solid #49345D !important;
    border-radius: 8px;
}

/* Select Boxes */
[data-baseweb="select"] > div {
    background: #241A30 !important;
    border-color: #49345D !important;
    border-radius: 8px;
}

[data-baseweb="select"] * {
    color: #E9DDF3 !important;
}

/* Slider */
.stSlider [data-baseweb="slider"] div[role="slider"] {
    background: #C18BEE;
}

/* Expanders */
[data-testid="stExpander"] {
    background: #1D1628;
    border: 1px solid #49345D;
    border-radius: 10px;
}

/* Tabs */
.stTabs [data-baseweb="tab-list"] {
    gap: 10px;
    background: #1B1425;
}

.stTabs [data-baseweb="tab"] {
    color: #C6B5D6;
}

.stTabs [aria-selected="true"] {
    color: #DDBBFF !important;
    border-bottom-color: #B77AE8 !important;
}

/* Alerts */
[data-testid="stAlert"] {
    border-radius: 10px;
}

/* Divider */
hr {
    border-color: #382748 !important;
}

/* Graph Area */
[data-testid="stGraphVizChart"] {
    background: #1B1425;
    border: 1px solid #382748;
    border-radius: 14px;
    padding: 12px;
}

/* Sidebar Headers */
[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 {
    color: #DDBBFF !important;
}

/* Custom Header */
.section-label {
    color: #B88BE0;
    font-size: 0.78rem;
    font-weight: 700;
    letter-spacing: 2px;
    text-transform: uppercase;
    margin-bottom: 8px;
}

.footer-text {
    color: #756782;
    font-size: 0.8rem;
    text-align: center;
    padding-top: 25px;
}

/* Scrollbar */
::-webkit-scrollbar {
    width: 8px;
}

::-webkit-scrollbar-track {
    background: #100C16;
}

::-webkit-scrollbar-thumb {
    background: #59406D;
    border-radius: 10px;
}

</style>
""", unsafe_allow_html=True)


# ==================== DEFAULT GRAPH ====================

INITIAL_GRAPH = {
    'A': [('B', 2), ('C', 5)],
    'B': [('A', 2), ('D', 4), ('E', 1)],
    'C': [('A', 5), ('F', 3)],
    'D': [('B', 4), ('G', 6)],
    'E': [('B', 1), ('G', 2)],
    'F': [('C', 3), ('G', 4)],
    'G': []
}

if 'graph_data' not in st.session_state:
    st.session_state.graph_data = INITIAL_GRAPH


# ==================== ALGORITHMS ====================

def run_pure_random(graph, start, goal, max_steps):
    curr = start
    path = [curr]
    total_cost = 0
    logs = [f"🟢 Traversal initialized at **{start}**"]

    for step in range(1, max_steps + 1):
        if curr == goal:
            return True, path, total_cost, logs, step

        neighbors = graph.get(curr, [])
        if not neighbors:
            logs.append(f"❌ Step {step}: Dead-end at node **{curr}**.")
            return False, path, total_cost, logs, step

        next_node, weight = random.choice(neighbors)
        total_cost += weight
        path.append(next_node)
        logs.append(f"Step {step}: Traversed **{curr}** ➔ **{next_node}** | Edge Weight: {weight}")
        curr = next_node

    logs.append(f"⚠️ Reached step limit ({max_steps}).")
    return False, path, total_cost, logs, max_steps


def run_random_closed_set(graph, start, goal, max_steps):
    curr = start
    visited = {curr}
    path = [curr]
    total_cost = 0
    logs = [f"🟢 Traversal initialized at **{start}**"]

    for step in range(1, max_steps + 1):
        if curr == goal:
            return True, path, total_cost, logs, len(visited)

        unvisited = [n for n in graph.get(curr, []) if n[0] not in visited]
        if not unvisited:
            logs.append(f"❌ Step {step}: No unvisited neighbors from **{curr}**.")
            return False, path, total_cost, logs, len(visited)

        next_node, weight = random.choice(unvisited)
        visited.add(next_node)
        total_cost += weight
        path.append(next_node)
        logs.append(f"Step {step}: Moved to **{next_node}** (Weight: {weight}) | Explored Set: {sorted(list(visited))}")
        curr = next_node

    return False, path, total_cost, logs, len(visited)


def run_random_frontier(graph, start, goal, max_steps):
    frontier = [(0, [start])]
    logs = [f"🟢 Frontier initialized with **{start}**"]
    steps = 0

    while frontier and steps < max_steps:
        steps += 1
        idx = random.randint(0, len(frontier) - 1)
        cost, path = frontier.pop(idx)
        curr = path[-1]

        logs.append(f"Step {steps}: Sampled path **{' → '.join(path)}** (Accumulated Cost: {cost})")
        if curr == goal:
            return True, path, cost, logs, steps

        for nxt, weight in graph.get(curr, []):
            if nxt not in path:
                frontier.append((cost + weight, path + [nxt]))

    return False, [], 0, logs, steps


def run_ucs(graph, start, goal):
    pq = [(0, [start])]
    visited = set()
    logs = [f"🟢 Priority Queue initialized with **{start}**"]
    expanded_count = 0

    while pq:
        cost, path = heapq.heappop(pq)
        curr = path[-1]
        expanded_count += 1

        logs.append(f"Dequeued path **{' → '.join(path)}** (Cost: **{cost}**)")
        if curr == goal:
            return True, path, cost, logs, expanded_count

        if curr not in visited:
            visited.add(curr)
            for nxt, weight in graph.get(curr, []):
                if nxt not in visited:
                    heapq.heappush(pq, (cost + weight, path + [nxt]))
                    logs.append(f"   └── Added candidate node **{nxt}** | Total Path Cost: {cost + weight}")

    logs.append("❌ Frontier exhausted. Goal node unreachable.")
    return False, [], 0, logs, expanded_count


# ==================== GRAPH VISUALIZATION ====================

def render_graph_viz(graph, path=None):
    dot = graphviz.Digraph(engine='dot')

    dot.attr(
        rankdir='LR',
        bgcolor='#1B1425',
        pad='0.35',
        nodesep='0.65',
        ranksep='0.85',
        splines='true'
    )

    dot.attr(
        'node',
        fontname='Arial',
        fontsize='13',
        shape='circle',
        style='filled',
        color='#76528E',
        penwidth='1.8'
    )

    dot.attr(
        'edge',
        fontname='Arial',
        fontsize='11',
        fontcolor='#D0BCE3',
        color='#705A83',
        penwidth='1.5'
    )

    path_edges = set()

    if path:
        for i in range(len(path) - 1):
            path_edges.add((path[i], path[i+1]))

    all_nodes = set(graph.keys())

    for nbrs in graph.values():
        for n, _ in nbrs:
            all_nodes.add(n)

    for node in sorted(all_nodes):
        if path and node in path:
            dot.node(
                node,
                node,
                fillcolor='#8855B5',
                fontcolor='white',
                color='#D5A7FF',
                penwidth='2.5'
            )
        else:
            dot.node(
                node,
                node,
                fillcolor='#30213F',
                fontcolor='#E8D9F5',
                color='#74528C'
            )

    for src, neighbors in graph.items():
        for dst, weight in neighbors:

            if (src, dst) in path_edges:
                dot.edge(
                    src,
                    dst,
                    label=str(weight),
                    color='#D49AFF',
                    fontcolor='#E8C9FF',
                    penwidth='3'
                )
            else:
                dot.edge(
                    src,
                    dst,
                    label=str(weight),
                    color='#705A83'
                )

    return dot


# ==================== MAIN UI ====================

st.markdown(
    '<div class="main-title">⚡ AI Graph Search Visualizer</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="sub-text">Interactive environment for analyzing randomized and uninformed graph exploration algorithms.</div>',
    unsafe_allow_html=True
)

st.divider()


# ==================== SIDEBAR CONTROLS ====================

st.sidebar.markdown("## ⚙️ Execution Settings")

st.sidebar.caption("Configure your graph search algorithm.")

algo_choice = st.sidebar.selectbox(
    "Algorithm Variant",
    [
        "Uniform Cost Search (Optimal)",
        "Random Search (Closed List)",
        "Random Search (Frontier Bag)",
        "Pure Random Walk"
    ]
)

all_nodes = sorted(
    list(
        set(st.session_state.graph_data.keys()).union(
            {
                nbr
                for sub in st.session_state.graph_data.values()
                for nbr, _ in sub
            }
        )
    )
)

start_sel = st.sidebar.selectbox(
    "Start Node",
    all_nodes,
    index=0
)

goal_sel = st.sidebar.selectbox(
    "Goal Node",
    all_nodes,
    index=len(all_nodes) - 1 if all_nodes else 0
)

step_cap = st.sidebar.slider(
    "Step Threshold (Randomized)",
    10,
    1000,
    300
)

st.sidebar.divider()

st.sidebar.markdown("## 🛠️ Graph Modifier")

with st.sidebar.expander("➕ Add Custom Edge"):

    c1, c2 = st.columns(2)

    u_node = c1.text_input(
        "From Node",
        "A"
    ).upper().strip()

    v_node = c2.text_input(
        "To Node",
        "G"
    ).upper().strip()

    e_weight = st.number_input(
        "Weight",
        min_value=1,
        value=3
    )

    if st.button("Add Edge", use_container_width=True):

        if u_node and v_node:

            if u_node not in st.session_state.graph_data:
                st.session_state.graph_data[u_node] = []

            st.session_state.graph_data[u_node].append(
                (v_node, e_weight)
            )

            st.rerun()


if st.sidebar.button(
    "↻ Reset Graph Defaults",
    use_container_width=True
):
    st.session_state.graph_data = INITIAL_GRAPH
    st.rerun()


st.sidebar.divider()

st.sidebar.markdown(
    '<div class="footer-text">AI GRAPH SEARCH ENGINE<br>Dark Licorice Edition</div>',
    unsafe_allow_html=True
)


# ==================== MAIN LAYOUT ====================

col_graph, col_controls = st.columns(
    [1.2, 1],
    gap="large"
)


# ==================== GRAPH TOPOLOGY ====================

with col_graph:

    st.markdown(
        '<div class="section-label">01 / GRAPH STRUCTURE</div>',
        unsafe_allow_html=True
    )

    st.subheader("📌 Visual Topology")

    st.caption(
        "Explore the nodes and weighted connections in your graph."
    )

    st.graphviz_chart(
        render_graph_viz(st.session_state.graph_data),
        use_container_width=True
    )


# ==================== EXECUTION ENGINE ====================

with col_controls:

    st.markdown(
        '<div class="section-label">02 / SEARCH OPERATIONS</div>',
        unsafe_allow_html=True
    )

    st.subheader("🚀 Execution Engine")

    st.caption(
        "Select your algorithm and execute the traversal."
    )

    if st.button(
        "⚡ Run Traversal",
        type="primary",
        use_container_width=True
    ):

        t0 = time.perf_counter()

        if algo_choice == "Uniform Cost Search (Optimal)":

            found, final_path, cost, execution_logs, expanded = run_ucs(
                st.session_state.graph_data,
                start_sel,
                goal_sel
            )

        elif algo_choice == "Random Search (Closed List)":

            found, final_path, cost, execution_logs, expanded = run_random_closed_set(
                st.session_state.graph_data,
                start_sel,
                goal_sel,
                step_cap
            )

        elif algo_choice == "Random Search (Frontier Bag)":

            found, final_path, cost, execution_logs, expanded = run_random_frontier(
                st.session_state.graph_data,
                start_sel,
                goal_sel,
                step_cap
            )

        else:

            found, final_path, cost, execution_logs, expanded = run_pure_random(
                st.session_state.graph_data,
                start_sel,
                goal_sel,
                step_cap
            )

        t1 = time.perf_counter()

        elapsed_ms = (t1 - t0) * 1000

        st.divider()

        st.markdown(
            '<div class="section-label">03 / EXECUTION RESULTS</div>',
            unsafe_allow_html=True
        )

        m1, m2, m3 = st.columns(3)

        if found:

            m1.metric(
                "Status",
                "Goal Found",
                delta="Success"
            )

            m2.metric(
                "Path Cost",
                cost
            )

            m3.metric(
                "Latency",
                f"{elapsed_ms:.2f} ms"
            )

            st.success(
                f"**Optimal Route:** {' ➔ '.join(final_path)}"
            )

            st.graphviz_chart(
                render_graph_viz(
                    st.session_state.graph_data,
                    final_path
                ),
                use_container_width=True
            )

        else:

            m1.metric(
                "Status",
                "Failed"
            )

            m2.metric(
                "Path Cost",
                "N/A"
            )

            m3.metric(
                "Latency",
                f"{elapsed_ms:.2f} ms"
            )

            st.error(
                "No path could be established to the goal node."
            )

        st.divider()

        st.markdown(
            '<div class="section-label">04 / EXECUTION HISTORY</div>',
            unsafe_allow_html=True
        )

        st.subheader("📜 Step Logs")

        with st.expander(
            "Expand Step-by-Step Logs",
            expanded=True
        ):

            for entry in execution_logs:
                st.write(entry)


# ==================== FOOTER ====================

st.markdown(
    '<div class="footer-text">AI GRAPH SEARCH VISUALIZER &nbsp; • &nbsp; POWERED BY PYTHON & STREAMLIT</div>',
    unsafe_allow_html=True
)
