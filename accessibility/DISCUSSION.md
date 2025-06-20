<!-- Discussion Topic
Exploring the Accessibility of Election Maps

Purpose
This exercise aims to help you critically evaluate the accessibility of real-world visual data tools. You'll gain hands-on experience with assistive technology and develop a more inclusive lens when thinking about data visualization design.

Discussion Prompt
Find an interactive or static election map online (e.g., from a government website, news outlet, or civic tech organization). Using a screen reader, evaluate how accessible the map is for blind or low-vision users.

Describe your experience navigating the map with the screen reader.
Analyze the strengths and limitations of its accessibility:
What content is available to screen reader users, and what is missing?
How does the screen reader navigate the map—can you access meaningful information?
What improvements would you suggest?
Submit a video recording showing your screen reader in action.
Submit a video recording showing your screen reader in action.
Be sure to include the URL to the election map and mention the platform and screen reader you tested with.
(Optional) Use accessibility tools (e.g., WAVE, Axe DevTools, or browser inspectors) to supplement your analysis. -->

## Discussion: Accessibility Evaluation of the NYT 2024 Presidential Election Results Map

**Election Map URL:**  
https://www.nytimes.com/interactive/2024/11/05/us/elections/results-president.html

**Platform & Screen Reader Used:**  
(Please fill in your OS and screen reader, e.g., macOS with VoiceOver, or Windows with NVDA/JAWS.)

---

### Experience Navigating the Map with a Screen Reader

I evaluated the accessibility of the New York Times 2024 Presidential Election Results interactive map using a screen reader. My goal was to determine how effectively blind or low-vision users can access the election data presented on this page.

#### Strengths

- **Textual Summaries:** The page provides a significant amount of textual information, including national vote totals, electoral college counts, and state-by-state results. These are generally accessible to screen readers, allowing users to understand the overall outcome and key statistics.
- **Structured Headings:** The site uses headings to organize content, which helps with navigation via screen reader shortcuts.
- **Descriptive Links:** Many links to state-level results are labeled with the state name, making it easier to jump to specific state data.

#### Limitations

- **Map Visualization:** The interactive map itself is not accessible. The screen reader does not convey any information about the visual map, such as which states are colored for each candidate or the geographic distribution of results.
- **Data Tables:** While some data is available in text, much of the detailed precinct- or county-level data is only presented visually or in graphics, with no accessible table or alternative text.
- **Navigation Complexity:** The page contains many navigation elements, ads, and repeated content, which can make it difficult for screen reader users to quickly find the main results.
- **Live Updates:** If the map updates live, there is no ARIA live region or notification to alert screen reader users to changes.

#### Content Availability

- **Available:** National and state-level results, vote counts, and some summary statistics are accessible.
- **Missing:** Visual cues (such as color-coded states, margin shifts, and interactive map features) are not described or available in alternative formats.

#### Suggestions for Improvement

1. **Alternative Text for Maps:** Provide a text-based summary or data table that lists each state, its electoral votes, and the winning candidate, so users can access the same information as sighted users.
2. **ARIA Landmarks and Live Regions:** Use ARIA roles and live regions to help users navigate to main content and receive updates as results change.
3. **Skip Links:** Add skip links to allow users to bypass repetitive navigation and ads.
4. **Accessible Data Tables:** Offer downloadable or on-page tables with detailed results for all states and counties.
5. **Map Descriptions:** Include a summary description of the map's key takeaways (e.g., which regions flipped, notable trends).

---

### Conclusion

While the New York Times election results page provides accessible textual summaries and navigation for some key data, the interactive map and detailed visualizations are not accessible to screen reader users. Implementing the suggested improvements would make the election results more inclusive and ensure all users have equitable access to this important civic information.

*(Screen recording demonstrating the screen reader experience will be attached.)*

---

**References:**  
[NYT 2024 Presidential Election Results](https://www.nytimes.com/interactive/2024/11/05/us/elections/results-president.html)

