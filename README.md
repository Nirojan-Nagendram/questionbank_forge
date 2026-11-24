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
| `LOST_WORDS` | Text above the footer cutoff that does not belong to any extracted question |
| `SPLIT_QUESTION` | A question has no marker in its text, so it has probably been cut into pieces |
| `MERGED_QUESTION` | A question contains two or more markers, so several questions have been joined |
| `EMPTY_QUESTION` | A question number was found but it has no body text |
| `NONE` | No known failures |

## Development diary (Version control with Git/GitHub)

The dated log of how the project was built, with the decisions and bugs along the way, is in [devlog.md](devlog.md).

## Known issues
- `utility.example.py` is out of date and needs to match the current `utility.py`, so a fresh clone will not run as described in "How to run".
- The stripped question numbers are recalculated in several places (the validator and renderer). They should be computed once, when the `Question` is created, and stored as a field on the class. This would also remove the repeated `strip_number` calls in `validate.py`.
- marks pattern currently checks for "marks)" rather than the marks number, Strip chain function would be simpler (identical run method) if it used the number ie. "(3 marks)" = "3"
- validator and splitter use different methods of cutting footers one takes it away from page height other just find footer point and cuts it. Pick one and make it universal.

## Future plans
- The splitter is not universal, so each new worksheet type needs its conditions adjusting.
- Split the answer sheets per question too. They are handwritten images, so the text-based splitter cannot read them. The plan is to first try reusing the question regions on the answer PDF (which has the same layout), and to fall back to a vision model to find question numbers. Each answer image would then be linked to its question.
- Add the label columns (board, level, topic and so on) to the SQL database. Questions are already stored, but without labels.
- Use AI to label the questions automatically (topic, difficulty and so on) once the set of labels has been created.
- Flag any question where the model's label disagrees with the label of the folder it came from.
- Build a React front end for teachers to use from computers on a school-approved network.
- Add filtering to the front end, so that teachers can narrow the question bank down by topic, difficulty or problem area and build custom worksheets from the results.
