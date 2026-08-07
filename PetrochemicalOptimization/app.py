import streamlit as st

from chatbot.assistant import ChatAssistant
from chatbot.conversation import Conversation

from lp.optimizer import LinearProgrammingOptimizer

from utils.validator import InputValidator
from utils.charts import ChartGenerator

from models.maintenance import MaintenanceTask

from ga.genetic import GeneticAlgorithm

# --------------------------------------------------
# Initialize Assistant
# --------------------------------------------------

assistant = ChatAssistant()
conversation = Conversation(assistant)

# --------------------------------------------------
# Session State
# --------------------------------------------------

if "refinery" not in st.session_state:
    st.session_state.refinery = None

if "optimization_result" not in st.session_state:
    st.session_state.optimization_result = None

if "maintenance_schedule" not in st.session_state:
    st.session_state.maintenance_schedule = None

if "best_chromosome" not in st.session_state:
    st.session_state.best_chromosome = None

if "optimized" not in st.session_state:
    st.session_state.optimized = False

if "refinery" not in st.session_state:
    st.session_state.refinery = None

if "result" not in st.session_state:
    st.session_state.result = None

if "maintenance_schedule" not in st.session_state:
    st.session_state.maintenance_schedule = None

# --------------------------------------------------
# Page Configuration
# --------------------------------------------------

st.set_page_config(
    page_title="PetroOpt AI",
    page_icon="🏭",
    layout="wide"
)

# --------------------------------------------------
# Header
# --------------------------------------------------

st.title("🏭 PetroOpt AI")
st.subheader("Intelligent Petrochemical Optimization System")

st.markdown("---")

st.info(assistant.welcome_message())

# --------------------------------------------------
# General Information
# --------------------------------------------------

st.header("General Information")

total_feed = st.number_input(
    "Total Feed",
    min_value=0.0,
    step=1.0
)

total_energy = st.number_input(
    "Total Energy",
    min_value=0.0,
    step=1.0
)

number_of_units = st.number_input(
    "Number of Production Units",
    min_value=1,
    step=1
)

st.markdown("---")

# --------------------------------------------------
# Production Units
# --------------------------------------------------

st.header("Production Units")

production_units = []

for i in range(int(number_of_units)):

    st.subheader(f"Production Unit {i + 1}")

    name = st.text_input(
        "Unit Name",
        key=f"name_{i}"
    )

    capacity = st.number_input(
        "Capacity",
        min_value=0.0,
        step=1.0,
        key=f"capacity_{i}"
    )

    profit = st.number_input(
        "Profit per Ton",
        min_value=0.0,
        step=1.0,
        key=f"profit_{i}"
    )

    feed = st.number_input(
        "Feed Consumption",
        min_value=0.0,
        step=0.1,
        key=f"feed_{i}"
    )

    energy = st.number_input(
        "Energy Consumption",
        min_value=0.0,
        step=0.1,
        key=f"energy_{i}"
    )

    production_units.append(
        {
            "name": name,
            "capacity": capacity,
            "profit": profit,
            "feed": feed,
            "energy": energy
        }
    )

    st.markdown("---")

# --------------------------------------------------
# Maintenance Scheduling
# --------------------------------------------------

st.header("Maintenance Scheduling")

number_of_tasks = st.number_input(
    "Number of Maintenance Tasks",
    min_value=1,
    value=1,
    step=1
)

maintenance_tasks = []

for i in range(int(number_of_tasks)):

    st.subheader(f"Maintenance Task {i + 1}")

    unit_name = st.text_input(
        "Maintenance Unit Name",
        key=f"maintenance_name_{i}"
    )

    duration = st.number_input(
        "Duration (Days)",
        min_value=1,
        step=1,
        key=f"duration_{i}"
    )

    priority = st.number_input(
        "Priority",
        min_value=1,
        max_value=10,
        step=1,
        key=f"priority_{i}"
    )

    earliest_start = st.number_input(
        "Earliest Start Day",
        min_value=1,
        step=1,
        key=f"earliest_{i}"
    )

    latest_finish = st.number_input(
        "Latest Finish Day",
        min_value=1,
        step=1,
        key=f"latest_{i}"
    )

    maintenance_tasks.append({
        "unit_name": unit_name,
        "duration": duration,
        "priority": priority,
        "earliest_start": earliest_start,
        "latest_finish": latest_finish
    })

    st.markdown("---")

# --------------------------------------------------
# Optimization
# --------------------------------------------------

