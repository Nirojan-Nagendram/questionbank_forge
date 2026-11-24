# Development diary

A dated log of how Questionbank Forge was built. See the [README](README.md) for setup and an overview.

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

10/11:
- Added an empty question check to the validator. Any question whose text is blank, or contains only its number, is flagged along with that question number.
- Added split and merged question checks. A question with no marker in its text is flagged as split, and a question containing two or more markers is flagged as merged. To support these, `WorksheetReport` now also stores each question's number, text and regions as lists.
- Added a lost words check, which has been the most common error so far. The first approach compared the page height with the total height of the questions on it, but this was inconsistent. The check now looks for words that sit above the footer cutoff but outside every question region on their page, and flags them with the page and y-position. This required storing the full document on the worksheet report.

15/11:
- Generalised the validator patterns. Some of them (for example the blank check and the numbering chain) assumed the `1.` marker format, so other markers such as `1:` were not fully supported.
- Fixed a false positive in the lost words check, which occurred when question content sat slightly higher on the page than its marker. The check now compares the midpoint of each word with the question region rather than its top edge.
- Changed the counter and stripper functions in `validate.py` to work on whole lines instead of lists of words. Working on words made the marks pattern difficult to adjust.
- Reworked `is_sequential` so that the sequence resets when a 1 is found, as some worksheets restart their numbering but are still sequential.
- Applied the header cutoff in the splitter, so that header text is no longer included in a question.
- Added the `LAST_PAGE_FOOTER` option for PDFs whose final page ends with extra content, and applied it in both the splitter and the validator.
- Added an image check to the validator, which flags questions whose saved image is missing or shared with another question. This required storing image paths on the worksheet report.
- Extended the lost words check to respect the header and footer cutoffs, which removes further false positives.
- Moved shared functions into `helpers.py`.
- Shortened the lost words function to make it easier to read when debugging.
