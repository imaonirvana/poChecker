# REFACTOR **DO NOT SCRIPT NOW**
# poChecker

![PyPI - Version](https://img.shields.io/pypi/v/polib)

**```poChecker```** - is a script that automatically checks ```.po``` files against standard rules.

## Installation

Install the current version with:

```shell
git clone https://github.com/imaonirvana/poChecker
```

Then install all requirements:

```shell
cd poChecker
```
```shell
pip3 install -r requirements.txt
```

___

*Note: If you already have **```poChecker```** on your device, download the latest version before using it:*

```shell
cd poChecker
```
```shell
git pull
```

## Usage

### How to run

To use the **```poChecker```** script, follow the format below in the command line:

```python3
python3 main.py -path "/home/user/directory"
```

Replace */home/user/directory* with the path to the directory containing your ```.po``` files that you want to check.

#### Optional Parameters:

+ ```-path```: Specifies the path to the directory containing the ```.po``` files for checking.

#### For example:

```python3
python3 main.py -path "/Users/imaonirvana/cs_CZ.UTF-8"
```

This command will process ```.po``` files in the specified directory and check them against standard rules, generating an output file with any errors found.

___

### Results

The results will be saved in an output files named *```all_errors.txt``` & ```duplicates.txt```*.

*Note:* If the file already exists, it will be overwritten.

You can view the results by opening the *```all_errors.txt```* file, which will contain any errors found during the checking process.

You can view the results by opening the *```all_errors.txt```* file, which will contain any errors found during the checking process. The file *```duplicates.txt```* will specifically contain information about duplicates.

#### For example:
```python
===========================================================================
Error in apps.po, line 2757:
Description: Round bracket and $ translation mismatch
Original: 'User No. $(duress)'
Translated: 'Αριθμός χρήστη $(υποχρεωτική)'
===========================================================================

===========================================================================
Error in apps.po, line 2809:
Description: Duplicate string found
Original: 'High Wire'
===========================================================================

===========================================================================
Error in interactive.po, line 0:
Description: Error processing file
Original: 'Syntax error in po file (line 1)'
===========================================================================
```

### Line Endings Format

The **```poChecker```** script includes functionality to standardize line endings across all files to *Unix* format *(LF)*. This is done to ensure consistency and avoid potential cross-platform compatibility issues.

When the script processes files, it automatically converts line endings to the *Unix* format, which uses *LF (Line Feed)*. This ensures that the checked files adhere to a consistent line endings convention.

## Rules

### Rule 1

#### Description:

Check capital letters in the first character, excluding numbers and symbols.

#### Example:

```python
===========================================================================
Error in frontend.po, line 103:
Description: Capitalization mismatch
Original: 'Minutes'
Translated: 'minut'
===========================================================================
```

### Rule 2

#### Description:

Check single quotes in the translated string.

#### Example:

```python
===========================================================================
Error in apps.po, line 258:
Description: Odd number of single quotes
Original: 'Video on demand being viewed for %s (camera %s)'
Translated: 'Προβολή βίντεο κατ' απαίτηση για %s (κάμερα %s)'
===========================================================================
```

### Rule 3

#### Description:

Check % translation.

#### Example:

```python
===========================================================================
Error in api.po, line 186:
Description: % translation mismatch
Original: 'Remove Installers by ids %2'
Translated: 'Κατάργηση προγραμμάτων εγκατάστασης 2%'
===========================================================================
```

### Rule 4

#### Description:

Check tilde translation.

#### Example:

```python
===========================================================================
Error in xml.po, line 403:
Description: Tilde translation found
Original: 'Location: ~location~'
Translated: 'Emplacement: ~emplacement~'
===========================================================================
```

### Rule 5

#### Description:

Check translate words inside the "round brackets" and with $ before them.

#### Example:

```python
===========================================================================
Error in xml.po, line 668:
Description: Round bracket and $ translation mismatch
Original: '[112] Activates Output $(output)'
Translated: '[112] Ενεργοποιεί την έξοδο $(έξοδος)'
===========================================================================
```

### Rule 6

#### Description:

Check double quotes, excluding those within square brackets.

#### Example:

```python
===========================================================================
Error in api.po, line 402:
Description: Double quotes should be replaced with single quotes
Original: ''%value%' is not less than or equal to '%max%''
Translated: 'Το "%value%" δεν είναι μικρότερο ή ίσο με το "%max%"'
===========================================================================
```

### Rule 7

#### Description:

Check duplicate strings.

#### Example:

```python
===========================================================================
Error in frontend.po, line 1688:
Description: Duplicate string found
Original: 'All-Notification'
===========================================================================
```

## Customizing Ignore Phrases

You can utilize the *```ignore_phrases.py```* file. This file allows you to define phrases that, when present in the ```.po``` files, will not trigger duplicate error warnings. These phrases typically represent strings that should not be translated.

#### Structure of *```ignore_phrases.py```*

The *```ignore_phrases.py```* file is organized into sections, such as:

+ PowerManage
+ Panels & Panel Families
+ Devices & etc.
+ Roles
+ Communication & Protocols 
+ Locales 
+ Countries 
+ Abbreviation 
+ Metric 
+ Variables
+ Errors, troubles & notice
+ Masks 
+ Numeric options 
+ Options
+ Tunes 
+ Other 

Each section contains a list of phrases that are exempt from the duplicate checking process.

## Bug Reports and Feature Requests

If you encounter any bugs or have suggestions for new features, please feel free to contact me in Telegram or Teams. I appreciate your feedback and contributions to improve **```poChecker```**.

[Telegram](https://t.me/imaonirvana "Telegram") | [MS Teams](https://teams.microsoft.com/ "MS Teams") *(contact Dmytro Dudnyk)*
