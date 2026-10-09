## Questionbank Forge

Questionbank Forge is software for teachers that makes building custom worksheets quicker and easier.

It takes existing maths and science worksheet PDFs and splits them into individual questions, saving each one as an image along with the information needed to find it again. Once a set of labels has been created (topic, difficulty and other details), AI is used to label the questions automatically. Teachers can then search the question bank and pinpoint specific problem areas or difficulty levels within a topic, and put together a worksheet of just the questions their class needs.

Teachers will use it through a React web application, so it's easy to use from any computer on a school-approved network.

## How to run

To be continued...

## Development diary (Version control with Git/GitHub)
30/09:
- Firstly I do- Downloaded all the worksheets of a specific type and opened them with the PyMuPDF library to extract the text. The question papers are proper text PDFs (minus the images), but the answers are handwritten, so they are just an image.
- Next I needed to separate the worksheets by question. I printed the properties of every word, then used the position of each question number to isolate the questions. I then picked out the attributes that were identical across question numbers, and used them to guard against mistaking other text for a new question.
- Built the splitter and ran it across a worksheet to check the output, but one question was missing. This was due to inconsistent labelling in the PDF ("marks" instead of "mark" on question 11), so I added that possibility to the conditions in case it came up again.
- Edited the splitter to work on multiple types of worksheets. I had to remove some conditions as the layouts were quite different. The conditions are fairly simple to edit for a new worksheet type, but the splitter is not universal. I removed the quesition ending check, as I can just use the start of the next question instead.

07/10:
- Once a worksheet is split, each question is stored as a region (page number, top and bottom y-coordinates). Using PyMuPDF, I clip the page to each region and render it to a pixmap at 150 DPI.
- Questions that span more than one page are made up of several regions. These are stitched together vertically on a white canvas using Pillow, so each question ends up as a single PNG.
- The images are saved to a folder named after the worksheet (`images/<worksheet name>/question<n>.png`). This is for debugging, so I can check that the splitting and clipping are correct.
- Next, I'm working on storing the questions properly, with all the necessary information, instead of just saving images.

## Known limitations / Future plans
- Currently unable to upload all required files, due to refactoring potential copyright concerns for an open project.
- The splitter is not universal, so each new worksheet type needs its conditions adjusting.
- Store the questions and their labels in an SQL database, instead of just saving images.
- Use AI to label the questions automatically (topic, difficulty and so on) once the set of labels has been created.
- Build a React front end for teachers to use from computers on a school-approved network.
- Add filtering to the front end, so teachers can narrow the question bank down by topic, difficulty or problem area and build custom worksheets from the results.

## Important info
