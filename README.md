hours
=====

Description
-----------
Hours is a simple command line time tracker for invoicing written in Python. It tracks multiple clients, projects, etc. Hours can output CSV files for invoicing.

Functions
---------
Below is a summary of the functions that Hours can perform:

 * (n) Start new entry - Starts a new entry with the current time. If a clock is started, will automatically close it to begin new entry.
 * (c) Close entry - Closes clock if there is a clock open.
 * (e) Edit entry - Allows the user to edit an entry by line number.
 * (i) Create Invoice - Creates an invoice for uninvoiced lines for specified customer.
 * (p) Mark Invoice as Paid - Select an invoice to mark as paid.
 * (sa) Show all entries - Print all entries in CSV to screen
 * (su) Show un-invoiced entries - Print all un-invoiced entries to screen
 * (so) Show outstanding invoices - Print all un-paid invoices to screen
 * (sk) Search by keyword - Search entries by keyword
 * (sm) Search by month/year - Search entries by month and year
 * (si) Search by invoice number - Search entries by invoice number
 * (u) Re-import/Update CSV - Re-read CSV file from disk
 * (r) Re-sort and re-calculate all entries - Sort entries by date, and recalculate times and costs.
