<!-- Discussion Prompt
Storytelling Approach – What narrative did you choose for your data story? Why?
Challenges & Iteration – What difficulties did you encounter in designing your data story? How did you refine your approach?
Share your annotated visualization(s) as an image or GIF/video 
Or if it's article-style, embed a PDF or other interactive media (e.g., Streamlit)
Respond to the discussion prompts in a short write-up. -->

# Burtin's Antibiotic Dataset: Interactive Data Story

### Storytelling Approach

For this data story, I chose an interactive, multipage Streamlit app to guide users through Burtin's Antibiotic Dataset. The narrative is structured to move from foundational understanding (introduction and data exploration) to deeper insights (antibiotic effectiveness, Gram staining analysis, and outliers), culminating in actionable recommendations. This approach allows users to not only absorb the key findings but also to explore the data themselves, fostering engagement and discovery. Each page is designed with clear titles, concise descriptions, and visualizations that build upon one another, making the story accessible to both technical and non-technical audiences.

The core narrative centers on how different antibiotics perform against various bacteria, with a special focus on the distinction between Gram-positive and Gram-negative types. By leveraging interactive charts (bar charts, heatmaps, boxplots, and annotated scatterplots), users can visually compare antibiotic effectiveness, identify patterns, and spot exceptions. The final summary page distills these findings into practical recommendations, using a "traffic light" diagram for clarity.

### Challenges & Iteration

One of the main challenges was ensuring clarity and usability in a multipage, interactive format. Early iterations suffered from information overload and unclear navigation. To address this, I adopted a numbered, Camel Case menu structure and provided succinct explanations above every chart. Another challenge was handling data edge cases—such as empty filters or inconsistent column names—which could break visualizations. I resolved these by adding robust data checks and clear user feedback when no data is available.

Designing for both exploration and storytelling required balancing interactivity with narrative flow. I iterated on the visual hierarchy, ensuring that each page had a clear focus and that users were guided through the story with both text and visuals. The addition of a sidebar footer and consistent page footers helped reinforce authorship and provided easy access to contact information.

### Sharing & Reflection

The final product is an interactive Streamlit app that can be shared as a live web app or embedded in Canvas. Users can explore the data, interact with visualizations, and gain insights at their own pace. This approach not only communicates the main findings but also empowers users to ask their own questions of the data, making the story both informative and engaging.


