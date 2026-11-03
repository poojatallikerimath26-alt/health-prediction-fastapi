# Task 2 test data and expected outcome

Enter exactly as given (dots in dates are accepted and converted to dd/mm/yyyy).

| # | Name | DOB | Email | Gluc | Hb | Chol | Expected | Why |
|---|---|---|---|---|---|---|---|---|
| 1 | Robyn Pears | 28.01.1960 | robyn@gmail.com | 232 | 13.5 | 180 | Saved | valid |
| 2 | John Hunter | 10.12.1990 | hunter@gmail | 94 | 15 | 200 | Rejected | email has no domain extension (.com etc.) |
| 3 | Darryl Tim | 12.11.1993 | timd@smh.com.au | 240 | 18.6 | 326 | Saved | valid |
| 4 | Peter Larry | 31.11.2001 | Larry@hotmail.com | 88 | 11.5 | 165 | Rejected | 31 November does not exist |
| 5 | Sam Kerr | 09.12.2006 | sam@news.com.au | 198 | 8.9 | 192 | Saved | valid |
| 6 | Robyn Pears | 28.01.1960 | robyn@gmail.com | 232 | 13.5 | 180 | Rejected | duplicate of row 1 |
| 7 | Madison XI | 12.09.1998 | madison@hotmail.com | 85 | 7.6 | 163 | Saved | valid |
| 8 | Kris Wu | 19.10.2030 | Kris.wu.gmail.com | 79 | 16.5 | 197 | Rejected | DOB in the future AND email has no @ (two errors) |
| 9 | Tenille Singh | 30.11.1991 | Tenille@yahoo.com | 101 | 15 | 310 | Saved | valid |
| 10 | Prem Kumar | 28.04.1990 | prem@telstra.com | 155 | 12.5 | 265 | Saved | valid |

Then: EDIT Darryl Tim's email to gokul@infocare.com, DELETE one record (e.g. Madison XI), and show the list again.
