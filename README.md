# Job Application Automation with Python and Playwright

Automate the job application process on Lever's website using Python and Playwright! This project provides a script to simplify job application submissions by filling out forms automatically, reducing repetitive tasks and saving time.

## Features

- Auto-fills resume and personal information fields.
- Responds to custom questions and equal employment opportunity questions.
- Optional manual review before final submission to ensure accuracy.
- Compatible with Chrome, Firefox, and WebKit browsers.

## Example Workflow

The script follows these main steps:

1. Opens the job application URL.
2. Clicks "Apply for this job".
3. Attaches your resume.
4. Auto-fills basic information, custom questions, and demographic questions.
5. Waits for manual review before final submission.


## How It Works

1. **Automated Job Application**: The script opens a job posting URL, simulates clicking the "Apply" button, and begins the application.
2. **Resume Upload and Form Filling**: It attaches a resume, fills out personal information fields (like name, email, and LinkedIn profile), and answers required questions.
3. **Custom Question Handling**: The script can answer custom questions based on saved responses or keywords found in questions.
4. **Equal Employment and Demographic Questions**: It completes equal employment questions and demographic surveys if present, selecting from options like dropdowns or checkboxes.
5. **Manual Review**: Before final submission, the script pauses, allowing users to review answers and submit manually if desired.

