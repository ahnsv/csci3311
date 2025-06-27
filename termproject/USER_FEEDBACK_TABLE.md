## User Feedback Examples for Slides 5-9

This document provides detailed, table-formatted examples of user feedback for your College Affordability Dashboard evaluation. Each table represents a different user persona.

---

### **User 1: The Computer Science Student**

| Challenge                                                                                             | Result                                                                                                                              | Solution                                                                                                   |
| ----------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------- |
| The filter for "School Type" (Public/Private) was a dropdown menu that only allowed for one selection at a time. | The user was unable to compare public and private school costs on the same chart simultaneously, which they expected to be able to do. | Change the filter from a single-select dropdown to a multi-select checkbox group to allow for direct comparison. |

---

### **User 2: The Graphic Designer (UX Background)**

| Challenge                                                                                                       | Result                                                                                                                                                           | Solution                                                                                                                                            |
| --------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------- |
| The main chart used colors for different data series (e.g., tuition, fees, housing) that were not colorblind-safe and had poor contrast. | The user found it difficult to distinguish between the lines on the chart and noted that this would be an accessibility issue for many users. | 1.  Update the color palette to be WCAG AA compliant.<br>2. Add patterns (e.g., dashed lines, dotted lines) as another visual differentiator. |

---

### **User 3: The Family Member (Limited Tech Expertise)**

| Challenge                                                                                             | Result                                                                                                                                                           | Solution                                                                                                                                                       |
| ----------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Key terms like "Net Price," "Sticker Price," and "Cost of Attendance" were used without any explanation. | The user was confused by the terminology and misinterpreted the data, thinking the "Net Price" was the only cost they would need to worry about. | Add small info icons `(i)` next to key terms. On hover, these icons will display a tooltip with a simple, clear definition of the term. |

---

### **User 4: The Non-Technical Classmate**

| Challenge                                                                                                | Result                                                                                                                                                               | Solution                                                                                                                                                               |
| -------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| The dashboard loaded with a dense, statewide view showing data for all 50 states, which was overwhelming. | The user felt lost and didn't know where to start. They said, "I don't know what I'm even looking at," and didn't interact much with the filters. | Change the default view to focus on a single, national average. Add a clear call-to-action like "Select a state to begin exploring" to guide the user's first interaction. |

---

### **User 5: The High School Guidance Counselor**

| Challenge                                                                                         | Result                                                                                                                                                                            | Solution                                                                                                                                                                                          |
| ------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| The "Return on Investment" (ROI) visualization was a single chart that couldn't be filtered by major or field of study. | The dashboard failed to answer the user's most critical question: "Which majors provide the best ROI?" The user stated the tool was "not specific enough to be useful for student advising." | Add a new filter to the ROI visualization that allows users to select a specific field of study (e.g., Engineering, Arts, Business), making the data far more actionable for career planning. |

---

### **Summary of Proposed Changes**

This table consolidates the individual feedback into a prioritized action plan.

| Priority | Proposed Change                                                 | Category             | Justification                                                                |
| -------- | --------------------------------------------------------------- | -------------------- | ---------------------------------------------------------------------------- |
| **High** | Add a filter for "field of study" to the ROI visualization      | New Feature / Data   | Addresses a core need for the key advisor persona (User 5).                  |
| **High** | Add info icons with tooltips for key terms (e.g., "Net Price")  | Content / UX         | Prevents major confusion for non-expert users (User 3).                      |
| **High** | Change "School Type" filter to multi-select checkboxes          | UI / UX              | Enables critical comparison functionality requested by technical users (User 1). |
| **Medium** | Change default view to a national average with a call-to-action | UI / UX              | Reduces initial cognitive load and guides new users (User 4).                |
| **Medium** | Update chart color palette to be WCAG compliant                 | Accessibility / UI   | Ensures the dashboard is usable for visually impaired users (User 2).        | 