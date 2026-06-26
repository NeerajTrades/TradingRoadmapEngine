import plotly.graph_objects as go
import streamlit as st
import pandas as pd
import numpy as np


st.set_page_config(
    page_title="Trading Roadmap Engine",
    page_icon="🚀",
    layout="wide"
)

st.markdown("""
<style>

/* Remove Streamlit header anchor links */

a[data-testid="stHeaderActionElements"] {
    display: none !important;
}

/* Remove all heading link icons */

.stHeading a {
    display: none !important;
}

/* Remove markdown anchor buttons */

button[kind="header"] {
    display: none !important;
}

</style>
""", unsafe_allow_html=True)

st.markdown(
    """
    <h1 style='
    text-align:center;
    margin-bottom:5px;
    '>
    🚀 Trading Roadmap Engine
    </h1>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <div style='
    text-align:center;
    color:#9aa0aa;
    font-size:18px;
    margin-bottom:35px;
    '>
    Milestone & Growth Projection System
    </div>
    """,
    unsafe_allow_html=True
)

# -----------------------------------
# GOOGLE SHEETS CONNECTION
# -----------------------------------

sheet_id = "1p36E9e6tx97J1jZ1cx9-6BRmCNaHAxaUOye-uPdlseE"

csv_url = (
    f"https://docs.google.com/spreadsheets/d/"
    f"{sheet_id}/export?format=csv"
)

df = pd.read_csv(csv_url)

df = df.iloc[:, :13]

current_capital = float(
    df["Trade Amount"].iloc[-1]
)

actual_trade_numbers = list(

    range(
        len(df)
    )
)

actual_capital_curve = list(

    df["Trade Amount"]
)

MILESTONES = [

    10000,
    50000,

    100000,
    500000,

    1000000,
    2500000,
    5000000,

    10000000,
    20000000
]

def get_next_milestone(capital):

    for milestone in MILESTONES:

        if capital < milestone:
            return milestone

    crore = 30000000

    while capital >= crore:
        crore += 10000000

    return crore

def calculate_projection(

    current_capital,

    target_milestone,

    win_rate,

    rrr,

    risk_percent,

    trades_per_month

):

    win_rate_decimal = (
        win_rate / 100
    )

    loss_rate_decimal = (
        1 - win_rate_decimal
    )

    expectancy_r = (

        win_rate_decimal * rrr

        -

        loss_rate_decimal

    )

    growth_per_trade = (

        expectancy_r
        *
        risk_percent

    ) / 100

    projection_capital = (
        current_capital
    )

    trades_needed = 0

    trade_numbers = [0]

    capital_curve = [
        current_capital
    ]

    while (

        projection_capital
        <
        target_milestone

        and

        trades_needed
        <
        10000

    ):

        projection_capital *= (

            1 +
            growth_per_trade
        )

        trade_numbers.append(
            trades_needed + 1
        )

        capital_curve.append(
            projection_capital
        )

        if projection_capital >= target_milestone:

            capital_curve[-1] = target_milestone

            break

        trades_needed += 1

    projection_df = pd.DataFrame({

        "Trade": trade_numbers,

        "Capital": capital_curve

    })

    # -----------------------------------
    # PROJECTED CURVE
    # -----------------------------------

    projection_trade_numbers = [

        actual_trade_numbers[-1]
    ]

    projection_capital_curve = [

        current_capital
    ]

    for i in range(

        len(trade_numbers) - 1

    ):

        projection_trade_numbers.append(

            actual_trade_numbers[-1]
            +
            i
            +
            1

        )

        projection_capital_curve.append(

            capital_curve[i + 1]

        )

    months_needed = (

        trades_needed
        /
        trades_per_month

    )

    growth_multiple = (

        projection_capital
        /
        current_capital

    )

    return {

        "trades_needed":
        trades_needed,

        "months_needed":
        months_needed,

        "projection_capital":
        projection_capital,

        "growth_multiple":
        growth_multiple,

        "projection_df":
        projection_df,

        "projection_trade_numbers":
        projection_trade_numbers,

        "projection_capital_curve":
        projection_capital_curve

    }


next_milestone = get_next_milestone(
    current_capital
)

