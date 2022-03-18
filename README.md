<!-- Add banner here -->

# Data Science Job Detective

<!-- Add buttons here -->

<!-- Describe your project in brief -->
Getting your dream Data Science Job is a great motivation for developing a Data Science Roadmap. How do you develop a Roadmap without knowing the relevant skills and tools to Learn. In this project, I will explore over 800 Data Science Job postings in Canada. The data used was collected from postings on Glassdoor and Indeed in early June, 2021.

Link to [Medium] - (https://medium.com/@Olohireme/job-skills-extraction-from-data-science-job-posts-38fd58b94675) 

# Table of contents

<!-- After you have introduced your project, it is a good idea to add a **Table of contents** or **TOC** as **cool** people say it. This would make it easier for people to navigate through your README and find exactly what they are looking for.

Here is a sample TOC(*wow! such cool!*) that is actually the TOC for this README. -->

- [Project Title](#data-science-job-detective)
- [Table of contents](#table-of-contents)
- [Installation](#installation)
- [Usage](#usage)
- [Demo](#footer)

# Installation
[(Back to top)](#table-of-contents)

```pip install requirements.txt ```

# Usage
[(Back to top)](#table-of-contents)

<!-- This is optional and it is used to give the user info on how to use the project after installation. This could be added in the Installation section also. -->
- Stage 1: Scraping Data using selenium - Run glassdoor.py and indeed.py to scrape jobs.
- Stage 2: Performed Exploratory Data analysis in EDA.ipynb
- Stage 3: Performed Rule Based Skill Extraction using Spacy in skill_extraction.ipynb
- Stage 4: Training and testing skill extraction LSTM model in job_skills_prediction.ipynb
- Stage 5: Use saved LSTM and Rule-Based model to predict unseen text (i.e. Text that was not in the dataset) in job_skills_extraction_pipeline.ipynb
- Stage 6: Streamlit deployment code in  deploy.py

To run locally - `streamlit run deploy.py`


# Demo 
[(Back to top)](#table-of-contents)


You can find the [Demo](https://share.streamlit.io/remeajayi/ds-job-detective/main/deploy.py) here.


Leave a star in GitHub, give a clap in Medium and share this guide if you found this helpful.

<!-- Add the footer here -->

<!-- ![Footer](https://github.com/navendu-pottekkat/awesome-readme/blob/master/fooooooter.png) -->
