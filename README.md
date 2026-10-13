## Questionbank Forge

Questionbank Forge is software for teachers that makes building custom worksheets quicker and easier.

It takes existing maths and science worksheet PDFs and splits them into individual questions, saving each one as an image along with the information needed to find it again. Once a set of labels has been created (topic, difficulty and other details), AI is used to label the questions automatically. Teachers can then search the question bank and pinpoint specific problem areas or difficulty levels within a topic, and put together a worksheet of just the questions their class needs.

Teachers will use it through a React web application, so it's easy to use from any computer on a school-approved network.

## How to run

1. Create a virtual environment and install the dependencies (`pymupdf`, `Pillow`):
   ```bash
   python -m venv .venv
   source .venv/Scripts/activate   # Windows (Git Bash); on Mac/Linux use: source .venv/bin/activate
   pip install -r requirements.txt
   ```
2. Create your local settings from the examples. The real `config.py` and `utility.py` are git-ignored because they point at specific worksheet sources:
   ```bash
   copy config.example.py config.py
   copy utility.example.py utility.py
   ```
3. Put your worksheet PDFs in `pdf_folder/` (contents are git-ignored).
4. Edit `config.py` with the layout values for your PDFs (left margin, header/footer cutoff, question marker). `printer.py` prints each word's position to help you measure them.
5. Edit `utility.py` to set which source flag is `True` and point `pdf_path` / `root` at your PDFs.
6. Run `python main.py`. Question images are written to `images/<worksheet name>/`.

## Development diary (Version control with Git/GitHub)
30/09:
- Downloaded all the worksheets of a specific type and opened them with the PyMuPDF library to extract the text. The question papers are proper text PDFs (minus the images), but the answers are handwritten, so they are just an image.(ignored for now)
- Separated the worksheets by question by printing the properties of every word, then used the position of each question number to isolate the questions. Picked out the attributes that were identical across question numbers, and used them to guard against mistaking other text for a new question.
- Built the splitter and ran it across a worksheet to check the output, but one question was missing. This was due to inconsistent labelling in the PDF ("marks" instead of "mark" on question 11), so that possibility was added to the conditions in case it came up again.
- Edited the splitter to work on multiple types of worksheets. Removed some conditions, as the layouts were quite different. The conditions are fairly simple to edit for a new worksheet type, but the splitter is not universal. Removed the question ending check, as the start of the next question can be used instead.

07/10:
- Once a worksheet is split, each question is stored as a region (page number, top and bottom y-coordinates). Using PyMuPDF, the page is clipped to each region and rendered to a pixmap at 150 DPI.
- Questions that span more than one page are made up of several regions. These are stitched together vertically on a white canvas using Pillow, so each question ends up as a single PNG.
- The images are saved to a folder named after the worksheet (`images/<worksheet name>/question<n>.png`). This is for debugging, to check that the splitting and clipping are correct.
- Next: store the questions properly, with all the necessary information, instead of just saving images.

09/10:
- Added a `Question` dataclass in `models.py` to hold everything about a question in one place
- The splitter now returns a list of `Question` objects, instead of a list of regions. Moved the region-reshaping function (`format_data`) from the renderer into the splitter, so the renderer gets tidy data.
- Fixed how question numbers get stored. Before, the word that triggered the *next* question was saved, which could be wrong. Now the number is kept alongside the start position and used instead.
- The renderer fills in each question's image path, width and height when it saves the PNG. It also now returns every question image, where before it only returned the last one.
- Next: get the questions into a database.

11/10:
- Added `db.py`, which stores each question in a SQLite database (`questions.db`) using Python's built-in `sqlite3`. Each row holds the source PDF, question number, regions (as JSON) and the image path, with a `UNIQUE (source_pdf, number)` constraint so a question can't be saved twice. The table is wiped on every run during debugging.
- `main.py` now calls `export_to_db` for each worksheet after rendering.
- Fixed two bugs. SQLite can't store a `pathlib` `WindowsPath`, so the PDF path is converted to a string before saving. The `number` column had been created as `INTEGER`, which silently turned `"1."` into `1`. `CREATE TABLE IF NOT EXISTS` doesn't change an existing table, so the table has to be dropped and recreated. The column is now `TEXT`, which keeps the marker in case a PDF needs to be re-split.

13/10:
- Wrote the list of labels in `topics.py`. It covers Edexcel GCSE maths specification.
- Every subtopic has a name and a short description. The description says what the question asks the student to do, and how to tell it apart from similar subtopics. This is for the AI that will label the questions later.
- Kept a separate list of the subtopics that are Higher tier only.
- Added a `topics` table to the database. Categories and subtopics live in the same table, and each subtopic points at its category with `parent_id`. It also stores the description and whether the topic is Higher only.
- Added a `question_topics` table that links questions to topics. A question can have more than one topic.
- Wrote `seed_topic`, which fills the `topics` table from `topics.py` when the database is set up. It checks first that every Higher-only name matches a real subtopic, so a typo gets caught straight away.
- Turned on foreign keys in SQLite, so a link can't point at a question or topic that doesn't exist. Because of this the tables have to be dropped in the right order, links first.
- Each question now has an `idx`, which is its position in the worksheet (1, 2, 3...). The database uses `(source_pdf, idx)` to stop duplicates, where before it used the question number. Position is safer, as two questions could be printed with the same number within a worksheet.
- The splitter no longer imports its layout settings. They are passed in as a config, and `main.py` loops over every worksheet source in `SOURCES`. This means several worksheet types can be run in one go, each with its own settings.
- Image file names are now cleaned up, so characters that Windows doesn't allow at the end of a name (like `.` or `:`) are removed.
- Next: write script using Claude API to label questions with topics.

## Known limitations / Future plans
- The splitter is not universal, so each new worksheet type needs its conditions adjusting.
- Split the answer sheets per question too. They are handwritten images, so the text-based splitter can't read them. Plan: first try reusing the question regions on the answer PDF (exact same layout) or fall back to a vision model to find question numbers. Each answer image would then be linked to its question.
- Add the label columns (board, level, topic and so on) to the SQL database. Questions are already stored, but without labels.
- Use AI to label the questions automatically (topic, difficulty and so on) once the set of labels has been created.
- ADD if model disagrees with original folder label, flag it

- Build a React front end for teachers to use from computers on a school-approved network.
- Add filtering to the front end, so teachers can narrow the question bank down by topic, difficulty or problem area and build custom worksheets from the results.

## Important info