capital_needed = (
    next_milestone -
    current_capital
)

growth_needed = (
    (
        next_milestone /
        current_capital
    ) - 1
) * 100

st.markdown(
    f"""
    <style>
    .summary-panel {{
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 12px;
        background:
        rgba(10,18,30,0.75);    
        padding: 28px 10px;
        margin-top: 30px;
        margin-bottom: 40px;
    }}
    .summary-grid {{
        display: grid;
        grid-template-columns:
        repeat(4,1fr);
        align-items: center;
        text-align: center;
    }}
    .summary-item {{
        
    }}
    .summary-label {{
        color:
        rgba(180,180,180,0.85);
        font-size: 12px;
        letter-spacing: 2px;
        text-transform: uppercase;
        margin-bottom: 14px;
    }}
    .summary-value {{
        color: white;
        font-size: 28px;
        font-weight: 600;
        text-shadow:
        0 0 25px
        rgba(255,255,255,0.15);
    }}
    </style>
    <div class="summary-panel">
        <div class="summary-grid">
            <div class="summary-item">
                <div class="summary-label">
                    Current Capital
                </div>
                <div class="summary-value">
                    ₹{current_capital:,.0f}
                </div>
            </div>
            <div class="summary-item">
                <div class="summary-label">
                    Next Milestone
                </div>
                <div class="summary-value">
                    ₹{next_milestone:,.0f}
                </div>
            </div>
            <div class="summary-item">
                <div class="summary-label">
                    Capital Needed
                </div>
                <div class="summary-value">
                    ₹{capital_needed:,.0f}
                </div>
            </div>
            <div class="summary-item">
                <div class="summary-label">
                    Growth Needed
                </div>
                <div class="summary-value">
                    {growth_needed:.1f}%
                </div>
            </div>
        </div>
    </div>

    """,

    unsafe_allow_html=True
)

# -----------------------------------
# SIDEBAR
# -----------------------------------


st.sidebar.markdown(
    """
    <h2 style='text-align:center;'>
    🎯 MILESTONE
    </h2>
    """,
    unsafe_allow_html=True
)
st.sidebar.markdown("---")

milestone_mode = st.sidebar.radio(

    "Milestone Mode",

    [
        "Next Milestone",
        "Choose Milestone",
        "Custom Milestone"
    ]
)

if milestone_mode == "Next Milestone":

    target_milestone = next_milestone

elif milestone_mode == "Choose Milestone":

    target_milestone = st.sidebar.selectbox(

        "Target Milestone",

        MILESTONES,

        index=1
    )

else:

    target_milestone = st.sidebar.number_input(

        "Custom Target",

        min_value=int(current_capital),

        value=int(next_milestone),

        step=1000
    )

st.sidebar.markdown("---")

with st.sidebar.expander(
    "📈 Scenario A",
    expanded=False
):
    
    trades_per_month_a = st.number_input(

        "Trades Per Month",

        min_value=1,

        max_value=100,

        value=8
    )

    win_rate_a = st.slider(

        "Win Rate %",

        min_value=1,

        max_value=100,

        value=50
    )

    rrr_a = st.number_input(

        "RRR",

        min_value=1.0,

        value=5.0,

        step=0.1
    )

    risk_a = st.number_input(

        "Risk %",

        min_value=0.5,

        value=15.0,

        step=0.1
    )

st.sidebar.markdown("---")

with st.sidebar.expander(
    "📈 Scenario B",
    expanded=False
):

    trades_per_month_b = st.number_input(

        "Trades Per Month (B)",

        min_value=1,

        max_value=100,

        value=8
    )

    win_rate_b = st.slider(

        "Win Rate % (B)",

        min_value=1,

        max_value=100,

        value=45
    )

    rrr_b = st.number_input(

        "RRR (B)",

        min_value=1.0,

        value=4.0,

        step=0.1
    )

    risk_percent_b = st.number_input(

        "Risk % (B)",

        min_value=0.5,

        value=10.0,

        step=0.1
    )

st.sidebar.markdown("---")

