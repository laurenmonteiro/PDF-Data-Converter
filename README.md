# PDF Data Converter
This program scrapes a given set of PDF files and returns a CSV file composed of cleaned data that has been aggregated and formatted to existing specifications. 

# How it Works
<ol>
  <li>PDFs are opened by the program and the data is cleaned.
    <ul>
      <li>Rows not containing data are removed.</li>
      <li>State names are converted to their respective two-letter abbreviations.</li>
      <li>Dates are uniformly formatted.</li>
    </ul>
  <li>The data is compiled in the order specified by the CSV headers and written to a CSV file.</li>
</ol>
