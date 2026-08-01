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

@st.cache_data(ttl=3600)
def load_sheet():

    return pd.read_csv(csv_url)

df = load_sheet()

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

# -----------------------------------
# MILESTONE SELECTOR
# -----------------------------------

def handle_milestone_selection(
    selected_label,
    milestone_map
):

    if selected_label == "CUSTOM":

        st.session_state.custom_mode = True

    else:

        st.session_state.custom_mode = False

        st.session_state.selected_milestone = (
            milestone_map[selected_label]
        )

    if st.session_state.custom_mode:

        if "custom_target" not in st.session_state:

            st.session_state.custom_target = int(
                st.session_state.selected_milestone
            )

        custom_value = st.number_input(

            "Custom Target (₹)",

            min_value=10000,

            max_value=1000000000,

            step=10000,

            format="%d",

            key="custom_target"

        )

        st.session_state.selected_milestone = custom_value

def calculate_projection(

    current_capital,

    target_milestone,

    win_rate,

    rrr,

    risk_percent,

    fee_percent,

    trades_per_month

):

    win_rate_decimal = (
        win_rate / 100
    )

    loss_rate_decimal = (
        1 - win_rate_decimal
    )

    gross_profit = (

        risk_percent
        *
        rrr

    )

    net_profit = (

        gross_profit
        -
        fee_percent

    )

    net_loss = (

        risk_percent
        +
        fee_percent

    )

    growth_per_trade = (

        (

            win_rate_decimal
            *
            net_profit

        )

        -

        (

            loss_rate_decimal
            *
            net_loss

        )

    ) / 100

    projection_capital = (
        current_capital
    )

    trades_needed = 0

    trade_numbers = [0]

    capital_curve = [
        current_capital
    ]

    while trades_needed < 10000:

        trades_needed += 1

        projection_capital *= (1 + growth_per_trade)

        trade_numbers.append(trades_needed)

        if projection_capital >= target_milestone:

            projection_capital = target_milestone

            capital_curve.append(projection_capital)

            break

        capital_curve.append(projection_capital)


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

    net_rrr = (

        net_profit

        /

        net_loss

    )

    breakeven_wr = (

        net_loss

        /

        (

            net_profit

            +

            net_loss

        )

    ) * 100

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
        projection_capital_curve,

        "net_profit": net_profit,

        "net_loss": net_loss,

        "gross_profit": gross_profit,

        "expectancy": growth_per_trade * 100,
        
        "net_rrr": net_rrr,

        "win_rate": win_rate,

        "breakeven_winrate": breakeven_wr,

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



    

st.markdown(
    """
    <style>
    div[data-testid="stVerticalBlockBorderWrapper"]:has(.milestone-card){
        border:1px solid rgba(0,255,200,0.15);
        border-radius:18px;
        background:linear-gradient(
            180deg,
            rgba(0,255,180,0.03),
            rgba(255,255,255,0.01)
        );
        box-shadow:
            0 0 30px rgba(0,255,180,0.04);
        padding:8px;
    }
    </style>
    """,
    unsafe_allow_html=True
)





milestone_card = st.container(border=True)