with st.sidebar.expander(
    "📈 Scenario C",
    expanded=False
):

    trades_per_month_c = st.number_input(

        "Trades Per Month (C)",

        min_value=1,

        max_value=100,

        value=8
    )

    win_rate_c = st.slider(

        "Win Rate % (C)",

        min_value=1,

        max_value=100,

        value=60
    )

    rrr_c = st.number_input(

        "RRR (C)",

        min_value=1.0,

        value=3.0,

        step=0.1
    )

    risk_percent_c = st.number_input(

        "Risk % (C)",

        min_value=0.5,

        value=8.0,

        step=0.1
    )

st.sidebar.markdown("---")

if "run_projection" not in st.session_state:
    st.session_state.run_projection = False

if st.sidebar.button(
    "🚀 Run Projection",
    use_container_width=True
):
    st.session_state.run_projection = True

# -----------------------------------
# PROJECTION ENGINE
# -----------------------------------

if st.session_state.run_projection:

    scenario_a = calculate_projection(

        current_capital=current_capital,

        target_milestone=target_milestone,

        win_rate=win_rate_a,

        rrr=rrr_a,

        risk_percent=risk_a,

        trades_per_month=trades_per_month_a

    )

    

    trades_needed = scenario_a["trades_needed"]

    months_needed = scenario_a["months_needed"]

    projection_capital = scenario_a["projection_capital"]

    growth_multiple = scenario_a["growth_multiple"]

    projection_df = scenario_a["projection_df"]

    projection_trade_numbers = scenario_a[
        "projection_trade_numbers"
    ]

    projection_capital_curve = scenario_a[
        "projection_capital_curve"
    ]

    st.markdown("---")

    st.markdown(
        """
        <div style='
        font-size:24px;
        font-weight:700;
        color:white;
        margin-bottom:15px;
        '>
        📊 Projection Summary
        </div>
        """,
        unsafe_allow_html=True
    )

    summary_col1, summary_col2, summary_col3, summary_col4 = st.columns(4)

    with summary_col1:

        st.markdown(
            f"""
            <div style="
            background:rgba(0,229,168,0.08);
            border:1px solid rgba(0,229,168,0.35);
            border-radius:14px;
            padding:22px;
            text-align:center;
            ">
                <div style="
                color:#9aa0aa;
                font-size:12px;
                letter-spacing:1px;
                ">
                TRADES NEEDED
                </div>
                <div style="
                font-size:38px;
                font-weight:700;
                color:#00E5A8;
                ">
                {trades_needed}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with summary_col2:

        st.markdown(
            f"""
            <div style="
            background:rgba(255,215,0,0.08);
            border:1px solid rgba(255,215,0,0.35);
            border-radius:14px;
            padding:22px;
            text-align:center;
            ">
                <div style="
                color:#9aa0aa;
                font-size:12px;
                letter-spacing:1px;
                ">
                MONTHS NEEDED
                </div>
                <div style="
                font-size:38px;
                font-weight:700;
                color:#FFD700;
                ">
                {months_needed:.1f}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with summary_col3:

        st.markdown(
            f"""
            <div style="
            background:rgba(0,229,255,0.08);
            border:1px solid rgba(0,229,255,0.35);
            border-radius:14px;
            padding:22px;
            text-align:center;
            ">
                <div style="
                color:#9aa0aa;
                font-size:12px;
                letter-spacing:1px;
                ">
                EXPECTED CAPITAL
                </div>
                <div style="
                font-size:38px;
                font-weight:700;
                color:#00E5FF;
                ">
                ₹{projection_capital:,.0f}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with summary_col4:

        st.markdown(
            f"""
            <div style="
            background:rgba(107,124,255,0.08);
            border:1px solid rgba(107,124,255,0.35);
            border-radius:14px;
            padding:22px;
            text-align:center;
            ">
                <div style="
                color:#9aa0aa;
                font-size:12px;
                letter-spacing:1px;
                ">
                GROWTH MULTIPLE
                </div>
                <div style="
                font-size:38px;
                font-weight:700;
                color:#6B7CFF;
                ">
                {growth_multiple:.2f}x
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown("---")

    st.markdown(
        """
        <div style='
        font-size:24px;
        font-weight:700;
        color:white;
        margin-bottom:15px;
        '>
        📈 Roadmap Projection
        </div>
        """,
        unsafe_allow_html=True
    )

    scenario_b = calculate_projection(

        current_capital=current_capital,

        target_milestone=target_milestone,

        win_rate=win_rate_b,

        rrr=rrr_b,

        risk_percent=risk_percent_b,

        trades_per_month=trades_per_month_b

    )

    scenario_c = calculate_projection(

        current_capital=current_capital,

        target_milestone=target_milestone,

        win_rate=win_rate_c,

        rrr=rrr_c,

        risk_percent=risk_percent_c,

        trades_per_month=trades_per_month_c

    )

    roadmap_results = []

    for milestone in MILESTONES:

        if milestone <= current_capital:
            continue

        milestone_projection = calculate_projection(

            current_capital=current_capital,

            target_milestone=milestone,

            win_rate=win_rate_a,

            rrr=rrr_a,

            risk_percent=risk_a,

            trades_per_month=trades_per_month_a

        )

        roadmap_results.append({

            "Milestone": f"₹{milestone:,.0f}",

            "Trades": milestone_projection["trades_needed"],

            "Months": round(

                milestone_projection["months_needed"],

                1

            ),

            "Capital": f"₹{milestone:,.0f}"

        })

    fig = go.Figure()

    projection_trade_numbers_b = (
        scenario_b["projection_trade_numbers"]
    )

    projection_capital_curve_b = (
        scenario_b["projection_capital_curve"]
    )

    projection_trade_numbers_c = (
        scenario_c["projection_trade_numbers"]
    )

    projection_capital_curve_c = (
        scenario_c["projection_capital_curve"]
    )

    # -----------------------------------
    # NORMALIZED SCENARIO LENGTHS
    # -----------------------------------

    max_length = max(

        len(projection_trade_numbers),

        len(projection_trade_numbers_b),

        len(projection_trade_numbers_c)

    )

    while len(projection_trade_numbers) < max_length:

        projection_trade_numbers.append(

            projection_trade_numbers[-1] + 1

        )

        projection_capital_curve.append(

            projection_capital_curve[-1]

        )

    while len(projection_trade_numbers_b) < max_length:

        projection_trade_numbers_b.append(

            projection_trade_numbers_b[-1] + 1

        )

        projection_capital_curve_b.append(

            projection_capital_curve_b[-1]

        )

    while len(projection_trade_numbers_c) < max_length:

        projection_trade_numbers_c.append(

            projection_trade_numbers_c[-1] + 1

        )

        projection_capital_curve_c.append(

            projection_capital_curve_c[-1]

        )

    fig.add_trace(

        go.Scatter(

            x=actual_trade_numbers,

            y=actual_capital_curve,

            mode="lines+markers",

            name="Actual",

            line=dict(
                width=4,
                color="#6B7CFF"
            ),
            marker=dict(

                size=5,

                color="#6B7CFF"

            ),
            hovertemplate=
            "Trade %{x}<br>" +
            "Capital ₹%{y:,.0f}" +
            "<extra>Actual</extra>",

        )
    )

    fig.add_trace(

        go.Scatter(

            x=projection_trade_numbers,

            y=projection_capital_curve,

            mode="lines+markers",

            name="Scenario A",

            line=dict(

                width=2.5,

                color="rgba(0,229,255,0.85)",

                shape="linear"

            ),
            marker=dict(

                size=4,

                color="rgba(255,255,255,1)"

            ),
            hovertemplate=
            "Trade %{x}<br>" +
            "Capital ₹%{y:,.0f}" +
            "<extra>Scenario A</extra>",
        )
    )

    fig.add_trace(

        go.Scatter(

            x=projection_trade_numbers,

            y=projection_capital_curve,

            mode="lines",

            line=dict(width=0),

            showlegend=False,

            hoverinfo="skip"

        )

    )

    # Scenario B Line

    fig.add_trace(

        go.Scatter(

            x=projection_trade_numbers_b,

            y=projection_capital_curve_b,

            mode="lines+markers",

            name="Scenario B",

            line=dict(

                width=2,

                color="rgba(255,0,0,0.75)",

                shape="linear"

            ),
            marker=dict(

                size=4,

                color="rgba(255,255,255,1)"

            ),
            hovertemplate=
            "Trade %{x}<br>" +
            "Capital ₹%{y:,.0f}" +
            "<extra>Scenario B</extra>",

        )

    )

    # Invisible copy of Scenario A

    fig.add_trace(

        go.Scatter(

            x=projection_trade_numbers,

            y=projection_capital_curve,

            mode="lines",

            line=dict(width=0),

            showlegend=False,

            hoverinfo="skip"

        )

    )

    # Fill A -> B

    fig.add_trace(

        go.Scatter(

            x=projection_trade_numbers_b,

            y=projection_capital_curve_b,

            mode="lines",

            fill="tonexty",

            fillcolor="rgba(0,229,255,0.08)",

            line=dict(width=0),

            showlegend=False,

            hoverinfo="skip"

        )

    )


    fig.add_trace(

        go.Scatter(

            x=projection_trade_numbers_b,

            y=projection_capital_curve_b,

            mode="lines",

            line=dict(width=0),

            showlegend=False,

            hoverinfo="skip"

        )

    )

    fig.add_trace(

        go.Scatter(

            x=projection_trade_numbers_c,

            y=projection_capital_curve_c,

            mode="lines+markers",

            name="Scenario C",

            line=dict(

                width=2,

                color="rgba(255,190,0,0.75)",

                shape="linear"

            ),
            marker=dict(

                size=4,

                color="rgba(255,255,255,1)"

            ),
            hovertemplate=
            "Trade %{x}<br>" +
            "Capital ₹%{y:,.0f}" +
            "<extra>Scenario C</extra>",

        )

    )

    # Invisible B

    fig.add_trace(

        go.Scatter(

            x=projection_trade_numbers_b,

            y=projection_capital_curve_b,

            mode="lines",

            line=dict(width=0),

            showlegend=False,

            hoverinfo="skip"

        )

    )

    fig.add_trace(

        go.Scatter(

            x=projection_trade_numbers_c,

            y=projection_capital_curve_c,

            mode="lines",

            fill="tonexty",

            fillcolor="rgba(255,190,0,0.10)",

            line=dict(width=0),

            showlegend=False,

            hoverinfo="skip"

        )

    )

    fig.add_trace(

        go.Scatter(

            x=projection_trade_numbers_c,

            y=projection_capital_curve_c,

            mode="lines",

            fill="tonexty",

            fillcolor="rgba(255,190,0,0.10)",

            line=dict(width=0),

            showlegend=False,

            hoverinfo="skip"

        )

    )

    fig.add_trace(

        go.Scatter(

            x=[actual_trade_numbers[-1]],

            y=[current_capital],

            mode="markers",

            name="Current",

            marker=dict(

                size=12,

                color="#FF4D8D",

                line=dict(
                    width=2,
                    color="white"
                )

            )
        )
    )

    fig.add_hline(
        y=target_milestone,
        line_width=2,
        line_color="rgba(255,215,0,0.55)"
    )

    

    fig.update_layout(

        height=800,

        template="plotly_dark",

        title="Capital Growth Roadmap",

        xaxis_title="Trade Number",

        yaxis_title="Capital (₹)",

        yaxis=dict(

            range=[

                0,

                target_milestone * 1.15

            ]

        ),

        legend=dict(

            orientation="h",

            yanchor="top",

            y=-0.12,

            xanchor="center",

            x=0.5,
            traceorder="normal"

        ),

        showlegend=True
    )

    st.plotly_chart(

        fig,

        use_container_width=True
    )

    st.markdown("---")

    st.markdown( 
        """ 
        <div style=' 
        font-size:24px; 
        font-weight:700; 
        color:white; 
        '> 
        🛣️ Milestone Timeline 
        </div> 
        """, 
        unsafe_allow_html=True )

    completed_count = 0

    milestone_values = [

        50000,
        100000,
        500000,
        1000000,
        2500000,
        5000000,
        10000000,
        20000000

    ]

    progress_percent = (

        current_capital
        /
        next_milestone

    ) * 100

    progress_percent = min(
        progress_percent,
        100
    )

    ladder_html = f"""
    <div style='
    position:relative;
    display:flex;
    justify-content:space-between;
    align-items:flex-start;
    margin-top:40px;
    margin-bottom:40px;
    padding-top:10px;
    '>
    <div style='
    position:absolute;
    top:11px;
    left:5%;
    right:5%;
    height:2px;
    background:rgba(255,255,255,0.12);
    '>
    </div>
    <div style='
    position:absolute;
    top:11px;
    left:5%;
    width:14%;
    height:2px;
    background:#00E5A8;
    box-shadow:0 0 12px #00E5A8;
    '>
    </div>
    """

    for i, row in enumerate(roadmap_results):
        milestone = milestone_values[i]

        if current_capital >= milestone:

            node_color = "#00E5A8"
            glow = "0 0 15px #00E5A8"
            scale = "1"

        elif milestone > current_capital and milestone == next_milestone:

            node_color = "#FFD700"
            glow = "0 0 25px #FFD700"
            scale = "1.25"

        else:

            node_color = "#64748B"
            glow = "none"
            scale = "1"
        ladder_html += f"""
        <div style='
            text-align:center;
            flex:1;
            '>
            <div style='
            width:24px;
            height:24px;
            transform:scale({scale});
            border-radius:50%;
            background:{node_color};
            position:relative;
            z-index:2;
            margin:auto;
            margin-top:-10px;
            box-shadow:{glow};
            '>
            </div>
            <div style='
            color:white;
            font-weight:600;
            margin-top:8px;
            '>
            {row["Milestone"]}
            </div>
            <div style='
            color:#9aa0aa;
            font-size:12px;
            margin-top:4px;
            '>
            {row["Trades"]} Trades
            </div>
            <div style='
            color:#6f7b8f;
            font-size:11px;
            margin-top:2px;
            '>
            {row["Months"]} Months
            </div>
        </div>
        """
    
    ladder_html += "</div>"

    st.html(ladder_html)
    
    #roadmap_df = pd.DataFrame(
    #    roadmap_results
    #)

    #st.dataframe(

     #   roadmap_df,

      #  use_container_width=True,

       # hide_index=True
    #)

    st.markdown("---")

    st.markdown(
        """
        <div style='
        font-size:24px;
        font-weight:700;
        color:white;
        '>
        📊 Scenario Comparison
        </div>
        """,
        unsafe_allow_html=True
    )

    comparison_df = pd.DataFrame({

        "Scenario": [

            "A",
            "B",
            "C"

        ],

        "Trades": [

            scenario_a["trades_needed"],

            scenario_b["trades_needed"],

            scenario_c["trades_needed"]

        ],

        "Months": [

            round(
                scenario_a["months_needed"],
                1
            ),

            round(
                scenario_b["months_needed"],
                1
            ),

            round(
                scenario_c["months_needed"],
                1
            )

        ],

        "Final Capital": [

            f"₹{scenario_a['projection_capital']:,.0f}",

            f"₹{scenario_b['projection_capital']:,.0f}",

            f"₹{scenario_c['projection_capital']:,.0f}"

        ],

        "Growth Multiple": [

            f"{scenario_a['growth_multiple']:.2f}x",

            f"{scenario_b['growth_multiple']:.2f}x",

            f"{scenario_c['growth_multiple']:.2f}x"

        ]

    })

    best_growth_index = comparison_df[
        "Growth Multiple"
    ].str.replace(
        "x",
        "",
        regex=False
    ).astype(float).idxmax()

    fastest_index = comparison_df[
        "Trades"
    ].idxmin()

    lowest_risk_index = 2

    best_growth_name = (
        f"Scenario {comparison_df.loc[best_growth_index,'Scenario']}"
    )

    best_growth_multiple = float(
        comparison_df.loc[
            best_growth_index,
            "Growth Multiple"
        ].replace("x","")
    )

    fastest_name = (
        f"Scenario {comparison_df.loc[fastest_index,'Scenario']}"
    )

    fastest_trades = (
        comparison_df.loc[
            fastest_index,
            "Trades"
        ]
    )

    lowest_risk_name = "Scenario C"

    lowest_risk_value = risk_percent_c

    best_growth_col, fastest_col, risk_col = st.columns(3)

    with best_growth_col:

        st.markdown(
            f"""
            <div style="
            text-align:center;
            padding:25px;
            border-radius:14px;
            background:rgba(0,229,168,0.08);
            border:1px solid rgba(0,229,168,0.20);
            ">
                <div style="
                color:#00E5A8;
                letter-spacing:2px;
                font-size:12px;
                ">
                🏆 BEST GROWTH
                </div>
                <div style="
                font-size:22px;
                font-weight:600;
                margin-top:10px;
                margin-bottom:10px;
                ">
                {best_growth_name}
                </div>
                <div style="
                font-size:42px;
                font-weight:700;
                color:#00E5A8;
                ">
                {best_growth_multiple:.2f}x
                </div>   
                <div style="
                color:#9aa0aa;
                font-size:13px;
                margin-top:10px;
                ">
                Win Rate: {win_rate_a}% ,
                RRR: {rrr_a} ,
                Risk: {risk_a}%
                </div>            
            </div>
            """,
            unsafe_allow_html=True
        )
    with fastest_col:
        st.markdown(
            f"""
            <div style="
            text-align:center;
            padding:25px;
            border-radius:14px;
            background:rgba(255,215,0,0.08);
            border:1px solid rgba(255,215,0,0.20);
            ">
                <div style="
                color:#FFD700;
                letter-spacing:2px;
                font-size:12px;
                ">
                ⚡ FASTEST ROUTE
                </div>
                <div style="
                font-size:22px;
                font-weight:600;
                margin-top:10px;
                margin-bottom:10px;
                ">
                {fastest_name}
                </div>
                <div style="
                font-size:42px;
                font-weight:700;
                color:#FFD700;
                ">
                {fastest_trades}
                </div>
                <div style="
                color:#9aa0aa;
                font-size:13px;
                margin-top:10px;
                ">
                Trades Needed
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with risk_col:
        st.markdown(
            f"""
            <div style="
            text-align:center;
            padding:25px;
            border-radius:14px;
            background:rgba(255,80,80,0.08);
            border:1px solid rgba(255,80,80,0.20);
            ">
                <div style="
                color:#FF6B6B;
                letter-spacing:2px;
                font-size:12px;
                ">
                🔰 LOWEST RISK
                </div>
                <div style="
                font-size:22px;
                font-weight:600;
                margin-top:10px;
                margin-bottom:10px;
                ">
                {lowest_risk_name}
                </div>
                <div style="
                font-size:42px;
                font-weight:700;
                color:#FF6B6B;
                ">
                {lowest_risk_value:.1f}%
                </div>    
                <div style="
                color:#9aa0aa;
                font-size:13px;
                margin-top:10px;
                ">
                Capital Preservation Focus
                </div>          
            </div>
            """,
            unsafe_allow_html=True
        )
    st.markdown("---")

    st.markdown(
        """
        <div style='
        font-size:24px;
        font-weight:700;
        color:white;
        '>
        🛡️ Drawdown Stress Test
        </div>
        """,
        unsafe_allow_html=True
    )

    if "drawdown_risk" not in st.session_state:

        st.session_state.drawdown_risk = float(risk_a)

    drawdown_risk = st.number_input(

        "Evaluate Risk %",

        min_value=0.5,

        max_value=100.0,

        step=0.5,

        key="drawdown_risk",

        help="Test any fixed risk percentage."

    )

    drawdown_rows = []

    capital = current_capital

    for losses in range(1, 11):

        capital *= (

            1

            -

            drawdown_risk

            /

            100

        )

        risk_percent = (

            (current_capital - capital)

            /

            current_capital

        ) * 100

        drawdown = risk_percent

        drawdown_rows.append({

            "Losses": losses,

            "Capital Left": f"₹{capital:,.0f}",

            "Drawdown %": f"{drawdown:.1f}%"

        })

    drawdown_html = """
    <table style="
    width:100%;
    border-collapse:collapse;
    margin-top:15px;
    font-size:15px;
    ">

    <tr style="
    background:#1F2430;
    ">
    <th style="padding:14px;width:25%;text-align:center;">Losses</th>
    <th style="padding:14px;width:25%;text-align:center;">Capital Left</th>
    <th style="padding:14px;width:25%;text-align:center;">Drawdown</th>
    <th style="padding:14px;width:25%;text-align:center;">Status</th>
    </tr>
    """

    for row in drawdown_rows:

        dd = float(
            row["Drawdown %"].replace("%","")
        )

        if dd < 20:

            color = "#00E676"
            status = "🟢 Safe"

        elif dd < 40:

            color = "#FFD54F"
            status = "🟡 Moderate"

        elif dd < 60:

            color = "#FF9800"
            status = "🟠 High"

        else:

            color = "#FF5252"
            status = "🔴 Extreme"

        drawdown_html += f"""
        <tr style="
        border-bottom:1px solid rgba(255,255,255,0.08);
        ">
            <td style="
            padding:12px;
            text-align:center;
            ">
                {row["Losses"]}
            </td>

            <td style="
            padding:12px;
            text-align:center;
            ">
                {row["Capital Left"]}
            </td>

            <td style="
            padding:12px;
            text-align:center;
            color:{color};
            font-weight:700;
            ">
                {row["Drawdown %"]}
            </td>

            <td style="
            padding:12px;
            text-align:center;
            color:{color};
            font-weight:600;
            ">
                {status}
            </td>

        </tr>
        """

    drawdown_html += "</table>"

    st.html(drawdown_html)

    fifty_losses = None
    seventyfive_losses = None
    ninety_losses = None

    capital = current_capital

    losses = 0

    while losses < 50:

        losses += 1

        capital *= (1 - drawdown_risk / 100)

        drawdown = (

            (current_capital - capital)

            /

            current_capital

        ) * 100

        if fifty_losses is None and drawdown >= 50:

            fifty_losses = losses

        if seventyfive_losses is None and drawdown >= 75:

            seventyfive_losses = losses

        if ninety_losses is None and drawdown >= 90:

            ninety_losses = losses

    st.markdown("")

    dd_col1, dd_col2, dd_col3 = st.columns(3)

    with dd_col1:

        st.markdown(
            f"""
            <div style="
            text-align:center;
            padding:22px;
            border-radius:14px;
            background:rgba(255,165,0,0.08);
            border:1px solid rgba(255,165,0,0.25);
            ">
                <div style="
                color:#9aa0aa;
                font-size:12px;
                letter-spacing:2px;
                ">
                ⚠️ 50% DRAWDOWN
                </div>
                <div style="
                font-size:42px;
                font-weight:700;
                color:#FFA500;
                margin-top:10px;
                ">
                {fifty_losses}
                </div>
                <div style="
                color:#9aa0aa;
                ">
                Consecutive Losses
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with dd_col2:

        st.markdown(
            f"""
            <div style="
            text-align:center;
            padding:22px;
            border-radius:14px;
            background:rgba(255,80,80,0.08);
            border:1px solid rgba(255,80,80,0.25);
            ">
                <div style="
                color:#9aa0aa;
                font-size:12px;
                letter-spacing:2px;
                ">
                🚨 75% DRAWDOWN
                </div>
                <div style="
                font-size:42px;
                font-weight:700;
                color:#FF5252;
                margin-top:10px;
                ">
                {seventyfive_losses}
                </div>
                <div style="
                color:#9aa0aa;
                ">
                Consecutive Losses
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with dd_col3:

        st.markdown(
            f"""
            <div style="
            text-align:center;
            padding:22px;
            border-radius:14px;
            background:rgba(180,0,0,0.10);
            border:1px solid rgba(255,0,0,0.25);
            ">
                <div style="
                color:#9aa0aa;
                font-size:12px;
                letter-spacing:2px;
                ">
                ☠️ 90% DRAWDOWN
                </div>
                <div style="
                font-size:42px;
                font-weight:700;
                color:#FF3030;
                margin-top:10px;
                ">
                {ninety_losses}
                </div>
                <div style="
                color:#9aa0aa;
                ">
                Consecutive Losses
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