if st.button("🚀 Start Optimization"):

    # ------------------------------------------
    # Save General Information
    # ------------------------------------------

    assistant.save_general_information(
        total_feed,
        total_energy
    )

    # ------------------------------------------
    # Save Production Units
    # ------------------------------------------

    for unit in production_units:

        assistant.save_production_unit(
            name=unit["name"],
            capacity=unit["capacity"],
            profit=unit["profit"],
            feed_consumption=unit["feed"],
            energy_consumption=unit["energy"]
        )

    refinery = assistant.get_refinery_data()

    # ------------------------------------------
    # Validation
    # ------------------------------------------

    errors = []

    errors.extend(
        InputValidator.validate_refinery(refinery)
    )

    errors.extend(
        InputValidator.validate_maintenance_tasks(
            maintenance_tasks
        )
    )

    if errors:

        for error in errors:
            st.error(error)

        st.stop()

    # ------------------------------------------
    # Linear Programming Optimization
    # ------------------------------------------

    optimizer = LinearProgrammingOptimizer()

    result = optimizer.optimize(refinery)

    # ------------------------------------------
    # Prepare Maintenance Tasks
    # ------------------------------------------

    maintenance_objects = []

    for task in maintenance_tasks:

        maintenance_objects.append(

            MaintenanceTask(

                unit_name=task["unit_name"],

                duration=task["duration"],

                priority=task["priority"],

                earliest_start=task["earliest_start"],

                latest_finish=task["latest_finish"]

            )

        )

    # ------------------------------------------
    # Run Genetic Algorithm
    # ------------------------------------------

    if len(maintenance_objects) > 1:
        ga = GeneticAlgorithm(
            maintenance_objects
        )

        best_chromosome, maintenance_schedule = ga.run()

    elif len(maintenance_objects) == 1:

        task = maintenance_objects[0]

        best_chromosome = None

        maintenance_schedule = {
            task.unit_name: {
                "start_day": task.earliest_start,
                "finish_day": (
                    task.earliest_start +
                    task.duration -
                    1
                ),
                "duration": task.duration,
                "priority": task.priority
            }
        }

    else:

        best_chromosome = None

        maintenance_schedule = {}

    st.session_state.refinery = refinery
    st.session_state.result = result
    st.session_state.maintenance_schedule = maintenance_schedule
    st.session_state.optimized = True

if st.session_state.optimized:

    refinery = st.session_state.refinery
    result = st.session_state.result
    maintenance_schedule = st.session_state.maintenance_schedule

    # ------------------------------------------
    # Results Dashboard
    # ------------------------------------------

    st.success("✅ Optimization completed successfully!")

    st.divider()

    col1, col2 = st.columns(2)

    with col1:

        st.metric(
            label="Status",
            value=result.status
        )

        st.metric(
            label="Maximum Profit",
            value=f"${result.optimal_profit:,.2f}"
        )

    with col2:

        st.metric(
            label="Feed Used",
            value=f"{result.used_feed:.2f}"
        )

        st.metric(
            label="Energy Used",
            value=f"{result.used_energy:.2f}"
        )

    st.divider()

    # ------------------------------------------
    # Production Plan
    # ------------------------------------------

    st.subheader("Production Plan")

    for unit_name, amount in result.production_plan.items():

        st.write(
            f"🔹 **{unit_name}** : {amount:.2f} tons"
        )

    st.divider()

    # ------------------------------------------
    # Remaining Resources
    # ------------------------------------------

    st.subheader("Remaining Resources")

    st.write(f"Remaining Feed : {result.remaining_feed:.2f}")

    st.write(f"Remaining Energy : {result.remaining_energy:.2f}")

    st.divider()

    # ------------------------------------------
    # Production Table
    # ------------------------------------------

    st.subheader("Production Table")

    df = ChartGenerator.production_dataframe(result)

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )

    st.divider()

    # ------------------------------------------
    # Production Chart
    # ------------------------------------------

    st.subheader("Production Chart")

    fig = ChartGenerator.production_chart(result)

    st.pyplot(fig)
    st.divider()

    st.subheader("Maintenance Schedule")

    if maintenance_schedule:

        for unit_name, schedule in maintenance_schedule.items():

            start_day = schedule["start_day"]
            finish_day = schedule["finish_day"]
            duration = schedule["duration"]
            priority = schedule["priority"]

            if start_day == finish_day:

                day_text = f"Day {start_day}"

            else:

                day_text = (
                    f"Day {start_day} → Day {finish_day}"
                )

            st.write(
                f"🔧 **{unit_name}** → "
                f"{day_text} "
                f"(Duration: {duration} days, "
                f"Priority: {priority})"
            )

    else:

        st.info("No maintenance schedule generated.")

    st.divider()

    st.header("🤖 PetroOpt AI Assistant")

    user_question = st.text_input(
        "Ask a question about the optimization"
    )

    if st.button("Ask Assistant"):

        answer = conversation.send_message(
            user_message=user_question,
            refinery=st.session_state.refinery,
            optimization_result=st.session_state.result,
            maintenance_schedule=st.session_state.maintenance_schedule
        )

        st.session_state.chat_answer = answer

    # -----------------------------
    # Show Last Assistant Response
    # -----------------------------

    if "chat_answer" in st.session_state:

        st.success(st.session_state.chat_answer)	