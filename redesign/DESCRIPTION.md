<!-- #  Discussion Topic
Design and Redesign: Testing the Impact of Visualization Alternatives

Purpose
You'll practice formulating experimental comparisons and task-based questions, setting the foundation for evaluating data visualization effectiveness.

Discussion Prompt
Find an existing data visualization online and create at least two alternative designs for presenting the same data, either using Altair (if data is available) or simply pen and paper to sketch ideas. Then, write 2–3 task questions that you would ask participants to assess how effectively they can interpret the visualizations  (e.g., "Which country had the longest protest?" or "How many revolutions occurred in 2011?").

If you can't find a suitable visualization, use one of the following resources:

Design and RedesignLinks to an external site.
Settling the Debate: Bars vs Lollipops (vs Dot Plots)Links to an external site.
Don't Mekko with My MarimekkoLinks to an external site.
A Redesign of Florence Nightingale's Rose ChartLinks to an external site.
Share your design sketches and task questions, along with your hypothesis on which design might perform best.

(Optional) Set up your experiment in Qualtrics to allow others to participate. You may need to use a randomizer to assign each participant to a different experimental condition. -->

# Redesigning Moseley's X-ray Law Visualization

## Original Visualization
The original visualization of Moseley's X-ray law typically presents a scatter plot of the square root of X-ray frequency (√frequency) versus atomic number (Z), often with regression lines for different X-ray series (Kα, Kβ, etc.). This design is effective for showing the linear relationship discovered by Moseley, but it can be limited in helping users connect the data to the periodic table structure or in supporting more complex comparative tasks.

## Alternative Designs

### Design A: Scatter Plot with Regression Lines (Interactive)
- **Description:**  
  This design uses an interactive scatter plot (Altair) where users can toggle the Y-axis between √frequency and wavelength. Each point represents an element's X-ray emission, colored by series (Kα, Kβ, Lα, Lβ). Regression lines are overlaid for each series, and tooltips provide detailed data on hover.
- **Strengths:**  
  - Clearly shows the linear relationship for each series.
  - Allows users to switch between two scientific perspectives (frequency vs. wavelength).
  - Interactive tooltips enhance data exploration.

### Design B: Small-Multiples Slope Charts + Linked Periodic Table
- **Description:**  
  This design presents two coordinated views:
  1. **Periodic Table:** Elements are arranged in their periodic table positions. Clicking an element highlights it across both views.
  2. **Slope Charts:** For each X-ray series, a small-multiple chart shows √frequency vs. Z, with regression lines. The opacity of points/lines is linked to the selected element.
- **Strengths:**  
  - Connects X-ray data to the periodic table, supporting chemical context.
  - Small multiples allow for easier comparison between series.
  - Linked highlighting helps users see relationships between atomic structure and X-ray properties.

## Task Questions for Evaluation

1. **Which element has the highest √frequency for the Kα series?**  
   *(Assesses ability to identify maxima within a series.)*
2. **How does the trend of √frequency vs. atomic number differ between the Kα and Lα series?**  
   *(Assesses ability to compare trends across series.)*
3. **Find an element in the periodic table and describe its X-ray emission properties.**  
   *(Assesses ability to use the linked views to connect periodic table position with X-ray data.)*

## Hypothesis

**I hypothesize that Design B (Small-Multiples + Linked Periodic Table) will perform best for tasks that require connecting atomic properties to periodic table structure or comparing across series.**
- For simple trend identification (e.g., finding the highest value in a series), both designs are effective, but Design A's single scatter plot may be faster.
- For tasks involving chemical context or cross-series comparison, Design B's linked and faceted views will reduce cognitive load and improve accuracy.

## (Optional) Experiment Setup
If implemented in Qualtrics, participants would be randomly assigned to one of the two designs and asked to answer the task questions above. Their accuracy and response times would be measured to evaluate the effectiveness of each design.

---

References:  
- Streamlit App: Moseley X-ray Redesign (see attached code)  
- Altair Documentation: https://altair-viz.github.io/  
- Moseley's Law - Wikipedia: https://en.wikipedia.org/wiki/Moseley%27s_law