with milestone_card:

    st.markdown(
        '<div class="milestone-card"></div>',
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div style="
            display:flex;
            justify-content:space-between;
            align-items:center;
            padding-bottom:14px;
            margin-bottom:18px;
            border-bottom:1px solid rgba(255,255,255,0.08);
        ">
            <div style="
                font-size:24px;
                font-weight:700;
                color:white;
            ">
                🎯 Milestone Selection
            </div>
            <div style="
                padding:6px 16px;
                border-radius:20px;
                background:rgba(0,255,180,0.08);
                color:#00E6A8;
                font-size:12px;
                font-weight:700;
                letter-spacing:1px;
            ">
                TARGET
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    milestone_labels = [

        "₹10K",

        "₹25K",

        "₹50K",

        "₹1L",

        "₹2.5L",

        "₹5L",

        "₹10L",

        "₹25L",

        "₹50L",

        "₹1CR",

        "₹2.5CR",

        "₹5CR",

        "₹10CR",

        "CUSTOM"

    ]

    milestone_values = [

        10000,

        25000,

        50000,

        100000,

        250000,

        500000,

        1000000,

        2500000,

        5000000,

        10000000,

        25000000,

        50000000,

        100000000

    ]

    milestone_map = dict(
        zip(
            milestone_labels[:-1],
            milestone_values
        )
    )

    if "selected_milestone" not in st.session_state:

        st.session_state.selected_milestone = next_milestone

    if "confirmed_milestone" not in st.session_state:

        st.session_state.confirmed_milestone = next_milestone

    # -----------------------------------
    # CONFIRMED PROJECTION VALUES
    # -----------------------------------

    defaults = {

        "confirmed_trades_a":3,
        "confirmed_win_a":50,
        "confirmed_rrr_a":5.0,
        "confirmed_risk_a":12.5,
        "confirmed_fee_a":2.5,

        "confirmed_trades_b":3,
        "confirmed_win_b":66,
        "confirmed_rrr_b":5.0,
        "confirmed_risk_b":12.5,
        "confirmed_fee_b":2.5,

        "confirmed_trades_c":3,
        "confirmed_win_c":75,
        "confirmed_rrr_c":5.0,
        "confirmed_risk_c":12.5,
        "confirmed_fee_c":2.5

    }

    for key,value in defaults.items():

        if key not in st.session_state:

            st.session_state[key] = value

    if "custom_mode" not in st.session_state:

        st.session_state.custom_mode = False



    
    st.sidebar.markdown(
        """
        <h2 style='text-align:center;'>
        🎯 MILESTONE
        </h2>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <style>

        div[role="radiogroup"]{

            display:flex;

            flex-wrap:wrap;

            gap:10px;

            justify-content:flex-start;

        }

        div[role="radiogroup"] > label{

            background:#1A1F2B;

            border:1px solid rgba(255,255,255,.10);

            border-radius:14px;

            padding:14px 18px;

            min-width:92px;

            justify-content:center;

            transition:.25s;

            cursor:pointer;

            overflow:hidden;

            position:relative;

        }

        /* Entire radio button */
        label[data-baseweb="radio"]{

            display:flex !important;
            align-items:center;

            min-width:82px;

            height:48px;

            padding:0 16px;

            border-radius:12px;

            border:1px solid rgba(255,255,255,.12);

            background:#1B2230;

            transition:.25s;

            cursor:pointer;

        }

        /* Hover */

        label[data-baseweb="radio"]:hover{

            border:1px solid #3BA8FF;

            box-shadow:
                0 0 12px rgba(59,168,255,.18);

        }

        /* Hide radio circle */

        label[data-baseweb="radio"] > div:first-child{

            display:none !important;

        }

        /* Remove default spacing */

        label[data-baseweb="radio"] > div:last-child{

            margin-left:0 !important;

        }

        /* Selected */

        label[data-baseweb="radio"]:has(input:checked){

            background:
                linear-gradient(
                    180deg,
                    rgba(0,255,180,.18),
                    rgba(0,255,180,.08)
                );

            border:1px solid rgba(0,255,180,.70);

            box-shadow:
                inset 0 1px 0 rgba(255,255,255,.08),
                0 0 16px rgba(0,255,180,.22);

        }

        /* Bottom glow */

        label[data-baseweb="radio"]:has(input:checked)::after{

            content:"";

            position:absolute;

            left:18%;

            right:18%;

            bottom:-4px;

            height:3px;

            border-radius:10px;

            background:#00ffb4;

            box-shadow:
                0 0 12px #00ffb4;

        }

        </style>
        """,
        unsafe_allow_html=True
    )

    selected_label = st.radio(

        "",

        options=milestone_labels,

        horizontal=True,

        key="milestone_selector"

    )

    st.session_state.selected_label = selected_label

    handle_milestone_selection(

        selected_label,

        milestone_map

    )

projection_form = st.form(

    key="projection_setup",

    clear_on_submit=False

)

with projection_form:

    scenario_a_card = st.container(border=True)

    with scenario_a_card:

        st.markdown(
            """
            <div style="
                display:flex;
                align-items:center;
                justify-content:space-between;
                margin-bottom:22px;
                padding-bottom:14px;
                border-bottom:1px solid rgba(255,255,255,0.08);
            ">
                <div style="
                    font-size:24px;
                    font-weight:700;
                    color:white;
                ">
                    📈 Scenario A
                </div>
                <div style="
                    padding:6px 14px;
                    border-radius:20px;
                    background:rgba(0,255,170,0.08);
                    color:#00E6A8;
                    font-size:12px;
                    font-weight:700;
                    letter-spacing:1px;
                ">
                    STANDARD
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        scenario_a_col1, scenario_a_col2, scenario_a_col3, scenario_a_col4 = st.columns(4)

    with scenario_a_col1:

        trades_per_month_a = st.number_input(

            "Trades Per Month",

            min_value=1,

            max_value=100,

            value=3

        )


    with scenario_a_col2:

        win_rate_a = st.slider(

            "Win Rate %",

            min_value=1,

            max_value=100,

            value=50

        )


    with scenario_a_col3:

        rrr_a = st.number_input(

            "RRR",

            min_value=1.0,

            value=5.0,

            step=0.1

        )


    with scenario_a_col4:

        risk_col, fee_col = st.columns([3,2])

        with risk_col:

            risk_a = st.number_input(

                "Risk %",

                min_value=0.5,

                value=12.5,

                step=0.1,

                key="risk_a"

            )

        with fee_col:

            fee_a = st.number_input(

                "Fee %",

                min_value=0.0,

                value=2.5,

                step=0.1,

                key="fee_a"

            )

    st.markdown("")

    scenario_b_card = st.container(border=True)

    with scenario_b_card:

        st.markdown(
            """
            <div style="
                display:flex;
                align-items:center;
                justify-content:space-between;
                margin-bottom:22px;
                padding-bottom:14px;
                border-bottom:1px solid rgba(255,255,255,0.08);
            ">
                <div style="
                    font-size:24px;
                    font-weight:700;
                    color:white;
                ">
                    📈 Scenario B
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        scenario_b_col1, scenario_b_col2, scenario_b_col3, scenario_b_col4 = st.columns(4)

    with scenario_b_col1:

        trades_per_month_b = st.number_input(

            "Trades Per Month (B)",

            min_value=1,

            max_value=100,

            value=3

        )


    with scenario_b_col2:

        win_rate_b = st.slider(

            "Win Rate % (B)",

            min_value=1,

            max_value=100,

            value=66

        )


    with scenario_b_col3:

        rrr_b = st.number_input(

            "RRR (B)",

            min_value=1.0,

            value=5.0,

            step=0.1

        )


    with scenario_b_col4:

        risk_col, fee_col = st.columns([3,2])

        with risk_col:

            risk_percent_b = st.number_input(

                "Risk % (B)",

                min_value=0.5,

                value=12.5,

                step=0.1,

                key="risk_b"

            )

        with fee_col:

            fee_b = st.number_input(

                "Fee %",

                min_value=0.0,

                value=2.5,

                step=0.1,

                key="fee_b"

            )

    st.markdown("")

    scenario_c_card = st.container(border=True)

    with scenario_c_card:

        st.markdown(
            """
            <div style="
                display:flex;
                align-items:center;
                justify-content:space-between;
                margin-bottom:22px;
                padding-bottom:14px;
                border-bottom:1px solid rgba(255,255,255,0.08);
            ">
                <div style="
                    font-size:24px;
                    font-weight:700;
                    color:white;
                ">
                    📈 Scenario C
                </div>               
            </div>
            """,
            unsafe_allow_html=True
        )

        scenario_c_col1, scenario_c_col2, scenario_c_col3, scenario_c_col4 = st.columns(4)

    with scenario_c_col1:

        trades_per_month_c = st.number_input(

            "Trades Per Month (C)",

            min_value=1,

            max_value=100,

            value=3

        )


    with scenario_c_col2:

        win_rate_c = st.slider(

            "Win Rate % (C)",

            min_value=1,

            max_value=100,

            value=75

        )


    with scenario_c_col3:

        rrr_c = st.number_input(

            "RRR (C)",

            min_value=1.0,

            value=5.0,

            step=0.1

        )


    with scenario_c_col4:

        risk_col, fee_col = st.columns([3,2])

        with risk_col:

            risk_percent_c = st.number_input(

                "Risk % (C)",

                min_value=0.5,

                value=12.5,

                step=0.1,

                key="risk_c"

            )

        with fee_col:

            fee_c = st.number_input(

                "Fee %",

                min_value=0.0,

                value=2.5,

                step=0.1,

                key="fee_c"

            )

    st.sidebar.markdown("---")

    if "run_projection" not in st.session_state:
        st.session_state.run_projection = False

    st.markdown("")

    left_space, center_button, right_space = st.columns([2,3,2])

    with center_button:

        submitted = st.form_submit_button(
            "🚀 Run Projection",
            use_container_width=True
        )
        if submitted:

            st.session_state.run_projection = True

            st.session_state.confirmed_milestone = (
                st.session_state.selected_milestone
            )

            st.session_state.confirmed_trades_a = trades_per_month_a
            st.session_state.confirmed_win_a = win_rate_a
            st.session_state.confirmed_rrr_a = rrr_a
            st.session_state.confirmed_risk_a = risk_a
            st.session_state.confirmed_fee_a = fee_a

            st.session_state.confirmed_trades_b = trades_per_month_b
            st.session_state.confirmed_win_b = win_rate_b
            st.session_state.confirmed_rrr_b = rrr_b
            st.session_state.confirmed_risk_b = risk_percent_b
            st.session_state.confirmed_fee_b = fee_b

            st.session_state.confirmed_trades_c = trades_per_month_c
            st.session_state.confirmed_win_c = win_rate_c
            st.session_state.confirmed_rrr_c = rrr_c
            st.session_state.confirmed_risk_c = risk_percent_c
            st.session_state.confirmed_fee_c = fee_c


# -----------------------------------
# PROJECTION ENGINE
# -----------------------------------

if st.session_state.run_projection:

    scenario_a = calculate_projection(

        current_capital,

        st.session_state.confirmed_milestone,

        st.session_state.confirmed_win_a,

        st.session_state.confirmed_rrr_a,

        st.session_state.confirmed_risk_a,

        st.session_state.confirmed_fee_a,

        st.session_state.confirmed_trades_a

    )

    

    trades_needed = scenario_a["trades_needed"]

    months_needed = scenario_a["months_needed"]

    projection_capital = scenario_a["projection_capital"]

    growth_multiple = scenario_a["growth_multiple"]

    gross_profit = scenario_a["gross_profit"]

    net_profit = scenario_a["net_profit"]

    net_loss = scenario_a["net_loss"]

    expectancy = scenario_a["expectancy"]

    net_rrr = scenario_a["net_rrr"]

    breakeven_winrate = scenario_a["breakeven_winrate"]

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

    st.markdown(
        f"""
        <style>
        .projection-summary{{
            border:1px solid rgba(255,255,255,0.08);
            border-radius:18px;
            background:rgba(10,18,30,.72);
            padding:30px 34px;
            margin-top:18px;
            margin-bottom:28px;
        }}
        .projection-grid{{
            display:grid;
            grid-template-columns:1fr 1fr;
            gap:80px;
            position:relative;
        }}
        .projection-grid::after{{
            content:"";
            position:absolute;
            left:50%;
            top:0;
            bottom:0;
            width:1px;
            background:
            rgba(255,255,255,.05);
        }}
        .projection-row{{
            display:flex;
            justify-content:space-between;
            align-items:center;
            padding:11px 0;
            border-bottom:1px solid rgba(255,255,255,.06);
        }}
        .projection-label{{
            color:#8E98AA;
            font-size:12px;
            letter-spacing:1.2px;
            text-transform:uppercase;
        }}
        .projection-value{{
            color:white;
            font-size:20px;
            font-weight:700;
        }}
        </style>
        <div class="projection-summary">
            <div class="projection-grid">
                <div>
                    <div class="projection-row">
                        <div class="projection-label">
                            Gross Profit
                        </div>
                        <div class="projection-value" style="color:#00E5A8;">
                            {gross_profit:.2f}%
                        </div>
                    </div>
                    <div class="projection-row">
                        <div class="projection-label">
                            Net Profit
                        </div>
                        <div class="projection-value" style="color:#00E5A8;">
                            {net_profit:.2f}%
                        </div>
                    </div>
                    <div class="projection-row">
                        <div class="projection-label">
                            Net Loss
                        </div>
                        <div class="projection-value" style="color:#FF5C5C;">
                            -{net_loss:.2f}%
                        </div>
                    </div>
                    <div class="projection-row">
                        <div class="projection-label">
                            Net RRR
                        </div>
                        <div class="projection-value">
                            {net_rrr:.2f}R
                        </div>
                    </div>
                    <div class="projection-row">
                        <div class="projection-label">
                            Expectancy
                        </div>
                        <div class="projection-value">
                            {expectancy:.2f}%
                        </div>
                    </div>
                </div>
                <div>
                    <div class="projection-row">
                        <div class="projection-label">
                            Trades Needed
                        </div>
                        <div class="projection-value">
                            {trades_needed}
                        </div>
                    </div>
                    <div class="projection-row">
                        <div class="projection-label">
                            Months Needed
                        </div>
                        <div class="projection-value">
                            {months_needed:.1f}
                        </div>
                    </div>
                    <div class="projection-row">
                        <div class="projection-label">
                            Expected Capital
                        </div>
                        <div class="projection-value">
                            ₹{projection_capital:,.0f}
                        </div>
                    </div>
                    <div class="projection-row">
                        <div class="projection-label">
                            Growth Multiple
                        </div>
                        <div class="projection-value" style="color:#FFD700;">
                            {growth_multiple:.2f}×
                        </div>
                    </div>
                    <div class="projection-row">
                        <div class="projection-label">
                            Breakeven Win Rate
                        </div>
                        <div class="projection-value" style="color:#00D4FF;">
                            {breakeven_winrate:.2f}%
                        </div>
                    </div>
                </div>
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

        target_milestone=st.session_state.confirmed_milestone,

        win_rate=st.session_state.confirmed_win_b,

        rrr=st.session_state.confirmed_rrr_b,

        risk_percent=st.session_state.confirmed_risk_b,

        fee_percent=st.session_state.confirmed_fee_b,

        trades_per_month=st.session_state.confirmed_trades_b

    )

    scenario_c = calculate_projection(

        current_capital=current_capital,

        target_milestone=st.session_state.confirmed_milestone,

        win_rate=st.session_state.confirmed_win_c,

        rrr=st.session_state.confirmed_rrr_c,

        risk_percent=st.session_state.confirmed_risk_c,

        fee_percent=st.session_state.confirmed_fee_c,

        trades_per_month=st.session_state.confirmed_trades_c

    )

    roadmap_results = []

    timeline_results = [
        {
            "Milestone": "START",
            "Milestone Value": 0,
            "Trades": "-",
            "Months": "-"
        }
    ]

    

    for milestone in MILESTONES:

        if milestone <= current_capital:
            continue

        milestone_projection = calculate_projection(

            current_capital=current_capital,

            target_milestone=milestone,

            win_rate=st.session_state.confirmed_win_a,

            rrr=st.session_state.confirmed_rrr_a,

            risk_percent=st.session_state.confirmed_risk_a,

            fee_percent=st.session_state.confirmed_fee_a,

            trades_per_month=st.session_state.confirmed_trades_a

        )

        roadmap_results.append({

            "Milestone": f"₹{milestone:,.0f}",

            "Milestone Value": milestone,

            "Trades": milestone_projection["trades_needed"],

            "Months": round(

                milestone_projection["months_needed"],

                1

            ),

            "Capital": f"₹{milestone:,.0f}"

        })

    timeline_results.extend(roadmap_results)

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

    projection_trade_numbers_fill = projection_trade_numbers.copy()
    projection_capital_curve_fill = projection_capital_curve.copy()

    projection_trade_numbers_b_fill = projection_trade_numbers_b.copy()
    projection_capital_curve_b_fill = projection_capital_curve_b.copy()

    projection_trade_numbers_c_fill = projection_trade_numbers_c.copy()
    projection_capital_curve_c_fill = projection_capital_curve_c.copy()

    # -----------------------------------
    # NORMALIZED SCENARIO LENGTHS
    # -----------------------------------

    max_length = max(
        len(projection_trade_numbers_fill),
        len(projection_trade_numbers_b_fill),
        len(projection_trade_numbers_c_fill)
    )
    while len(projection_trade_numbers_fill) < max_length:
        projection_trade_numbers_fill.append(
            projection_trade_numbers_fill[-1] + 1
        )
        projection_capital_curve_fill.append(
            projection_capital_curve_fill[-1]
        )
    while len(projection_trade_numbers_b_fill) < max_length:
        projection_trade_numbers_b_fill.append(
            projection_trade_numbers_b_fill[-1] + 1
        )
        projection_capital_curve_b_fill.append(
            projection_capital_curve_b_fill[-1]
        )
    while len(projection_trade_numbers_c_fill) < max_length:
        projection_trade_numbers_c_fill.append(
            projection_trade_numbers_c_fill[-1] + 1
        )
        projection_capital_curve_c_fill.append(
            projection_capital_curve_c_fill[-1]
        )
    fig.add_trace(
        go.Scatter(
            x=actual_trade_numbers,
            y=actual_capital_curve,
            mode="lines+markers",
            name="Actual",
            line=dict(
                width=5,
                color="rgba(107,124,255,0.80)"
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
            mode="lines",
            fill="tozeroy",
            fillcolor="rgba(58,123,255,0.08)",
            name="Scenario A",
            line=dict(
                width=4.5,
                color="#3A7BFF",
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

    
    # Scenario B Line

    fig.add_trace(
        go.Scatter(
            x=projection_trade_numbers_b,
            y=projection_capital_curve_b,
            mode="lines",
            fill="tozeroy",
            fillcolor="rgba(196,69,69,0.07)",
            name="Scenario B",
            line=dict(
                width=3,
                color="#C44545",
                dash="solid",
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


    fig.add_trace(
        go.Scatter(
            x=projection_trade_numbers_c,
            y=projection_capital_curve_c,
            mode="lines",
            fill="tozeroy",
            fillcolor="rgba(35,155,90,0.07)",
            name="Scenario C",
            line=dict(
                width=3,
                color="#2FA36B",
                dash="solid",
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

    endpoint_traces = [

        (
            projection_trade_numbers[-1],
            projection_capital_curve[-1],
            "#3A7BFF"
        ),

        (
            projection_trade_numbers_b[-1],
            projection_capital_curve_b[-1],
            "#C44545"
        ),

        (
            projection_trade_numbers_c[-1],
            projection_capital_curve_c[-1],
            "#2FA36B"
        )

    ]

    for x, y, color in endpoint_traces:
        fig.add_trace(
            go.Scatter(
                x=[x],
                y=[y],
                mode="markers",
                showlegend=False,
                hoverinfo="skip",
                marker=dict(
                    size=32,
                    color=color,
                    opacity=0.12,
                    line=dict(width=0)
                )
            )
        )

        fig.add_trace(
            go.Scatter(
                x=[x],
                y=[y],
                mode="markers",
                showlegend=False,
                hoverinfo="skip",
                marker=dict(
                    size=7,
                    color=color,
                    line=dict(
                        width=1.5,
                        color="white"
                    )
                )
            )
        )

    fig.add_trace(

        go.Scatter(

            x=[actual_trade_numbers[-1]],

            y=[current_capital],

            mode="markers",

            showlegend=False,

            hoverinfo="skip",

            marker=dict(

                size=34,

                color="rgba(255,79,154,0.12)",

                line=dict(width=0)

            )

        )

    )

    fig.add_trace(

        go.Scatter(

            x=[actual_trade_numbers[-1]],

            y=[current_capital],

            mode="markers",

            name="Current",

            marker=dict(

                size=8,

                color="#FF4F9A",

                line=dict(

                    width=1.5,

                    color="white"

                )

            )
        )
    )

    fig.add_hline(

        y=st.session_state.confirmed_milestone,

        line_width=1.2,

        line_dash="solid",

        line_color="#D4AF37"

    )

    

    fig.update_layout(

        height=680,

        template="none",

        paper_bgcolor="rgba(10,18,30,0)",

        plot_bgcolor="rgba(10,18,30,0.82)",

        margin=dict(

            l=35,

            r=35,

            t=55,

            b=70

        ),

        title=None,

        xaxis=dict(

            title="Trade Number",

            showgrid=True,

            gridcolor="rgba(255,255,255,0.035)",

            gridwidth=1,

            zeroline=False,

            showline=False,

            ticks="outside",

            tickfont=dict(

                size=12,

                color="#9AA3B2"

            ),

            title_font=dict(

                size=13,

                color="#B8C2D0"

            )

        ),

        yaxis=dict(

            title="Capital (₹)",

            range=[

                0,

                st.session_state.confirmed_milestone * 1.15

            ],

            showgrid=True,

            gridcolor="rgba(255,255,255,0.035)",

            gridwidth=1,

            zeroline=False,

            tickfont=dict(

                size=12,

                color="#9AA3B2"

            ),

            title_font=dict(

                size=13,

                color="#B8C2D0"

            )

        ),

        showlegend=False,

        hoverlabel=dict(

            bgcolor="#111827",

            bordercolor="#2A3648",

            font=dict(

                color="white",

                size=13

            )

        )

    )

    

    st.plotly_chart(

        fig,

        use_container_width=True
    )

    st.markdown(
        """
        <div style="
        display:flex;
        justify-content:center;
        gap:34px;
        align-items:center;
        margin-top:12px;
        margin-bottom:28px;
        flex-wrap:wrap;
        ">
            <div style="display:flex;align-items:center;gap:8px;">
                <div style="
                    width:18px;
                    height:3px;
                    background:#6B7CFF;
                    border-radius:3px;
                "></div>
                <span style="color:#C7D1E0;">Actual</span>
            </div>
            <div style="display:flex;align-items:center;gap:8px;">
                <div style="
                    width:18px;
                    height:3px;
                    background:#3A7BFF;
                    border-radius:3px;
                "></div>
                <span style="color:#C7D1E0;">Scenario A</span>
            </div>
            <div style="display:flex;align-items:center;gap:8px;">
                <div style="
                    width:18px;
                    height:3px;
                    background:#C44545;
                    border-radius:3px;
                "></div>
                <span style="color:#C7D1E0;">Scenario B</span>
            </div>
            <div style="display:flex;align-items:center;gap:8px;">
                <div style="
                    width:18px;
                    height:3px;
                    background:#239B5A;
                    border-radius:3px;
                "></div>
                <span style="color:#C7D1E0;">Scenario C</span>
            </div>
            <div style="display:flex;align-items:center;gap:8px;">
                <div style="
                    width:10px;
                    height:10px;
                    border-radius:50%;
                    background:#FF4F9A;
                    border:2px solid white;
                "></div>
                <span style="color:#C7D1E0;">Current</span>
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

    timeline_steps = len(timeline_results)
    interval_width = 100 / (timeline_steps - 1)
    previous_milestone = 0
    next_value = timeline_results[1]["Milestone Value"]
    completed_intervals = 0

    for i in range(1, len(timeline_results)):

        milestone = timeline_results[i]["Milestone Value"]

        if current_capital >= milestone:

            completed_intervals += 1
            previous_milestone = milestone

        else:

            next_value = milestone
            break

    interval_progress = (
        current_capital - previous_milestone
    ) / (
        next_value - previous_milestone
    )

    interval_progress = max(
        0,
        min(interval_progress, 1)
    )

    progress_percent = (
        (completed_intervals - 1) * interval_width
    ) + (
        interval_progress * interval_width
    )

    progress_percent = max(progress_percent, 0)
    

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
    height:2px;
    width:calc({progress_percent * 0.89}% + 12px);
    background:#00E5A8;
    box-shadow:0 0 10px rgba(0,229,168,0.45);
    '>
    </div>
    """

    for row in timeline_results:
        milestone = row["Milestone Value"]
        if milestone <= current_capital:

            node_color = "#00E5A8"
            glow = "0 0 15px #00E5A8"
            scale = "1"
        elif milestone == next_milestone:
            node_color = "#64748B"
            glow = "none"
            scale = "1"
        else:
            node_color = "#64748B"
            glow = "none"
            scale = "1"
        if row["Milestone"] == "START":
            trades_text = ""
            months_text = ""
        else:
            trades_text = f'{row["Trades"]} Trades'
            months_text = f'{row["Months"]} Months'
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
            {trades_text}
            </div>
            <div style='
            color:#6f7b8f;
            font-size:11px;
            margin-top:2px;
            '>
            {months_text}
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
        "Total Risk": [
            f"{scenario_a['net_loss']:.2f}%",
            f"{scenario_b['net_loss']:.2f}%",
            f"{scenario_c['net_loss']:.2f}%"
        ],

        "Net RRR": [
            f"{scenario_a['net_rrr']:.2f}R",
            f"{scenario_b['net_rrr']:.2f}R",
            f"{scenario_c['net_rrr']:.2f}R"
        ],

        "Win Rate": [
            f"{scenario_a['win_rate']:.0f}%",
            f"{scenario_b['win_rate']:.0f}%",
            f"{scenario_c['win_rate']:.0f}%"
        ],

        "Expectancy": [
            f"{scenario_a['expectancy']:.2f}%",
            f"{scenario_b['expectancy']:.2f}%",
            f"{scenario_c['expectancy']:.2f}%"
        ],

        "Breakeven": [
            f"{scenario_a['breakeven_winrate']:.2f}%",
            f"{scenario_b['breakeven_winrate']:.2f}%",
            f"{scenario_c['breakeven_winrate']:.2f}%"
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

    comparison_df["Rank"] = (
        comparison_df["Trades"]
        .rank(method="dense")
        .astype(int)
    )

    comparison_df = comparison_df.sort_values(
        "Rank"
    ).reset_index(drop=True)

    scenario_cards = comparison_df.to_dict("records")

    comparison_cols = st.columns(3)

    for col, card in zip(comparison_cols, scenario_cards):
        rank = card["Rank"]
        if rank == 1:
            border = "#00E5A8"
            glow = "rgba(0,229,168,0.12)"
        elif rank == 2:
            border = "#F59E0B"
            glow = "rgba(245,158,11,0.10)"
        else:
            border = "#64748B"
            glow = "rgba(100,116,139,0.08)"
        with col:
            st.markdown(
                f"""
    <div style="
    padding:24px;
    border-radius:18px;
    border:1px solid {border};
    background:{glow};
    height:480px;
    ">
    <div style="
    display:flex;
    justify-content:space-between;
    align-items:center;
    ">
    <div style="
    font-size:22px;
    font-weight:700;
    color:white;
    ">
    Scenario {card["Scenario"]}
    </div>
    <div style="
    background:{border};
    color:black;
    padding:4px 10px;
    border-radius:999px;
    font-weight:700;
    font-size:13px;
    ">
    #{rank}
    </div>
    </div>
    <div style="
    margin-top:8px;
    font-size:13px;
    color:#8FA1B8;
    ">
    Projection Summary
    </div>
    <hr style="
    border:0;
    border-top:1px solid rgba(255,255,255,.08);
    margin:18px 0;
    ">
    <div style="display:flex;justify-content:space-between;">
    <span>Trades</span>
    <b>{card["Trades"]}</b>
    </div>
    <br>
    <div style="display:flex;justify-content:space-between;">
    <span>Months</span>
    <b>{card["Months"]}</b>
    </div>
    <br>
    <div style="display:flex;justify-content:space-between;">
    <span>Total Risk</span>
    <b>{card["Total Risk"]}</b>
    </div>
    <br>
    <div style="display:flex;justify-content:space-between;">
    <span>Net R:R</span>
    <b>{card["Net RRR"]}</b>
    </div>
    <br>
    <div style="display:flex;justify-content:space-between;">
    <span>Win Rate</span>
    <b>{card["Win Rate"]}</b>
    </div>
    <br>
    <div style="display:flex;justify-content:space-between;">
    <span>Expectancy</span>
    <b>{card["Expectancy"]}</b>
    </div>
    <br>
    <div style="display:flex;justify-content:space-between;">
    <span>Breakeven</span>
    <b>{card["Breakeven"]}</b>
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
        Drawdown Recovery Calculator
        </div>
        """,
        unsafe_allow_html=True
    )

    if "drawdown_risk" not in st.session_state:

        st.session_state.drawdown_risk = float(
            st.session_state.confirmed_risk_a
        )

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

    st.markdown("")

    left, middle, right = st.columns([1,2,1])

    with middle:

        current_drawdown = st.number_input(

            "Drawdown (%)",

            min_value=0.0,

            max_value=99.0,

            value=0.0,

            step=0.5,

            help="Enter any drawdown percentage."

        )

        if current_drawdown == 100:

            recovery_needed = 0

        else:

            recovery_needed = (

                current_drawdown

                /

                (

                    100

                    -

                    current_drawdown

                )

            ) * 100

        if current_drawdown < 20:

            difficulty = "🟢 Easy"

        elif current_drawdown < 40:

            difficulty = "🟡 Moderate"

        elif current_drawdown < 60:

            difficulty = "🟠 Hard"

        else:

            difficulty = "🔴 Extreme"

        st.markdown(
            f"""
            <div style="
            margin-top:20px;
            border:1px solid rgba(255,255,255,.08);
            border-radius:18px;
            padding:28px;
            background:rgba(20,24,34,.60);
            text-align:center;
            ">
                <div style="
                color:#8FA1B8;
                font-size:13px;
                letter-spacing:2px;
                text-transform:uppercase;
                ">
                Recovery Needed
                </div>
                <div style="
                margin-top:12px;
                font-size:48px;
                font-weight:700;
                color:#00E5A8;
                ">
                {recovery_needed:.2f}%
                </div>
                <div style="
                margin-top:10px;
                color:#AAB4C8;
                ">
                {difficulty}
                </div>
                <hr style="
                margin:24px 0;
                border:0;
                border-top:1px solid rgba(255,255,255,.08);
                ">
            </div>
            """,
            unsafe_allow_html=True
        )