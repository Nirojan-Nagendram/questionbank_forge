## Questionbank Forge

Questionbank Forge is software for teachers that makes building custom worksheets quicker and easier.

It takes existing maths and science worksheet PDFs and splits them into individual questions, saving each one as an image along with the information needed to find it again. Once a set of labels has been created (topic, difficulty and other details), AI is used to label the questions automatically. Teachers can then search the question bank, pinpoint specific problem areas or difficulty levels within a topic, and put together a worksheet of only the questions a class needs.

The software is intended to be used through a React web application, so that it is accessible from any computer on a school-approved network.

## How to run

1. Create a virtual environment and install the dependencies (`pymupdf`, `Pillow`):
   ```bash
   python -m venv .venv
   source .venv/Scripts/activate   # Windows (Git Bash); on Mac/Linux use: source .venv/bin/activate
   pip install -r requirements.txt
   ```
2. Create the local settings file from the example. The real `utility.py` is git-ignored because it points at specific worksheet sources:
   ```bash
   cp utility.example.py utility.py   # Windows (Command Prompt): copy utility.example.py utility.py
   ```
3. Place the worksheet PDFs in `pdf_folder/` (its contents are git-ignored).
4. Edit `SOURCES` in `utility.py`. Each entry represents one worksheet type:
   - `root` is the folder holding its PDFs. Subfolders are searched too, and any folder called `answers` is skipped.
   - The layout values (left margin, header/footer cutoff, question marker and so on) are described at the top of the file. `print_page_details` in `helpers.py` prints the position of each word to help measure them.
   - `SKIP_PAGE_ONE` ignores the first page of each PDF, for worksheets that begin with a cover sheet.
   - `patterns` defines the regular expressions that the validator uses to count the questions in each PDF (see "Validation" below).
   - Set `enabled` to `False` for any source that should not be processed.
5. Run `python main.py`. Every enabled source is processed: question images are written to `images/<worksheet name>/`, each worksheet is validated, and the questions are saved to `questions.db`.

## Validation

`validate.py` checks that each worksheet has been split correctly. The question numbers found in the PDF text are compared with the numbers of the questions the splitter extracted. Two patterns are used, as a single method could miss a question that is labelled unusually:

- `numbering` counts lines that begin with a question number (for example `1.`).
- `marks` counts the "(Total x marks)" lines, one per question.

Each check returns a flag, and a `WorksheetReport` (defined in `models.py`) stores the result for the worksheet. The failure modes are:

| Flag | Meaning |
| --- | --- |
| `MISSING_QUESTION` | A question number appears in the PDF but was not extracted |
| `EXTRA_QUESTION` | A question was extracted that does not appear in the PDF |
| `PDF_NON-SEQUENTIAL` | The numbers found in the PDF are not in order (1, 2, 3...) |
| `EXTRACTED_NON-SEQUENTIAL` | The extracted numbers are not in order |
| `NONE` | No known failures |

`SPLIT_QUESTION`, `MERGED_QUESTION` and `EMPTY_QUESTION` are defined but do not have checks yet.

## Development diary (Version control with Git/GitHub)
30/09:
- Downloaded all the worksheets of a specific type and opened them with the PyMuPDF library to extract the text. The question papers are text-based PDFs (apart from the images), but the answers are handwritten, so they are only an image. These were ignored for now.
- Separated the worksheets into questions by printing the properties of every word, then used the position of each question number to isolate the questions. The attributes that were identical across question numbers were identified and used as conditions, which guard against mistaking other text for a new question.
- Built the splitter and ran it across a worksheet to check the output, but one question was missing. The cause was inconsistent labelling in the PDF ("marks" instead of "mark" on question 11), so that variation was added to the conditions in case it occurred again.
- Edited the splitter to work on multiple types of worksheet. Some conditions were removed, as the layouts were quite different. The conditions are simple to edit for a new worksheet type, but the splitter is not universal. The question-ending check was removed, as the start of the next question can be used instead.

07/10:
- Once a worksheet is split, each question is stored as a region (page number, top and bottom y-coordinates). Using PyMuPDF, the page is clipped to each region and rendered to a pixmap at 150 DPI.
- Questions that span more than one page are made up of several regions. These are stitched together vertically on a white canvas using Pillow, so each question ends up as a single PNG.
- The images are saved to a folder named after the worksheet (`images/<worksheet name>/question<n>.png`). This is for debugging, to check that the splitting and clipping are correct.
- Next: store the questions properly, with all the necessary information, instead of only saving images.

09/10:
- Added a `Question` dataclass in `models.py` to hold everything about a question in one place.
- The splitter now returns a list of `Question` objects instead of a list of regions. The region-reshaping function (`format_data`) was moved from the renderer into the splitter, so the renderer receives tidy data.
- Fixed how question numbers are stored. Previously, the word that triggered the *next* question was saved, which could be wrong. The number is now kept alongside the start position and used instead.
- The renderer fills in each question's image path, width and height when it saves the PNG. It also now returns every question image, where previously it only returned the last one.
- Next: store the questions in a database.

11/10:
- Added `db.py`, which stores each question in a SQLite database (`questions.db`) using Python's built-in `sqlite3`. Each row holds the source PDF, question number, regions (as JSON) and the image path, with a `UNIQUE (source_pdf, number)` constraint so that a question cannot be saved twice. The table is wiped on every run during debugging.
- `main.py` now calls `export_to_db` for each worksheet after rendering.
- Fixed two bugs. SQLite cannot store a `pathlib` `WindowsPath`, so the PDF path is converted to a string before saving. The `number` column had been created as `INTEGER`, which silently turned `"1."` into `1`. `CREATE TABLE IF NOT EXISTS` does not change an existing table, so the table had to be dropped and recreated. The column is now `TEXT`, which keeps the marker in case a PDF needs to be re-split.

