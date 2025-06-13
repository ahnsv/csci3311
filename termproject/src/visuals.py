import altair as alt

def cost_bar_chart(avg_cost, year):
    return (
        alt.Chart(avg_cost)
        .mark_bar()
        .encode(
            x=alt.X("Type:N", title="Institution Type"),
            y=alt.Y("Cost:Q", title="Average Cost ($)"),
            color="Cost Type:N",
            tooltip=["Type", "Cost Type", alt.Tooltip("Cost", format=",.0f")],
        )
        .properties(
            title=f"Average College Costs by Type ({year})", width=600, height=400
        )
    )

def enrollment_bar_chart(enroll_by_type, year):
    return (
        alt.Chart(enroll_by_type)
        .mark_bar()
        .encode(
            x=alt.X("Type:N", title="Institution Type"),
            y=alt.Y("Enrollment:Q", title="Total Enrollment"),
            color="Type:N",
            tooltip=["Type", alt.Tooltip("Enrollment", format=",")],
        )
        .properties(
            title=f"Total Enrollment by Institution Type ({year})", width=500, height=350
        )
    )

def demographic_stacked_chart(demo_melted, year):
    return (
        alt.Chart(demo_melted)
        .mark_bar()
        .encode(
            x=alt.X("Type:N", title="Institution Type"),
            y=alt.Y("Count:Q", stack="normalize", title="Proportion"),
            color="Demographic:N",
            tooltip=["Type", "Demographic", alt.Tooltip("Count", format=",")],
        )
        .properties(
            title=f"Demographic Breakdown by Institution Type ({year})", width=500, height=350
        )
    ) 