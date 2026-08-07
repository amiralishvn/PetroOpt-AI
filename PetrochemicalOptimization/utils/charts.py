import pandas as pd
import matplotlib.pyplot as plt


class ChartGenerator:

    @staticmethod
    def production_dataframe(result):

        data = {
            "Production Unit": [],
            "Production (tons)": []
        }

        for unit, amount in result.production_plan.items():
            data["Production Unit"].append(unit)
            data["Production (tons)"].append(amount)

        return pd.DataFrame(data)

    @staticmethod
    def production_chart(result):

        df = ChartGenerator.production_dataframe(result)

        fig, ax = plt.subplots(figsize=(8, 4))

        ax.bar(
            df["Production Unit"],
            df["Production (tons)"]
        )

        ax.set_title("Production Plan")

        ax.set_xlabel("Units")

        ax.set_ylabel("Production")

        return fig