13/10:
- Wrote the list of labels in `topics.py`, covering the Edexcel GCSE maths specification.
- Every subtopic has a name and a short description. The description states what the question asks the student to do and how to tell it apart from similar subtopics. This is intended for the AI that will label the questions later.
- Kept a separate list of the subtopics that are Higher tier only.
- Added a `topics` table to the database. Categories and subtopics share the same table, and each subtopic points at its category with `parent_id`. The table also stores the description and whether the topic is Higher only. This structure allows the topics to be listed first, followed by only the relevant subtopics.
- Added a `question_topics` table that links questions to topics. A question can have more than one topic.
- Wrote `seed_topic`, which fills the `topics` table from `topics.py` when the database is set up. It first checks that every Higher-only name matches a real subtopic, so a typo is caught immediately.
- Turned on foreign keys in SQLite, so a link cannot point at a question or topic that does not exist. As a result, the tables must be dropped in the correct order, links first.
- Each question now has an `idx`, which is its position in the worksheet (1, 2, 3...). The database uses `(source_pdf, idx)` to prevent duplicates, where previously it used the question number. Position is safer, as two questions could be printed with the same number within a worksheet.
- The splitter no longer imports its layout settings. They are passed in as a config, and `main.py` loops over every worksheet source in `SOURCES`. This allows several worksheet types to be run together, each with its own settings.
- Image file names are now cleaned up, so characters that Windows does not allow at the end of a name (such as `.` or `:`) are removed.
- Next: write a script using the Claude API to label questions with topics.

14/10:
- Changed the inserts to `INSERT OR IGNORE`. Duplicates are now skipped without needing to delete the tables, so the program can be re-run safely.
- Fixed a foreign key failure on re-runs. When an insert was ignored, no new row id was returned (it defaulted to 0), so the link pointed at a row that did not exist.

16/10:
- Added `validate.py` to check that worksheets have been extracted correctly (see "Validation").
- Added `WorksheetReport` to `models.py` to store the details produced by the validator.
- Created flags for the common failure modes. Checks only raise a flag when it applies, for example the sequence check only runs on lists longer than one.
- Added multiple methods of detecting questions (question numbering and "marks" lines) to reduce the likelihood of a question being dropped unnoticed.
- Used lambda functions for one-off checks and list comprehensions for similar, simple lists.
- Remaining work: finish the checks list, fix the PDF sequence check, clean up the number stripping, and reduce unnecessary lambda functions for readability.
- The splitter needs to be made more robust. It currently fails on a line such as "Question *7." because of the marker before the question number.

29/10:
- Diagnosed the PDF sequence check failure. The PDF question numbers are never flattened: they are stored as a list per page, whereas the extracted numbers are already a flat list. The sequence check needs a flat list to work. The flattening was added inside the missing/extra question functions, but it should happen earlier, as the sequence check also depends on it. This would also be simpler, as the extracted numbers are already flat.

05/11:
- Reworked number extraction so that it takes an ordered list of regular expressions instead of being called repeatedly. `strip_chain` applies each expression to the output of the previous one and returns an integer, or `None` if any step fails to match. This keeps the cleaning rules in data rather than in nested calls, and makes a new rule a one-line addition.
- Used the chain to handle unexpected question markers such as `*10.`, where a leading symbol previously prevented the number from being recognised. `strip_chain` was moved into `utility.py` so that the validator and the renderer (which uses it to build safe image file names) share one implementation.
- Added a `SKIP_PAGE_ONE` option to each source's config, used by both the splitter and the validator. Cover sheets contain text such as dates and instructions that can match the question patterns, which produced false `EXTRA_QUESTION` and sequence failures.
09/11:
- Added a `text` field to the `Question` class so that the validator can detect empty questions. The text was already being extracted by the splitter, so it is now simply stored on the class, where it is easier to access.
- Resolved the issue of a number within the question text being counted as a second question number (for example, `2. 10 people bought an item` previously yielded both 2 and 10). The numbering chain now anchors on the start of the line before extracting the digits.

## Known issues
- `utility.example.py` is out of date and needs to match the current `utility.py` (for example, it does not include `strip_chain`), so a fresh clone will not run as described in "How to run".
- The stripped question numbers are recalculated in several places (the validator and renderer) They should be computed once, when the `Question` is created, and stored as a field on the class. This would also remove the repeated `strip_number` calls in `validate.py`.

## Known limitations / Future plans
- The splitter is not universal, so each new worksheet type needs its conditions adjusting.
- Split the answer sheets per question too. They are handwritten images, so the text-based splitter cannot read them. The plan is to first try reusing the question regions on the answer PDF (which has the same layout), and to fall back to a vision model to find question numbers. Each answer image would then be linked to its question.
- Add the label columns (board, level, topic and so on) to the SQL database. Questions are already stored, but without labels.
- Use AI to label the questions automatically (topic, difficulty and so on) once the set of labels has been created.
- Flag any question where the model's label disagrees with the label of the folder it came from.
- Build a React front end for teachers to use from computers on a school-approved network.
- Add filtering to the front end, so that teachers can narrow the question bank down by topic, difficulty or problem area and build custom worksheets from the results.
