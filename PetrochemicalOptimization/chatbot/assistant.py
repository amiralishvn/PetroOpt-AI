from models.refinery import RefineryData


class ChatAssistant:

    def __init__(self):

        self.refinery = RefineryData(
            total_feed=0,
            total_energy=0,
            units=[]
        )

    # -------------------------------------------------
    # Welcome Message
    # -------------------------------------------------

    def welcome_message(self):

        return (
            "👋 Welcome to PetroOpt AI.\n\n"
            "I can optimize petrochemical production, "
            "analyze optimization results and answer "
            "questions about your refinery."
        )
    # -------------------------------------------------
    # Intent Detection
    # -------------------------------------------------

    def detect_intent(self, message):

        text = message.lower()

        intents = {

            "greeting": [
                "hello",
                "hi",
                "hey",
                "good morning",
                "good evening"
            ],

            "profit": [
                "profit",
                "income",
                "revenue",
                "money",
                "earn",
                "why profit",
                "why high profit"
            ],

            "feed": [
                "feed",
                "feedstock",
                "raw material",
                "resource",
                "why feed",
                "feed exhausted"
            ],

            "energy": [
                "energy",
                "power",
                "electricity",
                "why energy",
                "energy remaining"
            ],

            "production": [
                "production",
                "produce",
                "output",
                "plan",
                "why production",
                "why selected",
                "why propylene",
                "why ethylene",
                "highest production",
                "lowest production"
            ],

            "maintenance": [
                "maintenance",
                "repair",
                "schedule",
                "overhaul"
            ],

            "recommendation": [
                "recommend",
                "suggest",
                "improve",
                "better",
                "optimize"
            ],

            "summary": [
                "summary",
                "report",
                "overall",
                "analysis",
                "result"
            ],

            "explain": [
                "why",
                "reason",
                "because",
                "explain"
            ],

            "compare": [
                "compare",
                "comparison",
                "versus",
                "vs"
            ],
            
            "bottleneck": [
                "bottleneck",
                "constraint",
                "limiting",
                "limit",
                "resource limit",
                "what limits",
                "what is limiting"
            ],

        }

        for intent, keywords in intents.items():

            for keyword in keywords:

                if keyword in text:

                    return intent

        return "unknown"


    # -------------------------------------------------
    # Save Data
    # -------------------------------------------------

    def save_general_information(
        self,
        total_feed,
        total_energy
    ):

        self.refinery.total_feed = total_feed
        self.refinery.total_energy = total_energy

    def save_production_unit(
        self,
        name,
        capacity,
        profit,
        feed_consumption,
        energy_consumption
    ):

        self.refinery.add_unit(

            name=name,

            capacity=capacity,

            profit=profit,

            feed_consumption=feed_consumption,

            energy_consumption=energy_consumption

        )

    def get_refinery_data(self):

        return self.refinery

    # -------------------------------------------------
    # Smart Chat
    # -------------------------------------------------

    def generate_response(

        self,

        message,

        refinery=None,

        optimization_result=None,

        maintenance_schedule=None,

        history=None,

        last_intent=None
        

    ):

        intent = self.detect_intent(message)

        text = message.lower()

        follow_up = False

        follow_up_words = [

            "more",

            "details",

            "again",

            "continue",

            "explain more",

            "tell me more",

            "next",

            "continue please",

            "more information"

        ]

        if intent == "unknown":

            if text in follow_up_words:

                if last_intent is not None:

                    intent = last_intent
                    follow_up = True

        # -------------------------
        # Greeting
        # -------------------------

        if intent == "greeting":

            return (
                "Hello! 👋\n"
                "How can I help you today?"
            )

        # -------------------------
        # Profit
        # -------------------------

        if intent == "profit":

            if follow_up:

                return self._profit_details(
                    refinery,
                    optimization_result
                )

            return self._profit_analysis(
                optimization_result
            )

        # -------------------------
        # Feed
        # -------------------------

        if intent == "feed":

            if follow_up:

                return self._feed_details(
                    refinery,
                    optimization_result
                )

            return self._feed_analysis(
                optimization_result
            )
        
        # -------------------------
        # Energy
        # -------------------------

        if intent == "energy":

            if follow_up:

                return self._energy_details(
                    refinery,
                    optimization_result
                )

            return self._energy_analysis(
                optimization_result
            )

        # -------------------------
        # Production
        # -------------------------

        if intent == "production":

            if follow_up:

                return self._production_details(
                    refinery,
                    optimization_result
                )

            return self._production_analysis(
                optimization_result
            )
        
        # -------------------------
        # Maintenance
        # -------------------------

        if intent == "maintenance":

            if follow_up:

                return self._maintenance_details(
                    maintenance_schedule
                )

            return self._maintenance_analysis(
                maintenance_schedule
            )

        # -------------------------
        # Recommendation
        # -------------------------

        if intent == "recommendation":

            if follow_up:

                return self._recommendation_details(
                    refinery,
                    optimization_result
                )

            return self._recommendation(
                optimization_result
            )
        
        if intent == "summary":

            if follow_up:

                return self._summary_details(
                    refinery,
                    optimization_result,
                    maintenance_schedule
                )

            return self._summary_analysis(
                optimization_result,
                maintenance_schedule
            )
        
        if intent == "explain":

            return self._explain_decision(
                message,
                refinery,
                optimization_result
            )
        
        if intent == "compare":

            return self._compare_units(
                refinery
            )
        
        if intent == "bottleneck":

            return self._bottleneck_analysis(
                optimization_result
            )

        return (
            "Sorry, I couldn't understand your question.\n"
            "Try asking about:\n"
            "- Summary \n"
            "- Profit\n"
            "- Feed\n"
            "- Energy\n"
            "- Production\n"
            "- Maintenance\n"
            "- Recommendation"
        )

    # ==========================================================
    # Analysis Functions
    # ==========================================================

    def _profit_analysis(self, result):

        if result is None:
            return "Optimization has not been executed."

        text = ""

        text += "Profit Analysis\n\n"

        text += (
            f"Current Optimal Profit : "
            f"${result.optimal_profit:,.2f}\n\n"
        )

        if result.remaining_feed == 0:

            text += (
                "• Feed has been fully utilized.\n"
            )

        else:

            text += (
                f"• Remaining Feed : "
                f"{result.remaining_feed:.2f}\n"
            )

        if result.remaining_energy > 0:

            text += (
                "• Energy capacity is still available.\n"
            )

        else:

            text += (
                "• Energy is fully utilized.\n"
            )

        if result.optimal_profit > 0:

            text += (
                "• Optimization completed successfully.\n"
            )

        return text

    def _feed_analysis(self, result):

        if result is None:

            return "No optimization results available."

        text = "Feed Analysis\n\n"

        text += (
            f"Total Feed Used : "
            f"{result.used_feed:.2f}\n"
        )

        text += (
            f"Remaining Feed : "
            f"{result.remaining_feed:.2f}\n\n"
        )

        if result.remaining_feed == 0:

            text += (
                "• All available feed has been consumed.\n"
            )

        elif result.remaining_feed < 10:

            text += (
                "• Feed inventory is running low.\n"
            )

        else:

            text += (
                "• Feed inventory is sufficient.\n"
            )

        utilization = (
            result.used_feed /
            (result.used_feed + result.remaining_feed)
        ) * 100

        text += (
            f"• Feed Utilization : "
            f"{utilization:.1f}%"
        )

        return text

    def _energy_analysis(self, result):

        if result is None:

            return "No optimization results available."

        text = "Energy Analysis\n\n"

        text += (
            f"Total Energy Used : "
            f"{result.used_energy:.2f}\n"
        )

        text += (
            f"Remaining Energy : "
            f"{result.remaining_energy:.2f}\n\n"
        )

        if result.remaining_energy == 0:

            text += (
                "• All available energy has been consumed.\n"
            )

        elif result.remaining_energy < 10:

            text += (
                "• Energy reserve is becoming limited.\n"
            )

        else:

            text += (
                "• Energy reserve is sufficient.\n"
            )

        utilization = (
            result.used_energy /
            (result.used_energy + result.remaining_energy)
        ) * 100

        text += (
            f"• Energy Utilization : "
            f"{utilization:.1f}%"
        )

        return text

    def _production_analysis(self, result):

        if result is None:

            return "No optimization results available."

        text = "Production Analysis\n\n"

        if not result.production_plan:

            return "No production plan available."

        highest_unit = max(
            result.production_plan,
            key=result.production_plan.get
        )

        lowest_unit = min(
            result.production_plan,
            key=result.production_plan.get
        )

        text += "Production Plan\n\n"

        for unit, value in result.production_plan.items():

            text += (
                f"• {unit} : "
                f"{value:.2f} tons\n"
            )

        text += "\n"

        text += (
            f"Highest Production : "
            f"{highest_unit} "
            f"({result.production_plan[highest_unit]:.2f} tons)\n"
        )

        text += (
            f"Lowest Production : "
            f"{lowest_unit} "
            f"({result.production_plan[lowest_unit]:.2f} tons)\n"
        )

        return text
    
    def _production_details(
        self,
        refinery,
        result
    ):
        if result is None:

            return "Run optimization first."

        text = "Detailed Production Report\n\n"

        for unit in refinery.units:

            produced = result.production_plan.get(
                unit.name,
                0
            )

            utilization = (
                produced / unit.capacity
            ) * 100

            text += (
                f"{unit.name}\n"
                f"Produced : {produced:.2f} tons\n"
                f"Capacity : {unit.capacity:.2f} tons\n"
                f"Capacity Utilization : {utilization:.1f}%\n"
                f"Profit : ${unit.profit:.2f}/ton\n"
                f"Feed : {unit.feed_consumption:.2f}\n"
                f"Energy : {unit.energy_consumption:.2f}\n\n"
            )

        return text

    def _maintenance_analysis(
        self,
        schedule
    ):

        if not schedule:

            return "No maintenance schedule available."

        text = "Maintenance Analysis\n\n"

        text += (
            f"Total Scheduled Tasks : "
            f"{len(schedule)}\n\n"
        )

        ordered = sorted(
            schedule.items(),
            key=lambda x: x[1]["start_day"]
        )

        for unit, data in ordered:

            text += (
                f"• {unit} : "
                f"Day {data['start_day']} → Day {data['finish_day']} "
                f"(Duration: {data['duration']} days, "
                f"Priority: {data['priority']})\n"
            )


        earliest = ordered[0]

        text += "\n"

        text += (
            f"Earliest Maintenance : "
            f"{earliest[0]} "
            f"(Day {earliest[1]['start_day']})"
        )

        return text

    def _recommendation(self, result):

        if result is None:
            return "Run optimization first."

        text = "Optimization Recommendations\n\n"

        # Feed
        if result.remaining_feed <= 0:

            text += (
                "• Increase feed availability.\n"
            )

        elif result.remaining_feed < result.used_feed * 0.10:

            text += (
                "• Feed reserve is becoming low.\n"
            )

        else:

            text += (
                "• Feed availability is satisfactory.\n"
            )

        # Energy
        if result.remaining_energy <= 0:

            text += (
                "• Increase available energy.\n"
            )

        elif result.remaining_energy < result.used_energy * 0.10:

            text += (
                "• Energy reserve is becoming limited.\n"
            )

        else:

            text += (
                "• Energy capacity is sufficient.\n"
            )

        # Resource bottleneck
        if result.remaining_feed < result.remaining_energy:

            text += (
                "\nFeed is currently the limiting resource."
            )

        elif result.remaining_energy < result.remaining_feed:

            text += (
                "\nEnergy is currently the limiting resource."
            )

        else:

            text += (
                "\nResources are well balanced."
            )

        return text
    
    def _summary_analysis(
    self,
    result,
    schedule
):

        if result is None:

            return "Run optimization first."

        text = "Optimization Summary\n\n"

        text += f"Status : {result.status}\n"

        text += f"Profit : ${result.optimal_profit:,.2f}\n"

        text += f"Feed Used : {result.used_feed:.2f}\n"

        text += f"Remaining Feed : {result.remaining_feed:.2f}\n"

        text += f"Energy Used : {result.used_energy:.2f}\n"

        text += f"Remaining Energy : {result.remaining_energy:.2f}\n\n"

        if result.production_plan:

            highest_unit = max(
                result.production_plan,
                key=result.production_plan.get
            )

            highest_amount = result.production_plan[highest_unit]

            text += (
                f"Highest Production Unit : "
                f"{highest_unit} "
                f"({highest_amount:.2f} tons)\n"
            )

        else:

            text += "Highest Production Unit : None\n"

        if schedule:

            text += (
                f"Maintenance Tasks : "
                f"{len(schedule)} scheduled\n"
            )

        else:

            text += "Maintenance Tasks : None\n"

        if result.remaining_feed < 5:

            text += "\nFeed resource is almost exhausted."

        else:

            text += "\nFeed reserve is available."

        if result.remaining_energy < 5:

            text += "\nEnergy resource is almost exhausted."

        else:

            text += "\nEnergy reserve is available."

        return text
    
    def _explain_decision(
        self,
        message,
        refinery,
        result
    ):

        if result is None:

            return "Run optimization first."

        text = message.lower()

        for unit in refinery.units:

            if unit.name.lower() in text:

                produced = result.production_plan.get(
                    unit.name,
                    0
                )

                return (

                    f"{unit.name} produces "

                    f"{produced:.2f} tons.\n\n"

                    f"It earns "

                    f"${unit.profit:.2f} per ton "

                    f"while consuming "

                    f"{unit.feed_consumption:.2f} feed "

                    f"and "

                    f"{unit.energy_consumption:.2f} energy.\n\n"

                    "The optimizer selected this "

                    "production level to maximize "

                    "overall refinery profit "

                    "while respecting all resource "

                    "constraints."

                )

        return (

            "Please specify the production "

            "unit name."

        )
    
    def _compare_units(
        self,
        refinery
    ):

        if refinery is None:

            return "No refinery data available."

        text = "Production Unit Comparison\n\n"

        for unit in refinery.units:

            text += (

                f"{unit.name}\n"

                f"Profit : ${unit.profit:.2f}/ton\n"

                f"Capacity : {unit.capacity:.2f}\n"

                f"Feed : {unit.feed_consumption:.2f}\n"

                f"Energy : {unit.energy_consumption:.2f}\n\n"

            )

        best = max(
            refinery.units,
            key=lambda u: u.profit
        )

        text += (

            f"Most Profitable Unit : "

            f"{best.name}"

        )

        return text
    
    def _bottleneck_analysis(self, result):

        if result is None:
            return "Run optimization first."

        text = "Bottleneck Analysis\n\n"

        if result.remaining_feed <= 0:

            text += (
                "Feed is the primary bottleneck.\n"
                "All available feed has been consumed.\n\n"
            )

        elif result.remaining_energy <= 0:

            text += (
                "Energy is the primary bottleneck.\n"
                "No remaining energy is available.\n\n"
            )

        else:

            text += (
                "No critical bottleneck detected.\n"
                "Both feed and energy still have reserve.\n\n"
            )

        text += (
            f"Remaining Feed : {result.remaining_feed:.2f}\n"
        )

        text += (
            f"Remaining Energy : {result.remaining_energy:.2f}"
        )

        return text
    
    def _profit_details(
        self,
        refinery,
        result
    ):

        if result is None:

            return "Run optimization first."

        text = "Detailed Profit Analysis\n\n"

        text += (
            f"Total Profit : "
            f"${result.optimal_profit:,.2f}\n\n"
        )

        if refinery is not None:

            text += "Unit Contributions\n\n"

            for unit in refinery.units:

                produced = result.production_plan.get(
                    unit.name,
                    0
                )

                unit_profit = produced * unit.profit

                text += (
                    f"{unit.name}\n"
                    f"Produced : {produced:.2f} tons\n"
                    f"Profit per Ton : ${unit.profit:.2f}\n"
                    f"Estimated Contribution : "
                    f"${unit_profit:,.2f}\n\n"
                )

        if result.remaining_feed == 0:

            text += (
                "Feed was completely utilized, "
                "which helped maximize profit.\n"
            )

        if result.remaining_energy > 0:

            text += (
                "Some energy capacity remains unused, "
                "indicating feed was the limiting resource."
            )

        return text


    def _feed_details(
        self,
        refinery,
        result
    ):

        if result is None:

            return "Run optimization first."

        text = "Detailed Feed Analysis\n\n"

        total_feed = (
            result.used_feed +
            result.remaining_feed
        )

        text += (
            f"Available Feed : {total_feed:.2f}\n"
        )

        text += (
            f"Consumed Feed : {result.used_feed:.2f}\n"
        )

        text += (
            f"Remaining Feed : {result.remaining_feed:.2f}\n\n"
        )

        if refinery is not None:

            text += "Feed Consumption by Unit\n\n"

            for unit in refinery.units:

                produced = result.production_plan.get(
                    unit.name,
                    0
                )

                consumed = (
                    produced *
                    unit.feed_consumption
                )

                text += (
                    f"{unit.name}\n"
                    f"Produced : {produced:.2f} tons\n"
                    f"Feed Consumption : "
                    f"{consumed:.2f}\n\n"
                )

        utilization = (
            result.used_feed / total_feed
        ) * 100

        text += (
            f"Overall Feed Utilization : "
            f"{utilization:.1f}%\n\n"
        )

        if utilization > 95:

            text += (
                "Feed was almost completely utilized."
            )

        elif utilization > 70:

            text += (
                "Feed utilization was efficient."
            )

        else:

            text += (
                "Large feed reserve remains available."
            )

        return text


    def _energy_details(
        self,
        refinery,
        result
    ):

        if result is None:

            return "Run optimization first."

        text = "Detailed Energy Analysis\n\n"

        total_energy = (
            result.used_energy +
            result.remaining_energy
        )

        text += (
            f"Available Energy : {total_energy:.2f}\n"
        )

        text += (
            f"Consumed Energy : {result.used_energy:.2f}\n"
        )

        text += (
            f"Remaining Energy : {result.remaining_energy:.2f}\n\n"
        )

        if refinery is not None:

            text += "Energy Consumption by Unit\n\n"

            for unit in refinery.units:

                produced = result.production_plan.get(
                    unit.name,
                    0
                )

                consumed = (
                    produced *
                    unit.energy_consumption
                )

                text += (
                    f"{unit.name}\n"
                    f"Produced : {produced:.2f} tons\n"
                    f"Energy Consumption : "
                    f"{consumed:.2f}\n\n"
                )

        utilization = (
            result.used_energy /
            total_energy
        ) * 100

        text += (
            f"Overall Energy Utilization : "
            f"{utilization:.1f}%\n\n"
        )

        if utilization > 95:

            text += (
                "Energy resources were almost fully utilized."
            )

        elif utilization > 70:

            text += (
                "Energy utilization was efficient."
            )

        else:

            text += (
                "Large energy reserve remains available."
            )

        return text


    def _maintenance_details(
        self,
        schedule
    ):

        if not schedule:

            return "No maintenance schedule available."

        text = "Detailed Maintenance Report\n\n"

        ordered = sorted(
            schedule.items(),
            key=lambda x: x[1]
        )

        for unit, day in ordered:

            text += (
                f"{unit}\n"
                f"Scheduled Day : {day}\n\n"
            )

        earliest = ordered[0]
        latest = ordered[-1]

        text += (
            f"Earliest Maintenance : "
            f"{earliest[0]} (Day {earliest[1]})\n"
        )

        text += (
            f"Latest Maintenance : "
            f"{latest[0]} (Day {latest[1]})\n\n"
        )

        text += (
            f"Total Scheduled Units : {len(schedule)}"
        )

        return text


    def _recommendation_details(
        self,
        refinery,
        result
    ):

        if result is None:

            return "Run optimization first."

        text = "Detailed Optimization Recommendations\n\n"

        if result.remaining_feed <= 0:

            text += (
                "Priority 1 : Increase feed availability.\n"
            )

        else:

            text += (
                "Feed supply is acceptable.\n"
            )

        if result.remaining_energy <= 0:

            text += (
                "Priority 2 : Increase energy capacity.\n"
            )

        else:

            text += (
                "Energy supply is acceptable.\n"
            )

        if refinery is not None:

            best = max(
                refinery.units,
                key=lambda u: u.profit
            )

            text += (
                f"\nHighest Profit Unit : "
                f"{best.name}\n"
            )

            text += (
                "Maintaining this unit at high utilization "
                "can improve refinery profitability.\n"
            )

        text += (
            "\nOverall recommendation:\n"
            "Increase the limiting resource before expanding production."
        )

        return text


    def _summary_details(
        self,
        refinery,
        result,
        schedule
    ):

        if result is None:

            return "Run optimization first."

        text = "Detailed Optimization Summary\n\n"

        text += (
            f"Optimization Status : {result.status}\n"
        )

        text += (
            f"Total Profit : ${result.optimal_profit:,.2f}\n\n"
        )

        text += (
            f"Feed Utilization : "
            f"{result.used_feed:.2f}/"
            f"{result.used_feed + result.remaining_feed:.2f}\n"
        )

        text += (
            f"Energy Utilization : "
            f"{result.used_energy:.2f}/"
            f"{result.used_energy + result.remaining_energy:.2f}\n\n"
        )

        if refinery is not None:

            text += "Production Overview\n\n"

            for unit in refinery.units:

                produced = result.production_plan.get(
                    unit.name,
                    0
                )

                text += (
                    f"{unit.name} : "
                    f"{produced:.2f} tons\n"
                )

        if schedule:

            text += (
                f"\nMaintenance Activities : "
                f"{len(schedule)}\n"
            )

        text += (
            "\nOptimization completed successfully "
            "while satisfying all resource constraints."
        )

        return text